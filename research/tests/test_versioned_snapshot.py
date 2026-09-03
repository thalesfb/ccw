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
    scope_ids: tuple[int, ...] = (101,),
    included_id: int = 101,
) -> tuple[Path, Path, Path]:
    papers_path = root / "papers.csv"
    with papers_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("id", "selection_stage"))
        writer.writeheader()
        writer.writerows(
            [
                {"id": 303, "selection_stage": "screening"},
                {"id": 202, "selection_stage": "eligibility"},
                {"id": included_id, "selection_stage": "included"},
            ]
        )

    summary_path = root / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "statistics": {
                    "total_papers": 4,
                    "prisma": {
                        "identification": 4,
                        "duplicates_removed": 1,
                        "screening": 3,
                        "screening_excluded": 1,
                        "eligibility": 2,
                        "eligibility_excluded": 1,
                        "included": 1,
                    },
                }
            }
        ),
        encoding="utf-8",
    )

    scope_path = root / "current_synthesis_scope.csv"
    with scope_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("study_id",))
        writer.writeheader()
        writer.writerows({"study_id": study_id} for study_id in scope_ids)
    return papers_path, summary_path, scope_path


def test_committed_snapshot_is_self_consistent() -> None:
    facts = validate_versioned_snapshot(
        papers_path=PAPERS_PATH,
        summary_path=SUMMARY_PATH,
        scope_path=SCOPE_PATH,
    )

    assert facts["papers_rows"] == sum(facts["papers_stage_counts"].values())
    assert facts["scope_rows"] == len(facts["included_ids"])
    assert facts["summary_prisma"]["included"] == facts["scope_rows"]


def test_arbitrary_coherent_snapshot_is_accepted(tmp_path: Path) -> None:
    paths = _write_fixture(tmp_path, scope_ids=(101,))

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
