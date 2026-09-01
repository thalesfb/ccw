"""Validate the committed representation of the current review snapshot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.analysis.reports import ReportGenerator


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

    assert manifest["schema_version"] == "1.1"
    assert manifest["database"]["versioned"] is False
    assert manifest["protocol"] == {
        "status": "current_snapshot_protocol",
        "year_min": 2015,
        "year_max": 2026,
        "cutoff_date": "2026-08-31",
        "languages": ["en", "pt"],
        "abstract_required": False,
        "relevance_threshold": 4.0,
        "canonical_query_count": 72,
        "query_generator": "research/src/search_terms.py",
        "sources": ["semantic_scholar", "openalex", "crossref", "core"],
        "source_count": 4,
        "max_results_per_query": 10,
        "interpretation": (
            "These parameters describe the protocol contract for a fresh run. "
            "External API responses, cache state and metadata may change; they "
            "do not replace the current versioned snapshot exports."
        ),
    }
    assert counts["total_records"] == 11904
    assert counts["selection_stage_counts"] == {
        "screening": 9413,
        "eligibility": 2475,
        "included": 16,
    }
    assert counts["prisma"] == {
        "identification": 11904,
        "duplicates_removed": 27,
        "screening": 11877,
        "screening_excluded": 9391,
        "eligibility": 2486,
        "eligibility_excluded": 2470,
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
    assert snapshot["candidate_audit"]["manual_overrides_recorded"] == 7
    assert "false_positives_removed" not in snapshot["candidate_audit"]
    assert len(snapshot["manual_overrides"]) == 7
    override_ledger = snapshot["manual_override_adjudication"]
    assert override_ledger["row_count"] == 7
    assert override_ledger["study_ids"] == [14, 15, 6915, 6919, 6922, 6925, 6926]
    assert override_ledger["adjudication_status_counts"] == {
        "proposed_pending_supervisor": 3,
        "requires_full_text_adjudication": 4,
    }
    audit = snapshot["deduplication_audit"]
    assert audit["raw_rows"] == 11904
    assert audit["operationally_flagged_rows"] == 0
    assert audit["deterministic_identity_duplicate_rows"] == 27
    assert audit["deterministic_identity_duplicate_rows_by_identifier"] == {
        "doi": 25,
        "url": 2,
        "persisted_flag": 0,
    }
    assert audit["confirmed_semantic_duplicates"] == 0
    assert audit["doi"]["repeated_groups"] == 25
    assert audit["doi"]["excess_rows"] == 25
    assert audit["url"]["repeated_groups"] == 2
    assert audit["url"]["excess_rows"] == 2
    assert audit["title"]["excess_rows"] == 257
    assert audit["title_only"]["repeated_groups"] == 154
    assert audit["title_only"]["repeated_rows"] == 386
    assert audit["title_only"]["excess_rows"] == 232


def test_manifest_hashes_and_bibliography_scope_are_current() -> None:
    manifest = _manifest()

    current_mmat = manifest["methodological_appraisal"]["current_mmat_qa"]
    assert current_mmat["final_ready"] is False
    assert current_mmat["source_or_period_hold_ids"] == ["6918"]
    assert current_mmat["primary_text_reviewed_rows"] == 9

    assert manifest["artifact_scope"] == "research_snapshot"
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
    artifact_paths = {artifact["path"] for artifact in manifest["artifacts"]}
    assert "research/data/protocol_execution_2025.json" in artifact_paths

    companion_paths = {
        document["path"] for document in manifest["companion_documents"]
    }
    assert companion_paths == {
        "docs/RECONCILIACAO-BASELINE-2026-08-31.md",
        "results/tcc/referencias.bib",
        "results/tcc/referencias_pedagogicas.bib",
        "results/tcc/main.pdf",
    }
    assert not artifact_paths.intersection(companion_paths)
    assert all(
        document["owner"] in {"documentation PR", "manuscript PR", "manuscript PR and LaTeX CI"}
        for document in manifest["companion_documents"]
    )


def test_summary_json_export_does_not_replace_audited_html(tmp_path: Path) -> None:
    generator = ReportGenerator(output_dir=tmp_path / "reports")
    report_data = {
        "title": "Relatório",
        "subtitle": "Snapshot atual",
        "generated_at": "31/08/2026 00:00",
        "statistics": {
            "total_papers": 10,
            "prisma": {
                "identification": 10,
                "screening": 10,
                "screening_excluded": 8,
                "eligibility": 2,
                "eligibility_excluded": 1,
                "included": 1,
            },
            "stage_percentages": {"included_of_identification": 10.0},
            "deduplication_audit": {
                "doi": {"repeated_groups": 1, "repeated_rows": 2, "excess_rows": 1},
                "url": {"repeated_groups": 0, "repeated_rows": 0, "excess_rows": 0},
                "title": {"repeated_groups": 0, "repeated_rows": 0, "excess_rows": 0},
                "operationally_flagged_rows": 0,
                "confirmed_semantic_duplicates": 0,
            },
        },
        "charts": [],
        "config": {},
        "included_list": [],
        "fulltext_stats": None,
    }

    generator._generate_html_report(report_data)
    generator._generate_json_summary(report_data)
    html = (tmp_path / "reports" / "summary_report.html").read_text(encoding="utf-8")

    assert "Percentuais do fluxo PRISMA" in html
    assert "Auditoria de identidade bibliográfica" in html
    assert "Contexto histórico da deduplicação" in html
    assert "2.517 duplicatas removidas" in html
