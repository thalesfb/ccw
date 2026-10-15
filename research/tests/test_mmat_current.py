from __future__ import annotations

from src.analysis.mmat_current import (
    load_component_reassessments,
    CURRENT_RECORD_IDS,
    CURRENT_EMPIRICAL_STUDY_IDS,
    CURRENT_MMAT_STUDY_IDS,
    PENDING_UNIT_ADJUDICATION_STUDY_IDS,
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
import json
import pytest


CURRENT_TABLE = Path(__file__).resolve().parents[1] / "exports" / "references" / "mmat_current_tcc_table.tex"
EVIDENCE_MATRIX = Path(__file__).resolve().parents[1] / "data" / "manual_override_evidence_matrix.csv"
CURRENT_HTML = Path(__file__).resolve().parents[1] / "exports" / "analysis" / "mmat_current.html"
PAPERS_CSV = Path(__file__).resolve().parents[1] / "exports" / "analysis" / "papers.csv"
PAPERS_JSON = Path(__file__).resolve().parents[1] / "exports" / "analysis" / "papers.json"


def test_current_mmat_artifacts_use_exact_current_denominator() -> None:
    registry = load_current_registry()
    reassessment = load_current_reassessment()
    primary_sources = load_primary_sources()
    synthesis_scope = load_current_synthesis_scope()

    assert [int(row["study_id"]) for row in registry] == list(CURRENT_RECORD_IDS)
    assert [int(row["study_id"]) for row in reassessment] == list(CURRENT_RECORD_IDS)
    assert [int(row["study_id"]) for row in primary_sources] == list(CURRENT_RECORD_IDS)
    assert [int(row["study_id"]) for row in synthesis_scope] == list(CURRENT_RECORD_IDS)
    assert list(CURRENT_STUDY_IDS) == list(CURRENT_RECORD_IDS)
    assert [
        int(row["study_id"])
        for row in synthesis_scope
        if row["record_status"] == "included_empirical_core"
    ] == list(CURRENT_EMPIRICAL_STUDY_IDS)
    assert [
        int(row["study_id"])
        for row in synthesis_scope
        if row["empirical_mmat_applicability"] == "applicable"
    ] == list(CURRENT_MMAT_STUDY_IDS)
    assert PENDING_UNIT_ADJUDICATION_STUDY_IDS == (8,)
    assert all(row["mmat_status"] != "final" for row in registry)
    assert all(row["assessment_status"] != "final" for row in reassessment)
    assert all(row["reviewer"] == "single_reviewer" for row in reassessment)
    assert all(
        row["adjudication_status"] == "supervisor_review_pending"
        for row in reassessment
        if row["study_id"] != "9"
    )
    excluded_after_abstract = next(row for row in reassessment if row["study_id"] == "9")
    assert excluded_after_abstract["adjudication_status"] == "not_applicable_scope_exclusion"


def test_current_mmat_rejects_missing_review_provenance(monkeypatch) -> None:
    from src.analysis import mmat_current as current

    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            rows[0]["reviewer"] = ""
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="reviewer"):
        current.load_current_reassessment()


def test_current_mmat_qa_explicitly_blocks_final_claim() -> None:
    report = validate_current_artifacts()

    assert report["current_denominator"] == 14
    assert report["historical_denominator"] == 17
    assert report["criterion_rows"] == 11
    assert report["assessment_registry_rows"] == 18
    assert report["primary_source_rows"] == 18
    assert report["synthesis_scope_rows"] == 18
    assert report["empirical_evidence_rows"] == 15
    assert report["included_empirical_study_ids"] == list(CURRENT_EMPIRICAL_STUDY_IDS)
    assert report["mmat_unit_hold_ids"] == ["8"]
    assert report["mmat_unit_hold_rows"] == 1
    assert report["contextual_study_rows"] == 1
    assert report["awaiting_full_text_rows"] == 1
    assert report["contextual_protocol_rows"] == 1
    assert report["primary_text_reviewed_rows"] == 14
    assert report["source_or_period_hold_rows"] == 0
    assert report["source_or_period_hold_ids"] == []
    assert report["evidence_levels"]["primary_full_text_reviewed_externally"] == 14
    assert report["evidence_levels"]["abstract_and_metadata_only"] == 0
    assert report["evidence_levels"]["metadata_only"] == 0
    assert report["evidence_levels"]["protocol_or_proposal_not_applicable"] == 1
    assert report["record_evidence_levels"]["pending_full_text_not_appraised"] == 1
    assert report["record_evidence_levels"]["primary_full_text_reviewed_externally"] == 15
    assert report["record_evidence_levels"]["abstract_and_metadata_only"] == 1
    assert report["non_ct_criterion_decisions"] > 0
    assert report["final_ready"] is False
    assert report["blocking_reasons"]
    assert not any("source/year eligibility hold" in reason for reason in report["blocking_reasons"])


def test_record_excluded_after_abstract_screen_has_no_mmat_appraisal() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    excluded = rows["9"]

    assert excluded["assessment_basis"] == "abstract_and_metadata_only"
    assert excluded["assessment_status"] == "not_assessed_after_abstract_exclusion"
    assert all(
        excluded[criterion] == ""
        for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5")
    )
    assert excluded["criterion_evidence"] == ""


def test_current_mmat_evidence_matches_criterion_values() -> None:
    rows = load_current_reassessment()
    sources = {row["study_id"]: row for row in load_primary_sources()}
    registry = {row["study_id"]: row for row in load_current_registry()}

    assert all(
        row["criterion_evidence"].count(";") == (1 if row["design"] == "design_pending" else 6)
        for row in rows
        if row["study_id"] not in {"8", "9", "6923"}
    )
    assert rows[1]["assessment_status"] == "provisional_primary_source_review"
    assert rows[1]["q2"] == "CT"
    assert registry["6923"]["empirical_status"] == "empirical_full_text_pending"
    assert registry["6923"]["design_status"] == "abstract_based"
    for study_id in ("1", "5", "10"):
        assert registry[study_id]["empirical_status"] == "empirical_confirmed_external"
        assert registry[study_id]["snapshot_date"] == "2026-10-14"
        assert sources[study_id]["full_text_status"] == "externally_reviewed_not_archived"
        assert sources[study_id]["accessed_date"] == "2026-10-14"
    current_by_id = {row["study_id"]: row for row in rows}
    assert "early stopping" in current_by_id["1"]["notes"].lower()
    assert current_by_id["1"]["q5"] == "CT"
    assert current_by_id["5"]["design_status"] == "allocation_unreported_pending"
    assert all(current_by_id["5"][criterion] == "" for criterion in ("q1", "q2", "q3", "q4", "q5"))
    assert "allocation" in current_by_id["5"]["notes"].lower()
    assert "cited study [17]" in current_by_id["10"]["notes"]
    assert current_by_id["10"]["q5"] == "CT"
    assert registry["9"]["empirical_status"] == "empirical_abstract_only"
    study_6923 = next(row for row in rows if row["study_id"] == "6923")
    assert study_6923["assessment_basis"] == "pending_full_text_not_appraised"
    assert study_6923["assessment_status"] == "hold_source_verification"
    assert all(study_6923[criterion] == "" for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5"))
    assert study_6923["criterion_evidence"] == ""
    assert "mmat was not applied" in study_6923["notes"].lower()
    assert sources["6923"]["full_text_status"] == "not_retrieved"


def test_abstract_only_measurement_criteria_do_not_overclaim_appropriateness() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}

    for study_id in ("2", "3", "4", "6", "6917"):
        study = rows[study_id]
        assert study["q3"] == "CT"
        if study_id in {"2", "3", "6", "6917"}:
            assert "Q3=CT" in study["criterion_evidence"]
    assert "measurement appropriateness" in study["criterion_evidence"]
    for study_id in ("1", "5", "10"):
        study = rows[study_id]
        assert study["assessment_basis"] == "primary_full_text_reviewed_externally"
        assert study["assessment_status"] == "provisional_primary_source_review"
        assert study["adjudication_status"] == "supervisor_review_pending"
        assert study["criterion_evidence"].count(";") == (1 if study["design"] == "design_pending" else 6)
        assert study["page_or_section"]
    assert rows["6923"]["assessment_basis"] == "pending_full_text_not_appraised"
    assert rows["6923"]["assessment_status"] == "hold_source_verification"
    assert (
        "Q3=CT grades demographics and predictors are identified but measurement "
        "appropriateness is not established"
    ) in rows["4"]["criterion_evidence"]
    component = next(
        row for row in load_component_reassessments()
        if row["study_id"] == "6920" and row["component"] == "quantitative"
    )
    assert component["c3"] == "N"
    assert "independent measurement of the target" in component["evidence_c3"]


def test_descriptive_sampling_and_target_population_are_not_inferred() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    assert rows["6"]["q1"] == "CT"
    assert "relevance of the sampling procedure" in rows["6"]["criterion_evidence"].lower()

    assert rows["2"]["q2"] == "CT"
    assert "target population" in rows["2"]["criterion_evidence"].lower()
    assert rows["6920"]["q2"] == "Y"
    assert rows["6920"]["q3"] == "CT"
    assert "integrated outputs" in rows["6920"]["criterion_evidence"].lower()
    assert "target-predictor overlap is a quantitative component concern" in rows["6920"]["criterion_evidence"].lower()
    assert "divergences between quantitative and qualitative results" in rows["6920"]["criterion_evidence"].lower()
    component = next(
        row for row in load_component_reassessments()
        if row["study_id"] == "6920" and row["component"] == "quantitative"
    )
    assert component["c2"] == "CT"
    assert rows["6920"]["q4"] == "CT"
    assert "without clarifying cohort provenance" in component["evidence_c4"].lower()
    assert "whether missing cases create nonresponse bias" in component["evidence_c4"].lower()


def test_unreported_allocation_and_appraisal_unit_keep_design_pending() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    expected_statuses = {
        "7": "allocation_unreported_pending",
        "8": "unit_of_appraisal_pending",
        "14": "allocation_conflict_pending",
    }

    for study_id, design_status in expected_statuses.items():
        study = rows[study_id]
        assert study["design"] == "design_pending"
        assert study["design_status"] == design_status
        if study_id == "8":
            assert study["assessment_status"] == "hold_unit_of_appraisal"
            assert all(study[criterion] == "" for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5"))
            assert study["criterion_evidence"] == ""
        else:
            assert all(study[criterion] == "" for criterion in ("q1", "q2", "q3", "q4", "q5"))

    for study_id in ("7",):
        study = rows[study_id]
        for criterion in ("q1", "q2", "q3", "q4", "q5"):
            assert not study[criterion]
            assert f"{criterion.upper()}=" not in study["criterion_evidence"]


def test_appraisal_unit_pending_is_not_mmat_appraised_but_stays_in_empirical_scope() -> None:
    study = {row["study_id"]: row for row in load_current_reassessment()}["8"]
    scope = {row["study_id"]: row for row in load_current_synthesis_scope()}["8"]
    assert study["design"] == "design_pending"
    assert study["design_status"] == "unit_of_appraisal_pending"
    assert study["assessment_status"] == "hold_unit_of_appraisal"
    assert all(study[criterion] == "" for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5"))
    assert study["criterion_evidence"] == ""
    assert scope["record_status"] == "included_empirical_core"
    assert scope["selection_status"] == "included"
    assert scope["empirical_mmat_applicability"] == "pending_unit_adjudication"
    assert "appraisal unit" in study["notes"].lower()
    assert "79 students" in study["notes"]
    assert "10,052 available steps" in study["notes"]
    assert "4,568-step subset of student-executed actions" in study["notes"]
    assert "pre-existing" in study["notes"]


def test_nonrandomized_outcome_completeness_and_confounding_are_not_overstated() -> None:
    study = {row["study_id"]: row for row in load_current_reassessment()}["7"]
    assert study["design"] == "design_pending"
    assert study["design_status"] == "allocation_unreported_pending"
    assert all(study[criterion] == "" for criterion in ("q1", "q2", "q3", "q4", "q5"))
    assert "allocation procedure" in study["notes"].lower()


def test_study_7_full_text_sample_and_allocation_evidence_are_preserved() -> None:
    study = {row["study_id"]: row for row in load_current_reassessment()}["7"]
    source = {row["study_id"]: row for row in load_primary_sources()}["7"]

    assert study["review_date"] == "2026-10-15"
    assert "120 students" in study["notes"]
    assert "50 experimental" in study["notes"]
    assert "52 control" in study["notes"]
    assert "p=.583" in study["notes"]
    assert "does not establish equivalence" in study["notes"]
    assert "researchgate.net" in source["verification_note"].lower()
    assert "CC BY 4.0" in source["verification_note"]


def test_current_mmat_html_cells_match_the_versioned_ledger() -> None:
    import re

    html = CURRENT_HTML.read_text(encoding="utf-8")
    rows = {row["study_id"]: row for row in load_current_reassessment()}

    for study_id in rows:
        match = re.search(
            rf"<tr>\s*<td>{re.escape(study_id)}</td>(.*?)</tr>",
            html,
            flags=re.DOTALL,
        )
        assert match, f"Study {study_id} missing from generated MMAT page"
        answers = re.findall(
            r'<span class="criterion(?: [^"]*)?"[^>]*>(Y|N|CT|N/A|—)</span>',
            match.group(1),
        )
        expected = [
            rows[study_id][criterion] or "—"
            for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5")
        ]
        assert answers == expected, f"Study {study_id} HTML cells differ from the MMAT ledger"
        meta = re.search(r'<span class="study-meta">([^<]+)</span>', match.group(1))
        assert meta, f"Study {study_id} HTML design label missing"
        assert meta.group(1).startswith(f"{rows[study_id]['study_key']} · ")

    assert "uma apreciação preliminar separada dos componentes" in html.lower()
    assert "15 textos integrais no núcleo empírico" in html.lower()
    assert "nenhum critério recebeu resposta" in html.lower()
    assert "perguntas de triagem do mmat 2018" in html.lower()
    assert "há perguntas de pesquisa claras?" in html.lower()
    assert "17 candidatos empíricos submetidos ao mmat" not in html.lower()
    assert "15 registros empíricos incluídos provisoriamente" in html.lower()
    assert "14 têm s1/s2 respondidas" in html.lower()
    assert "11 têm apreciação preliminar dos critérios da categoria" in html.lower()

    for study_id, expected_text in {
        "7": ("120 students", "50 experimental", "52 control", "p=.583"),
        "8": ("79 estudantes", "10.052 passos", "4.568 ações", "unidade de análise"),
    }.items():
        row = re.search(
            rf"<tr>\s*<td>{re.escape(study_id)}</td>(.*?)</tr>",
            html,
            flags=re.DOTALL,
        )
        assert row
        evidence_row = re.search(
            r'<tr class="mmat-evidence-row">(.*?)</tr>',
            html[row.end():],
            flags=re.DOTALL,
        )
        assert evidence_row
        normalized_note = re.sub(r"<[^>]+>", " ", evidence_row.group(1)).lower()
        for text in expected_text:
            assert text.lower() in normalized_note

    for study_id in ("6923",):
        row = re.search(
            rf"<tr>\s*<td>{re.escape(study_id)}</td>(.*?)</tr>",
            html,
            flags=re.DOTALL,
        )
        assert row
        evidence_row = re.search(
            r'<tr class="mmat-evidence-row">(.*?)</tr>',
            html[row.end():],
            flags=re.DOTALL,
        )
        assert evidence_row
        assert "situação da fonte e da apreciação" in evidence_row.group(1).lower()
        assert "nenhum critério mmat foi aplicado" in evidence_row.group(1).lower()
        assert "texto integral pendente; mmat não aplicado" in row.group(1).lower()
        assert "não avaliado" in row.group(1).lower()
        assert 'class="criterion criterion-pending"' in row.group(1)
        assert "criterion-ct" not in row.group(1)
        assert "texto integral não recuperado; mmat não aplicado" in evidence_row.group(1).lower()
        assert "criterion-ct" not in evidence_row.group(1)

    abstract_excluded = re.search(
        r"<tr>\s*<td>9</td>(.*?)</tr>", html, flags=re.DOTALL
    )
    assert abstract_excluded
    assert "excluído após resumo; mmat não aplicado" in abstract_excluded.group(1).lower()
    assert "criterion-ct" not in abstract_excluded.group(1)


def test_general_paper_exports_do_not_publish_superseded_mmat_payloads() -> None:
    with PAPERS_CSV.open(encoding="utf-8-sig", newline="") as handle:
        csv_notes = [row["notes"] for row in csv.DictReader(handle)]
    json_notes = [row.get("notes", "") for row in json.loads(PAPERS_JSON.read_text(encoding="utf-8"))]

    assert all('"mmat_' not in note for note in csv_notes + json_notes if isinstance(note, str))

    readme = " ".join(
        (PAPERS_CSV.parents[1] / "README.md").read_text(encoding="utf-8").lower().split()
    )
    assert "ledger atual" in readme
    assert "não representam a avaliação vigente" in readme


def test_defense_material_preserves_pending_mmat_decisions() -> None:
    root = Path(__file__).resolve().parents[2]
    slides = " ".join((root / "presentation/slides.md").read_text(encoding="utf-8").lower().split())
    storyboard = " ".join(
        (root / "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md")
        .read_text(encoding="utf-8")
        .lower()
        .split()
    )
    speaker_notes = " ".join(
        (root / "results/tcc/presentation/ROTEIRO_FALAS_TCC.md")
        .read_text(encoding="utf-8")
        .lower()
        .split()
    )

    assert "nos estudos 5, 7 e 14, q1–q5 não foram avaliados até definir o delineamento" in slides
    assert "o estudo 8 permanece no fluxo prisma e no corpus, sem respostas mmat" in slides
    assert "q1--q5 permanecem sem resposta até a definição do delineamento" in storyboard
    assert "sem respostas mmat até adjudicação de elegibilidade e unidade de análise" in storyboard
    assert "sem classificá-lo como randomizado ou não randomizado" in speaker_notes
    assert "nenhum critério mmat recebeu resposta até a adjudicação" in speaker_notes


def test_newly_reviewed_primary_sources_have_traceable_provisional_appraisal() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    sources = {row["study_id"]: row for row in load_primary_sources()}

    for study_id in ("1", "5", "10", "14", "6915", "6919"):
        assert rows[study_id]["assessment_basis"] == "primary_full_text_reviewed_externally"
        assert rows[study_id]["assessment_status"] == "provisional_primary_source_review"
        assert rows[study_id]["adjudication_status"] == "supervisor_review_pending"
        assert rows[study_id]["page_or_section"]
        assert sources[study_id]["full_text_status"] == "externally_reviewed_not_archived"
        expected_access_date = {
            "1": "2026-10-14",
            "5": "2026-10-14",
            "10": "2026-10-14",
            "14": "2026-10-12",
            "6915": "2026-10-09",
            "6919": "2026-10-12",
        }[study_id]
        assert sources[study_id]["accessed_date"] == expected_access_date
        assert not sources[study_id]["local_file"]

    assert rows["6919"]["design"] == "mixed_methods"
    assert rows["6919"]["snapshot_date"] == "2026-09-03"
    assert rows["6919"]["review_date"] == "2026-10-11"
    assert rows["6919"]["empirical_status"] == "empirical_confirmed_external"
    assert "4.1.1" in rows["6919"]["page_or_section"]
    assert "4.4.8" in rows["6919"]["page_or_section"]
    assert "2021" in rows["6919"]["notes"] and "2025" in rows["6919"]["notes"]
    assert "no specific machine-learning algorithm was identified in the examined passages" in (
        rows["6919"]["notes"].lower()
    )
    assert "not evidence that the paper contains none" in rows["6919"]["notes"].lower()
    assert "component-level appraisal is recorded separately" in rows["6919"]["notes"].lower()
    assert "component-level appraisal is recorded separately and remains provisional" in (
        rows["6919"]["notes"].lower()
    )
    assert sources["6919"]["source_type"] == "publisher_html"
    assert "www.mdpi.com/2071-1050/18/4/1900" in sources["6919"]["source_url"]
    assert "10.3390/su18041900" in sources["6919"]["verification_note"]

    assert rows["14"]["design"] == "design_pending"
    assert rows["14"]["design_status"] == "allocation_conflict_pending"
    assert all(rows["14"][criterion] == "" for criterion in ("q1", "q2", "q3", "q4", "q5"))
    assert "random" in rows["14"]["notes"].lower()
    assert "45" in rows["6915"]["notes"] and "90" in rows["6915"]["notes"]
    assert [rows["6915"][criterion] for criterion in ("q1", "q2", "q3", "q4", "q5")] == [
        "CT", "Y", "CT", "N", "Y"
    ]
    assert rows["6915"]["q4"] == "N"
    assert "Nyantah et al. (2025) & Pendente & Y & Y & --- & --- & --- & --- & ---" in (
        CURRENT_TABLE.read_text(encoding="utf-8")
    )

    assert rows["7"]["q5"] == ""
    assert rows["7"]["design"] == "design_pending"
    assert "Q5=" not in rows["7"]["criterion_evidence"]

    mixed_evidence = rows["6919"]["criterion_evidence"].lower()
    assert "q1=y the article states a rationale for a mixed-methods approach" in mixed_evidence
    assert "q2=y quantitative and qualitative components are integrated" in mixed_evidence
    assert "q3=n the interpretation extends to longer-term gains" in mixed_evidence
    assert rows["6919"]["q4"] == "CT"
    assert "q4=ct the reviewed sections do not establish whether quantitative and qualitative findings diverge" in mixed_evidence
    assert "q5=n the quality of both components" in mixed_evidence


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


def test_pending_design_status_cannot_be_attached_to_a_classified_design(monkeypatch) -> None:
    from src.analysis import mmat_current as current

    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(item for item in rows if item["study_id"] == "7")
            row["design"] = "quantitative_nonrandomized"
            row["design_status"] = "allocation_unreported_pending"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="requires a pending MMAT design"):
        current.validate_current_artifacts()


def test_pending_appraisal_unit_rejects_any_mmat_response(monkeypatch) -> None:
    from src.analysis import mmat_current as current

    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(item for item in rows if item["study_id"] == "8")
            row["s1"] = "Y"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="when no MMAT appraisal was undertaken"):
        current.validate_current_artifacts()


def test_protocol_is_retained_only_as_contextual_non_empirical_record() -> None:
    scope = {row["study_id"]: row for row in load_current_synthesis_scope()}
    reassessment = {row["study_id"]: row for row in load_current_reassessment()}
    assert scope["6921"]["synthesis_role"] == "contextual_protocol"
    assert scope["6921"]["empirical_mmat_applicability"] == "not_applicable"
    assert reassessment["6921"]["design"] == "not_applicable"
    assert all(reassessment["6921"][criterion] == "N/A" for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5"))


def test_all_18_records_have_explicit_empirical_scope_and_text_status() -> None:
    scope = load_current_synthesis_scope()
    by_id = {row["study_id"]: row for row in scope}
    assert len(by_id) == 18
    assert sum(row["empirical_mmat_applicability"] == "applicable" for row in scope) == 14
    assert sum(row["empirical_mmat_applicability"] == "pending_unit_adjudication" for row in scope) == 1
    assert sum(row["empirical_mmat_applicability"] == "context_only" for row in scope) == 1
    assert sum(row["empirical_mmat_applicability"] == "pending_full_text" for row in scope) == 1
    assert sum(row["empirical_mmat_applicability"] == "not_applicable" for row in scope) == 1
    assert {study_id for study_id, row in by_id.items() if row["empirical_mmat_applicability"] == "pending_full_text"} == {"6923"}
    assert {study_id for study_id, row in by_id.items() if row["empirical_mmat_applicability"] == "context_only"} == {
        "9"
    }


def test_current_mmat_table_contains_only_the_14_appraised_empirical_studies() -> None:
    rows = load_current_table_rows()
    ids = [row["study_id"] for row in rows]
    assert len(ids) == 14
    assert set(ids) == {str(study_id) for study_id in CURRENT_MMAT_STUDY_IDS}
    assert not {"8", "9", "6921", "6923"}.intersection(ids)
    assert "6919" in ids
    rendered = render_current_table(rows)
    assert "14 estudos empíricos" in rendered
    assert "Denominador: 14 estudos" in rendered
    assert "S1 e S2 são perguntas de triagem." in rendered
    assert "Q1--Q5 correspondem aos critérios MMAT da categoria;" in rendered
    assert "para os estudos 6916, 6919 e 6920, Q1--Q5 representam a categoria de métodos mistos." in rendered
    assert "Quant. = quantitativo; rand. = randomizado." in rendered
    assert "Base = fonte documental consultada." in rendered
    note = rendered.split(r"\textit{Nota:}", 1)[1].splitlines()[0]
    assert len(note) <= 450
    tcc_results = Path(__file__).resolve().parents[2] / "results/tcc/conteudo/resultadosesperados.tex"
    prose = tcc_results.read_text(encoding="utf-8")
    assert "O estudo 8 permanece no fluxo PRISMA e no corpus" in prose
    assert "elegibilidade e unidade de apreciação aguardam adjudicação humana" in prose


def test_public_mmat_page_marks_study_8_as_unassessed_due_to_unit_hold() -> None:
    html = CURRENT_HTML.read_text(encoding="utf-8")
    assert "14 estudos empíricos" in html
    assert "unidade de análise pendente" in html.lower()
    study_row = html.split('<td>8</td>', 1)[1].split('</tr>', 1)[0]
    assert "MMAT suspenso" in study_row
    assert study_row.count('aria-label="Não avaliado"') == 7


def test_mmat_appraisal_corrects_unfounded_analysis_and_sampling_decisions() -> None:
    records = {row["study_id"]: row for row in load_current_reassessment()}
    assert records["3"]["q5"] == "CT"
    assert records["6"]["q5"] == "CT"
    assert records["6917"]["q1"] == "CT"
    assert records["6917"]["q2"] == "CT"


def test_design_status_records_appraisal_state_not_source_review_provenance() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    for study_id in ("2", "3", "4", "6", "6915", "6917"):
        assert rows[study_id]["design_status"] == "design_reassessed_provisional"
    assert all(
        row["design_status"] not in {
            "primary_text_reviewed_external",
            "primary_full_text_reviewed_provisional",
        }
        for row in rows.values()
    )


def test_unknown_design_status_is_rejected(monkeypatch) -> None:
    from src.analysis import mmat_current as current

    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            rows[0]["design_status"] = "primary_text_reviewed_external"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="Invalid design status"):
        current.load_current_reassessment()


def test_nonrandomized_adherence_rating_uses_intervention_delivery_evidence() -> None:
    study = next(row for row in load_current_reassessment() if row["study_id"] == "6915")
    assert study["q5"] == "Y"
    q5_evidence = study["criterion_evidence"].split(";")[-1].lower()
    assert "18 teaching periods" in q5_evidence
    assert "instructional plan" in q5_evidence
    assert "train validation test split" not in q5_evidence


def test_mixed_methods_studies_have_separate_component_appraisals() -> None:
    records = {row["study_id"]: row for row in load_current_reassessment()}
    assert {study_id for study_id, row in records.items() if row["design"] == "mixed_methods"} == {"6916", "6919", "6920"}
    components = load_component_reassessments()
    assert len(components) == 6
    assert {row["study_id"] for row in components} == {"6916", "6919", "6920"}
    assert all(row["review_status"] == "provisional_single_reviewer" for row in components)


def test_current_mmat_tcc_table_is_generated_from_the_current_ledger() -> None:
    assert CURRENT_TABLE.read_text(encoding="utf-8") == render_current_table(
        load_current_table_rows()
    )
    table = CURRENT_TABLE.read_text(encoding="utf-8")
    assert "Nyantah et al. (2025) & Pendente" in table
    assert "Xia et al. (2026)" in table
    assert "Xia et al. (2026)" in table
    assert "3.1 (CT):" in table
    assert "2.1 (CT):" not in table
    assert "3.1--3.5 (quantitativo não randomizado)" in table
    assert "ID" not in table
    assert "Enhancing2025" not in table


def test_study_6919_scope_evidence_reflects_the_latest_primary_text_review() -> None:
    with EVIDENCE_MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    study = next(row for row in rows if row["study_id"] == "6919")

    assert study["snapshot_date"] == "2026-10-12"
    assert study["source_type"] == "publisher_html"
    assert "www.mdpi.com/2071-1050/18/4/1900" in study["source_url"]
    assert study["source_status"] == "primary_full_text_reviewed_not_archived"
    assert "4.1.1" in study["evidence_locator"]
    assert "4.4.8" in study["evidence_locator"]
    assert "2021" in study["population_or_context"] and "2025" in study["population_or_context"]
    assert "ledger records no named ML algorithm in the examined passages" in (
        study["computational_role"]
    )
    assert study["adjudication_status"] == "proposed_pending_supervisor"
