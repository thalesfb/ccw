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
            # Create tables
            conn.execute(PAPERS_SCHEMA)
            conn.execute(SEARCHES_SCHEMA)
            conn.execute(CACHE_SCHEMA)
            conn.execute(ANALYSIS_SCHEMA)

            # Create indexes
            for index in INDEXES:
                conn.execute(index)

            # Create views
            for view in VIEWS:
                conn.execute(view)

            conn.commit()

        logger.info(f"Database initialized at {self.db_path}")

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

            # Build INSERT query
            columns = list(data.keys())
            placeholders = ["?" for _ in columns]
            query = f"""
                INSERT OR IGNORE INTO papers ({', '.join(columns)})
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
                    data = {k: v for k, v in paper.to_dict().items()
                            if v is not None}
                    columns = list(data.keys())
                    placeholders = ["?" for _ in columns]
                    query = f"""
                        INSERT OR IGNORE INTO papers ({', '.join(columns)})
                        VALUES ({', '.join(placeholders)})
                    """
                    cursor.execute(query, list(data.values()))
                    if cursor.rowcount > 0:
                        inserted += 1
                except Exception as e:
                    logger.error(f"Error inserting paper: {e}")

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
