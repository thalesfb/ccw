"""Validate the committed representation of the current review snapshot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = (
    REPOSITORY_ROOT
    / "research"
    / "exports"
    / "reports"
    / "reproducibility_manifest.json"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _manifest() -> dict:
    assert MANIFEST_PATH.exists(), f"Missing manifest: {MANIFEST_PATH}"
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_describes_current_snapshot_without_sqlite() -> None:
    manifest = _manifest()
    snapshot = manifest["snapshot"]
    counts = snapshot["counts"]

    assert manifest["schema_version"] == "1.0"
    assert manifest["database"]["versioned"] is False
    assert counts["total_records"] == 11904
    assert counts["selection_stage_counts"] == {
        "screening": 9413,
        "eligibility": 2475,
        "included": 16,
    }
    assert counts["prisma"] == {
        "identification": 11904,
        "screening": 11904,
        "screening_excluded": 9413,
        "eligibility": 2491,
        "eligibility_excluded": 2475,
        "included": 16,
    }
    assert snapshot["included_ids"] == [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        6916,
        6917,
        6918,
        6920,
        6921,
        6923,
    ]
    assert snapshot["candidate_audit"]["operational_candidates"] == 23
    assert snapshot["candidate_audit"]["false_positives_removed"] == 7
    assert len(snapshot["manual_overrides"]) == 7


def test_manifest_hashes_and_bibliography_scope_are_current() -> None:
    manifest = _manifest()

    for artifact in manifest["artifacts"]:
        relative_path = artifact["path"]
        assert not relative_path.lower().endswith((".sqlite", ".db"))
        path = REPOSITORY_ROOT / relative_path
        assert path.exists(), f"Missing manifest artifact: {relative_path}"
        assert _sha256(path) == artifact["sha256"], (
            f"Hash drift detected for {relative_path}; regenerate the manifest"
        )

    bibliography = manifest["bibliography"]
    assert bibliography["pipeline_derived_studies"].endswith("included_papers.bib")
    assert bibliography["complete_tcc_bibliography"] == [
        "results/tcc/referencias.bib",
        "results/tcc/referencias_pedagogicas.bib",
    ]
    assert "external to the pipeline study set" in bibliography["separation_rule"]
