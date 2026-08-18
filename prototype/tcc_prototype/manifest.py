"""Dataset manifest loading and integrity verification."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")
DATASET_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ACQUISITION_METHODS = {
    "official_public_download",
    "public_download",
    "manual_download",
    "terms_acceptance_required",
}
REQUIRED_FIELDS = {
    "dataset_id",
    "version",
    "canonical_url",
    "accessed_at",
    "local_filename",
    "sha256",
    "license_or_terms",
    "redistribution_allowed",
    "acquisition_method",
}


class ManifestError(ValueError):
    """Raised when a dataset manifest or referenced file is invalid."""


@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    version: str
    canonical_url: str
    accessed_at: str
    local_filename: str
    sha256: str
    license_or_terms: str
    redistribution_allowed: bool
    acquisition_method: str
    size_bytes: int | None = None
    download_url: str | None = None
    notes: tuple[str, ...] = ()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Calculate the SHA-256 digest of a file without loading it all in memory."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> DatasetManifest:
    """Load a JSON manifest and validate its required fields and value contract."""

    try:
        payload: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"unable to read manifest {path}: {exc}") from exc

    missing = sorted(REQUIRED_FIELDS.difference(payload))
    if missing:
        raise ManifestError("manifest is missing fields: " + ", ".join(missing))

    dataset_id = payload["dataset_id"]
    if not isinstance(dataset_id, str) or not DATASET_ID_PATTERN.fullmatch(dataset_id):
        raise ManifestError("dataset_id contains unsafe characters")

    local_filename = payload["local_filename"]
    if (
        not isinstance(local_filename, str)
        or not local_filename
        or local_filename in {".", ".."}
        or "/" in local_filename
        or "\\" in local_filename
        or Path(local_filename).is_absolute()
    ):
        raise ManifestError("local_filename must be a file name without directories")

    digest = payload["sha256"]
    if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
        raise ManifestError("manifest sha256 must contain 64 lowercase hex characters")

    redistribution_allowed = payload["redistribution_allowed"]
    if not isinstance(redistribution_allowed, bool):
        raise ManifestError("redistribution_allowed must be boolean")

    acquisition_method = payload["acquisition_method"]
    if acquisition_method not in ACQUISITION_METHODS:
        raise ManifestError(f"unsupported acquisition_method: {acquisition_method}")

    size = payload.get("size_bytes")
    if size is not None and (not isinstance(size, int) or isinstance(size, bool) or size < 0):
        raise ManifestError("manifest size_bytes must be a non-negative integer")

    notes = payload.get("notes", [])
    if not isinstance(notes, list) or not all(isinstance(note, str) for note in notes):
        raise ManifestError("manifest notes must be a list of strings")

    return DatasetManifest(
        dataset_id=dataset_id,
        version=str(payload["version"]),
        canonical_url=str(payload["canonical_url"]),
        accessed_at=str(payload["accessed_at"]),
        local_filename=local_filename,
        sha256=digest,
        license_or_terms=str(payload["license_or_terms"]),
        redistribution_allowed=redistribution_allowed,
        acquisition_method=str(acquisition_method),
        size_bytes=size,
        download_url=(
            str(payload["download_url"]) if payload.get("download_url") else None
        ),
        notes=tuple(notes),
    )


def verify_manifest_file(manifest: DatasetManifest, raw_dir: Path) -> Path:
    """Verify file presence, optional size, and SHA-256 against a manifest."""

    path = raw_dir / manifest.local_filename
    if not path.is_file():
        raise ManifestError(f"dataset file not found: {path}")

    actual_size = path.stat().st_size
    if manifest.size_bytes is not None and actual_size != manifest.size_bytes:
        raise ManifestError(
            f"size mismatch for {path.name}: expected {manifest.size_bytes}, "
            f"found {actual_size}"
        )

    actual_digest = sha256_file(path)
    if actual_digest != manifest.sha256:
        raise ManifestError(
            f"SHA-256 mismatch for {path.name}: expected {manifest.sha256}, "
            f"found {actual_digest}"
        )
    return path
