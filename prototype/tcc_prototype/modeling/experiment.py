"""Reproducible leakage-safe baseline and nonlinear evaluation experiment."""

from __future__ import annotations

import itertools
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import log_loss

from .baselines import (
    MultiSkillSmoothedProbabilityBaseline,
    SmoothedProbabilityBaseline,
    student_history_probability,
)
from .evaluation import paired_cluster_bootstrap_primary_differences, probability_metrics
from .features import build_history_features, normalize_skill_ids
from .models import (
    NUMERIC_HISTORY_FEATURES,
    hashed_tree_features,
    hist_gradient_boosting_model,
    logistic_pipeline,
)
from .splits import (
    assign_personalized_temporal_split,
    assign_student_holdout_split,
    filter_eligible_students,
)


class ExperimentConfigError(ValueError):
    """Raised when the versioned experiment contract is not executable yet."""


@dataclass(frozen=True)
class BaselineExperimentResult:
    split_strategy: str
    seed: int
    config_schema_version: str
    selected_parameters: dict[str, Any]
    validation_metrics: dict[str, dict[str, object]]
    test_metrics: dict[str, dict[str, object]]
    skill_metrics: dict[str, dict[str, Any]]
    subgroup_metrics: dict[str, Any]
    hypothesis_comparisons: dict[str, Any]
    cold_start_slice: dict[str, dict[str, object]] | None
    predictions: pd.DataFrame
    splits: pd.DataFrame


@dataclass(frozen=True)
class BaselineArtifacts:
    metrics_path: Path
    predictions_path: Path
    splits_path: Path


def load_experiment_config(path: Path) -> dict[str, Any]:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ExperimentConfigError(f"unable to read experiment config {path}: {exc}") from exc
    validate_experiment_execution_config(config)
    return config


def validate_experiment_execution_config(config: dict[str, Any]) -> None:
    """Require every choice that must be frozen before partition/test evaluation."""

    try:
        eligibility = config["eligibility"]
        reporting = config["reporting"]
        execution = config["evaluation_execution"]
        seeds = config["random_seeds"]
        splits = config["splits"]
    except KeyError as exc:
        raise ExperimentConfigError(f"missing experiment section: {exc.args[0]}") from exc

    if eligibility.get("minimum_interactions_per_student") is None:
        raise ExperimentConfigError(
            "minimum_interactions_per_student must be frozen after dataset characterization before model evaluation"
        )
    skill_support = reporting.get("skill_support", {})
    if skill_support.get("minimum_test_rows") is None:
        raise ExperimentConfigError("minimum_test_rows must be frozen before per-skill test evaluation")
    if skill_support.get("minimum_test_students") is None:
        raise ExperimentConfigError("minimum_test_students must be frozen before per-skill test evaluation")
    subgroup = reporting.get("subgroup_audit", {})
    if subgroup.get("columns") and (
        subgroup.get("minimum_test_rows") is None
        or subgroup.get("minimum_test_students") is None
    ):
        raise ExperimentConfigError(
            "subgroup support thresholds must be frozen when subgroup auditing is enabled"
        )

    minimum_interactions = eligibility.get("minimum_interactions_per_student")
    if (
        not isinstance(minimum_interactions, int)
        or isinstance(minimum_interactions, bool)
        or minimum_interactions < 3
    ):
        raise ExperimentConfigError(
            "minimum_interactions_per_student must be an integer of at least three"
        )
    for name in ("minimum_test_rows", "minimum_test_students"):
        value = skill_support.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ExperimentConfigError(f"{name} must be a positive integer")

    required_execution = {
        "classification_threshold",
        "calibration_bins",
        "smoothing_strengths",
        "logistic_regression",
        "hist_gradient_boosting",
    }
    missing_execution = sorted(required_execution.difference(execution))
    if missing_execution:
        raise ExperimentConfigError(
            "missing evaluation_execution fields: " + ", ".join(missing_execution)
        )
    threshold = execution["classification_threshold"]
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not 0 < float(threshold) < 1:
        raise ExperimentConfigError("classification_threshold must be between zero and one")
    bins = execution["calibration_bins"]
    if not isinstance(bins, int) or isinstance(bins, bool) or bins < 2:
        raise ExperimentConfigError("calibration_bins must be an integer of at least two")
    strengths = execution["smoothing_strengths"]
    if not strengths or any(float(value) <= 0 for value in strengths):
        raise ExperimentConfigError("smoothing_strengths must contain positive values")
    logistic = execution["logistic_regression"]
    if not logistic.get("c_values") or any(float(value) <= 0 for value in logistic.get("c_values", [])):
        raise ExperimentConfigError("logistic_regression.c_values must contain positive values")
    hgb = execution["hist_gradient_boosting"]
    required_hgb = {
        "learning_rate_values",
        "max_leaf_nodes_values",
        "l2_regularization_values",
        "max_iter",
        "hash_features",
    }
    if required_hgb.difference(hgb):
        raise ExperimentConfigError("hist_gradient_boosting grid is incomplete")
    if not hgb["learning_rate_values"] or not hgb["max_leaf_nodes_values"] or not hgb["l2_regularization_values"]:
        raise ExperimentConfigError("hist_gradient_boosting grids must be non-empty")
    bootstrap_iterations = reporting.get("bootstrap", {}).get("iterations")
    if not isinstance(bootstrap_iterations, int) or isinstance(bootstrap_iterations, bool) or bootstrap_iterations < 1:
        raise ExperimentConfigError("bootstrap iterations must be a positive integer")
    if not seeds or len(set(seeds)) != len(seeds):
        raise ExperimentConfigError("random_seeds must contain distinct predefined seeds")
    if set(splits) != {"student_holdout", "personalized_temporal"}:
        raise ExperimentConfigError(
            "primary split strategies must be student_holdout and personalized_temporal"
        )


def _split_frame(modeled: pd.DataFrame, *, split_strategy: str, seed: int, config: dict[str, Any]) -> pd.DataFrame:
    eligible = filter_eligible_students(
        modeled,
        minimum_interactions=int(config["eligibility"]["minimum_interactions_per_student"]),
    )
    if eligible.empty:
        raise ValueError("no students satisfy the frozen eligibility threshold")
    split_config = config["splits"][split_strategy]
    kwargs = {
        "train_fraction": float(split_config["train_fraction"]),
        "validation_fraction": float(split_config["validation_fraction"]),
        "test_fraction": float(split_config["test_fraction"]),
    }
    if split_strategy == "student_holdout":
        return assign_student_holdout_split(eligible, seed=seed, **kwargs)
    if split_strategy == "personalized_temporal":
        return assign_personalized_temporal_split(eligible, **kwargs)
    raise ValueError("unsupported split strategy")


def _loss(target: pd.Series, probability: np.ndarray) -> float:
    return float(
        log_loss(
            target.astype(int).to_numpy(),
            np.clip(probability, 1e-15, 1 - 1e-15),
            labels=[0, 1],
        )
    )


def _select_strength(strengths: list[float], predictor: Any, validation: pd.DataFrame) -> tuple[float, np.ndarray]:
    candidates = []
    for strength in strengths:
        probability = predictor(float(strength))
        candidates.append((_loss(validation["target"], probability), float(strength), probability))
    _, best_strength, best_probability = min(candidates, key=lambda row: (row[0], row[1]))
    return best_strength, best_probability


def _baseline_predictions(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
    *,
    strengths: list[float],
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict[str, Any]]:
    global_model = SmoothedProbabilityBaseline((), prior_strength=0.0).fit(train)
    global_probability = global_model.global_probability
    validation_predictions = {"global_probability": global_model.predict_proba(validation)}
    test_predictions = {"global_probability": global_model.predict_proba(test)}
    selected: dict[str, Any] = {
        "global_probability": {"training_prevalence": global_probability}
    }

    item_strength, item_validation = _select_strength(
        strengths,
        lambda strength: SmoothedProbabilityBaseline(("item_id",), strength)
        .fit(train)
        .predict_proba(validation),
        validation,
    )
    item_model = SmoothedProbabilityBaseline(("item_id",), item_strength).fit(train)
    validation_predictions["item_smoothed_probability"] = item_validation
    test_predictions["item_smoothed_probability"] = item_model.predict_proba(test)
    selected["item_smoothed_probability"] = {"prior_strength": item_strength}

    skill_strength, skill_validation = _select_strength(
        strengths,
        lambda strength: MultiSkillSmoothedProbabilityBaseline(strength)
        .fit(train)
        .predict_proba(validation),
        validation,
    )
    skill_model = MultiSkillSmoothedProbabilityBaseline(skill_strength).fit(train)
    validation_predictions["skill_smoothed_probability"] = skill_validation
    test_predictions["skill_smoothed_probability"] = skill_model.predict_proba(test)
    selected["skill_smoothed_probability"] = {"prior_strength": skill_strength}

    student_strength, student_validation = _select_strength(
        strengths,
        lambda strength: student_history_probability(
            validation,
            prior_strength=strength,
            global_probability=global_probability,
        ),
        validation,
    )
    validation_predictions["student_history_smoothed_probability"] = student_validation
    test_predictions["student_history_smoothed_probability"] = student_history_probability(
        test,
        prior_strength=student_strength,
        global_probability=global_probability,
    )
    selected["student_history_smoothed_probability"] = {"prior_strength": student_strength}
    return validation_predictions, test_predictions, selected


def _select_logistic(train: pd.DataFrame, validation: pd.DataFrame, test: pd.DataFrame, *, seed: int, config: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    specification = config["evaluation_execution"]["logistic_regression"]
    max_iter = int(specification["max_iter"])
    columns = NUMERIC_HISTORY_FEATURES + ["item_id", "skill_signature"]
    candidates = []
    for c_value in [float(value) for value in specification["c_values"]]:
        model = logistic_pipeline(c_value=c_value, seed=seed, max_iter=max_iter)
        model.fit(train[columns], train["target"])
        probability = model.predict_proba(validation[columns])[:, 1]
        candidates.append((_loss(validation["target"], probability), c_value, probability))
    _, selected_c, validation_probability = min(candidates, key=lambda row: (row[0], row[1]))
    final_model = logistic_pipeline(c_value=selected_c, seed=seed, max_iter=max_iter)
    final_model.fit(train[columns], train["target"])
    return validation_probability, final_model.predict_proba(test[columns])[:, 1], {
        "C": selected_c,
        "penalty": "l2",
        "solver": "lbfgs",
        "max_iter": max_iter,
        "fit_partition": "train_only",
    }


def _select_hgb(train: pd.DataFrame, validation: pd.DataFrame, test: pd.DataFrame, *, seed: int, config: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    specification = config["evaluation_execution"]["hist_gradient_boosting"]
    hash_features = int(specification["hash_features"])
    train_features = hashed_tree_features(train, hash_features=hash_features)
    validation_features = hashed_tree_features(validation, hash_features=hash_features)
    test_features = hashed_tree_features(test, hash_features=hash_features)
    candidates = []
    max_iter = int(specification["max_iter"])
    for learning_rate, max_leaf_nodes, l2_regularization in itertools.product(
        [float(v) for v in specification["learning_rate_values"]],
        [int(v) for v in specification["max_leaf_nodes_values"]],
        [float(v) for v in specification["l2_regularization_values"]],
    ):
        model = hist_gradient_boosting_model(
            learning_rate=learning_rate,
            max_leaf_nodes=max_leaf_nodes,
            l2_regularization=l2_regularization,
            max_iter=max_iter,
            seed=seed,
        )
        model.fit(train_features, train["target"])
        probability = model.predict_proba(validation_features)[:, 1]
        params = (learning_rate, max_leaf_nodes, l2_regularization)
        candidates.append((_loss(validation["target"], probability), params, probability))
    _, selected, validation_probability = min(candidates, key=lambda row: (row[0], row[1]))
    learning_rate, max_leaf_nodes, l2_regularization = selected
    final_model = hist_gradient_boosting_model(
        learning_rate=learning_rate,
        max_leaf_nodes=max_leaf_nodes,
        l2_regularization=l2_regularization,
        max_iter=max_iter,
        seed=seed,
    )
    final_model.fit(train_features, train["target"])
    return validation_probability, final_model.predict_proba(test_features)[:, 1], {
        "learning_rate": learning_rate,
        "max_leaf_nodes": max_leaf_nodes,
        "l2_regularization": l2_regularization,
        "max_iter": max_iter,
        "early_stopping": False,
        "hash_features": hash_features,
        "hashing_policy": "target_independent_item_and_skill_tokens",
        "fit_partition": "train_only",
    }


def _metrics_by_model(frame: pd.DataFrame, probabilities: dict[str, np.ndarray], *, threshold: float, calibration_bins: int) -> dict[str, dict[str, object]]:
    return {
        name: probability_metrics(
            frame["target"].tolist(),
            probability.tolist(),
            threshold=threshold,
            calibration_bins=calibration_bins,
        )
        for name, probability in probabilities.items()
    }


def _skill_metrics(test: pd.DataFrame, probability_columns: dict[str, str], *, minimum_rows: int, minimum_students: int, threshold: float, calibration_bins: int) -> dict[str, dict[str, Any]]:
    skills = sorted(
        {skill for value in test["skill_ids"] for skill in normalize_skill_ids(value)}
    )
    result = {}
    for skill in skills:
        group = test.loc[
            test["skill_ids"].map(lambda value: skill in normalize_skill_ids(value))
        ]
        support = {
            "unique_interactions": int(group["source_row_id"].nunique()),
            "unique_students": int(group["student_id"].nunique()),
        }
        if support["unique_interactions"] < minimum_rows or support["unique_students"] < minimum_students:
            result[skill] = {"status": "insufficient_evidence", "support": support}
        else:
            result[skill] = {
                "status": "reported",
                "support": support,
                "models": {
                    name: probability_metrics(
                        group["target"].tolist(),
                        group[column].tolist(),
                        threshold=threshold,
                        calibration_bins=calibration_bins,
                    )
                    for name, column in probability_columns.items()
                },
            }
    return result


def _subgroup_metrics(test: pd.DataFrame, probability_columns: dict[str, str], *, config: dict[str, Any], threshold: float, calibration_bins: int) -> dict[str, Any]:
    audit = config["reporting"].get("subgroup_audit", {})
    columns = list(audit.get("columns", []))
    if not columns:
        return {"status": "not_applicable", "reason": "no_approved_subgroup_columns"}
    result: dict[str, Any] = {"status": "reported", "columns": {}}
    for column in columns:
        if column not in test.columns:
            raise ValueError(f"configured subgroup column is absent from canonical data: {column}")
        groups = {}
        for value, group in test.groupby(column, dropna=False, sort=True):
            support = {
                "unique_interactions": int(group["source_row_id"].nunique()),
                "unique_students": int(group["student_id"].nunique()),
            }
            key = str(value)
            if support["unique_interactions"] < int(audit["minimum_test_rows"]) or support["unique_students"] < int(audit["minimum_test_students"]):
                groups[key] = {"status": "insufficient_evidence", "support": support}
            else:
                groups[key] = {
                    "status": "reported",
                    "support": support,
                    "models": {
                        name: probability_metrics(
                            group["target"].tolist(),
                            group[prediction_column].tolist(),
                            threshold=threshold,
                            calibration_bins=calibration_bins,
                        )
                        for name, prediction_column in probability_columns.items()
                    },
                }
        result["columns"][column] = groups
    return result


def _cold_start_metrics(test: pd.DataFrame, probability_columns: dict[str, str], *, threshold: float, calibration_bins: int) -> dict[str, dict[str, object]]:
    first_rows = (
        test.sort_values(["student_id", "interaction_order", "source_row_id"])
        .groupby("student_id", sort=False, as_index=False)
        .head(1)
    )
    return {
        name: probability_metrics(
            first_rows["target"].tolist(),
            first_rows[column].tolist(),
            threshold=threshold,
            calibration_bins=calibration_bins,
        )
        for name, column in probability_columns.items()
    }


def run_baseline_experiment(interactions: pd.DataFrame, *, config: dict[str, Any], split_strategy: str, seed: int) -> BaselineExperimentResult:
    """Tune on validation, evaluate once on test, and preserve audit artifacts."""

    validate_experiment_execution_config(config)
    if seed not in config["random_seeds"]:
        raise ValueError("seed must belong to the predefined experiment random_seeds")
    split_frame = _split_frame(
        build_history_features(interactions),
        split_strategy=split_strategy,
        seed=seed,
        config=config,
    )
    train = split_frame.loc[split_frame["split"] == "train"].copy()
    validation = split_frame.loc[split_frame["split"] == "validation"].copy()
    test = split_frame.loc[split_frame["split"] == "test"].copy()
    if train.empty or validation.empty or test.empty:
        raise ValueError("experiment requires non-empty train, validation, and test sets")
    if train["target"].nunique() < 2:
        raise ValueError("train partition must contain both target classes")

    execution = config["evaluation_execution"]
    threshold = float(execution["classification_threshold"])
    calibration_bins = int(execution["calibration_bins"])
    strengths = [float(value) for value in execution["smoothing_strengths"]]

    validation_predictions, test_predictions, selected = _baseline_predictions(
        train, validation, test, strengths=strengths
    )
    logistic_validation, logistic_test, logistic_params = _select_logistic(
        train, validation, test, seed=seed, config=config
    )
    validation_predictions["logistic_regression"] = logistic_validation
    test_predictions["logistic_regression"] = logistic_test
    selected["logistic_regression"] = logistic_params
    hgb_validation, hgb_test, hgb_params = _select_hgb(
        train, validation, test, seed=seed, config=config
    )
    validation_predictions["hist_gradient_boosting"] = hgb_validation
    test_predictions["hist_gradient_boosting"] = hgb_test
    selected["hist_gradient_boosting"] = hgb_params

    validation_metrics = _metrics_by_model(
        validation,
        validation_predictions,
        threshold=threshold,
        calibration_bins=calibration_bins,
    )
    test_metrics = _metrics_by_model(
        test,
        test_predictions,
        threshold=threshold,
        calibration_bins=calibration_bins,
    )
    simple_models = [
        "item_smoothed_probability",
        "skill_smoothed_probability",
        "student_history_smoothed_probability",
    ]
    best_simple = min(
        simple_models,
        key=lambda name: (float(validation_metrics[name]["log_loss"]), name),
    )
    selected["best_simple_historical_baseline"] = {
        "model": best_simple,
        "selection_partition": "validation",
        "selection_metric": "log_loss",
    }

    prediction_metadata = [
        "student_id",
        "item_id",
        "skill_ids",
        "skill_signature",
        "interaction_order",
        "source_dataset",
        "source_row_id",
        "split",
        "target",
    ]
    for subgroup_column in config["reporting"].get("subgroup_audit", {}).get("columns", []):
        if subgroup_column not in prediction_metadata:
            prediction_metadata.append(subgroup_column)
    predictions = test[prediction_metadata].copy()
    probability_columns = {}
    for name, probability in test_predictions.items():
        column = f"{name}_probability"
        predictions[column] = probability
        probability_columns[name] = column

    support = config["reporting"]["skill_support"]
    skill_metrics = _skill_metrics(
        predictions,
        probability_columns,
        minimum_rows=int(support["minimum_test_rows"]),
        minimum_students=int(support["minimum_test_students"]),
        threshold=threshold,
        calibration_bins=calibration_bins,
    )
    subgroup_metrics = _subgroup_metrics(
        predictions,
        probability_columns,
        config=config,
        threshold=threshold,
        calibration_bins=calibration_bins,
    )

    bootstrap = config["reporting"]["bootstrap"]
    iterations = int(bootstrap["iterations"])
    comparison_seed = seed + 1_000_003
    comparisons: dict[str, Any] = {
        "H1_historical_vs_global": {},
        "H2_logistic_vs_best_simple": {},
        "E1_nonlinear_vs_logistic": {},
    }
    for historical in simple_models:
        comparisons["H1_historical_vs_global"][historical] = paired_cluster_bootstrap_primary_differences(
            predictions,
            candidate_column=probability_columns[historical],
            reference_column=probability_columns["global_probability"],
            iterations=iterations,
            seed=comparison_seed,
        )
    comparisons["H2_logistic_vs_best_simple"] = {
        "reference_model": best_simple,
        "differences": paired_cluster_bootstrap_primary_differences(
            predictions,
            candidate_column=probability_columns["logistic_regression"],
            reference_column=probability_columns[best_simple],
            iterations=iterations,
            seed=comparison_seed + 1,
        ),
    }
    comparisons["E1_nonlinear_vs_logistic"] = {
        "candidate_model": "hist_gradient_boosting",
        "reference_model": "logistic_regression",
        "differences": paired_cluster_bootstrap_primary_differences(
            predictions,
            candidate_column=probability_columns["hist_gradient_boosting"],
            reference_column=probability_columns["logistic_regression"],
            iterations=iterations,
            seed=comparison_seed + 2,
        ),
    }
    cold_start = (
        _cold_start_metrics(
            predictions,
            probability_columns,
            threshold=threshold,
            calibration_bins=calibration_bins,
        )
        if split_strategy == "student_holdout"
        else None
    )
    split_columns = [
        "student_id",
        "item_id",
        "skill_ids",
        "skill_signature",
        "interaction_order",
        "source_dataset",
        "source_row_id",
        "split",
        "target",
    ]
    return BaselineExperimentResult(
        split_strategy=split_strategy,
        seed=seed,
        config_schema_version=str(config["schema_version"]),
        selected_parameters=selected,
        validation_metrics=validation_metrics,
        test_metrics=test_metrics,
        skill_metrics=skill_metrics,
        subgroup_metrics=subgroup_metrics,
        hypothesis_comparisons=comparisons,
        cold_start_slice=cold_start,
        predictions=predictions.reset_index(drop=True),
        splits=split_frame[split_columns].reset_index(drop=True),
    )


def write_baseline_artifacts(result: BaselineExperimentResult, *, output_dir: Path, source_sha256: str, config_sha256: str) -> BaselineArtifacts:
    """Persist an immutable source/config/split/seed run directory."""

    if len(source_sha256) != 64 or len(config_sha256) != 64:
        raise ValueError("source_sha256 and config_sha256 must be full 64-character digests")
    run_dir = (
        output_dir
        / f"source-{source_sha256}"
        / f"config-{config_sha256}"
        / f"{result.split_strategy}-seed-{result.seed}"
    )
    if run_dir.exists():
        raise FileExistsError(f"refusing to overwrite an existing experiment run: {run_dir}")
    run_dir.mkdir(parents=True)
    predictions_path = run_dir / "predictions.parquet"
    splits_path = run_dir / "splits.parquet"
    metrics_path = run_dir / "metrics.json"
    result.predictions.to_parquet(predictions_path, index=False, engine="pyarrow")
    result.splits.to_parquet(splits_path, index=False, engine="pyarrow")

    from tcc_prototype.manifest import sha256_file

    payload = {
        "schema_version": "1.0.0",
        "experiment_config_schema_version": result.config_schema_version,
        "split_strategy": result.split_strategy,
        "seed": result.seed,
        "source_sha256": source_sha256,
        "config_sha256": config_sha256,
        "predictions_sha256": sha256_file(predictions_path),
        "splits_sha256": sha256_file(splits_path),
        "software_versions": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "selected_parameters": result.selected_parameters,
        "validation_metrics": result.validation_metrics,
        "test_metrics": result.test_metrics,
        "by_skill": result.skill_metrics,
        "by_subgroup": result.subgroup_metrics,
        "hypothesis_comparisons": result.hypothesis_comparisons,
        "true_cold_start_slice": result.cold_start_slice,
        "interpretation_guardrail": (
            "Predictive metrics quantify technical performance in held-out interactions; "
            "they do not establish learning, competence, causality, or pedagogical efficacy."
        ),
    }
    metrics_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return BaselineArtifacts(
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        splits_path=splits_path,
    )
