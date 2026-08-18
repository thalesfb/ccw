"""Leakage-safe features derived from information available before each response."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

REQUIRED_COLUMNS = {
    "student_id",
    "item_id",
    "skill_ids",
    "interaction_order",
    "correct",
    "source_dataset",
    "source_row_id",
}


def normalize_skill_ids(value: object) -> tuple[str, ...]:
    """Return a deterministic non-empty tuple containing every mapped skill."""

    if isinstance(value, str):
        values = [value]
    elif isinstance(value, Iterable):
        values = [str(skill) for skill in value]
    else:
        values = []
    skills = tuple(sorted({skill.strip() for skill in values if skill.strip()}))
    if not skills:
        raise ValueError("each interaction must have at least one skill")
    return skills


def skill_signature(value: object) -> str:
    """Encode the complete mapped skill set without selecting a primary skill."""

    return "||".join(normalize_skill_ids(value))


def build_history_features(interactions: pd.DataFrame) -> pd.DataFrame:
    """Create pre-response history features and retain current correctness only as target."""

    missing = sorted(REQUIRED_COLUMNS.difference(interactions.columns))
    if missing:
        raise ValueError("missing interaction columns: " + ", ".join(missing))

    frame = interactions.copy()
    frame["student_id"] = frame["student_id"].astype(str)
    frame["item_id"] = frame["item_id"].astype(str)
    frame["source_row_id"] = frame["source_row_id"].astype(str)
    frame["skill_ids"] = frame["skill_ids"].map(normalize_skill_ids)
    frame["skill_signature"] = frame["skill_ids"].map("||".join)
    frame["target"] = frame["correct"].astype(int)
    if not frame["target"].isin([0, 1]).all():
        raise ValueError("correct must map to a binary target")

    frame = frame.sort_values(
        ["student_id", "interaction_order", "source_row_id"], kind="mergesort"
    ).reset_index(drop=True)

    student_group = frame.groupby("student_id", sort=False, dropna=False)
    frame["prior_student_attempts"] = student_group.cumcount()
    frame["prior_student_correct"] = (
        student_group["target"].cumsum() - frame["target"]
    ).astype(int)
    frame["prior_student_accuracy"] = (
        frame["prior_student_correct"] + 1.0
    ) / (frame["prior_student_attempts"] + 2.0)

    skillset_group = frame.groupby(
        ["student_id", "skill_signature"], sort=False, dropna=False
    )
    frame["prior_student_skillset_attempts"] = skillset_group.cumcount()
    frame["prior_student_skillset_correct"] = (
        skillset_group["target"].cumsum() - frame["target"]
    ).astype(int)
    frame["prior_student_skillset_accuracy"] = (
        frame["prior_student_skillset_correct"] + 1.0
    ) / (frame["prior_student_skillset_attempts"] + 2.0)

    return frame
