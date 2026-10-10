from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_he_classroom_analysis_reports_cluster_level_uncertainty_cautiously():
    chapter = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(
        encoding="utf-8"
    )
    start = chapter.index(r"\citeonline[pp.~1, 16, 31--35]{He2025_6915}")
    end = chapter.index("Também foram identificados limites de relato e de comparação.")
    he_section = chapter[start:end]

    assert "agrupamento por turma e docente" in he_section
    assert "não autoriza declarar" in he_section
    assert "os resultados inválidos" in he_section
