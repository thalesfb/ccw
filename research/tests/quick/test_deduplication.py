"""
Tests for deduplication functionality.
"""
import pytest
import pandas as pd
from research.deduplication import deduplicate_articles, _choose_best
from research.config import PAPER_COLUMNS


def test_choose_best():
    """Test choosing best paper between duplicates."""
    data = {
        'doi_url': ['https://doi.org/10.1234', ''],
        'abstract': ['Short', 'Much longer abstract text']
    }
    df = pd.DataFrame(data)
    
    # Paper with DOI should be kept
    drop_idx = _choose_best(df, 0, 1)
    assert drop_idx == 1  # Remove paper without DOI
    
    # When both have no DOI, keep longer abstract
    df.loc[0, 'doi_url'] = ''
    drop_idx = _choose_best(df, 0, 1)
    assert drop_idx == 0  # Remove shorter abstract


def test_deduplicate_empty_df():
    """Test deduplication with empty DataFrame."""
    df_empty = pd.DataFrame(columns=PAPER_COLUMNS)
    result = deduplicate_articles(df_empty)
    
    assert result.empty
    assert list(result.columns) == PAPER_COLUMNS


def test_deduplicate_by_doi():
    """Test deduplication by DOI."""
    data = {
        'title': ['Paper A', 'Paper A Duplicate'],
        'doi_url': ['https://doi.org/10.1234', 'https://doi.org/10.1234'],
        'abstract': ['Abstract 1', 'Abstract 2'],
        'year': [2020, 2020]
    }
    df = pd.DataFrame(data)
    
    # Add missing columns
    for col in PAPER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    result = deduplicate_articles(df)
    
    # Should have only 1 paper after deduplication
    assert len(result) == 1


def test_deduplicate_by_title_similarity():
    """Test deduplication by similar titles."""
    data = {
        'title': [
            'Machine Learning in Mathematics Education',
            'Machine Learning in Mathematics Education',  # Exact duplicate
            'Completely Different Title About Physics'
        ],
        'doi_url': ['', '', ''],
        'abstract': ['Abstract 1', 'Abstract 2', 'Abstract 3'],
        'year': [2020, 2020, 2020]
    }
    df = pd.DataFrame(data)
    
    # Add missing columns
    for col in PAPER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    result = deduplicate_articles(df)
    
    # First two have identical titles and should be deduplicated
    assert len(result) == 2  # Should keep only 2 unique papers


def test_deduplicate_preserves_columns():
    """Test that deduplication preserves all columns."""
    data = {
        'title': ['Paper A', 'Paper B'],
        'authors': ['Author 1', 'Author 2'],
        'year': [2020, 2021],
        'doi_url': ['doi1', 'doi2'],
    }
    df = pd.DataFrame(data)
    
    # Add missing columns
    for col in PAPER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    result = deduplicate_articles(df)
    
    # Check all columns are preserved
    for col in PAPER_COLUMNS:
        assert col in result.columns
