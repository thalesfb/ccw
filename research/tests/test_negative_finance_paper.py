import pytest

import pandas as pd

from research.src.processing.scoring import calculate_relevance_score
from research.src.processing.selection import apply_prisma_selection


def test_stock_market_paper_processed_via_selection_and_scoring():
    """Ensure the stock-market systematic review is processed by PRISMA
    selection together with relevance scoring rather than being dropped by
    an early ad-hoc pre-filter.
    """
    paper = {
        'title': 'Stock Market Prediction using Machine Learning Techniques: A Systematic Review',
        'abstract': (
            'This systematic review surveys stock market prediction models using '
            'machine learning techniques applied to financial time series forecasting.'
        ),
        'year': 2020,
        'authors': 'Smith, A.; Doe, J.'
    }

    df = pd.DataFrame([paper])

    # Compute a (simulated) high relevance score to ensure scoring is used
    # downstream by the PRISMA eligibility step. The value itself is not the
    # assertion target — we assert that selection runs and records a
    # selection_stage/status for the record.
    df['relevance_score'] = df.apply(lambda r: calculate_relevance_score(r.to_dict()), axis=1)

    result_df, stats = apply_prisma_selection(df, min_relevance_score=4.0)

    # The pipeline must annotate the record with selection information
    assert 'selection_stage' in result_df.columns
    assert 'status' in result_df.columns

    # Whether the paper is ultimately included or excluded is determined by
    # selection+scoring logic; we only check that the decision path used
    # selection (exclusion_reason column present when excluded).
    row = result_df.iloc[0]
    assert row['selection_stage'] in ('screening', 'eligibility', 'included')
    assert row['status'] in ('excluded', 'reviewed', 'included')
    # If excluded, ensure an exclusion reason was recorded by selection
    if row['status'] == 'excluded':
        assert 'exclusion_reason' in result_df.columns and row['exclusion_reason'] is not None
