import hashlib
import json
from pathlib import Path

import pandas as pd

from tcc_prototype.manifest import DatasetManifest
from tcc_prototype.pipeline import _artifact_stem, prepare_assistments


def test_artifact_stem_distinguishes_source_file_versions() -> None:
    first = DatasetManifest(
        dataset_id="assistments_2009_2010_skill_builder_corrected",
        version="corrected",
        canonical_url="https://example.org/dataset",
        accessed_at="2026-07-22T00:00:00Z",
        local_filename="assistments.csv",
        sha256="a" * 64,
        license_or_terms="terms",
        redistribution_allowed=False,
        acquisition_method="manual_download",
    )
    second = DatasetManifest(
        **{**first.__dict__, "sha256": "b" * 64},
    )

    assert _artifact_stem(first) != _artifact_stem(second)
    assert _artifact_stem(first).endswith("-aaaaaaaaaaaa")


def test_prepare_assistments_writes_parquet_and_quality_report(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "processed"
    raw_dir.mkdir()
    raw_file = raw_dir / "assistments.csv"
    pd.DataFrame(
        {
            "user_id": [1, 1, 2],
            "problem_id": [10, 20, 10],
            "skill_id": ["fractions", "ratio", "fractions"],
            "order_id": [1, 2, 1],
            "correct": [1, 0, 1],
        }
    ).to_csv(raw_file, index=False)
    digest = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": "assistments_2009_2010_skill_builder_corrected",
                "version": "corrected-test",
                "canonical_url": "https://example.org/dataset",
                "accessed_at": "2026-07-22T00:00:00Z",
                "local_filename": raw_file.name,
                "sha256": digest,
                "size_bytes": raw_file.stat().st_size,
                "license_or_terms": "test fixture",
                "redistribution_allowed": False,
                "acquisition_method": "manual_download",
            }
        ),
        encoding="utf-8",
    )

    artifacts = prepare_assistments(
        manifest_path=manifest_path,
        raw_dir=raw_dir,
        output_dir=output_dir,
    )

    assert artifacts.parquet_path.exists()
    assert artifacts.report_path.exists()
    assert digest[:12] in artifacts.parquet_path.name
    prepared = pd.read_parquet(artifacts.parquet_path)
    report = json.loads(artifacts.report_path.read_text(encoding="utf-8"))
    assert len(prepared) == 3
    assert report["dataset_id"] == "assistments_2009_2010_skill_builder_corrected"
    assert report["students"] == 2
    assert report["items"] == 2
    assert report["skills"] == 2
    assert report["processed_sha256"] == artifacts.processed_sha256
    assert report["target_label_semantics"] == "correct_on_first_attempt_without_help"
    assert report["interaction_order_semantics"] == "chronological_original_problem_log_id"
