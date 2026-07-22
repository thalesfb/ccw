import hashlib
import json
from pathlib import Path

import pandas as pd

from tcc_prototype.workflow import run_autonomous_workflow


def test_autonomous_workflow_produces_content_addressed_run(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    manifest_dir = tmp_path / "manifests"
    output_root = tmp_path / "runs"
    raw_dir.mkdir()
    manifest_dir.mkdir()
    raw_file = raw_dir / "assistments.csv"

    rows = []
    for student in range(12):
        for order in range(10):
            rows.append(
                {
                    "user_id": student,
                    "problem_id": order % 4,
                    "skill_id": "fractions" if order % 2 == 0 else "ratio",
                    "order_id": order,
                    "correct": int((student + order) % 3 != 0),
                }
            )
    pd.DataFrame(rows).to_csv(raw_file, index=False)
    digest = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    source_manifest = manifest_dir / "assistments.json"
    source_manifest.write_text(
        json.dumps(
            {
                "dataset_id": "assistments_test",
                "version": "fixture-v1",
                "canonical_url": "https://example.org/assistments",
                "accessed_at": "2026-07-22T00:00:00Z",
                "local_filename": raw_file.name,
                "sha256": digest,
                "size_bytes": raw_file.stat().st_size,
                "license_or_terms": "synthetic fixture",
                "redistribution_allowed": False,
                "acquisition_method": "manual_download",
            }
        ),
        encoding="utf-8",
    )

    result = run_autonomous_workflow(
        source_manifest_path=source_manifest,
        raw_dir=raw_dir,
        output_root=output_root,
        run_id="fixture-run",
        git_commit="a" * 40,
        seeds=[2026],
        split_strategies=["cold_start", "temporal"],
        n_estimators=20,
        min_samples_leaf=1,
        minimum_profile_evidence=1,
        minimum_skill_rows=1,
        explanation_rows=2,
        permutation_repeats=2,
        preferred_report_split="temporal",
        preferred_report_seed=2026,
        pseudonym_salt="test-salt",
        dataset_label="Synthetic ASSISTments fixture",
        model_version="test",
    )

    assert result.run_directory == output_root / "fixture-run"
    assert result.manifest_path.exists()
    assert result.teacher_report_path is not None
    assert result.teacher_report_path.exists()
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["git_commit"] == "a" * 40
    assert manifest["dataset"]["source_sha256"] == digest
    assert manifest["configuration"]["seeds"] == [2026]
    assert manifest["configuration"]["split_strategies"] == [
        "cold_start",
        "temporal",
    ]
    assert len(manifest["experiments"]) == 2
    assert manifest["teacher_report"]["split_strategy"] == "temporal"
    assert manifest["teacher_report"]["seed"] == 2026
    assert all(record["sha256"] for record in manifest["artifacts"])
    assert "raw" not in {Path(record["path"]).parts[0] for record in manifest["artifacts"]}
    html = result.teacher_report_path.read_text(encoding="utf-8")
    assert "Synthetic ASSISTments fixture" in html
    assert "não constitui diagnóstico definitivo" in html


def test_autonomous_workflow_rejects_invalid_commit(tmp_path: Path) -> None:
    try:
        run_autonomous_workflow(
            source_manifest_path=tmp_path / "missing.json",
            raw_dir=tmp_path,
            output_root=tmp_path,
            run_id="run",
            git_commit="short",
            seeds=[2026],
            split_strategies=["temporal"],
            pseudonym_salt="salt",
            dataset_label="fixture",
            model_version="test",
        )
    except ValueError as error:
        assert "40-character" in str(error)
    else:
        raise AssertionError("invalid Git commits must fail before data access")


def test_autonomous_workflow_refuses_existing_run_directory(tmp_path: Path) -> None:
    existing = tmp_path / "run"
    existing.mkdir()

    try:
        run_autonomous_workflow(
            source_manifest_path=tmp_path / "missing.json",
            raw_dir=tmp_path,
            output_root=tmp_path,
            run_id="run",
            git_commit="a" * 40,
            seeds=[2026],
            split_strategies=["temporal"],
            pseudonym_salt="salt",
            dataset_label="fixture",
            model_version="test",
        )
    except FileExistsError as error:
        assert "already exists" in str(error)
    else:
        raise AssertionError("existing run directories must not be overwritten")
