"""Autonomous, content-addressed execution of the TCC prototype workflow."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from .manifest import load_manifest, sha256_file
from .modeling.candidate_experiment import (
    run_candidate_experiment,
    write_candidate_artifacts,
)
from .modeling.experiment import run_baseline_experiment, write_baseline_artifacts
from .pipeline import prepare_assistments
from .reporting.teacher_report import build_teacher_report

RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
GIT_COMMIT_PATTERN = re.compile(r"^[a-f0-9]{40}$")
ALLOWED_SPLITS = {"cold_start", "temporal"}


@dataclass(frozen=True)
class WorkflowResult:
    """Top-level artifacts produced by an autonomous execution."""

    run_directory: Path
    manifest_path: Path
    teacher_report_path: Path | None


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _artifact_records(run_directory: Path, *, exclude: set[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(run_directory.rglob("*"), key=lambda value: value.as_posix()):
        if not path.is_file() or path in exclude:
            continue
        relative = path.relative_to(run_directory)
        if "raw" in relative.parts:
            raise ValueError(f"raw data cannot be registered as a run artifact: {relative}")
        records.append(
            {
                "path": relative.as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return records


def _package_versions() -> dict[str, str]:
    versions: dict[str, str] = {"python": sys.version.split()[0]}
    for distribution in ("pandas", "pyarrow", "scikit-learn", "gdown"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = "not-installed"
    return versions


def _configuration_digest(configuration: dict[str, Any]) -> str:
    payload = json.dumps(configuration, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return _sha256_bytes(payload)


def run_autonomous_workflow(
    *,
    source_manifest_path: Path,
    raw_dir: Path,
    output_root: Path,
    run_id: str,
    git_commit: str,
    seeds: list[int],
    split_strategies: list[str],
    pseudonym_salt: str,
    dataset_label: str,
    model_version: str,
    n_estimators: int = 300,
    min_samples_leaf: int = 5,
    minimum_profile_evidence: int = 5,
    minimum_skill_rows: int = 100,
    explanation_rows: int = 20,
    permutation_repeats: int = 5,
    preferred_report_split: str = "temporal",
    preferred_report_seed: int = 2026,
    generated_at: datetime | None = None,
) -> WorkflowResult:
    """Execute preparation, baselines, candidate models, profiles, and report.

    Every run uses a new directory and records content hashes for all derived
    artifacts. Raw files are never copied into the run directory.
    """

    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("run_id must use only letters, numbers, dot, underscore, or hyphen")
    if not GIT_COMMIT_PATTERN.fullmatch(git_commit):
        raise ValueError("git_commit must be a full 40-character lowercase Git SHA")
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError("seeds must be a non-empty list of unique integers")
    if not split_strategies or len(set(split_strategies)) != len(split_strategies):
        raise ValueError("split_strategies must be non-empty and unique")
    unknown_splits = sorted(set(split_strategies).difference(ALLOWED_SPLITS))
    if unknown_splits:
        raise ValueError("unsupported split strategies: " + ", ".join(unknown_splits))
    if preferred_report_split not in split_strategies:
        raise ValueError("preferred report split must be executed")
    if preferred_report_seed not in seeds:
        raise ValueError("preferred report seed must be executed")
    if not pseudonym_salt:
        raise ValueError("pseudonym_salt is required")

    run_directory = output_root / run_id
    if run_directory.exists():
        raise FileExistsError(f"run directory already exists: {run_directory}")
    run_directory.mkdir(parents=True)

    timestamp = generated_at or datetime.now(UTC)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)

    source_manifest = load_manifest(source_manifest_path)
    provenance_directory = run_directory / "provenance"
    provenance_directory.mkdir()
    copied_manifest = provenance_directory / "source_manifest.json"
    shutil.copy2(source_manifest_path, copied_manifest)

    prepared_directory = run_directory / "prepared"
    prepared = prepare_assistments(
        manifest_path=source_manifest_path,
        raw_dir=raw_dir,
        output_dir=prepared_directory,
    )
    interactions = pd.read_parquet(prepared.parquet_path)

    configuration = {
        "seeds": seeds,
        "split_strategies": split_strategies,
        "n_estimators": n_estimators,
        "min_samples_leaf": min_samples_leaf,
        "minimum_profile_evidence": minimum_profile_evidence,
        "minimum_skill_rows": minimum_skill_rows,
        "explanation_rows": explanation_rows,
        "permutation_repeats": permutation_repeats,
        "preferred_report_split": preferred_report_split,
        "preferred_report_seed": preferred_report_seed,
        "ordinal_levels_enabled": False,
        "binary_alert_enabled": False,
    }
    experiments: list[dict[str, Any]] = []
    preferred_candidate = None
    preferred_candidate_artifacts = None

    for split_strategy in split_strategies:
        for seed in seeds:
            experiment_directory = (
                run_directory / "experiments" / split_strategy / f"seed-{seed}"
            )
            baseline_result = run_baseline_experiment(
                interactions,
                split_strategy=split_strategy,
                seed=seed,
                minimum_skill_rows=minimum_skill_rows,
            )
            baseline_artifacts = write_baseline_artifacts(
                baseline_result,
                output_dir=experiment_directory / "baseline",
            )
            candidate_result = run_candidate_experiment(
                interactions,
                split_strategy=split_strategy,
                seed=seed,
                n_estimators=n_estimators,
                min_samples_leaf=min_samples_leaf,
                minimum_profile_evidence=minimum_profile_evidence,
                explanation_rows=explanation_rows,
                permutation_repeats=permutation_repeats,
            )
            candidate_artifacts = write_candidate_artifacts(
                candidate_result,
                output_dir=experiment_directory / "candidate",
            )
            experiments.append(
                {
                    "split_strategy": split_strategy,
                    "seed": seed,
                    "test_rows": len(candidate_result.predictions),
                    "profile_rows": len(candidate_result.skill_profiles),
                    "baseline_metrics": baseline_artifacts.metrics_path.relative_to(
                        run_directory
                    ).as_posix(),
                    "candidate_metrics": candidate_artifacts.metrics_path.relative_to(
                        run_directory
                    ).as_posix(),
                }
            )
            if (
                split_strategy == preferred_report_split
                and seed == preferred_report_seed
            ):
                preferred_candidate = candidate_result
                preferred_candidate_artifacts = candidate_artifacts

    if preferred_candidate is None or preferred_candidate_artifacts is None:
        raise AssertionError("preferred candidate execution was not produced")

    report_directory = run_directory / "report"
    teacher_report_path = report_directory / "teacher-report.html"
    metrics_payload = json.loads(
        preferred_candidate_artifacts.metrics_path.read_text(encoding="utf-8")
    )
    build_teacher_report(
        profiles=preferred_candidate.skill_profiles,
        metrics=metrics_payload,
        importance=preferred_candidate.permutation_importance,
        output_path=teacher_report_path,
        pseudonym_salt=pseudonym_salt,
        dataset_label=dataset_label,
        model_version=model_version,
    )

    manifest_path = run_directory / "run.manifest.json"
    manifest = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "generated_at": timestamp.isoformat(),
        "git_commit": git_commit,
        "environment": _package_versions(),
        "dataset": {
            "dataset_id": source_manifest.dataset_id,
            "version": source_manifest.version,
            "source_sha256": source_manifest.sha256,
            "source_size_bytes": source_manifest.size_bytes,
            "source_manifest": copied_manifest.relative_to(run_directory).as_posix(),
            "processed_sha256": prepared.processed_sha256,
            "raw_data_included": False,
            "redistribution_allowed": source_manifest.redistribution_allowed,
        },
        "configuration": configuration,
        "configuration_sha256": _configuration_digest(configuration),
        "experiments": experiments,
        "teacher_report": {
            "path": teacher_report_path.relative_to(run_directory).as_posix(),
            "split_strategy": preferred_report_split,
            "seed": preferred_report_seed,
            "student_identifiers": "salted_sha256_pseudonyms",
        },
        "scientific_limits": [
            "Predictive metrics do not demonstrate educational effectiveness.",
            "Skill profiles are operational estimates, not definitive diagnoses.",
            "Ordinal labels and binary alerts remain disabled.",
            "Results apply to the analyzed dataset and declared split protocols.",
        ],
    }
    manifest["artifacts"] = _artifact_records(
        run_directory,
        exclude={manifest_path},
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return WorkflowResult(
        run_directory=run_directory,
        manifest_path=manifest_path,
        teacher_report_path=teacher_report_path,
    )
