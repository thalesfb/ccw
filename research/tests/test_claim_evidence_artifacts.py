"""Offline provenance gates; these checks do not adjudicate scientific support."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def test_source_manifest_preserves_every_canonical_study_without_private_paths():
    manifest = load('research/data/evidence_sources_current.json')
    path = ROOT / 'research/data/current_synthesis_scope.csv'
    scope = {row['study_id']: row for row in csv.DictReader(path.read_text(encoding='utf-8').splitlines())}
    sources = {row['study_id']: row for row in manifest['sources']}
    assert len(sources) == len(manifest['sources']) == 18
    assert sources.keys() == scope.keys()
    assert manifest['scope_sha256'] == hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
    assert manifest['extraction_settings']['chunk_size'] == 3000
    for relative, expected in manifest['code_hashes'].items():
        assert expected == hashlib.sha256((ROOT / relative).read_text(encoding='utf-8').encode()).hexdigest()
    for study_id, row in sources.items():
        assert row['bib_key'] == scope[study_id]['study_key']
        assert row['synthesis_role'] == scope[study_id]['synthesis_role']
        assert 'source_path' not in row and 'local_file' not in row
        if row['status'] == 'recovered_identity_candidate':
            assert re.fullmatch('[0-9a-f]{64}', row['sha256'])
            assert row['page_count'] > 0
            assert 'pending' in row['identity_status']


def test_research_dependency_matches_recorded_pdf_extractor_version():
    manifest = load('research/data/evidence_sources_current.json')
    requirements = (ROOT / 'research/requirements.txt').read_text(encoding='utf-8')
    expected = f"pypdf=={manifest['extraction_settings']['pypdf_version']}"

    assert expected in requirements.splitlines()


def test_optional_font_decoder_is_recorded_and_pinned_for_replay():
    manifest = load('research/data/evidence_sources_current.json')
    replay_validation = manifest.get('replay_validation', {})
    environment = replay_validation.get('environment', {})
    requirements = (ROOT / 'research/requirements.txt').read_text(encoding='utf-8')

    assert environment.get('pypdf_version') == manifest['extraction_settings']['pypdf_version']
    assert environment.get('fonttools_version')
    assert f"pypdf=={environment['pypdf_version']}" in requirements.splitlines()
    assert f"fonttools=={environment['fonttools_version']}" in requirements.splitlines()

    recovered = [source for source in manifest['sources']
                 if source['status'] == 'recovered_identity_candidate']
    assert replay_validation['checked_source_count'] == len(recovered)
    assert replay_validation['checked_chunk_count'] == sum(source['chunks'] for source in recovered)
    assert replay_validation['integrity_failures'] == 0


def test_reviewed_claims_preserve_manuscript_context_and_source_locators():
    sources = {row['study_id']: row for row in load('research/data/evidence_sources_current.json')['sources']}
    ledger = load('research/data/claim_evidence_current.json')
    assert ledger['claims']
    for claim in ledger['claims']:
        text = (ROOT / claim['tcc_file']).read_text(encoding='utf-8')
        assert claim['claim_text'] in text
        assert claim['manuscript_sha256'] == hashlib.sha256(text.encode()).hexdigest()
        source = sources[claim['source_id'].removeprefix('PS-')]
        assert claim['citation_keys'] == [source['bib_key']]
        assert claim['evidence_chunks']
        assert set(claim['evidence_chunks']) == claim['source_hashes'].keys()
        assert set(claim['source_hashes'].values()) == {source['sha256']}
        assert all(1 <= page <= source['page_count'] for page in claim['physical_pages'])
        assert claim['counterevidence_checked'] and claim['support_boundary']
        assert claim['human_adjudication'] == 'pending'


def test_maclellan_synthesis_is_bound_to_both_primary_analyses():
    claims = [claim for claim in load('research/data/claim_evidence_current.json')['claims']
              if claim['source_id'] == 'PS-8']
    assert len(claims) == 2
    assert {tuple(claim['physical_pages']) for claim in claims} == {(60, 64), (72,)}
    assert all(claim['support_status'] == 'SUPPORTED' for claim in claims)
    assert all(claim['human_adjudication'] == 'pending' for claim in claims)


def test_small_retrieval_evaluation_is_not_a_quality_score():
    report = load('research/exports/analysis/evidence_retrieval_evaluation.json')
    assert len(report['cases']) == 9
    assert all(row['passed'] for row in report['cases'])
    negatives = [row for row in report['cases'] if not row['expected_physical_pages']]
    assert len(negatives) == 3
    assert all(not row['retrieved_physical_pages'] for row in negatives)
    assert 'not semantic support' in report['purpose']
