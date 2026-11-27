"""The defense script must match the presenter notes of the canonical deck."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLIDES = ROOT / "presentation/slides.md"
SCRIPT = ROOT / "results/tcc/presentation/ROTEIRO_FALAS_TCC.md"


def _notes():
    text = SLIDES.read_text(encoding="utf-8").replace("\r\n", "\n")
    return re.findall(r"<!--\n\[(\d+:\d{2})\] MOSTRAR: (.+?)\n\nFALA: (.+?)\n-->", text, re.S)


def test_every_slide_has_presenter_notes():
    text = SLIDES.read_text(encoding="utf-8").replace("\r\n", "\n")
    slide_count = len(re.findall(r"^---$", text, re.M)) // 2
    assert slide_count == 24
    assert len(_notes()) == slide_count


def test_script_repeats_each_presenter_note():
    script = SCRIPT.read_text(encoding="utf-8")
    for time, show, speech in _notes():
        assert f"— {time}" in script
        assert f"**Mostrar:** {show}" in script
        assert f"**Fala:** {speech}" in script


def test_script_follows_current_selection_wording():
    script = SCRIPT.read_text(encoding="utf-8")
    slides = SLIDES.read_text(encoding="utf-8")
    for text in (script, slides):
        assert "seleção histórica" not in text
        assert "pp. 42" not in text
    assert "Figuras 4 e 5 do TCC" in slides
