from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

from .config import load_config
from .db import read_papers, get_db_manager

def list_suspects(cfg=None, *, min_relevance: float = 4.0, require_edu: bool = True, limit: Optional[int] = 100) -> pd.DataFrame:
    """Return a DataFrame of suspect papers for human review.

    Criteria (simple, configurable):
    - relevance_score is not None and < min_relevance
    - OR edu_approach is missing when require_edu is True

    This function is intentionally conservative and intended for interactive review.
    """
    cfg = cfg or load_config()
    df = read_papers(cfg)
    if df.empty:
        return df

    masks = []
    if 'relevance_score' in df.columns:
        masks.append(df['relevance_score'].notna() & (df['relevance_score'] < float(min_relevance)))

    if require_edu and 'edu_approach' in df.columns:
        masks.append(df['edu_approach'].isna() | (df['edu_approach'].astype(str).str.strip() == ''))

    if not masks:
        return pd.DataFrame(columns=df.columns)

    combined = masks[0]
    for m in masks[1:]:
        combined = combined | m

    suspects = df[combined].copy()
    # Order by low relevance, then by year
    if 'relevance_score' in suspects.columns:
        suspects = suspects.sort_values(by=['relevance_score', 'year'], ascending=[True, False])
    if limit:
        suspects = suspects.head(limit)

    return suspects

def bulk_exclude(
    dois: Iterable[str],
    reason: str,
    cfg=None,
    *,
    selection_stage: str = 'screening',
    dry_run: bool = False,
) -> int:
    """Apply exclusions for a list of DOIs (or titles fallback) and persist to DB.

    If `dry_run=True`, the function returns the number of rows that *would*
    be updated, but does not perform any commits.

    Returns number of rows updated (or would be updated in dry-run).
    """
    cfg = cfg or load_config()
    manager = get_db_manager(cfg)
    updated = 0
    try:
        conn = manager._get_connection()
        cur = conn.cursor()

        for doi in dois:
            # Check existing rows by DOI or title
            cur.execute("SELECT id FROM papers WHERE doi = ? LIMIT 1", (doi,))
            row = cur.fetchone()
            if row:
                if not dry_run:
                    cur.execute(
                        "UPDATE papers SET selection_stage = ?, status = ?, exclusion_reason = ?, updated_at = datetime('now') WHERE id = ?",
                        (selection_stage, 'excluded', reason, row['id']),
                    )
                updated += 1
                continue

            # Fallback: try matching by title
            cur.execute("SELECT id FROM papers WHERE title = ? LIMIT 1", (doi,))
            row = cur.fetchone()
            if row:
                if not dry_run:
                    cur.execute(
                        "UPDATE papers SET selection_stage = ?, status = ?, exclusion_reason = ?, updated_at = datetime('now') WHERE id = ?",
                        (selection_stage, 'excluded', reason, row['id']),
                    )
                updated += 1

        if not dry_run:
            conn.commit()
    except Exception:
        # Never fail loudly from CLI helper — caller will handle messaging
        pass

    return updated

# Depreciar para que os dois venham única e exclusivamente do banco de dados
def load_dois_from_csv(path: Path) -> List[str]:
    df = pd.read_csv(path)
    if 'doi' in df.columns:
        return df['doi'].dropna().astype(str).tolist()
    # Try to fallback to title column if no doi
    if 'title' in df.columns:
        return df['title'].dropna().astype(str).tolist()
    return []
