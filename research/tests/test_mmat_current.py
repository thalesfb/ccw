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
import re
import pytest


def test_operational_appraisal_decisions_are_explicit_and_do_not_certify_allocation():
    rows = {r['study_id']: r for r in load_current_reassessment()}
    assert rows['8']['design'] == 'quantitative_descriptive'
    assert [rows['8'][k] for k in ('s1','s2','q1','q2','q3','q4','q5')] == ['Y','Y','Y','CT','CT','CT','CT']
    assert rows['14']['design'] == 'quantitative_randomized'
    assert [rows['14'][k] for k in ('q1','q2','q3','q4','q5')] == ['CT','N','Y','CT','CT']
    for sid in ('5', '7'):
        assert rows[sid]['design'] == 'quantitative_nonrandomized'
        assert all(rows[sid][k] == 'CT' for k in ('q1','q2','q3','q4','q5'))
        assert rows[sid]['adjudication_status'] == 'supervisor_review_pending'
    decision_path = Path(__file__).resolve().parents[1] / 'data/mmat_operational_decisions_2026-10-28.json'
    decisions = {d['study_id']: d for d in json.loads(decision_path.read_text(encoding='utf-8'))['decisions']}
    for sid, decision in decisions.items():
        assert decision['answers'] == [rows[sid][f'q{i}'] for i in range(1, 6)]
        assert decision['status'] == rows[sid]['design_status']
        for key in ('s1', 's2'):
            assert decision['screening'][key]['answer'] == rows[sid][key]
            assert decision['screening'][key]['rationale_pt'] in rows[sid]['criterion_evidence']
    assert 'historical_pdf_sha256' in decisions['7'] and 'source_sha256' not in decisions['7']
    assert decisions['7']['reviewed_url'].startswith('https://www.researchgate.net/')


def test_followup_questions_cover_every_indeterminate_criterion_and_structural_hold():
    from src.analysis.mmat_followups import load_questions, validate_questions, render_markdown
    questions = load_questions()
    validate_questions(questions)
    expected = {
        (r["study_id"], "study", key.upper())
        for r in load_current_reassessment()
        for key in ("s1", "s2", "q1", "q2", "q3", "q4", "q5") if r[key] == "CT"
    } | {
        (r["study_id"], r["component"], key.upper())
        for r in load_component_reassessments()
        for key in ("c1", "c2", "c3", "c4", "c5") if r[key] == "CT"
    }
    actual = {(q["study_id"], q["component"], q["criterion"]) for q in questions if q["component"] != "record"}
    assert actual == expected
    assert len(actual) == 72
    assert {q["study_id"] for q in questions if q["criterion"] == "design"} == set()
    assert all(q["status"] == "prepared_not_sent" for q in questions)
    report = Path(__file__).resolve().parents[2] / "docs/tcc/MMAT-PERGUNTAS-PENDENTES.md"
    assert report.read_text(encoding="utf-8") == render_markdown(questions)
    with pytest.raises(ValueError, match="coverage"):
        validate_questions(questions[1:])


def test_resolved_documentary_tasks_do_not_promote_indeterminate_mmat_answers():
    records = {r['study_id']: r for r in load_current_reassessment()}
    assert records['6916']['q5'] == 'CT'
    assert 'pending the separate component appraisal' not in records['6916']['criterion_evidence']
    assert 'componentes já apreciados' in records['6916']['criterion_evidence']
    for study_id in ('2', '6', '6917'):
        assert 'físicas' in records[study_id]['page_or_section']
    components = {(r['study_id'], r['component']): r for r in load_component_reassessments()}
    quantitative = components[('6920', 'quantitative')]
    assert quantitative['c2'] == 'CT'
    assert 'população-alvo mais ampla' not in quantitative['evidence_c2']
    assert '428' in quantitative['evidence_c2'] and '633' in quantitative['evidence_c2']
    qualitative = components[('6920', 'qualitative')]
    assert qualitative['c5'] == 'CT'
    assert 'registros dos estudantes' not in qualitative['evidence_c5']
    for component in ('quantitative', 'qualitative'):
        assert 'Páginas físicas' in components[('6919', component)]['source_locator']
        assert 'não revalidado' not in components[('6919', component)]['source_locator']
    assert 'Revalidado no PDF primário em 29/10/2026' in records['6919']['notes']


def test_pending_page_distinguishes_documentary_tasks_from_uncertain_article_reporting():
    html = CURRENT_HTML.read_text(encoding='utf-8')
    assert 'CT não é uma tarefa incompleta' in html
    assert 'não depende de obter resposta a todas as perguntas' in html
    assert 'Tarefas de consolidação' in html
    assert '16/05/2027' in html
    assert '75 envios obrigatórios' not in html
    import json
    actions = json.loads((Path(__file__).resolve().parents[1] / 'data/mmat_consolidation_actions_current.json').read_text(encoding='utf-8'))
    assert len({a['id'] for a in actions['actions']}) == len(actions['actions'])
    assert any(a['status'] == 'completed_documentary' for a in actions['actions'])
    assert any(a['status'] == 'pending_human_review' for a in actions['actions'])
    assert all(a['evidence'] and a['next_step'] for a in actions['actions'])


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
    assert PENDING_UNIT_ADJUDICATION_STUDY_IDS == ()
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


def test_registry_preserves_operational_routes_and_unknown_allocation():
    registry = {r['study_id']: r for r in load_current_registry()}
    ledger = {r['study_id']: r for r in load_current_reassessment()}
    for sid in ('5','7','8','14'):
        assert registry[sid]['design_status'] == ledger[sid]['design_status']
    assert ledger['5']['design_status'] == ledger['7']['design_status'] == 'operational_category_inferred_allocation_unknown'
    assert ledger['8']['design_status'] == 'operational_category_adaptation'
    assert ledger['14']['design_status'] == 'design_reassessed_provisional_with_allocation_conflict'



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

    assert report["current_denominator"] == 15
    assert report["historical_denominator"] == 17
    assert report["criterion_rows"] == 15
    assert report["assessment_registry_rows"] == 18
    assert report["current_mmat_ledger_rows"] == 18
    assert report["historical_mmat_assessment_rows"] == 17
    assert report["primary_source_rows"] == 18
    assert report["synthesis_scope_rows"] == 18
    assert report["empirical_evidence_rows"] == 15
    assert report["included_empirical_study_ids"] == list(CURRENT_EMPIRICAL_STUDY_IDS)
    assert report["mmat_unit_hold_ids"] == []
    assert report["mmat_unit_hold_rows"] == 0
    assert report["contextual_study_rows"] == 1
    assert report["awaiting_full_text_rows"] == 1
    assert report["contextual_protocol_rows"] == 1
    assert report["primary_text_reviewed_rows"] == 15
    assert report["source_or_period_hold_rows"] == 0
    assert report["source_or_period_hold_ids"] == []
    assert report["evidence_levels"]["primary_full_text_reviewed_externally"] == 15
    assert report["evidence_levels"]["abstract_and_metadata_only"] == 0
    assert report["evidence_levels"]["metadata_only"] == 0
    assert report["evidence_levels"]["protocol_or_proposal_not_applicable"] == 1
    assert report["record_evidence_levels"]["pending_full_text_not_appraised"] == 1
    assert report["record_evidence_levels"]["primary_full_text_reviewed_externally"] == 15
    assert report["record_evidence_levels"]["abstract_and_metadata_only"] == 0
    assert report["record_evidence_levels"]["primary_full_text_scope_exclusion"] == 1
    assert report["non_ct_criterion_decisions"] > 0
    assert report["final_ready"] is False
    assert report["blocking_reasons"]
    assert not any("source/year eligibility hold" in reason for reason in report["blocking_reasons"])


def test_historical_mmat_count_requires_unique_record_ids(tmp_path) -> None:
    historical_mmat = tmp_path / "historical-mmat.csv"
    historical_mmat.write_text(
        "ID,Title\nlegacy-1,First record\nlegacy-1,Duplicate record\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unique, non-empty IDs"):
        validate_current_artifacts(historical_mmat_path=historical_mmat)


def test_full_text_confirmation_preserves_scope_exclusion_without_mmat() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    excluded = rows["9"]

    assert excluded["assessment_basis"] == "primary_full_text_scope_exclusion"
    assert excluded["assessment_status"] == "not_assessed_scope_exclusion_confirmed"
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
        if row["study_id"] not in {"8", "9", "6921", "6923"}
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
    assert current_by_id["5"]["design_status"] == "operational_category_inferred_allocation_unknown"
    assert all(current_by_id["5"][criterion] == "CT" for criterion in ("q1", "q2", "q3", "q4", "q5"))
    assert "alocação" in current_by_id["5"]["notes"].lower()
    assert "cited study [17]" in current_by_id["10"]["notes"]
    assert current_by_id["10"]["q5"] == "CT"
    assert registry["9"]["empirical_status"] == "empirical_outside_mathematics_scope"
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
    assert "adequação dos indicadores" in rows["6917"]["criterion_evidence"]
    for study_id in ("1", "5", "10"):
        study = rows[study_id]
        assert study["assessment_basis"] == "primary_full_text_reviewed_externally"
        assert study["assessment_status"] == "provisional_primary_source_review"
        assert study["adjudication_status"] == "supervisor_review_pending"
        assert study["criterion_evidence"].count(";") == (1 if study["design"] == "design_pending" else 6)
        assert study["page_or_section"]
    assert rows["6923"]["assessment_basis"] == "pending_full_text_not_appraised"
    assert rows["6923"]["assessment_status"] == "hold_source_verification"
    assert "Q3=CT binary and five-class grade thresholds" in rows["4"]["criterion_evidence"]
    assert "selected predictor subsets are insufficiently specified" in rows["4"]["criterion_evidence"]
    component = next(
        row for row in load_component_reassessments()
        if row["study_id"] == "6920" and row["component"] == "quantitative"
    )
    assert component["c3"] == "N"
    assert "mensuração independente do alvo" in component["evidence_c3"]


def test_descriptive_sampling_and_target_population_are_not_inferred() -> None:
    rows = {row["study_id"]: row for row in load_current_reassessment()}
    assert rows["6"]["q1"] == "Y"
    assert rows["6"]["q2"] == "CT"
    assert "não demonstra representatividade" in rows["6"]["criterion_evidence"].lower()

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
    assert "sem esclarecer a origem dos grupos" in component["evidence_c4"].lower()
    assert "se os casos ausentes produzem viés de não resposta" in component["evidence_c4"].lower()


def test_operational_routes_do_not_claim_confirmed_study_designs():
    rows = {r['study_id']: r for r in load_current_reassessment()}
    for sid in ('5','7'):
        assert rows[sid]['design_status'] == 'operational_category_inferred_allocation_unknown'
        assert 'não confirma' in rows[sid]['notes'] or 'sem certificar' in rows[sid]['notes'] or 'sem afirmar' in rows[sid]['notes']
    assert 'não corresponde literalmente' in rows['8']['notes']
    assert rows['14']['q1'] == 'CT'



def test_thesis_unit_is_one_report_without_duplicate_fractions_or_inherited_trial_design():
    study = {r['study_id']: r for r in load_current_reassessment()}['8']
    scope = {r['study_id']: r for r in load_current_synthesis_scope()}['8']
    assert scope['record_status'] == 'included_empirical_core'
    assert scope['empirical_mmat_applicability'] == 'applicable'
    assert study['s1'] == study['s2'] == 'Y'
    assert study['design_status'] == 'operational_category_adaptation'
    assert 'Frações são reutilizadas' in study['notes']
    assert 'não classifica a tese inteira como ensaio randomizado' in study['notes']



def test_unknown_allocation_completeness_and_confounding_remain_indeterminate():
    study = {r['study_id']: r for r in load_current_reassessment()}['7']
    assert study['design_status'] == 'operational_category_inferred_allocation_unknown'
    assert study['q3'] == study['q4'] == 'CT'
    assert 'alocação' in study['notes']



def test_study_7_sample_allocation_and_access_limits_are_preserved():
    study = {r['study_id']: r for r in load_current_reassessment()}['7']
    assert study['review_date'] == '2026-10-28'
    assert '120 participantes' in study['notes'] and '50/52' in study['notes']
    assert 'não prova completude' in study['notes']
    assert 'não se declara nova recuperação do PDF' in study['notes']
    assert 'p=0,583' in study['criterion_evidence']



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
            r'<span class="criterion(?: [^"]*)?"[^>]*>(Y|N|CT|—)</span>',
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
    assert "15 registros com consulta documental declarada" in html.lower()
    assert "não comprova leitura humana integral" in html.lower()
    assert "não recebeu respostas MMAT" in html
    assert "perguntas de triagem do mmat 2018" in html.lower()
    assert "há perguntas de pesquisa claras?" in html.lower()
    assert "17 candidatos empíricos submetidos ao mmat" not in html.lower()
    assert "15 registros empíricos incluídos provisoriamente" in html.lower()
    assert "15 têm s1/s2 respondidas" in html.lower()
    assert "15 têm apreciação preliminar dos critérios da categoria" in html.lower()

    for study_id, expected_text in {
        "7": ("120 participantes", "50/52", "não prova completude"),
        "8": ("uma tese", "Frações são reutilizadas", "empírico computacional"),
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
    assert "texto integral conferido; fora do escopo matemático" in abstract_excluded.group(1).lower()
    assert "criterion-ct" not in abstract_excluded.group(1)


def test_mmat_longtables_allow_natural_pagination() -> None:
    from src.analysis.mmat_current_tcc_table import load_rows, render_table

    prefix = render_table(load_rows()).split(r"\begin{longtable}", 1)[0]
    assert r"\clearpage" not in prefix


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
    assert "estudos 5 e 7: categoria 3 operacional, alocação desconhecida" in slides
    assert "estudo 8: categoria 4 adaptada" in slides
    assert "categoria 3 operacional" in storyboard
    assert "categoria 4 adaptada" in storyboard


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
            "6919": "2026-10-17",
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

    assert rows["14"]["design"] == "quantitative_randomized"
    assert rows["14"]["design_status"] == "design_reassessed_provisional_with_allocation_conflict"
    assert [rows["14"][criterion] for criterion in ("q1", "q2", "q3", "q4", "q5")] == ["CT","N","Y","CT","CT"]
    assert "random" in rows["14"]["notes"].lower()
    assert "45" in rows["6915"]["notes"] and "90" in rows["6915"]["notes"]
    assert [rows["6915"][criterion] for criterion in ("q1", "q2", "q3", "q4", "q5")] == [
        "CT", "Y", "CT", "N", "Y"
    ]
    assert rows["6915"]["q4"] == "N"
    assert r"\citeonline{Enhancing2025_012} & Cat. 2 declarada (contraditória) & Y & Y & CT & N & Y & CT & CT" in (
        CURRENT_TABLE.read_text(encoding="utf-8")
    )

    assert rows["7"]["q5"] == "CT"
    assert rows["7"]["design"] == "quantitative_nonrandomized"
    assert "Q5=CT" in rows["7"]["criterion_evidence"]

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
            row["design"] = "design_pending"
            row["design_status"] = "allocation_conflict_pending"
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
            row["design"] = "design_pending"
            row["design_status"] = "unit_of_appraisal_pending"
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
    assert all(reassessment["6921"][criterion] == "" for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5"))
    assert reassessment["6921"]["criterion_evidence"] == ""


@pytest.mark.parametrize("study_id", ["1", "6921"])
def test_na_is_a_record_status_not_an_mmat_criterion_response(monkeypatch, study_id) -> None:
    from src.analysis import mmat_current as current

    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(item for item in rows if item["study_id"] == study_id)
            row["q1"] = "N/A"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="Invalid q1 response"):
        current.load_current_reassessment()


def test_all_18_records_have_explicit_empirical_scope_and_text_status() -> None:
    scope = load_current_synthesis_scope()
    by_id = {row["study_id"]: row for row in scope}
    assert len(by_id) == 18
    assert sum(row["empirical_mmat_applicability"] == "applicable" for row in scope) == 15
    assert sum(row["empirical_mmat_applicability"] == "pending_unit_adjudication" for row in scope) == 0
    assert sum(row["empirical_mmat_applicability"] == "context_only" for row in scope) == 1
    assert sum(row["empirical_mmat_applicability"] == "pending_full_text" for row in scope) == 1
    assert sum(row["empirical_mmat_applicability"] == "not_applicable" for row in scope) == 1
    assert {study_id for study_id, row in by_id.items() if row["empirical_mmat_applicability"] == "pending_full_text"} == {"6923"}
    assert {study_id for study_id, row in by_id.items() if row["empirical_mmat_applicability"] == "context_only"} == {
        "9"
    }


def test_current_mmat_table_contains_only_records_with_screening_responses() -> None:
    rows = load_current_table_rows()
    ids = [row["study_id"] for row in rows]
    assert len(ids) == 15
    assert set(ids) == {str(study_id) for study_id in CURRENT_MMAT_STUDY_IDS}
    assert not {"9", "6921", "6923"}.intersection(ids)
    assert "6919" in ids
    rendered = render_current_table(rows)
    assert "15 estudos do corpus" in rendered
    main_table, component_table = rendered.split(r"\label{qua:mmat-componentes}", 1)
    assert len(re.findall(r"^\\citeonline\{[^}]+\} &", main_table, re.M)) == 15
    assert len(re.findall(r"^\\citeonline\{[^}]+\} &", component_table, re.M)) == 6
    assert "S1/S2 = perguntas de triagem" in rendered
    assert "Q1--Q5 = critérios da categoria" in rendered
    assert rendered.index(r"\fonte{Elaborado pelo autor (2026).}") < rendered.index(r"\endgroup")
    assert "Quant. = quantitativo; rand. = randomizado." in rendered
    assert r"\textbf{Base}" not in rendered
    note = rendered.split(r"\textit{Nota:}", 1)[1].splitlines()[0]
    assert len(note) <= 450
    tcc_results = Path(__file__).resolve().parents[2] / "results/tcc/conteudo/resultadosesperados.tex"
    prose = tcc_results.read_text(encoding="utf-8")
    assert r"A categoria 4 foi adaptada à modelagem computacional da tese de \citeonline{Computational2017_008}" in prose
    assert "As categorias utilizadas provisoriamente não confirmam delineamentos" in prose
    assert "adjudicação" not in prose


def test_public_mmat_page_marks_operational_routes_without_certifying_designs():
    html = CURRENT_HTML.read_text(encoding='utf-8')
    assert '15 estudos empíricos' in html
    assert 'Categoria 4 adaptada · modelagem computacional' in html
    assert 'Categoria 3 operacional · alocação desconhecida' in html
    assert 'Categoria 2 declarada · alocação contraditória' in html
    assert 'essas rotas não certificam delineamentos' in html.lower()



def test_mmat_appraisal_corrects_unfounded_analysis_and_sampling_decisions() -> None:
    records = {row["study_id"]: row for row in load_current_reassessment()}
    assert records["3"]["q5"] == "CT"
    assert records["6"]["q5"] == "CT"
    assert records["6917"]["q1"] == "Y"
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
    assert r"\citeonline{Enhancing2025_012} & Cat. 2 declarada" in table
    assert r"\citeonline{UniversityMathematics2026_6919} & Métodos mistos" in table
    assert r"\citeonline{UniversityMathematics2026_6919} & Quant. não rand." in table
    assert "3.1 (CT):" in table
    assert "2.1 (CT):" not in table
    assert r"\ref{sec:avaliacao-qualidade}" in table
    assert "ID" not in table
    assert "Nyantah et al. (2025)" not in table


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
