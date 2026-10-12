"""Regression tests for the current protocol rather than the historical corpus.

PR #23 contained useful protocol checks, but its expectations were tied to the
17-study historical snapshot.  These tests preserve the valid intent of those
checks while asserting the adjudicated 18-study snapshot and the corrected token
boundaries in the selector/scoring implementation.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from src.processing.scoring import extract_techniques
from src.processing.selection import PRISMASelector
from src.search_terms import generate_search_queries


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = RESEARCH_ROOT / "exports" / "reports" / "summary.json"
PAPERS_PATH = RESEARCH_ROOT / "exports" / "analysis" / "papers.csv"
PROTOCOL_PATH = RESEARCH_ROOT / "data" / "current_eligibility_protocol.csv"
SYNTHESIS_SCOPE_PATH = RESEARCH_ROOT / "data" / "current_synthesis_scope.csv"
PRISMA_RECONCILIATION_PATH = RESEARCH_ROOT / "data" / "prisma_population_reconciliation.csv"
REFERENCE_AUDIT_PATH = RESEARCH_ROOT / "data" / "reference_audit.csv"
TCC_REVIEW_PATH = RESEARCH_ROOT.parent / "results" / "tcc" / "conteudo" / "resultadosesperados.tex"


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
    assert prisma["prioritization"] == 2486
    assert prisma["prioritization_excluded"] == 2468
    assert prisma["shortlisted"] == 18
    assert prisma["abstract_screening_excluded"] == 1
    assert prisma["reports_sought"] == 17
    assert prisma["reports_not_retrieved"] == 4
    assert prisma["eligibility"] == 13
    assert prisma["eligibility_excluded"] == 1
    assert prisma["included"] == 12
    assert prisma["stage_percentages"] == {
        "screening_excluded_of_identification": 78.89,
        "screening_advanced_of_identification": 20.88,
        "screening_excluded_of_screened_records": 79.07,
        "prioritization_passed_of_screened_records": 20.93,
        "prioritization_excluded_of_prioritization": 99.28,
        "shortlisted_of_prioritization": 0.72,
        "abstract_screening_excluded_of_shortlist": 5.56,
        "reports_not_retrieved_of_reports_sought": 23.53,
        "full_text_excluded_of_assessed": 7.69,
        "included_of_assessed": 92.31,
        "eligibility_excluded_of_eligibility": 7.69,
        "included_of_eligibility": 92.31,
        "included_of_identification": 0.1,
    }
    assert prisma["deduplication_audit"]["doi"]["excess_rows"] == 25
    assert prisma["deduplication_audit"]["url"]["excess_rows"] == 2
    assert prisma["deduplication_audit"]["confirmed_semantic_duplicates"] == 0


def test_prisma_reconciliation_uses_the_current_scope_and_mmat_denominator() -> None:
    with PRISMA_RECONCILIATION_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    current = {
        row["metric"]: int(row["value"])
        for row in rows
        if row["snapshot_date"] == "2026-10-12"
    }

    assert current["reports_sought"] == 17
    assert current["reports_not_retrieved"] == 4
    assert current["reports_assessed_at_full_text"] == 13
    assert current["full_text_scope_exclusions"] == 1
    assert current["empirical_studies_included"] == 12
    assert current["current_mmat_empirical_denominator"] == 12


def test_current_export_has_exactly_the_adjudicated_empirical_core_ids() -> None:
    with PAPERS_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    included_ids = {
        int(row["id"])
        for row in rows
        if row.get("selection_stage") == "included"
    }

    assert included_ids == {
        2,
        3,
        4,
        6,
        7,
        8,
        14,
        6915,
        6916,
        6917,
        6919,
        6920,
    }


def test_current_evidence_ledgers_have_consistent_csv_rows() -> None:
    for path in (SYNTHESIS_SCOPE_PATH, REFERENCE_AUDIT_PATH):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))

        assert rows
        expected_width = len(rows[0])
        malformed_rows = [index for index, row in enumerate(rows[1:], start=2) if len(row) != expected_width]
        assert malformed_rows == [], f"{path.name} has malformed CSV rows: {malformed_rows}"


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


def test_tcc_review_table_distinguishes_all_shortlisted_records_by_stage() -> None:
    manuscript = TCC_REVIEW_PATH.read_text(encoding="utf-8")
    table = manuscript.split(r"\begin{longtable}", maxsplit=1)[1].split(
        r"\end{longtable}", maxsplit=1
    )[0]
    reference_keys = set(re.findall(r"\\citeonline\{([^}]+)\}", table))

    assert len(reference_keys) == 18
    for reference_key in {
        "Implementation2025_000",
        "Math2021_001",
        "He2025_6915",
        "Villegas2025_6916",
        "Multimodels2020_002",
        "Analysis2022_003",
        "Ozseven2026_6917",
        "Design2025_004",
        "Innovative2023_005",
        "Identifying2017_006",
        "Machine2019_007",
        "Computational2017_008",
        "Machine2024_009",
        "UniversityMathematics2026_6919",
        "Echeveria2025_6920",
        "Enhancing2025_012",
        "Imperatrice2025_6921",
        "Zeng2025_6923",
    }:
        assert reference_key in reference_keys

    pending_rows = [
        line for line in table.splitlines()
        if line.startswith(r"\citeonline") and "Pendente:" in line
    ]
    assert len(pending_rows) == 4
    assert all("MMAT não aplicado" in line for line in pending_rows)
    for reference_key in {
        "Math2021_001",
        "Design2025_004",
        "Machine2024_009",
        "Zeng2025_6923",
    }:
        assert any(
            f"\\citeonline{{{reference_key}}}" in line for line in pending_rows
        )
    assert "excluído após resumo" in table.lower()
    assert "excluído da síntese empírica após texto completo" in table.lower()
    assert "não apresentar resultados empíricos concluídos" in table.lower()
