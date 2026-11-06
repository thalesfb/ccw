"""Documentary clarifications must not change the MMAT judgments."""
from pathlib import Path

from src.analysis.mmat_current_tcc_table import CRITERIA, load_rows, render_table

ROOT = Path(__file__).resolve().parents[2]


def test_historical_mmat_marker_preserves_every_response():
    rows = load_rows()
    table = render_table(rows)
    for row in rows:
        line = next(line for line in table.splitlines()
                    if line.startswith(r"\citeonline{" + row["study_key"] + "}"))
        assert line.split(" & ")[2:] == [
            *[row[key] or "---" for key in CRITERIA[:-1]],
            (row[CRITERIA[-1]] or "---") + " " + "\\\\",
        ]
        assert ("(*)" in line) == (row["study_key"] == "Multimodels2020_002")
    assert "julgamentos históricos e preliminares, não reconferidos nesta versão" in table


def test_current_specification_declares_partial_r23_coverage():
    text = (ROOT / "results/tcc/conteudo/aceitacao-cenarios.tex").read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("F05 &"))
    assert "R23 (parcial)" in row
    assert "não estão operacionalizadas nem abrangidas pela aceitação nesta especificação" in row


def test_search_expression_label_keeps_the_configured_counts():
    text = (ROOT / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
    assert "Expressões de busca configuradas & 72 (48 em inglês + 24 em português)" in text
