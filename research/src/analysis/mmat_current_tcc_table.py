"""Render the current preliminary MMAT assessment for the TCC.

The output is deliberately labelled preliminary.  It is generated from the
current 16-record dataset and does not assign an overall quality score.
"""

from __future__ import annotations

import argparse
import csv
import difflib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = REPO_ROOT / "research" / "data" / "mmat_reassessment_current.csv"
OUTPUT_PATH = (
    REPO_ROOT / "research" / "exports" / "references" / "mmat_current_tcc_table.tex"
)

CRITERIA = ("s1", "s2", "q1", "q2", "q3", "q4", "q5")
DESIGN_LABELS = {
    "quantitative_descriptive": "Quant. descritivo",
    "quantitative_nonrandomized": "Quant. não rand.",
    "quantitative_randomized": "Quant. rand.",
    "qualitative": "Qualitativo",
    "mixed_methods": "Métodos mistos",
    "metadata_hold": "Não confirmado",
    "not_applicable": "Não aplicável",
}
BASIS_LABELS = {
    "primary_full_text_reviewed_externally": "Texto primário externo",
    "abstract_and_metadata_only": "Abstract/metadados",
    "abstract_only": "Abstract",
    "metadata_only": "Metadados",
    "protocol_or_proposal_not_applicable": "Protocolo/proposta",
}
STATUS_LABELS = {
    "provisional_primary_source_review": "Provisório: fonte primária",
    "provisional_abstract_plus_metadata": "Provisório: abstract/metadados",
    "hold_source_verification": "Provisório: fonte documental",
    "hold_empirical_status": "Não aplicável: protocolo",
}
STUDY_LABELS = {
    "1": r"Pejic et al. (2021) \cite{Math2021_001}",
    "2": r"Tjahyadi (2025) \cite{Implementation2025_000}",
    "3": r"Sokkhey et al. (2020) \cite{Multimodels2020_002}",
    "4": r"Kumar et al. (2022) \cite{Analysis2022_003}",
    "5": r"Zhang et al. (2025) \cite{Design2025_004}",
    "6": r"Depren et al. (2017) \cite{Identifying2017_006}",
    "7": r"Zhang (2023) \cite{Innovative2023_005}",
    "8": r"MacLellan (2017) \cite{Computational2017_008}",
    "9": r"Uskov et al. (2019) \cite{Machine2019_007}",
    "10": r"Milićević et al. (2024) \cite{Machine2024_009}",
    "6916": r"Villegas-Ch et al. (2025) \cite{Villegas2025_6916}",
    "6917": r"Özseven e Özseven (2026) \cite{Ozseven2026_6917}",
    "6918": r"Käser Jacober (2014) \cite{KaserJacober2014}",
    "6920": r"Echeveria et al. (2025) \cite{Echeveria2025_6920}",
    "6921": r"Imperatrice et al. (2025) \cite{Imperatrice2025_6921}",
    "6923": r"Zeng (2025) \cite{Zeng2025_6923}",
}


def load_rows(path: Path = DATA_PATH) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 6916, 6917, 6918, 6920, 6921, 6923]
    ids = [int(row["study_id"]) for row in rows]
    if ids != expected_ids:
        raise ValueError(f"Expected current MMAT IDs {expected_ids}; found {ids}")
    for row in rows:
        if row.get("assessment_status") == "final":
            raise ValueError("The current TCC table cannot render final MMAT claims")
        for criterion in CRITERIA:
            if row.get(criterion) not in {"Y", "N", "CT"}:
                raise ValueError(f"Invalid {criterion} value for study {row.get('study_id')}")
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


def render_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "% Tabela gerada de research/data/mmat_reassessment_current.csv",
        "% Avaliação metodológica documental preliminar; não representa score nem avaliação final.",
        "% Não editar manualmente; execute: python -m src.analysis.mmat_current_tcc_table",
        r"\begin{landscape}",
        r"\scriptsize",
        r"\begin{longtable}{|p{4.55cm}|p{2.0cm}|ccccccc|p{3.0cm}|p{3.5cm}|}",
        r"\caption{Avaliação metodológica documental preliminar dos estudos incluídos com o MMAT 2018.}\label{tab:mmat-avaliacao-atual}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Desenho} & "
        r"\textbf{S1} & \textbf{S2} & \textbf{Q1} & \textbf{Q2} & "
        r"\textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Base} & \textbf{Estado} \\",
        r"\hline",
        r"\endfirsthead",
        r"\multicolumn{11}{c}{\tablename\ \thetable\ -- Continuação}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Desenho} & "
        r"\textbf{S1} & \textbf{S2} & \textbf{Q1} & \textbf{Q2} & "
        r"\textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Base} & \textbf{Estado} \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\multicolumn{11}{r}{\textit{Continua na próxima página}}\\",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]
    for row in rows:
        design = row.get("design") or row.get("design_status") or "not_applicable"
        if row.get("assessment_status") == "hold_source_verification":
            design = "metadata_hold"
        study_label = STUDY_LABELS.get(row["study_id"])
        if study_label is None:
            raise ValueError(f"No reader-facing label configured for study {row['study_id']}")
        values = [
            study_label,
            _latex_escape(DESIGN_LABELS.get(design, design)),
            *[row[criterion] for criterion in CRITERIA],
            _latex_escape(BASIS_LABELS.get(row["assessment_basis"], row["assessment_basis"])),
            _latex_escape(STATUS_LABELS.get(row["assessment_status"], row["assessment_status"])),
        ]
        lines.append(" & ".join(values) + r" \\")
    lines.extend(
        [
            r"\end{longtable}",
            r"\textit{Nota:} Y = sim; N = não; CT = não é possível determinar. A coluna Base indica a fonte documental considerada, e a coluna Estado indica o caráter preliminar da decisão. O protocolo/proposta contextual não integra a síntese empírica nem a avaliação MMAT empírica.",
            r"\end{landscape}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
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
            raise SystemExit(f"Current MMAT TCC export is stale:\n{diff}")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(expected, encoding="utf-8")


if __name__ == "__main__":
    main()
