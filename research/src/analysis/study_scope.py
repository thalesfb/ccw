"""Load candidate IDs and source metadata without interpreting MMAT decisions."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


CANDIDATE_STUDY_IDS: tuple[int, ...] = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 6915, 6916, 6917, 6919, 6920, 6921, 6923
)
DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
PRIMARY_SOURCES_PATH = DATA_ROOT / "mmat_primary_sources_manifest.csv"
CANDIDATE_SCOPE_PATH = DATA_ROOT / "current_synthesis_scope.csv"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _ids(rows: Iterable[dict[str, str]], field: str = "study_id") -> list[int]:
    try:
        return [int(row[field]) for row in rows]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid study identifier in field {field!r}") from exc


def load_primary_sources(
    path: Path | str = PRIMARY_SOURCES_PATH,
) -> list[dict[str, str]]:
    """Load one source-ledger row for every current study."""
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CANDIDATE_STUDY_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Primary-source manifest must contain exactly {expected}; got {ids}"
        )
    for row in rows:
        if not row.get("source_id") or not row.get("source_url"):
            raise ValueError(f"Study {row.get('study_id')} lacks a source identifier or URL")
    return rows

def load_candidate_scope(
    path: Path | str = CANDIDATE_SCOPE_PATH,
) -> list[dict[str, str]]:
    """Load candidate records by ID without interpreting selection or MMAT fields."""
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CANDIDATE_STUDY_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Candidate scope must contain exactly {expected}; got {ids}"
        )
    return rows
