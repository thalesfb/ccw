from __future__ import annotations

import json
from pathlib import Path

from src.validation.derived_assets import (
    ASSET_NAMES,
    MANIFEST_PATH,
    sync_derived_assets,
    validate_derived_assets,
)


def _make_repository(tmp_path: Path) -> Path:
    (tmp_path / "research" / "src").mkdir(parents=True)
    (tmp_path / "research" / "data").mkdir(parents=True)
    (tmp_path / "research" / "exports" / "analysis").mkdir(parents=True)
    (tmp_path / "research" / "exports" / "visualizations").mkdir(parents=True)
    (tmp_path / "research" / "exports" / "reports").mkdir(parents=True)

    (tmp_path / "research" / "src" / "pipeline.py").write_text(
        "PIPELINE_VERSION = 1\n", encoding="utf-8"
    )
    (tmp_path / "research" / "data" / "snapshot.csv").write_text(
        "id\n1\n", encoding="utf-8"
    )
    (tmp_path / "research" / "exports" / "analysis" / "papers.csv").write_text(
        "id,title\n1,Example\n", encoding="utf-8"
    )

    for index, name in enumerate(ASSET_NAMES, start=1):
        (tmp_path / "research" / "exports" / "visualizations" / name).write_bytes(
            f"png-{index}".encode("ascii")
        )
    return tmp_path


def test_sync_copies_all_assets_and_writes_stable_manifest(tmp_path: Path) -> None:
    repository = _make_repository(tmp_path)

    manifest_path = sync_derived_assets(repository)

    assert manifest_path == repository / MANIFEST_PATH
    assert validate_derived_assets(repository) == []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "generated_at" not in manifest
    assert len(manifest["assets"]) == len(ASSET_NAMES)


def test_validation_reports_tampered_consumer_copy(tmp_path: Path) -> None:
    repository = _make_repository(tmp_path)
    sync_derived_assets(repository)

    target = repository / "results" / "tcc" / "images" / ASSET_NAMES[0]
    target.write_bytes(b"not-the-canonical-chart")

    errors = validate_derived_assets(repository)

    assert any("tcc copy differs" in error for error in errors)
    assert any("asset hashes" in error for error in errors)


def test_validation_reports_changed_pipeline_source(tmp_path: Path) -> None:
    repository = _make_repository(tmp_path)
    sync_derived_assets(repository)
    source = repository / "research" / "src" / "pipeline.py"
    source.write_text("PIPELINE_VERSION = 2\n", encoding="utf-8")

    errors = validate_derived_assets(repository)

    assert any("source fingerprint is stale" in error for error in errors)
