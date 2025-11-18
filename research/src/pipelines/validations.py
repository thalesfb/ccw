from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from ..config import load_config
from ..db import read_papers


# -----------------------------
# validate_exports (DB ↔ CSV ↔ summary.json)
# -----------------------------

def _safe_int(v: Any) -> Optional[int]:
    try:
        if v is None:
            return None
        return int(float(v))
    except Exception:
        return None


def validate_exports_report(
    db_path: Optional[Path] = None,
    csv_path: Optional[Path] = None,
    summary_path: Optional[Path] = None,
) -> Dict[str, Any]:
    cfg = load_config()
    db_path = Path(db_path) if db_path else Path(cfg.database.db_path)
    csv_path = Path(csv_path) if csv_path else Path(cfg.database.exports_dir) / "analysis" / "papers.csv"
    summary_path = (
        Path(summary_path)
        if summary_path
        else Path(cfg.database.exports_dir) / "reports" / "summary.json"
    )

    report: Dict[str, Any] = {"db": {}, "csv": {}, "summary": {}, "diffs": {}, "samples": {}}

    # DB totals and samples
    if not db_path.exists():
        report["db"]["error"] = f"Missing DB at {db_path}"
    else:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        try:
            tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        except Exception:
            tables = []

        table = None
        for cand in ["papers", "papers_table", "articles", "records"]:
            if cand in tables:
                table = cand
                break
        if table is None:
            table = tables[0] if tables else None

        if table is None:
            report["db"]["error"] = "No tables found in DB"
        else:
            report["db"]["table"] = table
            try:
                total = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except Exception as e:
                total = None
                report["db"]["error_total"] = str(e)
            report["db"]["total"] = total

            # included (robust variants)
            included = None
            for v in ["included", "Included", "Incluídos", "Incluidos", "incluídos", "incluidos"]:
                try:
                    cnt = cur.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE selection_stage = ?",
                        (v,),
                    ).fetchone()[0]
                    if cnt and cnt > 0:
                        included = cnt
                        report["db"]["included_variant"] = v
                        break
                except Exception:
                    pass
            if included is None:
                try:
                    included = cur.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE LOWER(COALESCE(selection_stage,'')) LIKE '%inclu%'"
                    ).fetchone()[0]
                except Exception:
                    included = None
            report["db"]["included"] = included

            # years
            try:
                rows = cur.execute(
                    f"SELECT year, COUNT(*) FROM {table} GROUP BY year ORDER BY year"
                ).fetchall()
                dist: Dict[str, int] = {}
                for yr, c in rows:
                    if yr is None:
                        continue
                    y = _safe_int(yr)
                    key = str(y) if y is not None else str(yr)
                    dist[key] = int(c)
                report["db"]["years"] = dist
            except Exception as e:
                report["db"]["years_error"] = str(e)

            # duplicate DOIs
            try:
                rows = cur.execute(
                    f"SELECT doi, COUNT(*) FROM {table} WHERE doi IS NOT NULL AND doi != '' GROUP BY doi HAVING COUNT(*)>1 ORDER BY COUNT(*) DESC LIMIT 50"
                ).fetchall()
                report["db"]["dup_doi"] = [{"doi": r[0], "count": r[1]} for r in rows]
            except Exception as e:
                report["db"]["dup_doi_error"] = str(e)

        conn.close()

    # CSV
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path, dtype=str)
            report["csv"]["path"] = str(csv_path)
            report["csv"]["total"] = int(len(df))
            if "selection_stage" in df.columns:
                report["csv"]["included"] = int(
                    df["selection_stage"].astype(str).str.lower().str.contains("inclu").sum()
                )
            else:
                report["csv"]["included"] = None
            if "year" in df.columns:
                yrs = df["year"].map(_safe_int).dropna().astype(int)
                ydist = yrs.value_counts().sort_index().to_dict()
                report["csv"]["years"] = {str(k): int(v) for k, v in ydist.items()}
            else:
                report["csv"]["years"] = {}
            if "doi" in df.columns:
                dup = df["doi"].dropna().replace("", pd.NA)
                dup_counts = dup.value_counts()
                dup = dup_counts[dup_counts > 1].head(50)
                report["csv"]["dup_doi"] = [
                    {"doi": d, "count": int(c)} for d, c in zip(dup.index, dup.values)
                ]
            else:
                report["csv"]["dup_doi"] = []
        except Exception as e:
            report["csv"]["error"] = str(e)
    else:
        report["csv"]["error"] = f"Missing CSV at {csv_path}"

    # summary.json
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            stats = summary.get("statistics", {})
            report["summary"]["total_papers"] = stats.get("total_papers")
            report["summary"]["prisma"] = stats.get("prisma")
            report["summary"]["selection_stages"] = stats.get("selection_stages")
            report["summary"]["years"] = stats.get("years", {}).get("distribution", {})
        except Exception as e:
            report["summary"]["error"] = str(e)
    else:
        report["summary"]["error"] = f"Missing summary at {summary_path}"

    # Diffs
    report["diffs"]["total"] = {
        "db": report.get("db", {}).get("total"),
        "csv": report.get("csv", {}).get("total"),
        "summary": report.get("summary", {}).get("total_papers"),
    }
    report["diffs"]["included"] = {
        "db": report.get("db", {}).get("included"),
        "csv": report.get("csv", {}).get("included"),
        "summary_prisma_included": report.get("summary", {}).get("prisma", {}).get("included"),
    }

    # Samples
    try:
        bad_years = []
        sums = report.get("summary", {}).get("years", {}) or {}
        for y, c in sums.items():
            try:
                yy = int(y)
                if yy < 2015 or yy > 2025:
                    bad_years.append({"year": y, "count": c})
            except Exception:
                pass
        report["samples"]["summary_out_of_range_years"] = bad_years[:20]
    except Exception:
        report["samples"]["summary_out_of_range_years"] = []

    report["samples"]["csv_dup_doi_sample"] = report.get("csv", {}).get("dup_doi", [])[:10]
    report["samples"]["db_dup_doi_sample"] = report.get("db", {}).get("dup_doi", [])[:10]

    return report


# -----------------------------
# verify_papers (quality checks on CSV)
# -----------------------------

_NORMALIZE_RE = re.compile(r"[^0-9a-zA-Z]+")


def _normalize_title(s: str) -> str:
    if not isinstance(s, str):
        return ""
    t = s.lower().strip()
    t = _NORMALIZE_RE.sub(" ", t)
    return " ".join(t.split())


def _has_keyword(text: str, keywords) -> bool:
    if not isinstance(text, str):
        return False
    txt = text.lower()
    for kw in keywords:
        if kw.lower() in txt:
            return True
    return False


def verify_papers(csv_path: Path, out_path: Path) -> Dict[str, Any]:
    df = pd.read_csv(csv_path)
    total = len(df)

    df["normalized_title"] = df.get("title", "").fillna("").apply(_normalize_title)
    df["doi_clean"] = df.get("doi", "").fillna("").str.strip().str.lower()

    dup_doi_mask = df["doi_clean"] != ""
    doi_counts = df.loc[dup_doi_mask, "doi_clean"].value_counts()
    duplicated_dois = doi_counts[doi_counts > 1].index.tolist()
    df["duplicate_doi"] = df["doi_clean"].isin(duplicated_dois)

    title_counts = df["normalized_title"].value_counts()
    duplicated_titles = title_counts[title_counts > 1].index.tolist()
    df["duplicate_title"] = df["normalized_title"].isin(duplicated_titles)

    df["missing_doi"] = df.get("doi", "").isnull() | (df.get("doi", "").astype(str).str.strip() == "")
    df["missing_abstract"] = df.get("abstract", "").isnull() | (df.get("abstract", "").astype(str).str.strip() == "")

    # Primary terms from config (fallback to a small legacy list)
    cfg = load_config()
    legacy = [
        "mathematics education",
        "ensino de matemática",
        "math learning",
        "aprendizagem matemática",
        "mathematics teaching",
        "educação matemática",
    ]
    keywords = sorted({*(kw.lower() for kw in getattr(cfg.review, "keywords", []) or []), *legacy})

    df["keyword_in_title"] = df.get("title", "").fillna("").apply(lambda s: _has_keyword(s, keywords))
    df["keyword_in_abstract"] = df.get("abstract", "").fillna("").apply(lambda s: _has_keyword(s, keywords))
    df["keyword_match"] = df["keyword_in_title"] | df["keyword_in_abstract"]
    df["likely_irrelevant"] = ~df["keyword_match"]

    # Save report
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    summary = {
        "total": int(total),
        "duplicate_doi_rows": int(df["duplicate_doi"].sum()),
        "duplicate_title_rows": int(df["duplicate_title"].sum()),
        "missing_doi": int(df["missing_doi"].sum()),
        "missing_abstract": int(df["missing_abstract"].sum()),
        "likely_irrelevant": int(df["likely_irrelevant"].sum()),
        "report_path": str(out_path),
    }
    return summary


# -----------------------------
# check_exports_consistency (text report)
# -----------------------------


def _extract_stats_from_summary_html(path: Path) -> Dict[str, int]:
    txt = path.read_text(encoding="utf-8")
    stats: Dict[str, int] = {}
    h3_vals = re.findall(r"<h3>\s*([0-9,]+)\s*</h3>", txt)
    if h3_vals:
        clean = [int(v.replace(",", "")) for v in h3_vals]
        stats["total_from_summary"] = clean[0] if len(clean) > 0 else None
        stats["included_from_summary"] = clean[1] if len(clean) > 1 else None

    def find_row(label: str) -> Optional[int]:
        m = re.search(rf"{re.escape(label)}[\s\S]*?<td[^>]*>\s*([0-9,]+)\s*</td>", txt)
        if m:
            return int(m.group(1).replace(",", ""))
        return None

    stats["identification"] = find_row("Identificação") or 0
    stats["screening_approved"] = find_row("Triagem (aprovados)") or 0
    stats["screening_excluded"] = find_row("Excluídos na triagem") or 0
    stats["eligibility_approved"] = find_row("Elegibilidade (aprovados)") or 0
    stats["eligibility_excluded"] = find_row("Excluídos na elegibilidade") or 0
    stats["included_final"] = find_row("Incluídos (final)") or 0
    return stats


def check_exports_consistency(cfg=None) -> Tuple[str, str]:
    cfg = cfg or load_config()
    root = Path(__file__).resolve().parents[3]

    # DB and CSV
    df_db = read_papers(cfg)
    db_total = len(df_db)

    csv_path = Path(cfg.database.exports_dir) / "analysis" / "papers.csv"
    df_csv = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame()
    csv_total = len(df_csv)

    stage_db = (
        df_db["selection_stage"].value_counts().to_dict()
        if "selection_stage" in df_db.columns
        else {}
    )
    stage_csv = (
        df_csv["selection_stage"].value_counts().to_dict()
        if "selection_stage" in df_csv.columns
        else {}
    )
    status_db = df_db.get("status").value_counts().to_dict() if "status" in df_db.columns else {}
    status_csv = df_csv.get("status").value_counts().to_dict() if "status" in df_csv.columns else {}

    reports_dir = Path(cfg.database.exports_dir) / "reports"
    summary_html = reports_dir / "summary_report.html"
    papers_html = reports_dir / "papers_report_included.html"
    summary_stats = _extract_stats_from_summary_html(summary_html) if summary_html.exists() else {}
    papers_stats = _extract_stats_from_summary_html(papers_html) if papers_html.exists() else {}

    # Run verifier using internal function
    verifier_out = root / "research" / "logs" / "verify_papers_report.csv"
    verifier_summary: Optional[Dict[str, Any]] = None
    if csv_path.exists():
        try:
            verifier_summary = verify_papers(csv_path, verifier_out)
        except Exception as e:
            verifier_summary = {"error": str(e)}

    # Build text report
    lines = []
    lines.append("Export Consistency Report")
    lines.append("Generated by CLI validations")
    lines.append("")
    lines.append("DB vs CSV")
    lines.append(f"  DB total rows: {db_total}")
    lines.append(f"  CSV total rows: {csv_total} (path: {csv_path})")
    if db_total == csv_total:
        lines.append("  Totals match: OK")
    else:
        lines.append("  Totals MISMATCH: ❌")
        lines.append("  Suggestion: regenerate exports from DB or inspect filtering logic")

    lines.append("")
    lines.append("Selection stage distribution (DB):")
    for k, v in stage_db.items():
        lines.append(f"  {k}: {v}")
    lines.append("Selection stage distribution (CSV):")
    for k, v in stage_csv.items():
        lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("Status distribution (DB):")
    for k, v in status_db.items():
        lines.append(f"  {k}: {v}")
    lines.append("Status distribution (CSV):")
    for k, v in status_csv.items():
        lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("Summary HTML stats:")
    for k, v in summary_stats.items():
        lines.append(f"  {k}: {v}")
    lines.append("Papers report HTML stats:")
    for k, v in papers_stats.items():
        lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("Verifier summary:")
    if verifier_summary:
        for k, v in verifier_summary.items():
            lines.append(f"  {k}: {v}")
        lines.append(f"  report_csv: {verifier_out}")
    else:
        lines.append("  Not executed")

    out_path = root / "research" / "logs" / "export_consistency_report.txt"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return str(out_path), "\n".join(lines)


# -----------------------------
# regenerate summary.json
# -----------------------------


def regenerate_summary_from_db() -> Path:
    from ..analysis.reports import ReportGenerator

    cfg = load_config()
    df = read_papers(cfg)
    rg = ReportGenerator()
    rg.generate_summary_report(
        df,
        stats=None,
        config={
            "year_range": f"{cfg.review.year_min}-{cfg.review.year_max}",
            "languages": list(cfg.review.languages),
            "abstract_required": cfg.review.abstract_required,
            "relevance_threshold": cfg.review.relevance_threshold,
        },
    )
    return rg.output_dir / "summary.json"


# -----------------------------
# diagnose included (by title)
# -----------------------------


def diagnose_included(title: str) -> Dict[str, Any]:
    """Return diagnostic info for why a paper was included using current rules."""
    # Load from exports CSV
    root = Path(__file__).resolve().parents[3]
    csv_path = root / "research" / "exports" / "analysis" / "papers.csv"
    if not csv_path.exists():
        return {"error": f"exports CSV not found at {csv_path}"}
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    if "title" not in df.columns:
        return {"error": "CSV missing 'title' column"}

    matches = df[df["title"].str.contains(title, case=False, na=False)]
    if matches.empty:
        return {"error": f"No matches for title: {title}"}
    row = matches.iloc[0].to_dict()

    # Import project modules
    from ..processing.scoring import calculate_relevance_score
    from ..processing.selection import apply_prisma_selection

    # Coerce year
    year_val = 0
    try:
        if row.get("year"):
            year_val = int(float(row.get("year")))
    except Exception:
        year_val = 0

    paper = {
        "title": row.get("title", ""),
        "abstract": row.get("abstract", ""),
        "year": year_val,
        "is_open_access": row.get("is_open_access", "") in ["True", "true", "1"],
    }
    score = calculate_relevance_score(paper)
    paper["relevance_score"] = score

    df_one = pd.DataFrame([paper])
    df_one["relevance_score"] = df_one.apply(lambda r: calculate_relevance_score(r.to_dict()), axis=1)
    result_df, stats = apply_prisma_selection(df_one, min_relevance_score=4.0)

    result = {
        "input_title": title,
        "matched_title": row.get("title"),
        "doi": row.get("doi"),
        "score": float(score),
        "selection_stage": result_df.iloc[0].get("selection_stage"),
        "status": result_df.iloc[0].get("status"),
        "exclusion_reason": result_df.iloc[0].get("exclusion_reason"),
        "stats": stats,
    }
    return result
