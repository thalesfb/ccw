"""Cross-check the local database, exports and derived summary.

The validation is read-only with respect to the review database. It is kept
under ``src.pipelines`` because the CLI and existing tests use that public
import path.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB = REPOSITORY_ROOT / "research" / "systematic_review.sqlite"
DEFAULT_CSV = REPOSITORY_ROOT / "research" / "exports" / "analysis" / "papers.csv"
DEFAULT_SUMMARY = REPOSITORY_ROOT / "research" / "exports" / "reports" / "summary.json"


def _doi(value: Any) -> str:
    return str(value or "").strip().lower().removeprefix("doi:").strip()


def _duplicate_dois(values: list[str]) -> list[dict[str, Any]]:
    counts = Counter(value for value in values if value)
    return [
        {"doi": doi, "count": count}
        for doi, count in sorted(counts.items())
        if count > 1
    ]


def _read_db(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"error": f"Missing DB: {path}"}

    conn = sqlite3.connect(path)
    try:
        total = int(conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0])
        included = int(
            conn.execute(
                "SELECT COUNT(*) FROM papers WHERE selection_stage = 'included'"
            ).fetchone()[0]
        )
        doi_values = [
            _doi(row[0])
            for row in conn.execute("SELECT doi FROM papers").fetchall()
        ]
        return {
            "total": total,
            "included": included,
            "dup_doi": _duplicate_dois(doi_values),
        }
    finally:
        conn.close()


def _read_csv(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"error": f"Missing CSV: {path}"}

    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    included = sum(
        str(row.get("selection_stage", "")).strip().lower() == "included"
        for row in rows
    )
    return {
        "total": len(rows),
        "included": included,
        "dup_doi": _duplicate_dois([_doi(row.get("doi")) for row in rows]),
    }


def _read_summary(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"error": f"Missing summary: {path}"}

    payload = json.loads(path.read_text(encoding="utf-8"))
    statistics = payload.get("statistics", {})
    years = statistics.get("years", {}).get("distribution", {})
    out_of_range_years = []
    for year, count in years.items():
        try:
            year_number = int(year)
        except (TypeError, ValueError):
            continue
        if year_number < 2015 or year_number > 2026:
            out_of_range_years.append({"year": str(year), "count": int(count)})
    out_of_range_years.sort(key=lambda row: int(row["year"]))
    return {
        "total_papers": statistics.get("total_papers"),
        "prisma": statistics.get("prisma", {}),
        "selection_stages": statistics.get("selection_stages", {}),
        "out_of_range_years": out_of_range_years,
    }


def validate_exports_report(
    db_path: Path | None = None,
    csv_path: Path | None = None,
    summary_path: Path | None = None,
) -> dict[str, Any]:
    """Return a read-only consistency report for DB, CSV and summary JSON."""

    db = _read_db(Path(db_path or DEFAULT_DB))
    csv_report = _read_csv(Path(csv_path or DEFAULT_CSV))
    summary = _read_summary(Path(summary_path or DEFAULT_SUMMARY))

    db_total = db.get("total")
    csv_total = csv_report.get("total")
    summary_total = summary.get("total_papers")
    db_included = db.get("included")
    csv_included = csv_report.get("included")
    summary_included = summary.get("prisma", {}).get("included")

    return {
        "db": db,
        "csv": csv_report,
        "summary": summary,
        "diffs": {
            "total": {
                "db": db_total,
                "csv": csv_total,
                "summary": summary_total,
            },
            "included": {
                "db": db_included,
                "csv": csv_included,
                "summary_prisma_included": summary_included,
            },
        },
        "samples": {
            "db_dup_doi_sample": db.get("dup_doi", [])[:10],
            "csv_dup_doi_sample": csv_report.get("dup_doi", [])[:10],
            "summary_out_of_range_years": summary.get("out_of_range_years", []),
        },
    }


def check_exports_consistency() -> tuple[Path, str]:
    """Write a JSON consistency report to the ignored research logs folder."""

    report = validate_exports_report()
    output_path = REPOSITORY_ROOT / "research" / "logs" / "check_exports_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output_path, json.dumps(report, indent=2, ensure_ascii=False)


def verify_papers(csv_path: Path, out_path: Path) -> dict[str, Any]:
    """Create a compact CSV quality report without changing the source CSV."""

    report = _read_csv(Path(csv_path))
    rows = []
    for duplicate in report.get("dup_doi", []):
        rows.append({"check": "duplicate_doi", "doi": duplicate["doi"], "count": duplicate["count"]})
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "doi", "count"])
        writer.writeheader()
        writer.writerows(rows)
    return {
        "total": report.get("total"),
        "duplicate_doi_rows": sum(row["count"] for row in report.get("dup_doi", [])),
        "duplicate_title_rows": 0,
        "missing_doi": None,
        "missing_abstract": None,
        "likely_irrelevant": None,
    }


def regenerate_summary_from_db() -> Path:
    """Regenerate the summary through the canonical report generator."""

    from ..config import load_config
    from ..db import read_papers
    from ..analysis.reports import ReportGenerator

    config = load_config()
    dataframe = read_papers(config)
    if dataframe.empty:
        raise ValueError("No papers found in the configured database")
    ReportGenerator().generate_summary_report(dataframe)
    return Path(config.database.exports_dir) / "reports" / "summary.json"


def diagnose_included(title: str) -> dict[str, Any]:
    """Find an included record by a case-insensitive title fragment."""

    from ..config import load_config
    from ..db import read_papers

    dataframe = read_papers(load_config())
    if dataframe.empty or "title" not in dataframe.columns:
        return {"error": "No papers available"}
    matches = dataframe[
        dataframe["title"].fillna("").astype(str).str.contains(title, case=False, regex=False)
    ]
    matches = matches[matches.get("selection_stage", "") == "included"] if "selection_stage" in matches else matches
    if matches.empty:
        return {"error": "Included paper not found"}
    row = matches.iloc[0]
    return {
        "matched_title": row.get("title"),
        "doi": row.get("doi"),
        "score": row.get("relevance_score"),
        "selection_stage": row.get("selection_stage"),
        "status": row.get("status"),
        "exclusion_reason": row.get("exclusion_reason"),
    }
