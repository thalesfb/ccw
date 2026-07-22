import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from tcc_prototype.academic import AcademicArtifactError, generate_academic_artifacts


def _write_artifact(run_dir: Path, relative: str, content: bytes) -> dict[str, object]:
    path = run_dir / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {
        "path": relative,
        "size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def _complete_run(tmp_path: Path, *, dataset_id: str = "approved_math") -> tuple[Path, Path]:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    source_manifest = {
        "dataset_id": dataset_id,
        "version": "v1",
        "canonical_url": "https://example.org/data",
        "accessed_at": "2026-07-22T00:00:00Z",
        "local_filename": "source.csv",
        "sha256": "a" * 64,
        "size_bytes": 100,
        "license_or_terms": "research terms",
        "redistribution_allowed": False,
        "acquisition_method": "terms_acceptance_required",
        "terms_url": "https://example.org/terms",
        "terms_accepted_at": "2026-07-22T00:00:00Z",
        "research_purpose": "TCC experiment",
    }
    source_record = _write_artifact(
        run_dir,
        "provenance/source_manifest.json",
        (json.dumps(source_manifest) + "\n").encode(),
    )
    quality = {
        "dataset_id": dataset_id,
        "dataset_version": "v1",
        "input_rows": 120,
        "duplicate_rows_removed": 2,
        "invalid_rows_removed": 1,
        "output_rows": 117,
        "students": 12,
        "items": 20,
        "skills": 4,
    }
    quality_record = _write_artifact(
        run_dir,
        f"prepared/{dataset_id}.quality.json",
        (json.dumps(quality) + "\n").encode(),
    )
    metrics = {
        "split_strategy": "temporal",
        "seed": 2026,
        "models": {
            "global_probability": {
                "observations": 24,
                "log_loss": 0.69,
                "brier_score": 0.25,
                "roc_auc": 0.5,
                "expected_calibration_error": 0.12,
            },
            "logistic_regression": {
                "observations": 24,
                "log_loss": 0.61,
                "brier_score": 0.21,
                "roc_auc": 0.71,
                "expected_calibration_error": 0.08,
            },
            "random_forest": {
                "observations": 24,
                "log_loss": 0.58,
                "brier_score": 0.19,
                "roc_auc": 0.76,
                "expected_calibration_error": 0.06,
            },
        },
        "by_skill": {},
    }
    metrics_record = _write_artifact(
        run_dir,
        "experiments/temporal/seed-2026/candidate/candidate_temporal_seed_2026.metrics.json",
        (json.dumps(metrics) + "\n").encode(),
    )
    profiles = pd.DataFrame(
        {
            "student_id": ["s1", "s1", "s2"],
            "skill_id": ["fractions", "ratio", "fractions"],
            "evidence_count": [5, 3, 7],
            "predicted_probability": [0.4, 0.7, 0.8],
            "prediction_std": [0.1, 0.05, 0.03],
            "observed_accuracy": [0.4, 0.67, 0.86],
            "observed_accuracy_lower": [0.12, 0.21, 0.49],
            "observed_accuracy_upper": [0.77, 0.94, 0.97],
            "evidence_status": ["estimated", "estimated", "estimated"],
            "level": [None, None, None],
            "threshold_version": [None, None, None],
            "interpretation_limit": ["not a diagnosis"] * 3,
        }
    )
    profile_path = run_dir / "experiments/temporal/seed-2026/candidate/candidate_temporal_seed_2026.skill_profiles.parquet"
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profiles.to_parquet(profile_path, index=False)
    profile_record = {
        "path": profile_path.relative_to(run_dir).as_posix(),
        "size_bytes": profile_path.stat().st_size,
        "sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
    }
    manifest = {
        "schema_version": "1.0.0",
        "run_id": "approved-run",
        "generated_at": "2026-07-22T00:00:00Z",
        "git_commit": "b" * 40,
        "dataset": {
            "dataset_id": dataset_id,
            "version": "v1",
            "source_sha256": "a" * 64,
            "source_manifest": source_record["path"],
            "processed_sha256": "c" * 64,
            "raw_data_included": False,
            "redistribution_allowed": False,
        },
        "configuration": {
            "seeds": [2026],
            "split_strategies": ["temporal"],
            "ordinal_levels_enabled": False,
            "binary_alert_enabled": False,
        },
        "experiments": [
            {
                "split_strategy": "temporal",
                "seed": 2026,
                "candidate_metrics": metrics_record["path"],
            }
        ],
        "teacher_report": {
            "split_strategy": "temporal",
            "seed": 2026,
        },
        "artifacts": [source_record, quality_record, metrics_record, profile_record],
    }
    manifest_path = run_dir / "run.manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    approved = tmp_path / "sources.json"
    approved.write_text(
        json.dumps(
            {
                "sources": [
                    {"id": "approved_math", "role": "primary", "domain": "mathematics"}
                ]
            }
        ),
        encoding="utf-8",
    )
    return manifest_path, approved


def test_generate_academic_artifacts_writes_traceable_latex(tmp_path: Path) -> None:
    manifest_path, approved = _complete_run(tmp_path)
    output_dir = tmp_path / "latex"

    artifacts = generate_academic_artifacts(
        run_manifest_path=manifest_path,
        approved_sources_path=approved,
        output_dir=output_dir,
    )

    assert artifacts.model_comparison_path.exists()
    assert artifacts.data_quality_path.exists()
    assert artifacts.skill_summary_path.exists()
    assert artifacts.provenance_path.exists()
    model_text = artifacts.model_comparison_path.read_text(encoding="utf-8")
    provenance_text = artifacts.provenance_path.read_text(encoding="utf-8")
    assert "Random Forest" in model_text
    assert "0{,}580" in model_text
    assert "approved-run" in provenance_text
    assert "bbbbbbbbbbbb" in provenance_text
    assert "não demonstram eficácia pedagógica" in provenance_text


def test_generation_rejects_unapproved_dataset(tmp_path: Path) -> None:
    manifest_path, approved = _complete_run(tmp_path, dataset_id="unknown")

    with pytest.raises(AcademicArtifactError, match="not approved"):
        generate_academic_artifacts(
            run_manifest_path=manifest_path,
            approved_sources_path=approved,
            output_dir=tmp_path / "latex",
        )


def test_generation_rejects_tampered_artifact(tmp_path: Path) -> None:
    manifest_path, approved = _complete_run(tmp_path)
    run_dir = manifest_path.parent
    metrics_path = next(run_dir.rglob("*.metrics.json"))
    original = metrics_path.read_text(encoding="utf-8")
    tampered = original.replace("0.58", "0.57", 1)
    assert len(tampered.encode("utf-8")) == len(original.encode("utf-8"))
    metrics_path.write_text(tampered, encoding="utf-8")

    with pytest.raises(AcademicArtifactError, match="SHA-256 mismatch"):
        generate_academic_artifacts(
            run_manifest_path=manifest_path,
            approved_sources_path=approved,
            output_dir=tmp_path / "latex",
        )


def test_generation_rejects_enabled_diagnostic_labels(tmp_path: Path) -> None:
    manifest_path, approved = _complete_run(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["configuration"]["binary_alert_enabled"] = True
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(AcademicArtifactError, match="binary alerts"):
        generate_academic_artifacts(
            run_manifest_path=manifest_path,
            approved_sources_path=approved,
            output_dir=tmp_path / "latex",
        )
