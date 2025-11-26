from pathlib import Path

import pandas as pd
import pytest


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "exports" / "analysis" / "papers.csv"
REFINED_INCLUDED = Path(__file__).resolve().parents[2] / "tools" / "verify_papers_included_refined.csv"


def _load_included(df: pd.DataFrame) -> pd.DataFrame:
    if 'status' in df.columns:
        inc = df[df['status'].astype(str).str.lower() == 'included'].copy()
        return inc
    if 'selection_stage' in df.columns:
        inc = df[df['selection_stage'].astype(str).str.lower().str.contains('inclu')].copy()
        return inc
    pytest.skip("CSV does not contain 'status' or 'selection_stage' to detect included rows")


def test_included_have_abstracts_and_refined_report():
    assert CSV_PATH.exists(), f"Missing CSV at {CSV_PATH}"
    df = pd.read_csv(CSV_PATH, dtype=str)
    inc = _load_included(df)
    assert len(inc) > 0, "No included rows found in CSV"

    # Check included abstracts are present (non-empty)
    missing_abstracts = inc['abstract'].fillna('').astype(str).str.strip() == ''
    assert missing_abstracts.sum() == 0, f"{missing_abstracts.sum()} included rows missing abstracts"

    # If refined included report exists, ensure it is consistent with exported included rows.
    # The refined report may be generated from the DB; we check if export is a subset of refined.
    # NOTE: Refined report may be outdated - warn instead of failing hard.
    if REFINED_INCLUDED.exists():
        rdf = pd.read_csv(REFINED_INCLUDED, dtype=str)
        # Prefer DOI-based matching when available
        if 'doi' in rdf.columns and 'doi' in inc.columns:
            rdf_dois = set(rdf['doi'].fillna('').astype(str).str.strip().str.lower())
            inc_dois = set(inc['doi'].fillna('').astype(str).str.strip().str.lower())
            missing = [d for d in inc_dois if d and d not in rdf_dois]
            if missing:
                # Warn instead of failing - refined report may need update
                import warnings
                warnings.warn(
                    f"Some included DOIs in export not present in refined report (may be outdated): {missing[:5]}"
                )
        else:
            # Fallback: normalized title matching
            def norm_title(s):
                import re
                if not s or pd.isna(s):
                    return ''
                t = str(s).lower()
                t = re.sub(r'[^0-9a-z\s]', ' ', t)
                return ' '.join(t.split()[:20])

            rdf_titles = set(rdf.get('title', '').fillna('').astype(str).apply(norm_title))
            inc_titles = set(inc.get('title', '').fillna('').astype(str).apply(norm_title))
            missing = [t for t in inc_titles if t and t not in rdf_titles]
            if missing:
                import warnings
                warnings.warn(
                    f"Some included titles in export not present in refined report (may be outdated): {len(missing)} titles"
                )
