"""Database manager for systematic review."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from ..config import AppConfig, load_config
from .schema import (
    ANALYSIS_SCHEMA,
    CACHE_SCHEMA,
    INDEXES,
    PAPERS_SCHEMA,
    PaperRecord,
    SEARCHES_SCHEMA,
    VIEWS,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages all database operations for the systematic review."""

    def __init__(self, config: Optional[AppConfig] = None):
        """Initialize database manager.

        Args:
            config: Application configuration
        """
        self.config = config or load_config()
        self.db_path = Path(self.config.database.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_database(self):
        """Initialize database with all tables, indexes and views."""
        with self._get_connection() as conn:
            # Create tables (idempotent)
            conn.execute(PAPERS_SCHEMA)
            conn.execute(SEARCHES_SCHEMA)
            conn.execute(CACHE_SCHEMA)
            conn.execute(ANALYSIS_SCHEMA)

            # Attempt schema migration to non-destructive dedup strategy
            self._migrate_schema_if_needed(conn)

            # Create indexes
            for index in INDEXES:
                conn.execute(index)

            # Create views
            for view in VIEWS:
                conn.execute(view)

            conn.commit()

        logger.info(f"Database initialized at {self.db_path}")

    def _migrate_schema_if_needed(self, conn: sqlite3.Connection) -> None:
        """Migrate existing schema to remove UNIQUE on DOI and add duplicate flags.

        - If current papers table definition contains UNIQUE on doi, rebuild table without UNIQUE.
        - Ensure columns `is_duplicate` and `duplicate_of` exist.
        """
        cur = conn.cursor()
        # Check current table SQL
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='papers'")
        row = cur.fetchone()
        current_sql = (row[0] or "") if row else ""

        # Add missing columns if needed (cheap migration)
        def _has_column(name: str) -> bool:
            cur.execute("PRAGMA table_info(papers)")
            return any(col[1] == name for col in cur.fetchall())

        try:
            if not _has_column("is_duplicate"):
                cur.execute("ALTER TABLE papers ADD COLUMN is_duplicate BOOLEAN DEFAULT 0")
            if not _has_column("duplicate_of"):
                cur.execute("ALTER TABLE papers ADD COLUMN duplicate_of TEXT")
        except Exception:
            # If table doesn't exist yet, ignore; it will be created by PAPERS_SCHEMA
            pass

        # If UNIQUE still present on DOI, rebuild table without UNIQUE
        if "UNIQUE" in current_sql.upper():
            logger.info("Migrating 'papers' table to remove UNIQUE constraint on DOI (non-destructive dedup)")
            
            # Temporarily disable foreign key enforcement during migration
            cur.execute("PRAGMA foreign_keys = OFF")
            
            # Create new table with desired schema
            cur.execute("ALTER TABLE papers RENAME TO papers_old")
            cur.execute(PAPERS_SCHEMA)

            # Determine shared columns between old and new schemas
            cur.execute("PRAGMA table_info(papers_old)")
            old_cols = [r[1] for r in cur.fetchall()]
            cur.execute("PRAGMA table_info(papers)")
            new_cols = [r[1] for r in cur.fetchall()]
            shared_cols = [c for c in old_cols if c in new_cols]

            # Build insert selecting shared columns; add defaults for new columns if missing
            insert_cols = ", ".join(shared_cols)
            select_cols = ", ".join(shared_cols)
            cur.execute(f"INSERT INTO papers ({insert_cols}) SELECT {select_cols} FROM papers_old")
            cur.execute("DROP TABLE papers_old")
            
            # Re-enable foreign key enforcement
            cur.execute("PRAGMA foreign_keys = ON")
            conn.commit()

    # ============= Paper Operations =============

    def insert_paper(self, paper: PaperRecord) -> int:
        """Insert a single paper into the database.

        Args:
            paper: Paper record to insert

        Returns:
            ID of inserted paper
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Convert to dict and remove None values
            data = {k: v for k, v in paper.to_dict().items() if v is not None}

            # Build INSERT query (no IGNORE: we keep all records, mark duplicates later)
            columns = list(data.keys())
            placeholders = ["?" for _ in columns]
            query = f"""
                INSERT INTO papers ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
            """

            cursor.execute(query, list(data.values()))
            conn.commit()

            return cursor.lastrowid

    def insert_papers_bulk(self, papers: List[PaperRecord]) -> int:
        """Insert multiple papers in bulk.

        Args:
            papers: List of paper records

        Returns:
            Number of papers inserted
        """
        if not papers:
            return 0

        with self._get_connection() as conn:
            cursor = conn.cursor()
            inserted = 0

            for paper in papers:
                try:
                    data = {k: v for k, v in paper.to_dict().items() if v is not None}

                    # Always insert; do not upsert by DOI/title to avoid overwriting duplicates
                    if data:
                        columns = list(data.keys())
                        placeholders = ["?" for _ in columns]
                        insert_sql = f"""
                            INSERT INTO papers ({', '.join(columns)})
                            VALUES ({', '.join(placeholders)})
                        """
                        cursor.execute(insert_sql, list(data.values()))
                        if cursor.rowcount > 0:
                            inserted += 1

                    # # 2) Atualiza campos críticos se já existia (upsert por DOI/título)
                    # update_candidates = {
                    #     k: v for k, v in data.items() if k in {
                    #         "selection_stage", "status", "exclusion_reason", "inclusion_criteria_met",
                    #         "relevance_score", "comp_techniques", "edu_approach", "study_type", "eval_methods"
                    #     }
                    # }
                    # if update_candidates:
                    #     update_candidates["updated_at"] = datetime.now().isoformat()

                    #     if data.get("doi"):
                    #         set_clause = ", ".join([f"{k} = ?" for k in update_candidates.keys()])
                    #         params = list(update_candidates.values()) + [data["doi"]]
                    #         cursor.execute(
                    #             f"UPDATE papers SET {set_clause} WHERE doi = ?",
                    #             params
                    #         )
                    #     elif data.get("title"):
                    #         # fallback por título quando não há DOI (melhor esforço)
                    #         set_clause = ", ".join([f"{k} = ?" for k in update_candidates.keys()])
                    #         params = list(update_candidates.values()) + [data["title"]]
                    #         cursor.execute(
                    #             f"UPDATE papers SET {set_clause} WHERE title = ?",
                    #             params
                    #         )

                except Exception as e:
                    logger.error(f"Error inserting/updating paper: {e}")

            conn.commit()

        logger.info(f"Inserted {inserted} papers")
        return inserted

    def get_papers(
        self,
        selection_stage: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """Get papers from database with optional filters.

        Args:
            selection_stage: Filter by selection stage
            status: Filter by status
            limit: Limit number of results

        Returns:
            DataFrame with papers
        """
        query = "SELECT * FROM papers WHERE 1=1"
        params = []

        if selection_stage:
            query += " AND selection_stage = ?"
            params.append(selection_stage)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY relevance_score DESC, year DESC"

        if limit:
            query += f" LIMIT {limit}"

        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=params)

        return df

    def update_paper(self, paper_id: int, updates: Dict[str, Any]) -> bool:
        """Update a paper record.

        Args:
            paper_id: ID of paper to update
            updates: Dictionary of fields to update

        Returns:
            True if successful
        """
        if not updates:
            return False

        # Add updated_at timestamp
        updates["updated_at"] = datetime.now().isoformat()

        # Build UPDATE query
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE papers SET {set_clause} WHERE id = ?"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, list(updates.values()) + [paper_id])
            conn.commit()

            return cursor.rowcount > 0

    def update_selection_stage(
        self,
        paper_ids: List[int],
        stage: str,
        exclusion_reason: Optional[str] = None
    ) -> int:
        """Update selection stage for multiple papers.

        Args:
            paper_ids: List of paper IDs
            stage: New selection stage
            exclusion_reason: Reason for exclusion (if applicable)

        Returns:
            Number of papers updated
        """
        if not paper_ids:
            return 0

        updates = {
            "selection_stage": stage,
            "updated_at": datetime.now().isoformat()
        }

        if exclusion_reason:
            updates["exclusion_reason"] = exclusion_reason

        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        placeholders = ", ".join(["?" for _ in paper_ids])
        query = f"UPDATE papers SET {set_clause} WHERE id IN ({placeholders})"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, list(updates.values()) + paper_ids)
            conn.commit()

            return cursor.rowcount

    # ============= Cache Operations =============

    def get_cached_results(self, query_hash: str, api: str) -> Optional[List[Dict]]:
        """Get cached results for a query.

        Args:
            query_hash: Hash of the query
            api: API name

        Returns:
            Cached results or None
        """
        query = """
            SELECT results FROM cache 
            WHERE query_hash = ? AND api = ?
            AND (expires_at IS NULL OR expires_at > datetime('now'))
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (query_hash, api))
            row = cursor.fetchone()

            if row and row["results"]:
                # Update hit count
                cursor.execute(
                    "UPDATE cache SET hit_count = hit_count + 1 WHERE query_hash = ?",
                    (query_hash,)
                )
                conn.commit()

                return json.loads(row["results"])

        return None

    def save_cache(
        self,
        query_hash: str,
        query_text: str,
        api: str,
        results: List[Dict],
        expires_in_hours: int = 24
    ):
        """Save results to cache.

        Args:
            query_hash: Hash of the query
            query_text: Original query text
            api: API name
            results: Results to cache
            expires_in_hours: Hours until expiration
        """
        query = """
            INSERT OR REPLACE INTO cache 
            (query_hash, query, api, results, expires_at)
            VALUES (?, ?, ?, ?, datetime('now', '+' || ? || ' hours'))
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (query_hash, query_text, api, json.dumps(results), expires_in_hours)
            )
            conn.commit()

    # ============= Search Log Operations =============

    def log_search(
        self,
        query: str,
        api: str,
        results_count: int,
        filtered_count: int,
        status: str = "success",
        error_message: Optional[str] = None
    ):
        """Log a search operation.

        Args:
            query: Search query
            api: API used
            results_count: Total results
            filtered_count: Filtered results
            status: Status of search
            error_message: Error message if failed
        """
        query_sql = """
            INSERT INTO searches 
            (query, api, results_count, filtered_count, status, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query_sql,
                (query, api, results_count, filtered_count, status, error_message)
            )
            conn.commit()

    # ============= Analysis Operations =============

    def save_analysis(
        self,
        paper_id: int,
        analysis_type: str,
        results: Dict,
        confidence: Optional[float] = None
    ):
        """Save analysis results for a paper.

        Args:
            paper_id: ID of analyzed paper
            analysis_type: Type of analysis
            results: Analysis results
            confidence: Confidence score
        """
        query = """
            INSERT INTO analysis 
            (paper_id, analysis_type, results, confidence)
            VALUES (?, ?, ?, ?)
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (paper_id, analysis_type, json.dumps(results), confidence)
            )
            conn.commit()

    def save_search_log(
        self,
        query_summary: str,
        results_summary: Dict[str, Any]
    ):
        """Save search execution log.

        Args:
            query_summary: Summary of the search query
            results_summary: Dictionary with results summary
        """
        query = """
            INSERT INTO searches 
            (query_summary, results_summary)
            VALUES (?, ?)
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (query_summary, json.dumps(results_summary))
            )
            conn.commit()

    # ============= Statistics Operations =============

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics.

        Returns:
            Dictionary with statistics
        """
        stats = {}

        with self._get_connection() as conn:
            # Total papers
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM papers")
            stats["total_papers"] = cursor.fetchone()["total"]

            # Papers by stage
            cursor.execute("""
                SELECT selection_stage, COUNT(*) as count
                FROM papers
                GROUP BY selection_stage
            """)
            stats["by_stage"] = {row["selection_stage"]                                 : row["count"] for row in cursor}

            # Papers by year
            cursor.execute("""
                SELECT year, COUNT(*) as count
                FROM papers
                WHERE year IS NOT NULL
                GROUP BY year
                ORDER BY year DESC
                LIMIT 10
            """)
            stats["by_year"] = {row["year"]: row["count"] for row in cursor}

            # Papers by database
            cursor.execute("""
                SELECT database, COUNT(*) as count
                FROM papers
                GROUP BY database
            """)
            stats["by_database"] = {row["database"]                                    : row["count"] for row in cursor}

            # Cache statistics
            cursor.execute("""
                SELECT COUNT(*) as total, SUM(hit_count) as hits
                FROM cache
            """)
            cache_stats = cursor.fetchone()
            stats["cache"] = {
                "total_entries": cache_stats["total"],
                "total_hits": cache_stats["hits"] or 0
            }

        return stats

    def export_to_dataframe(self, table: str = "papers") -> pd.DataFrame:
        """Export table to DataFrame.

        Args:
            table: Table name to export

        Returns:
            DataFrame with table data
        """
        with self._get_connection() as conn:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

        return df

    def get_last_search_results(self) -> Optional[Dict[str, Any]]:
        """Return the results_summary JSON from the most recent entry in searches, if any."""
        query = "SELECT results_summary FROM searches ORDER BY rowid DESC LIMIT 1"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if row and row["results_summary"]:
                try:
                    return json.loads(row["results_summary"])
                except Exception:
                    return None
        return None

    # ============= Maintenance Utilities =============
    def normalize_prisma_stages(self) -> Dict[str, int]:
        """Normalize legacy selection_stage values into PRISMA-compliant stages.

        - 'screening_excluded'  -> selection_stage='screening',   status='excluded'
        - 'eligibility_excluded'-> selection_stage='eligibility', status='excluded'

        Returns:
            Dict with number of rows updated per rule.
        """
        results = {"screening": 0, "eligibility": 0}
        with self._get_connection() as conn:
            cur = conn.cursor()

            # Screening legacy
            cur.execute(
                """
                UPDATE papers
                SET selection_stage='screening',
                    status=COALESCE(NULLIF(status,''), 'excluded'),
                    updated_at = datetime('now')
                WHERE selection_stage='screening_excluded'
                """
            )
            results["screening"] = cur.rowcount

            # Eligibility legacy
            cur.execute(
                """
                UPDATE papers
                SET selection_stage='eligibility',
                    status=COALESCE(NULLIF(status,''), 'excluded'),
                    updated_at = datetime('now')
                WHERE selection_stage='eligibility_excluded'
                """
            )
            results["eligibility"] = cur.rowcount

            conn.commit()

        logger.info(
            f"Normalized PRISMA stages: screening={results['screening']}, eligibility={results['eligibility']}"
        )
        return results

    def normalize_consistency(self) -> Dict[str, int]:
        """Normalize and align PRISMA-related fields for consistency.

        - Fix legacy stages via normalize_prisma_stages
        - Ensure rows with status='included' also have selection_stage='included'

        Returns:
            Dict with counters of updated rows per rule.
        """
        counters = {"legacy_fixed": 0, "included_aligned": 0}
        try:
            legacy = self.normalize_prisma_stages()
            counters["legacy_fixed"] = sum(legacy.values())
        except Exception:
            # Best-effort; continue
            pass

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE papers
                SET selection_stage = 'included',
                    updated_at = datetime('now')
                WHERE LOWER(COALESCE(status,'')) = 'included'
                  AND LOWER(COALESCE(selection_stage,'')) != 'included'
                """
            )
            counters["included_aligned"] = cur.rowcount
            conn.commit()

        if any(counters.values()):
            logger.info(
                f"Normalized consistency: legacy_fixed={counters['legacy_fixed']}, "
                f"included_aligned={counters['included_aligned']}"
            )
        return counters
