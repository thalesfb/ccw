"""Generate the historical 17-study MMAT criterion table.

The canonical source is ``research/data/mmat_assessments.csv``. This module
keeps the historical landscape table reproducible and separate from the
current 16-record reassessment in ``mmat_reassessment_current.csv``. It must
not be presented as the current scientific appraisal.
"""

from __future__ import annotations

import argparse
import csv
import difflib
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = REPO_ROOT / "research" / "data" / "mmat_assessments.csv"
OUTPUT_PATH = (
    REPO_ROOT / "research" / "exports" / "references" / "mmat_tcc_table.tex"
)

DESIGN_LABELS = {
    "qualitative": "Qualitativo",
    "quantitative_randomized": "Quant. randomizado",
    "quantitative_nonrandomized": "Quant. não rand.",
    "quantitative_descriptive": "Quant. descritivo",
    "mixed_methods": "Métodos mistos",
}
RESPONSE_LABELS = {"Y": "S", "N": "N", "CT": "ND"}


def load_rows(path: Path = DATA_PATH) -> List[Dict[str, str]]:
    """Load and minimally validate the canonical appraisal rows."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    required = {
        "Authors",
        "Year",
        "Design",
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "Q5",
        "Limitations",
    }
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Missing MMAT columns: {sorted(missing)}")
    if len(rows) != 17:
        raise ValueError(f"Expected 17 historical MMAT rows, found {len(rows)}")

    for row in rows:
        if row["Design"] not in DESIGN_LABELS:
            raise ValueError(f"Unknown design: {row['Design']}")
        for criterion in ("Q1", "Q2", "Q3", "Q4", "Q5"):
            if row[criterion] not in RESPONSE_LABELS:
                raise ValueError(
                    f"Invalid response {row[criterion]!r} for "
                    f"{row.get('ID', '?')}.{criterion}"
                )
    return rows


def _latex_escape(value: object) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in str(value))


def render_table(rows: List[Dict[str, str]]) -> str:
    """Render the landscape longtable consumed by the TCC."""
    lines = [
        "% Tabela MMAT 2018 histórica gerada de research/data/mmat_assessments.csv",
        "% Não representa a avaliação vigente dos 16 registros (15 empíricos e 1 contextual).",
        "% Não editar manualmente; execute: python -m src.analysis.mmat_tcc_table",
        r"\begin{longtable}{|p{2.8cm}|p{2.8cm}|ccccc|p{13.0cm}|}",
        r"\caption{Respostas aos critérios do MMAT 2018.}\label{tab:mmat-avaliacao}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Desenho} & \textbf{Q1} & "
        r"\textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & "
        r"\textbf{Limitações observadas} \\",
        r"\hline",
        r"\endfirsthead",
        r"\multicolumn{8}{c}{\tablename\ \thetable\ -- Continuação}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Desenho} & \textbf{Q1} & "
        r"\textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & "
        r"\textbf{Limitações observadas} \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\multicolumn{8}{r}{\textit{Continua na próxima página}}\\",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]

    for row in rows:
        values = [
            _latex_escape(f"{row['Authors']} ({row['Year']})"),
            _latex_escape(DESIGN_LABELS[row["Design"]]),
            *[
                RESPONSE_LABELS[row[key]]
                for key in ("Q1", "Q2", "Q3", "Q4", "Q5")
            ],
            _latex_escape(row["Limitations"]),
        ]
        lines.append(" & ".join(values) + r" \\")

    lines.extend(
        [
            r"\end{longtable}",
            r"% S = Sim; N = Não; ND = Não é possível determinar.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when the committed TCC table differs from the canonical CSV",
    )
    args = parser.parse_args()

    expected = render_table(load_rows())
    if args.check:
        actual = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if actual != expected:
            diff = "".join(
                difflib.unified_diff(
                    actual.splitlines(keepends=True),
                    expected.splitlines(keepends=True),
                    fromfile=str(OUTPUT_PATH),
                    tofile="generated",
                )
            )
            raise SystemExit(f"MMAT TCC LaTeX export is stale:\n{diff}")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(expected, encoding="utf-8")


if __name__ == "__main__":
    main()
