"""Regression tests for the review's temporal scope."""

from research.src.config import load_config
from research.src.ingestion.core import COREClient
from research.src.ingestion.crossref import CrossrefClient
from research.src.ingestion.openalex import OpenAlexClient
from research.src.ingestion.semantic_scholar import SemanticScholarClient
from research.src.validation.temporal import is_within_review_period


def test_review_period_is_inclusive_and_enforces_cutoff() -> None:
    common = {"year_min": 2015, "year_max": 2026, "cutoff_date": "2026-08-31"}

    assert is_within_review_period(2015, **common)
    assert is_within_review_period(2026, publication_date="2026-08-31", **common)
    assert not is_within_review_period(2014, **common)
    assert not is_within_review_period(2027, **common)
    assert not is_within_review_period(2026, publication_date="2026-09-01", **common)
    assert not is_within_review_period(2026, publication_date="not-a-date", **common)


def test_core_rejects_years_outside_configured_range() -> None:
    client = COREClient(load_config())

    assert client._normalize_result({"yearPublished": 2027}) is None
    assert client._normalize_result({"yearPublished": 2014}) is None


def test_crossref_rejects_date_after_cutoff() -> None:
    client = CrossrefClient(load_config())
    item = {
        "title": ["A study"],
        "published-online": {"date-parts": [[2026, 9, 1]]},
    }

    assert client._normalize_result(item) is None


def test_openalex_rejects_year_after_configured_range() -> None:
    client = OpenAlexClient(load_config())

    assert client._normalize_result({"publication_year": 2027}) is None


def test_semantic_scholar_rejects_year_after_configured_range() -> None:
    client = SemanticScholarClient(load_config())

    assert client._normalize_result({"year": 2027}) is None
