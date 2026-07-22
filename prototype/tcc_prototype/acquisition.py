"""Controlled acquisition of the approved ASSISTments dataset."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .manifest import sha256_file

ASSISTMENTS_FILE_ID = "1NNXHFRxcArrU0ZJSb9BIL56vmUt5FhlE"
ASSISTMENTS_FILENAME = "skill_builder_data_corrected_collapsed.csv"
ASSISTMENTS_DATASET_ID = "assistments_2009_2010_skill_builder_corrected"
ASSISTMENTS_CANONICAL_URL = (
    "https://sites.google.com/site/assistmentsdata/home/"
    "2009-2010-assistment-data/skill-builder-data-2009-2010"
)
ASSISTMENTS_TERMS_URL = (
    "https://sites.google.com/site/assistmentsdata/termsofuseforusingdata"
)
ASSISTMENTS_DOWNLOAD_URL = (
    "https://drive.google.com/file/d/1NNXHFRxcArrU0ZJSb9BIL56vmUt5FhlE/view"
)


class AcquisitionError(RuntimeError):
    """Raised when controlled data acquisition cannot be completed safely."""


@dataclass(frozen=True)
class AcquisitionResult:
    raw_path: Path
    manifest_path: Path
    sha256: str


def _gdown_download(file_id: str, output_path: Path) -> None:
    try:
        import gdown
    except ImportError as exc:  # pragma: no cover - installation guard
        raise AcquisitionError(
            "gdown is required for automated acquisition; install prototype dependencies"
        ) from exc
    result = gdown.download(id=file_id, output=str(output_path), quiet=False)
    if result is None:
        raise AcquisitionError("Google Drive download did not return an output file")


def acquire_assistments(
    *,
    raw_dir: Path,
    manifest_dir: Path,
    purpose: str,
    accept_terms: bool,
    downloader: Callable[[str, Path], None] | None = None,
    now: datetime | None = None,
) -> AcquisitionResult:
    """Download the corrected dataset only after explicit terms acceptance.

    The caller records a concrete research purpose and accepts the official
    non-reidentification and non-redistribution terms. The raw file remains
    outside Git and receives a machine-readable integrity manifest.
    """

    if not accept_terms:
        raise AcquisitionError(
            "explicit acceptance of the ASSISTments terms is required"
        )
    purpose = purpose.strip()
    if not purpose:
        raise AcquisitionError("a concrete research purpose must be recorded")

    timestamp = now or datetime.now(UTC)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / ASSISTMENTS_FILENAME
    partial_path = raw_dir / f"{ASSISTMENTS_FILENAME}.part"
    manifest_path = manifest_dir / f"{ASSISTMENTS_DATASET_ID}.json"
    if partial_path.exists():
        partial_path.unlink()

    download = downloader or _gdown_download
    try:
        download(ASSISTMENTS_FILE_ID, partial_path)
    except Exception as exc:
        partial_path.unlink(missing_ok=True)
        if isinstance(exc, AcquisitionError):
            raise
        raise AcquisitionError(f"unable to download ASSISTments data: {exc}") from exc

    if not partial_path.is_file() or partial_path.stat().st_size == 0:
        partial_path.unlink(missing_ok=True)
        raise AcquisitionError("download produced an empty file")
    partial_path.replace(raw_path)

    digest = sha256_file(raw_path)
    manifest = {
        "dataset_id": ASSISTMENTS_DATASET_ID,
        "version": "corrected-collapsed-one-row-per-student-problem",
        "canonical_url": ASSISTMENTS_CANONICAL_URL,
        "download_url": ASSISTMENTS_DOWNLOAD_URL,
        "accessed_at": timestamp.isoformat(),
        "local_filename": ASSISTMENTS_FILENAME,
        "sha256": digest,
        "size_bytes": raw_path.stat().st_size,
        "license_or_terms": (
            "Official ASSISTments anonymized-data terms: no reidentification, "
            "no redistribution, acknowledgement required, and research code public."
        ),
        "terms_url": ASSISTMENTS_TERMS_URL,
        "terms_accepted_at": timestamp.isoformat(),
        "research_purpose": purpose,
        "redistribution_allowed": False,
        "acquisition_method": "terms_acceptance_required",
        "notes": [
            "Do not commit or redistribute the raw dataset.",
            "Do not attempt to identify students or link records to individuals.",
            "If identifying information is discovered, delete it and notify ASSISTments.",
            "Cite the canonical dataset page and the ASSISTments system paper.",
            "Keep the analysis code public when publishing work based on this dataset.",
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return AcquisitionResult(
        raw_path=raw_path,
        manifest_path=manifest_path,
        sha256=digest,
    )
