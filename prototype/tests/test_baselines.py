import pandas as pd
import pytest

from tcc_prototype.modeling.baselines import (
    MultiSkillSmoothedProbabilityBaseline,
    SmoothedProbabilityBaseline,
    student_history_probability,
)


def test_group_baseline_smooths_known_groups_and_falls_back_to_global() -> None:
    train = pd.DataFrame(
        {
            "group": ["a", "a", "b", "b"],
            "target": [1, 1, 0, 0],
        }
    )
    model = SmoothedProbabilityBaseline(("group",), prior_strength=2.0).fit(train)

    predictions = model.predict_proba(pd.DataFrame({"group": ["a", "b", "new"]}))

    assert predictions.tolist() == [0.75, 0.25, 0.5]


def test_multiskill_baseline_uses_every_mapped_skill_without_row_explosion() -> None:
    train = pd.DataFrame(
        {
            "skill_ids": [["a"], ["a", "b"], ["b"], ["b"]],
            "target": [1, 1, 0, 0],
        }
    )
    model = MultiSkillSmoothedProbabilityBaseline(prior_strength=2.0).fit(train)

    predictions = model.predict_proba(
        pd.DataFrame({"skill_ids": [["a"], ["b"], ["a", "b"], ["unseen"]]})
    )

    assert predictions[0] > predictions[2] > predictions[1]
    assert predictions[3] == pytest.approx(0.5)


def test_student_history_baseline_remains_available_for_held_out_students() -> None:
    frame = pd.DataFrame(
        {
            "prior_student_correct": [0, 3],
            "prior_student_attempts": [0, 4],
        }
    )

    predictions = student_history_probability(
        frame,
        prior_strength=2.0,
        global_probability=0.5,
    )

    assert predictions.tolist() == [0.5, pytest.approx(4 / 6)]
