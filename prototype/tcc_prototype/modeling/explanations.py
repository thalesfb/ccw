"""Exact logistic explanations reconstructed from frozen experiment artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline

from .features import build_history_features
from .models import NUMERIC_HISTORY_FEATURES, logistic_pipeline


@dataclass(frozen=True)
class LogisticExplanationReconstruction:
    """Verified reconstruction of the logistic model used by an experiment run."""

    max_abs_probability_error: float
    explanations: list[dict[str, Any]]
    permutation_importance: pd.DataFrame


def explain_logistic_rows(
    model: Pipeline,
    frame: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Decompose fitted binary-logistic predictions into exact log-odds terms."""

    if "preprocessor" not in model.named_steps or "classifier" not in model.named_steps:
        raise ValueError("expected a pipeline with preprocessor and classifier steps")
    preprocessor = model.named_steps["preprocessor"]
    classifier = model.named_steps["classifier"]
    if not hasattr(classifier, "coef_") or classifier.coef_.shape[0] != 1:
        raise ValueError("only fitted binary logistic classifiers are supported")

    transformed = preprocessor.transform(frame)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    values = np.asarray(transformed, dtype=float)
    feature_names = preprocessor.get_feature_names_out().tolist()
    coefficients = np.asarray(classifier.coef_[0], dtype=float)
    intercept = float(classifier.intercept_[0])
    probabilities = model.predict_proba(frame)[:, 1]
    log_odds = model.decision_function(frame)

    explanations: list[dict[str, Any]] = []
    for row_number, row_values in enumerate(values):
        contributions = [
            {
                "feature": feature_name,
                "transformed_value": float(value),
                "coefficient": float(coefficient),
                "contribution": float(value * coefficient),
            }
            for feature_name, value, coefficient in zip(
                feature_names,
                row_values,
                coefficients,
                strict=True,
            )
        ]
        contributions.sort(
            key=lambda record: abs(record["contribution"]),
            reverse=True,
        )
        explanations.append(
            {
                "row_number": row_number,
                "intercept": intercept,
                "log_odds": float(log_odds[row_number]),
                "probability": float(probabilities[row_number]),
                "contributions": contributions,
                "interpretation_limit": (
                    "Contributions explain the fitted model computation in log-odds "
                    "space and do not establish causal factors, learning, competence, "
                    "or pedagogical diagnoses."
                ),
            }
        )
    return explanations


def reconstruct_logistic_explanations(
    interactions: pd.DataFrame,
    *,
    splits: pd.DataFrame,
    predictions: pd.DataFrame,
    selected_parameters: dict[str, Any],
    seed: int,
    explanation_rows: int = 20,
    probability_tolerance: float = 1e-12,
    permutation_repeats: int = 5,
) -> LogisticExplanationReconstruction:
    """Refit only the frozen logistic specification and verify registered probabilities."""

    if explanation_rows < 0:
        raise ValueError("explanation_rows must be non-negative")
    if probability_tolerance < 0:
        raise ValueError("probability_tolerance must be non-negative")
    if permutation_repeats < 1:
        raise ValueError("permutation_repeats must be positive")
    if "C" not in selected_parameters or "max_iter" not in selected_parameters:
        raise ValueError("selected logistic parameters must include C and max_iter")

    required_split_columns = {"source_row_id", "split"}
    missing_split = sorted(required_split_columns.difference(splits.columns))
    if missing_split:
        raise ValueError("missing split columns: " + ", ".join(missing_split))
    probability_column = "logistic_regression_probability"
    required_prediction_columns = {"source_row_id", probability_column}
    missing_predictions = sorted(required_prediction_columns.difference(predictions.columns))
    if missing_predictions:
        raise ValueError(
            "missing prediction columns: " + ", ".join(missing_predictions)
        )

    modeled = build_history_features(interactions)
    modeled["source_row_id"] = modeled["source_row_id"].astype(str)
    assignments = splits[["source_row_id", "split"]].copy()
    assignments["source_row_id"] = assignments["source_row_id"].astype(str)
    if assignments["source_row_id"].duplicated().any():
        raise ValueError("split artifact contains duplicate source_row_id values")

    reconstructed = modeled.merge(
        assignments,
        on="source_row_id",
        how="inner",
        validate="one_to_one",
    )
    if len(reconstructed) != len(assignments):
        raise ValueError("canonical interactions do not reproduce every registered split row")

    train = reconstructed.loc[reconstructed["split"] == "train"].copy()
    test = reconstructed.loc[reconstructed["split"] == "test"].copy()
    if train.empty or test.empty:
        raise ValueError("registered split must contain non-empty train and test partitions")

    columns = NUMERIC_HISTORY_FEATURES + ["item_id", "skill_signature"]
    model = logistic_pipeline(
        c_value=float(selected_parameters["C"]),
        seed=seed,
        max_iter=int(selected_parameters["max_iter"]),
    )
    model.fit(train[columns], train["target"])

    registered = predictions[["source_row_id", probability_column]].copy()
    registered["source_row_id"] = registered["source_row_id"].astype(str)
    if registered["source_row_id"].duplicated().any():
        raise ValueError("prediction artifact contains duplicate source_row_id values")

    aligned = test.merge(
        registered,
        on="source_row_id",
        how="inner",
        validate="one_to_one",
    )
    if len(aligned) != len(test) or len(aligned) != len(registered):
        raise ValueError("registered predictions do not match the reconstructed test partition")

    reconstructed_probability = model.predict_proba(aligned[columns])[:, 1]
    registered_probability = aligned[probability_column].to_numpy(dtype=float)
    max_abs_error = float(
        np.max(np.abs(reconstructed_probability - registered_probability))
    )
    if max_abs_error > probability_tolerance:
        raise ValueError(
            "reconstructed logistic probabilities differ from the registered experiment "
            f"artifact by {max_abs_error:.3e}, exceeding tolerance {probability_tolerance:.3e}"
        )

    explanation_frame = aligned[columns].head(explanation_rows)
    explanations = (
        explain_logistic_rows(model, explanation_frame)
        if explanation_rows > 0
        else []
    )
    for explanation, source_row_id in zip(
        explanations,
        aligned["source_row_id"].head(explanation_rows),
        strict=True,
    ):
        explanation["source_row_id"] = str(source_row_id)

    importance = permutation_importance(
        model,
        aligned[columns],
        aligned["target"],
        scoring="neg_log_loss",
        n_repeats=permutation_repeats,
        random_state=seed,
        n_jobs=-1,
    )
    importance_frame = (
        pd.DataFrame(
            {
                "feature": columns,
                "importance_mean": importance.importances_mean,
                "importance_std": importance.importances_std,
            }
        )
        .sort_values("importance_mean", ascending=False, kind="mergesort")
        .reset_index(drop=True)
    )

    return LogisticExplanationReconstruction(
        max_abs_probability_error=max_abs_error,
        explanations=explanations,
        permutation_importance=importance_frame,
    )
