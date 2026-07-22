import math

import pytest

from tcc_prototype.modeling.evaluation import expected_calibration_error, probability_metrics


def test_probability_metrics_include_calibration_and_discrimination() -> None:
    metrics = probability_metrics(
        y_true=[0, 0, 1, 1],
        probabilities=[0.1, 0.4, 0.6, 0.9],
    )

    assert metrics["log_loss"] > 0
    assert metrics["brier_score"] == pytest.approx(0.085)
    assert metrics["roc_auc"] == 1.0
    assert metrics["average_precision"] == 1.0
    assert metrics["accuracy"] == 1.0
    assert metrics["expected_calibration_error"] >= 0


def test_probability_metrics_return_null_auc_for_single_class() -> None:
    metrics = probability_metrics(y_true=[1, 1], probabilities=[0.7, 0.8])

    assert metrics["roc_auc"] is None
    assert not math.isnan(metrics["log_loss"])


def test_expected_calibration_error_weights_bins_by_frequency() -> None:
    error = expected_calibration_error(
        y_true=[0, 1, 1, 1],
        probabilities=[0.1, 0.2, 0.8, 0.9],
        bins=2,
    )

    assert error == pytest.approx(0.25)
