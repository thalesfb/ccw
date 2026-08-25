"""Regularized linear and nonlinear candidate models for the baseline experiment."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .features import normalize_skill_ids

NUMERIC_HISTORY_FEATURES = [
    "prior_student_attempts",
    "prior_student_correct",
    "prior_student_accuracy",
    "prior_student_skillset_attempts",
    "prior_student_skillset_correct",
    "prior_student_skillset_accuracy",
]


def logistic_pipeline(*, c_value: float, seed: int, max_iter: int) -> Pipeline:
    """Build the predeclared regularized logistic model."""

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_HISTORY_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                ["item_id", "skill_signature"],
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    C=c_value,
                    penalty="l2",
                    solver="lbfgs",
                    max_iter=max_iter,
                    random_state=seed,
                ),
            ),
        ]
    )


def hashed_tree_features(frame: pd.DataFrame, *, hash_features: int) -> np.ndarray:
    """Create fixed-width, target-independent item/skill context for tree models."""

    if hash_features < 2:
        raise ValueError("hash_features must be at least two")
    required = set(NUMERIC_HISTORY_FEATURES) | {"item_id", "skill_ids"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError("missing tree feature columns: " + ", ".join(missing))

    tokens = []
    for _, row in frame.iterrows():
        row_tokens = [f"item={row['item_id']}"]
        row_tokens.extend(
            f"skill={skill}" for skill in normalize_skill_ids(row["skill_ids"])
        )
        tokens.append(row_tokens)
    hashed = FeatureHasher(
        n_features=hash_features,
        input_type="string",
        alternate_sign=False,
    ).transform(tokens)
    numeric = frame[NUMERIC_HISTORY_FEATURES].to_numpy(dtype=float)
    return np.hstack([numeric, hashed.toarray()])


def hist_gradient_boosting_model(
    *,
    learning_rate: float,
    max_leaf_nodes: int,
    l2_regularization: float,
    max_iter: int,
    seed: int,
) -> HistGradientBoostingClassifier:
    """Build the nonlinear candidate with no implicit validation split."""

    return HistGradientBoostingClassifier(
        loss="log_loss",
        learning_rate=learning_rate,
        max_leaf_nodes=max_leaf_nodes,
        l2_regularization=l2_regularization,
        max_iter=max_iter,
        early_stopping=False,
        random_state=seed,
    )
