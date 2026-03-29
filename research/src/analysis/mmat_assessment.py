"""Módulo para avaliação de qualidade MMAT (Mixed Methods Appraisal Tool) 2018.

Implementa a avaliação de qualidade metodológica dos estudos incluídos
na revisão sistemática, conforme o MMAT versão 2018 (Hong et al., 2018).

References
----------
Hong, Q. N., Pluye, P., Fàbregues, S., Bartlett, G., Boardman, F.,
Cargo, M., ... & Vedel, I. (2018). Mixed Methods Appraisal Tool (MMAT),
version 2018. Registration of Copyright (#1148552).
"""

from __future__ import annotations

import csv
import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from ..config import load_config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MMAT 2018 criteria definitions per study design
# ---------------------------------------------------------------------------

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
        "Q2": "Are measurements appropriate regarding both the outcome and intervention (or exposure)?",
        "Q3": "Are there complete outcome data?",
        "Q4": "Are the confounders accounted for in the design and analysis?",
        "Q5": "During the study period, is the intervention administered (or exposure occurred) as intended?",
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
        "Q3": "Are the outputs of the integration of qualitative and quantitative components adequately interpreted?",
        "Q4": "Are divergences and inconsistencies between quantitative and qualitative results adequately addressed?",
        "Q5": "Do the different components of the study adhere to the quality criteria of each tradition?",
    },
}

# Valores válidos para cada critério MMAT
VALID_RESPONSES = {"Y", "N", "CT"}  # Yes, No, Can't Tell

# ---------------------------------------------------------------------------
# Mapping: paper_id prefix -> database id (title fragment)
# These are the 17 included studies with their real MMAT assessments.
# ---------------------------------------------------------------------------

MMAT_ASSESSMENTS: Dict[str, Dict[str, Any]] = {
    "Implementation2025_000": {
        "title_fragment": "Implementation of Educational Data Mining",
        "authors_fragment": "Tjahyadi",
        "year": 2025,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "N", "Q3": "Y", "Q4": "CT", "Q5": "Y"},
        "score": 3,
        "limitations": "Single private school (n=280); limited representativeness; nonresponse not discussed",
    },
    "Design2025_004": {
        "title_fragment": "Design of Personalized Learning Path",
        "authors_fragment": "Zhang",
        "year": 2025,
        "design": "quantitative_nonrandomized",
        "criteria": {"Q1": "CT", "Q2": "Y", "Q3": "CT", "Q4": "N", "Q5": "Y"},
        "score": 2,
        "limitations": "Population unclear; data completeness not discussed; confounders not controlled",
    },
    "Enhancing2025_012": {
        "title_fragment": "Enhancing Student Achievement in Circle Theorems",
        "authors_fragment": "Nyantah",
        "year": 2025,
        "design": "quantitative_nonrandomized",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "CT", "Q4": "N", "Q5": "Y"},
        "score": 3,
        "limitations": "Cluster assignment; confounders not controlled; data completeness not reported",
    },
    "Machine2024_009": {
        "title_fragment": "Machine learning methods as auxiliary tool",
        "authors_fragment": "Milićević",
        "year": 2024,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "N", "Q3": "Y", "Q4": "CT", "Q5": "Y"},
        "score": 3,
        "limitations": "Single technical faculty; limited representativeness; nonresponse not discussed",
    },
    "Authentic2024_013": {
        "title_fragment": "Authentic Assessment for Motivating Student Learning",
        "authors_fragment": "Appiah-Odame",
        "year": 2024,
        "design": "qualitative",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "Y", "Q4": "Y", "Q5": "N"},
        "score": 4,
        "limitations": "Small sample (12 teachers); specific rural context; no triangulation",
    },
    "Assessing2024_015": {
        "title_fragment": "Assessing the Effectiveness of Adaptive Learning",
        "authors_fragment": "Jose",
        "year": 2024,
        "design": "mixed_methods",
        "criteria": {"Q1": "Y", "Q2": "CT", "Q3": "CT", "Q4": "N", "Q5": "Y"},
        "score": 2,
        "limitations": "Quali-quanti integration insufficient; divergences not discussed",
    },
    "Innovative2023_005": {
        "title_fragment": "Innovative Model of Higher Mathematics",
        "authors_fragment": "Zhang",
        "year": 2023,
        "design": "quantitative_nonrandomized",
        "criteria": {"Q1": "CT", "Q2": "Y", "Q3": "CT", "Q4": "Y", "Q5": "Y"},
        "score": 3,
        "limitations": "Higher education only; data completeness not reported",
    },
    "Performance2023_014": {
        "title_fragment": "Performance assessment: Improving metacognitive",
        "authors_fragment": "Mertasari",
        "year": 2023,
        "design": "quantitative_nonrandomized",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "CT", "Q4": "Y", "Q5": "Y"},
        "score": 4,
        "limitations": "Cluster randomization; data completeness not explicit",
    },
    "Analysis2022_003": {
        "title_fragment": "Analysis of Feature Selection and Data Mining",
        "authors_fragment": "Kumar",
        "year": 2022,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "CT", "Q3": "Y", "Q4": "CT", "Q5": "N"},
        "score": 2,
        "limitations": "Dataset origin unclear; no cross-validation; limited metrics",
    },
    "Machine2022_010": {
        "title_fragment": "Machine Learning and Explainable AI Approach",
        "authors_fragment": "Hasib",
        "year": 2022,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "Y", "Q4": "CT", "Q5": "Y"},
        "score": 4,
        "limitations": "Secondary dataset; completeness not discussed; no real classroom validation",
    },
    "Math2021_001": {
        "title_fragment": "Math proficiency prediction in computer-based",
        "authors_fragment": "Pejic",
        "year": 2021,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "Y", "Q4": "Y", "Q5": "Y"},
        "score": 5,
        "limitations": "Robust PISA dataset; rigorous sampling; no critical limitations identified",
    },
    "Analysis2021_016": {
        "title_fragment": "Analysis of Facebook in the Teaching-Learning",
        "authors_fragment": "Salas-Rueda",
        "year": 2021,
        "design": "quantitative_nonrandomized",
        "criteria": {"Q1": "N", "Q2": "Y", "Q3": "CT", "Q4": "N", "Q5": "CT"},
        "score": 1,
        "limitations": "Small sample (n=46); convenience sample; confounders not controlled; observational",
    },
    "Multimodels2020_002": {
        "title_fragment": "Multi-models of Educational Data Mining",
        "authors_fragment": "Sokkhey",
        "year": 2020,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "CT", "Q3": "Y", "Q4": "CT", "Q5": "Y"},
        "score": 3,
        "limitations": "Cambodia-specific context; representativeness not discussed",
    },
    "Data2020_011": {
        "title_fragment": "Data Mining for Student Performance Prediction",
        "authors_fragment": "Ünal",
        "year": 2020,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "CT", "Q3": "CT", "Q4": "CT", "Q5": "CT"},
        "score": 1,
        "limitations": "Insufficient methodology description; metrics not detailed; bias not discussed",
    },
    "Machine2019_007": {
        "title_fragment": "Machine Learning-based Predictive Analytics",
        "authors_fragment": "Uskov",
        "year": 2019,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "N", "Q3": "Y", "Q4": "CT", "Q5": "Y"},
        "score": 3,
        "limitations": "Single university; benchmark without classroom application; data not shared",
    },
    "Identifying2017_006": {
        "title_fragment": "Identifying the Classification Performances",
        "authors_fragment": "Depren",
        "year": 2017,
        "design": "quantitative_descriptive",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "Y", "Q4": "Y", "Q5": "Y"},
        "score": 5,
        "limitations": "Robust TIMSS dataset; international sampling; multivariate analysis",
    },
    "Computational2017_008": {
        "title_fragment": "Computational Models of Human Learning",
        "authors_fragment": "MacLellan",
        "year": 2017,
        "design": "quantitative_nonrandomized",
        "criteria": {"Q1": "Y", "Q2": "Y", "Q3": "Y", "Q4": "Y", "Q5": "Y"},
        "score": 5,
        "limitations": "7-domain validation; mixed-effects regression; well-specified models",
    },
}

# ---------------------------------------------------------------------------
# Design labels (Portuguese and English)
# ---------------------------------------------------------------------------

DESIGN_LABELS: Dict[str, str] = {
    "qualitative": "Qualitativo",
    "quantitative_randomized": "Quantitativo Randomizado",
    "quantitative_nonrandomized": "Quantitativo Não-Randomizado",
    "quantitative_descriptive": "Quantitativo Descritivo",
    "mixed_methods": "Métodos Mistos",
}

DESIGN_LABELS_EN: Dict[str, str] = {
    "qualitative": "Qualitative",
    "quantitative_randomized": "Quantitative Randomized",
    "quantitative_nonrandomized": "Quantitative Non-randomized",
    "quantitative_descriptive": "Quantitative Descriptive",
    "mixed_methods": "Mixed Methods",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def classify_study_design(title: str, abstract: str, study_type: Optional[str] = None) -> str:
    """Classify a study design based on metadata.

    This is a heuristic classifier; for the 17 included studies the design
    is already encoded in ``MMAT_ASSESSMENTS``.  This function is provided
    for extensibility to new studies.

    Parameters
    ----------
    title : str
        Paper title.
    abstract : str
        Paper abstract.
    study_type : str, optional
        Pre-classified study type from database.

    Returns
    -------
    str
        One of the keys from ``MMAT_CRITERIA``.
    """
    text = f"{title} {abstract} {study_type or ''}".lower()

    if any(kw in text for kw in ["mixed method", "quali-quanti", "qualitative and quantitative"]):
        return "mixed_methods"
    if any(kw in text for kw in ["qualitative", "interview", "thematic analysis", "phenomenolog"]):
        return "qualitative"
    if any(kw in text for kw in ["randomized controlled", "rct", "randomized trial"]):
        return "quantitative_randomized"
    if any(kw in text for kw in [
        "quasi-experiment", "pre-post", "comparison group",
        "non-randomized", "nonrandomized", "control group",
    ]):
        return "quantitative_nonrandomized"

    # Default for ML/data mining studies
    return "quantitative_descriptive"


def compute_mmat_score(criteria: Dict[str, str]) -> int:
    """Compute the MMAT quality score (count of 'Y' responses).

    Parameters
    ----------
    criteria : dict
        Mapping Q1..Q5 -> 'Y'|'N'|'CT'.

    Returns
    -------
    int
        Number of criteria rated 'Y' (range 0-5).
    """
    return sum(1 for v in criteria.values() if v == "Y")


def get_quality_rating(score: int) -> str:
    """Return a human-readable quality rating from the MMAT score.

    Parameters
    ----------
    score : int
        MMAT score (0-5).

    Returns
    -------
    str
        Quality label.
    """
    if score >= 4:
        return "Alta"
    elif score >= 3:
        return "Moderada"
    elif score >= 2:
        return "Baixa"
    else:
        return "Muito Baixa"


def get_quality_rating_en(score: int) -> str:
    """Return an English quality rating label.

    Parameters
    ----------
    score : int
        MMAT score (0-5).

    Returns
    -------
    str
        Quality label in English.
    """
    if score >= 4:
        return "High"
    elif score >= 3:
        return "Moderate"
    elif score >= 2:
        return "Low"
    else:
        return "Very Low"


# ---------------------------------------------------------------------------
# Match assessment keys to database papers
# ---------------------------------------------------------------------------


def match_assessments_to_papers(
    db_path: str,
) -> List[Dict[str, Any]]:
    """Match MMAT assessment entries to papers in the database.

    Uses ``title_fragment`` from each assessment to locate the
    corresponding row in the ``papers`` table where
    ``selection_stage = 'included'``.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database.

    Returns
    -------
    list of dict
        Each dict contains assessment data enriched with database
        fields (``db_id``, ``full_title``, ``authors``, ``year``).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, title, authors, year FROM papers WHERE selection_stage = 'included'"
    ).fetchall()
    conn.close()

    results: List[Dict[str, Any]] = []

    for key, assessment in MMAT_ASSESSMENTS.items():
        fragment = assessment["title_fragment"].lower()
        matched = None
        for row in rows:
            if fragment in (row["title"] or "").lower():
                matched = row
                break

        if matched is None:
            logger.warning("Could not match assessment '%s' to any included paper.", key)
            continue

        results.append({
            "assessment_key": key,
            "db_id": matched["id"],
            "full_title": matched["title"],
            "authors": matched["authors"],
            "year": matched["year"],
            "design": assessment["design"],
            "design_label": DESIGN_LABELS.get(assessment["design"], assessment["design"]),
            "criteria": assessment["criteria"],
            "score": assessment["score"],
            "quality_rating": get_quality_rating(assessment["score"]),
            "limitations": assessment["limitations"],
        })

    logger.info("Matched %d/%d assessments to database papers.", len(results), len(MMAT_ASSESSMENTS))
    return results


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------


def build_results_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Build a flat DataFrame from matched assessment results.

    Parameters
    ----------
    results : list of dict
        Output of ``match_assessments_to_papers``.

    Returns
    -------
    pd.DataFrame
    """
    rows = []
    for r in results:
        row = {
            "ID": r["assessment_key"],
            "Title": r["full_title"],
            "Authors": _short_authors(r["authors"]),
            "Year": r["year"],
            "Design": r["design_label"],
            "Q1": r["criteria"]["Q1"],
            "Q2": r["criteria"]["Q2"],
            "Q3": r["criteria"]["Q3"],
            "Q4": r["criteria"]["Q4"],
            "Q5": r["criteria"]["Q5"],
            "Score": r["score"],
            "Quality": r["quality_rating"],
            "Limitations": r["limitations"],
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sort_values(["Year", "Authors"], ascending=[False, True]).reset_index(drop=True)
    return df


def _short_authors(authors_str: Optional[str]) -> str:
    """Extract a short 'First Author et al.' label."""
    if not authors_str:
        return "N/A"
    # authors may be JSON list or semicolon-separated
    try:
        authors_list = json.loads(authors_str)
        if isinstance(authors_list, list) and len(authors_list) > 0:
            first = authors_list[0] if isinstance(authors_list[0], str) else str(authors_list[0])
            if len(authors_list) > 1:
                return f"{first} et al."
            return first
    except (json.JSONDecodeError, TypeError):
        pass
    # Fallback: semicolon or comma separated
    parts = [p.strip() for p in authors_str.replace(";", ",").split(",") if p.strip()]
    if len(parts) > 1:
        return f"{parts[0]} et al."
    return parts[0] if parts else "N/A"


def export_csv(df: pd.DataFrame, output_path: Path) -> Path:
    """Export MMAT results to CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Results dataframe from ``build_results_dataframe``.
    output_path : Path
        Target CSV file path.

    Returns
    -------
    Path
        Path to the written file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    logger.info("CSV exported to %s", output_path)
    return output_path


def export_latex_table(df: pd.DataFrame, output_path: Path) -> Path:
    """Export MMAT results as a LaTeX longtable.

    Parameters
    ----------
    df : pd.DataFrame
        Results dataframe.
    output_path : Path
        Target .tex file path.

    Returns
    -------
    Path
        Path to the written file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build LaTeX content
    lines: List[str] = []
    lines.append("% MMAT Quality Assessment Table (auto-generated)")
    lines.append(f"% Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append(r"\begin{longtable}{p{3.5cm}cp{3cm}ccccccc}")
    lines.append(r"\caption{Avaliação de qualidade MMAT dos estudos incluídos}")
    lines.append(r"\label{tab:mmat_assessment} \\")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Autores (Ano)} & \textbf{Design} & \textbf{Q1} & \textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Score} & \textbf{Qualidade} \\")
    lines.append(r"\midrule")
    lines.append(r"\endfirsthead")
    lines.append("")
    lines.append(r"\multicolumn{9}{c}{\tablename\ \thetable\ -- Continuação} \\")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Autores (Ano)} & \textbf{Design} & \textbf{Q1} & \textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Score} & \textbf{Qualidade} \\")
    lines.append(r"\midrule")
    lines.append(r"\endhead")
    lines.append("")
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{9}{r}{Continua na próxima página} \\")
    lines.append(r"\endfoot")
    lines.append("")
    lines.append(r"\bottomrule")
    lines.append(r"\endlastfoot")
    lines.append("")

    # Map response to LaTeX symbols
    def _latex_symbol(val: str) -> str:
        if val == "Y":
            return r"\checkmark"
        elif val == "N":
            return r"\texttimes"
        else:
            return "?"

    # Design abbreviations for compactness
    design_abbrev: Dict[str, str] = {
        "Qualitativo": "QL",
        "Quantitativo Randomizado": "QR",
        "Quantitativo Não-Randomizado": "QNR",
        "Quantitativo Descritivo": "QD",
        "Métodos Mistos": "MM",
    }

    for _, row in df.iterrows():
        authors_year = _latex_escape(f"{row['Authors']} ({row['Year']})")
        design = design_abbrev.get(row["Design"], row["Design"])
        q1 = _latex_symbol(row["Q1"])
        q2 = _latex_symbol(row["Q2"])
        q3 = _latex_symbol(row["Q3"])
        q4 = _latex_symbol(row["Q4"])
        q5 = _latex_symbol(row["Q5"])
        score = f"{row['Score']}/5"
        quality = _latex_escape(row["Quality"])
        lines.append(
            f"{authors_year} & {design} & {q1} & {q2} & {q3} & {q4} & {q5} & {score} & {quality} \\\\"
        )

    lines.append("")
    lines.append(r"\end{longtable}")
    lines.append("")
    lines.append(r"% Legend: \checkmark = Yes, \texttimes = No, ? = Can't Tell")
    lines.append(r"% Design: QL = Qualitative, QR = Quantitative Randomized,")
    lines.append(r"% QNR = Quantitative Non-randomized, QD = Quantitative Descriptive, MM = Mixed Methods")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("LaTeX table exported to %s", output_path)
    return output_path


def _latex_escape(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
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
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    return text


# ---------------------------------------------------------------------------
# Database update
# ---------------------------------------------------------------------------


def update_database_with_scores(
    db_path: str,
    results: List[Dict[str, Any]],
) -> int:
    """Update the papers table with MMAT quality scores.

    Stores the MMAT score and assessment details in the ``notes`` column
    as a JSON-enriched string, preserving any existing notes.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database.
    results : list of dict
        Output of ``match_assessments_to_papers``.

    Returns
    -------
    int
        Number of rows updated.
    """
    conn = sqlite3.connect(db_path)
    updated = 0

    for r in results:
        mmat_data = {
            "mmat_design": r["design"],
            "mmat_criteria": r["criteria"],
            "mmat_score": r["score"],
            "mmat_quality": r["quality_rating"],
            "mmat_limitations": r["limitations"],
            "mmat_assessed_at": datetime.now().isoformat(),
        }

        # Read existing notes
        row = conn.execute(
            "SELECT notes FROM papers WHERE id = ?", (r["db_id"],)
        ).fetchone()
        existing_notes = row[0] if row and row[0] else ""

        # Try to merge with existing JSON notes
        try:
            notes_dict = json.loads(existing_notes) if existing_notes else {}
        except (json.JSONDecodeError, TypeError):
            notes_dict = {"_original_notes": existing_notes} if existing_notes else {}

        notes_dict.update(mmat_data)

        conn.execute(
            "UPDATE papers SET notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (json.dumps(notes_dict, ensure_ascii=False), r["db_id"]),
        )
        updated += 1

    conn.commit()
    conn.close()
    logger.info("Updated %d papers with MMAT scores in database.", updated)
    return updated


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print summary statistics of the MMAT assessment.

    Parameters
    ----------
    results : list of dict
        Output of ``match_assessments_to_papers``.
    """
    if not results:
        print("No results to summarize.")
        return

    scores = [r["score"] for r in results]
    designs = [r["design"] for r in results]

    print("\n" + "=" * 60)
    print("MMAT 2018 - Quality Assessment Summary")
    print("=" * 60)
    print(f"Total studies assessed: {len(results)}")
    print(f"Mean score: {sum(scores) / len(scores):.2f}/5")
    print(f"Median score: {sorted(scores)[len(scores) // 2]}/5")
    print(f"Min score: {min(scores)}/5")
    print(f"Max score: {max(scores)}/5")

    # Score distribution
    print("\nScore distribution:")
    for s in range(1, 6):
        count = scores.count(s)
        bar = "#" * count
        print(f"  {s}/5: {count:2d} studies {bar}")

    # Quality rating distribution
    print("\nQuality rating:")
    ratings = [get_quality_rating(s) for s in scores]
    for label in ["Alta", "Moderada", "Baixa", "Muito Baixa"]:
        count = ratings.count(label)
        if count > 0:
            print(f"  {label}: {count} studies")

    # Design distribution
    print("\nStudy designs:")
    for design_key, design_label in DESIGN_LABELS.items():
        count = designs.count(design_key)
        if count > 0:
            print(f"  {design_label}: {count} studies")

    print("=" * 60)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the full MMAT assessment pipeline.

    1. Connect to the SQLite database
    2. Match assessments to included papers
    3. Export CSV and LaTeX table
    4. Update database with MMAT scores
    5. Print summary statistics
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    config = load_config()
    db_path = config.database.db_path
    exports_dir = Path(config.database.exports_dir)

    logger.info("Starting MMAT assessment pipeline...")
    logger.info("Database: %s", db_path)

    # 1. Match assessments to database papers
    results = match_assessments_to_papers(db_path)

    if not results:
        logger.error("No assessments could be matched to database papers.")
        return

    # 2. Build results dataframe
    df = build_results_dataframe(results)

    # 3. Export CSV
    csv_path = exports_dir / "analysis" / "mmat_assessment.csv"
    export_csv(df, csv_path)

    # 4. Export LaTeX table
    latex_path = exports_dir / "references" / "mmat_table.tex"
    export_latex_table(df, latex_path)

    # 5. Update database
    updated = update_database_with_scores(db_path, results)
    logger.info("Database updated: %d papers.", updated)

    # 6. Print summary
    print_summary(results)

    logger.info("MMAT assessment pipeline complete.")


if __name__ == "__main__":
    main()
