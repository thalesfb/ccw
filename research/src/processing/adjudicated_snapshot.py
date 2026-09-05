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
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from ..analysis.reports import ReportGenerator
from ..analysis.visualizations import ReviewVisualizer
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


def _build_scope(
    papers: pd.DataFrame,
    decisions: list[dict[str, str]],
) -> None:
    existing = _read_csv(SCOPE_PATH)
    existing_by_id = {int(row["study_id"]): row for row in existing}
    decision_by_id = {int(row["study_id"]): row for row in decisions}
    scope_rows: list[dict[str, str]] = []
    fields = [
        "snapshot_date",
        "study_id",
        "study_key",
        "operational_inclusion",
        "synthesis_role",
        "empirical_mmat_applicability",
        "disposition_note",
    ]

    for raw_id in papers.loc[
        papers["selection_stage"] == "included", "id"
    ].astype(int).tolist():
        old = existing_by_id.get(raw_id, {})
        decision = decision_by_id.get(raw_id, {})
        row = {
            "snapshot_date": "2026-09-03",
            "study_id": str(raw_id),
            "study_key": old.get("study_key") or decision.get("study_key", ""),
            "operational_inclusion": "retained_in_current_snapshot",
            "synthesis_role": old.get("synthesis_role")
            or decision.get("final_synthesis_role", "empirical_evidence"),
            "empirical_mmat_applicability": old.get("empirical_mmat_applicability")
            or decision.get("final_empirical_mmat_applicability", "applicable"),
            "disposition_note": (
                "Retained after the 2026-09-03 scope adjudication; final MMAT "
                "assessment remains provisional."
            ),
        }
        scope_rows.append(row)

    scope_rows.sort(key=lambda row: int(row["study_id"]))
    with SCOPE_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(scope_rows)


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
    eligibility_excluded = int(
        ((stages == "eligibility") & statuses.str.contains("exclu")).sum()
    )
    included = int((stages == "included").sum())
    eligibility = int(stages.isin({"eligibility", "included"}).sum())
    screening = int(len(papers))
    identification = int(prisma["identification"])
    if identification - int(prisma["duplicates_removed"]) != screening:
        raise ValueError("Immutable identity counts no longer match papers.csv")

    prisma.update(
        {
            "screening": screening,
            "screening_excluded": screening_excluded,
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
            100 * eligibility / identification, 2
        ),
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
    updated = apply_adjudications(papers, decisions)
    _write_analysis_exports(updated)
    _build_scope(updated, decisions)
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
    updated = apply_adjudications(papers, decisions)
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
        "stage_counts": {"screening": 9391, "eligibility": 2468, "included": 18},
        "included_ids": [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 6915, 6916, 6917,
            6919, 6920, 6921, 6923,
        ],
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
