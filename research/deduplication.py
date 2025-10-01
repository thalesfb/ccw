"""
Deduplication module for removing duplicate papers.
"""
import logging
from typing import Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from rapidfuzz import fuzz

from .config import DEDUP_RATIO_THRESHOLD, DEDUP_COSINE_THRESHOLD
from .utils import normalize_text


def _choose_best(df: pd.DataFrame, i: int, j: int) -> int:
    """
    Choose the best paper to keep between two duplicates.
    
    Rule: DOI > longer abstract
    
    Args:
        df: DataFrame containing papers
        i: Index of first paper
        j: Index of second paper
        
    Returns:
        Index of paper to remove
    """
    has_doi_i = bool(df.at[i, "doi_url"])
    has_doi_j = bool(df.at[j, "doi_url"])
    
    if not has_doi_i and has_doi_j:
        return i  # remove i
    if has_doi_i and not has_doi_j:
        return j  # remove j
    
    # Longer abstract wins
    if len(str(df.at[j, "abstract"])) > len(str(df.at[i, "abstract"])):
        return i
    return j


def deduplicate_articles(
    df: pd.DataFrame,
    logger: Optional[logging.Logger] = None,
    thresh_ratio: int = DEDUP_RATIO_THRESHOLD,
    thresh_cosine: float = DEDUP_COSINE_THRESHOLD,
) -> pd.DataFrame:
    """
    Remove duplicate articles from DataFrame.
    
    Uses two-stage approach:
    1. Remove exact DOI/URL duplicates
    2. Remove similar titles using TF-IDF and fuzzy matching
    
    Args:
        df: DataFrame with papers
        logger: Optional logger instance
        thresh_ratio: Fuzzy matching threshold (0-100)
        thresh_cosine: Cosine distance threshold for similarity
        
    Returns:
        Deduplicated DataFrame
    """
    if logger is None:
        logger = logging.getLogger("dedup")
    
    if df.empty or "title" not in df.columns:
        logger.warning("DataFrame vazio ou sem coluna 'title'.")
        return df.copy()
    
    # Stage 1: Remove DOI/URL duplicates
    df1 = df.copy()
    df1["doi_url"] = (
        df1["doi_url"].fillna("").astype(str).str.strip()
           .str.lower().str.replace("https://doi.org/", "", regex=False)
    )
    seen = {}
    keep_idx = []
    
    for idx, doi in df1["doi_url"].items():
        if doi and (doi.startswith("10.") or doi.startswith("http")):
            if doi in seen:
                continue
            seen[doi] = idx
        keep_idx.append(idx)
    
    if logger:
        logger.info(
            f"🔖 Removidas {len(df1) - len(keep_idx)} duplicatas por DOI/URL"
        )
    df2 = df1.loc[keep_idx]
    
    # Stage 2: Prepare canonical titles and blocking
    df2["_canon"] = df2["title"].fillna("").apply(normalize_text)
    df2["_block"] = df2["_canon"].str[:8]  # Short prefix for blocking
    final_keep = set(df2.index)
    
    # Stage 3: Iterate block by block
    removed_sim = 0
    for _, blk in df2.groupby("_block"):
        idx_list = blk.index.tolist()
        if len(idx_list) <= 1:
            continue
        
        # 3a. Identical canonical titles - instant drop
        canon_seen = {}
        for idx in idx_list:
            c = df2.at[idx, "_canon"]
            if c in canon_seen:
                final_keep.discard(idx)
                removed_sim += 1
            else:
                canon_seen[c] = idx
        
        idx_list = [i for i in idx_list if i in final_keep]
        if len(idx_list) <= 1:
            continue
        
        # 3b. TF-IDF + nearest neighbors within radius
        try:
            vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1).fit_transform(
                [df2.at[i, "_canon"] for i in idx_list]
            )
            nn = NearestNeighbors(
                metric="cosine", radius=thresh_cosine
            ).fit(vec)
            graph = nn.radius_neighbors_graph(vec, mode="distance")
            
            rows, cols = graph.nonzero()
            for r, c in zip(rows, cols):
                if r >= c:
                    continue  # Avoid repeated pairs
                
                i, j = idx_list[r], idx_list[c]
                
                # 3c. RapidFuzz confirmation
                ratio = fuzz.token_set_ratio(
                    df2.at[i, "_canon"],
                    df2.at[j, "_canon"]
                )
                if ratio >= thresh_ratio:
                    drop = _choose_best(df2, i, j)
                    if drop in final_keep:
                        final_keep.remove(drop)
                        removed_sim += 1
        except Exception as e:
            logger.warning(f"Erro ao processar bloco: {e}")
            continue
    
    logger.info(
        f"🪄 Removidas {removed_sim} duplicatas por similaridade de título"
    )
    result = (
        df2.loc[sorted(final_keep)]
           .drop(columns=["_canon", "_block"])
           .reset_index(drop=True)
    )
    logger.info(f"✅ Total final de artigos: {len(result)}")
    return result
