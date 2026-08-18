import pandas as pd
import pytest

from tcc_prototype.modeling.evaluation import (
    calibration_intercept_slope,
    expected_calibration_error,
    paired_cluster_bootstrap_primary_differences,
    probability_metrics,
)


def test_probability_metrics_include_full_calibration_diagnostics() -> None:
    metrics = probability_metrics(
        y_true=[0, 0, 1, 1],
        probabilities=[0.1, 0.4, 0.6, 0.9],
        threshold=0.5,
        calibration_bins=2,
    )

    assert metrics["brier_score"] == pytest.approx(0.085)
    assert metrics["roc_auc"] == 1.0
    assert metrics["average_precision"] == 1.0
    assert metrics["calibration_intercept"] is not None
    assert metrics["calibration_slope"] is not None
    assert len(metrics["reliability_curve"]) == 2
    assert expected_calibration_error(
        [0, 1, 1, 1], [0.1, 0.2, 0.8, 0.9], bins=2
    ) == pytest.approx(0.25)


def test_single_class_calibration_regression_is_reported_as_undefined() -> None:
    assert calibration_intercept_slope([1, 1], [0.7, 0.8]) == (None, None)


def test_primary_metric_bootstrap_is_paired_and_clustered_by_student() -> None:
    predictions = pd.DataFrame(
        {
            "student_id": ["a", "a", "b", "b"],
            "target": [0, 1, 0, 1],
            "candidate": [0.2, 0.8, 0.3, 0.7],
            "reference": [0.4, 0.6, 0.4, 0.6],
        }
    )

    result = paired_cluster_bootstrap_primary_differences(
        predictions,
        candidate_column="candidate",
        reference_column="reference",
        iterations=100,
        seed=2026,
    )

    assert result["log_loss_difference"]["upper_95"] < 0
    assert result["brier_difference"]["upper_95"] < 0
