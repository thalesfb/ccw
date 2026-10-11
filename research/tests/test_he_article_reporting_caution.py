from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_he_classroom_analysis_reports_cluster_level_uncertainty_cautiously():
    chapter = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(
        encoding="utf-8"
    )
    section_start = chapter.index(r"\section{Tendências e Lacunas}")
    section_end = chapter.index(
        r"\section{Limitações e Contribuições da Revisão}", section_start
    )
    evidence_section = chapter[section_start:section_end]
    he_start = evidence_section.index(
        r"Em \citeonline[pp.~1, 16, 31--35]{He2025_6915}"
    )
    he_end = evidence_section.index("\n\n", he_start)
    he_section = evidence_section[he_start:he_end].lower()

    assert "45 estudantes por turma" in he_section
    assert "amostra total de 90" in he_section
    assert "agrupamento" in he_section
    assert "não é possível, portanto, reconstruir a unidade analítica" in he_section
    assert "sem autorizar corrigir o denominador por inferência" in he_section
    assert "declarar os resultados inválidos" in he_section
