"""Render the current preliminary MMAT reassessment for the TCC.

The output is deliberately labelled preliminary.  It is generated from the
current 18-record ledger and does not assign an overall quality score.
"""

from __future__ import annotations

import argparse
import csv
import difflib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = REPO_ROOT / "research" / "data" / "mmat_reassessment_current.csv"
PAPERS_PATH = REPO_ROOT / "research" / "exports" / "analysis" / "papers.csv"
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
    "hold_source_verification": "Hold: verificar fonte",
    "hold_empirical_status": "Hold: verificar empiricidade",
}


def load_rows(path: Path = DATA_PATH) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 6915, 6916, 6917, 6919, 6920, 6921, 6923]
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


def load_study_labels(path: Path = PAPERS_PATH) -> dict[str, str]:
    """Return reader-facing author/year labels for the current MMAT rows."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))

    labels: dict[str, str] = {}
    for record in records:
        study_id = str(record.get("id", "")).strip()
        if not study_id or not record.get("year"):
            continue
        authors = str(record.get("authors", "")).strip()
        first_author = authors.split(";")[0].strip()
        if "," in first_author:
            family_name = first_author.split(",", 1)[0].strip()
        else:
            family_name = first_author.split()[-1] if first_author else ""
        if not family_name:
            family_name = str(record.get("paper_id", study_id)).strip()
        suffix = " et al." if ";" in authors else ""
        labels[study_id] = f"{family_name}{suffix} ({record['year']})"

    return labels


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


def render_table(
    rows: list[dict[str, str]], labels: dict[str, str] | None = None
) -> str:
    labels = labels or load_study_labels()
    lines = [
        "% Tabela gerada de research/data/mmat_reassessment_current.csv",
        "% Reavaliação documental preliminar; não representa score nem avaliação final.",
        "% Não editar manualmente; execute: python -m src.analysis.mmat_current_tcc_table",
        r"\begin{longtable}{|p{3.9cm}|p{2.0cm}|ccccccc|p{3.0cm}|p{3.5cm}|}",
        r"\caption{Reavaliação documental preliminar dos estudos atuais com o MMAT 2018.}\label{tab:mmat-reavaliacao-atual}\\",
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
        values = [
            _latex_escape(labels.get(row["study_id"], row["study_key"])),
            _latex_escape(DESIGN_LABELS.get(design, design)),
            *[row[criterion] for criterion in CRITERIA],
            _latex_escape(BASIS_LABELS.get(row["assessment_basis"], row["assessment_basis"])),
            _latex_escape(STATUS_LABELS.get(row["assessment_status"], row["assessment_status"])),
        ]
        lines.append(" & ".join(values) + r" \\")
    lines.extend(
        [
            r"\end{longtable}",
            r"\textit{Nota:} Y = sim; N = não; CT = não é possível determinar. A base e o estado são os registrados no ledger na data do snapshot; a adjudicação metodológica pelo supervisor permanece pendente. O protocolo ou proposta contextual retido não integra a síntese empírica nem uma avaliação MMAT empírica. Um registro bibliográfico fora do recorte temporal foi excluído do escopo atual.",
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
