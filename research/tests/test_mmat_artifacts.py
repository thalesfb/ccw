"""Reproducibility checks for committed MMAT exports."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analysis.mmat_assessment import export_latex_table
from src.analysis.mmat_tcc_table import load_rows, render_table


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
DATA = RESEARCH_ROOT / "data" / "mmat_assessments.csv"
CSV_EXPORT = RESEARCH_ROOT / "exports" / "analysis" / "mmat_assessment.csv"
GENERIC_LATEX = RESEARCH_ROOT / "exports" / "references" / "mmat_table.tex"
TCC_LATEX = RESEARCH_ROOT / "exports" / "references" / "mmat_tcc_table.tex"


def test_committed_csv_matches_canonical_data() -> None:
    assert DATA.read_bytes() == CSV_EXPORT.read_bytes()


def test_generic_latex_export_is_current(tmp_path: Path) -> None:
    frame = pd.read_csv(DATA, encoding="utf-8-sig")
    generated = tmp_path / "mmat_table.tex"
    export_latex_table(frame, generated)
    assert generated.read_text(encoding="utf-8") == GENERIC_LATEX.read_text(
        encoding="utf-8"
    )


def test_tcc_latex_export_is_current() -> None:
    assert TCC_LATEX.read_text(encoding="utf-8") == render_table(load_rows())
