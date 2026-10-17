"""Test the artifact parser with representative nested memoir captions."""
import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location("pdf_gate", Path(__file__).resolve().parents[2] / "scripts/validate_tcc_pdf.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def test_list_parser_handles_nested_titles_and_ignores_font_directives():
    data = (r"\contentsline {quadro}{\numberline {1}{\ignorespaces Camadas.}}{24}{quadro.35}%" "\n"
            r"\contentsline {section}{\numberline {2.4}\textit{ML}}{20}{section.4}%" "\n"
            r"\addvspace {10pt}")
    assert gate.list_entries(data) == [("24", "quadro.35"), ("20", "section.4")]


def test_normalization_handles_pdf_line_breaks_case_and_accents():
    assert gate.normalize("CONTRIBUIÇÕES\nPEDAGÓGICAS") == gate.normalize("Contribuições Pedagógicas")


def test_quadro_count_includes_traceability_and_mixed_methods_appraisal(tmp_path):
    entries = [
        rf"\contentsline {{quadro}}{{\numberline {{{index}}}{{Quadro {index}.}}}}{{{index}}}{{quadro.{index}}}"
        for index in range(1, 8)
    ]
    (tmp_path / "main.loq").write_text("\n".join(entries), encoding="utf-8")

    assert gate.validate_quadro_count(tmp_path) == 7
