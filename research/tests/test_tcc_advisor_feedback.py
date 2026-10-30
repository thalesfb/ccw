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
    methodology = _read(TCC_CONTENT / "metodologia.tex")
    assert r"Um \textit{cache} local armazenou respostas obtidas anteriormente" in methodology
    assert "Um acerto ocorre quando uma solicitação é atendida com uma resposta armazenada, sem nova consulta à API" in methodology


def test_prisma_reporting_and_protocol_are_not_conflated() -> None:
    methodology = _read(TCC_CONTENT / "metodologia.tex")
    lowered = methodology.lower()
    assert "prisma 2020" in lowered
    assert "diretriz de relato" in lowered
    assert "prisma-p 2015" in lowered
    assert "orienta o planejamento e o relato de protocolos" in lowered
    assert "seus princípios foram utilizados parcialmente" in lowered
    assert "não houve registro prospectivo" in lowered
    for unsupported in (
        "seguiu integralmente",
        "seguiu rigorosamente",
        "aderência integral ao prisma-p",
        "foi integralmente aderente ao prisma-p",
    ):
        assert unsupported not in lowered


def test_current_deduplication_description_matches_identity_audit() -> None:
    methodology = _read(TCC_CONTENT / "metodologia.tex")
    assert (
        "mesmo \\textit{Digital Object Identifier} (DOI, identificador de objeto digital), "
        "após padronização, ou o mesmo \\textit{Uniform Resource Locator} "
        "(URL, localizador uniforme de recursos)"
    ) in methodology
    assert "removeram 27 duplicatas: 25 por DOI e 2 por URL" in methodology
    assert "232 registros com título repetido" in methodology
    assert "restantes foram indicados para conferência manual" in methodology
    review = _read(TCC_CONTENT / "resultadosesperados.tex")
    assert "não tratados como duplicatas confirmadas" in review
    assert "determinística" not in methodology


def test_query_count_is_reported_as_canonical_strategy_not_http_execution() -> None:
    methodology = _read(TCC_CONTENT / "metodologia.tex")
    assert "A estratégia canônica reuniu 72 consultas: 48 em inglês e 24 em português" in methodology
    assert "ausência de histórico completo das requisições impede determinar quantas foram concluídas" in methodology
    assert "Foram executadas 72 consultas" not in methodology
    assert "resultaram em 11.904 registros identificados" not in methodology


def test_interpretation_precedes_the_long_synthesis_quadro() -> None:
    chapter = _read(TCC_CONTENT / "resultadosesperados.tex")
    interpretation = chapter.index("O Quadro~\\ref{qua:sintese-estudos-empiricos}")
    quadro = chapter.index(r"\label{qua:sintese-estudos-empiricos}")
    assert interpretation < quadro
    assert "As diferenças entre populações, instrumentos, variáveis e desenhos impedem tratar os resultados como medidas de um mesmo fenômeno" in chapter[interpretation:quadro]


def test_unbreakable_python_identifiers_do_not_leak_into_prose() -> None:
    source = _all_tex()
    assert r"\texttt{RandomForestClassifier}" not in source
    assert r"\path{RandomForestClassifier}" not in source
    assert r"\nolinkurl{RandomForestClassifier}" not in source


def test_repository_paths_are_breakable_in_tcc_prose() -> None:
    source = _all_tex()
    for path in (
        "research/data/current_eligibility_protocol.csv",
        "research/exports/reports/reproducibility_manifest.json",
        "research/data/mmat_reassessment_current.csv",
    ):
        assert rf"\path{{{path}}}" in source


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

    assert "O escopo compreendeu a revisão, a apreciação metodológica preliminar dos estudos empíricos incluídos e a elaboração de uma especificação conceitual de protótipo" in _read(TCC_CONTENT / "metodologia.tex")
    assert "A delimitação dos procedimentos executados" in introduction
    assert "especificação conceitual do protótipo" in prototype
    limitations = _read(TCC_CONTENT / "resultadosesperados.tex").split(
        r"\section{Limitações e Contribuições da Revisão}", 1
    )[1]
    assert "A especificação permaneceu documental" in limitations
    assert "Não incluiu uma aplicação educacional funcional" in limitations
    assert "O componente propositivo do objetivo geral foi realizado no escopo documental" in results
    assert "resposta à pergunta ``como estruturar''" in conclusion
    assert "Este trabalho propôs uma especificação técnica e pedagógica" in abstract
    assert "protocolo docente ainda não aplicado" in abstract


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
    assert "responsabilidade do professor pela interpretação" in foundation.lower()
    assert "não observa diretamente todos os processos" in foundation.lower()
    assert r"\cite{Romero2020}" in _read(TCC_CONTENT / "introducao.tex")
    assert r"\cite{NRC2001}" in foundation
    assert r"\cite{LGPD2018}" in foundation
    assert "não foram estimados neste trabalho" in foundation
    assert "não como efeito demonstrado pelos estudos reunidos" in foundation


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
    study8_row = next(
        (
            line
            for line in chapter.splitlines()
            if r"\citeonline{Computational2017_008}" in line and " & " in line
        ),
        "",
    )
    assert "Incluído como uma tese/um relatório de modelagem computacional" in study8_row
    assert "Frações reutilizadas entre capítulos não são contadas duas vezes" in study8_row
    assert "adjudicação" not in study8_row
    assert r"O Quadro~\ref{qua:sintese-estudos-empiricos}" in chapter
    assert "Não há medida harmonizada de efeito" in chapter
    assert "Resultado reportado" not in chapter
    mmat_section = chapter[chapter.index("Avaliação Metodológica com o MMAT") :]
    assert not re.search(r"\b[0-5]\s*/\s*5\b", mmat_section)
    assert "sem média, ranking ou categoria geral" in mmat_section
    assert r"\input{../../research/exports/references/mmat_current_tcc_table.tex}" in chapter
    assert "Tjahyadi (2025) & Quant." not in chapter

    methodology = _read(TCC_CONTENT / "metodologia.tex")
    normalized_methodology = " ".join(methodology.split())
    assert "Institute of Medicine" not in methodology
    assert "referências do" not in methodology
    storyboard = _read(TCC_ROOT / "presentation" / "APRESENTACAO_TCC_SLIDES_CONTEUDO.md")
    slides = _read(REPO_ROOT / "presentation" / "slides.md")
    for text in (methodology, storyboard, slides):
        assert "Nove textos estão arquivados" not in text
        assert "nove fontes" not in text
    assert r"\citeonline{Zeng2025_6923}" in chapter
    assert "A categoria 3 foi utilizada para examinar as comparações quantitativas" in chapter
    assert "com alocação desconhecida" in chapter
    assert "a execução da randomização recebeu ct" in chapter.lower()
    assert "Um único revisor conduziu seleção e apreciação, com apoio de IA generativa em ambas" in chapter
    assert "ainda dependem de conferência humana por fonte e critério" in chapter
    assert "não foram convertidos em escore agregado ou síntese final de qualidade" in chapter
    for removed in ("adjudicação",):
        assert removed not in methodology
    assert "um único revisor, o autor" in methodology
    assert "Não há segunda avaliação independente documentada" in methodology
    assert "IA generativa na seleção e no preenchimento do MMAT" in methodology
    appendix = _read(TCC_ROOT / "postextuais" / "apendice.tex")
    selection_row = next(line for line in appendix.splitlines() if line.startswith("8 & Seleção &"))
    appraisal_row = next(line for line in appendix.splitlines() if line.startswith("11 & Viés nos estudos &"))
    assert r"Cap.~\ref{cap:metodologia}, Processo de Seleção" in selection_row
    assert r"Cap.~\ref{cap:revisao}, Limitações e Contribuições da Revisão" in selection_row
    assert "seleção como único revisor" in selection_row
    assert "regras automatizadas e apoio de IA generativa" in selection_row
    assert "não há segunda seleção independente documentada" in selection_row
    assert r"Cap.~\ref{cap:metodologia}, Avaliação da Qualidade Metodológica" in appraisal_row
    assert "apreciação como único revisor, com apoio de IA generativa" in appraisal_row
    assert "conferência humana por fonte e critério permanece pendente" in appraisal_row
    assert "a verificação documental permanece incompleta" not in selection_row
    assert "com fontes e julgamentos ainda incompletos" not in appraisal_row
    assert "Os critérios Q1--Q5 dependem da categoria" in normalized_methodology
    assert "em estudos quantitativos descritivos, q1 examina a estratégia de amostragem" in normalized_methodology.lower()
    assert "nos não randomizados, examina a representatividade dos participantes" in normalized_methodology.lower()
    assert "foram apreciados separadamente, sem contar estudos adicionais" in chapter
    mmat_table = MMAT_LATEX.read_text(encoding="utf-8")
    assert "Q1--Q5 = critérios da categoria" in mmat_table
    for key in ("Villegas2025_6916", "UniversityMathematics2026_6919", "Echeveria2025_6920"):
        assert rf"\citeonline{{{key}}} & Métodos mistos &" in mmat_table


def test_author_created_sources_use_the_standard_year_form() -> None:
    invalid: list[str] = []
    pattern = re.compile(r"\\fonte\{(Elaborado pelo autor.*)\}$", re.MULTILINE)
    expected = re.compile(r"Elaborado pelo autor \((?:19|20)\d{2}\)(?:\.|, com base em \\citeonline\{PRISMA2020\}\..*)")

    for path in sorted(TCC_ROOT.rglob("*.tex")):
        for source in pattern.findall(_read(path)):
            if not expected.fullmatch(source):
                invalid.append(f"{path.relative_to(REPO_ROOT)}: {source}")

    assert not invalid, "Non-standard author-created sources:\n" + "\n".join(invalid)
