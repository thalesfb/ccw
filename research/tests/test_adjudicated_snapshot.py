from __future__ import annotations

import pandas as pd

from src.processing.adjudicated_snapshot import (
    EXPECTED_DECISION_IDS,
    PAPERS_PATH,
    apply_adjudications,
    load_decisions,
)


def test_approved_decision_ledger_covers_the_population_changes() -> None:
    decisions = load_decisions()

    assert tuple(int(row["study_id"]) for row in decisions) == EXPECTED_DECISION_IDS
    assert all(row["decision_status"] == "approved_in_pr54" for row in decisions)
    assert [row["final_disposition"] for row in decisions].count("include") == 3
    assert [row["final_disposition"] for row in decisions].count("exclude_temporal") == 1


def test_adjudicated_export_is_idempotent_and_has_expected_stage_counts() -> None:
    papers = pd.read_csv(PAPERS_PATH, encoding="utf-8-sig")
    replayed = apply_adjudications(papers)

    assert len(replayed) == 11877
    assert replayed["selection_stage"].value_counts().to_dict() == {
        "screening": 9391,
        "eligibility": 2468,
        "included": 18,
    }
    included_ids = sorted(
        replayed.loc[replayed["selection_stage"] == "included", "id"]
        .astype(int)
        .tolist()
    )
    assert included_ids == [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 6915, 6916, 6917,
        6919, 6920, 6921, 6923,
    ]

    row_6918 = replayed.loc[replayed["id"] == 6918].iloc[0]
    assert int(row_6918["year"]) == 2014
    assert row_6918["selection_stage"] == "eligibility"
    assert row_6918["exclusion_reason"] == "exclude_temporal"
    assert row_6918["status"] == "excluded"
