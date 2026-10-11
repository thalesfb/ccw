from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TCC = ROOT / "results" / "tcc"


def test_selection_percentages_refer_to_records_not_a_study_population() -> None:
    review = (TCC / "conteudo" / "resultadosesperados.tex").read_text(encoding="utf-8")

    assert "parcela dos registros inicialmente identificados" in review
    assert "parcela da população inicialmente identificada" not in review
    assert "O corpus retido compreende 17 candidatos empíricos provisórios" in review
    assert "A população retida compreende" not in review


def test_study_specific_limitations_are_concentrated_in_the_gaps_section() -> None:
    review = (TCC / "conteudo" / "resultadosesperados.tex").read_text(encoding="utf-8")
    synthesis = review.split(r"\section{Síntese dos Estudos Incluídos}", 1)[1].split(
        r"\section{Avaliação Metodológica com o MMAT}", 1
    )[0]
    gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
        r"\section{Limitações e Contribuições da Revisão}", 1
    )[0]

    detailed_caveats = (
        "45 estudantes por turma",
        "seis semanas",
        "oito itens da escala de mentalidade matemática",
    )
    for caveat in detailed_caveats:
        assert caveat not in synthesis
        assert caveat in gaps
    assert r"\ref{sec:tendencias-lacunas}" in synthesis


def test_tcc_front_pages_exclude_unfilled_optional_elements() -> None:
    main = (TCC / "main.tex").read_text(encoding="utf-8")
    for optional_page in ("dedicatoria", "agradecimentos", "epigrafe", "folhadeautorizacao"):
        assert rf"\include{{pretextuais/{optional_page}}}" not in main
        assert not (TCC / "pretextuais" / f"{optional_page}.tex").exists()


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

    for study_id in ("1", "3", "4", "9", "10"):
        assert rows[study_id]["q1"] == "CT"
        evidence = next(
            item for item in rows[study_id]["criterion_evidence"].split(";")
            if item.startswith("Q1=")
        )
        assert "sampling" in evidence.lower() or "selection" in evidence.lower()

    assert rows["9"]["q5"] == "CT"
    q5_evidence = next(
        item for item in rows["9"]["criterion_evidence"].split(";")
        if item.startswith("Q5=")
    )
    assert "analysis" in q5_evidence.lower()

    methodology = " ".join(
        (TCC / "conteudo" / "metodologia.tex")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "a pertinência temática do conjunto de dados não foi considerada suficiente" in methodology
    assert r"\cite{MMATGuide2018}" in methodology
