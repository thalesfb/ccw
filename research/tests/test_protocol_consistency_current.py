"""Regression tests for the current protocol rather than the historical corpus.

PR #23 contained useful protocol checks, but its expectations were tied to the
17-study historical snapshot.  These tests preserve the valid intent of those
checks while asserting the reconciled 16-study snapshot and the corrected token
boundaries in the selector/scoring implementation.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from src.processing.scoring import extract_techniques
from src.processing.selection import PRISMASelector
from src.search_terms import generate_search_queries


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = RESEARCH_ROOT / "exports" / "reports" / "summary.json"
PAPERS_PATH = RESEARCH_ROOT / "exports" / "analysis" / "papers.csv"
PROTOCOL_PATH = RESEARCH_ROOT / "data" / "current_eligibility_protocol.csv"


def test_canonical_search_strategy_remains_72_queries() -> None:
    queries = generate_search_queries()

    assert len(queries) == 72
    assert len([query for query in queries if query.startswith(("mathematics ", "math "))]) == 48
    assert len([query for query in queries if query.startswith("matemática ")]) == 24


def test_ai_token_does_not_match_substrings_inside_ordinary_words() -> None:
    selector = PRISMASelector()
    false_positive_texts = [
        "This study aims to examine formative assessment in mathematics.",
        "Teacher training supports mathematics assessment in rural schools.",
        "Ghanaian students studied geometry with cooperative learning.",
    ]

    for abstract in false_positive_texts:
        meets, criteria = selector.apply_inclusion_criteria(
            {"title": "Mathematics education study", "abstract": abstract, "year": 2024}
        )
        assert "computational_techniques" not in criteria
        assert meets is False
        assert "machine_learning" not in extract_techniques(abstract)

    explicit_ai = "Artificial intelligence and machine learning for mathematics education."
    meets, criteria = selector.apply_inclusion_criteria(
        {"title": "Mathematics education", "abstract": explicit_ai, "year": 2024}
    )
    assert "computational_techniques" in criteria
    assert meets is True
    assert "machine_learning" in extract_techniques(explicit_ai)


def test_current_summary_preserves_full_prisma_flow_and_nonzero_identity_audit() -> None:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    prisma = summary["statistics"]["prisma"]

    assert prisma["identification"] == 11904
    assert prisma["duplicates_removed"] == 27
    assert prisma["screening"] == 11877
    assert prisma["screening_excluded"] == 9391
    assert prisma["eligibility"] == 2486
    assert prisma["eligibility_excluded"] == 2470
    assert prisma["included"] == 16
    assert prisma["stage_percentages"] == {
        "screening_excluded_of_identification": 78.89,
        "screening_advanced_of_identification": 20.88,
        "eligibility_excluded_of_eligibility": 99.36,
        "included_of_eligibility": 0.64,
        "included_of_identification": 0.13,
    }
    assert prisma["deduplication_audit"]["doi"]["excess_rows"] == 25
    assert prisma["deduplication_audit"]["url"]["excess_rows"] == 2
    assert prisma["deduplication_audit"]["confirmed_semantic_duplicates"] == 0


def test_current_export_has_exactly_the_operational_sixteen_ids() -> None:
    with PAPERS_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    included_ids = {
        int(row["id"])
        for row in rows
        if row.get("selection_stage") == "included"
    }

    assert included_ids == {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        6916,
        6917,
        6918,
        6920,
        6921,
        6923,
    }


def test_current_eligibility_protocol_makes_adjudication_gates_explicit() -> None:
    with PROTOCOL_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert {row["criterion_id"] for row in rows} == {
        "domain_centrality",
        "computational_centrality",
        "empirical_completion",
        "mathematics_outcome_specificity",
        "publication_and_source",
    }
    assert all(row["if_unresolved"] == "hold" for row in rows)
    assert all(row["evidence_required"] for row in rows)
