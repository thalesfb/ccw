
import pandas as pd
import pytest
from src.exports.excel import get_best_duplicates, _compute_prisma_stats_from_df

def test_get_best_duplicates_no_duplicates():
    df = pd.DataFrame({
        'doi': ['doi1', 'doi2'],
        'title': ['Title 1', 'Title 2'],
        'is_duplicate': [False, False],
        'duplicate_of': [None, None],
        'abstract': ['Abstract 1', 'Abstract 2'],
        'citation_count': [10, 20]
    })
    result = get_best_duplicates(df)
    assert len(result) == 2
    assert set(result['doi']) == {'doi1', 'doi2'}

def test_get_best_duplicates_simple_group():
    # Original (unique) + 1 Duplicate
    # Duplicate has better abstract
    df = pd.DataFrame({
        'doi': ['doi1', 'doi1_dup'],
        'title': ['Title 1', 'Title 1 Dup'],
        'is_duplicate': [False, True],
        'duplicate_of': [None, 'DOI:doi1'],
        'abstract': ['Short', 'Longer Abstract'],
        'citation_count': [10, 10]
    })
    result = get_best_duplicates(df)
    assert len(result) == 1
    # Should pick the one with longer abstract
    assert result.iloc[0]['abstract'] == 'Longer Abstract'
    # Should have is_duplicate=False
    assert result.iloc[0]['is_duplicate'] == False

def test_get_best_duplicates_orphan():
    # Duplicate points to non-existent DOI
    df = pd.DataFrame({
        'doi': ['doi1_dup'],
        'title': ['Title 1 Dup'],
        'is_duplicate': [True],
        'duplicate_of': ['DOI:doi_missing'],
        'abstract': ['Abstract'],
        'citation_count': [10]
    })
    result = get_best_duplicates(df)
    assert len(result) == 1
    assert result.iloc[0]['doi'] == 'doi1_dup'
    assert result.iloc[0]['is_duplicate'] == False

def test_get_best_duplicates_multiple_groups():
    # Group 1: doi1 (unique) + doi1_dup (dup)
    # Group 2: doi2 (unique)
    # Group 3: doi3_dup (orphan dup)
    df = pd.DataFrame({
        'doi': ['doi1', 'doi1_dup', 'doi2', 'doi3_dup'],
        'title': ['T1', 'T1D', 'T2', 'T3D'],
        'is_duplicate': [False, True, False, True],
        'duplicate_of': [None, 'DOI:doi1', None, 'DOI:doi3'],
        'abstract': ['A', 'BBB', 'C', 'D'],
        'citation_count': [1, 1, 1, 1]
    })
    result = get_best_duplicates(df)
    assert len(result) == 3
    # doi1 group -> should pick doi1_dup (longer abstract)
    # doi2 -> stays as is
    # doi3_dup -> becomes new unique
    
    dois = set(result['doi'])
    assert 'doi1_dup' in dois
    assert 'doi2' in dois
    assert 'doi3_dup' in dois
    assert 'doi1' not in dois # Replaced by doi1_dup


def test_compute_prisma_stats_identification_uses_raw_rows():
    df = pd.DataFrame(
        {
            'doi': ['10/foo', '10/foo', '10/bar', '10/baz'],
            'title': ['T1', 'T1 dup', 'T2', 'T3'],
            'is_duplicate': [False, True, False, False],
            'duplicate_of': [None, 'DOI:10/foo', None, None],
            'selection_stage': ['screening', 'screening', 'eligibility', 'screening'],
            'status': ['included', 'excluded', 'included', 'Excluded at screening'],
        }
    )

    stats = _compute_prisma_stats_from_df(df)

    assert stats['raw_rows'] == 4
    assert stats['identification'] == 4  # precisa refletir o total bruto
    assert stats['duplicates_removed'] == 1
    assert stats['screening'] == 3  # duplicata removida nao entra na triagem
    assert stats['screening_excluded'] == 1  # apenas registros unicos contam
    assert stats['eligibility'] == 1
    assert stats['included'] == 0


def test_compute_prisma_stats_without_duplicate_flag_fallbacks():
    df = pd.DataFrame(
        {
            'doi': ['10/foo', '10/foo', '10/bar'],
            'title': ['T1', 'T1 dup', 'T2'],
            'selection_stage': ['screening', 'screening', 'included'],
            'status': ['included', 'excluded', 'included'],
        }
    )

    stats = _compute_prisma_stats_from_df(df)

    assert stats['identification'] == 3
    assert stats['duplicates_removed'] == 1  # fallback por DOI/titulo
    assert stats['screening'] == 2
    assert stats['included'] == 1


def test_compute_prisma_stats_with_custom_unique_subset():
    raw = pd.DataFrame(
        {
            'doi': ['10/orphan', '10/bar'],
            'title': ['Orphan', 'Bar'],
            'is_duplicate': [True, False],
            'duplicate_of': ['DOI:10/missing', None],
            'selection_stage': ['included', 'screening'],
            'status': ['included', 'excluded'],
        }
    )

    deduped = raw.copy()
    deduped['is_duplicate'] = False
    deduped['duplicate_of'] = None

    stats = _compute_prisma_stats_from_df(raw, unique_subset=deduped)

    assert stats['identification'] == 2
    assert stats['screening'] == 2  # usa subconjunto fornecido
    assert stats['duplicates_removed'] == 0  # nenhum registro realmente removido
    assert stats['included'] == 1

if __name__ == "__main__":
    # Manual run if pytest not available
    test_get_best_duplicates_no_duplicates()
    test_get_best_duplicates_simple_group()
    test_get_best_duplicates_orphan()
    test_get_best_duplicates_multiple_groups()
    print("All tests passed!")
