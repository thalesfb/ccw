"""
API clients for systematic review.
"""
from .semantic_scholar import SemanticScholarSearcher
from .openalex import OpenAlexSearcher
from .crossref import CrossrefSearcher
from .core import CoreSearcher

__all__ = [
    'SemanticScholarSearcher',
    'OpenAlexSearcher',
    'CrossrefSearcher',
    'CoreSearcher',
]
