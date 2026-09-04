"""Regression checks for the corrections requested in the advisor feedback."""

from __future__ import annotations

import csv
import re
from pathlib import Path

from src.analysis.mmat_current_tcc_table import load_rows, render_table


REPO_ROOT = Path(__file__).resolve().parents[2]
TCC_ROOT = REPO_ROOT / "results" / "tcc"
TCC_CONTENT = TCC_ROOT / "conteudo"
TCC_ABSTRACT = TCC_ROOT / "pretextuais" / "resumo.tex"
MMAT_DATA = REPO_ROOT / "research" / "data" / "mmat_reassessment_current.csv"
MMAT_LATEX = REPO_ROOT / "research" / "exports" / "references" / "mmat_current_tcc_table.tex"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _all_tex() -> str:
    return "\n".join(_read(path) for path in sorted(TCC_ROOT.rglob("*.tex")))


def test_no_duplicated_latex_emphasis_commands() -> None:
    source = _all_tex()
    forbidden = {
        "nested textbf": r"\\textbf\{\s*\\textbf\{",
        "nested textit": r"\\textit\{\s*\\textit\{",
        "nested emph": r"\\emph\{\s*\\emph\{",
    }
    found = [name for name, pattern in forbidden.items() if re.search(pattern, source)]
    assert not found, f"Duplicated LaTeX formatting found: {found}"


def test_cache_percentages_are_not_reported_as_stable_metrics() -> None:
    source = _all_tex()
    fixed_cache_claim = re.compile(
        r"(?is)(?:cache.{0,100}(?:63\s*\\?%|92\s*\\?%|265\s*/\s*287)|"
        r"(?:63\s*\\?%|92\s*\\?%|265\s*/\s*287).{0,100}cache)"
    )
    assert not fixed_cache_claim.search(source)
    assert "Um acerto de cache ocorre" in _read(TCC_CONTENT / "metodologia.tex")


def test_prisma_reporting_and_protocol_are_not_conflated() -> None:
    methodology = _read(TCC_CONTENT / "metodologia.tex")
    lowered = methodology.lower()
    assert "prisma 2020" in lowered
    assert "diretriz de relato" in lowered
    assert "prisma-p 2015" in lowered
    assert "protocolos de revisões sistemáticas" in lowered
    assert "não se afirma conformidade integral com o prisma-p" in lowered
    for unsupported in (
        "seguiu integralmente",
        "seguiu rigorosamente",
        "aderência integral ao prisma-p",
        "foi integralmente aderente ao prisma-p",
    ):
        assert unsupported not in lowered


def test_current_deduplication_description_matches_identity_audit() -> None:
    methodology = _read(TCC_CONTENT / "metodologia.tex")
    assert "DOI normalizado" in methodology
    assert "URL exata" in methodology
    assert "27 linhas excedentes" in methodology
    assert "232 excedentes" in methodology
    assert "não foram removidos automaticamente por título" in methodology


def test_interpretation_precedes_the_long_synthesis_table() -> None:
    chapter = _read(TCC_CONTENT / "resultadosesperados.tex")
    interpretation = chapter.index("Antes da tabela detalhada")
    table = chapter.index(r"\label{tab:sintese-estudos-empiricos}")
    assert interpretation < table


def test_long_python_identifier_is_breakable() -> None:
    source = _all_tex()
    assert r"\texttt{RandomForest\allowbreak Classifier}" in source
    assert r"\texttt{RandomForestClassifier}" not in source
    assert r"\path{RandomForestClassifier}" not in source
    assert r"\nolinkurl{RandomForestClassifier}" not in source


def test_tcc_uses_conclusive_voice_without_fabricated_results() -> None:
    key_files = [
        TCC_ABSTRACT,
        TCC_CONTENT / "introducao.tex",
        TCC_CONTENT / "fundamentacao.tex",
        TCC_CONTENT / "metodologia.tex",
        TCC_CONTENT / "resultadosesperados.tex",
        TCC_CONTENT / "prototipo.tex",
        TCC_CONTENT / "resultados.tex",
        TCC_CONTENT / "conclusao.tex",
        TCC_CONTENT / "cronograma.tex",
    ]
    source = "\n".join(_read(path) for path in key_files).lower()

    proposal_markers = (
        "como próxima etapa",
        "a próxima etapa deverá",
        "etapa posterior de prototipação",
        "etapas ainda pendentes",
        "será destinado aos resultados",
        "resultados que deverão ser documentados",
        "permanece reservado para resultados",
        "a conclusão final deverá ser atualizada",
        "será escolhido antes da implementação",
        "o capítulo não apresenta implementação concluída",
        "em andamento &",
        "planejado \\",
    )
    for marker in proposal_markers:
        assert marker not in source, f"Proposal-style marker remains: {marker}"

    unsupported_completion_claims = (
        "o protótipo foi implementado",
        "foi desenvolvido um protótipo funcional",
        "foram executados experimentos em contexto escolar real",
        "o tcc foi submetido e defendido",
        "o projeto foi concluído em todas as suas fases",
    )
    for claim in unsupported_completion_claims:
        assert claim not in source

    introduction = _read(TCC_CONTENT / "introducao.tex")
    prototype = _read(TCC_CONTENT / "prototipo.tex")
    results = _read(TCC_CONTENT / "resultados.tex")
    conclusion = _read(TCC_CONTENT / "conclusao.tex")
    abstract = _read(TCC_ABSTRACT)

    assert "O escopo executado compreendeu" in introduction
    assert "especificação conceitual do protótipo" in prototype
    assert "não foi tratada como evidência de uma aplicação funcional" in prototype
    assert "O objetivo geral foi alcançado" in results
    assert "Este trabalho investigou" in conclusion
    assert "Como contribuições, o trabalho produziu" in abstract


def test_learning_concepts_and_teacher_role_are_explicit() -> None:
    foundation = _read(TCC_CONTENT / "fundamentacao.tex")
    for concept in (
        "Desempenho observado",
        "Proficiência estimada",
        "Competência",
        "Aprendizagem",
        "conhecimento prévio",
        "resolução de problemas",
        "avaliação formativa",
    ):
        assert concept.lower() in foundation.lower()
    assert "o professor permanece responsável" in foundation.lower()
    assert "não observa diretamente todos os processos" in foundation.lower()


def test_mmat_is_criterion_level_and_has_auditable_provenance() -> None:
    for path in (MMAT_DATA,):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        assert len(rows) == 18
        assert "score" not in (reader.fieldnames or [])
        assert "quality" not in (reader.fieldnames or [])
        assert {"q1", "q2", "q3", "q4", "q5"} <= set(reader.fieldnames or [])
        assert {"assessment_basis", "reviewer", "notes"} <= set(
            reader.fieldnames or []
        )
        assert all(row["assessment_basis"].strip() for row in rows)
        assert all(row["reviewer"].strip() for row in rows)
        assert all(row["notes"].strip() for row in rows)

    assert MMAT_LATEX.read_text(encoding="utf-8") == render_table(load_rows())

    chapter = _read(TCC_CONTENT / "resultadosesperados.tex")
    mmat_section = chapter[chapter.index("Avaliação Metodológica com o MMAT") :]
    assert not re.search(r"\b[0-5]\s*/\s*5\b", mmat_section)
    assert "sem média, ranking ou categoria geral" in mmat_section
    assert r"\input{../../research/exports/references/mmat_current_tcc_table.tex}" in chapter
    assert "Tjahyadi (2025) & Quant." not in chapter


def test_author_created_sources_use_the_standard_year_form() -> None:
    invalid: list[str] = []
    pattern = re.compile(r"\\fonte\{(Elaborado pelo autor[^}]*)\}")
    expected = re.compile(r"Elaborado pelo autor \((?:19|20)\d{2}\)\.")

    for path in sorted(TCC_ROOT.rglob("*.tex")):
        for source in pattern.findall(_read(path)):
            if not expected.fullmatch(source):
                invalid.append(f"{path.relative_to(REPO_ROOT)}: {source}")

    assert not invalid, "Non-standard author-created sources:\n" + "\n".join(invalid)
