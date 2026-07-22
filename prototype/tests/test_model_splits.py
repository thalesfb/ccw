import pandas as pd

from tcc_prototype.modeling.splits import (
    assign_cold_start_split,
    assign_temporal_split,
)


def _interactions(students: int = 12, rows_per_student: int = 10) -> pd.DataFrame:
    rows = []
    for student in range(students):
        for order in range(rows_per_student):
            rows.append(
                {
                    "student_id": f"s{student}",
                    "interaction_order": order,
                    "source_row_id": f"{student}-{order}",
                }
            )
    return pd.DataFrame(rows)


def test_cold_start_split_keeps_students_disjoint_and_is_deterministic() -> None:
    interactions = _interactions()

    first = assign_cold_start_split(interactions, seed=2026)
    second = assign_cold_start_split(interactions, seed=2026)

    assert first["split"].tolist() == second["split"].tolist()
    groups = {
        name: set(first.loc[first["split"] == name, "student_id"])
        for name in ("train", "validation", "test")
    }
    assert groups["train"]
    assert groups["validation"]
    assert groups["test"]
    assert groups["train"].isdisjoint(groups["validation"])
    assert groups["train"].isdisjoint(groups["test"])
    assert groups["validation"].isdisjoint(groups["test"])


def test_temporal_split_preserves_order_within_each_student() -> None:
    interactions = _interactions(students=2, rows_per_student=10)

    split = assign_temporal_split(interactions)

    for _, group in split.groupby("student_id", sort=False):
        labels = group.sort_values("interaction_order")["split"].tolist()
        assert labels == [
            "train",
            "train",
            "train",
            "train",
            "train",
            "train",
            "train",
            "validation",
            "test",
            "test",
        ]


def test_temporal_split_excludes_students_without_minimum_history() -> None:
    interactions = _interactions(students=1, rows_per_student=2)

    split = assign_temporal_split(interactions, minimum_interactions=3)

    assert split.empty
