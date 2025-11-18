"""
Enrichment helpers extracted from notebook-style pipeline.

Provides functions to enrich DataFrames with derived fields such as
`relevance_score`, `comp_techniques`, `main_results` and `identified_gaps`.
These helpers are designed to be used by multiple pipeline implementations.
"""
from typing import Any, Dict, Iterable, Mapping, Optional

import re
import pandas as pd

from .scoring import calculate_relevance_score
from ..config import load_config


_SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def _split_sentences(text: str) -> Iterable[str]:
    """Split text into sentences using a simple, robust regex.

    Falls back to the full text when empty.
    """
    if not text:
        return []
    sentences = _SENT_SPLIT_RE.split(text.strip())
    return [s.strip() for s in sentences if s.strip()]


def _compile_terms_mapping(mapping: Mapping[str, Iterable[str]]) -> Dict[str, re.Pattern]:
    """Compile a mapping of category -> compiled regex pattern with word boundaries."""
    compiled = {}
    for category, terms in mapping.items():
        # escape terms and join with alternation, enforce word boundaries
        escaped = [re.escape(t.strip()) for t in terms if t and t.strip()]
        if not escaped:
            continue
        pattern = r"\b(" + r"|".join(escaped) + r")\b"
        compiled[category] = re.compile(pattern, flags=re.IGNORECASE)
    return compiled


def extract_comp_techniques(row: pd.Series, mapping: Optional[Mapping[str, Iterable[str]]] = None) -> str:
    """Extrai técnicas computacionais do título/abstract usando regex com boundaries.

    Accepts an optional `mapping` to allow configuration via `config` in tests.
    """
    title = str(row.get('title', '') or '')
    abstract = str(row.get('abstract', '') or '')
    text = f"{title} {abstract}"

    if mapping is None:
        mapping = {
            'Machine Learning': ['machine learning', 'ml', 'neural network', 'deep learning'],
            'Learning Analytics': ['learning analytics', 'educational data mining'],
            'Intelligent Tutoring': ['intelligent tutoring', 'tutoring system'],
            'Adaptive Learning': ['adaptive learning', 'personalized learning'],
            'AI/Artificial Intelligence': ['artificial intelligence', 'ai'],
            'Assessment': ['assessment', 'evaluation', 'testing'],
            'Predictive Analytics': ['predictive', 'prediction', 'forecasting']
        }

    compiled = _compile_terms_mapping(mapping)
    techniques = [cat for cat, pat in compiled.items() if pat.search(text)]
    return ', '.join(techniques) if techniques else 'Não especificado'


def extract_main_results(row: pd.Series, result_terms: Optional[Iterable[str]] = None) -> str:
    """Extrai principais resultados do abstract com segmentacao de sentencas.

    Busca por sentenças que contenham palavras-chave de resultado.
    """
    abstract = str(row.get('abstract', '') or '')
    title = str(row.get('title', '') or '')

    if result_terms is None:
        result_terms = ['improved', 'increased', 'enhanced', 'better', 'effective', 'significant']

    # compile keyword regex
    kw_pat = re.compile(r"\b(" + r"|".join(re.escape(t) for t in result_terms) + r")\b", flags=re.IGNORECASE)

    sentences = list(_split_sentences(abstract))
    results = []
    for sent in sentences:
        if kw_pat.search(sent):
            results.append(sent.strip())
            if len(results) >= 2:
                break

    if results:
        return '. '.join(results)

    # fallback heuristics based on title
    if 'review' in title.lower():
        return 'Revisão da literatura sobre o tema'
    if 'system' in title.lower():
        return 'Desenvolvimento/avaliação de sistema'
    return 'Resultados não explicitamente mencionados'


def identify_gaps(row: pd.Series, gap_terms: Optional[Iterable[str]] = None) -> str:
    """Identifica lacunas mencionadas no abstract com correspondência mais robusta."""
    abstract = str(row.get('abstract', '') or '')

    if gap_terms is None:
        gap_terms = ['limitation', 'limitations', 'challenge', 'challenges', 'future work', 'further research', 'need for']

    kw_pat = re.compile(r"\b(" + r"|".join(re.escape(t) for t in gap_terms) + r")\b", flags=re.IGNORECASE)

    sentences = list(_split_sentences(abstract))
    gaps = []
    for sent in sentences:
        if kw_pat.search(sent):
            gaps.append(sent.strip())
            if len(gaps) >= 2:
                break

    return '. '.join(gaps) if gaps else 'Lacunas não explicitamente mencionadas'


def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Applies enrichment transformations to the given DataFrame.

    - Uses the project `config` when available to allow mapping overrides.
    - Safer sentence splitting and regex matching to reduce false positives.
    """
    cfg = None
    try:
        cfg = load_config()
    except Exception:
        cfg = None

    df_enriched = df.copy()

    # Relevance score: compute only if not present
    if 'relevance_score' not in df_enriched.columns:
        df_enriched['relevance_score'] = df_enriched.apply(
            lambda row: calculate_relevance_score(row.to_dict()), axis=1
        )

    # Fill missing abstracts / years
    if 'abstract' not in df_enriched.columns:
        df_enriched['abstract'] = 'Abstract não disponível'
    else:
        df_enriched['abstract'] = df_enriched['abstract'].fillna('Abstract não disponível')

    if 'year' not in df_enriched.columns:
        df_enriched['year'] = 2020
    else:
        df_enriched['year'] = df_enriched['year'].fillna(2020)

    # Determine mapping: prefer config if available
    mapping = None
    if cfg and getattr(cfg.review, 'tech_terms_map', None):
        # cfg.review.tech_terms_map expected as mapping category->list
        mapping = getattr(cfg.review, 'tech_terms_map')

    # Add extracted fields using compiled, safer methods
    df_enriched['comp_techniques'] = df_enriched.apply(lambda r: extract_comp_techniques(r, mapping), axis=1)
    df_enriched['main_results'] = df_enriched.apply(lambda r: extract_main_results(r), axis=1)
    df_enriched['identified_gaps'] = df_enriched.apply(lambda r: identify_gaps(r), axis=1)

    return df_enriched
