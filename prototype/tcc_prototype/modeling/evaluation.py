"""Metrics for calibrated next-response probability estimates."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)


def expected_calibration_error(
    y_true: Sequence[int],
    probabilities: Sequence[float],
    *,
    bins: int = 10,
) -> float:
    """Calculate frequency-weighted absolute calibration error."""

    if bins < 1:
        raise ValueError("bins must be positive")
    y = np.asarray(y_true, dtype=float)
    probability = np.asarray(probabilities, dtype=float)
    if y.shape != probability.shape:
        raise ValueError("targets and probabilities must have the same shape")
    if y.size == 0:
        raise ValueError("calibration requires at least one observation")
    if np.any((probability < 0) | (probability > 1)):
        raise ValueError("probabilities must be between zero and one")

    edges = np.linspace(0.0, 1.0, bins + 1)
    bin_ids = np.digitize(probability, edges[1:-1], right=False)
    error = 0.0
    for bin_id in range(bins):
        mask = bin_ids == bin_id
        if not np.any(mask):
            continue
        observed = float(y[mask].mean())
        predicted = float(probability[mask].mean())
        error += float(mask.mean()) * abs(observed - predicted)
    return error


def probability_metrics(
    y_true: Sequence[int],
    probabilities: Sequence[float],
    *,
    threshold: float = 0.5,
    calibration_bins: int = 10,
) -> dict[str, float | None]:
    """Return discrimination, classification, and calibration metrics."""

    y = np.asarray(y_true, dtype=int)
    probability = np.asarray(probabilities, dtype=float)
    if y.shape != probability.shape:
        raise ValueError("targets and probabilities must have the same shape")
    if y.size == 0:
        raise ValueError("evaluation requires at least one observation")
    if np.any((probability < 0) | (probability > 1)):
        raise ValueError("probabilities must be between zero and one")
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between zero and one")

    clipped = np.clip(probability, 1e-15, 1 - 1e-15)
    predicted = (probability >= threshold).astype(int)
    has_both_classes = len(np.unique(y)) == 2

    return {
        "observations": float(len(y)),
        "positive_rate": float(y.mean()),
        "log_loss": float(log_loss(y, clipped, labels=[0, 1])),
        "brier_score": float(brier_score_loss(y, probability)),
        "roc_auc": float(roc_auc_score(y, probability))
        if has_both_classes
        else None,
        "average_precision": float(average_precision_score(y, probability)),
        "accuracy": float(accuracy_score(y, predicted)),
        "precision": float(precision_score(y, predicted, zero_division=0)),
        "recall": float(recall_score(y, predicted, zero_division=0)),
        "f1": float(f1_score(y, predicted, zero_division=0)),
        "expected_calibration_error": expected_calibration_error(
            y, probability, bins=calibration_bins
        ),
    }
