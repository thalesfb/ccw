"""Apply the approved scope adjudications to the versioned research snapshot.

This module is intentionally independent of SQLite and network state.  It
uses the committed row-level export plus the explicit decision ledger, so the
public snapshot can be regenerated without distributing the operational
database.  Applying the ledger is idempotent: a second run produces the same
population and preserves the original PRISMA identification and identity
deduplication audit.
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from ..analysis.reports import ReportGenerator
from ..analysis.visualizations import ReviewVisualizer
from ..analysis.mmat_current import CURRENT_MMAT_STUDY_IDS, load_current_synthesis_scope
from ..exports.excel import to_excel_with_filters
from ..validation.derived_assets import sync_derived_assets


RESEARCH_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_ROOT = RESEARCH_ROOT / "exports" / "analysis"
REPORT_ROOT = RESEARCH_ROOT / "exports" / "reports"
VISUALIZATION_ROOT = RESEARCH_ROOT / "exports" / "visualizations"
PAPERS_PATH = ANALYSIS_ROOT / "papers.csv"
SUMMARY_PATH = REPORT_ROOT / "summary.json"
SCOPE_PATH = RESEARCH_ROOT / "data" / "current_synthesis_scope.csv"
DECISIONS_PATH = RESEARCH_ROOT / "data" / "adjudicated_population_decisions.csv"

DECISION_FIELDS = (
    "decision_date",
    "source_snapshot_date",
    "study_id",
    "study_key",
    "decision_type",
    "previous_selection_stage",
    "previous_status",
    "final_disposition",
    "final_selection_stage",
    "final_status",
    "final_year",
    "final_synthesis_role",
    "final_empirical_mmat_applicability",
    "decision_basis",
    "evidence_source",
    "evidence_checked_on",
    "decision_status",
    "notes",
)

EXPECTED_DECISION_IDS = (14, 15, 6915, 6918, 6919, 6922, 6925, 6926)
INCLUDED_DISPOSITIONS = {"include"}
FINAL_EXCLUSION_REASONS = {
    15: "exclude_computational_centrality",
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_decisions(path: Path | str = DECISIONS_PATH) -> list[dict[str, str]]:
    """Load and validate the explicit final scope decisions."""

    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        missing = [field for field in DECISION_FIELDS if field not in fields]
        if missing:
            raise ValueError(f"{path} is missing decision fields: {missing}")
        rows = list(reader)

    ids = [int(row["study_id"]) for row in rows]
    if tuple(sorted(ids)) != EXPECTED_DECISION_IDS or len(ids) != len(set(ids)):
        raise ValueError(f"Unexpected adjudication IDs: {ids}")
    for row in rows:
        if row["decision_status"] != "approved_in_pr54":
            raise ValueError(
                f"Decision {row['study_id']} is not marked as approved by PR54"
            )
        if not row["final_selection_stage"] or not row["final_status"]:
            raise ValueError(f"Decision {row['study_id']} lacks a final state")
        if not row["decision_basis"] or not row["evidence_source"]:
            raise ValueError(f"Decision {row['study_id']} lacks evidence")
    return rows


def _normalise_text(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def _append_provenance_note(existing: object, study_id: int) -> str:
    marker = f"Adjudicação de escopo PR54 aplicada (estudo {study_id});"
    current = _normalise_text(existing)
    if marker in current:
        return current.replace(f"{marker} ver", marker).strip()
    return f"{marker} {current}".strip()


def _remove_criterion(criteria: object, criterion: str) -> str:
    values = [
        item.strip()
        for item in _normalise_text(criteria).split(";")
        if item.strip() and item.strip() != criterion
    ]
    return "; ".join(values)


def apply_adjudications(
    papers: pd.DataFrame,
    decisions: list[dict[str, str]] | None = None,
) -> pd.DataFrame:
    """Return the final row-level population after applying the decision ledger."""

    decisions = decisions or load_decisions()
    result = papers.copy()
    result["id"] = pd.to_numeric(result["id"], errors="raise").astype(int)
    by_id = {int(row["id"]): index for index, row in result.iterrows()}
    scope_by_id = {
        int(row["study_id"]): row for row in load_current_synthesis_scope()
    }

    for decision in decisions:
        study_id = int(decision["study_id"])
        if study_id not in by_id:
            raise ValueError(f"Decision {study_id} has no row in papers.csv")
        index = by_id[study_id]
        current_stage = _normalise_text(result.at[index, "selection_stage"])
        current_status = _normalise_text(result.at[index, "status"])
        allowed_previous = {
            (decision["previous_selection_stage"], decision["previous_status"]),
            (decision["final_selection_stage"], decision["final_status"]),
        }
        if "eligibility" in {
            decision["previous_selection_stage"], decision["final_selection_stage"]
        }:
            # The current export deliberately renamed this legacy operational
            # threshold stage to `prioritization`; permit replay of the older
            # adjudication ledger against that semantically equivalent label.
            allowed_previous.add(("prioritization", decision["previous_status"]))
            allowed_previous.add(("prioritization", decision["final_status"]))
        if study_id in scope_by_id:
            scope_row = scope_by_id[study_id]
            allowed_previous.add(
                (scope_row["selection_stage"], scope_row["selection_status"])
            )
        if (current_stage, current_status) not in allowed_previous:
            raise ValueError(
                f"Study {study_id} has unexpected state {(current_stage, current_status)!r}; "
                f"expected one of {sorted(allowed_previous)!r}"
            )

        result.at[index, "selection_stage"] = decision["final_selection_stage"]
        result.at[index, "status"] = decision["final_status"]
        result.at[index, "exclusion_reason"] = (
            "" if decision["final_disposition"] in INCLUDED_DISPOSITIONS
            else FINAL_EXCLUSION_REASONS.get(
                study_id, decision["final_disposition"]
            )
        )
        result.at[index, "notes"] = _append_provenance_note(
            result.at[index, "notes"], study_id
        )

        final_year = decision.get("final_year", "").strip()
        if final_year:
            result.at[index, "year"] = int(final_year)
        if decision["final_disposition"] == "exclude_temporal":
            result.at[index, "inclusion_criteria_met"] = _remove_criterion(
                result.at[index, "inclusion_criteria_met"], "year_range"
            )

    return result


def apply_current_scope_adjudications(
    papers: pd.DataFrame,
    scope: list[dict[str, str]] | None = None,
) -> pd.DataFrame:
    """Apply the current full-text, context and empirical-scope decisions.

    The source-controlled scope ledger is the current disposition authority;
    the older PR54 population ledger remains an independently replayable
    historical decision layer.
    """
    scope = scope or load_current_synthesis_scope()
    result = papers.copy()
    result["id"] = pd.to_numeric(result["id"], errors="raise").astype(int)
    by_id = {int(row["id"]): index for index, row in result.iterrows()}
    expected_ids = {int(row["study_id"]) for row in scope}
    if not expected_ids.issubset(by_id):
        raise ValueError(
            f"Scope decisions have no papers.csv rows: {sorted(expected_ids - set(by_id))}"
        )

    # The former 2,468-row `eligibility` label represented an automated
    # operational prioritization threshold, not full-text eligibility. Do not
    # relabel the shortlisted studies whose current full-text dispositions
    # also use the `eligibility` stage.
    candidate_ids = {int(row["study_id"]) for row in scope}
    operational_threshold = (
        result["selection_stage"].eq("eligibility")
        & ~result["id"].isin(candidate_ids)
    )
    result.loc[operational_threshold, "selection_stage"] = "prioritization"

    for decision in scope:
        study_id = int(decision["study_id"])
        index = by_id[study_id]
        current = (
            _normalise_text(result.at[index, "selection_stage"]),
            _normalise_text(result.at[index, "status"]),
        )
        candidate_state = ("included", "included")
        final_state = (decision["selection_stage"], decision["selection_status"])
        if current not in {candidate_state, final_state}:
            raise ValueError(
                f"Study {study_id} has unexpected state {current!r}; expected "
                f"the shortlisted state or current decision {final_state!r}"
            )
        result.at[index, "selection_stage"] = final_state[0]
        result.at[index, "status"] = final_state[1]
        result.at[index, "exclusion_reason"] = (
            "" if final_state[1] == "included" else decision["selection_reason"]
        )
        note = f"Adjudicação de escopo 2026-10-12 ({decision['record_status']});"
        existing = _normalise_text(result.at[index, "notes"])
        existing = re.sub(
            r"(?:Adjudicação de escopo \d{4}-\d{2}-\d{2} \([^)]*\)|"
            r"Adjudicação de escopo PR54 aplicada \(estudo \d+\));\s*",
            "",
            existing,
        ).strip()
        result.at[index, "notes"] = f"{note} {existing}".strip()
    return result


def apply_current_adjudications(
    papers: pd.DataFrame,
    decisions: list[dict[str, str]] | None = None,
    scope: list[dict[str, str]] | None = None,
) -> pd.DataFrame:
    """Replay historical population adjudications, then current scope decisions."""
    updated = apply_adjudications(papers, decisions)
    return apply_current_scope_adjudications(updated, scope)


def _write_analysis_exports(papers: pd.DataFrame) -> None:
    ANALYSIS_ROOT.mkdir(parents=True, exist_ok=True)
    csv_papers = papers.copy()
    for column in csv_papers.select_dtypes(include=["object", "string"]).columns:
        csv_papers[column] = csv_papers[column].map(
            lambda value: "\n".join(
                part.rstrip() for part in value.replace("\r", "").split("\n")
            )
            if isinstance(value, str)
            else value
        )
    csv_papers.to_csv(
        PAPERS_PATH,
        index=False,
        encoding="utf-8-sig",
        lineterminator="\n",
    )
    papers.to_json(
        ANALYSIS_ROOT / "papers.json",
        orient="records",
        indent=2,
        force_ascii=False,
    )
    papers.to_excel(ANALYSIS_ROOT / "papers.xlsx", index=False)
    to_excel_with_filters(
        papers,
        ANALYSIS_ROOT / "revisao_sistematica.xlsx",
    )


def _validate_scope_reconciliation(papers: pd.DataFrame) -> None:
    scope = load_current_synthesis_scope()
    by_id = {int(row["id"]): row for _, row in papers.iterrows()}
    for decision in scope:
        study_id = int(decision["study_id"])
        row = by_id[study_id]
        observed = (
            _normalise_text(row["selection_stage"]),
            _normalise_text(row["status"]),
        )
        expected = (decision["selection_stage"], decision["selection_status"])
        if observed != expected:
            raise ValueError(
                f"Scope ledger and papers.csv disagree for study {study_id}: "
                f"{expected!r} != {observed!r}"
            )


def _prisma_seed() -> dict[str, Any]:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    prisma = copy.deepcopy(summary["statistics"]["prisma"])
    required = ("identification", "duplicates_removed", "screening")
    if any(key not in prisma for key in required):
        raise ValueError("summary.json lacks the immutable PRISMA identity counts")
    return prisma


def _updated_prisma(papers: pd.DataFrame) -> dict[str, Any]:
    prisma = _prisma_seed()
    stages = papers["selection_stage"].fillna("").astype(str)
    statuses = papers["status"].fillna("").astype(str).str.lower()
    screening_excluded = int(
        ((stages == "screening") & statuses.str.contains("exclu")).sum()
    )
    prioritization_excluded = int(
        ((stages == "prioritization") & statuses.str.contains("exclu")).sum()
    )
    abstract_screening_excluded = int(
        ((stages == "abstract_screening") & statuses.str.contains("exclu")).sum()
    )
    reports_not_retrieved = int((stages == "not_retrieved").sum())
    eligibility_excluded = int(
        ((stages == "eligibility") & statuses.str.contains("exclu")).sum()
    )
    included = int((stages == "included").sum())
    screening = int(len(papers))
    prioritization = screening - screening_excluded
    shortlisted = abstract_screening_excluded + reports_not_retrieved + eligibility_excluded + included
    reports_sought = reports_not_retrieved + eligibility_excluded + included
    eligibility = eligibility_excluded + included
    identification = int(prisma["identification"])
    if identification - int(prisma["duplicates_removed"]) != screening:
        raise ValueError("Immutable identity counts no longer match papers.csv")
    if prioritization_excluded + shortlisted != prioritization:
        raise ValueError("Prioritization counts do not reconcile with the shortlisted records")
    if abstract_screening_excluded + reports_sought != shortlisted:
        raise ValueError("Abstract-screening counts do not reconcile with reports sought")
    if reports_not_retrieved + eligibility != reports_sought:
        raise ValueError("Report-retrieval counts do not reconcile with full-text assessment")

    prisma.update(
        {
            "screening": screening,
            "screening_excluded": screening_excluded,
            "prioritization": prioritization,
            "prioritization_excluded": prioritization_excluded,
            "shortlisted": shortlisted,
            "abstract_screening_excluded": abstract_screening_excluded,
            "reports_sought": reports_sought,
            "reports_not_retrieved": reports_not_retrieved,
            "eligibility": eligibility,
            "eligibility_excluded": eligibility_excluded,
            "included": included,
        }
    )
    prisma["stage_percentages"] = {
        "screening_excluded_of_identification": round(
            100 * screening_excluded / identification, 2
        ),
        "screening_advanced_of_identification": round(
            100 * prioritization / identification, 2
        ),
        "screening_excluded_of_screened_records": round(
            100 * screening_excluded / screening, 2
        ),
        "prioritization_passed_of_screened_records": round(
            100 * prioritization / screening, 2
        ),
        "prioritization_excluded_of_prioritization": round(
            100 * prioritization_excluded / prioritization, 2
        ),
        "shortlisted_of_prioritization": round(
            100 * shortlisted / prioritization, 2
        ),
        "abstract_screening_excluded_of_shortlist": round(
            100 * abstract_screening_excluded / shortlisted, 2
        ),
        "reports_not_retrieved_of_reports_sought": round(
            100 * reports_not_retrieved / reports_sought, 2
        ),
        "full_text_excluded_of_assessed": round(
            100 * eligibility_excluded / eligibility, 2
        ),
        "included_of_assessed": round(100 * included / eligibility, 2),
        "eligibility_excluded_of_eligibility": round(
            100 * eligibility_excluded / eligibility, 2
        ),
        "included_of_eligibility": round(100 * included / eligibility, 2),
        "included_of_identification": round(100 * included / identification, 2),
    }
    audit = prisma.get("deduplication_audit", {})
    prisma["_audit"] = {
        "raw_included_total": included,
        "duplicates_marked_included": 0,
        "included_without_operational_flag": included,
        "expected_delta": 0,
        "actual_delta": 0,
    }
    prisma["deduplication_audit"] = audit
    return prisma


def _regenerate_reports(papers: pd.DataFrame, prisma: dict[str, Any]) -> None:
    generator = ReportGenerator(REPORT_ROOT)
    generator.generate_summary_report(papers, prisma, config={})
    generator.generate_papers_report(papers, "included")
    generator.generate_gap_analysis(papers)
    VISUALIZATION_ROOT.mkdir(parents=True, exist_ok=True)
    ReviewVisualizer(VISUALIZATION_ROOT).generate_all_visualizations(papers, prisma)
    sync_derived_assets()


def regenerate() -> dict[str, Any]:
    """Apply decisions and regenerate versioned derived artifacts."""

    decisions = load_decisions()
    papers = pd.read_csv(PAPERS_PATH, encoding="utf-8-sig")
    updated = apply_current_adjudications(papers, decisions)
    _validate_scope_reconciliation(updated)
    _write_analysis_exports(updated)
    prisma = _updated_prisma(updated)
    _regenerate_reports(updated, prisma)
    return {
        "papers_rows": len(updated),
        "stage_counts": dict(
            sorted(Counter(updated["selection_stage"].astype(str)).items())
        ),
        "included_ids": sorted(
            updated.loc[updated["selection_stage"] == "included", "id"]
            .astype(int)
            .tolist()
        ),
        "prisma": prisma,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the current final states without rewriting artifacts.",
    )
    args = parser.parse_args()
    decisions = load_decisions()
    papers = pd.read_csv(PAPERS_PATH, encoding="utf-8-sig")
    updated = apply_current_adjudications(papers, decisions)
    _validate_scope_reconciliation(updated)
    facts = {
        "papers_rows": len(updated),
        "stage_counts": dict(
            sorted(Counter(updated["selection_stage"].astype(str)).items())
        ),
        "included_ids": sorted(
            updated.loc[updated["selection_stage"] == "included", "id"]
            .astype(int)
            .tolist()
        ),
        "prisma": _updated_prisma(updated),
    }
    expected = {
        "papers_rows": 11877,
        "stage_counts": {
            "abstract_screening": 1,
            "eligibility": 1,
            "included": 12,
            "not_retrieved": 4,
            "prioritization": 2468,
            "screening": 9391,
        },
        "included_ids": list(CURRENT_MMAT_STUDY_IDS),
    }
    if facts["papers_rows"] != expected["papers_rows"]:
        raise SystemExit(f"Unexpected row count: {facts['papers_rows']}")
    if facts["stage_counts"] != expected["stage_counts"]:
        raise SystemExit(f"Unexpected stage counts: {facts['stage_counts']}")
    if facts["included_ids"] != expected["included_ids"]:
        raise SystemExit(f"Unexpected included IDs: {facts['included_ids']}")
    if args.check:
        print(json.dumps(facts, ensure_ascii=False, indent=2))
        return
    regenerate()
    print(json.dumps(facts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
