"""End-to-end preparation pipeline for approved educational datasets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .adapters.assistments import AssistmentsAdapter
from .manifest import load_manifest, sha256_file, verify_manifest_file


@dataclass(frozen=True)
class PreparedArtifacts:
    """Paths and integrity metadata produced by one preparation run."""

    parquet_path: Path
    report_path: Path
    processed_sha256: str


def _count_skills(frame: pd.DataFrame) -> int:
    return len({skill for skills in frame["skill_ids"] for skill in skills})


def prepare_assistments(
    *,
    manifest_path: Path,
    raw_dir: Path,
    output_dir: Path,
    skill_separator: str | None = None,
) -> PreparedArtifacts:
    """Validate, normalize, and persist ASSISTments interactions.

    The raw file is never modified. Output filenames derive from the dataset ID
    in the manifest so repeated executions overwrite only the same declared
    dataset version artifacts.
    """

    manifest = load_manifest(manifest_path)
    raw_file = verify_manifest_file(manifest, raw_dir)
    source = pd.read_csv(raw_file, low_memory=False)
    normalized, quality = AssistmentsAdapter(
        source_dataset=manifest.dataset_id,
        skill_separator=skill_separator,
    ).normalize(source)

    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / f"{manifest.dataset_id}.parquet"
    report_path = output_dir / f"{manifest.dataset_id}.quality.json"

    normalized.to_parquet(parquet_path, index=False, engine="pyarrow")
    processed_sha256 = sha256_file(parquet_path)

    report = {
        "dataset_id": manifest.dataset_id,
        "dataset_version": manifest.version,
        "source_sha256": manifest.sha256,
        "processed_sha256": processed_sha256,
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
