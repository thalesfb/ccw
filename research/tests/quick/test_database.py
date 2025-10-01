"""
Tests for database operations.
"""
import pytest
import os
import tempfile
from research.database import DatabaseManager
from research.models import Paper


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


def test_database_initialization(temp_db):
    """Test database initialization."""
    db = DatabaseManager(temp_db)
    assert os.path.exists(temp_db)


def test_save_and_load_papers(temp_db):
    """Test saving and loading papers."""
    db = DatabaseManager(temp_db)
    
    papers = [
        Paper(
            title="Paper 1",
            authors="Author 1",
            year=2020,
            database="test",
            doi_url="doi1"
        ),
        Paper(
            title="Paper 2",
            authors="Author 2",
            year=2021,
            database="test",
            doi_url="doi2"
        )
    ]
    
    saved_count = db.save_papers(papers)
    assert saved_count == 2
    
    # Load papers
    df = db.load_papers()
    assert len(df) == 2
    assert "Paper 1" in df['title'].values
    assert "Paper 2" in df['title'].values


def test_duplicate_prevention(temp_db):
    """Test that duplicates are not saved."""
    db = DatabaseManager(temp_db)
    
    paper = Paper(
        title="Duplicate Paper",
        doi_url="doi123",
        year=2020
    )
    
    # Save once
    saved_count = db.save_papers([paper])
    assert saved_count == 1
    
    # Try to save again
    saved_count = db.save_papers([paper])
    assert saved_count == 0  # Should not save duplicate
    
    # Verify only one exists
    df = db.load_papers()
    assert len(df) == 1


def test_filter_by_database(temp_db):
    """Test filtering papers by database."""
    db = DatabaseManager(temp_db)
    
    papers = [
        Paper(title="Paper 1", database="db1", year=2020, doi_url="doi1"),
        Paper(title="Paper 2", database="db2", year=2020, doi_url="doi2"),
        Paper(title="Paper 3", database="db1", year=2020, doi_url="doi3"),
    ]
    
    db.save_papers(papers)
    
    # Filter by database
    df_db1 = db.load_papers(database="db1")
    assert len(df_db1) == 2
    assert all(df_db1['database'] == "db1")


def test_filter_by_year(temp_db):
    """Test filtering papers by year."""
    db = DatabaseManager(temp_db)
    
    papers = [
        Paper(title="Paper 1", year=2015, doi_url="doi1"),
        Paper(title="Paper 2", year=2020, doi_url="doi2"),
        Paper(title="Paper 3", year=2022, doi_url="doi3"),
    ]
    
    db.save_papers(papers)
    
    # Filter by year
    df_recent = db.load_papers(year_min=2020)
    assert len(df_recent) == 2
    assert all(df_recent['year'] >= 2020)


def test_clear_papers(temp_db):
    """Test clearing all papers."""
    db = DatabaseManager(temp_db)
    
    papers = [
        Paper(title="Paper 1", doi_url="doi1", year=2020),
        Paper(title="Paper 2", doi_url="doi2", year=2020),
    ]
    
    db.save_papers(papers)
    assert len(db.load_papers()) == 2
    
    db.clear_papers()
    assert len(db.load_papers()) == 0
