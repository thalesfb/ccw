import pandas as pd

from tcc_prototype.modeling.features import build_history_features


def test_history_features_use_only_prior_responses() -> None:
    interactions = pd.DataFrame(
        {
            "student_id": ["s1", "s1", "s1", "s2"],
            "item_id": ["i1", "i2", "i3", "i1"],
            "skill_ids": [["fractions"], ["fractions"], ["ratio"], ["fractions"]],
            "interaction_order": [1, 2, 3, 1],
            "correct": [True, False, True, False],
            "source_row_id": ["0", "1", "2", "3"],
        }
    )

    modeled = build_history_features(interactions)
    s1 = modeled.loc[modeled["student_id"] == "s1"].reset_index(drop=True)

    assert s1["target"].tolist() == [1, 0, 1]
    assert s1["prior_student_attempts"].tolist() == [0, 1, 2]
    assert s1["prior_student_correct"].tolist() == [0, 1, 1]
    assert s1["prior_student_accuracy"].tolist() == [0.5, 2 / 3, 0.5]
    assert s1["prior_student_skill_attempts"].tolist() == [0, 1, 0]
    assert s1["prior_student_skill_correct"].tolist() == [0, 1, 0]


def test_history_features_choose_a_deterministic_primary_skill() -> None:
    interactions = pd.DataFrame(
        {
            "student_id": ["s1"],
            "item_id": ["i1"],
            "skill_ids": [["ratio", "fractions"]],
            "interaction_order": [1],
            "correct": [True],
            "source_row_id": ["0"],
        }
    )

    modeled = build_history_features(interactions)

    assert modeled.loc[0, "primary_skill_id"] == "fractions"
