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
import csv
import pytest


CURRENT_TABLE = Path(__file__).resolve().parents[1] / "exports" / "references" / "mmat_current_tcc_table.tex"
EVIDENCE_MATRIX = Path(__file__).resolve().parents[1] / "data" / "manual_override_evidence_matrix.csv"


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
    assert report["primary_text_reviewed_rows"] == 12
    assert report["source_or_period_hold_rows"] == 0
    assert report["source_or_period_hold_ids"] == []
    assert report["evidence_levels"]["primary_full_text_reviewed_externally"] == 12
    assert report["evidence_levels"]["abstract_and_metadata_only"] == 5
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


def test_newly_reviewed_primary_sources_have_traceable_provisional_appraisal() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    sources = {row["study_id"]: row for row in load_primary_sources()}

    for study_id in ("14", "6915", "6919"):
        assert rows[study_id]["assessment_basis"] == "primary_full_text_reviewed_externally"
        assert rows[study_id]["assessment_status"] == "provisional_primary_source_review"
        assert rows[study_id]["adjudication_status"] == "supervisor_review_pending"
        assert rows[study_id]["page_or_section"]
        assert sources[study_id]["full_text_status"] == "externally_reviewed_not_archived"
        assert sources[study_id]["accessed_date"] == "2026-10-09"
        assert not sources[study_id]["local_file"]

    assert rows["6919"]["design"] == "mixed_methods"
    assert rows["6919"]["snapshot_date"] == "2026-09-03"
    assert rows["6919"]["review_date"] == "2026-10-09"
    assert rows["6919"]["empirical_status"] == "empirical_confirmed_external"
    assert "4.1.1" in rows["6919"]["page_or_section"]
    assert "4.4.8" in rows["6919"]["page_or_section"]
    assert "2021" in rows["6919"]["notes"] and "2025" in rows["6919"]["notes"]
    assert "machine learning" not in rows["6919"]["notes"].lower()
    assert sources["6919"]["source_type"] == "full_text_mirror"
    assert "researchgate.net/publication/400728111" in sources["6919"]["source_url"]
    assert "10.3390/su18041900" in sources["6919"]["verification_note"]

    assert rows["14"]["design"] == "design_pending"
    assert rows["14"]["design_status"] == "allocation_conflict_pending"
    assert all(rows["14"][criterion] == "CT" for criterion in ("q1", "q2", "q3", "q4", "q5"))
    assert "random" in rows["14"]["notes"].lower()
    assert "45" in rows["6915"]["notes"] and "90" in rows["6915"]["notes"]
    assert [rows["6915"][criterion] for criterion in ("q1", "q2", "q3", "q4", "q5")] == [
        "N", "Y", "CT", "N", "Y"
    ]
    assert rows["6915"]["q4"] == "N"
    assert "Nyantah et al. (2025) & Pendente & Y & Y & CT & CT & CT & CT & CT" in (
        CURRENT_TABLE.read_text(encoding="utf-8")
    )


def test_unresolved_mmat_design_cannot_receive_category_specific_ratings(monkeypatch) -> None:
    from src.analysis import mmat_current as current

    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(item for item in rows if item["study_id"] == "14")
            row["q1"] = "N"
            row["criterion_evidence"] = row["criterion_evidence"].replace(
                "Q1=CT", "Q1=N"
            )
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="unresolved MMAT design"):
        current.validate_current_artifacts()


def test_protocol_is_retained_only_as_contextual_non_empirical_record() -> None:
    scope = {row["study_id"]: row for row in load_current_synthesis_scope()}
    assert scope["6921"]["synthesis_role"] == "contextual_protocol"
    assert scope["6921"]["empirical_mmat_applicability"] == "not_applicable"


def test_current_mmat_tcc_table_is_generated_from_the_current_ledger() -> None:
    assert CURRENT_TABLE.read_text(encoding="utf-8") == render_current_table(
        load_current_table_rows()
    )
    table = CURRENT_TABLE.read_text(encoding="utf-8")
    assert "Nyantah et al. (2025) & Pendente" in table
    assert "Xia et al. (2026) & M\u00e9todos mistos" in table
    assert "ID" not in table
    assert "Enhancing2025" not in table


def test_study_6919_scope_evidence_reflects_the_latest_primary_text_review() -> None:
    with EVIDENCE_MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    study = next(row for row in rows if row["study_id"] == "6919")

    assert study["snapshot_date"] == "2026-10-09"
    assert study["source_type"] == "full_text_mirror"
    assert study["source_status"] == "primary_full_text_reviewed_not_archived"
    assert "4.1.1" in study["evidence_locator"]
    assert "4.4.8" in study["evidence_locator"]
    assert "2021" in study["population_or_context"] and "2025" in study["population_or_context"]
    assert "no specific ML algorithm identified" in study["computational_role"]
    assert study["adjudication_status"] == "proposed_pending_supervisor"
