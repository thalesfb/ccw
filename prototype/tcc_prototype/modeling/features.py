"""Feature engineering using only information preceding each response."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

REQUIRED_COLUMNS = {
    "student_id",
    "item_id",
    "skill_ids",
    "interaction_order",
    "correct",
    "source_row_id",
}


def _primary_skill(value: object) -> str:
    if isinstance(value, str):
        skills = [value]
    elif isinstance(value, Iterable):
        skills = [str(skill) for skill in value if str(skill)]
    else:
        skills = []
    if not skills:
        raise ValueError("each interaction must have at least one skill")
    return sorted(set(skills))[0]


def build_history_features(interactions: pd.DataFrame) -> pd.DataFrame:
    """Create prior-history features without using the current response.

    The current response is retained only in ``target``. Laplace smoothing with
    one virtual success and one virtual failure yields a neutral 0.5 estimate
    for interactions without history.
    """

    missing = sorted(REQUIRED_COLUMNS.difference(interactions.columns))
    if missing:
        raise ValueError("missing interaction columns: " + ", ".join(missing))

    frame = interactions.copy()
    frame["student_id"] = frame["student_id"].astype(str)
    frame["item_id"] = frame["item_id"].astype(str)
    frame["source_row_id"] = frame["source_row_id"].astype(str)
    frame["primary_skill_id"] = frame["skill_ids"].map(_primary_skill)
    frame["target"] = frame["correct"].astype(int)
    frame = frame.sort_values(
        ["student_id", "interaction_order", "source_row_id"],
        kind="mergesort",
    ).reset_index(drop=True)

    student_group = frame.groupby("student_id", sort=False, dropna=False)
    frame["prior_student_attempts"] = student_group.cumcount()
    frame["prior_student_correct"] = (
        student_group["target"].cumsum() - frame["target"]
    ).astype(int)
    frame["prior_student_accuracy"] = (
        frame["prior_student_correct"] + 1.0
    ) / (frame["prior_student_attempts"] + 2.0)

    skill_group = frame.groupby(
        ["student_id", "primary_skill_id"], sort=False, dropna=False
    )
    frame["prior_student_skill_attempts"] = skill_group.cumcount()
    frame["prior_student_skill_correct"] = (
        skill_group["target"].cumsum() - frame["target"]
    ).astype(int)
    frame["prior_student_skill_accuracy"] = (
        frame["prior_student_skill_correct"] + 1.0
    ) / (frame["prior_student_skill_attempts"] + 2.0)

    return frame
