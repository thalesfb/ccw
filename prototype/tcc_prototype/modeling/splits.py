"""Deterministic split strategies for educational interaction data."""

from __future__ import annotations

import hashlib

import pandas as pd


def _validate_fractions(
    train_fraction: float,
    validation_fraction: float,
    test_fraction: float,
) -> None:
    values = (train_fraction, validation_fraction, test_fraction)
    if any(value <= 0 or value >= 1 for value in values):
        raise ValueError("all split fractions must be between zero and one")
    if abs(sum(values) - 1.0) > 1e-9:
        raise ValueError("split fractions must sum to one")


def assign_cold_start_split(
    frame: pd.DataFrame,
    *,
    seed: int = 2026,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
    test_fraction: float = 0.15,
) -> pd.DataFrame:
    """Assign whole students to train, validation, or test sets."""

    _validate_fractions(train_fraction, validation_fraction, test_fraction)
    if "student_id" not in frame.columns:
        raise ValueError("student_id is required for a cold-start split")

    result = frame.copy()
    students = sorted(result["student_id"].astype(str).unique())
    if len(students) < 3:
        raise ValueError("at least three students are required for disjoint splits")

    ranked = sorted(
        students,
        key=lambda student: hashlib.sha256(
            f"{seed}:{student}".encode("utf-8")
        ).hexdigest(),
    )
    train_count = max(1, int(len(ranked) * train_fraction))
    validation_count = max(1, int(len(ranked) * validation_fraction))
    if train_count + validation_count >= len(ranked):
        train_count = max(1, len(ranked) - 2)
        validation_count = 1

    assignments = {
        student: (
            "train"
            if index < train_count
            else "validation"
            if index < train_count + validation_count
            else "test"
        )
        for index, student in enumerate(ranked)
    }
    result["student_id"] = result["student_id"].astype(str)
    result["split"] = result["student_id"].map(assignments)
    return result


def assign_temporal_split(
    frame: pd.DataFrame,
    *,
    minimum_interactions: int = 3,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
    test_fraction: float = 0.15,
) -> pd.DataFrame:
    """Split each eligible student's history in chronological order."""

    _validate_fractions(train_fraction, validation_fraction, test_fraction)
    required = {"student_id", "interaction_order", "source_row_id"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError("missing temporal split columns: " + ", ".join(missing))
    if minimum_interactions < 3:
        raise ValueError("minimum_interactions must be at least three")

    ordered = frame.copy()
    ordered["student_id"] = ordered["student_id"].astype(str)
    ordered["source_row_id"] = ordered["source_row_id"].astype(str)
    ordered = ordered.sort_values(
        ["student_id", "interaction_order", "source_row_id"],
        kind="mergesort",
    )

    eligible = ordered.groupby("student_id")["student_id"].transform("size")
    ordered = ordered.loc[eligible >= minimum_interactions].copy()
    if ordered.empty:
        ordered["split"] = pd.Series(dtype="object")
        return ordered.reset_index(drop=True)

    labels = pd.Series(index=ordered.index, dtype="object")
    for _, group in ordered.groupby("student_id", sort=False):
        count = len(group)
        train_count = max(1, int(count * train_fraction))
        validation_count = max(1, int(count * validation_fraction))
        if train_count + validation_count >= count:
            validation_count = 1
            train_count = count - 2
        positions = list(group.index)
        labels.loc[positions[:train_count]] = "train"
        labels.loc[
            positions[train_count : train_count + validation_count]
        ] = "validation"
        labels.loc[positions[train_count + validation_count :]] = "test"

    ordered["split"] = labels
    return ordered.reset_index(drop=True)
