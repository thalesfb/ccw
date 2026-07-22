import pandas as pd

from tcc_prototype.modeling.candidate import build_random_forest_pipeline


def test_random_forest_candidate_returns_deterministic_probabilities() -> None:
    frame = pd.DataFrame(
        {
            "item_id": ["i1", "i2", "i1", "i2", "i3", "i3"],
            "primary_skill_id": ["fractions", "ratio"] * 3,
            "prior_student_attempts": [0, 1, 2, 3, 4, 5],
            "prior_student_correct": [0, 1, 1, 2, 2, 3],
            "prior_student_accuracy": [0.5, 2 / 3, 0.5, 0.6, 0.5, 4 / 7],
            "prior_student_skill_attempts": [0, 0, 1, 1, 2, 2],
            "prior_student_skill_correct": [0, 0, 1, 0, 1, 1],
            "prior_student_skill_accuracy": [0.5, 0.5, 2 / 3, 1 / 3, 0.5, 0.5],
        }
    )
    target = [0, 1, 1, 0, 1, 0]

    first = build_random_forest_pipeline(seed=2026, n_estimators=25, min_samples_leaf=1)
    second = build_random_forest_pipeline(seed=2026, n_estimators=25, min_samples_leaf=1)
    first.fit(frame, target)
    second.fit(frame, target)

    first_probability = first.predict_proba(frame)[:, 1]
    second_probability = second.predict_proba(frame)[:, 1]

    assert first_probability.tolist() == second_probability.tolist()
    assert all(0 <= value <= 1 for value in first_probability)
