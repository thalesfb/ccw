"""Local, page-traceable retrieval; retrieval is never a support judgment.

Uses the existing page extractor and SQLite FTS5 (no embeddings or remote API).
FTS query syntax: https://www.sqlite.org/fts5.html#full_text_query_syntax
PDF extraction limitations: https://pypdf.readthedocs.io/en/6.10.0/user/extract-text.html
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from pathlib import Path

from .pdf_feedback import extract_feedback

ROLES = {'empirical_evidence', 'contextual_protocol', 'pedagogy', 'methodology',
         'normative', 'technical'}
STATUSES = {'SUPPORTED', 'PARTIALLY_SUPPORTED', 'CONTRADICTED',
            'INSUFFICIENT_EVIDENCE', 'NOT_APPLICABLE'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_chunks(pdf: Path, source: dict, chunk_size: int = 3000) -> list[dict]:
    """Extract single-page chunks with stable identity and byte-level provenance.

    Page numbers are physical, one-based PDF positions, not printed page labels.
    Source identity (title/DOI) must be checked separately before scientific use.
    """
    if chunk_size < 32 or not source.get('study_id') or not source.get('bib_key'):
        raise ValueError('Invalid source identity or chunk size')
    if source.get('synthesis_role') not in ROLES:
        raise ValueError('Invalid evidence role')
    extracted = extract_feedback(pdf)
    chunks = []
    for page in extracted['pages']:
        text = page['text']
        for offset in range(0, len(text), chunk_size):
            part = text[offset:offset + chunk_size]
            if not part.strip():
                continue
            identity = f"{source['study_id']}:{source['bib_key']}:{source['synthesis_role']}:" + \
                f"{extracted['source_sha256']}:{page['page']}:{offset}:{chunk_size}"
            chunks.append({
                'chunk_id': digest(identity.encode())[:24],
                'study_id': str(source['study_id']), 'bib_key': source['bib_key'],
                'synthesis_role': source['synthesis_role'],
                'source_url': source.get('source_url', ''),
                'source_path': str(Path(pdf).resolve()),
                'source_sha256': extracted['source_sha256'],
                'page_start': page['page'], 'page_end': page['page'],
                'section': None, 'char_start': offset,
                'text': part, 'text_sha256': digest(part.encode('utf-8')),
                'page_text_sha256': page['text_sha256'],
                'chunk_size': chunk_size,
            })
    if not chunks:
        raise ValueError('PDF has no extractable text; OCR/review is required')
    return chunks


def _chunk_errors(chunk: dict, sources: dict | None = None) -> list[str]:
    errors = []
    if digest(chunk['text'].encode('utf-8')) != chunk['text_sha256']:
        errors.append('Chunk text hash mismatch')
    path = Path(chunk['source_path'])
    sources = {} if sources is None else sources
    if path not in sources:
        sources[path] = extract_feedback(path) if path.is_file() else None
    original = sources[path]
    if original is None or original['source_sha256'] != chunk['source_sha256']:
        errors.append('Source file hash mismatch or missing source')
        return errors
    if chunk['page_start'] < 1 or chunk['page_start'] != chunk['page_end']:
        errors.append('Invalid single-page locator')
        return errors
    pages = {page['page']: page for page in original['pages']}
    page = pages.get(chunk['page_start'])
    offset, size = chunk['char_start'], chunk['chunk_size']
    if page is None or offset < 0 or size < 32 or offset % size != 0:
        errors.append('Invalid page or character locator')
        return errors
    if (chunk['text'] != page['text'][offset:offset + size] or
            chunk['page_text_sha256'] != page['text_sha256']):
        errors.append('Chunk is not bound to the original page')
    identity = f"{chunk['study_id']}:{chunk['bib_key']}:{chunk['synthesis_role']}:" + \
        f"{original['source_sha256']}:{chunk['page_start']}:{offset}:{size}"
    if chunk['chunk_id'] != digest(identity.encode())[:24]:
        errors.append('Chunk identity mismatch')
    return errors


class EvidenceIndex:
    """Separate operational index with an explicit canonical scope allowlist.

    Scientific use supplies bib/role bindings and PDF sha256 values from the
    reviewed source manifest. Scope-only mode is generic, unverified retrieval.
    A manifest hash anchors bytes, not publisher identity or scientific validity.
    """

    def __init__(self, path: Path, *, allowed_ids: set[str], source_registry: dict | None = None):
        self.allowed_ids = {str(value) for value in allowed_ids}
        self.source_registry = source_registry
        if source_registry is not None and not self.allowed_ids <= source_registry.keys():
            raise ValueError('Canonical source registry does not cover the allowed scope')
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('CREATE TABLE IF NOT EXISTS evidence '
                                '(chunk_id TEXT PRIMARY KEY, study_id TEXT, '
                                'role TEXT, payload TEXT)')
        self.connection.execute('CREATE VIRTUAL TABLE IF NOT EXISTS chunks '
                                'USING fts5(chunk_id UNINDEXED, text, '
                                "tokenize='unicode61 remove_diacritics 2')")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.connection.close()

    def _binding_matches(self, chunk: dict) -> bool:
        if self.source_registry is None:
            return True  # Generic retrieval; scientific use must supply canonical bindings.
        expected = self.source_registry.get(chunk['study_id'], {})
        return (all(chunk[key] == expected.get(key) for key in ('bib_key', 'synthesis_role')) and
                (not expected.get('sha256') or chunk['source_sha256'] == expected['sha256']))

    def add(self, chunks: list[dict]) -> None:
        """Replace each study/role atomically; reject unknown or altered sources."""
        sources = {}
        for chunk in chunks:
            if chunk['study_id'] not in self.allowed_ids:
                raise ValueError('Study is outside the declared scope')
            if not self._binding_matches(chunk):
                raise ValueError('Canonical bibliography/role binding mismatch')
            if chunk['synthesis_role'] not in ROLES or _chunk_errors(chunk, sources):
                raise ValueError('Invalid role or source/chunk hash')
        groups = {(row['study_id'], row['synthesis_role']) for row in chunks}
        with self.connection:
            for study_id, role in groups:
                old = self.connection.execute(
                    'SELECT chunk_id FROM evidence WHERE study_id=? AND role=?',
                    (study_id, role)).fetchall()
                self.connection.executemany('DELETE FROM chunks WHERE chunk_id=?',
                                            [(row[0],) for row in old])
                self.connection.execute('DELETE FROM evidence WHERE study_id=? AND role=?',
                                        (study_id, role))
            self.connection.executemany('INSERT INTO evidence VALUES (?,?,?,?)', [
                (row['chunk_id'], row['study_id'], row['synthesis_role'],
                 json.dumps(row, ensure_ascii=False)) for row in chunks])
            self.connection.executemany('INSERT INTO chunks VALUES (?,?)', [
                (row['chunk_id'], row['text']) for row in chunks])

    def get(self, chunk_id: str) -> dict | None:
        row = self.connection.execute('SELECT chunk_id, study_id, role, payload '
                                      'FROM evidence WHERE chunk_id=?',
                                      (chunk_id,)).fetchone()
        chunk = json.loads(row['payload']) if row else None
        if not chunk or chunk['study_id'] not in self.allowed_ids:
            return None
        if (not self._row_matches(row, chunk) or
                not self._binding_matches(chunk) or _chunk_errors(chunk)):
            raise ValueError('Evidence integrity or canonical binding drift; rebuild the index')
        return chunk

    @staticmethod
    def _row_matches(row, chunk: dict) -> bool:
        return (row['chunk_id'] == chunk['chunk_id'] and
                row['study_id'] == chunk['study_id'] and
                row['role'] == chunk['synthesis_role'] and
                ('fts_text' not in row.keys() or row['fts_text'] == chunk['text']))

    def search(self, query: str, *, study_ids: set[str] | None = None,
               roles: set[str] | None = None, k: int = 5) -> list[dict]:
        """Conservative AND retrieval; no result means no lexical match, not refutation.

        Tokens are quoted rather than accepting caller-supplied FTS operators.
        Only empirical evidence is searched by default. BM25 ranks passages; it
        does not measure scientific confidence or semantic support.
        """
        tokens = [word for word in re.findall(r'\w+', query.lower())
                  if len(word) > 1 and word not in {'and', 'or', 'not', 'near'}]
        roles = {'empirical_evidence'} if roles is None else roles
        ids = self.allowed_ids if study_ids is None else {str(v) for v in study_ids}
        ids = ids & self.allowed_ids
        if not tokens or not roles or not ids or k < 1:
            return []
        if not roles <= ROLES:
            raise ValueError('Unknown retrieval role')
        sql = ('SELECT e.chunk_id, e.study_id, e.role, e.payload, chunks.text AS fts_text '
               'FROM chunks JOIN evidence e '
               'ON chunks.chunk_id=e.chunk_id WHERE chunks MATCH ? '
               f"AND e.study_id IN ({','.join('?' for _ in ids)}) "
               f"AND e.role IN ({','.join('?' for _ in roles)}) "
               'ORDER BY bm25(chunks), e.chunk_id LIMIT ?')
        values = [' AND '.join('"' + word + '"' for word in tokens),
                  *sorted(ids), *sorted(roles), min(k, 100)]
        rows = self.connection.execute(sql, values).fetchall()
        results = [json.loads(row['payload']) for row in rows]
        sources = {}
        if any(not self._row_matches(row, chunk) or
               chunk['study_id'] not in ids or chunk['synthesis_role'] not in roles or
               not self._binding_matches(chunk) or _chunk_errors(chunk, sources)
               for row, chunk in zip(rows, results)):
            raise ValueError('Retrieved source hash drift; rebuild the index')
        return results


def validate_claim(claim: dict, index: EvidenceIndex, bib_keys: set[str]) -> list[str]:
    """Check traceability, not truth; support remains a documented review decision."""
    errors = []
    if claim.get('support_status') not in STATUSES:
        errors.append('Unknown support status')
    if not set(claim.get('citation_keys', [])) <= bib_keys:
        errors.append('Unknown bibliography key')
    manuscript = Path(claim['tcc_file'])
    text = manuscript.read_text(encoding='utf-8') if manuscript.is_file() else ''
    if not manuscript.is_file() or claim['claim_text'] not in text:
        errors.append('Claim text drift or missing manuscript')
    if claim.get('manuscript_sha256') and digest(text.encode('utf-8')) != claim['manuscript_sha256']:
        errors.append('Manuscript hash drift; review the statement in its new context')
    requires_evidence = claim.get('support_status') in {
        'SUPPORTED', 'PARTIALLY_SUPPORTED', 'CONTRADICTED'}
    if requires_evidence and (not claim.get('evidence_chunks') or
                              not claim.get('reviewer') or
                              not claim.get('counterevidence_checked')):
        errors.append('Support decision lacks evidence, reviewer or counterevidence check')
    for chunk_id in claim.get('evidence_chunks', []):
        try:
            chunk = index.get(chunk_id)
        except ValueError as error:
            errors.append(str(error))
            continue
        if chunk is None:
            errors.append('Missing evidence chunk')
            continue
        if claim.get('source_hashes', {}).get(chunk_id) != chunk['source_sha256']:
            errors.append('Claim source hash mismatch')
        if chunk['bib_key'] not in claim.get('citation_keys', []):
            errors.append('Evidence belongs to a different citation')
        if claim.get('claim_type') == 'empirical_result' and chunk['synthesis_role'] != 'empirical_evidence':
            errors.append('Protocol/context or other non-empirical source cannot support an empirical result')
    return errors
