import json
import sqlite3
from pathlib import Path

import pandas as pd

from src.pipelines.validations import validate_exports_report


def _seed_database(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE papers (
                id INTEGER PRIMARY KEY,
                doi TEXT,
                selection_stage TEXT,
                status TEXT,
                year INTEGER
            )
            """
        )
        rows = [
            (1, "10.0/alpha", "included", "included", 2020),
            (2, "10.0/beta", "screening", "excluded", 2019),
            (3, "10.0/alpha", "screening", "excluded", 2018),
            (4, None, "eligibility", "excluded", 2022),
        ]
        conn.executemany(
            "INSERT INTO papers (id, doi, selection_stage, status, year) VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()


def _seed_csv(csv_path: Path) -> None:
    df = pd.DataFrame(
        [
            {
                "doi": "10.0/alpha",
                "selection_stage": "included",
                "status": "included",
                "year": 2020,
            },
            {
                "doi": "10.0/alpha",
                "selection_stage": "screening",
                "status": "excluded",
                "year": 2018,
            },
            {
                "doi": "10.0/beta",
                "selection_stage": "screening",
                "status": "excluded",
                "year": 2019,
            },
        ]
    )
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)


def _seed_summary(summary_path: Path) -> None:
    payload = {
        "statistics": {
            "total_papers": 4,
            "prisma": {"identification": 4, "included": 1},
            "selection_stages": {
                "Identificação": 4,
                "Triagem": 3,
                "Incluídos": 1,
            },
            "years": {"distribution": {"2020": 1, "2035": 2}},
        }
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(payload), encoding="utf-8")


def test_validate_exports_report_collects_metrics(tmp_path):
    db_path = tmp_path / "papers.sqlite"
    csv_path = tmp_path / "exports" / "analysis" / "papers.csv"
    summary_path = tmp_path / "exports" / "reports" / "summary.json"

    _seed_database(db_path)
    _seed_csv(csv_path)
    _seed_summary(summary_path)

    report = validate_exports_report(db_path=db_path, csv_path=csv_path, summary_path=summary_path)

    assert report["db"]["total"] == 4
    assert report["csv"]["total"] == 3
    assert report["summary"]["total_papers"] == 4
    assert report["diffs"]["total"] == {"db": 4, "csv": 3, "summary": 4}

    dup_db = report["db"].get("dup_doi", [])
    assert dup_db and dup_db[0]["doi"] == "10.0/alpha"

    dup_csv = report["samples"].get("csv_dup_doi_sample", [])
    assert dup_csv and dup_csv[0]["doi"] == "10.0/alpha"

    assert report["samples"]["summary_out_of_range_years"] == [{"year": "2035", "count": 2}]


def test_validate_exports_report_handles_missing_inputs(tmp_path):
    db_path = tmp_path / "missing.sqlite"
    csv_path = tmp_path / "missing.csv"
    summary_path = tmp_path / "missing.json"

    report = validate_exports_report(db_path=db_path, csv_path=csv_path, summary_path=summary_path)

    assert "Missing DB" in report["db"].get("error", "")
    assert "Missing CSV" in report["csv"].get("error", "")
    assert "Missing summary" in report["summary"].get("error", "")

    assert report["diffs"]["total"] == {"db": None, "csv": None, "summary": None}
    assert report["samples"]["csv_dup_doi_sample"] == []
    assert report["samples"]["db_dup_doi_sample"] == []
    assert report["samples"]["summary_out_of_range_years"] == []
