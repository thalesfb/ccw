"""Tests for cross-artifact versioned snapshot validation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from src.validation.versioned_snapshot import (
    PAPERS_PATH,
    SCOPE_PATH,
    SUMMARY_PATH,
    validate_versioned_snapshot,
)


def _write_fixture(
    root: Path,
    *,
    scope_ids: tuple[int, ...] = (101, 202),
    included_id: int = 101,
) -> tuple[Path, Path, Path]:
    papers_path = root / "papers.csv"
    with papers_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("id", "selection_stage", "status", "year"))
        writer.writeheader()
        writer.writerows(
            [
                {"id": 303, "selection_stage": "screening", "status": "excluded", "year": 2020},
                {"id": 202, "selection_stage": "not_retrieved", "status": "not_retrieved", "year": 2021},
                {"id": included_id, "selection_stage": "included", "status": "included", "year": 2022},
            ]
        )

    summary_path = root / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "statistics": {
                    "total_papers": 4,
                    "years": {
                        "min": 2020,
                        "max": 2022,
                        "distribution": {"2020": 1, "2021": 1, "2022": 1},
                        "out_of_range_count": 0,
                    },
                    "prisma": {
                        "identification": 4,
                        "duplicates_removed": 1,
                        "screening": 3,
                        "screening_excluded": 1,
                        "prioritization": 2,
                        "prioritization_excluded": 0,
                        "shortlisted": 2,
                        "abstract_screening_excluded": 0,
                        "reports_sought": 2,
                        "reports_not_retrieved": 1,
                        "eligibility": 1,
                        "eligibility_excluded": 0,
                        "included": 1,
                    },
                }
            }
        ),
        encoding="utf-8",
    )

    scope_path = root / "current_synthesis_scope.csv"
    with scope_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "study_id", "record_status", "synthesis_role",
                "empirical_mmat_applicability", "selection_stage", "selection_status",
            ),
        )
        writer.writeheader()
        writer.writerows(
            {
                "study_id": study_id,
                "record_status": "included_empirical_core" if study_id == included_id else "awaiting_full_text",
                "synthesis_role": "empirical_evidence" if study_id == included_id else "pending_full_text",
                "empirical_mmat_applicability": "applicable" if study_id == included_id else "pending_full_text",
                "selection_stage": "included" if study_id == included_id else "not_retrieved",
                "selection_status": "included" if study_id == included_id else "not_retrieved",
            }
            for study_id in scope_ids
        )
    return papers_path, summary_path, scope_path


def test_committed_snapshot_is_self_consistent() -> None:
    facts = validate_versioned_snapshot(
        papers_path=PAPERS_PATH,
        summary_path=SUMMARY_PATH,
        scope_path=SCOPE_PATH,
    )

    assert facts["papers_rows"] == sum(facts["papers_stage_counts"].values())
    assert facts["scope_rows"] == facts["summary_prisma"]["shortlisted"]
    assert facts["summary_prisma"]["included"] == len(facts["included_ids"])


def test_arbitrary_coherent_snapshot_is_accepted(tmp_path: Path) -> None:
    paths = _write_fixture(tmp_path, scope_ids=(101, 202))

    facts = validate_versioned_snapshot(
        papers_path=paths[0], summary_path=paths[1], scope_path=paths[2]
    )

    assert facts["included_ids"] == [101]


def test_summary_drift_is_rejected(tmp_path: Path) -> None:
    papers_path, summary_path, scope_path = _write_fixture(tmp_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["statistics"]["prisma"]["included"] = 2
    summary_path.write_text(json.dumps(summary), encoding="utf-8")

    try:
        validate_versioned_snapshot(
            papers_path=papers_path,
            summary_path=summary_path,
            scope_path=scope_path,
        )
    except ValueError as exc:
        assert "inconsistent eligibility relation" in str(exc)
    else:
        raise AssertionError("summary drift was accepted")


def test_scope_drift_is_rejected_against_papers(tmp_path: Path) -> None:
    paths = _write_fixture(tmp_path, scope_ids=(999,))

    try:
        validate_versioned_snapshot(
            papers_path=paths[0], summary_path=paths[1], scope_path=paths[2]
        )
    except ValueError as exc:
        assert "study IDs disagree" in str(exc)
    else:
        raise AssertionError("scope drift was accepted")


def test_year_distribution_drift_is_rejected(tmp_path: Path) -> None:
    paths = _write_fixture(tmp_path)
    summary = json.loads(paths[1].read_text(encoding="utf-8"))
    summary["statistics"]["years"]["distribution"]["2020"] = 2
    paths[1].write_text(json.dumps(summary), encoding="utf-8")

    try:
        validate_versioned_snapshot(
            papers_path=paths[0], summary_path=paths[1], scope_path=paths[2]
        )
    except ValueError as exc:
        assert "year distribution" in str(exc)
    else:
        raise AssertionError("year distribution drift was accepted")


def test_out_of_range_rows_are_accounted_for(tmp_path: Path) -> None:
    paths = _write_fixture(tmp_path)
    with paths[0].open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows[0]["year"] = "2019"
    summary = json.loads(paths[1].read_text(encoding="utf-8"))
    summary["statistics"]["years"]["distribution"]["2020"] = 0
    paths[1].write_text(json.dumps(summary), encoding="utf-8")
    with paths[0].open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("id", "selection_stage", "status", "year"))
        writer.writeheader()
        writer.writerows(rows)

    try:
        validate_versioned_snapshot(
            papers_path=paths[0], summary_path=paths[1], scope_path=paths[2]
        )
    except ValueError as exc:
        assert "out-of-range" in str(exc)
    else:
        raise AssertionError("out-of-range row drift was accepted")
