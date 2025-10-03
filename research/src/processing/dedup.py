"""Módulo para deduplicação de artigos."""

from __future__ import annotations

import logging
from typing import List, Set, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def deduplicate_by_doi(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas baseando-se no DOI.
    
    Args:
        df: DataFrame com os artigos
        
    Returns:
        DataFrame sem duplicatas por DOI
    """
    if df.empty:
        return df
    
    initial_count = len(df)
    
    # Remover linhas com DOI vazio ou None
    df_with_doi = df[df["doi"].notna() & (df["doi"] != "")]
    df_without_doi = df[df["doi"].isna() | (df["doi"] == "")]
    
    # Deduplicar por DOI
    df_dedup = df_with_doi.drop_duplicates(subset=["doi"], keep="first")
    
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
    
    # Preprocessar títulos
    df_valid["title_clean"] = df_valid["title"].str.lower().str.strip()
    
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
    by_title: bool = True,
    title_threshold: float = 0.9
) -> pd.DataFrame:
    """Aplica todos os métodos de deduplicação em sequência.
    
    Args:
        df: DataFrame com os artigos
        by_doi: Se deve deduplicar por DOI
        by_url: Se deve deduplicar por URL
        by_title: Se deve deduplicar por similaridade de título
        title_threshold: Limiar para similaridade de título
        
    Returns:
        DataFrame deduplicado
    """
    if df.empty:
        return df
    
    initial_count = len(df)
    result = df.copy()
    
    if by_doi:
        result = deduplicate_by_doi(result)
    
    if by_url:
        result = deduplicate_by_url(result)
    
    if by_title:
        result = deduplicate_by_title_similarity(result, title_threshold)
    
    total_removed = initial_count - len(result)
    logger.info(f"Total deduplication: removed {total_removed} items ({initial_count} -> {len(result)})")
    
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
    result["is_duplicate"] = False
    result["duplicate_of"] = None
    
    # Marcar duplicatas por DOI
    if "doi" in df.columns:
        doi_counts = df["doi"].value_counts()
        duplicate_dois = doi_counts[doi_counts > 1].index
        
        for doi in duplicate_dois:
            if pd.notna(doi) and doi != "":
                indices = df[df["doi"] == doi].index
                # Marcar todos exceto o primeiro como duplicata
                for idx in indices[1:]:
                    result.loc[idx, "is_duplicate"] = True
                    result.loc[idx, "duplicate_of"] = f"DOI:{doi}"
    
    # Marcar duplicatas por URL
    if "url" in df.columns:
        url_counts = df["url"].value_counts()
        duplicate_urls = url_counts[url_counts > 1].index
        
        for url in duplicate_urls:
            if pd.notna(url) and url != "":
                indices = df[df["url"] == url].index
                # Marcar todos exceto o primeiro como duplicata
                for idx in indices[1:]:
                    if not result.loc[idx, "is_duplicate"]:
                        result.loc[idx, "is_duplicate"] = True
                        result.loc[idx, "duplicate_of"] = f"URL:{url[:50]}"
    
    duplicate_count = result["is_duplicate"].sum()
    logger.info(f"Found {duplicate_count} potential duplicates")
    
    return result
