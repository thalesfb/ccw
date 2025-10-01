"""
Quick tests for systematic review pipeline.
"""
import pytest
from research.models import Paper
from research.utils import normalize_text, queries_generator, is_relevant_paper


def test_normalize_text():
    """Test text normalization."""
    assert normalize_text("Educação Matemática") == "educacao matematica"
    assert normalize_text("Machine Learning") == "machine learning"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_queries_generator():
    """Test query generation."""
    first = ["math", "education"]
    second = ["ai", "ml"]
    queries = queries_generator(first, second)
    
    assert len(queries) == 4
    assert '"math" AND "ai"' in queries
    assert '"education" AND "ml"' in queries


def test_paper_creation():
    """Test Paper dataclass."""
    paper = Paper(
        title="Test Paper",
        authors="John Doe, Jane Smith",
        year=2020,
        database="test"
    )
    
    assert paper.title == "Test Paper"
    assert paper.year == 2020
    assert paper.database == "test"
    
    # Test to_dict
    paper_dict = paper.to_dict()
    assert isinstance(paper_dict, dict)
    assert paper_dict['title'] == "Test Paper"


def test_is_relevant_paper():
    """Test paper relevance filtering."""
    # Relevant paper
    paper = Paper(
        title="Machine Learning in Mathematics Education",
        abstract="This study explores adaptive learning systems",
        year=2020
    )
    
    relevant, reason = is_relevant_paper(
        paper,
        year_min=2015,
        langs=["en"],
        keywords=["education", "learning", "mathematics"],
        tech_terms=["machine learning", "adaptive"]
    )
    
    assert relevant is True
    assert reason == ""
    
    # Old paper
    old_paper = Paper(
        title="Machine Learning in Mathematics Education",
        year=2010
    )
    
    relevant, reason = is_relevant_paper(
        old_paper,
        year_min=2015,
        langs=["en"],
        keywords=["education"],
        tech_terms=["machine learning"]
    )
    
    assert relevant is False
    assert "Ano" in reason
    
    # Missing keywords
    no_keyword_paper = Paper(
        title="Some random topic",
        abstract="Not related to education",
        year=2020
    )
    
    relevant, reason = is_relevant_paper(
        no_keyword_paper,
        year_min=2015,
        langs=["en"],
        keywords=["education", "learning"],
        tech_terms=["machine learning"]
    )
    
    assert relevant is False


def test_paper_to_dict_roundtrip():
    """Test Paper to dict and back."""
    original = Paper(
        title="Test",
        year=2020,
        abstract="Abstract text"
    )
    
    paper_dict = original.to_dict()
    restored = Paper(**paper_dict)
    
    assert restored.title == original.title
    assert restored.year == original.year
    assert restored.abstract == original.abstract
