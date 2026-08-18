"""Probabilistic evaluation and paired student-cluster uncertainty utilities."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
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


def _validated_arrays(y_true: Sequence[int], probabilities: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    y = np.asarray(y_true, dtype=int)
    probability = np.asarray(probabilities, dtype=float)
    if y.shape != probability.shape or y.size == 0:
        raise ValueError("evaluation arrays must be non-empty and have the same shape")
    if not np.isin(y, [0, 1]).all():
        raise ValueError("targets must be binary")
    if np.any((probability < 0) | (probability > 1)):
        raise ValueError("probabilities must be between zero and one")
    return y, probability


def reliability_curve(y_true: Sequence[int], probabilities: Sequence[float], *, bins: int) -> list[dict[str, float | int]]:
    y, probability = _validated_arrays(y_true, probabilities)
    if bins < 1:
        raise ValueError("bins must be positive")
    edges = np.linspace(0.0, 1.0, bins + 1)
    bin_ids = np.digitize(probability, edges[1:-1], right=False)
    result = []
    for bin_id in range(bins):
        mask = bin_ids == bin_id
        if np.any(mask):
            result.append({
                "lower": float(edges[bin_id]),
                "upper": float(edges[bin_id + 1]),
                "count": int(mask.sum()),
                "mean_predicted": float(probability[mask].mean()),
                "observed_rate": float(y[mask].mean()),
            })
    return result


def expected_calibration_error(y_true: Sequence[int], probabilities: Sequence[float], *, bins: int) -> float:
    curve = reliability_curve(y_true, probabilities, bins=bins)
    observations = sum(int(row["count"]) for row in curve)
    return sum(
        int(row["count"]) / observations
        * abs(float(row["observed_rate"]) - float(row["mean_predicted"]))
        for row in curve
    )


def calibration_intercept_slope(y_true: Sequence[int], probabilities: Sequence[float]) -> tuple[float | None, float | None]:
    y, probability = _validated_arrays(y_true, probabilities)
    if len(np.unique(y)) < 2:
        return None, None
    clipped = np.clip(probability, 1e-6, 1 - 1e-6)
    logits = np.log(clipped / (1.0 - clipped)).reshape(-1, 1)
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=1000)
    model.fit(logits, y)
    return float(model.intercept_[0]), float(model.coef_[0][0])


def probability_metrics(y_true: Sequence[int], probabilities: Sequence[float], *, threshold: float, calibration_bins: int) -> dict[str, object]:
    y, probability = _validated_arrays(y_true, probabilities)
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between zero and one")
    predicted = (probability >= threshold).astype(int)
    has_both_classes = len(np.unique(y)) == 2
    intercept, slope = calibration_intercept_slope(y, probability)
    return {
        "observations": int(len(y)),
        "positive_rate": float(y.mean()),
        "log_loss": float(log_loss(y, np.clip(probability, 1e-15, 1 - 1e-15), labels=[0, 1])),
        "brier_score": float(brier_score_loss(y, probability)),
        "roc_auc": float(roc_auc_score(y, probability)) if has_both_classes else None,
        "average_precision": float(average_precision_score(y, probability)) if has_both_classes else None,
        "accuracy": float(accuracy_score(y, predicted)),
        "precision": float(precision_score(y, predicted, zero_division=0)),
        "recall": float(recall_score(y, predicted, zero_division=0)),
        "f1": float(f1_score(y, predicted, zero_division=0)),
        "calibration_intercept": intercept,
        "calibration_slope": slope,
        "expected_calibration_error": expected_calibration_error(y, probability, bins=calibration_bins),
        "reliability_curve": reliability_curve(y, probability, bins=calibration_bins),
    }


def paired_cluster_bootstrap_primary_differences(predictions: pd.DataFrame, *, candidate_column: str, reference_column: str, iterations: int, seed: int) -> dict[str, dict[str, float]]:
    """Bootstrap candidate-minus-reference primary loss differences by student."""

    if iterations < 1:
        raise ValueError("bootstrap iterations must be positive")
    required = {"student_id", "target", candidate_column, reference_column}
    missing = sorted(required.difference(predictions.columns))
    if missing:
        raise ValueError("missing bootstrap columns: " + ", ".join(missing))
    if predictions.empty:
        raise ValueError("bootstrap requires held-out predictions")

    frame = predictions.copy()
    y = frame["target"].to_numpy(dtype=float)
    candidate = np.clip(frame[candidate_column].to_numpy(dtype=float), 1e-15, 1 - 1e-15)
    reference = np.clip(frame[reference_column].to_numpy(dtype=float), 1e-15, 1 - 1e-15)
    frame["log_loss_difference"] = -(y * np.log(candidate) + (1 - y) * np.log(1 - candidate)) + (y * np.log(reference) + (1 - y) * np.log(1 - reference))
    frame["brier_difference"] = (candidate - y) ** 2 - (reference - y) ** 2
    clusters = frame.groupby("student_id", sort=True).agg(
        count=("target", "size"),
        log_loss_difference=("log_loss_difference", "sum"),
        brier_difference=("brier_difference", "sum"),
    ).reset_index(drop=True)
    rng = np.random.default_rng(seed)
    cluster_count = len(clusters)
    counts = clusters["count"].to_numpy(dtype=float)
    metric_sums = {metric: clusters[metric].to_numpy(dtype=float) for metric in ("log_loss_difference", "brier_difference")}
    samples = {metric: np.empty(iterations, dtype=float) for metric in metric_sums}
    for iteration in range(iterations):
        draw = rng.integers(0, cluster_count, size=cluster_count)
        denominator = counts[draw].sum()
        for metric, sums in metric_sums.items():
            samples[metric][iteration] = sums[draw].sum() / denominator
    return {
        metric: {
            "mean": float(values.mean()),
            "lower_95": float(np.quantile(values, 0.025)),
            "upper_95": float(np.quantile(values, 0.975)),
        }
        for metric, values in samples.items()
    }
