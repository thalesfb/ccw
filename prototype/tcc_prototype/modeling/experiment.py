"""Reproducible baseline experiment for next-response prediction."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .baselines import SmoothedProbabilityBaseline
from .evaluation import probability_metrics
from .features import build_history_features
from .splits import assign_cold_start_split, assign_temporal_split


@dataclass(frozen=True)
class BaselineExperimentResult:
    split_strategy: str
    seed: int
    metrics: dict[str, dict[str, float | None]]
    skill_metrics: dict[str, dict[str, dict[str, float | None]]]
    predictions: pd.DataFrame
    splits: pd.DataFrame


@dataclass(frozen=True)
class BaselineArtifacts:
    metrics_path: Path
    predictions_path: Path
    splits_path: Path


def _logistic_pipeline(seed: int) -> Pipeline:
    numeric_features = [
        "prior_student_attempts",
        "prior_student_correct",
        "prior_student_accuracy",
        "prior_student_skill_attempts",
        "prior_student_skill_correct",
        "prior_student_skill_accuracy",
    ]
    categorical_features = ["item_id", "primary_skill_id"]
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=seed,
                    solver="lbfgs",
                ),
            ),
        ]
    )


def _skill_metrics(
    test: pd.DataFrame,
    probability_columns: dict[str, str],
    *,
    minimum_rows: int,
) -> dict[str, dict[str, dict[str, float | None]]]:
    result: dict[str, dict[str, dict[str, float | None]]] = {}
    for skill, group in test.groupby("primary_skill_id", sort=True):
        if len(group) < minimum_rows:
            continue
        result[str(skill)] = {
            model_name: probability_metrics(
                group["target"].tolist(), group[column].tolist()
            )
            for model_name, column in probability_columns.items()
        }
    return result


def run_baseline_experiment(
    interactions: pd.DataFrame,
    *,
    split_strategy: str,
    seed: int = 2026,
    minimum_skill_rows: int = 1,
) -> BaselineExperimentResult:
    """Build history features, split data, fit baselines, and evaluate test rows."""

    modeled = build_history_features(interactions)
    if split_strategy == "cold_start":
        split_frame = assign_cold_start_split(modeled, seed=seed)
    elif split_strategy == "temporal":
        split_frame = assign_temporal_split(modeled)
    else:
        raise ValueError("split_strategy must be 'cold_start' or 'temporal'")

    train = split_frame.loc[split_frame["split"] == "train"].copy()
    test = split_frame.loc[split_frame["split"] == "test"].copy()
    if train.empty or test.empty:
        raise ValueError("experiment requires non-empty train and test sets")
    if train["target"].nunique() < 2:
        raise ValueError("logistic regression requires both target classes in training")

    prediction_columns: dict[str, str] = {}
    baseline_definitions = {
        "global_probability": (),
        "item_probability": ("item_id",),
        "skill_probability": ("primary_skill_id",),
        "student_history_probability": ("student_id",),
    }
    for model_name, group_columns in baseline_definitions.items():
        baseline = SmoothedProbabilityBaseline(
            group_columns=group_columns,
            prior_strength=5.0,
        ).fit(train)
        column = f"{model_name}_probability"
        test[column] = baseline.predict_proba(test)
        prediction_columns[model_name] = column

    logistic = _logistic_pipeline(seed)
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
    logistic.fit(train[feature_columns], train["target"])
    logistic_column = "logistic_regression_probability"
    test[logistic_column] = logistic.predict_proba(test[feature_columns])[:, 1]
    prediction_columns["logistic_regression"] = logistic_column

    metrics = {
        model_name: probability_metrics(
            test["target"].tolist(), test[column].tolist()
        )
        for model_name, column in prediction_columns.items()
    }
    skill_metrics = _skill_metrics(
        test,
        prediction_columns,
        minimum_rows=minimum_skill_rows,
    )

    prediction_metadata = [
        "student_id",
        "item_id",
        "primary_skill_id",
        "interaction_order",
        "source_row_id",
        "split",
        "target",
    ]
    predictions = test[
        prediction_metadata + list(prediction_columns.values())
    ].reset_index(drop=True)
    splits = split_frame[
        [
            "student_id",
            "item_id",
            "primary_skill_id",
            "interaction_order",
            "source_row_id",
            "split",
            "target",
        ]
    ].reset_index(drop=True)
    return BaselineExperimentResult(
        split_strategy=split_strategy,
        seed=seed,
        metrics=metrics,
        skill_metrics=skill_metrics,
        predictions=predictions,
        splits=splits,
    )


def write_baseline_artifacts(
    result: BaselineExperimentResult,
    *,
    output_dir: Path,
) -> BaselineArtifacts:
    """Persist metrics, test predictions, and split assignments."""

    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"baseline_{result.split_strategy}_seed_{result.seed}"
    metrics_path = output_dir / f"{prefix}.metrics.json"
    predictions_path = output_dir / f"{prefix}.predictions.parquet"
    splits_path = output_dir / f"{prefix}.splits.parquet"

    metrics_path.write_text(
        json.dumps(
            {
                "split_strategy": result.split_strategy,
                "seed": result.seed,
                "models": result.metrics,
                "by_skill": result.skill_metrics,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    result.predictions.to_parquet(predictions_path, index=False, engine="pyarrow")
    result.splits.to_parquet(splits_path, index=False, engine="pyarrow")
    return BaselineArtifacts(
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        splits_path=splits_path,
    )
