import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from tcc_prototype.acquisition import AcquisitionError, acquire_assistments


def test_acquisition_requires_explicit_terms_acceptance(tmp_path: Path) -> None:
    with pytest.raises(AcquisitionError, match="explicit acceptance"):
        acquire_assistments(
            raw_dir=tmp_path / "raw",
            manifest_dir=tmp_path / "manifests",
            purpose="TCC research",
            accept_terms=False,
            downloader=lambda _file_id, _path: None,
        )


def test_acquisition_requires_a_recorded_research_purpose(tmp_path: Path) -> None:
    with pytest.raises(AcquisitionError, match="research purpose"):
        acquire_assistments(
            raw_dir=tmp_path / "raw",
            manifest_dir=tmp_path / "manifests",
            purpose="   ",
            accept_terms=True,
            downloader=lambda _file_id, _path: None,
        )


def test_acquisition_downloads_and_writes_a_nonredistributable_manifest(
    tmp_path: Path,
) -> None:
    payload = b"user_id,problem_id,skill_id,order_id,correct\n1,2,fractions,1,1\n"

    def fake_download(file_id: str, output_path: Path) -> None:
        assert file_id == "1NNXHFRxcArrU0ZJSb9BIL56vmUt5FhlE"
        output_path.write_bytes(payload)

    result = acquire_assistments(
        raw_dir=tmp_path / "raw",
        manifest_dir=tmp_path / "manifests",
        purpose="Reproducible TCC experiment on mathematical skill profiles",
        accept_terms=True,
        downloader=fake_download,
        now=datetime(2026, 7, 22, 12, 0, tzinfo=UTC),
    )

    assert result.raw_path.exists()
    assert result.manifest_path.exists()
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["sha256"] == hashlib.sha256(payload).hexdigest()
    assert manifest["redistribution_allowed"] is False
    assert manifest["acquisition_method"] == "terms_acceptance_required"
    assert manifest["research_purpose"].startswith("Reproducible TCC")
    assert manifest["terms_accepted_at"] == "2026-07-22T12:00:00+00:00"
    assert "termsofuseforusingdata" in manifest["terms_url"]


def test_acquisition_rejects_an_empty_download(tmp_path: Path) -> None:
    def empty_download(_file_id: str, output_path: Path) -> None:
        output_path.touch()

    with pytest.raises(AcquisitionError, match="empty file"):
        acquire_assistments(
            raw_dir=tmp_path / "raw",
            manifest_dir=tmp_path / "manifests",
            purpose="TCC research",
            accept_terms=True,
            downloader=empty_download,
        )
