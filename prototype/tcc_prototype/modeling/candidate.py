"""Non-linear candidate model evaluated only after transparent baselines."""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

NUMERIC_FEATURES = [
    "prior_student_attempts",
    "prior_student_correct",
    "prior_student_accuracy",
    "prior_student_skill_attempts",
    "prior_student_skill_correct",
    "prior_student_skill_accuracy",
]
CATEGORICAL_FEATURES = ["item_id", "primary_skill_id"]
MODEL_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def build_random_forest_pipeline(
    *,
    seed: int,
    n_estimators: int = 300,
    min_samples_leaf: int = 5,
) -> Pipeline:
    """Build a sparse-compatible random forest classification pipeline."""

    if n_estimators < 1:
        raise ValueError("n_estimators must be positive")
    if min_samples_leaf < 1:
        raise ValueError("min_samples_leaf must be positive")

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", "passthrough", NUMERIC_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    classifier = RandomForestClassifier(
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        class_weight="balanced_subsample",
        random_state=seed,
        n_jobs=-1,
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def permutation_importance_report(
    model: Pipeline,
    frame: pd.DataFrame,
    target: pd.Series,
    *,
    seed: int,
    repeats: int = 5,
) -> pd.DataFrame:
    """Calculate model-agnostic importance over the original input columns."""

    if repeats < 1:
        raise ValueError("repeats must be positive")
    result = permutation_importance(
        model,
        frame[MODEL_FEATURES],
        target,
        scoring="neg_log_loss",
        n_repeats=repeats,
        random_state=seed,
        n_jobs=-1,
    )
    return (
        pd.DataFrame(
            {
                "feature": MODEL_FEATURES,
                "importance_mean": result.importances_mean,
                "importance_std": result.importances_std,
            }
        )
        .sort_values("importance_mean", ascending=False, kind="mergesort")
        .reset_index(drop=True)
    )
