"""Check publication boundaries of the documentary source-coverage matrix."""

import json
from pathlib import Path

from src.analysis.mmat_current import CURRENT_RECORD_IDS, load_current_synthesis_scope


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "research/data/study_contribution_current.json"


def test_contribution_matrix_keeps_all_candidates_and_does_not_adjudicate_scope():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = matrix["records"]
    scope = {row["study_id"]: row for row in load_current_synthesis_scope()}

    assert [int(row["study_id"]) for row in rows] == list(CURRENT_RECORD_IDS)
    for row in rows:
        assert row["record_status"] == scope[row["study_id"]]["record_status"]
        assert row["human_reading_status"] == "pending"
        assert row["multimodal_complete"] is False
        assert row["contribution"] and row["does_not_support"]


def test_available_source_coverage_is_bound_to_identified_pdf_bytes():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    sources = json.loads(
        (ROOT / "research/data/evidence_sources_current.json").read_text(encoding="utf-8")
    )
    source_by_id = {row["study_id"]: row for row in sources["sources"]}
    available = [row for row in matrix["records"] if row["full_text_available_locally"]]

    assert len(available) == 16
    for row in available:
        source = source_by_id[row["study_id"]]
        assert row["source_sha256"] == source["sha256"]
        assert row["physical_page_count"] == source["page_count"]
        pages = row["physical_text_pages_read"]
        assert pages == sorted(set(pages))
        assert all(1 <= page <= row["physical_page_count"] for page in pages)
        assert all(1 <= page <= row["physical_page_count"] for page in row["physical_visual_pages"])
    thesis = next(row for row in available if row["study_id"] == "8")
    assert len(thesis["physical_text_pages_read"]) == 38
    assert thesis["physical_page_count"] == 108
    assert thesis["text_reading_extent"] == "partial"


def test_missing_primary_sources_do_not_acquire_reading_or_empirical_verification():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    missing = [row for row in matrix["records"] if not row["full_text_available_locally"]]
    assert {row["study_id"] for row in missing} == {"3", "6923"}
    for row in missing:
        assert row["source_sha256"] is None
        assert row["physical_page_count"] is None
        assert row["physical_text_pages_read"] == []
        assert row["physical_visual_pages"] == []
        assert row["text_reading_extent"] == "not_read_in_this_audit"


def test_public_matrix_contains_no_private_paths_or_operational_agent_details():
    text = MATRIX.read_text(encoding="utf-8")
    for forbidden in ("C:/", "C:\\", ".cache/", "feedback/private", "AppData", "ConversationId", "SessionID"):
        assert forbidden not in text


def test_supplementary_ocr_review_does_not_claim_a_replayed_text_index():
    sources = json.loads(
        (ROOT / "research/data/evidence_sources_current.json").read_text(encoding="utf-8")
    )
    study = next(row for row in sources["sources"] if row["study_id"] == "9")
    assert study["extraction_method"] == "local_ocr_with_selective_visual_check"
    assert study["replay_status"] == "not_in_frozen_retrieval_replay"
    assert study["page_count"] == 7
    assert sources["replay_validation"]["checked_source_count"] == 12


def test_unavailable_sources_keep_explicit_access_and_appraisal_limits():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = {row["study_id"]: row for row in matrix["records"]}
    assert rows["3"]["access_status"] == "purchase_required_reported_by_author"
    assert rows["3"]["current_appraisal_verification"] == "not_revalidated_without_primary_text"
    assert rows["6923"]["access_status"] == "repository_embargo"
    assert rows["6923"]["current_appraisal_verification"] == "not_appraised"


def test_published_mmat_provenance_includes_the_source_coverage_matrix():
    workflow = (ROOT / ".github/workflows/publish-reports.yml").read_text(encoding="utf-8")
    generator = (ROOT / "scripts/generate-mmat-page.mjs").read_text(encoding="utf-8")
    assert "cp research/data/study_contribution_current.json _site/research/data/" in workflow
    assert 'href="../../../research/data/study_contribution_current.json"' in generator
