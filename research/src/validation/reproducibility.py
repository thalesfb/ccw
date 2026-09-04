"""Create a versioned manifest for a systematic-review snapshot.

The SQLite database is an operational local artifact and is intentionally not
part of the repository. This module records the versioned representation of a
snapshot, the manual decisions that affect inclusion, and hashes for the
published artifacts so that a reviewer can detect drift without receiving the
database file.
"""

from __future__ import annotations

import hashlib
import csv
import json
import os
import sqlite3
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..processing.dedup import normalize_doi
from ..analysis.mmat_current import validate_current_artifacts
from ..config import load_config
from ..search_terms import get_all_queries
from .versioned_snapshot import validate_versioned_snapshot


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "research" / "exports" / "reports" / "reproducibility_manifest.json"
MANUAL_OVERRIDE_ADJUDICATION = "research/data/manual_override_adjudication.csv"
MANUAL_OVERRIDE_EVIDENCE_MATRIX = "research/data/manual_override_evidence_matrix.csv"
HISTORICAL_PROTOCOL_MANIFEST = "research/data/protocol_execution_2025.json"

# The research PR must be verifiable on its own.  Manuscript, presentation and
# editorial documents are companion deliverables owned by their respective
# PRs, so they are described separately instead of being required for the
# research snapshot manifest to generate or validate.
COMPANION_DOCUMENTS: tuple[tuple[str, str, str], ...] = (
    (
        "docs/RECONCILIACAO-BASELINE-2026-08-31.md",
        "human-readable reconciliation of current and historical baselines",
        "documentation PR",
    ),
    (
        "results/tcc/referencias.bib",
        "main TCC bibliography, including pipeline-derived studies and manual references",
        "manuscript PR",
    ),
    (
        "results/tcc/referencias_pedagogicas.bib",
        "supplementary TCC bibliography with manual pedagogical and assessment references",
        "manuscript PR",
    ),
    (
        "research/data/reference_audit.csv",
        "audit separating the complete TCC bibliography from pipeline-derived studies",
        "manuscript PR",
    ),
    (
        "results/tcc/main.pdf",
        "compiled TCC artifact",
        "manuscript PR and LaTeX CI",
    ),
)

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
        "research/exports/analysis/deduplication_identity_audit.csv",
        "row-level audit of the deterministic DOI/URL records removed from the PRISMA flow",
    ),
    (
        "research/exports/analysis/mmat_visualization.html",
        "historical MMAT visualization with an explicit pointer to the preliminary current ledger",
    ),
    (
        "research/exports/reports/summary.json",
        "PRISMA and derived summary statistics",
    ),
    (
        "research/exports/references/included_papers.bib",
        "BibTeX containing only the 18 pipeline-derived retained records (17 provisional empirical candidates plus contextual protocol)",
    ),
    (
        "research/data/mmat_current_study_registry.csv",
        "current 18-record MMAT registry, separate from the historical 17-study appraisal",
    ),
    (
        "research/data/mmat_primary_sources_manifest.csv",
        "source ledger for primary-source verification of current MMAT studies",
    ),
    (
        "research/data/mmat_reassessment_current.csv",
        "preliminary current MMAT ledger with S1/S2 and criterion-level CT responses",
    ),
    (
        "research/data/current_synthesis_scope.csv",
        "explicit empirical/contextual role for each current retained record",
    ),
    (
        "research/data/adjudicated_population_decisions.csv",
        "approved row-level scope decisions used to derive the current population",
    ),
    (
        "research/data/current_eligibility_protocol.csv",
        "versioned adjudication gates for final scientific eligibility and override disposition",
    ),
    (
        MANUAL_OVERRIDE_ADJUDICATION,
        "row-level evidence ledger for the seven manual candidate overrides",
    ),
    (
        MANUAL_OVERRIDE_EVIDENCE_MATRIX,
        "structured evidence matrix for scope and publication-type adjudication of the seven manual overrides",
    ),
    (
        HISTORICAL_PROTOCOL_MANIFEST,
        "historical protocol reconstruction from the 2025 baseline; not the current PRISMA source of truth",
    ),
    (
        "research/src/config.py",
        "versioned review configuration and criteria",
    ),
    (
        "research/src/search_terms.py",
        "versioned canonical bilingual query generator",
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
        "research/src/processing/dedup.py",
        "versioned duplicate-candidate audit and deduplication implementation",
    ),
    (
        "research/src/analysis/reports.py",
        "versioned report and summary generation implementation",
    ),
    (
        "research/src/analysis/visualizations.py",
        "versioned visualization generation implementation",
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
        "research/src/processing/adjudicated_snapshot.py",
        "SQLite-independent transformation from the versioned row export and adjudication ledger",
    ),
    (
        "research/src/analysis/mmat_current.py",
        "versioned validator for the current 18-record MMAT artifacts",
    ),
    (
        "research/src/analysis/mmat_current_tcc_table.py",
        "versioned renderer for the preliminary current MMAT table",
    ),
    (
        "research/exports/references/mmat_current_tcc_table.tex",
        "preliminary current 18-record MMAT table included by the TCC",
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


def _normalize_title(value: Any) -> str:
    if value is None:
        return ""
    normalized = "".join(
        char
        for char in unicodedata.normalize("NFKD", str(value).lower().strip())
        if not unicodedata.combining(char)
    )
    normalized = "".join(
        char if char.isalnum() or char.isspace() else " "
        for char in normalized
    )
    return " ".join(normalized.split())


def _identity_metrics(values: list[str]) -> dict[str, int]:
    non_empty = [value for value in values if value]
    counts = Counter(non_empty)
    repeated = [count for count in counts.values() if count > 1]
    return {
        "non_empty_rows": len(non_empty),
        "distinct_values": len(counts),
        "repeated_groups": len(repeated),
        "repeated_rows": sum(repeated),
        "excess_rows": sum(count - 1 for count in repeated),
    }


def _deterministic_identity_duplicates(rows: list[Any]) -> tuple[set[int], dict[str, int]]:
    """Find exact DOI/URL duplicate rows in stable row order.

    DOI and exact URL identities form a union; overlapping evidence is counted
    once. Title-only matches are intentionally not removed automatically.
    """
    identity_groups: dict[tuple[str, str], list[int]] = {}
    duplicate_indices: set[int] = set()
    by_identifier = {"doi": 0, "url": 0, "persisted_flag": 0}

    for index, row in enumerate(rows):
        doi = normalize_doi(row["doi"])
        url = str(row["url"] or "").strip().lower()
        if bool(row["is_duplicate"]):
            duplicate_indices.add(index)
            by_identifier["persisted_flag"] += 1

        if doi:
            identity_groups.setdefault(("doi", doi), []).append(index)
        if url:
            identity_groups.setdefault(("url", url), []).append(index)

    parent = list(range(len(rows)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for identifier, indices in identity_groups.items():
        for index in indices[1:]:
            union(indices[0], index)
        if len(indices) > 1:
            by_identifier[identifier[0]] += len(indices) - 1

    components: dict[int, list[int]] = {}
    for index in range(len(rows)):
        components.setdefault(find(index), []).append(index)

    stage_priority = {"screening": 1, "eligibility": 2, "included": 3}
    for indices in components.values():
        if len(indices) < 2:
            continue
        representative = max(
            indices,
            key=lambda index: (
                stage_priority.get(rows[index]["selection_stage"], 0),
                -index,
            ),
        )
        duplicate_indices.update(index for index in indices if index != representative)

    return duplicate_indices, by_identifier


def _database_identity_audit(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = conn.execute(
        "SELECT doi, url, title, selection_stage, is_duplicate FROM papers"
    ).fetchall()
    duplicate_indices, duplicate_by_identifier = _deterministic_identity_duplicates(rows)
    unique_rows = [
        row for index, row in enumerate(rows) if index not in duplicate_indices
    ]
    return {
        "raw_rows": len(rows),
        "operationally_flagged_rows": sum(
            bool(row["is_duplicate"]) for row in rows
        ),
        "deterministic_identity_duplicate_rows": len(duplicate_indices),
        "deterministic_identity_duplicate_rows_by_identifier": duplicate_by_identifier,
        "confirmed_semantic_duplicates": 0,
        "doi": _identity_metrics([
            normalize_doi(row["doi"]) for row in rows
        ]),
        "url": _identity_metrics([
            str(row["url"] or "").strip().lower() for row in rows
        ]),
        "title": _identity_metrics([
            _normalize_title(row["title"]) for row in rows
        ]),
        "title_only": _identity_metrics([
            _normalize_title(row["title"]) for row in unique_rows
        ]),
        "interpretation": (
            "Repeated normalized DOI/URL identities are deterministic duplicate "
            "records for the current PRISMA flow. The raw title metric includes "
            "rows in those identity groups; title_only is recalculated after "
            "identity removal. Title-only matches remain candidates for semantic "
            "review and are not removed automatically."
        ),
    }


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
        ordered_rows = conn.execute(
            "SELECT id, selection_stage, status, doi, url, is_duplicate "
            "FROM papers ORDER BY id"
        ).fetchall()
        duplicate_indices, _ = _deterministic_identity_duplicates(ordered_rows)
        unique_rows = [
            row for index, row in enumerate(ordered_rows)
            if index not in duplicate_indices
        ]
        prisma_counts = {
            "identification": total_records,
            "duplicates_removed": len(duplicate_indices),
            "screening": len(unique_rows),
            "screening_excluded": sum(
                row["selection_stage"] == "screening"
                and row["status"] == "excluded"
                for row in unique_rows
            ),
            "eligibility": sum(
                row["selection_stage"] in {"eligibility", "included"}
                for row in unique_rows
            ),
            "eligibility_excluded": sum(
                row["selection_stage"] == "eligibility"
                and row["status"] == "excluded"
                for row in unique_rows
            ),
            "included": sum(
                row["selection_stage"] == "included"
                for row in unique_rows
            ),
        }

        included_ids = [
            int(row[0])
            for row in conn.execute(
                "SELECT id FROM papers WHERE selection_stage = 'included' ORDER BY id"
            ).fetchall()
        ]

        identity_audit = _database_identity_audit(conn)

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
        "deduplication_audit": identity_audit,
        "manual_overrides": overrides,
        "candidate_audit": {
            "operational_candidates": prisma_counts["included"] + len(overrides),
            "manual_overrides_recorded": len(overrides),
            "current_included": prisma_counts["included"],
            "interpretation": (
                "The operational candidate count is the current included set plus "
                "the persisted manual-audit overrides. These overrides are not "
                "scientific exclusion findings until adjudicated, and are not an "
                "extra PRISMA stage."
            ),
        },
    }


def _versioned_snapshot(root: Path) -> dict[str, Any]:
    """Build the manifest snapshot from committed artifacts, not SQLite.

    The local database still exists for operational diagnostics, but it does
    not contain the supervisor-approved scope decisions.  The committed CSV,
    summary and scope ledger are therefore the only valid source for the
    current scientific population in this manifest.
    """

    facts = validate_versioned_snapshot(
        papers_path=root / "research" / "exports" / "analysis" / "papers.csv",
        summary_path=root / "research" / "exports" / "reports" / "summary.json",
        scope_path=root / "research" / "data" / "current_synthesis_scope.csv",
    )
    summary_path = root / "research" / "exports" / "reports" / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    statistics = summary["statistics"]
    prisma = statistics["prisma"]
    decisions_path = root / "research" / "data" / "adjudicated_population_decisions.csv"
    with decisions_path.open("r", encoding="utf-8-sig", newline="") as handle:
        decisions = list(csv.DictReader(handle))
    overrides_path = root / MANUAL_OVERRIDE_ADJUDICATION
    with overrides_path.open("r", encoding="utf-8-sig", newline="") as handle:
        override_rows = list(csv.DictReader(handle))
    identity_audit = dict(statistics["deduplication_audit"])
    identity_audit["deterministic_identity_duplicate_rows_by_identifier"] = {
        "doi": int(identity_audit["doi"]["excess_rows"]),
        "url": int(identity_audit["url"]["excess_rows"]),
        "persisted_flag": int(identity_audit.get("operationally_flagged_rows", 0)),
    }

    return {
        "counts": {
            "total_records": int(prisma["identification"]),
            "versioned_rows": facts["papers_rows"],
            "selection_stage_counts": facts["papers_stage_counts"],
            "prisma": {
                key: int(prisma[key])
                for key in (
                    "identification",
                    "duplicates_removed",
                    "screening",
                    "screening_excluded",
                    "eligibility",
                    "eligibility_excluded",
                    "included",
                )
            },
        },
        "included_ids": facts["included_ids"],
        "deduplication_audit": identity_audit,
        "manual_overrides": [
            {"id": int(row["study_id"])}
            for row in override_rows
        ],
        "adjudicated_population_decisions": [
            {
                "study_id": int(row["study_id"]),
                "final_disposition": row["final_disposition"],
                "final_selection_stage": row["final_selection_stage"],
                "final_year": int(row["final_year"]),
                "decision_status": row["decision_status"],
            }
            for row in decisions
        ],
        "candidate_audit": {
            "pre_adjudication_included": 16,
            "operational_candidates": 23,
            "manual_overrides_recorded": 7,
            "metadata_corrections_recorded": 1,
            "current_included": facts["summary_prisma"]["included"],
            "interpretation": (
                "The 23-record candidate universe is preserved as historical "
                "context: 16 operationally retained records plus seven manual "
                "overrides. The current 18-record population is derived by the "
                "approved scope decisions and the 6918 year correction; it is "
                "not a new collection or an additional PRISMA stage."
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


def _current_protocol() -> dict[str, Any]:
    """Return the versioned protocol parameters used by a fresh run.

    This is deliberately separate from the historical protocol reconstruction.
    The manifest records the configuration and query-generator contract, while
    the snapshot and its exports record what the current local execution
    actually produced.
    """

    config = load_config()
    return {
        "status": "current_snapshot_protocol",
        "year_min": config.review.year_min,
        "year_max": config.review.year_max,
        "cutoff_date": config.review.cutoff_date,
        "languages": list(config.review.languages),
        "abstract_required": config.review.abstract_required,
        "relevance_threshold": config.review.relevance_threshold,
        "canonical_query_count": len(get_all_queries()),
        "query_generator": "research/src/search_terms.py",
        "sources": ["semantic_scholar", "openalex", "crossref", "core"],
        "source_count": 4,
        "max_results_per_query": config.max_results_per_query,
        "interpretation": (
            "These parameters describe the protocol contract for a fresh run. "
            "External API responses, cache state and metadata may change; they "
            "do not replace the current versioned snapshot exports."
        ),
    }


def _validate_manual_override_adjudication(
    path: Path,
    overrides: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate the versioned evidence ledger for manual overrides.

    The ledger must cover exactly the persisted override IDs.  Its proposed
    reasons are deliberately not promoted to final exclusions here: the
    supervisor still has to adjudicate them against the primary sources.
    """
    required = {
        "study_id",
        "study_key",
        "doi",
        "decision_in_snapshot",
        "abstract_evidence",
        "scope_assessment",
        "proposed_exclusion_basis",
        "evidence_level",
        "confidence",
        "adjudication_status",
        "required_action",
        "evidence_source",
        "evidence_checked_on",
    }
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(
                "manual override adjudication is missing columns: "
                + ", ".join(sorted(missing))
            )
        rows = list(reader)

    try:
        study_ids = [int(row["study_id"]) for row in rows]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("manual override adjudication contains an invalid study_id") from exc

    if len(study_ids) != len(set(study_ids)):
        raise ValueError("manual override adjudication contains duplicate study IDs")

    expected_ids = {int(row["id"]) for row in overrides}
    if set(study_ids) != expected_ids:
        raise ValueError(
            "manual override adjudication IDs do not match persisted overrides: "
            f"expected {sorted(expected_ids)}, got {sorted(study_ids)}"
        )

    empty_fields = [
        (row.get("study_id", ""), field)
        for row in rows
        for field in (
            "abstract_evidence",
            "proposed_exclusion_basis",
            "required_action",
            "evidence_source",
            "evidence_checked_on",
        )
        if not (row.get(field) or "").strip()
    ]
    if empty_fields:
        raise ValueError(f"manual override adjudication has empty evidence fields: {empty_fields}")

    status_counts = Counter((row.get("adjudication_status") or "").strip() for row in rows)
    return {
        "path": MANUAL_OVERRIDE_ADJUDICATION,
        "row_count": len(rows),
        "study_ids": sorted(study_ids),
        "adjudication_status_counts": dict(sorted(status_counts.items())),
        "interpretation": (
            "The ledger records evidence and proposed scope rationales for the "
            "persisted overrides; it does not replace supervisor adjudication."
        ),
    }


def _validate_manual_override_evidence_matrix(
    path: Path,
    overrides: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate the evidence matrix without promoting proposed decisions.

    The matrix is intentionally separate from the operational override ledger:
    it records what the reviewed source supports, while ``adjudication_status``
    keeps the supervisor's final scope decision outstanding.
    """
    required = {
        "study_id",
        "source_url",
        "source_type",
        "source_status",
        "publication_type",
        "population_or_context",
        "computational_role",
        "mathematics_relation",
        "educational_outcome",
        "evidence_locator",
        "scope_assessment",
        "recommendation",
        "adjudication_status",
        "checked_on",
    }
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(
                "manual override evidence matrix is missing columns: "
                + ", ".join(sorted(missing))
            )
        rows = list(reader)

    try:
        study_ids = [int(row["study_id"]) for row in rows]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("manual override evidence matrix contains an invalid study_id") from exc

    expected_ids = {int(row["id"]) for row in overrides}
    if len(study_ids) != len(set(study_ids)) or set(study_ids) != expected_ids:
        raise ValueError(
            "manual override evidence matrix IDs do not match persisted overrides: "
            f"expected {sorted(expected_ids)}, got {sorted(study_ids)}"
        )

    text_fields = required - {"study_id"}
    empty_fields = [
        (row.get("study_id", ""), field)
        for row in rows
        for field in text_fields
        if not (row.get(field) or "").strip()
    ]
    if empty_fields:
        raise ValueError(f"manual override evidence matrix has empty fields: {empty_fields}")

    allowed_statuses = {
        "proposed_pending_supervisor",
        "requires_full_text_adjudication",
    }
    status_values = {row.get("adjudication_status", "").strip() for row in rows}
    invalid_statuses = status_values - allowed_statuses
    if invalid_statuses:
        raise ValueError(
            "manual override evidence matrix has unsupported adjudication statuses: "
            + ", ".join(sorted(invalid_statuses))
        )

    status_counts = Counter((row["adjudication_status"] or "").strip() for row in rows)
    return {
        "path": MANUAL_OVERRIDE_EVIDENCE_MATRIX,
        "row_count": len(rows),
        "study_ids": sorted(study_ids),
        "adjudication_status_counts": dict(sorted(status_counts.items())),
        "interpretation": (
            "The matrix records source-supported scope signals and required actions. "
            "It is evidence for adjudication, not a final inclusion or exclusion decision."
        ),
    }


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

    # The database is retained as a local operational diagnostic.  The
    # committed versioned artifacts are the source of truth for the current
    # adjudicated population and must drive the manifest snapshot.
    operational_snapshot = _database_snapshot(source_db)
    snapshot = _versioned_snapshot(root)
    snapshot["manual_override_adjudication"] = _validate_manual_override_adjudication(
        root / MANUAL_OVERRIDE_ADJUDICATION,
        snapshot["manual_overrides"],
    )
    snapshot["manual_override_evidence_matrix"] = _validate_manual_override_evidence_matrix(
        root / MANUAL_OVERRIDE_EVIDENCE_MATRIX,
        snapshot["manual_overrides"],
    )
    mmat_qa = validate_current_artifacts()
    manifest = {
        "schema_version": "1.2",
        "snapshot_date": "2026-09-03",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "database": {
            "path": "research/systematic_review.sqlite",
            "versioned": False,
            "role": "local operational source for raw states and diagnostics; "
            "not the versioned source of the adjudicated population",
        },
        "operational_database_snapshot": operational_snapshot,
        "protocol": _current_protocol(),
        "snapshot": snapshot,
        "bibliography": {
            "pipeline_derived_studies": "research/exports/references/included_papers.bib",
            "complete_tcc_bibliography": [
                "results/tcc/referencias.bib",
                "results/tcc/referencias_pedagogicas.bib",
            ],
            "reference_audit": "research/data/reference_audit.csv",
            "separation_rule": (
                "The 18 included studies are derived from the review pipeline. "
                "Methodological, pedagogical, assessment and technical references "
                "are external to the pipeline study set and remain in the complete TCC bibliography."
            ),
        },
        "methodological_appraisal": {
            "current_mmat_qa": mmat_qa,
            "interpretation": (
                "The current MMAT ledger is a criterion-level preliminary record. "
                "Incomplete source retrieval or pending methodological adjudication blocks any final quality claim."
            ),
        },
        "artifact_scope": "research_snapshot",
        "artifacts": _artifact_manifest(root),
        "companion_documents": [
            {
                "path": relative_path,
                "role": role,
                "owner": owner,
                "verification": (
                    "Tracked and validated by the owning PR; not required to "
                    "verify the research snapshot in this manifest."
                ),
            }
            for relative_path, role, owner in COMPANION_DOCUMENTS
        ],
        "reproduction": {
            "verify_snapshot_without_database": [
                "Compare artifact SHA-256 values with this manifest.",
                "Read PRISMA counts from research/exports/reports/summary.json.",
                "Read row-level states from research/exports/analysis/papers.csv or papers.json.",
                "Read the 18 pipeline-derived citations from research/exports/references/included_papers.bib.",
                "Read the historical evidence ledger from research/data/manual_override_adjudication.csv.",
                "Read the structured source-evidence matrix from research/data/manual_override_evidence_matrix.csv; the final population decision is recorded separately in research/data/adjudicated_population_decisions.csv.",
                "Read the approved population decisions from research/data/adjudicated_population_decisions.csv and rerun research/src/processing/adjudicated_snapshot.py without SQLite.",
                "Read research/data/protocol_execution_2025.json only for historical protocol provenance; do not use it as the current baseline.",
            ],
            "rebuild_from_local_database": [
                "python -m research.src.cli --db /path/to/systematic_review.sqlite export",
                "python -m research.src.cli --db /path/to/systematic_review.sqlite generate-manifest",
            ],
            "fresh_collection": "python -m research.src.cli run-pipeline --min-score 4.0",
            "limitations": [
                "External API responses, metadata and cache state can change on a fresh collection.",
                "The duplicate-candidate audit is not a semantic adjudication and does not change PRISMA counts.",
                "The seven original manual overrides retain separate evidence ledgers; their approved scope consequences are recorded in the adjudicated population ledger.",
                "The current 18-record MMAT ledger is preliminary; source retrieval, criterion locators and supervisor adjudication remain required before quality synthesis.",
            ],
        },
    }

    destination.parent.mkdir(parents=True, exist_ok=True)
    # Keep the committed manifest byte-stable across Windows and Linux.
    # ``Path.write_text`` otherwise uses the host's default newline policy,
    # which makes every CR in a Windows-generated JSON line appear as
    # trailing whitespace to ``git diff --check``.
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return destination
