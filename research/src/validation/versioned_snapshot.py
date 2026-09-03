"""Validate the committed research snapshot using only versioned artifacts.

The validator compares the row-level ``papers.csv``, the derived PRISMA
counts in ``summary.json`` and the retained-study IDs in
``current_synthesis_scope.csv``. It deliberately does not use the local
SQLite database, network state or any manuscript/presentation artifact.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


RESEARCH_ROOT = Path(__file__).resolve().parents[2]
PAPERS_PATH = RESEARCH_ROOT / "exports" / "analysis" / "papers.csv"
SUMMARY_PATH = RESEARCH_ROOT / "exports" / "reports" / "summary.json"
SCOPE_PATH = RESEARCH_ROOT / "data" / "current_synthesis_scope.csv"

PAPERS_REQUIRED_FIELDS = ("id", "selection_stage", "year")
SCOPE_REQUIRED_FIELDS = ("study_id",)
PRISMA_FIELDS = (
    "identification",
    "duplicates_removed",
    "screening",
    "screening_excluded",
    "eligibility",
    "eligibility_excluded",
    "included",
)


class VersionedSnapshotError(ValueError):
    """Raised when versioned snapshot artifacts cannot agree."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise VersionedSnapshotError(message)


def _read_csv(path: Path, required_fields: tuple[str, ...]) -> list[dict[str, str]]:
    _require(path.is_file(), f"Missing versioned artifact: {path}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = tuple(reader.fieldnames or ())
            missing = [field for field in required_fields if field not in fields]
            _require(not missing, f"{path} is missing required columns: {missing!r}")
            return list(reader)
    except (OSError, csv.Error) as exc:
        raise VersionedSnapshotError(f"Cannot read {path}: {exc}") from exc


def _read_summary(path: Path) -> dict[str, Any]:
    _require(path.is_file(), f"Missing versioned artifact: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VersionedSnapshotError(f"Cannot read {path}: {exc}") from exc
    _require(isinstance(payload, dict), f"{path} must contain a JSON object")
    return payload


def _parse_ids(rows: list[dict[str, str]], field: str, path: Path) -> list[int]:
    identifiers: list[int] = []
    for row_number, row in enumerate(rows, start=2):
        try:
            identifiers.append(int(row[field]))
        except (KeyError, TypeError, ValueError) as exc:
            raise VersionedSnapshotError(
                f"{path} has an invalid {field} at line {row_number}: "
                f"{row.get(field)!r}"
            ) from exc
    return identifiers


def _prisma_counts(summary: dict[str, Any], path: Path) -> dict[str, int]:
    statistics = summary.get("statistics")
    _require(isinstance(statistics, dict), f"{path} lacks statistics")
    prisma = statistics.get("prisma")
    _require(isinstance(prisma, dict), f"{path} lacks statistics.prisma")

    counts: dict[str, int] = {}
    for field in PRISMA_FIELDS:
        value = prisma.get(field)
        _require(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0,
            f"{path} has an invalid statistics.prisma.{field}: {value!r}",
        )
        counts[field] = value

    total_papers = statistics.get("total_papers")
    _require(
        total_papers == counts["identification"],
        f"{path} total_papers disagrees with prisma.identification",
    )
    _require(
        counts["identification"] - counts["duplicates_removed"]
        == counts["screening"],
        f"{path} has an inconsistent identification/deduplication relation",
    )
    _require(
        counts["screening_excluded"] + counts["eligibility"]
        == counts["screening"],
        f"{path} has an inconsistent screening relation",
    )
    _require(
        counts["eligibility_excluded"] + counts["included"]
        == counts["eligibility"],
        f"{path} has an inconsistent eligibility relation",
    )
    return counts


def _temporal_accounting(
    summary: dict[str, Any],
    summary_path: Path,
    papers: list[dict[str, str]],
    papers_path: Path,
) -> dict[str, Any]:
    """Check that the reported year distribution accounts for every row.

    The committed snapshot intentionally keeps rows outside the analytical
    range in ``papers.csv`` while reporting them separately in
    ``summary.json``. The range itself is represented by the distribution
    keys, so this check remains valid when a future snapshot changes the
    protocol dates.
    """

    statistics = summary.get("statistics")
    _require(isinstance(statistics, dict), f"{summary_path} lacks statistics")
    years = statistics.get("years")
    _require(isinstance(years, dict), f"{summary_path} lacks statistics.years")
    distribution = years.get("distribution")
    _require(
        isinstance(distribution, dict) and distribution,
        f"{summary_path} has an invalid statistics.years.distribution",
    )

    reported_years: dict[int, int] = {}
    for raw_year, count in distribution.items():
        try:
            year = int(raw_year)
        except (TypeError, ValueError) as exc:
            raise VersionedSnapshotError(
                f"{summary_path} has an invalid year key: {raw_year!r}"
            ) from exc
        _require(
            isinstance(count, int) and not isinstance(count, bool) and count >= 0,
            f"{summary_path} has an invalid count for year {raw_year!r}: {count!r}",
        )
        reported_years[year] = count

    minimum = years.get("min")
    maximum = years.get("max")
    _require(
        isinstance(minimum, int) and not isinstance(minimum, bool)
        and isinstance(maximum, int)
        and not isinstance(maximum, bool)
        and minimum == min(reported_years)
        and maximum == max(reported_years),
        f"{summary_path} year bounds disagree with the reported distribution",
    )

    observed_years: Counter[int] = Counter()
    for row_number, row in enumerate(papers, start=2):
        raw_year = row.get("year")
        try:
            observed_years[int(raw_year)] += 1
        except (TypeError, ValueError) as exc:
            raise VersionedSnapshotError(
                f"{papers_path} has an invalid year at line {row_number}: "
                f"{raw_year!r}"
            ) from exc

    observed_distribution = {
        year: observed_years[year] for year in reported_years
    }
    _require(
        observed_distribution == reported_years,
        f"{papers_path} year distribution disagrees with {summary_path}",
    )
    observed_out_of_range = sum(
        count for year, count in observed_years.items() if year not in reported_years
    )
    out_of_range = years.get("out_of_range_count")
    _require(
        isinstance(out_of_range, int)
        and not isinstance(out_of_range, bool)
        and out_of_range >= 0,
        f"{summary_path} has an invalid statistics.years.out_of_range_count",
    )
    _require(
        observed_out_of_range == out_of_range,
        f"{papers_path} out-of-range year count disagrees with {summary_path}",
    )
    _require(
        sum(reported_years.values()) + out_of_range == len(papers),
        f"{summary_path} year accounting does not cover all paper rows",
    )
    return {
        "distribution": dict(sorted(reported_years.items())),
        "out_of_range_count": out_of_range,
    }


def validate_versioned_snapshot(
    *,
    papers_path: Path | str = PAPERS_PATH,
    summary_path: Path | str = SUMMARY_PATH,
    scope_path: Path | str = SCOPE_PATH,
) -> dict[str, Any]:
    """Validate cross-artifact consistency for the committed snapshot.

    No expected count, study ID, date or adjudication decision is embedded in
    this check. A different snapshot is valid when its three versioned
    artifacts agree with one another.
    """

    papers_path = Path(papers_path)
    summary_path = Path(summary_path)
    scope_path = Path(scope_path)

    papers = _read_csv(papers_path, PAPERS_REQUIRED_FIELDS)
    summary = _read_summary(summary_path)
    scope = _read_csv(scope_path, SCOPE_REQUIRED_FIELDS)

    paper_ids = _parse_ids(papers, "id", papers_path)
    _require(
        len(paper_ids) == len(set(paper_ids)),
        f"{papers_path} contains duplicate record IDs",
    )
    stage_counts = Counter(row["selection_stage"] for row in papers)
    prisma = _prisma_counts(summary, summary_path)
    temporal = _temporal_accounting(summary, summary_path, papers, papers_path)
    expected_stage_counts = {
        "screening": prisma["screening_excluded"],
        "eligibility": prisma["eligibility_excluded"],
        "included": prisma["included"],
    }
    _require(
        dict(stage_counts) == expected_stage_counts,
        f"{papers_path} stage counts disagree with {summary_path}: "
        f"{dict(stage_counts)!r} != {expected_stage_counts!r}",
    )
    _require(
        len(papers) == prisma["screening"],
        f"{papers_path} row count disagrees with {summary_path} screening",
    )

    scope_ids = _parse_ids(scope, "study_id", scope_path)
    _require(
        len(scope_ids) == len(set(scope_ids)),
        f"{scope_path} contains duplicate study IDs",
    )
    included_ids = sorted(
        int(row["id"]) for row in papers if row["selection_stage"] == "included"
    )
    _require(
        sorted(scope_ids) == included_ids,
        f"{scope_path} study IDs disagree with included IDs in {papers_path}",
    )
    _require(
        len(scope_ids) == prisma["included"],
        f"{scope_path} row count disagrees with {summary_path} included",
    )

    return {
        "papers_rows": len(papers),
        "papers_stage_counts": dict(sorted(stage_counts.items())),
        "included_ids": included_ids,
        "summary_prisma": prisma,
        "summary_years": temporal,
        "scope_rows": len(scope),
    }


def main() -> None:
    facts = validate_versioned_snapshot()
    print(
        "Validated versioned snapshot: "
        f"{facts['papers_rows']} CSV rows, "
        f"{facts['scope_rows']} scoped studies, "
        f"{facts['summary_prisma']['included']} included."
    )


if __name__ == "__main__":
    main()
