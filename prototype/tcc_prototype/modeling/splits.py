"""Deterministic split strategies for educational interaction data."""

from __future__ import annotations

import hashlib

import pandas as pd


def validate_split_fractions(
    train_fraction: float, validation_fraction: float, test_fraction: float
) -> None:
    values = (train_fraction, validation_fraction, test_fraction)
    if any(value <= 0 or value >= 1 for value in values):
        raise ValueError("all split fractions must be between zero and one")
    if abs(sum(values) - 1.0) > 1e-9:
        raise ValueError("split fractions must sum to one")


def filter_eligible_students(
    frame: pd.DataFrame, *, minimum_interactions: int
) -> pd.DataFrame:
    """Apply the pre-frozen interaction-count rule before partition generation."""

    if minimum_interactions < 1:
        raise ValueError("minimum_interactions must be positive")
    if "student_id" not in frame.columns:
        raise ValueError("student_id is required for eligibility filtering")
    student_ids = frame["student_id"].astype(str)
    counts = student_ids.groupby(student_ids).transform("size")
    return frame.loc[counts >= minimum_interactions].copy().reset_index(drop=True)


def assign_student_holdout_split(
    frame: pd.DataFrame,
    *,
    seed: int,
    train_fraction: float,
    validation_fraction: float,
    test_fraction: float,
) -> pd.DataFrame:
    """Assign whole students to train, validation, or test partitions."""

    validate_split_fractions(train_fraction, validation_fraction, test_fraction)
    if "student_id" not in frame.columns:
        raise ValueError("student_id is required for a student-holdout split")

    result = frame.copy()
    result["student_id"] = result["student_id"].astype(str)
    students = sorted(result["student_id"].unique())
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
    result["split"] = result["student_id"].map(assignments)
    return result


def assign_personalized_temporal_split(
    frame: pd.DataFrame,
    *,
    train_fraction: float,
    validation_fraction: float,
    test_fraction: float,
) -> pd.DataFrame:
    """Split each eligible student's interactions chronologically."""

    validate_split_fractions(train_fraction, validation_fraction, test_fraction)
    required = {"student_id", "interaction_order", "source_row_id"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError("missing temporal split columns: " + ", ".join(missing))

    ordered = frame.copy()
    ordered["student_id"] = ordered["student_id"].astype(str)
    ordered["source_row_id"] = ordered["source_row_id"].astype(str)
    ordered = ordered.sort_values(
        ["student_id", "interaction_order", "source_row_id"], kind="mergesort"
    )
    labels = pd.Series(index=ordered.index, dtype="object")
    for _, group in ordered.groupby("student_id", sort=False):
        count = len(group)
        if count < 3:
            raise ValueError(
                "eligible temporal students must have at least three interactions"
            )
        train_count = max(1, int(count * train_fraction))
        validation_count = max(1, int(count * validation_fraction))
        if train_count + validation_count >= count:
            train_count = count - 2
            validation_count = 1
        positions = list(group.index)
        labels.loc[positions[:train_count]] = "train"
        labels.loc[
            positions[train_count : train_count + validation_count]
        ] = "validation"
        labels.loc[positions[train_count + validation_count :]] = "test"
    ordered["split"] = labels
    return ordered.reset_index(drop=True)
