from __future__ import annotations

import pandas as pd

from src.exports.excel import export_for_analysis, remove_legacy_mmat_from_notes
from src.processing.adjudicated_snapshot import (
    EXPECTED_DECISION_IDS,
    PAPERS_PATH,
    _updated_prisma,
    apply_adjudications,
    apply_current_adjudications,
    apply_current_scope_adjudications,
    apply_record_corrections,
    _reconciled_json_records,
    load_decisions,
    load_record_corrections,
)


def test_approved_decision_ledger_covers_the_population_changes() -> None:
    decisions = load_decisions()

    assert tuple(int(row["study_id"]) for row in decisions) == EXPECTED_DECISION_IDS
    assert all(row["decision_status"] == "approved_in_pr54" for row in decisions)
    assert [row["final_disposition"] for row in decisions].count("include") == 3
    assert [row["final_disposition"] for row in decisions].count("exclude_temporal") == 1


def test_historical_pr54_decisions_can_be_replayed_on_current_snapshot() -> None:
    papers = pd.read_csv(PAPERS_PATH, encoding="utf-8-sig")
    replayed = apply_adjudications(papers)

    rows = replayed.set_index("id")
    for decision in load_decisions():
        row = rows.loc[int(decision["study_id"])]
        assert row["selection_stage"] == decision["final_selection_stage"]
        assert row["status"] == decision["final_status"]

    row_6918 = replayed.loc[replayed["id"] == 6918].iloc[0]
    assert int(row_6918["year"]) == 2014
    assert row_6918["selection_stage"] == "eligibility"
    assert row_6918["exclusion_reason"] == "exclude_temporal"
    assert row_6918["status"] == "excluded"


def test_current_scope_has_reconciled_prisma_stages_and_empirical_core() -> None:
    papers = pd.read_csv(PAPERS_PATH, encoding="utf-8-sig")
    replayed = apply_current_adjudications(papers)

    assert len(replayed) == 11875
    assert replayed["selection_stage"].value_counts().to_dict() == {
        "screening": 9393,
        "prioritization": 2464,
        "included": 15,
        "not_retrieved": 1,
        "eligibility": 1,
        "abstract_screening": 1,
    }
    included_ids = sorted(
        replayed.loc[replayed["selection_stage"] == "included", "id"]
        .astype(int)
        .tolist()
    )
    assert included_ids == [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 6915, 6916, 6917, 6919, 6920]
    assert replayed.loc[replayed["id"] == 9, "selection_stage"].item() == "abstract_screening"
    row_6919 = replayed.loc[replayed["id"] == 6919].iloc[0]
    assert row_6919["selection_stage"] == "included"
    assert "included_empirical_core" in row_6919["notes"]
    assert "context_only" not in row_6919["notes"]
    assert "Adjudicação de escopo PR54 aplicada" not in row_6919["notes"]
    assert row_6919["notes"].startswith(
        "Adjudicação de escopo 2026-10-12 (included_empirical_core);"
    )
    row_15 = replayed.loc[replayed["id"] == 15, "notes"].item()
    assert row_15.count("Adjudicação de escopo PR54 aplicada (estudo 15)") == 1
    assert replayed.loc[replayed["id"] == 6921, "selection_stage"].item() == "eligibility"
    assert replayed.loc[replayed["id"].isin([1, 5, 10]), "selection_stage"].eq("included").all()
    assert replayed.loc[replayed["id"] == 6923, "selection_stage"].item() == "not_retrieved"


def test_confirmed_record_corrections_preserve_duplicate_provenance_and_years() -> None:
    papers = pd.read_csv(PAPERS_PATH, encoding="utf-8-sig")
    replayed = apply_current_adjudications(papers)
    rows = replayed.set_index("id")
    corrections = {int(row["record_id"]): row for row in load_record_corrections()}

    assert 6952 not in rows.index
    assert corrections[6952]["corrected_year"] == "2016"
    assert corrections[6952]["duplicate_of"] == "155"
    assert corrections[6952]["previous_selection_stage"] == "prioritization"
    assert "removido antes da triagem" in corrections[6952]["notes"].lower()
    assert "5ebb4290e486a924fd9ab8ee2c46efe7daa94adc54f5de615df15b2ff2dc3f01" in corrections[6952]["evidence_description"]

    assert 6977 not in rows.index
    assert corrections[6977]["corrected_year"] == "2017"
    assert corrections[6977]["duplicate_of"] == "8"
    assert corrections[6977]["previous_selection_stage"] == "prioritization"
    assert "removido antes da triagem" in corrections[6977]["notes"].lower()
    assert "IsIdenticalTo" in corrections[6977]["evidence_description"]

    assert int(rows.loc[7001, "year"]) == 1997
    assert rows.loc[7001, "selection_stage"] == "screening"
    assert rows.loc[7001, "exclusion_reason"] == "year_range"
    assert int(rows.loc[361, "year"]) == 2005
    assert rows.loc[361, "selection_stage"] == "screening"
    assert rows.loc[361, "exclusion_reason"] == "year_range"

    assert len(replayed) == 11875
    assert len(load_record_corrections()) == 4
    prisma = _updated_prisma(replayed)
    assert prisma["identification"] == 11904
    assert prisma["duplicates_removed"] == 29
    assert prisma["screening"] == 11875
    assert prisma["screening_excluded"] == 9393
    assert prisma["prioritization"] == 2482
    assert prisma["prioritization_excluded"] == 2464
    assert prisma["shortlisted"] == 18
    assert prisma["included"] == 15
    assert prisma["deduplication_audit"]["deterministic_identity_duplicate_rows"] == 27
    assert prisma["deduplication_audit"]["adjudicated_same_report_duplicate_rows"] == 2


def test_record_corrections_replay_on_a_small_source_frame() -> None:
    papers = pd.DataFrame(
        [
            {"id": 8, "year": 2017, "selection_stage": "included", "status": "included", "exclusion_reason": "", "inclusion_criteria_met": "year_range; math_focus"},
            {"id": 155, "year": 2016, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "inclusion_criteria_met": "year_range; math_focus"},
            {"id": 6952, "year": 2020, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "inclusion_criteria_met": "year_range; math_focus"},
            {"id": 6977, "year": 2018, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "inclusion_criteria_met": "year_range; math_focus"},
            {"id": 361, "year": 2024, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "inclusion_criteria_met": "year_range; math_focus"},
            {"id": 7001, "year": 2015, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "inclusion_criteria_met": "year_range; math_focus"},
        ]
    )

    corrected = apply_record_corrections(papers)
    rows = corrected.set_index("id")

    assert set(rows.index) == {8, 155, 361, 7001}
    assert rows.loc[361, "year"] == 2005
    assert rows.loc[361, "selection_stage"] == "screening"
    assert rows.loc[361, "exclusion_reason"] == "year_range"
    assert rows.loc[7001, "year"] == 1997
    assert rows.loc[7001, "selection_stage"] == "screening"
    assert rows.loc[7001, "exclusion_reason"] == "year_range"


def test_json_export_preserves_unmodified_source_text_and_removes_duplicate_rows() -> None:
    source = pd.DataFrame(
        [
            {"id": 361, "year": 2024, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "notes": "historical score"},
            {"id": 6952, "year": 2020, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "notes": "duplicate row"},
        ]
    )
    updated = pd.DataFrame(
        [
            {"id": 361, "year": 2005, "selection_stage": "screening", "status": "excluded", "exclusion_reason": "year_range", "notes": "corrected year", "abstract": "unchanged"},
        ]
    )
    original = [
        {"id": 361, "year": 2024, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "notes": "historical score", "abstract": "paragraph one\r\nparagraph two"},
        {"id": 6952, "year": 2020, "selection_stage": "prioritization", "status": "excluded", "exclusion_reason": "low_relevance_score", "notes": "duplicate row", "abstract": "duplicate"},
    ]

    records = _reconciled_json_records(source, updated, original)

    assert [record["id"] for record in records] == [361]
    assert records[0]["year"] == 2005
    assert records[0]["selection_stage"] == "screening"
    assert records[0]["exclusion_reason"] == "year_range"
    assert records[0]["notes"] == "corrected year"
    assert records[0]["abstract"] == "paragraph one\r\nparagraph two"


def test_current_scope_removes_superseded_mmat_fields_without_losing_other_notes() -> None:
    papers = pd.DataFrame(
        [
            {
                "id": 1,
                "selection_stage": "included",
                "status": "included",
                "exclusion_reason": "",
                "notes": '{"mmat_score": 4, "mmat_quality": "Alta", "keep": "context"}',
            },
            {
                "id": 99,
                "selection_stage": "screening",
                "status": "retained",
                "exclusion_reason": "",
                "notes": 'scope note; {"mmat_criteria": {"Q1": "Y"}, "keep": true}',
            },
        ]
    )
    scope = [
        {
            "study_id": "1",
            "selection_stage": "included",
            "selection_status": "included",
            "selection_reason": "",
            "record_status": "included_empirical_core",
        }
    ]

    updated = apply_current_scope_adjudications(papers, scope)

    assert all("mmat_" not in note for note in updated["notes"])
    assert '"keep": "context"' in updated.loc[updated["id"] == 1, "notes"].item()
    assert '"keep": true' in updated.loc[updated["id"] == 99, "notes"].item()


def test_public_export_notes_remove_only_superseded_mmat_fields() -> None:
    papers = pd.DataFrame(
        {
            "notes": [
                '{"mmat_score": 5, "mmat_quality": "Alta", "keep": true}',
                'scope note; {"mmat_criteria": {"Q1": "Y"}, "keep": "yes"}',
                "ordinary note without appraisal metadata",
            ]
        }
    )

    clean = remove_legacy_mmat_from_notes(papers)

    assert all("mmat_" not in note for note in clean["notes"])
    assert '"keep": true' in clean.loc[0, "notes"]
    assert '"keep": "yes"' in clean.loc[1, "notes"]
    assert clean.loc[2, "notes"] == papers.loc[2, "notes"]


def test_analysis_export_strips_legacy_mmat_without_mutating_input(tmp_path) -> None:
    papers = pd.DataFrame(
        {
            "id": [1],
            "notes": ['{"mmat_score": 3, "keep": "source note"}'],
        }
    )

    files = export_for_analysis(papers, tmp_path, formats=["csv", "json"])

    assert '"mmat_score"' not in files["csv"].read_text(encoding="utf-8-sig")
    assert '"mmat_score"' not in files["json"].read_text(encoding="utf-8")
    assert '"mmat_score"' in papers.loc[0, "notes"]
