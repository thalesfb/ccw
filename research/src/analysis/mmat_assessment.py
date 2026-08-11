"""Criterion-level MMAT 2018 appraisal support.

The MMAT authors discourage producing a single overall numerical score because
it hides which methodological criteria were met or not met. This module keeps
Q1--Q5 responses visible, validates their provenance, and exports deterministic
criterion-level artefacts.
"""

from __future__ import annotations

import csv
import json
import logging
import re
import sqlite3
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import pandas as pd

from ..config import load_config

logger = logging.getLogger(__name__)

MMAT_CRITERIA: Dict[str, Dict[str, str]] = {
    "qualitative": {
        "Q1": "Is the qualitative approach appropriate to answer the research question?",
        "Q2": "Are the qualitative data collection methods adequate to address the research question?",
        "Q3": "Are the findings adequately derived from the data?",
        "Q4": "Is the interpretation of results sufficiently substantiated by data?",
        "Q5": "Is there coherence between qualitative data sources, collection, analysis and interpretation?",
    },
    "quantitative_randomized": {
        "Q1": "Is randomization appropriately performed?",
        "Q2": "Are the groups comparable at baseline?",
        "Q3": "Are there complete outcome data?",
        "Q4": "Are outcome assessors blinded to the intervention provided?",
        "Q5": "Did the participants adhere to the assigned intervention?",
    },
    "quantitative_nonrandomized": {
        "Q1": "Are the participants representative of the target population?",
        "Q2": "Are measurements appropriate regarding both the outcome and intervention?",
        "Q3": "Are there complete outcome data?",
        "Q4": "Are the confounders accounted for in the design and analysis?",
        "Q5": "Did the intervention or exposure occur as intended?",
    },
    "quantitative_descriptive": {
        "Q1": "Is the sampling strategy relevant to address the research question?",
        "Q2": "Is the sample representative of the target population?",
        "Q3": "Are the measurements appropriate?",
        "Q4": "Is the risk of nonresponse bias low?",
        "Q5": "Is the statistical analysis appropriate to answer the research question?",
    },
    "mixed_methods": {
        "Q1": "Is there an adequate rationale for using a mixed methods design?",
        "Q2": "Are the different components of the study effectively integrated?",
        "Q3": "Are the outputs of the integration adequately interpreted?",
        "Q4": "Are divergences between quantitative and qualitative results addressed?",
        "Q5": "Do the components adhere to the quality criteria of each tradition?",
    },
}

VALID_RESPONSES = {"Y", "N", "CT"}
EXPECTED_COLUMNS = [
    "ID",
    "Title",
    "Authors",
    "Year",
    "Design",
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Q5",
    "AssessmentBasis",
    "ReviewerRole",
    "Limitations",
]
DESIGN_LABELS = {
    "qualitative": "Qualitativo",
    "quantitative_randomized": "Quantitativo Randomizado",
    "quantitative_nonrandomized": "Quantitativo Não-Randomizado",
    "quantitative_descriptive": "Quantitativo Descritivo",
    "mixed_methods": "Métodos Mistos",
}
DEFAULT_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "mmat_assessments.csv"


def classify_study_design(
    title: str,
    abstract: str,
    study_type: Optional[str] = None,
) -> str:
    """Classify a study design heuristically for records without manual review."""
    text = f"{title} {abstract} {study_type or ''}".lower()
    if any(term in text for term in ("mixed method", "quali-quanti")):
        return "mixed_methods"
    if any(term in text for term in ("qualitative", "interview", "thematic analysis")):
        return "qualitative"
    if any(term in text for term in ("randomized controlled", "randomised controlled", " rct ")):
        return "quantitative_randomized"
    if any(
        term in text
        for term in (
            "quasi-experiment",
            "pre-post",
            "comparison group",
            "non-randomized",
            "nonrandomized",
            "control group",
        )
    ):
        return "quantitative_nonrandomized"
    return "quantitative_descriptive"


def _normalize(value: object) -> str:
    """Normalize text for stable cross-source matching."""
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _first_author(value: object) -> str:
    """Return a normalized first-author token from JSON or plain text."""
    if value is None:
        return ""
    text = str(value)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list) and parsed:
            first = parsed[0]
            if isinstance(first, Mapping):
                first = first.get("name") or first.get("author") or ""
            return _normalize(first).split(" ")[-1]
    except (json.JSONDecodeError, TypeError):
        pass
    first = re.split(r"[;,]", text, maxsplit=1)[0]
    normalized = re.sub(r"\bet\s+al\b.*$", "", _normalize(first)).strip()
    return normalized.split(" ")[-1] if normalized else ""


def load_assessments(
    csv_path: Path | str = DEFAULT_DATA_PATH,
    *,
    expected_count: Optional[int] = 17,
) -> List[Dict[str, Any]]:
    """Load and validate the canonical criterion-level appraisal dataset."""
    path = Path(csv_path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"Unexpected MMAT columns: {reader.fieldnames}; expected {EXPECTED_COLUMNS}"
            )
        rows = [dict(row) for row in reader]

    if expected_count is not None and len(rows) != expected_count:
        raise ValueError(f"Expected {expected_count} MMAT assessments, found {len(rows)}")

    ids = [row["ID"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("MMAT assessment IDs must be unique")

    for row in rows:
        if row["Design"] not in MMAT_CRITERIA:
            raise ValueError(f"Invalid MMAT design for {row['ID']}: {row['Design']}")
        try:
            row["Year"] = int(row["Year"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid year for {row['ID']}: {row['Year']}") from exc
        for criterion in ("Q1", "Q2", "Q3", "Q4", "Q5"):
            if row[criterion] not in VALID_RESPONSES:
                raise ValueError(
                    f"Invalid response for {row['ID']}.{criterion}: {row[criterion]}"
                )
        for field in ("Title", "Authors", "AssessmentBasis", "ReviewerRole", "Limitations"):
            if not str(row[field]).strip():
                raise ValueError(f"{row['ID']} is missing {field}")

    return rows


def match_assessments_to_papers(
    db_path: str,
    assessments: Optional[Sequence[Mapping[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Match each appraisal to exactly one included database record.

    Matching requires normalized title, publication year, and first author.
    Missing or ambiguous matches fail closed instead of silently producing an
    incomplete export.
    """
    records = list(assessments or load_assessments())
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        papers = conn.execute(
            "SELECT id, title, authors, year FROM papers "
            "WHERE selection_stage = 'included'"
        ).fetchall()

    results: List[Dict[str, Any]] = []
    for assessment in records:
        title_key = _normalize(assessment["Title"])
        author_key = _first_author(assessment["Authors"])
        year = int(assessment["Year"])

        candidates = [
            paper
            for paper in papers
            if _normalize(paper["title"]) == title_key
            and int(paper["year"]) == year
            and _first_author(paper["authors"]) == author_key
        ]

        if len(candidates) != 1:
            raise ValueError(
                f"Assessment {assessment['ID']} expected one database match, "
                f"found {len(candidates)}"
            )

        paper = candidates[0]
        criteria = {key: assessment[key] for key in ("Q1", "Q2", "Q3", "Q4", "Q5")}
        results.append(
            {
                "assessment_key": assessment["ID"],
                "db_id": paper["id"],
                "full_title": paper["title"],
                "authors": assessment["Authors"],
                "year": year,
                "design": assessment["Design"],
                "design_label": DESIGN_LABELS[assessment["Design"]],
                "criteria": criteria,
                "assessment_basis": assessment["AssessmentBasis"],
                "reviewer_role": assessment["ReviewerRole"],
                "limitations": assessment["Limitations"],
            }
        )

    return results


def build_results_dataframe(results: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    """Build the deterministic criterion-level export dataframe."""
    rows = []
    for result in results:
        row = {
            "ID": result["assessment_key"],
            "Title": result["full_title"],
            "Authors": result["authors"],
            "Year": int(result["year"]),
            "Design": result["design"],
            **dict(result["criteria"]),
            "AssessmentBasis": result["assessment_basis"],
            "ReviewerRole": result["reviewer_role"],
            "Limitations": result["limitations"],
        }
        rows.append(row)
    return (
        pd.DataFrame(rows, columns=EXPECTED_COLUMNS)
        .sort_values(["Year", "Authors", "ID"], ascending=[False, True, True])
        .reset_index(drop=True)
    )


def export_csv(df: pd.DataFrame, output_path: Path) -> Path:
    """Export criterion-level MMAT data without volatile timestamps."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig", lineterminator="\n")
    return output_path


def _latex_escape(value: object) -> str:
    text = str(value)
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
    return "".join(replacements.get(char, char) for char in text)


def export_latex_table(df: pd.DataFrame, output_path: Path) -> Path:
    """Export an eight-column longtable with Q1--Q5 and limitations."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% MMAT 2018 criterion-level appraisal (auto-generated)",
        r"\begin{longtable}{|p{2.8cm}|p{2.4cm}|ccccc|p{7cm}|}",
        r"\caption{Respostas aos critérios do MMAT 2018}",
        r"\label{tab:mmat_assessment} \\",
        r"\hline",
        r"\textbf{Autores (Ano)} & \textbf{Desenho} & \textbf{Q1} & "
        r"\textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & "
        r"\textbf{Limitações observadas} \\",
        r"\hline",
        r"\endfirsthead",
        r"\multicolumn{8}{c}{\tablename\ \thetable\ -- Continuação} \\",
        r"\hline",
        r"\textbf{Autores (Ano)} & \textbf{Desenho} & \textbf{Q1} & "
        r"\textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & "
        r"\textbf{Limitações observadas} \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\multicolumn{8}{r}{Continua na próxima página} \\",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]
    for _, row in df.iterrows():
        values = [
            _latex_escape(f"{row['Authors']} ({row['Year']})"),
            _latex_escape(DESIGN_LABELS[row["Design"]]),
            *[
                "ND" if row[key] == "CT" else ("S" if row[key] == "Y" else "N")
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
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def update_database_with_assessments(
    db_path: str,
    results: Sequence[Mapping[str, Any]],
) -> int:
    """Persist criterion-level appraisal data while preserving existing notes."""
    with sqlite3.connect(db_path) as conn:
        for result in results:
            row = conn.execute(
                "SELECT notes FROM papers WHERE id = ?", (result["db_id"],)
            ).fetchone()
            existing = row[0] if row and row[0] else ""
            try:
                notes = json.loads(existing) if existing else {}
            except (json.JSONDecodeError, TypeError):
                notes = {"_original_notes": existing} if existing else {}
            notes.update(
                {
                    "mmat_version": "2018",
                    "mmat_design": result["design"],
                    "mmat_criteria": dict(result["criteria"]),
                    "mmat_assessment_basis": result["assessment_basis"],
                    "mmat_reviewer_role": result["reviewer_role"],
                    "mmat_limitations": result["limitations"],
                }
            )
            notes.pop("mmat_score", None)
            notes.pop("mmat_quality", None)
            conn.execute(
                "UPDATE papers SET notes = ?, updated_at = CURRENT_TIMESTAMP "
                "WHERE id = ?",
                (json.dumps(notes, ensure_ascii=False), result["db_id"]),
            )
        conn.commit()
    return len(results)


def summarize_criteria(
    results: Sequence[Mapping[str, Any]],
) -> Dict[str, Dict[str, int]]:
    """Count Y/N/CT responses separately for every criterion."""
    summary: Dict[str, Dict[str, int]] = {}
    for criterion in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        counts = Counter(result["criteria"][criterion] for result in results)
        summary[criterion] = {
            response: counts.get(response, 0) for response in ("Y", "N", "CT")
        }
    return summary


def print_summary(results: Sequence[Mapping[str, Any]]) -> None:
    """Print design and criterion counts without an overall quality score."""
    print(f"MMAT 2018 studies assessed: {len(results)}")
    designs = Counter(result["design"] for result in results)
    for design, count in sorted(designs.items()):
        print(f"  {DESIGN_LABELS[design]}: {count}")
    print("Criterion responses:")
    for criterion, counts in summarize_criteria(results).items():
        print(f"  {criterion}: Y={counts['Y']} N={counts['N']} CT={counts['CT']}")


def main() -> None:
    """Run matching, criterion-level exports, and database synchronization."""
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    assessments = load_assessments()
    results = match_assessments_to_papers(config.database.db_path, assessments)
    dataframe = build_results_dataframe(results)
    exports_dir = Path(config.database.exports_dir)
    export_csv(dataframe, exports_dir / "analysis" / "mmat_assessment.csv")
    export_latex_table(dataframe, exports_dir / "references" / "mmat_table.tex")
    update_database_with_assessments(config.database.db_path, results)
    print_summary(results)


if __name__ == "__main__":
    main()
