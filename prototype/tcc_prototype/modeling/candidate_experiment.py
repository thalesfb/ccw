"""Candidate model comparison, explanations, and skill-profile artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ..profiles import OrdinalThresholds, build_skill_profiles
from .candidate import (
    MODEL_FEATURES,
    build_random_forest_pipeline,
    permutation_importance_report,
)
from .evaluation import probability_metrics
from .experiment import _logistic_pipeline, run_baseline_experiment
from .explanations import explain_logistic_rows
from .features import build_history_features
from .splits import assign_cold_start_split, assign_temporal_split


@dataclass(frozen=True)
class CandidateExperimentResult:
    split_strategy: str
    seed: int
    metrics: dict[str, dict[str, float | None]]
    skill_metrics: dict[str, dict[str, dict[str, float | None]]]
    predictions: pd.DataFrame
    permutation_importance: pd.DataFrame
    skill_profiles: pd.DataFrame
    logistic_explanations: list[dict[str, object]]


@dataclass(frozen=True)
class CandidateArtifacts:
    metrics_path: Path
    predictions_path: Path
    importance_path: Path
    profiles_path: Path
    explanations_path: Path


def _split_frame(
    interactions: pd.DataFrame,
    *,
    split_strategy: str,
    seed: int,
) -> pd.DataFrame:
    modeled = build_history_features(interactions)
    if split_strategy == "cold_start":
        return assign_cold_start_split(modeled, seed=seed)
    if split_strategy == "temporal":
        return assign_temporal_split(modeled)
    raise ValueError("split_strategy must be 'cold_start' or 'temporal'")


def run_candidate_experiment(
    interactions: pd.DataFrame,
    *,
    split_strategy: str,
    seed: int = 2026,
    n_estimators: int = 300,
    min_samples_leaf: int = 5,
    minimum_profile_evidence: int = 5,
    thresholds: OrdinalThresholds | None = None,
    explanation_rows: int = 20,
    permutation_repeats: int = 5,
) -> CandidateExperimentResult:
    """Compare a random forest with baselines on identical partitions."""

    if explanation_rows < 0:
        raise ValueError("explanation_rows must be non-negative")
    baseline = run_baseline_experiment(
        interactions,
        split_strategy=split_strategy,
        seed=seed,
        minimum_skill_rows=minimum_profile_evidence,
    )
    split_frame = _split_frame(
        interactions,
        split_strategy=split_strategy,
        seed=seed,
    )
    train = split_frame.loc[split_frame["split"] == "train"].copy()
    test = split_frame.loc[split_frame["split"] == "test"].copy()

    random_forest = build_random_forest_pipeline(
        seed=seed,
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
    )
    random_forest.fit(train[MODEL_FEATURES], train["target"])
    test_probability = random_forest.predict_proba(test[MODEL_FEATURES])[:, 1]

    random_forest_predictions = test[["source_row_id"]].copy()
    random_forest_predictions["random_forest_probability"] = test_probability
    predictions = baseline.predictions.merge(
        random_forest_predictions,
        on="source_row_id",
        how="left",
        validate="one_to_one",
    )

    metrics = dict(baseline.metrics)
    metrics["random_forest"] = probability_metrics(
        test["target"].tolist(), test_probability.tolist()
    )
    skill_metrics = {
        skill: dict(model_metrics)
        for skill, model_metrics in baseline.skill_metrics.items()
    }
    for skill, group in test.groupby("primary_skill_id", sort=True):
        if len(group) < minimum_profile_evidence:
            continue
        skill_metrics.setdefault(str(skill), {})["random_forest"] = probability_metrics(
            group["target"].tolist(),
            random_forest.predict_proba(group[MODEL_FEATURES])[:, 1].tolist(),
        )

    importance = permutation_importance_report(
        random_forest,
        test[MODEL_FEATURES],
        test["target"],
        seed=seed,
        repeats=permutation_repeats,
    )

    logistic = _logistic_pipeline(seed)
    logistic.fit(train[MODEL_FEATURES], train["target"])
    explanation_frame = test[MODEL_FEATURES].head(explanation_rows)
    logistic_explanations = (
        explain_logistic_rows(logistic, explanation_frame)
        if explanation_rows > 0
        else []
    )
    for explanation, source_row_id in zip(
        logistic_explanations,
        test["source_row_id"].head(explanation_rows),
        strict=True,
    ):
        explanation["source_row_id"] = str(source_row_id)

    profiles = build_skill_profiles(
        predictions,
        probability_column="random_forest_probability",
        minimum_evidence=minimum_profile_evidence,
        thresholds=thresholds,
    )
    return CandidateExperimentResult(
        split_strategy=split_strategy,
        seed=seed,
        metrics=metrics,
        skill_metrics=skill_metrics,
        predictions=predictions,
        permutation_importance=importance,
        skill_profiles=profiles,
        logistic_explanations=logistic_explanations,
    )


def write_candidate_artifacts(
    result: CandidateExperimentResult,
    *,
    output_dir: Path,
) -> CandidateArtifacts:
    """Persist model comparison, explanations, and profiles."""

    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"candidate_{result.split_strategy}_seed_{result.seed}"
    metrics_path = output_dir / f"{prefix}.metrics.json"
    predictions_path = output_dir / f"{prefix}.predictions.parquet"
    importance_path = output_dir / f"{prefix}.permutation_importance.csv"
    profiles_path = output_dir / f"{prefix}.skill_profiles.parquet"
    explanations_path = output_dir / f"{prefix}.logistic_explanations.json"

    metrics_path.write_text(
        json.dumps(
            {
                "split_strategy": result.split_strategy,
                "seed": result.seed,
                "models": result.metrics,
                "by_skill": result.skill_metrics,
                "interpretation_limit": (
                    "Predictive metrics compare models on held-out interactions; "
                    "they do not demonstrate educational effectiveness."
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    result.predictions.to_parquet(predictions_path, index=False, engine="pyarrow")
    result.permutation_importance.to_csv(importance_path, index=False)
    result.skill_profiles.to_parquet(profiles_path, index=False, engine="pyarrow")
    explanations_path.write_text(
        json.dumps(result.logistic_explanations, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return CandidateArtifacts(
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        importance_path=importance_path,
        profiles_path=profiles_path,
        explanations_path=explanations_path,
    )
