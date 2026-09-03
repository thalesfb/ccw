from __future__ import annotations

from src.analysis.mmat_current import (
    CURRENT_STUDY_IDS,
    load_current_registry,
    load_primary_sources,
    load_current_reassessment,
    load_current_synthesis_scope,
    validate_current_artifacts,
)
from src.analysis.mmat_current_tcc_table import load_rows as load_current_table_rows
from src.analysis.mmat_current_tcc_table import render_table as render_current_table

from pathlib import Path


CURRENT_TABLE = Path(__file__).resolve().parents[1] / "exports" / "references" / "mmat_current_tcc_table.tex"


def test_current_mmat_artifacts_use_exact_current_denominator() -> None:
    registry = load_current_registry()
    reassessment = load_current_reassessment()
    primary_sources = load_primary_sources()
    synthesis_scope = load_current_synthesis_scope()

    assert [int(row["study_id"]) for row in registry] == list(CURRENT_STUDY_IDS)
    assert [int(row["study_id"]) for row in reassessment] == list(CURRENT_STUDY_IDS)
    assert [int(row["study_id"]) for row in primary_sources] == list(CURRENT_STUDY_IDS)
    assert [int(row["study_id"]) for row in synthesis_scope] == list(CURRENT_STUDY_IDS)
    assert all(row["mmat_status"] != "final" for row in registry)
    assert all(row["assessment_status"] != "final" for row in reassessment)


def test_current_mmat_qa_explicitly_blocks_final_claim() -> None:
    report = validate_current_artifacts()

    assert report["current_denominator"] == 18
    assert report["historical_denominator"] == 17
    assert report["criterion_rows"] == 18
    assert report["primary_source_rows"] == 18
    assert report["synthesis_scope_rows"] == 18
    assert report["empirical_evidence_rows"] == 17
    assert report["contextual_protocol_rows"] == 1
    assert report["primary_text_reviewed_rows"] == 9
    assert report["source_or_period_hold_rows"] == 0
    assert report["source_or_period_hold_ids"] == []
    assert report["evidence_levels"]["primary_full_text_reviewed_externally"] == 9
    assert report["evidence_levels"]["abstract_and_metadata_only"] == 8
    assert report["evidence_levels"]["metadata_only"] == 0
    assert report["evidence_levels"]["protocol_or_proposal_not_applicable"] == 1
    assert report["non_ct_criterion_decisions"] > 0
    assert report["final_ready"] is False
    assert report["blocking_reasons"]
    assert not any("source/year eligibility hold" in reason for reason in report["blocking_reasons"])


def test_current_mmat_evidence_matches_criterion_values() -> None:
    rows = load_current_reassessment()
    registry = {row["study_id"]: row for row in load_current_registry()}

    assert all(row["criterion_evidence"].count(";") == 6 for row in rows)
    assert rows[1]["assessment_status"] == "provisional_primary_source_review"
    assert rows[1]["q2"] == "N"
    assert registry["6923"]["empirical_status"] == "empirical_abstract_only"
    assert registry["6923"]["design_status"] == "abstract_based"


def test_protocol_is_retained_only_as_contextual_non_empirical_record() -> None:
    scope = {row["study_id"]: row for row in load_current_synthesis_scope()}
    assert scope["6921"]["synthesis_role"] == "contextual_protocol"
    assert scope["6921"]["empirical_mmat_applicability"] == "not_applicable"


def test_current_mmat_tcc_table_is_generated_from_the_current_ledger() -> None:
    assert CURRENT_TABLE.read_text(encoding="utf-8") == render_current_table(
        load_current_table_rows()
    )
    table = CURRENT_TABLE.read_text(encoding="utf-8")
    assert "14 & Enhancing2025\\_012 & Quant. n\u00e3o rand." in table
    assert "6919 & UniversityMathematics2026\\_6919 & M\u00e9todos mistos" in table
    assert "6918 &" not in table
