"""Build auditable skill-evidence artifacts from a frozen experiment run."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .manifest import sha256_file
from .modeling.explanations import reconstruct_logistic_explanations
from .profiles import build_skill_profiles, validate_profile_config


@dataclass(frozen=True)
class ProfileArtifacts:
    """Paths emitted by one immutable profile-analysis run."""

    profile_path: Path
    explanations_path: Path
    permutation_importance_path: Path
    manifest_path: Path


def _require_sha256(value: str, *, name: str) -> str:
    if (
        len(value) != 64
        or value != value.lower()
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{name} must be a full lowercase SHA-256 digest")
    return value


def verify_profile_input_provenance(
    input_path: Path,
    experiment_run_dir: Path,
) -> dict[str, str]:
    """Verify that profile generation uses the processed input bound to the run."""

    provenance_path = experiment_run_dir / "input-provenance.json"
    try:
        payload = json.loads(provenance_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"unable to read experiment input provenance {provenance_path}: {exc}"
        ) from exc

    required = {
        "processed_input_sha256",
        "source_sha256",
        "experiment_config_sha256",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(
            "experiment input provenance is missing fields: " + ", ".join(missing)
        )

    processed_input_sha256 = _require_sha256(
        str(payload["processed_input_sha256"]),
        name="processed_input_sha256",
    )
    source_sha256 = _require_sha256(
        str(payload["source_sha256"]),
        name="source_sha256",
    )
    experiment_config_sha256 = _require_sha256(
        str(payload["experiment_config_sha256"]),
        name="experiment_config_sha256",
    )
    actual_input_sha256 = sha256_file(input_path)
    if actual_input_sha256 != processed_input_sha256:
        raise ValueError(
            "processed input SHA-256 mismatch: the profile input does not match "
            "the canonical artifact registered by the experiment run"
        )

    return {
        "processed_input_sha256": processed_input_sha256,
        "source_sha256": source_sha256,
        "experiment_config_sha256": experiment_config_sha256,
        "input_provenance_sha256": sha256_file(provenance_path),
    }


def build_profile_artifacts(
    interactions: pd.DataFrame,
    *,
    experiment_run_dir: Path,
    profile_config: dict,
    profile_config_sha256: str,
    output_dir: Path,
    explanation_rows: int = 20,
    permutation_repeats: int = 5,
) -> ProfileArtifacts:
    """Consume one frozen #13 run without creating a new split or tuning cycle."""

    validate_profile_config(profile_config)
    profile_config_sha256 = _require_sha256(
        profile_config_sha256,
        name="profile_config_sha256",
    )
    if explanation_rows < 0:
        raise ValueError("explanation_rows must be non-negative")
    if permutation_repeats < 1:
        raise ValueError("permutation_repeats must be positive")

    metrics_path = experiment_run_dir / "metrics.json"
    predictions_path = experiment_run_dir / "predictions.parquet"
    splits_path = experiment_run_dir / "splits.parquet"
    try:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read experiment metrics {metrics_path}: {exc}") from exc

    predictions_sha256 = sha256_file(predictions_path)
    splits_sha256 = sha256_file(splits_path)
    if metrics.get("predictions_sha256") != predictions_sha256:
        raise ValueError("experiment predictions SHA-256 does not match metrics.json")
    if metrics.get("splits_sha256") != splits_sha256:
        raise ValueError("experiment splits SHA-256 does not match metrics.json")

    probability_source = str(profile_config["probability_source"])
    if probability_source not in metrics.get("validation_metrics", {}):
        raise ValueError(
            "profile probability_source is not a model registered in validation_metrics"
        )
    probability_column = f"{probability_source}_probability"

    predictions = pd.read_parquet(predictions_path)
    splits = pd.read_parquet(splits_path)
    if probability_column not in predictions.columns:
        raise ValueError(
            f"experiment predictions do not contain profile source column {probability_column}"
        )

    profile = build_skill_profiles(
        predictions,
        probability_column=probability_column,
        minimum_evidence=int(profile_config["minimum_student_skill_interactions"]),
    )

    selected_parameters = metrics.get("selected_parameters", {}).get(
        "logistic_regression"
    )
    if not isinstance(selected_parameters, dict):
        raise ValueError("experiment metrics do not register logistic parameters")
    reconstruction = reconstruct_logistic_explanations(
        interactions,
        splits=splits,
        predictions=predictions,
        selected_parameters=selected_parameters,
        seed=int(metrics["seed"]),
        explanation_rows=explanation_rows,
        probability_tolerance=1e-12,
        permutation_repeats=permutation_repeats,
    )

    experiment_metrics_sha256 = sha256_file(metrics_path)
    run_dir = (
        output_dir
        / f"experiment-{experiment_metrics_sha256}"
        / f"profile-{profile_config_sha256}"
    )
    if run_dir.exists():
        raise FileExistsError(f"refusing to overwrite an existing profile run: {run_dir}")
    run_dir.mkdir(parents=True)

    profile_path = run_dir / "skill-profiles.parquet"
    explanations_path = run_dir / "logistic-explanations.json"
    permutation_importance_path = run_dir / "logistic-permutation-importance.csv"
    manifest_path = run_dir / "profile-manifest.json"

    profile.to_parquet(profile_path, index=False, engine="pyarrow")
    explanations_path.write_text(
        json.dumps(reconstruction.explanations, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    reconstruction.permutation_importance.to_csv(
        permutation_importance_path,
        index=False,
    )

    manifest = {
        "schema_version": "1.0.0",
        "source_sha256": metrics.get("source_sha256"),
        "experiment_config_sha256": metrics.get("config_sha256"),
        "experiment_metrics_sha256": experiment_metrics_sha256,
        "experiment_predictions_sha256": predictions_sha256,
        "experiment_splits_sha256": splits_sha256,
        "profile_config_sha256": profile_config_sha256,
        "probability_source": probability_source,
        "minimum_student_skill_interactions": int(
            profile_config["minimum_student_skill_interactions"]
        ),
        "explanation_rows": explanation_rows,
        "permutation_repeats": permutation_repeats,
        "skill_profiles_sha256": sha256_file(profile_path),
        "logistic_explanations_sha256": sha256_file(explanations_path),
        "logistic_permutation_importance_sha256": sha256_file(
            permutation_importance_path
        ),
        "logistic_probability_reproduction_max_abs_error": (
            reconstruction.max_abs_probability_error
        ),
        "interpretation_guardrail": (
            "Skill profiles summarize held-out performance evidence and contextual "
            "prediction probabilities; they do not measure mastery, learning, latent "
            "competence, causality, or pedagogical effectiveness. Logistic explanations "
            "describe model computation and predictive dependence only."
        ),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return ProfileArtifacts(
        profile_path=profile_path,
        explanations_path=explanations_path,
        permutation_importance_path=permutation_importance_path,
        manifest_path=manifest_path,
    )
