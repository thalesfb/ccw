import pandas as pd

from tcc_prototype.modeling.splits import (
    assign_personalized_temporal_split,
    assign_student_holdout_split,
    filter_eligible_students,
)


def _interactions(students: int = 12, rows_per_student: int = 12) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "student_id": f"s{student}",
                "interaction_order": order,
                "source_row_id": f"{student}-{order}",
            }
            for student in range(students)
            for order in range(rows_per_student)
        ]
    )


def test_student_holdout_split_is_deterministic_and_student_disjoint() -> None:
    interactions = _interactions()
    first = assign_student_holdout_split(
        interactions,
        seed=2026,
        train_fraction=0.70,
        validation_fraction=0.15,
        test_fraction=0.15,
    )
    second = assign_student_holdout_split(
        interactions,
        seed=2026,
        train_fraction=0.70,
        validation_fraction=0.15,
        test_fraction=0.15,
    )

    assert first["split"].tolist() == second["split"].tolist()
    groups = {
        name: set(first.loc[first["split"] == name, "student_id"])
        for name in ("train", "validation", "test")
    }
    assert groups["train"].isdisjoint(groups["validation"] | groups["test"])
    assert groups["validation"].isdisjoint(groups["test"])


def test_personalized_temporal_split_preserves_chronological_order() -> None:
    split = assign_personalized_temporal_split(
        _interactions(students=2),
        train_fraction=0.70,
        validation_fraction=0.15,
        test_fraction=0.15,
    )

    for _, group in split.groupby("student_id", sort=False):
        labels = group.sort_values(["interaction_order", "source_row_id"])["split"].tolist()
        assert labels == ["train"] * 8 + ["validation"] + ["test"] * 3


def test_eligibility_filter_is_applied_before_partition_generation() -> None:
    interactions = pd.concat(
        [
            _interactions(students=2, rows_per_student=4),
            _interactions(students=1, rows_per_student=2).assign(student_id="short"),
        ],
        ignore_index=True,
    )

    eligible = filter_eligible_students(interactions, minimum_interactions=3)

    assert "short" not in set(eligible["student_id"])
