import pandas as pd
import pytest

from src.processing.dedup import audit_duplicate_candidates, normalize_doi


@pytest.mark.parametrize("missing_doi", [None, float("nan"), pd.NA])
def test_normalize_doi_treats_missing_values_as_empty(missing_doi):
    assert normalize_doi(missing_doi) == ""


def test_title_audit_does_not_treat_missing_dois_as_identity_duplicates():
    df = pd.DataFrame(
        {
            "doi": [float("nan"), pd.NA],
            "url": [None, ""],
            "title": ["Same title", "Same title"],
            "is_duplicate": [False, False],
        }
    )

    audit = audit_duplicate_candidates(df)

    assert audit["deterministic_identity_duplicate_rows"] == 0
    assert audit["title_only"]["repeated_groups"] == 1
    assert audit["title_only"]["excess_rows"] == 1
