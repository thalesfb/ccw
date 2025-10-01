"""
SQLite database manager for systematic review.
"""
import sqlite3
import logging
from typing import List
import pandas as pd

from .config import PAPER_COLUMNS
from .models import Paper


class DatabaseManager:
    """Manager for SQLite database operations."""
    
    def __init__(self, db_path: str = "research/systematic_review.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = logging.getLogger("database")
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create papers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                authors TEXT,
                year INTEGER,
                source_publication TEXT,
                abstract TEXT,
                full_text TEXT,
                doi_url TEXT,
                database TEXT,
                search_terms TEXT,
                is_open_access BOOLEAN,
                country TEXT,
                study_type TEXT,
                comp_techniques TEXT,
                eval_methods TEXT,
                math_topic TEXT,
                main_results TEXT,
                identified_gaps TEXT,
                relevance_score INTEGER,
                selection_stage TEXT,
                exclusion_reason TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on DOI for faster deduplication
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_doi_url ON papers(doi_url)
        """)
        
        # Create index on title for faster searching
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_title ON papers(title)
        """)
        
        conn.commit()
        conn.close()
        self.logger.info(f"Database initialized at {self.db_path}")
    
    def save_papers(self, papers: List[Paper]) -> int:
        """
        Save papers to database.
        
        Args:
            papers: List of Paper objects
            
        Returns:
            Number of papers saved
        """
        if not papers:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for paper in papers:
            # Check if paper already exists
            cursor.execute(
                "SELECT id FROM papers WHERE doi_url = ? OR title = ?",
                (paper.doi_url, paper.title)
            )
            if cursor.fetchone():
                self.logger.debug(f"Paper already exists: {paper.title[:60]}")
                continue
            
            # Insert paper
            cursor.execute("""
                INSERT INTO papers (
                    title, authors, year, source_publication, abstract,
                    full_text, doi_url, database, search_terms, is_open_access,
                    country, study_type, comp_techniques, eval_methods,
                    math_topic, main_results, identified_gaps, relevance_score,
                    selection_stage, exclusion_reason, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.title, paper.authors, paper.year, paper.source_publication,
                paper.abstract, paper.full_text, paper.doi_url, paper.database,
                paper.search_terms, paper.is_open_access, paper.country,
                paper.study_type, paper.comp_techniques, paper.eval_methods,
                paper.math_topic, paper.main_results, paper.identified_gaps,
                paper.relevance_score, paper.selection_stage,
                paper.exclusion_reason, paper.notes
            ))
            saved_count += 1
        
        conn.commit()
        conn.close()
        self.logger.info(f"Saved {saved_count} papers to database")
        return saved_count
    
    def load_papers(
        self,
        database: str = None,
        year_min: int = None
    ) -> pd.DataFrame:
        """
        Load papers from database.
        
        Args:
            database: Filter by database name
            year_min: Filter by minimum year
            
        Returns:
            DataFrame with papers
        """
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM papers WHERE 1=1"
        params = []
        
        if database:
            query += " AND database = ?"
            params.append(database)
        
        if year_min:
            query += " AND year >= ?"
            params.append(year_min)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        self.logger.info(f"Loaded {len(df)} papers from database")
        return df
    
    def clear_papers(self):
        """Clear all papers from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM papers")
        conn.commit()
        conn.close()
        self.logger.info("Cleared all papers from database")
