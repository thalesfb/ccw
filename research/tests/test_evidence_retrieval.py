"""Deterministic retrieval checks; fixtures are not educational evidence."""

import hashlib
from pathlib import Path

import pytest
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

from research.src.validation.evidence_retrieval import (
    EvidenceIndex, extract_chunks, validate_claim,
)


def pdf_fixture(path, texts):
    writer = PdfWriter()
    for text in texts:
        page = writer.add_blank_page(width=400, height=500)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject()
        stream.set_data(('BT /F1 12 Tf 30 450 Td (' + text + ') Tj ET').encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    writer.write(path)


def source(study_id='2', role='empirical_evidence'):
    return {'study_id': study_id, 'bib_key': 'Implementation2025_000',
            'synthesis_role': role, 'title': 'Synthetic retrieval fixture',
            'source_url': 'https://example.org/fixture.pdf'}


def test_extraction_preserves_pages_and_stable_source_hash(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline', 'holdout calibration error'])
    chunks = extract_chunks(pdf, source(), chunk_size=64)
    assert [row['page_start'] for row in chunks] == [1, 2]
    assert all(row['page_start'] == row['page_end'] for row in chunks)
    assert chunks[0]['source_sha256'] == hashlib.sha256(pdf.read_bytes()).hexdigest()
    assert extract_chunks(pdf, source(), chunk_size=64) == chunks


def test_blank_pdf_is_not_usable_evidence(tmp_path):
    pdf = tmp_path / 'blank.pdf'
    writer = PdfWriter()
    writer.add_blank_page(width=400, height=500)
    writer.write(pdf)
    with pytest.raises(ValueError, match='extractable text'):
        extract_chunks(pdf, source())


def test_page_filter_and_empirical_scope_block_context_and_unknown_ids(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction', 'calibration baseline'])
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2', '6921'}) as index:
        index.add(extract_chunks(pdf, source()))
        index.add(extract_chunks(pdf, source('6921', 'contextual_protocol')))
        assert [row['study_id'] for row in index.search('performance prediction')] == ['2']
        assert index.search('performance prediction', study_ids={'6921'}) == []
        assert len(index.search('performance prediction', roles={'contextual_protocol'})) == 1
        assert index.search('calibration baseline')[0]['page_start'] == 2
        with pytest.raises(ValueError, match='scope'):
            index.add(extract_chunks(pdf, source('excluded')))


def test_unanswered_query_and_fts_operators_are_not_evidence(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2'}) as index:
        index.add(extract_chunks(pdf, source()))
        assert index.search('quantum chromodynamics') == []
        assert index.search('') == []
        assert index.search('" OR *') == []


def test_narrowed_scope_cannot_resolve_an_old_chunk(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    chunk = extract_chunks(pdf, source())[0]
    database = tmp_path / 'index.sqlite'
    with EvidenceIndex(database, allowed_ids={'2'}) as index:
        index.add([chunk])
    with EvidenceIndex(database, allowed_ids={'6921'}) as index:
        assert index.get(chunk['chunk_id']) is None


@pytest.mark.parametrize('alteration', ['page', 'text', 'identity', 'bibliography'])
def test_index_rejects_passages_not_bound_to_the_original_page(tmp_path, alteration):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction', 'calibration baseline'])
    chunk = extract_chunks(pdf, source())[0]
    if alteration == 'page':
        chunk['page_start'] = chunk['page_end'] = 2
    elif alteration == 'text':
        chunk['text'] = 'Invented educational efficacy'
        chunk['text_sha256'] = hashlib.sha256(chunk['text'].encode()).hexdigest()
    elif alteration == 'bibliography':
        chunk['bib_key'] = 'Forged2025_000'
    else:
        chunk['chunk_id'] = 'invented-identity'
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2'}) as index:
        with pytest.raises(ValueError):
            index.add([chunk])


def test_index_can_enforce_canonical_source_bindings(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    registry = {'2': {'bib_key': 'Implementation2025_000', 'synthesis_role': 'empirical_evidence'}}
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2'}, source_registry=registry) as index:
        forged = extract_chunks(pdf, {**source(), 'bib_key': 'Forged2025_000'})
        with pytest.raises(ValueError, match='binding'):
            index.add(forged)
        wrong_role = extract_chunks(pdf, source('2', 'contextual_protocol'))
        with pytest.raises(ValueError, match='binding'):
            index.add(wrong_role)


def test_canonical_pdf_hash_blocks_reextraction_of_a_substituted_source(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    registry = {'2': {**source(), 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest()}}
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2'}, source_registry=registry) as index:
        index.add(extract_chunks(pdf, source()))
        pdf_fixture(pdf, ['invented educational efficacy'])
        with pytest.raises(ValueError, match='binding'):
            index.add(extract_chunks(pdf, source()))


def test_retrieval_rejects_source_file_drift(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2'}) as index:
        index.add(extract_chunks(pdf, source()))
        pdf_fixture(pdf, ['altered evidence'])
        with pytest.raises(ValueError, match='drift'):
            index.search('performance prediction')


@pytest.mark.parametrize('column', ['study_id', 'role', 'fts_text'])
def test_retrieval_rejects_index_metadata_that_disagrees_with_the_source(tmp_path, column):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    chunk = extract_chunks(pdf, source('6921', 'contextual_protocol'))[0]
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2', '6921'}) as index:
        index.add([chunk])
        if column == 'role':
            index.connection.execute("UPDATE evidence SET role='empirical_evidence'")
            kwargs = {}
        elif column == 'study_id':
            index.connection.execute("UPDATE evidence SET study_id='2'")
            kwargs = {'roles': {'contextual_protocol'}, 'study_ids': {'2'}}
        else:
            index.connection.execute("UPDATE chunks SET text='invented efficacy'")
            kwargs = {'roles': {'contextual_protocol'}}
        query = 'invented efficacy' if column == 'fts_text' else 'performance prediction'
        with pytest.raises(ValueError, match='drift'):
            index.search(query, **kwargs)
        if column != 'fts_text':
            with pytest.raises(ValueError, match='drift'):
                index.get(chunk['chunk_id'])


def test_claim_requires_real_chunk_hash_and_manuscript_text(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['performance prediction baseline'])
    manuscript = tmp_path / 'chapter.tex'
    manuscript.write_text('Prediction does not establish learning.', encoding='utf-8')
    chunk = extract_chunks(pdf, source())[0]
    claim = {'claim_text': 'Prediction does not establish learning.',
             'tcc_file': str(manuscript), 'support_status': 'SUPPORTED',
             'citation_keys': ['Implementation2025_000'],
             'evidence_chunks': [chunk['chunk_id']],
             'source_hashes': {chunk['chunk_id']: chunk['source_sha256']},
             'counterevidence_checked': True, 'reviewer': 'fixture-reviewer'}
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2'}) as index:
        index.add([chunk])
        assert validate_claim(claim, index, {'Implementation2025_000'}) == []
        claim['source_hashes'][chunk['chunk_id']] = 'wrong'
        assert any('hash' in error for error in validate_claim(claim, index, {'Implementation2025_000'}))
        claim['evidence_chunks'] = []
        assert any('evidence' in error for error in validate_claim(claim, index, {'Implementation2025_000'}))


def test_claim_detects_context_drift_even_when_the_sentence_remains(tmp_path):
    manuscript = tmp_path / 'chapter.tex'
    manuscript.write_text('Prediction is situated. Original context.', encoding='utf-8')
    claim = {'claim_text': 'Prediction is situated.', 'tcc_file': str(manuscript),
             'manuscript_sha256': hashlib.sha256(manuscript.read_text().encode()).hexdigest(),
             'support_status': 'INSUFFICIENT_EVIDENCE', 'citation_keys': []}
    manuscript.write_text('Prediction is situated. A different context.', encoding='utf-8')
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids=set()) as index:
        assert any('Manuscript hash' in error for error in validate_claim(claim, index, set()))


def test_reindex_replaces_old_source_and_claims_cannot_cite_context(tmp_path):
    pdf = tmp_path / 'primary.pdf'
    pdf_fixture(pdf, ['old performance baseline'])
    with EvidenceIndex(tmp_path / 'index.sqlite', allowed_ids={'2', '6921'}) as index:
        index.add(extract_chunks(pdf, source()))
        pdf_fixture(pdf, ['new calibration baseline'])
        index.add(extract_chunks(pdf, source()))
        assert index.search('old performance') == []
        assert len(index.search('new calibration')) == 1
        chunk = extract_chunks(pdf, source('6921', 'contextual_protocol'))[0]
        index.add([chunk])
        manuscript = tmp_path / 'chapter.tex'
        manuscript.write_text('A measured benefit.', encoding='utf-8')
        claim = {'claim_text': 'A measured benefit.', 'tcc_file': str(manuscript),
                 'claim_type': 'empirical_result', 'support_status': 'SUPPORTED',
                 'citation_keys': ['Implementation2025_000'],
                 'evidence_chunks': [chunk['chunk_id']],
                 'source_hashes': {chunk['chunk_id']: chunk['source_sha256']},
                 'counterevidence_checked': True, 'reviewer': 'fixture-reviewer'}
        assert any('context' in error for error in validate_claim(claim, index, {'Implementation2025_000'}))
