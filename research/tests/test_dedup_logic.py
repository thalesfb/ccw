
import pandas as pd
import pytest
from src.exports.excel import get_best_duplicates, _compute_prisma_stats_from_df
from src.processing.dedup import (
    audit_duplicate_candidates,
    build_identity_audit_rows,
    deterministic_identity_duplicate_mask,
    find_duplicates,
    normalize_doi,
)


def test_normalize_doi_accepts_common_resolver_forms_and_citation_punctuation():
    assert normalize_doi(" DOI:10.1234/ABC. ") == "10.1234/abc"
    assert normalize_doi("https://doi.org/10.1234/ABC,") == "10.1234/abc"
    assert normalize_doi("https://dx.doi.org/10.1234/ABC;") == "10.1234/abc"

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


def test_get_best_duplicates_collapses_exact_doi_records_even_with_same_doi():
    df = pd.DataFrame({
        'doi': ['10.1234/test', '10.1234/test'],
        'title': ['Title 1', 'Title 1'],
        'is_duplicate': [False, True],
        'duplicate_of': [None, 'DOI:10.1234/test'],
        'abstract': ['Short', 'Longer Abstract'],
        'citation_count': [10, 10]
    })
    result = get_best_duplicates(df)
    assert len(result) == 1
    assert result.iloc[0]['doi'] == '10.1234/test'


def test_identity_mask_detects_exact_doi_url_even_when_persisted_flags_are_zero():
    df = pd.DataFrame({
        'doi': ['10.1/a', '10.1/a', '', ''],
        'url': ['https://example.test/a', 'https://example.test/b',
                'https://example.test/c', 'https://example.test/c'],
        'is_duplicate': [False, False, False, False],
    })
    mask = deterministic_identity_duplicate_mask(df)
    assert mask.tolist() == [False, True, False, True]


def test_identity_audit_exposes_retained_record_for_each_duplicate():
    df = pd.DataFrame({
        'id': [10, 20, 30],
        'doi': ['10.1/a', '10.1/a', ''],
        'url': ['', '', 'https://example.test/c'],
        'title': ['A', 'A', 'C'],
        'selection_stage': ['screening', 'screening', 'screening'],
        'status': ['excluded', 'excluded', 'excluded'],
    })
    rows = build_identity_audit_rows(df)
    assert rows == [{
        'duplicate_id': 20,
        'retained_id': 10,
        'identifier_type': 'doi',
        'identifier': '10.1/a',
        'duplicate_title': 'A',
        'retained_title': 'A',
        'duplicate_stage': 'screening',
        'retained_stage': 'screening',
        'duplicate_status': 'excluded',
        'retained_status': 'excluded',
        'decision': 'remove_duplicate_record_from_prisma_flow',
    }]


def test_compute_prisma_stats_detects_identity_with_zero_persisted_flags():
    df = pd.DataFrame({
        'doi': ['10/foo', '10/foo', '10/bar'],
        'title': ['T1', 'T1', 'T2'],
        'is_duplicate': [False, False, False],
        'selection_stage': ['screening', 'screening', 'included'],
        'status': ['excluded', 'excluded', 'included'],
    })
    stats = _compute_prisma_stats_from_df(df)
    assert stats['duplicates_removed'] == 1
    assert stats['screening'] == 2
    assert stats['deduplication_audit']['deterministic_identity_duplicate_rows'] == 1

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
    assert stats['stage_percentages']['screening_excluded_of_identification'] == 25.0
    assert stats['stage_percentages']['screening_advanced_of_identification'] == 25.0
    assert stats['deduplication_audit']['doi']['excess_rows'] == 1


def test_duplicate_candidate_audit_does_not_claim_semantic_removals():
    df = pd.DataFrame(
        {
            'id': [1, 2, 3, 4, 5],
            'doi': ['10/x', ' DOI:10/X ', '', None, '10/y'],
            'url': ['https://example.test/a', 'https://example.test/a', '', '', ''],
            'title': ['Editorial', ' editorial ', 'A study', 'A study', 'A different study'],
            'is_duplicate': [False, False, False, False, True],
        }
    )

    audit = audit_duplicate_candidates(df)

    assert audit['raw_rows'] == 5
    assert audit['operationally_flagged_rows'] == 1
    assert audit['confirmed_semantic_duplicates'] == 0
    assert audit['doi']['repeated_groups'] == 1
    assert audit['doi']['excess_rows'] == 1
    assert audit['url']['repeated_groups'] == 1
    assert audit['url']['excess_rows'] == 1
    assert audit['title']['repeated_groups'] == 2
    assert audit['title']['excess_rows'] == 2
    assert audit['title_only']['repeated_groups'] == 1
    assert audit['title_only']['excess_rows'] == 1


def test_identity_audit_matches_actual_retained_export_record():
    raw = pd.DataFrame(
        {
            'id': [10, 20],
            'doi': ['10.1/a', '10.1/a'],
            'url': ['', ''],
            'title': ['Short screening record', 'Eligibility record'],
            'abstract': ['x', 'x' * 100],
            'selection_stage': ['included', 'screening'],
            'status': ['included', 'excluded'],
            'is_duplicate': [False, False],
        }
    )
    marked = find_duplicates(raw)
    retained = get_best_duplicates(marked)
    rows = build_identity_audit_rows(marked, retained_df=retained)

    assert len(retained) == 1
    assert retained.iloc[0]['id'] == 20
    assert rows[0]['duplicate_id'] == 10
    assert rows[0]['retained_id'] == 20
    assert rows[0]['identifier_type'] == 'doi'
    assert rows[0]['retained_stage'] == 'included'
    assert rows[0]['retained_stage_source_id'] == 10


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
    assert stats['duplicates_removed'] == 1  # somente fallback por DOI
    assert stats['screening'] == 2
    assert stats['included'] == 1


def test_compute_prisma_stats_does_not_remove_title_only_candidates():
    df = pd.DataFrame(
        {
            'doi': ['', '', '10/bar'],
            'title': ['Same title', 'same  title', 'Bar'],
            'selection_stage': ['screening', 'eligibility', 'included'],
            'status': ['excluded', 'excluded', 'included'],
        }
    )

    stats = _compute_prisma_stats_from_df(df)

    assert stats['duplicates_removed'] == 0
    assert stats['screening'] == 3
    assert stats['deduplication_audit']['title']['excess_rows'] == 1
    assert stats['deduplication_audit']['title_only']['excess_rows'] == 1


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
