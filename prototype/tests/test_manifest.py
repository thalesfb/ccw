import hashlib
import json
from pathlib import Path

import pytest

from tcc_prototype.manifest import ManifestError, load_manifest, verify_manifest_file


def _write_manifest(tmp_path: Path, **overrides: object) -> Path:
    payload: dict[str, object] = {
        "dataset_id": "assistments_2009_2010_skill_builder_corrected",
        "version": "corrected",
        "canonical_url": "https://example.org/dataset",
        "accessed_at": "2026-07-22T00:00:00Z",
        "local_filename": "assistments.csv",
        "sha256": "0" * 64,
        "license_or_terms": "free to use; cite source page",
        "redistribution_allowed": False,
        "acquisition_method": "manual_download",
    }
    payload.update(overrides)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    return manifest_path


def test_verify_manifest_accepts_matching_file(tmp_path: Path) -> None:
    raw_file = tmp_path / "assistments.csv"
    raw_file.write_bytes(b"student,item,correct\n1,10,1\n")
    digest = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    manifest_path = _write_manifest(
        tmp_path,
        sha256=digest,
        size_bytes=raw_file.stat().st_size,
    )

    manifest = load_manifest(manifest_path)

    assert verify_manifest_file(manifest, tmp_path) == raw_file


def test_verify_manifest_rejects_hash_mismatch(tmp_path: Path) -> None:
    raw_file = tmp_path / "assistments.csv"
    raw_file.write_text("changed", encoding="utf-8")
    manifest_path = _write_manifest(tmp_path)

    manifest = load_manifest(manifest_path)

    with pytest.raises(ManifestError, match="SHA-256 mismatch"):
        verify_manifest_file(manifest, tmp_path)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("version", "", "version must be a non-empty string"),
        ("canonical_url", "", "canonical_url must be a non-empty string"),
        ("accessed_at", "", "accessed_at must be a non-empty string"),
        ("license_or_terms", "", "license_or_terms must be a non-empty string"),
        ("redistribution_allowed", "false", "redistribution_allowed must be boolean"),
        ("acquisition_method", [], "unsupported acquisition_method"),
        ("acquisition_method", "scraped_download", "unsupported acquisition_method"),
        ("local_filename", "../assistments.csv", "local_filename must be a file name"),
        ("sha256", "A" * 64, "sha256 must contain 64 lowercase hex characters"),
        ("dataset_id", "../assistments", "dataset_id contains unsafe characters"),
    ],
)
def test_load_manifest_rejects_values_outside_contract(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    manifest_path = _write_manifest(tmp_path, **{field: value})

    with pytest.raises(ManifestError, match=message):
        load_manifest(manifest_path)
