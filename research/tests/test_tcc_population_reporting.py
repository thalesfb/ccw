"""Guard traceable dates, flow terminology and percentage denominators in the TCC."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_tcc_distinguishes_search_cutoff_from_scope_adjudication() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")

    assert "corte temporal declarado da busca foi 31 de agosto de 2026" in methodology
    assert "adjudicação de escopo da população foi concluída em 3 de setembro de 2026" in methodology
    assert "não foram preservados logs por consulta e por API" in methodology


def test_tcc_does_not_present_heuristic_prioritization_as_full_report_eligibility() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "não corresponde à avaliação de elegibilidade de relatórios" in methodology
    assert "não reproduz todas as etapas do diagrama padrão do PRISMA 2020" in results
    assert "priorização operacional" in results


def test_tcc_population_percentages_name_their_denominators() -> None:
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")

    assert "0,23\\% dos 11.904 registros identificados" in results
    assert "78,89\\% dos mesmos 11.904 registros identificados" in results
    assert "99,28\\% dos 2.486 registros submetidos à priorização operacional" in results


def test_tcc_and_presentation_use_the_updated_primary_text_coverage() -> None:
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    results = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
    presentation = (
        ROOT / "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md"
    ).read_text(encoding="utf-8")

    assert "Doze registros empíricos tiveram o texto primário consultado externamente, cinco" in methodology
    assert "doze registros tiveram o texto primário consultado e cinco foram" in results
    assert "doze registros tiveram texto primário consultado e cinco foram" in presentation
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
