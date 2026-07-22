"""Exact local contribution explanations for fitted logistic pipelines."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def explain_logistic_rows(
    model: Pipeline,
    frame: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Decompose each logistic prediction into additive log-odds contributions.

    The returned contributions are exact for the fitted linear classifier after
    preprocessing. They describe the model computation and must not be treated
    as causal explanations of student behavior.
    """

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
                feature_names, row_values, coefficients, strict=True
            )
        ]
        contributions.sort(
            key=lambda record: abs(record["contribution"]), reverse=True
        )
        explanations.append(
            {
                "row_number": row_number,
                "intercept": intercept,
                "log_odds": float(log_odds[row_number]),
                "probability": float(probabilities[row_number]),
                "contributions": contributions,
                "interpretation_limit": (
                    "Contributions explain the fitted model in log-odds space; "
                    "they do not establish causal factors or pedagogical diagnoses."
                ),
            }
        )
    return explanations
