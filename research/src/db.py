"""Database operations for systematic review (compatibility layer)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from .config import AppConfig, load_config
from .database import DatabaseManager, PaperRecord

logger = logging.getLogger(__name__)

# Instância global do gerenciador de banco
_db_manager: Optional[DatabaseManager] = None


def get_db_manager(cfg: Optional[AppConfig] = None) -> DatabaseManager:
    """Get or create database manager instance.
    
    Args:
        cfg: Application configuration
        
    Returns:
        Database manager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(cfg or load_config())
    return _db_manager


def init_db(cfg: AppConfig | None = None, extra_columns: Iterable[str] | None = None) -> Path:
    """Initialize database (compatibility function).
    
    Args:
        cfg: Application configuration
        extra_columns: Additional columns (ignored, schema is fixed)
        
    Returns:
        Path to database file
    """
    manager = get_db_manager(cfg)
    if extra_columns:
        logger.warning("extra_columns parameter is deprecated, schema is now fixed")
    return manager.db_path


def save_papers(df: pd.DataFrame, cfg: AppConfig | None = None) -> int:
    """Save papers from DataFrame to database.
    
    Args:
        df: DataFrame with papers
        cfg: Application configuration
        
    Returns:
        Number of papers inserted
    """
    if df.empty:
        return 0
    
    # Reset index to ensure proper column structure
    df = df.reset_index(drop=True)
    
    manager = get_db_manager(cfg)
    
    # Convert DataFrame rows to PaperRecord objects
    papers = []
    for _, row in df.iterrows():
        paper = PaperRecord()
        
        # Map DataFrame columns to PaperRecord fields
        for field in df.columns:
            try:
                field_str = str(field)  # Ensure field is string
                if hasattr(paper, field_str):
                    value = row[field]
                    # Handle NaN values
                    if pd.isna(value):
                        value = None
                    setattr(paper, field_str, value)
            except TypeError as e:
                print(f"ERROR: field={repr(field)}, type={type(field)}")
                raise e
        
        papers.append(paper)
    
    # Bulk insert
    inserted = manager.insert_papers_bulk(papers)
    logger.info(f"Saved {inserted} papers to database")
    
    return inserted

def read_papers(cfg: AppConfig | None = None) -> pd.DataFrame:
    """Read all papers from database.
    
    Args:
        cfg: Application configuration
        
    Returns:
        DataFrame with papers
    """
    manager = get_db_manager(cfg)
    return manager.get_papers()


def get_papers_by_stage(stage: str, cfg: AppConfig | None = None) -> pd.DataFrame:
    """Get papers by selection stage.
    
    Args:
        stage: Selection stage (identification, screening, eligibility, included)
        cfg: Application configuration
        
    Returns:
        DataFrame with papers
    """
    manager = get_db_manager(cfg)
    return manager.get_papers(selection_stage=stage)


def update_paper_stage(
    paper_ids: list[int],
    stage: str,
    exclusion_reason: Optional[str] = None,
    cfg: AppConfig | None = None
) -> int:
    """Update selection stage for papers.
    
    Args:
        paper_ids: List of paper IDs
        stage: New selection stage
        exclusion_reason: Reason for exclusion
        cfg: Application configuration
        
    Returns:
        Number of papers updated
    """
    manager = get_db_manager(cfg)
    return manager.update_selection_stage(paper_ids, stage, exclusion_reason)


def get_statistics(cfg: AppConfig | None = None) -> dict:
    """Get database statistics.
    
    Args:
        cfg: Application configuration
        
    Returns:
        Dictionary with statistics
    """
    manager = get_db_manager(cfg)
    return manager.get_statistics()