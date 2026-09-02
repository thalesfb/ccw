"""Temporal-scope validation shared by ingestion clients."""

from __future__ import annotations

import re
from datetime import date
from typing import Any, Optional


def parse_publication_year(value: Any) -> Optional[int]:
    """Return a four-digit publication year when ``value`` is usable."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None

    match = re.match(r"^\s*(\d{4})", str(value))
    return int(match.group(1)) if match else None


def _parse_publication_date(value: Any) -> Optional[date]:
    """Parse ISO date or year-month metadata conservatively."""
    if value is None or str(value).strip() == "":
        return None

    text = str(value).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        try:
            return date.fromisoformat(text)
        except ValueError:
            return None
    if re.fullmatch(r"\d{4}-\d{2}", text):
        try:
            return date.fromisoformat(f"{text}-01")
        except ValueError:
            return None
    if re.fullmatch(r"\d{4}", text):
        try:
            return date.fromisoformat(f"{text}-01-01")
        except ValueError:
            return None
    return None


def is_within_review_period(
    year: Any,
    *,
    year_min: int,
    year_max: int,
    publication_date: Any = None,
    cutoff_date: Any = None,
) -> bool:
    """Check the inclusive protocol year range and optional cutoff date.

    A malformed non-empty publication date is rejected instead of silently
    falling back to its year. A missing date remains permissible when the
    normalized year is valid.
    """
    parsed_year = parse_publication_year(year)
    if parsed_year is None or not int(year_min) <= parsed_year <= int(year_max):
        return False

    if publication_date is None or str(publication_date).strip() == "":
        return True

    parsed_date = _parse_publication_date(publication_date)
    if parsed_date is None:
        return False

    if cutoff_date is None or str(cutoff_date).strip() == "":
        return True

    cutoff = _parse_publication_date(cutoff_date)
    return cutoff is not None and parsed_date <= cutoff
