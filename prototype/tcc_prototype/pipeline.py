"""End-to-end preparation pipeline for approved educational datasets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .adapters.assistments import AssistmentsAdapter
from .manifest import (
    DatasetManifest,
    ManifestError,
    load_manifest,
    sha256_file,
    verify_manifest_file,
)

ASSISTMENTS_DATASET_ID = "assistments_2009_2010_skill_builder_corrected"


@dataclass(frozen=True)
class PreparedArtifacts:
    """Paths and integrity metadata produced by one preparation run."""

    parquet_path: Path
    report_path: Path
    processed_sha256: str


def _count_skills(frame: pd.DataFrame) -> int:
    return len({skill for skills in frame["skill_ids"] for skill in skills})


def _artifact_stem(manifest: DatasetManifest) -> str:
    """Return a stable source-versioned stem using the full source digest."""

    return f"{manifest.dataset_id}-{manifest.sha256}"


def prepare_assistments(
    *,
    manifest_path: Path,
    raw_dir: Path,
    output_dir: Path,
) -> PreparedArtifacts:
    """Validate, normalize, and persist corrected ASSISTments interactions.

    The raw file is never modified. Output filenames include the full source
    digest, so a republished or otherwise changed source file does not silently
    replace artifacts produced from a previously registered source version.
    """

    manifest = load_manifest(manifest_path)
    if manifest.dataset_id != ASSISTMENTS_DATASET_ID:
        raise ManifestError(
            "prepare-assistments requires the approved ASSISTments dataset_id "
            f"{ASSISTMENTS_DATASET_ID!r}; found {manifest.dataset_id!r}"
        )

    raw_file = verify_manifest_file(manifest, raw_dir)
    source = pd.read_csv(raw_file, low_memory=False)
    normalized, quality = AssistmentsAdapter(
        source_dataset=manifest.dataset_id,
    ).normalize(source)

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_stem = _artifact_stem(manifest)
    parquet_path = output_dir / f"{artifact_stem}.parquet"
    report_path = output_dir / f"{artifact_stem}.quality.json"

    normalized.to_parquet(parquet_path, index=False, engine="pyarrow")
    processed_sha256 = sha256_file(parquet_path)

    report = {
        "dataset_id": manifest.dataset_id,
        "dataset_version": manifest.version,
        "source_filename": manifest.local_filename,
        "source_sha256": manifest.sha256,
        "processed_sha256": processed_sha256,
        "target_label_semantics": "correct_on_first_attempt_without_help",
        "interaction_order_semantics": "chronological_original_problem_log_id",
        **quality,
        "students": int(normalized["student_id"].nunique()),
        "items": int(normalized["item_id"].nunique()),
        "skills": _count_skills(normalized),
        "minimum_interaction_order": (
            int(normalized["interaction_order"].min()) if len(normalized) else None
        ),
        "maximum_interaction_order": (
            int(normalized["interaction_order"].max()) if len(normalized) else None
        ),
    }
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return PreparedArtifacts(
        parquet_path=parquet_path,
        report_path=report_path,
        processed_sha256=processed_sha256,
    )
