"""Guard traceable dates, flow terminology and percentage denominators in the TCC."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_tcc_distinguishes_search_cutoff_from_scope_adjudication() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")

    assert "corte temporal declarado da busca foi 31 de agosto de 2026" in methodology
    assert "adjudicação inicial do escopo da população foi concluída em 3 de setembro de 2026" in methodology
    assert "não foram preservados logs por consulta e por API" in methodology


def test_tcc_does_not_present_heuristic_prioritization_as_full_report_eligibility() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "não corresponde à avaliação de elegibilidade de relatórios" in methodology
    assert "elaborada com referência ao PRISMA 2020" in results
    assert "a priorização não equivale a essa avaliação" in results


def test_tcc_population_percentages_name_their_denominators() -> None:
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "0,23\\% dos 11.904 registros identificados" in results
    assert "78,89\\% dos mesmos 11.904 registros identificados" in results
    assert "99,28\\% dos 2.486 registros submetidos à priorização operacional" in results


def test_results_table_reports_the_final_selection_flow_without_mislabeling_17_records() -> None:
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "Registros na shortlist operacional & 18" in results
    assert "Excluídos após triagem do resumo & 1" in results
    assert "Relatórios procurados após triagem do resumo & 17" in results
    assert "Relatórios não recuperados & 4" in results
    assert "Relatórios avaliados em texto completo & 13" in results
    assert "Protocolos excluídos após texto completo & 1" in results
    assert "Estudos empíricos incluídos & 12" in results
    assert "Candidatos empíricos provisórios & 17" not in results


def test_methodology_dates_final_scope_reconciliation_without_implying_a_new_search() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")

    assert "Em 12 de outubro de 2026, uma reconciliação final confrontou os 18 registros shortlistados" in methodology
    assert "sem nova consulta às bases" in methodology
    assert "sem alterar o corte temporal da busca" in methodology


def test_research_readme_uses_operational_prioritization_and_explicit_denominators() -> None:
    readme = (ROOT / "research/README.md").read_text(encoding="utf-8")
    current = readme.split("**População do snapshot de busca (03/09/2026), com escopo atualizado em 12/10/2026**:", 1)[1].split(
        "**Baseline histórico", 1
    )[0]

    assert "2.486 submetidos à priorização operacional" in current
    assert "20,88% encaminhados à priorização" in current
    assert "99,28% não avançaram nessa etapa" in current
    assert "0,72% formaram a shortlist" in current
    assert "17 relatórios procurados" in current
    assert "12 estudos empíricos incluídos" in current
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

    assert "quatro textos integrais não foram recuperados" in methodology
    assert "12 estudos empíricos foram incluídos" in methodology
    assert "quatro não foram recuperados" in results
    assert "12 estudos compõem o núcleo empírico incluído" in results
    assert "quatro textos integrais não foram recuperados" in normalized_presentation
    assert "os outros 12 estudos empíricos integram o núcleo incluído" in normalized_presentation
    assert "nove registros tiveram" not in results.lower()
    assert "nove registros tiveram" not in presentation.lower()


def test_tcc_and_decks_do_not_call_operational_prioritization_eligibility() -> None:
    results = (ROOT / "results/tcc/conteudo/resultados.tex").read_text(encoding="utf-8")
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
    pptx_source = (ROOT / "scripts/generate_tcc_presentation.py").read_text(encoding="utf-8")
    storyboard = (
        ROOT / "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md"
    ).read_text(encoding="utf-8")
    speaker_notes = (ROOT / "results/tcc/presentation/ROTEIRO_FALAS_TCC.md").read_text(encoding="utf-8")

    assert "triagem e a avaliação de elegibilidade, 18 registros" not in results
    assert "priorização operacional" in results
    assert "não equivale à avaliação de elegibilidade de relatórios" in methodology
    assert "9 tiveram texto primário revisado e 8 foram" not in slides
    assert "nove registros com texto primário revisado e oito" not in pptx_source
    assert "na elegibilidade; 2.468 excluídos na elegibilidade" not in storyboard
    assert "encaminhou 2.486 para elegibilidade" not in speaker_notes
