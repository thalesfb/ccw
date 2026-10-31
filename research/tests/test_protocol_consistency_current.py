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
SELECTION_AMENDMENT_PATH = RESEARCH_ROOT / "data" / "selection_protocol_amendment_2026-10-31.json"
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
    assert prisma["duplicates_removed"] == 29
    assert prisma["screening"] == 11875
    assert prisma["screening_excluded"] == 9393
    assert prisma["prioritization"] == 2482
    assert prisma["prioritization_excluded"] == 2464
    assert prisma["shortlisted"] == 18
    assert prisma["abstract_screening_excluded"] == 1
    assert prisma["reports_sought"] == 17
    assert prisma["reports_not_retrieved"] == 1
    assert prisma["eligibility"] == 16
    assert prisma["eligibility_excluded"] == 1
    assert prisma["included"] == 15
    assert prisma["stage_percentages"] == {
        "screening_excluded_of_identification": 78.91,
        "screening_advanced_of_identification": 20.85,
        "screening_excluded_of_screened_records": 79.1,
        "prioritization_passed_of_screened_records": 20.9,
        "prioritization_excluded_of_prioritization": 99.27,
        "shortlisted_of_prioritization": 0.73,
        "abstract_screening_excluded_of_shortlist": 5.56,
        "reports_not_retrieved_of_reports_sought": 5.88,
        "full_text_excluded_of_assessed": 6.25,
        "included_of_assessed": 93.75,
        "eligibility_excluded_of_eligibility": 6.25,
        "included_of_eligibility": 93.75,
        "included_of_identification": 0.13,
    }
    assert prisma["deduplication_audit"]["doi"]["excess_rows"] == 25
    assert prisma["deduplication_audit"]["url"]["excess_rows"] == 2
    assert prisma["deduplication_audit"]["deterministic_identity_duplicate_rows"] == 27
    assert prisma["deduplication_audit"]["adjudicated_same_report_duplicate_rows"] == 2
    assert prisma["deduplication_audit"]["confirmed_semantic_duplicates"] == 0


def test_prisma_reconciliation_uses_the_current_scope_and_mmat_denominator() -> None:
    with PRISMA_RECONCILIATION_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    flow = {
        row["metric"]: int(row["value"])
        for row in rows
        if row["snapshot_date"] == "2026-10-14"
    }
    latest_scope = {
        row["metric"]: int(row["value"])
        for row in rows
        if row["snapshot_date"] == "2026-10-14"
    }

    assert flow["reports_sought"] == 17
    assert flow["reports_not_retrieved"] == 1
    assert flow["reports_assessed_at_full_text"] == 16
    assert flow["full_text_scope_exclusions"] == 1
    assert flow["empirical_studies_included"] == 15
    assert latest_scope["empirical_studies_included"] == 15
    assert latest_scope["current_mmat_empirical_denominator"] == 14


def test_latest_prisma_reconciliation_is_labeled_historical_until_reapplication() -> None:
    with PRISMA_RECONCILIATION_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    latest = [row for row in rows if row["snapshot_date"] == "2026-10-31"]
    amendment = json.loads(SELECTION_AMENDMENT_PATH.read_text(encoding="utf-8"))

    assert len(latest) == 10
    assert {
        row["status"] for row in latest
    } == {"historical_snapshot_reconciled_pending_reapplication"}
    assert amendment["post_decision_data_reconciliation"]["flow_status"] == (
        "historical_snapshot_reconciled_pending_reapplication"
    )
    assert amendment["post_decision_data_reconciliation"]["selection_reapplication_complete"] is False
    interpretation = amendment["post_decision_data_reconciliation"]["interpretation"]
    assert "duplicates are counted before screening" in interpretation
    assert "not a post-amendment corpus" in interpretation


def test_current_export_has_exactly_the_adjudicated_empirical_core_ids() -> None:
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
        10,
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


def test_approved_threshold_amendment_uses_score_only_for_ordering() -> None:
    amendment = json.loads(SELECTION_AMENDMENT_PATH.read_text(encoding="utf-8"))

    assert amendment["decision_date"] == "2026-10-31"
    assert amendment["status"] == "approved_pending_reapplication"
    assert amendment["eligibility_criteria_changed"] is False
    assert amendment["scope_refinement_adopted"] is False
    assert amendment["search_reprocessed"] is False
    assert "orders the reading queue only" in amendment["amended_rule"]
    assert "not an exclusion criterion" in amendment["amended_rule"]
    assert amendment["post_decision_data_reconciliation"]["flow_status"] == (
        "historical_snapshot_reconciled_pending_reapplication"
    )

    census = amendment["rationale"]["census_3_75_to_3_95"]
    assert census["examined"] == 45
    assert census["eligible"] == 13
    assert census["ineligible"] + census["uncertain"] + census["not_retrieved"] == 32

    directed = amendment["rationale"]["directed_3_50_to_3_74"]
    assert directed["examined"] == 54
    assert directed["eligible"] == 29
    assert "not representative" in directed["method"]

    sample = amendment["rationale"]["stratified_random_3_00_to_3_49"]
    assert sample["seed"] == 20261030
    assert sample["examined"] == 30
    assert sample["eligible"] == 5
    assert sample["conservative_95_percent_interval_for_eligible_records"] == [13, 356]


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
    assert len(pending_rows) == 1
    assert all("MMAT não aplicado" in line for line in pending_rows)
    for reference_key in {"Zeng2025_6923"}:
        assert any(
            f"\\citeonline{{{reference_key}}}" in line for line in pending_rows
        )
    assert "após resumo" in table.lower()
    assert "excluído da síntese empírica após texto completo" in table.lower()
    assert "não apresentar resultados empíricos concluídos" in table.lower()
