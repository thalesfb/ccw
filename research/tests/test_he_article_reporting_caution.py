from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_he_classroom_analysis_reports_cluster_level_uncertainty_cautiously():
    chapter = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(
        encoding="utf-8"
    )
    section_start = chapter.index(r"\section{Limitações e Contribuições da Revisão}")
    evidence_section = chapter[section_start:]
    he_start = evidence_section.index(
        r"Em \citeonline[p.~1, 16, 31--35]{He2025_6915}"
    )
    he_end = evidence_section.index("\n\n", he_start)
    he_section = evidence_section[he_start:he_end].lower()

    assert "oito turmas com 45 estudantes cada" in he_section
    assert "amostra total de 90" in he_section
    assert "agrupamento" in he_section
    assert "não se pode reconstruir se a análise tratou estudantes ou turmas como observações" in he_section
    assert "nem a precisão das comparações" in he_section
    assert "As divergências não foram corrigidas por inferência" in evidence_section
    assert "nem atribuídas automaticamente à execução dos procedimentos" in evidence_section
