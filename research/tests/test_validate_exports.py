"""Validate the versioned review snapshot without requiring the local SQLite DB."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = RESEARCH_ROOT / "exports" / "analysis" / "papers.csv"
SUMMARY_PATH = RESEARCH_ROOT / "exports" / "reports" / "summary.json"


def _load_snapshot() -> tuple[pd.DataFrame, dict]:
    assert CSV_PATH.exists(), f"Missing versioned export at {CSV_PATH}"
    assert SUMMARY_PATH.exists(), f"Missing versioned summary at {SUMMARY_PATH}"
    return pd.read_csv(CSV_PATH), json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


def test_versioned_export_partition_matches_summary() -> None:
    """The published deduplicated export must reproduce the PRISMA partition."""
    dataframe, summary = _load_snapshot()
    prisma = summary["statistics"]["prisma"]

    assert len(dataframe) == prisma["screening"]
    assert dataframe["id"].is_unique
    assert dataframe["selection_stage"].value_counts().to_dict() == {
        "screening": prisma["screening_excluded"],
        "eligibility": prisma["eligibility_excluded"],
        "included": prisma["included"],
    }
    assert int(dataframe["status"].eq("included").sum()) == prisma["included"]


def test_versioned_export_preserves_deduplication_accounting() -> None:
    """Deduplication is explicit; it must not silently disappear from reports."""
    _, summary = _load_snapshot()
    prisma = summary["statistics"]["prisma"]
    audit = summary["statistics"]["deduplication_audit"]

    assert prisma["raw_rows"] == summary["statistics"]["total_papers"]
    assert prisma["raw_rows"] - prisma["duplicates_removed"] == prisma["screening"]
    assert prisma["duplicates_removed"] == 27
    assert audit["doi"]["excess_rows"] == 25
    assert audit["url"]["excess_rows"] == 2
    assert audit["confirmed_semantic_duplicates"] == 0
