from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TCC = ROOT / "results" / "tcc"


def test_selection_percentages_refer_to_records_not_a_study_population() -> None:
    review = (TCC / "conteudo" / "resultadosesperados.tex").read_text(encoding="utf-8")

    assert "parcela dos registros inicialmente identificados" in review
    assert "parcela da população inicialmente identificada" not in review
    assert "15 estudos compõem o corpus final" in review
    assert "17 candidatos empíricos provisórios" not in review
    assert "A população retida compreende" not in review


def test_study_specific_limitations_are_concentrated_in_the_gaps_section() -> None:
    review = (TCC / "conteudo" / "resultadosesperados.tex").read_text(encoding="utf-8")
    synthesis = review.split(r"\section{Caracterização dos Registros Selecionados Preliminarmente}", 1)[1].split(
        r"\section{Avaliação Metodológica com o MMAT}", 1
    )[0]
    gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
        r"\section{Limitações e Contribuições da Revisão}", 1
    )[0]

    detailed_caveats = (
        "oito turmas com 45 estudantes cada",
        "seis semanas",
        "oito itens da escala de mentalidade matemática",
    )
    for caveat in detailed_caveats:
        assert caveat not in synthesis
        assert caveat in gaps
    assert r"\ref{sec:tendencias-lacunas}" in synthesis


def test_tcc_front_pages_preserve_inactive_optional_templates() -> None:
    main = (TCC / "main.tex").read_text(encoding="utf-8")
    active_main = "\n".join(
        line for line in main.splitlines() if not line.lstrip().startswith("%")
    )
    for optional_page in ("dedicatoria", "agradecimentos", "epigrafe", "folhadeautorizacao"):
        assert rf"\include{{pretextuais/{optional_page}}}" not in active_main
        assert (TCC / "pretextuais" / f"{optional_page}.tex").is_file()


def test_pedagogical_support_uses_plain_language_without_mixing_theories() -> None:
    foundation = (TCC / "conteudo" / "fundamentacao.tex").read_text(encoding="utf-8")

    assert "apoio pedagógico temporário" in foundation
    assert "scaffolding" not in foundation.lower()
    assert "andaimento" not in foundation.lower()
    assert "Piaget" not in foundation


def test_introduction_cites_frameworks_and_limits_predictive_claims() -> None:
    introduction = (TCC / "conteudo" / "introducao.tex").read_text(encoding="utf-8")

    assert r"\cite{NRC2001}" in introduction
    assert r"\cite{PRISMA2020}" in introduction
    assert r"\cite{MMAT2018}" in introduction
    assert "sistemas tutores inteligentes" not in introduction


def test_mmat_does_not_infer_sampling_or_analysis_from_topic_relevance_alone() -> None:
    ledger_path = ROOT / "research" / "data" / "mmat_reassessment_current.csv"
    with ledger_path.open(encoding="utf-8-sig", newline="") as source:
        rows = {row["study_id"]: row for row in csv.DictReader(source)}

    for study_id in ("3", "4"):
        assert rows[study_id]["q1"] == "CT"
        evidence = next(
            item for item in rows[study_id]["criterion_evidence"].split(";")
            if item.startswith("Q1=")
        )
        assert "sampling" in evidence.lower() or "selection" in evidence.lower()

    assert rows["1"]["s1"] == "Y" and rows["1"]["s2"] == "Y"
    assert rows["1"]["q1"] == "Y"
    assert rows["5"]["assessment_status"] == "provisional_primary_source_review"
    assert rows["5"]["design_status"] == "operational_category_inferred_allocation_unknown"
    assert all(rows["5"][criterion] == "CT" for criterion in ("q1", "q2", "q3", "q4", "q5"))
    assert rows["10"]["s1"] == "Y" and rows["10"]["s2"] == "Y"
    for study_id in ("6923", "9"):
        assert all(rows[study_id][criterion] == "" for criterion in ("s1", "s2", "q1", "q2", "q3", "q4", "q5"))
        assert rows[study_id]["criterion_evidence"] == ""
    assert rows["9"]["assessment_status"] == "not_assessed_scope_exclusion_confirmed"
    assert rows["9"]["assessment_basis"] == "primary_full_text_scope_exclusion"
    assert rows["9"]["design"] == "not_applicable"

    methodology = " ".join(
        (TCC / "conteudo" / "metodologia.tex")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "A pertinência temática de um estudo não substitui nenhum critério metodológico." in methodology
    assert r"\cite{MMATGuide2018}" in methodology
