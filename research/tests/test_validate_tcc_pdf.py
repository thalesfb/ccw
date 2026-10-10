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
