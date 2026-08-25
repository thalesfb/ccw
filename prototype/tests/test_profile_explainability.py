import pandas as pd
import pytest

from tcc_prototype.modeling.explanations import reconstruct_logistic_explanations
from tcc_prototype.modeling.experiment import run_baseline_experiment
from tcc_prototype.profiles import (
    ProfileConfigError,
    build_skill_profiles,
    validate_profile_config,
)


def _interactions(students: int = 18, rows: int = 12) -> pd.DataFrame:
    data = []
    for student in range(students):
        for order in range(rows):
            skills = (
                ["fractions", "ratio"]
                if order == 2
                else (["fractions"] if order % 2 == 0 else ["ratio"])
            )
            data.append(
                {
                    "student_id": f"s{student}",
                    "item_id": f"i{order % 5}",
                    "skill_ids": skills,
                    "interaction_order": order,
                    "correct": (student + order) % 3 != 0,
                    "source_dataset": "synthetic",
                    "source_row_id": f"{student}-{order}",
                }
            )
    return pd.DataFrame(data)


def _experiment_config() -> dict:
    return {
        "schema_version": "1.2.0-test",
        "eligibility": {"minimum_interactions_per_student": 3},
        "random_seeds": [2026, 1701, 31415],
        "splits": {
            "student_holdout": {
                "train_fraction": 0.7,
                "validation_fraction": 0.15,
                "test_fraction": 0.15,
            },
            "personalized_temporal": {
                "train_fraction": 0.7,
                "validation_fraction": 0.15,
                "test_fraction": 0.15,
            },
        },
        "evaluation_execution": {
            "classification_threshold": 0.5,
            "calibration_bins": 5,
            "smoothing_strengths": [1.0, 5.0],
            "logistic_regression": {
                "c_values": [0.1, 1.0],
                "max_iter": 500,
            },
            "hist_gradient_boosting": {
                "learning_rate_values": [0.1],
                "max_leaf_nodes_values": [15],
                "l2_regularization_values": [0.0],
                "max_iter": 20,
                "hash_features": 8,
            },
        },
        "reporting": {
            "skill_support": {
                "minimum_test_rows": 1,
                "minimum_test_students": 1,
            },
            "subgroup_audit": {"columns": []},
            "bootstrap": {"iterations": 20},
        },
    }


def test_profile_config_refuses_unfrozen_operational_choices() -> None:
    config = {
        "schema_version": "2.0.0-test",
        "probability_source": None,
        "minimum_student_skill_interactions": None,
        "ordinal_levels": {"enabled": False},
        "binary_alert": {"enabled": False},
    }

    with pytest.raises(ProfileConfigError, match="probability_source"):
        validate_profile_config(config)

    config["probability_source"] = "logistic_regression"
    with pytest.raises(ProfileConfigError, match="minimum_student_skill_interactions"):
        validate_profile_config(config)


def test_profile_uses_every_mapped_skill_without_claiming_mastery() -> None:
    predictions = pd.DataFrame(
        {
            "student_id": ["s1", "s1", "s2"],
            "skill_ids": [
                ["fractions", "ratio"],
                ["fractions"],
                ["ratio"],
            ],
            "source_row_id": ["r1", "r2", "r3"],
            "target": [1, 0, 1],
            "logistic_regression_probability": [0.8, 0.4, 0.7],
        }
    )

    profile = build_skill_profiles(
        predictions,
        probability_column="logistic_regression_probability",
        minimum_evidence=2,
    )

    fractions = profile.loc[
        (profile["student_id"] == "s1") & (profile["skill_id"] == "fractions")
    ].iloc[0]
    ratio = profile.loc[
        (profile["student_id"] == "s1") & (profile["skill_id"] == "ratio")
    ].iloc[0]

    assert fractions["evidence_count"] == 2
    assert fractions["mean_predicted_correct_probability"] == pytest.approx(0.6)
    assert fractions["observed_accuracy"] == pytest.approx(0.5)
    assert fractions["evidence_status"] == "reported"
    assert ratio["evidence_count"] == 1
    assert ratio["evidence_status"] == "insufficient_evidence"
    assert "level" not in profile.columns
    assert "primary_skill_id" not in profile.columns
    assert "not a measure of mastery" in fractions["interpretation_limit"]


def test_logistic_explanations_reconstruct_registered_test_predictions() -> None:
    interactions = _interactions()
    result = run_baseline_experiment(
        interactions,
        config=_experiment_config(),
        split_strategy="personalized_temporal",
        seed=2026,
    )

    reconstructed = reconstruct_logistic_explanations(
        interactions,
        splits=result.splits,
        predictions=result.predictions,
        selected_parameters=result.selected_parameters["logistic_regression"],
        seed=2026,
        explanation_rows=5,
        probability_tolerance=1e-12,
    )

    assert reconstructed.max_abs_probability_error <= 1e-12
    assert len(reconstructed.explanations) == 5
    for explanation in reconstructed.explanations:
        contribution_sum = explanation["intercept"] + sum(
            row["contribution"] for row in explanation["contributions"]
        )
        assert contribution_sum == pytest.approx(explanation["log_odds"], abs=1e-10)
        assert "source_row_id" in explanation
        assert "do not establish causal" in explanation["interpretation_limit"]
