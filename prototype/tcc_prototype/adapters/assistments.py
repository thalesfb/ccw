"""ASSISTments 2009-2010 Skill Builder adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

CANONICAL_COLUMNS = [
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


class AdapterError(ValueError):
    """Raised when source data cannot satisfy the canonical contract."""


@dataclass(frozen=True)
class AssistmentsAdapter:
    """Normalize the corrected ASSISTments Skill Builder export."""

    source_dataset: str = "assistments_2009_2010_skill_builder_corrected"
    skill_separator: str | None = None

    def _skill_values(self, value: Any) -> list[str]:
        if pd.isna(value):
            return []
        text = str(value).strip()
        if not text:
            return []
        if self.skill_separator:
            return sorted(
                {
                    token.strip()
                    for token in text.split(self.skill_separator)
                    if token.strip()
                }
            )
        return [text]

    def normalize(self, source: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
        """Return canonical interactions and a deterministic quality report."""

        required = {"user_id", "problem_id", "order_id", "correct"}
        missing = sorted(required.difference(source.columns))
        skill_column = next(
            (name for name in ("skill_id", "skill_name") if name in source.columns),
            None,
        )
        if missing:
            raise AdapterError("missing ASSISTments columns: " + ", ".join(missing))
        if skill_column is None:
            raise AdapterError("missing ASSISTments skill_id or skill_name column")

        input_rows = len(source)
        working = source.copy()
        working["_source_row_id"] = working.index.map(str)
        duplicate_mask = working.duplicated(
            subset=["user_id", "problem_id", "order_id", "correct", skill_column],
            keep="first",
        )
        duplicate_rows_removed = int(duplicate_mask.sum())
        working = working.loc[~duplicate_mask].copy()

        working["_skill_ids"] = working[skill_column].map(self._skill_values)
        valid_mask = (
            working["user_id"].notna()
            & working["problem_id"].notna()
            & working["order_id"].notna()
            & working["correct"].isin([0, 1, False, True])
            & working["_skill_ids"].map(bool)
        )
        invalid_rows_removed = int((~valid_mask).sum())
        working = working.loc[valid_mask].copy()

        def optional_integer(column: str) -> pd.Series:
            if column not in working.columns:
                return pd.Series([None] * len(working), index=working.index, dtype="object")
            values = pd.to_numeric(working[column], errors="coerce")
            return values.map(lambda value: int(value) if pd.notna(value) else None)

        normalized = pd.DataFrame(index=working.index)
        normalized["student_id"] = working["user_id"].map(lambda value: str(value))
        normalized["item_id"] = working["problem_id"].map(lambda value: str(value))
        normalized["skill_ids"] = working["_skill_ids"]
        normalized["interaction_order"] = pd.to_numeric(
            working["order_id"], errors="raise"
        ).astype(int)
        normalized["timestamp"] = None
        normalized["correct"] = working["correct"].astype(int).astype(bool)
        normalized["answer"] = None
        normalized["attempt_count"] = optional_integer("attempt_count")
        normalized["hint_count"] = optional_integer("hint_count")
        elapsed_column = next(
            (
                name
                for name in ("elapsed_time_ms", "ms_first_response")
                if name in working.columns
            ),
            None,
        )
        normalized["elapsed_time_ms"] = (
            optional_integer(elapsed_column)
            if elapsed_column is not None
            else pd.Series([None] * len(working), index=working.index, dtype="object")
        )
        normalized["session_id"] = None
        normalized["source_dataset"] = self.source_dataset
        normalized["source_row_id"] = working["_source_row_id"]

        normalized = normalized.sort_values(
            ["student_id", "interaction_order", "source_row_id"],
            kind="mergesort",
        ).reset_index(drop=True)
        normalized = normalized[CANONICAL_COLUMNS]

        report = {
            "input_rows": input_rows,
            "duplicate_rows_removed": duplicate_rows_removed,
            "invalid_rows_removed": invalid_rows_removed,
            "output_rows": len(normalized),
        }
        return normalized, report
