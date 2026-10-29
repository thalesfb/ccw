from pathlib import Path


def _read(repository_root: Path, relative_path: str) -> str:
    return (repository_root / relative_path).read_text(encoding="utf-8")


def test_tcc_publishes_separate_lists_for_figures_quadros_and_tables() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    main = _read(repository_root, "results/tcc/main.tex")

    assert "\\listoffigures*" in main
    assert "\\listofquadros*" in main
    assert "\\listoftables*" in main
    assert "% \\listofquadros*" not in main
    assert "% \\listoftables*" not in main


def test_review_section_uses_semantic_float_types_and_labels() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    review = _read(repository_root, "results/tcc/conteudo/resultadosesperados.tex")

    assert review.count("\\begin{figure}") == 0
    assert review.count("\\begin{fluxograma}") == 1
    assert review.count("\\begin{grafico}") == 1
    assert review.count("\\begin{table}") == 1
    assert "\\label{qua:sintese-estudos-empiricos}" in review
    assert "Tabela~\\ref{tab:sintese-estudos-empiricos}" not in review
    assert "Tabela~\\ref{tab:mmat-reavaliacao-atual}" not in review
    assert "\\quadroname\\ \\thequadro" in review


def test_generated_mmat_export_is_a_quadro_and_is_self_describing() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    export = _read(
        repository_root,
        "research/exports/references/mmat_current_tcc_table.tex",
    )

    assert "\\def\\LTcaptype{quadro}" in export
    assert "\\label{qua:mmat-reavaliacao-atual}" in export
    assert "\\quadroname\\ \\thequadro" in export
    assert "\\label{tab:mmat-reavaliacao-atual}" not in export
    assert "S1/S2 = perguntas de triagem" in export
    assert "Q1--Q5 = critérios da categoria" in export
    assert "\\ref{sec:avaliacao-qualidade}" in export
    assert "Quant. = quantitativo" in export
    assert r"\textbf{Base}" not in export
    assert r"\clearpage" not in export
    assert r"\par\noindent\textit{Nota:}" in export

    component_caption = r"\caption{Componentes qualitativos e quantitativos dos estudos de métodos mistos.}"
    component_caption_index = export.index(component_caption)
    previous_table_end = export.rfind(r"\end{longtable}", 0, component_caption_index)
    component_table_start = export.rfind(r"\begin{longtable}", 0, component_caption_index)
    assert previous_table_end < component_table_start < component_caption_index
    assert r"\Needspace{18\baselineskip}" not in export


def test_prisma_appendix_classifies_checklist_as_quadro() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    appendix = _read(repository_root, "results/tcc/postextuais/apendice.tex")

    assert "\\def\\LTcaptype{quadro}" in appendix
    assert "\\label{qua:prisma-checklist}" in appendix
    assert "\\quadroname\\ \\thequadro" in appendix
    assert "\\label{tab:prisma-checklist}" not in appendix
