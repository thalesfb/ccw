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
    assert manifest['schema_version'] == 2
    assert manifest['retrieval_scope_sha256'] != manifest['scope_sha256']
    assert manifest['scope_unchanged'] is False
    assert 'not been replayed' in manifest['scope_drift_explanation']
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
                 if source.get('replay_status') == 'frozen_retrieval_replay_verified']
    assert replay_validation['checked_study_ids'] == [source['study_id'] for source in recovered]
    assert replay_validation['checked_source_count'] == len(recovered)
    assert replay_validation['checked_chunk_count'] == sum(source['chunks'] for source in recovered)
    assert replay_validation['integrity_failures'] == 0
