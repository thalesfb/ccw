"""Mechanical editorial rules; these checks do not certify legibility or ABNT."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = json.loads((ROOT / "scripts/tcc_quadros.json").read_text(encoding="utf-8"))


def test_all_fourteen_quadros_call_the_shared_style_once():
    rows = INVENTORY["quadros"]
    assert len(rows) == len({row["label"] for row in rows}) == 14
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
        for number in range(1, 15):
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


def rendered_sources():
    return {i: "Fonte: autor" for i in range(1, 15)}


def test_pdf_gate_reads_actual_caption_body_and_source_font_runs():
    result = gate.inspect_pdf(SimpleNamespace(pages=[RenderedPage()]), 0, INVENTORY,
                              {i: f"Quadro {i} – Título" for i in range(1, 15)},
                              rendered_sources())
    assert len(result) == 14
    assert all(row["body_runs"] == 1 and row["source_seen"] for row in result)


def test_continued_caption_can_arrive_as_separate_pdf_fragments():
    result = gate.inspect_pdf(SimpleNamespace(pages=[RenderedPage("split_continuation")]),
                              0, INVENTORY, {i: f"Quadro {i} – Título" for i in range(1, 15)},
                              rendered_sources())
    assert result[6]["body_runs"] == 2


@pytest.mark.parametrize("fault", ["caption", "body", "source", "landscape",
                                  "missing_source", "source_first", "source_content",
                                  "header", "continuation_header", "text_scale"])
def test_pdf_gate_rejects_bad_typography_order_and_unapproved_rotation(fault):
    with pytest.raises(ValueError):
        gate.inspect_pdf(SimpleNamespace(pages=[RenderedPage(fault)]), 0, INVENTORY,
                         {i: f"Quadro {i} – Título" for i in range(1, 15)},
                         rendered_sources())


class FragmentPage(RenderedPage):
    def __init__(self, runs):
        super().__init__()
        self.runs = runs

    def extract_text(self, visitor_text):
        for text, size, y in self.runs:
            visitor_text(text, [1, 0, 0, 1, 0, 0], [1, 0, 0, 1, 85, y], {},
                         size * gate.PT_TO_PDF)


def inspect_source_fragments(tail, expected="Fonte: autor. Nota: texto final.", same_page=False):
    sources = rendered_sources()
    sources[14] = expected
    runs = [(text, size, y) for i in range(1, 15)
            for text, size, y in [(f"Quadro {i} – Título", 12, 120),
                                  ("Dado", 10, 100), ("Fonte: autor", 10, 80)]]
    if same_page:
        runs.extend(tail[0])
        tail = tail[1:]
    pages = [FragmentPage(runs), *[FragmentPage(page) for page in tail]]
    return gate.inspect_pdf(SimpleNamespace(pages=pages), 0, INVENTORY,
                            {i: f"Quadro {i} – Título" for i in range(1, 15)}, sources)


@pytest.mark.parametrize("size", [8, 12])
@pytest.mark.parametrize("kind", ["source", "notes"])
def test_pdf_source_continuation_rejects_wrong_size_across_pages(size, kind):
    expected, fragment = (("Fonte: autor texto final.", "texto final.") if kind == "source"
                          else ("Fonte: autor. Nota: texto final.", ". Nota: texto final."))
    with pytest.raises(ValueError, match="source/notes.*typography"):
        inspect_source_fragments([[(fragment, size, 740)]], expected)


def test_pdf_source_rejects_12pt_content_after_30pt_gap():
    with pytest.raises(ValueError, match="source/notes.*typography"):
        inspect_source_fragments([[('. Nota: texto final.', 12, 50)]], same_page=True)


@pytest.mark.parametrize("prose_y", [740, 710])
def test_pdf_accepts_complete_crosspage_notes_then_normal_prose(prose_y):
    rows = inspect_source_fragments([
        [('90', 12, 800), ('. Nota:', 10, 770)],
        [('texto ', 10, 770), ('final.', 10, 750),
         ('Prosa normal depois da nota.', 12, prose_y)],
    ])
    assert rows[-1]["source_seen"]
    assert rows[-1]["pages"] == [1, 2, 3]


def test_pdf_accepts_following_prose_without_waiting_for_a_large_gap():
    rows = inspect_source_fragments([[('Prosa normal.', 12, 70)]], "Fonte: autor", same_page=True)
    assert rows[-1]["source_seen"]


def test_pdf_accepts_crosspage_source_then_prose_after_30pt_gap():
    rows = inspect_source_fragments([
        [('texto final.', 10, 740), ('Prosa normal.', 12, 710)],
    ], "Fonte: autor texto final.")
    assert rows[-1]["source_seen"] and rows[-1]["pages"] == [1, 2]


def test_pdf_rejects_missing_expected_note_at_end_or_before_another_quadro():
    for tail in ([], [[('Quadro 1 – Título', 12, 740)]]):
        with pytest.raises(ValueError, match="source/notes"):
            inspect_source_fragments(tail)


@pytest.mark.parametrize("override", [
    r"\setstretch{1.5}", r"\begin{spacing}{1.5}",
    r"\baselineskip=18pt", r"\setlength{\baselineskip}{18pt}",
    r"\addtolength{\baselineskip}{6pt}", r"\renewcommand{\baselinestretch}{1.5}",
    r"\linespread{1.5}", r"\OnehalfSpacing", r"\DoubleSpacing",
    r"\onehalfspacing", r"\doublespacing", r"\begin{DoubleSpace}",
])
@pytest.mark.parametrize("location", ["body", "source", "note"])
def test_source_gate_rejects_local_leading_overrides(monkeypatch, override, location):
    override += " "
    sources = gate.included_sources(ROOT)
    row = INVENTORY["quadros"][5]
    text = sources[row["source"]]
    if location == "body":
        marker = r"\TCCQuadroSetup{" + row["label"] + "}"
        text = text.replace(marker, marker + override, 1)
    elif location == "source":
        text = text.replace(r"\fonte{", r"\fonte{" + override, 1)
    else:
        text = text.replace(r"\textit{Nota:}", r"\textit{Nota:}" + override, 1)
    sources[row["source"]] = text
    monkeypatch.setattr(gate, "included_sources", lambda root: sources)
    with pytest.raises(ValueError, match="Local .*overrides the shared style"):
        gate.validate_sources(ROOT)


def test_source_gate_allows_grid_spacing_comments_and_following_prose(monkeypatch):
    sources = gate.included_sources(ROOT)
    row = INVENTORY["quadros"][0]
    key = row["source"]
    marker = r"\TCCQuadroSetup{" + row["label"] + "}"
    sources[key] = sources[key].replace(marker, marker + r"\renewcommand{\arraystretch}{1.3}", 1)
    sources[key] = sources[key].replace(r"\end{quadro}",
                                      "\\end{quadro}\n\\setstretch{1.5}\nProsa normal.", 1)
    monkeypatch.setattr(gate, "included_sources", lambda root: sources)
    gate.validate_sources(ROOT)


def test_expected_source_text_handles_nested_groups_notes_and_aux_references(tmp_path, monkeypatch):
    sources = gate.included_sources(ROOT)
    row = INVENTORY["quadros"][0]
    sources[row["source"]] = sources[row["source"]].replace(
        r"\fonte{Elaborado pelo autor (2026).}",
        r"\fonte{Elaborado pelo \textbf{autor}, com \citeonline{PRISMA2020}.}"
        "\n" + r"\par\noindent\textit{Nota:} Ver Seção~\ref{sec:teste}.\par", 1)
    monkeypatch.setattr(gate, "included_sources", lambda root: sources)
    (tmp_path / "main.aux").write_text(
        r"\bibciteEXPL{PRISMA2020}{Page et al.}" + "\n" +
        r"\bibciteYEAR{PRISMA2020}{2021}" + "\n" +
        r"\newlabel{sec:teste}{{3.6}{27}{Título}{section.33}{}}", encoding="utf-8")
    result = gate.source_texts(ROOT, {"quadros": [row]}, tmp_path)
    assert gate.compact(result[1]) == gate.compact(
        "Fonte: Elaborado pelo autor, com Page et al. (2021). Nota: Ver Seção 3.6.")


def test_expected_source_text_does_not_silently_drop_unknown_macros(tmp_path, monkeypatch):
    sources = gate.included_sources(ROOT)
    row = INVENTORY["quadros"][0]
    sources[row["source"]] = sources[row["source"]].replace(
        r"\fonte{Elaborado pelo autor (2026).}", r"\fonte{\unknownsource{autor}}", 1)
    monkeypatch.setattr(gate, "included_sources", lambda root: sources)
    with pytest.raises(ValueError, match="Unsupported.*source/notes"):
        gate.source_texts(ROOT, {"quadros": [row]}, tmp_path)


def test_expected_source_text_stops_before_next_group_or_saved_table(tmp_path):
    result = gate.source_texts(ROOT, {"quadros": INVENTORY["quadros"][3:5]}, tmp_path)
    assert all(gate.compact(text) == gate.compact("Fonte: Elaborado pelo autor (2026).")
               for text in result.values())


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
    assert details.endswith("\n") and not details.endswith("\n\n")
    assert len(rows) == 6 and len({row["study_key"] for row in rows}) == 3
    for row in rows:
        assert _latex_escape(row["source_locator"]) in details
        for index, criterion in enumerate(COMPONENT_CRITERIA, 1):
            assert f".{index} ({row[criterion]}):" in details
            assert _latex_escape(row[f"evidence_{criterion}"]) in details
    assert (ROOT / "research/exports/references/mmat_component_details_tcc.tex").read_text(
        encoding="utf-8") == details
