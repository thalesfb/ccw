"""Create a versioned manifest for a systematic-review snapshot.

The SQLite database is an operational local artifact and is intentionally not
part of the repository. This module records the versioned representation of a
snapshot, the manual decisions that affect inclusion, and hashes for the
published artifacts so that a reviewer can detect drift without receiving the
database file.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "research" / "exports" / "reports" / "reproducibility_manifest.json"

ARTIFACTS: tuple[tuple[str, str], ...] = (
    (
        "research/exports/analysis/papers.csv",
        "row-level versioned representation of the current snapshot",
    ),
    (
        "research/exports/analysis/papers.json",
        "JSON representation of the current snapshot",
    ),
    (
        "research/exports/reports/summary.json",
        "PRISMA and derived summary statistics",
    ),
    (
        "research/exports/references/included_papers.bib",
        "BibTeX containing only the 16 pipeline-derived included studies",
    ),
    (
        "research/data/reference_audit.csv",
        "audit separating included studies from theoretical and methodological references",
    ),
    (
        "docs/RECONCILIACAO-BASELINE-2026-08-31.md",
        "human-readable reconciliation of current and historical baselines",
    ),
    (
        "results/tcc/referencias.bib",
        "main TCC bibliography, including pipeline-derived studies and manual references",
    ),
    (
        "results/tcc/referencias_pedagogicas.bib",
        "supplementary TCC bibliography with manual pedagogical and assessment references",
    ),
    (
        "results/tcc/main.pdf",
        "compiled TCC artifact",
    ),
    (
        "research/src/config.py",
        "versioned review configuration and criteria",
    ),
    (
        "research/src/processing/scoring.py",
        "versioned relevance-scoring implementation",
    ),
    (
        "research/src/processing/selection.py",
        "versioned selection-stage implementation",
    ),
    (
        "research/src/analysis/deep_review_analysis.py",
        "versioned full-text analysis implementation",
    ),
    (
        "research/src/cli_audit.py",
        "manual-audit helper used to persist exclusions",
    ),
    (
        "research/src/cli.py",
        "versioned command-line entry point for the research workflow",
    ),
    (
        "research/src/pipelines/validations.py",
        "versioned read-only cross-check of DB, exports and summary",
    ),
    (
        "research/src/validation/reproducibility.py",
        "versioned generator for this reproducibility manifest",
    ),
    (
        "research/requirements.txt",
        "research runtime dependencies",
    ),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _count(conn: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> int:
    value = conn.execute(query, params).fetchone()[0]
    return int(value)


def _database_snapshot(db_path: Path) -> dict[str, Any]:
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        total_records = _count(conn, "SELECT COUNT(*) FROM papers")
        stage_counts = {
            "screening": _count(
                conn,
                "SELECT COUNT(*) FROM papers WHERE selection_stage = 'screening'",
            ),
            "eligibility": _count(
                conn,
                "SELECT COUNT(*) FROM papers WHERE selection_stage = 'eligibility'",
            ),
            "included": _count(
                conn,
                "SELECT COUNT(*) FROM papers WHERE selection_stage = 'included'",
            ),
        }
        prisma_counts = {
            "identification": total_records,
            "screening": total_records,
            "screening_excluded": _count(
                conn,
                "SELECT COUNT(*) FROM papers "
                "WHERE selection_stage = 'screening' AND status = 'excluded'",
            ),
            "eligibility": stage_counts["eligibility"] + stage_counts["included"],
            "eligibility_excluded": _count(
                conn,
                "SELECT COUNT(*) FROM papers "
                "WHERE selection_stage = 'eligibility' AND status = 'excluded'",
            ),
            "included": stage_counts["included"],
        }

        included_ids = [
            int(row[0])
            for row in conn.execute(
                "SELECT id FROM papers WHERE selection_stage = 'included' ORDER BY id"
            ).fetchall()
        ]

        overrides = []
        for row in conn.execute(
            """
            SELECT id, doi, title, year, relevance_score, selection_stage,
                   status, exclusion_reason
            FROM papers
            WHERE exclusion_reason = 'manual_exclusion_after_audit'
            ORDER BY id
            """
        ).fetchall():
            overrides.append(
                {
                    "id": int(row["id"]),
                    "doi": row["doi"] or "",
                    "title": row["title"] or "",
                    "year": int(row["year"]) if row["year"] is not None else None,
                    "relevance_score": row["relevance_score"],
                    "selection_stage": row["selection_stage"],
                    "status": row["status"],
                    "exclusion_reason": row["exclusion_reason"],
                    "rationale_status": "individual_rationale_pending",
                }
            )
    finally:
        conn.close()

    if sum(stage_counts.values()) != total_records:
        raise ValueError("selection stages do not partition the database records")

    return {
        "counts": {
            "total_records": total_records,
            "selection_stage_counts": stage_counts,
            "prisma": prisma_counts,
        },
        "included_ids": included_ids,
        "manual_overrides": overrides,
        "candidate_audit": {
            "operational_candidates": prisma_counts["included"] + len(overrides),
            "false_positives_removed": len(overrides),
            "current_included": prisma_counts["included"],
            "interpretation": (
                "The operational candidate count is the current included set plus "
                "the persisted manual-audit overrides. It is not an extra PRISMA stage."
            ),
        },
    }


def _artifact_manifest(root: Path) -> list[dict[str, str]]:
    artifacts = []
    for relative_path, role in ARTIFACTS:
        path = root / relative_path
        if not path.exists():
            raise FileNotFoundError(f"Required reproducibility artifact not found: {relative_path}")
        artifacts.append(
            {
                "path": relative_path,
                "role": role,
                "sha256": _sha256(path),
            }
        )
    return artifacts


def generate_manifest(
    db_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    """Generate the reproducibility manifest from a local operational DB."""

    root = REPOSITORY_ROOT
    configured_db = os.getenv("CCW_DB_PATH")
    source_db = Path(db_path or configured_db or root / "research" / "systematic_review.sqlite")
    if not source_db.is_absolute():
        source_db = root / source_db
    destination = output_path or DEFAULT_OUTPUT
    if not destination.is_absolute():
        destination = root / destination

    snapshot = _database_snapshot(source_db)
    manifest = {
        "schema_version": "1.0",
        "snapshot_date": "2026-08-31",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "database": {
            "path": "research/systematic_review.sqlite",
            "versioned": False,
            "role": "local operational source for states and counts",
        },
        "snapshot": snapshot,
        "bibliography": {
            "pipeline_derived_studies": "research/exports/references/included_papers.bib",
            "complete_tcc_bibliography": [
                "results/tcc/referencias.bib",
                "results/tcc/referencias_pedagogicas.bib",
            ],
            "reference_audit": "research/data/reference_audit.csv",
            "separation_rule": (
                "The 16 included studies are derived from the review pipeline. "
                "Methodological, pedagogical, assessment and technical references "
                "are external to the pipeline study set and remain in the complete TCC bibliography."
            ),
        },
        "artifacts": _artifact_manifest(root),
        "reproduction": {
            "verify_snapshot_without_database": [
                "Compare artifact SHA-256 values with this manifest.",
                "Read PRISMA counts from research/exports/reports/summary.json.",
                "Read row-level states from research/exports/analysis/papers.csv or papers.json.",
                "Read the 16 pipeline-derived citations from research/exports/references/included_papers.bib.",
            ],
            "rebuild_from_local_database": [
                "python -m research.src.cli --db /path/to/systematic_review.sqlite export",
                "python -m research.src.cli --db /path/to/systematic_review.sqlite generate-manifest",
            ],
            "fresh_collection": "python -m research.src.cli run-pipeline --min-score 4.0",
            "limitations": [
                "External API responses, metadata and cache state can change on a fresh collection.",
                "The seven manual overrides are recorded, but their substantive individual rationales remain pending.",
                "The MMAT appraisal must be reapplied to the current 16 studies before quality synthesis.",
            ],
        },
    }

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return destination
