"""Tests for criterion-level MMAT 2018 appraisal support."""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from src.analysis.mmat_assessment import (
    EXPECTED_COLUMNS,
    VALID_RESPONSES,
    build_results_dataframe,
    classify_study_design,
    export_csv,
    export_latex_table,
    load_assessments,
    match_assessments_to_papers,
    summarize_criteria,
    update_database_with_assessments,
)


def _assessment(**overrides):
    row = {
        "ID": "Study2026_001",
        "Title": "A Study About Mathematics Learning",
        "Authors": "Ana Silva et al.",
        "Year": 2026,
        "Design": "quantitative_descriptive",
        "Q1": "Y",
        "Q2": "N",
        "Q3": "CT",
        "Q4": "Y",
        "Q5": "Y",
        "AssessmentBasis": "Full text",
        "ReviewerRole": "Single reviewer",
        "Limitations": "Single-site study with incomplete reporting",
    }
    row.update(overrides)
    return row


def _database(path: Path, rows):
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE papers (
                id INTEGER PRIMARY KEY,
                title TEXT,
                authors TEXT,
                year INTEGER,
                selection_stage TEXT,
                notes TEXT,
                updated_at TEXT
            )
            """
        )
        conn.executemany(
            """
            INSERT INTO papers
                (id, title, authors, year, selection_stage, notes)
            VALUES (?, ?, ?, ?, 'included', ?)
            """,
            rows,
        )
        conn.commit()


class TestCanonicalData:
    def test_loads_all_17_assessments(self):
        rows = load_assessments()
        assert len(rows) == 17
        assert len({row["ID"] for row in rows}) == 17

    def test_uses_criterion_level_columns(self):
        rows = load_assessments()
        assert list(rows[0]) == EXPECTED_COLUMNS
        assert "Score" not in rows[0]
        assert "Quality" not in rows[0]

    def test_responses_and_provenance_are_valid(self):
        for row in load_assessments():
            assert {row[key] for key in ("Q1", "Q2", "Q3", "Q4", "Q5")} <= VALID_RESPONSES
            assert row["AssessmentBasis"]
            assert row["ReviewerRole"]
            assert row["Limitations"]

    def test_rejects_invalid_response(self, tmp_path):
        path = tmp_path / "invalid.csv"
        row = _assessment(Q1="MAYBE")
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=EXPECTED_COLUMNS)
            writer.writeheader()
            writer.writerow(row)
        with pytest.raises(ValueError, match="Invalid response"):
            load_assessments(path, expected_count=1)


class TestMatching:
    def test_matches_title_year_and_first_author(self, tmp_path):
        db = tmp_path / "papers.db"
        _database(
            db,
            [
                (
                    1,
                    "A Study About Mathematics Learning",
                    json.dumps(["Ana Silva", "João Souza"]),
                    2026,
                    "{}",
                )
            ],
        )
        results = match_assessments_to_papers(str(db), [_assessment()])
        assert len(results) == 1
        assert results[0]["db_id"] == 1

    def test_missing_match_fails_closed(self, tmp_path):
        db = tmp_path / "papers.db"
        _database(db, [])
        with pytest.raises(ValueError, match="found 0"):
            match_assessments_to_papers(str(db), [_assessment()])

    def test_ambiguous_match_fails_closed(self, tmp_path):
        db = tmp_path / "papers.db"
        repeated = (
            "A Study About Mathematics Learning",
            json.dumps(["Ana Silva"]),
            2026,
            "{}",
        )
        _database(db, [(1, *repeated), (2, *repeated)])
        with pytest.raises(ValueError, match="found 2"):
            match_assessments_to_papers(str(db), [_assessment()])


class TestExports:
    def test_dataframe_has_no_score_or_quality(self):
        result = {
            "assessment_key": "Study2026_001",
            "full_title": "A Study About Mathematics Learning",
            "authors": "Ana Silva et al.",
            "year": 2026,
            "design": "quantitative_descriptive",
            "criteria": {"Q1": "Y", "Q2": "N", "Q3": "CT", "Q4": "Y", "Q5": "Y"},
            "assessment_basis": "Full text",
            "reviewer_role": "Single reviewer",
            "limitations": "Single-site study",
        }
        frame = build_results_dataframe([result])
        assert list(frame.columns) == EXPECTED_COLUMNS
        assert "Score" not in frame
        assert "Quality" not in frame

    def test_csv_export_is_deterministic(self, tmp_path):
        frame = pd.DataFrame([_assessment()], columns=EXPECTED_COLUMNS)
        first = tmp_path / "first.csv"
        second = tmp_path / "second.csv"
        export_csv(frame, first)
        export_csv(frame, second)
        assert first.read_bytes() == second.read_bytes()

    def test_latex_export_has_eight_columns_and_no_score(self, tmp_path):
        frame = pd.DataFrame([_assessment()], columns=EXPECTED_COLUMNS)
        output = tmp_path / "mmat.tex"
        export_latex_table(frame, output)
        content = output.read_text(encoding="utf-8")
        assert r"\multicolumn{8}" in content
        assert "Score" not in content
        assert "Qualidade" not in content
        assert "ND" in content


class TestDatabaseUpdate:
    def test_replaces_legacy_score_fields(self, tmp_path):
        db = tmp_path / "papers.db"
        legacy_notes = json.dumps({"mmat_score": 4, "mmat_quality": "Alta", "keep": True})
        _database(
            db,
            [
                (
                    1,
                    "A Study About Mathematics Learning",
                    json.dumps(["Ana Silva"]),
                    2026,
                    legacy_notes,
                )
            ],
        )
        result = {
            "db_id": 1,
            "design": "quantitative_descriptive",
            "criteria": {"Q1": "Y", "Q2": "N", "Q3": "CT", "Q4": "Y", "Q5": "Y"},
            "assessment_basis": "Full text",
            "reviewer_role": "Single reviewer",
            "limitations": "Single-site study",
        }
        assert update_database_with_assessments(str(db), [result]) == 1
        with sqlite3.connect(db) as conn:
            notes = json.loads(conn.execute("SELECT notes FROM papers").fetchone()[0])
        assert notes["keep"] is True
        assert notes["mmat_criteria"]["Q3"] == "CT"
        assert "mmat_score" not in notes
        assert "mmat_quality" not in notes


class TestSummariesAndClassification:
    def test_summary_preserves_each_response_type(self):
        results = [
            {"criteria": {"Q1": "Y", "Q2": "N", "Q3": "CT", "Q4": "Y", "Q5": "Y"}},
            {"criteria": {"Q1": "N", "Q2": "N", "Q3": "Y", "Q4": "CT", "Q5": "Y"}},
        ]
        summary = summarize_criteria(results)
        assert summary["Q1"] == {"Y": 1, "N": 1, "CT": 0}
        assert summary["Q3"] == {"Y": 1, "N": 0, "CT": 1}

    @pytest.mark.parametrize(
        ("title", "abstract", "expected"),
        [
            ("Mixed method study", "", "mixed_methods"),
            ("", "Qualitative interview study", "qualitative"),
            ("Randomized controlled trial", "", "quantitative_randomized"),
            ("", "Quasi-experimental design", "quantitative_nonrandomized"),
            ("Machine learning prediction", "Data mining", "quantitative_descriptive"),
        ],
    )
    def test_design_classification(self, title, abstract, expected):
        assert classify_study_design(title, abstract) == expected
