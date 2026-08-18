import pandas as pd
import pytest

from tcc_prototype.adapters.assistments import AdapterError, AssistmentsAdapter


def test_adapter_normalizes_and_orders_interactions() -> None:
    source = pd.DataFrame(
        {
            "user_id": [2, 1, 1],
            "problem_id": [30, 20, 10],
            "skill_id": ["fractions", "ratio", "fractions"],
            "order_id": [1, 2, 1],
            "correct": [0, 1, 1],
            "attempt_count": [2, 1, 1],
            "hint_count": [1, 0, 0],
            "ms_first_response": [5000, 2000, 3000],
        }
    )

    normalized, report = AssistmentsAdapter().normalize(source)

    assert normalized.columns.tolist() == [
        "student_id",
        "item_id",
        "skill_ids",
        "interaction_order",
        "timestamp",
        "correct",
        "answer",
        "attempt_count",
        "hint_count",
        "elapsed_time_ms",
        "session_id",
        "source_dataset",
        "source_row_id",
    ]
    assert normalized["student_id"].tolist() == ["1", "1", "2"]
    assert normalized["interaction_order"].tolist() == [1, 2, 1]
    assert normalized["skill_ids"].tolist() == [
        ["fractions"],
        ["ratio"],
        ["fractions"],
    ]
    assert normalized["correct"].tolist() == [True, True, False]
    assert report["input_rows"] == 3
    assert report["output_rows"] == 3
    assert report["duplicate_rows_removed"] == 0


def test_adapter_preserves_collapsed_multiskill_ids_from_corrected_export() -> None:
    source = pd.DataFrame(
        {
            "user_id": [1],
            "problem_id": [10],
            "skill_id": ["17_42"],
            "order_id": [1],
            "correct": [1],
        }
    )

    normalized, _ = AssistmentsAdapter().normalize(source)

    assert normalized.loc[0, "skill_ids"] == ["17", "42"]


def test_adapter_rejects_legacy_multiline_skill_encoding() -> None:
    source = pd.DataFrame(
        {
            "user_id": [1, 1],
            "problem_id": [10, 10],
            "skill_id": ["17", "42"],
            "order_id": [1, 1],
            "correct": [1, 1],
        }
    )

    with pytest.raises(AdapterError, match="corrected one-row-per-interaction format"):
        AssistmentsAdapter().normalize(source)


def test_adapter_removes_exact_duplicate_interactions() -> None:
    source = pd.DataFrame(
        {
            "user_id": [1, 1],
            "problem_id": [10, 10],
            "skill_id": ["fractions", "fractions"],
            "order_id": [1, 1],
            "correct": [1, 1],
        }
    )

    normalized, report = AssistmentsAdapter().normalize(source)

    assert len(normalized) == 1
    assert report["duplicate_rows_removed"] == 1
