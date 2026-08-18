import pandas as pd

from tcc_prototype.modeling.features import build_history_features


def _interactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "student_id": ["s1", "s1", "s1", "s2"],
            "item_id": ["i1", "i2", "i3", "i1"],
            "skill_ids": [
                ["fractions"],
                ["fractions"],
                ["ratio", "fractions"],
                ["fractions"],
            ],
            "interaction_order": [1, 2, 3, 1],
            "correct": [True, False, True, False],
            "source_dataset": ["synthetic"] * 4,
            "source_row_id": ["0", "1", "2", "3"],
        }
    )


def test_history_features_use_only_prior_responses() -> None:
    original = build_history_features(_interactions())
    changed = _interactions()
    changed.loc[2, "correct"] = False
    modified = build_history_features(changed)

    history_columns = [
        "prior_student_attempts",
        "prior_student_correct",
        "prior_student_accuracy",
        "prior_student_skillset_attempts",
        "prior_student_skillset_correct",
        "prior_student_skillset_accuracy",
    ]
    assert original.loc[2, history_columns].tolist() == modified.loc[2, history_columns].tolist()
    assert original.loc[2, "target"] == 1
    assert modified.loc[2, "target"] == 0


def test_history_features_preserve_complete_multiskill_context() -> None:
    modeled = build_history_features(_interactions())

    assert modeled.loc[2, "skill_ids"] == ("fractions", "ratio")
    assert modeled.loc[2, "skill_signature"] == "fractions||ratio"
    assert modeled.loc[0, "prior_student_accuracy"] == 0.5


def test_history_rate_prior_is_explicitly_configurable() -> None:
    modeled = build_history_features(
        _interactions(),
        virtual_successes=2.0,
        virtual_failures=1.0,
    )

    assert modeled.loc[0, "prior_student_accuracy"] == 2 / 3
    assert modeled.loc[0, "prior_student_skillset_accuracy"] == 2 / 3
    assert modeled.loc[1, "prior_student_accuracy"] == 3 / 4
