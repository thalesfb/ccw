"""Módulo para deduplicação de artigos."""

from __future__ import annotations

import logging
import re
from typing import Any, List, Set, Tuple, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def _normalize_title_for_audit(title: Any) -> str:
    """Normalize a title conservatively for duplicate-candidate counts.

    This helper is intentionally used only for an audit of possible identity
    collisions.  It must not silently turn title matches into PRISMA
    exclusions because titles such as ``Editorial`` can refer to different
    publications.
    """
    import unicodedata

    if title is None or pd.isna(title):
        return ""
    value = str(title).lower().strip()
    value = "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )
    value = "".join(char if char.isalnum() or char.isspace() else " " for char in value)
    return " ".join(value.split())


def _duplicate_group_metrics(values: pd.Series) -> dict[str, int]:
    """Return deterministic group/row/excess counts for non-empty values."""
    non_empty = values.fillna("").astype(str).str.strip()
    non_empty = non_empty[non_empty.ne("")]
    counts = non_empty.value_counts()
    repeated = counts[counts > 1]
    return {
        "non_empty_rows": int(non_empty.size),
        "distinct_values": int(counts.size),
        "repeated_groups": int(repeated.size),
        "repeated_rows": int(repeated.sum()),
        "excess_rows": int((repeated - 1).sum()),
    }


def _normalize_identity_url(url: Any) -> str:
    """Normalize a URL conservatively for exact identity comparisons."""
    if url is None or pd.isna(url):
        return ""
    return str(url).strip().lower()


def deterministic_identity_duplicate_mask(df: pd.DataFrame) -> pd.Series:
    """Return rows that are duplicate records by exact DOI/URL identity.

    Title similarity is intentionally excluded. A repeated normalized DOI
    identifies the same publication even when APIs return translated or
    differently formatted titles. URLs are used as an independent secondary
    identity key; the union is counted once when DOI and URL evidence overlap.
    Already persisted operational flags are preserved in the mask.
    """
    if df is None or df.empty:
        return pd.Series(False, index=getattr(df, "index", pd.Index([])), dtype=bool)

    mask = pd.Series(False, index=df.index, dtype=bool)
    if "is_duplicate" in df.columns:
        mask |= df["is_duplicate"].fillna(False).astype(bool)

    seen_dois: set[str] = set()
    seen_urls: set[str] = set()
    for index, row in df.iterrows():
        doi = normalize_doi(row.get("doi")) if "doi" in df.columns else ""
        url = _normalize_identity_url(row.get("url")) if "url" in df.columns else ""

        if doi and doi in seen_dois:
            mask.loc[index] = True
        if url and url in seen_urls:
            mask.loc[index] = True
        if doi:
            seen_dois.add(doi)
        if url:
            seen_urls.add(url)

    return mask


def build_identity_audit_rows(
    df: pd.DataFrame,
    retained_df: Optional[pd.DataFrame] = None,
) -> list[dict[str, Any]]:
    """Build a row-level audit of deterministic DOI/URL duplicate records.

    ``retained_df`` may be the already-deduplicated export.  When supplied,
    the audit points to the exact record that the export retained, rather
    than assuming that the first record encountered is the representative.
    This matters when a later record has a more complete abstract or a more
    advanced selection stage.
    """
    if df is None or df.empty:
        return []

    # When the caller supplies the exported unique subset, derive the audit
    # from the same retained rows.  A flagged row can legitimately be the
    # metadata winner within an identity group; in that case the first row is
    # the removed record, not the retained one.
    if retained_df is not None and not retained_df.empty:
        key_to_indices: dict[str, list[Any]] = {}
        row_keys: dict[Any, list[tuple[str, str]]] = {}
        for index, row in df.iterrows():
            keys: list[tuple[str, str]] = []
            doi = normalize_doi(row.get("doi")) if "doi" in df.columns else ""
            url = _normalize_identity_url(row.get("url")) if "url" in df.columns else ""
            if doi:
                keys.append(("doi", doi))
            if url:
                keys.append(("url", url))
            row_keys[index] = keys
            for identifier_type, identifier in keys:
                key_to_indices.setdefault(f"{identifier_type}:{identifier}", []).append(index)

        parent: dict[Any, Any] = {index: index for index in row_keys}

        def find(index: Any) -> Any:
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        def union(left: Any, right: Any) -> None:
            left_root, right_root = find(left), find(right)
            if left_root != right_root:
                parent[right_root] = left_root

        for indices in key_to_indices.values():
            for index in indices[1:]:
                union(indices[0], index)

        components: dict[Any, list[Any]] = {}
        for index in row_keys:
            components.setdefault(find(index), []).append(index)

        retained_doi = (
            retained_df["doi"].map(normalize_doi)
            if "doi" in retained_df.columns
            else pd.Series("", index=retained_df.index)
        )
        retained_url = (
            retained_df["url"].map(_normalize_identity_url)
            if "url" in retained_df.columns
            else pd.Series("", index=retained_df.index)
        )
        rows: list[dict[str, Any]] = []
        for indices in components.values():
            if len(indices) < 2:
                continue
            component_keys = {
                key for index in indices for key in row_keys[index]
            }
            candidate_mask = pd.Series(False, index=retained_df.index, dtype=bool)
            for identifier_type, identifier in component_keys:
                if identifier_type == "doi":
                    candidate_mask |= retained_doi.eq(identifier)
                else:
                    candidate_mask |= retained_url.eq(identifier)
            retained_candidates = retained_df[candidate_mask]
            if retained_candidates.empty:
                continue
            retained = retained_candidates.iloc[0]
            retained_id = retained.get("id", retained_candidates.index[0])
            for index in indices:
                row = df.loc[index]
                duplicate_id = row.get("id", index)
                if duplicate_id == retained_id:
                    continue
                keys = row_keys[index]
                shared_doi = next(
                    (identifier for identifier_type, identifier in keys
                     if (identifier_type, identifier) in component_keys
                     and identifier_type == "doi"),
                    "",
                )
                shared_url = next(
                    (identifier for identifier_type, identifier in keys
                     if (identifier_type, identifier) in component_keys
                     and identifier_type == "url"),
                    "",
                )
                identifier_type, identifier = (
                    ("doi", shared_doi) if shared_doi else ("url", shared_url)
                )
                rows.append(
                    {
                        "duplicate_id": duplicate_id,
                        "retained_id": retained_id,
                        "identifier_type": identifier_type,
                        "identifier": identifier,
                        "duplicate_title": row.get("title", ""),
                        "retained_title": retained.get("title", ""),
                        "duplicate_stage": row.get("selection_stage", ""),
                        "retained_stage": retained.get("selection_stage", ""),
                        "duplicate_status": row.get("status", ""),
                        "retained_status": retained.get("status", ""),
                        "retained_stage_source_id": retained.get(
                            "stage_source_id", retained_id
                        ),
                        "decision": "remove_duplicate_record_from_prisma_flow",
                    }
                )
        return rows

    seen_dois: dict[str, int] = {}
    seen_urls: dict[str, int] = {}
    rows: list[dict[str, Any]] = []

    for index, row in df.iterrows():
        doi = normalize_doi(row.get("doi")) if "doi" in df.columns else ""
        url = _normalize_identity_url(row.get("url")) if "url" in df.columns else ""
        retained_index = seen_dois.get(doi) if doi else None
        identifier_type = "doi" if retained_index is not None else ""
        identifier = doi if retained_index is not None else ""
        if retained_index is None and url:
            retained_index = seen_urls.get(url)
            identifier_type = "url" if retained_index is not None else ""
            identifier = url if retained_index is not None else ""
        if retained_index is not None:
            retained = df.loc[retained_index]
            if retained_df is not None and not retained_df.empty:
                retained_mask = pd.Series(False, index=retained_df.index, dtype=bool)
                if doi and "doi" in retained_df.columns:
                    retained_mask |= retained_df["doi"].map(normalize_doi).eq(doi)
                if url and "url" in retained_df.columns:
                    retained_mask |= retained_df["url"].map(_normalize_identity_url).eq(url)
                retained_candidates = retained_df[retained_mask]
                if not retained_candidates.empty:
                    retained = retained_candidates.iloc[0]
            rows.append(
                {
                    "duplicate_id": row.get("id", index),
                    "retained_id": retained.get("id", retained_index),
                    "identifier_type": identifier_type,
                    "identifier": identifier,
                    "duplicate_title": row.get("title", ""),
                    "retained_title": retained.get("title", ""),
                    "duplicate_stage": row.get("selection_stage", ""),
                    "retained_stage": retained.get("selection_stage", ""),
                    "duplicate_status": row.get("status", ""),
                    "retained_status": retained.get("status", ""),
                    "decision": "remove_duplicate_record_from_prisma_flow",
                }
            )
        if doi and doi not in seen_dois:
            seen_dois[doi] = index
        if url and url not in seen_urls:
            seen_urls[url] = index

    return rows


def audit_duplicate_candidates(df: pd.DataFrame) -> dict[str, Any]:
    """Audit possible identity collisions without changing the DataFrame.

    The returned counts separate deterministic DOI/URL identity removals from
    weaker normalized-title candidates. A semantic disposition is still
    required for title-only clusters and unusual version relationships.
    """
    if df is None or df.empty:
        return {
            "raw_rows": 0,
            "operationally_flagged_rows": 0,
            "deterministic_identity_duplicate_rows": 0,
            "confirmed_semantic_duplicates": 0,
            "doi": _duplicate_group_metrics(pd.Series(dtype=object)),
            "url": _duplicate_group_metrics(pd.Series(dtype=object)),
            "title": _duplicate_group_metrics(pd.Series(dtype=object)),
            "title_only": _duplicate_group_metrics(pd.Series(dtype=object)),
            "interpretation": (
                "No rows are available. Candidate counts do not represent "
                "confirmed removals."
            ),
        }

    result: dict[str, Any] = {
        "raw_rows": int(len(df)),
        "operationally_flagged_rows": (
            int(df["is_duplicate"].fillna(False).astype(bool).sum())
            if "is_duplicate" in df.columns
            else 0
        ),
        "deterministic_identity_duplicate_rows": int(
            deterministic_identity_duplicate_mask(df).sum()
        ),
        "confirmed_semantic_duplicates": 0,
    }

    if "doi" in df.columns:
        result["doi"] = _duplicate_group_metrics(
            df["doi"].map(normalize_doi)
        )
    else:
        result["doi"] = _duplicate_group_metrics(pd.Series(dtype=object))

    if "url" in df.columns:
        result["url"] = _duplicate_group_metrics(
            df["url"].map(_normalize_identity_url)
        )
    else:
        result["url"] = _duplicate_group_metrics(pd.Series(dtype=object))

    if "title" in df.columns:
        normalized_titles = df["title"].map(_normalize_title_for_audit)
        result["title"] = _duplicate_group_metrics(normalized_titles)

        # The raw title metric includes rows already identified by an exact
        # DOI/URL collision.  Report the weaker, non-identity candidates
        # separately so a title count is not presented as an additional
        # removal or as 257 independent candidates in the current snapshot.
        identity_mask = deterministic_identity_duplicate_mask(df)
        result["title_only"] = _duplicate_group_metrics(
            normalized_titles[~identity_mask]
        )
    else:
        result["title"] = _duplicate_group_metrics(pd.Series(dtype=object))
        result["title_only"] = _duplicate_group_metrics(pd.Series(dtype=object))

    result["interpretation"] = (
        "Exact normalized DOI/URL identity rows are removed deterministically "
        "from the PRISMA flow; normalized-title counts remain weaker candidates "
        "for semantic review because versioned records and unrelated works must "
        "remain distinct. The title metric includes identity-overlap rows; "
        "title_only is calculated after deterministic identity removal."
    )
    return result


def normalize_doi(doi: Optional[str]) -> str:
    """Normalize a DOI string for identity comparisons.

    The normalization accepts the common ``doi:`` and DOI resolver forms and
    removes citation punctuation that is appended after a DOI in prose. It
    deliberately does not perform fuzzy matching: the result is still an
    exact identity key.

    Args:
        doi: DOI string to normalize

    Returns:
        Normalized DOI string
    """
    if doi is None:
        return ""
    d = str(doi).strip().lower()
    d = re.sub(r"^doi:\s*", "", d)
    d = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", d)
    d = re.sub(r"[\s.,;:]+$", "", d)
    return d.strip()


def deduplicate_by_doi(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas baseando-se no DOI normalizado.

    Args:
        df: DataFrame com os artigos

    Returns:
        DataFrame sem duplicatas por DOI
    """
    if df.empty:
        return df

    initial_count = len(df)

    # Normalizar DOIs
    df = df.copy()
    df['doi_normalized'] = df.get('doi', '').fillna('').astype(str).apply(normalize_doi)

    # Remover linhas com DOI vazio ou None
    df_with_doi = df[df["doi_normalized"] != ""]
    df_without_doi = df[df["doi_normalized"] == ""]

    # Deduplicar por DOI normalizado (case-insensitive, sem prefixo 'doi:')
    df_dedup = df_with_doi.drop_duplicates(subset=["doi_normalized"], keep="first")
    df_dedup = df_dedup.drop(columns=['doi_normalized'])

    # Remover coluna temporária de df_without_doi também
    df_without_doi = df_without_doi.drop(columns=['doi_normalized'])

    # Combinar com artigos sem DOI
    result = pd.concat([df_dedup, df_without_doi], ignore_index=True)

    removed = initial_count - len(result)
    logger.info(f"Removed {removed} duplicates by DOI ({initial_count} -> {len(result)})")

    return result


def deduplicate_by_url(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas baseando-se na URL.

    Args:
        df: DataFrame com os artigos

    Returns:
        DataFrame sem duplicatas por URL
    """
    if df.empty:
        return df

    initial_count = len(df)

    # Remover linhas com URL vazia ou None
    df_with_url = df[df["url"].notna() & (df["url"] != "")]
    df_without_url = df[df["url"].isna() | (df["url"] == "")]

    # Deduplicar por URL
    df_dedup = df_with_url.drop_duplicates(subset=["url"], keep="first")

    # Combinar com artigos sem URL
    result = pd.concat([df_dedup, df_without_url], ignore_index=True)

    removed = initial_count - len(result)
    logger.info(f"Removed {removed} duplicates by URL ({initial_count} -> {len(result)})")

    return result


def deduplicate_by_title_similarity(
    df: pd.DataFrame,
    threshold: float = 0.9,
    batch_size: int = 1000
) -> pd.DataFrame:
    """Remove duplicatas baseando-se na similaridade de títulos usando TF-IDF.

    Args:
        df: DataFrame com os artigos
        threshold: Limiar de similaridade (0-1) para considerar duplicata
        batch_size: Tamanho do batch para processamento (evita memória excessiva)

    Returns:
        DataFrame sem duplicatas por título similar
    """
    if df.empty or "title" not in df.columns:
        return df

    initial_count = len(df)

    # Filtrar títulos válidos
    df_valid = df[df["title"].notna() & (df["title"] != "")].copy()
    df_invalid = df[df["title"].isna() | (df["title"] == "")]

    if len(df_valid) == 0:
        return df

    # Preprocessar títulos: normalizar case, remover diacríticos e pontuação, colapsar espaços
    def _normalize_title(t: str) -> str:
        import unicodedata
        s = str(t).lower().strip()
        # Remover diacríticos (á -> a)
        s = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
        # Remover pontuação
        s = ''.join(ch if ch.isalnum() or ch.isspace() else ' ' for ch in s)
        # Colapsar espaços múltiplos
        s = ' '.join(s.split())
        return s

    df_valid = df_valid.copy()
    df_valid["title_clean"] = df_valid["title"].apply(_normalize_title)

    # Processar em batches para datasets grandes
    duplicates_to_remove = set()

    for start_idx in range(0, len(df_valid), batch_size):
        end_idx = min(start_idx + batch_size, len(df_valid))
        batch = df_valid.iloc[start_idx:end_idx]

        if len(batch) < 2:
            continue

        # Vetorizar títulos
        vectorizer = TfidfVectorizer(
            min_df=1,
            analyzer='char_wb',
            ngram_range=(2, 4),
            lowercase=True
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(batch["title_clean"])

            # Calcular similaridade
            similarity_matrix = cosine_similarity(tfidf_matrix)

            # Encontrar duplicatas
            for i in range(len(similarity_matrix)):
                for j in range(i + 1, len(similarity_matrix)):
                    if similarity_matrix[i, j] >= threshold:
                        # Marcar o índice com menos informações como duplicata
                        idx_i = batch.index[i]
                        idx_j = batch.index[j]

                        # Preferir manter o que tem mais campos preenchidos
                        count_i = df_valid.loc[idx_i].notna().sum()
                        count_j = df_valid.loc[idx_j].notna().sum()

                        if count_i >= count_j:
                            duplicates_to_remove.add(idx_j)
                        else:
                            duplicates_to_remove.add(idx_i)

        except Exception as e:
            logger.warning(f"Error in similarity calculation: {e}")
            continue

    # Remover duplicatas identificadas
    df_dedup = df_valid[~df_valid.index.isin(duplicates_to_remove)]
    df_dedup = df_dedup.drop(columns=["title_clean"])

    # Combinar com artigos sem título válido
    result = pd.concat([df_dedup, df_invalid], ignore_index=True)

    removed = initial_count - len(result)
    logger.info(f"Removed {removed} duplicates by title similarity ({initial_count} -> {len(result)})")

    return result


def deduplicate(
    df: pd.DataFrame,
    by_doi: bool = True,
    by_url: bool = True,
    by_title: bool = False,
    title_threshold: float = 0.9
) -> pd.DataFrame:
    """Aplica deduplicação de identidade; título só com habilitação explícita.

    O fluxo PRISMA canônico usa DOI/URL como identidade determinística. A
    similaridade de título é apenas uma etapa exploratória de auditoria e não
    deve remover registros por padrão, pois títulos parecidos não provam que
    duas linhas representam a mesma publicação.

    Args:
        df: DataFrame com os artigos
        by_doi: Se deve deduplicar por DOI
        by_url: Se deve deduplicar por URL
        by_title: Se deve habilitar explicitamente a deduplicação exploratória
            por similaridade de título (padrão: ``False``)
        title_threshold: Limiar para similaridade de título

    Returns:
        DataFrame deduplicado
    """
    if df.empty:
        return df

    initial_count = len(df)
    result = df.copy()

    removed_by_doi = 0
    removed_by_url = 0
    removed_by_title = 0

    if by_doi:
        before = len(result)
        result = deduplicate_by_doi(result)
        removed_by_doi = before - len(result)

    if by_url:
        before = len(result)
        result = deduplicate_by_url(result)
        removed_by_url = before - len(result)

    if by_title:
        before = len(result)
        result = deduplicate_by_title_similarity(result, title_threshold)
        removed_by_title = before - len(result)

    total_removed = initial_count - len(result)
    logger.info(f"Total deduplication: removed {total_removed} items ({initial_count} -> {len(result)})")

    # Record deduplication statistics on the returned DataFrame (pandas attrs)
    try:
        result.attrs = getattr(result, 'attrs', {}) or {}
        result.attrs['dedup_stats'] = {
            'initial_count': int(initial_count),
            'removed_by_doi': int(removed_by_doi),
            'removed_by_url': int(removed_by_url),
            'removed_by_title': int(removed_by_title),
            'total_removed': int(total_removed),
        }
    except Exception:
        # Non-fatal: if attrs can't be written, just continue
        logger.debug("Could not attach dedup_stats to DataFrame.attrs")

    return result


def find_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Identifica possíveis duplicatas sem removê-las.

    Args:
        df: DataFrame com os artigos

    Returns:
        DataFrame com colunas adicionais indicando duplicatas
    """
    if df.empty:
        return df

    result = df.copy()
    existing_flags = (
        df["is_duplicate"].fillna(False).astype(bool)
        if "is_duplicate" in df.columns
        else pd.Series(False, index=df.index)
    )
    result["is_duplicate"] = existing_flags
    if "duplicate_of" not in result.columns:
        result["duplicate_of"] = pd.Series(None, index=df.index, dtype=object)
    else:
        result["duplicate_of"] = result["duplicate_of"].astype(object)

    # Marcar duplicatas por DOI (case-insensitive)
    if "doi" in df.columns:
        # Normalizar DOIs para comparação case-insensitive
        result['doi_normalized'] = result.get('doi', '').fillna('').astype(str).apply(normalize_doi)

        # Contar DOIs normalizados (ignorar vazios)
        doi_counts = result[result['doi_normalized'] != '']['doi_normalized'].value_counts()
        duplicate_dois = doi_counts[doi_counts > 1].index

        for doi_norm in duplicate_dois:
            if doi_norm != "":
                # Encontrar todos os índices com esse DOI normalizado
                indices = result[result['doi_normalized'] == doi_norm].index.tolist()
                # Marcar todos exceto o primeiro como duplicata
                first_idx = indices[0]
                for idx in indices[1:]:
                    result.loc[idx, "is_duplicate"] = True
                    # Usar o DOI original do primeiro registro como referência
                    result.loc[idx, "duplicate_of"] = f"DOI:{result.loc[first_idx, 'doi']}"

        # Remover coluna temporária
        result = result.drop(columns=['doi_normalized'])

    # Marcar duplicatas por URL
    if "url" in df.columns:
        normalized_urls = df["url"].map(_normalize_identity_url)
        url_counts = normalized_urls.value_counts()
        duplicate_urls = url_counts[url_counts > 1].index

        for url in duplicate_urls:
            if pd.notna(url) and url != "":
                indices = normalized_urls[normalized_urls == url].index
                # Marcar todos exceto o primeiro como duplicata
                for idx in indices[1:]:
                    if not result.loc[idx, "is_duplicate"]:
                        result.loc[idx, "is_duplicate"] = True
                        result.loc[idx, "duplicate_of"] = f"URL:{url}"

    duplicate_count = result["is_duplicate"].sum()
    logger.info(f"Found {duplicate_count} potential duplicates")

    return result
