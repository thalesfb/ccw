"""Mechanical editorial rules; these checks do not certify legibility or ABNT."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = json.loads((ROOT / "scripts/tcc_quadros.json").read_text(encoding="utf-8"))


def test_all_fifteen_quadros_call_the_shared_style_once():
    rows = INVENTORY["quadros"]
    assert len(rows) == len({row["label"] for row in rows}) == 15
    for row in rows:
        text = (ROOT / row["source"]).read_text(encoding="utf-8")
        assert text.count(r"\TCCQuadroSetup{" + row["label"] + "}") == 1
        assert text.count(r"\label{" + row["label"] + "}") == 1


def test_body_typography_is_an_editorial_rule_separate_from_captions():
    config = (ROOT / "results/tcc/config_inicial.tex").read_text(encoding="utf-8")
    assert r"\newcommand{\TCCQuadroSetup}[1]" in config
    assert r"\fontsize{10}{12}\selectfont" in config
    assert r"\newcommand{\TCCQuadroCaption}" in config
    assert r"\captionnamefont{\TCCQuadroCaption}" in config
    assert r"\captiontitlefont{\TCCQuadroCaption}" in config
    assert INVENTORY["body_pt"] == 10
    assert INVENTORY["baseline_pt"] == 12
    assert INVENTORY["caption_pt"] == 12
    assert INVENTORY["source_pt"] == 10
    assert INVENTORY["landscape_allowlist"] == []

import importlib.util
from types import SimpleNamespace

import pytest

spec = importlib.util.spec_from_file_location("quadros_gate", ROOT / "scripts/validate_tcc_quadros.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def test_active_inputs_preserve_title_body_source_order():
    gate.validate_sources(ROOT)


def test_source_gate_rejects_a_missing_source_before_the_next_quadro(monkeypatch):
    sources = gate.included_sources(ROOT)
    key = INVENTORY["quadros"][0]["source"]
    sources[key] = sources[key].replace(r"\fonte{Elaborado pelo autor (2026).}", "", 1)
    monkeypatch.setattr(gate, "included_sources", lambda root: sources)
    with pytest.raises(ValueError, match="title/number, body, source"):
        gate.validate_sources(ROOT)


def test_compilation_gate_checks_the_effective_font_and_leading():
    log = "\n".join(f"TCCQUADRO|{row['label']}|size=10|baseline=12.0pt"
                    for row in INVENTORY["quadros"])
    gate.validate_style_log(log, INVENTORY)
    for wrong in (log.replace("size=10", "size=11", 1),
                  log.replace("baseline=12.0", "baseline=18.0", 1),
                  "\n".join(log.splitlines()[:-1])):
        with pytest.raises(ValueError):
            gate.validate_style_log(wrong, INVENTORY)


class RenderedPage:
    mediabox = SimpleNamespace(width=595.276, height=841.89)

    def __init__(self, fault=None):
        self.fault = fault

    def get(self, key, default):
        return 90 if self.fault == "landscape" else default

    def extract_text(self, visitor_text):
        matrix = [1, 0, 0, 1, 0, 0]
        for number in range(1, 16):
            runs = [(f"Quadro {number} – Título", 12), ("Dado", 10), ("Fonte: autor", 10)]
            if number == 7:
                if self.fault == "source_content":
                    runs[-1:] = [("Fonte:", 10), ("autor", 8)]
                if self.fault == "header":
                    runs.insert(1, ("Cabeçalho", 12))
                if self.fault == "continuation_header":
                    runs[2:2] = [("Quadro 7 – Continuação", 12), ("Cabeçalho", 12)]
                if self.fault == "split_continuation":
                    runs[2:2] = [("Quadro 7 – ", 12), ("Continuação", 12), ("Dado", 10)]
                if self.fault in {"caption", "body", "source"}:
                    index = {"caption": 0, "body": 1, "source": 2}[self.fault]
                    runs[index] = (runs[index][0], 11)
                if self.fault == "missing_source":
                    runs.pop()
                if self.fault == "source_first":
                    runs = [runs[0], runs[2], runs[1]]
            for text, size in runs:
                tm = [.8, 0, 0, .8, 0, 0] if self.fault == "text_scale" else matrix
                visitor_text(text, matrix, tm, {}, size * gate.PT_TO_PDF)


def test_pdf_gate_reads_actual_caption_body_and_source_font_runs():
    result = gate.inspect_pdf(SimpleNamespace(pages=[RenderedPage()]), 0, INVENTORY,
                              {i: f"Quadro {i} – Título" for i in range(1, 16)})
    assert len(result) == 15
    assert all(row["body_runs"] == 1 and row["source_seen"] for row in result)


def test_continued_caption_can_arrive_as_separate_pdf_fragments():
    result = gate.inspect_pdf(SimpleNamespace(pages=[RenderedPage("split_continuation")]),
                              0, INVENTORY, {i: f"Quadro {i} – Título" for i in range(1, 16)})
    assert result[6]["body_runs"] == 2


@pytest.mark.parametrize("fault", ["caption", "body", "source", "landscape",
                                  "missing_source", "source_first", "source_content",
                                  "header", "continuation_header", "text_scale"])
def test_pdf_gate_rejects_bad_typography_order_and_unapproved_rotation(fault):
    with pytest.raises(ValueError):
        gate.inspect_pdf(SimpleNamespace(pages=[RenderedPage(fault)]), 0, INVENTORY,
                         {i: f"Quadro {i} – Título" for i in range(1, 16)})


def test_bbox_gate_handles_poppler_controls_without_hiding_overflow(tmp_path):
    path = tmp_path / "bounds.xml"
    xml = '<html xmlns="http://www.w3.org/1999/xhtml"><body><page width="595.276" height="841.89">' \
          '<word xMin="85" xMax="538" yMin="100" yMax="112">Dado\x07</word></page></body></html>'
    path.write_text(xml, encoding="utf-8")
    gate.validate_bbox(path, {1})
    path.write_text(xml.replace('xMax="538"', 'xMax="600"'), encoding="utf-8")
    with pytest.raises(ValueError, match="margins"):
        gate.validate_bbox(path, {1})


def test_text_transform_check_accepts_translation_but_rejects_scaling_and_skew():
    assert gate.unscaled([1, 0, 0, 1, 80, 300], [1, 0, 0, 1, 40, 10])
    assert not gate.unscaled([1, .2, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0])
    assert not gate.unscaled([1, 0, 0, 1, 0, 0], [.8, 0, 0, .8, 0, 0])


def test_component_appendix_preserves_every_response_rationale_and_locator():
    from src.analysis.mmat_current_tcc_table import (
        COMPONENT_CRITERIA, _latex_escape, load_component_rows, render_component_details,
    )
    rows = load_component_rows()
    details = render_component_details(rows)
    assert len(rows) == 6 and len({row["study_key"] for row in rows}) == 3
    for row in rows:
        assert _latex_escape(row["source_locator"]) in details
        for index, criterion in enumerate(COMPONENT_CRITERIA, 1):
            assert f".{index} ({row[criterion]}):" in details
            assert _latex_escape(row[f"evidence_{criterion}"]) in details
    assert (ROOT / "research/exports/references/mmat_component_details_tcc.tex").read_text(
        encoding="utf-8") == details


