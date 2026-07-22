import hashlib
import json
from pathlib import Path

import pytest

from tcc_prototype.manifest import ManifestError, load_manifest, verify_manifest_file


def test_verify_manifest_accepts_matching_file(tmp_path: Path) -> None:
    raw_file = tmp_path / "assistments.csv"
    raw_file.write_bytes(b"student,item,correct\n1,10,1\n")
    digest = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": "assistments_2009_2010_skill_builder_corrected",
                "version": "corrected",
                "canonical_url": "https://example.org/dataset",
                "accessed_at": "2026-07-22T00:00:00Z",
                "local_filename": raw_file.name,
                "sha256": digest,
                "size_bytes": raw_file.stat().st_size,
                "license_or_terms": "free to use; cite source page",
                "redistribution_allowed": False,
                "acquisition_method": "manual_download",
            }
        ),
        encoding="utf-8",
    )

    manifest = load_manifest(manifest_path)

    assert verify_manifest_file(manifest, tmp_path) == raw_file


def test_verify_manifest_rejects_hash_mismatch(tmp_path: Path) -> None:
    raw_file = tmp_path / "assistments.csv"
    raw_file.write_text("changed", encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": "assistments",
                "version": "v1",
                "canonical_url": "https://example.org/dataset",
                "accessed_at": "2026-07-22T00:00:00Z",
                "local_filename": raw_file.name,
                "sha256": "0" * 64,
                "license_or_terms": "terms",
                "redistribution_allowed": False,
                "acquisition_method": "manual_download",
            }
        ),
        encoding="utf-8",
    )

    manifest = load_manifest(manifest_path)

    with pytest.raises(ManifestError, match="SHA-256 mismatch"):
        verify_manifest_file(manifest, tmp_path)


def test_terms_controlled_manifest_requires_acceptance_metadata(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": "assistments",
                "version": "corrected",
                "canonical_url": "https://example.org/dataset",
                "accessed_at": "2026-07-22T00:00:00Z",
                "local_filename": "assistments.csv",
                "sha256": "0" * 64,
                "license_or_terms": "controlled terms",
                "redistribution_allowed": False,
                "acquisition_method": "terms_acceptance_required",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match="terms-controlled manifest"):
        load_manifest(manifest_path)


def test_terms_controlled_manifest_preserves_purpose_and_acceptance(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": "assistments",
                "version": "corrected",
                "canonical_url": "https://example.org/dataset",
                "accessed_at": "2026-07-22T00:00:00Z",
                "local_filename": "assistments.csv",
                "sha256": "0" * 64,
                "license_or_terms": "controlled terms",
                "terms_url": "https://example.org/terms",
                "terms_accepted_at": "2026-07-22T00:00:00Z",
                "research_purpose": "TCC experiment",
                "redistribution_allowed": False,
                "acquisition_method": "terms_acceptance_required",
            }
        ),
        encoding="utf-8",
    )

    manifest = load_manifest(manifest_path)

    assert manifest.terms_url == "https://example.org/terms"
    assert manifest.terms_accepted_at == "2026-07-22T00:00:00Z"
    assert manifest.research_purpose == "TCC experiment"
