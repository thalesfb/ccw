import pytest

from tcc_prototype.modeling.explanations import explain_logistic_rows
from tcc_prototype.modeling.experiment import _logistic_pipeline
from tcc_prototype.modeling.features import build_history_features
from test_baseline_experiment import _synthetic_interactions


def test_logistic_contributions_reconstruct_model_log_odds() -> None:
    modeled = build_history_features(_synthetic_interactions())
    feature_columns = [
        "item_id",
        "primary_skill_id",
        "prior_student_attempts",
        "prior_student_correct",
        "prior_student_accuracy",
        "prior_student_skill_attempts",
        "prior_student_skill_correct",
        "prior_student_skill_accuracy",
    ]
    model = _logistic_pipeline(seed=2026)
    model.fit(modeled[feature_columns], modeled["target"])

    explanations = explain_logistic_rows(model, modeled[feature_columns].head(2))

    assert len(explanations) == 2
    for row_index, explanation in enumerate(explanations):
        reconstructed = explanation["intercept"] + sum(
            contribution["contribution"]
            for contribution in explanation["contributions"]
        )
        expected = model.decision_function(
            modeled[feature_columns].iloc[[row_index]]
        )[0]
        assert reconstructed == pytest.approx(expected)
        assert explanation["log_odds"] == pytest.approx(expected)
        assert 0 <= explanation["probability"] <= 1
