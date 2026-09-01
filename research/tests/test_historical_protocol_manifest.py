"""Regression checks for the preserved 2025 protocol reconstruction."""

from __future__ import annotations

import json
from pathlib import Path


MANIFEST = Path(__file__).resolve().parents[1] / "data" / "protocol_execution_2025.json"


def test_historical_protocol_is_not_presented_as_current_baseline() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["status"] == "historical_reconstruction_not_current_baseline"
    assert manifest["current_baseline"] == {
        "manifest": "research/exports/reports/reproducibility_manifest.json",
        "identified": 11904,
        "deterministic_identity_duplicates_removed": 27,
        "screening": 11877,
        "eligibility": 2486,
        "included_operational": 16,
        "note": "This historical protocol record must not be used as the current PRISMA baseline.",
    }
    assert manifest["counts"]["identified"] == 9431
    assert manifest["counts"]["included"] == 17
    assert manifest["evidence"]["historical_deduplication_discrepancy"] == {
        "reported_in_historical_documents": 2517,
        "preserved_sqlite_results_summary_total_removed": 2494,
        "status": "unresolved",
        "notes": "The historical artifact needed to arbitrate these values was not preserved. Neither value is reused for the current flow.",
    }


def test_historical_protocol_preserves_strategy_limits() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["search_strategy"]["canonical_query_count"] == 72
    assert manifest["search_strategy"]["query_count_evidence"] == (
        "versioned_strategy_not_http_request_audit"
    )
    assert manifest["operational_selection"]["language_is_required_criterion"] is False
    assert manifest["operational_selection"]["peer_review_document_type_filter"] is False
    assert manifest["operational_selection"]["full_text_review_enforced_by_pipeline"] is False
    assert manifest["limitations"]["historical_deduplication_artifact_preserved"] is False
