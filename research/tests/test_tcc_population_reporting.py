"""Guard traceable dates, flow terminology and percentage denominators in the TCC."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_tcc_distinguishes_search_cutoff_from_scope_adjudication() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")

    assert "corte temporal declarado da busca foi 31 de agosto de 2026" in methodology
    assert "definição inicial do escopo do corpus foi concluída em 3 de setembro de 2026" in methodology
    assert "adjudicação inicial do escopo" not in methodology
    assert "não foi preservado um registro histórico completo das requisições" in methodology


def test_tcc_does_not_present_heuristic_prioritization_as_full_report_eligibility() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "não corresponde à avaliação de elegibilidade em texto completo" in methodology
    assert "elaborada com referência ao PRISMA 2020" in results
    assert "a priorização não equivale a essa avaliação" in results


def test_tcc_population_percentages_name_their_denominators() -> None:
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "0,23\\% dos 11.904 registros identificados" in results
    assert "78,89\\% dos mesmos 11.904 registros identificados" in results
    assert "99,28\\% dos 2.486 registros submetidos à priorização por relevância" in results


def test_results_table_reports_the_final_selection_flow_without_mislabeling_17_records() -> None:
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "Registros na lista preliminar & 18" in results
    assert "Excluídos após triagem do resumo & 1" in results
    assert "Relatórios procurados após triagem do resumo & 17" in results
    assert "Relatórios não recuperados & 1" in results
    assert "Relatórios avaliados em texto completo & 16" in results
    assert "Protocolos excluídos após texto completo & 1" in results
    assert "Estudos empíricos no corpus final & 15" in results
    assert "mantidos provisoriamente & 15" not in results
    assert "Candidatos empíricos provisórios & 17" not in results


def test_methodology_dates_final_scope_reconciliation_without_implying_a_new_search() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")

    assert "Em 14 de outubro de 2026, uma conferência atualizada confrontou os 18 registros da lista preliminar" in methodology
    assert "sem nova consulta às bases" in methodology
    assert "sem alterar o corte temporal da busca" in methodology


def test_research_readme_uses_operational_prioritization_and_explicit_denominators() -> None:
    readme = (ROOT / "research/README.md").read_text(encoding="utf-8")
    current = readme.split("**População do snapshot de busca (03/09/2026), com escopo atualizado em 20/10/2026**:", 1)[1].split(
        "**Baseline histórico", 1
    )[0]

    assert "2.486 submetidos à priorização operacional" in current
    assert "20,88% encaminhados à priorização" in current
    assert "99,28% não avançaram nessa etapa" in current
    assert "0,72% formaram a shortlist" in current
    assert "17 relatórios procurados" in current
    assert "15 estudos empíricos mantidos provisoriamente" in current
    assert "Para diagnóstico da execução no SQLite local" in readme
    assert "não devem substituir os números versionados no TCC" in readme
    assert "Para obter os números atualizados" not in readme


def test_tcc_and_presentation_use_the_updated_primary_text_coverage() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
    presentation = (
        ROOT / "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md"
    ).read_text(encoding="utf-8")
    normalized_presentation = " ".join(presentation.split())

    assert "um texto não recuperado" in methodology
    assert "15 estudos empíricos no corpus final" in methodology
    assert "um não foi recuperado" in results
    assert "15 estudos compõem o corpus final" in results
    assert "núcleo empírico" not in results
    assert "um texto integral não foi recuperado" in normalized_presentation
    assert "os outros 15 estudos empíricos integram o núcleo incluído" in normalized_presentation
    assert "nove registros tiveram" not in results.lower()
    assert "nove registros tiveram" not in presentation.lower()


def test_prisma_counts_are_current_in_tcc_presentation_and_appendix() -> None:
    presentation = " ".join(
        (ROOT / "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md")
        .read_text(encoding="utf-8")
        .split()
    )
    appendix = " ".join(
        (ROOT / "results/tcc/postextuais/apendice.tex")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "17 relatórios foram procurados, um não foi recuperado e 16 foram avaliados" in presentation
    assert "17 relatórios foram procurados, 1 não foi recuperado e 16 foram avaliados" in appendix
    assert "quatro não foi recuperado" not in presentation
    assert "4 não recuperados, 13 avaliados" not in appendix
    assert "quatro descrições se limitam" not in appendix


def test_canonical_defense_deck_uses_reconciled_full_text_counts() -> None:
    slides = " ".join((ROOT / "presentation/slides.md").read_text(encoding="utf-8").split())
    parallel_pptx = (ROOT / "scripts/generate_tcc_presentation.py").read_text(encoding="utf-8")

    assert "dos 17 relatórios procurados, um não foi recuperado e 16 foram avaliados em texto completo" in slides.lower()
    assert "para 13, avaliação em texto completo" not in slides
    assert "Dos 17 relatórios procurados, um não foi recuperado e 16 foram avaliados em texto completo" in parallel_pptx


def test_gray_literature_eligibility_has_an_explicit_methodological_rationale() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")

    assert "A inclusão de teses e dissertações" in methodology
    assert "tipo de veículo de publicação" in methodology
    assert "sem flexibilizar os critérios de elegibilidade" in methodology


def test_tcc_and_decks_do_not_call_operational_prioritization_eligibility() -> None:
    results = (ROOT / "results/tcc/conteudo/resultados.tex").read_text(encoding="utf-8")
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
    pptx_source = (ROOT / "scripts/generate_tcc_presentation.py").read_text(encoding="utf-8")
    storyboard = (
        ROOT / "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md"
    ).read_text(encoding="utf-8")

    assert "triagem e a avaliação de elegibilidade, 18 registros" not in results
    assert "priorização por relevância" in results
    assert "priorização operacional" not in results
    assert "não corresponde à avaliação de elegibilidade em texto completo" in methodology
    assert "9 tiveram texto primário revisado e 8 foram" not in slides
    assert "nove registros com texto primário revisado e oito" not in pptx_source
    assert "na elegibilidade; 2.468 excluídos na elegibilidade" not in storyboard
    assert "encaminhou 2.486 para elegibilidade" not in storyboard
    assert "registros → 18 em avaliação de escopo" in slides


def test_background_distinguishes_abstract_only_records_from_verified_full_text_evidence() -> None:
    introduction = (ROOT / "results/tcc/conteudo/introducao.tex").read_text(encoding="utf-8")
    foundations = (ROOT / "results/tcc/conteudo/fundamentacao.tex").read_text(encoding="utf-8")

    assert "excluído na triagem do resumo" in introduction
    assert "somente como contexto bibliográfico" in introduction
    assert "resumo indexado" in introduction
    assert "somente como contexto bibliográfico, não como evidência incluída na síntese" in introduction
    for citation in ("Math2021_001", "Design2025_004", "Machine2024_009"):
        assert f"\\citeonline{{{citation}}}" in foundations
    assert "não constituem, em conjunto, evidência de eficácia de ensino personalizado" in foundations
    assert "não informa amostra, alocação nem análise inferencial suficientes" in foundations
    assert "foram investigadas tarefas de predição de desempenho escolar" not in introduction
