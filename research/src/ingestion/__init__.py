"""Módulos para coleta de dados das APIs científicas."""

from .base import BaseAPIClient
from .semantic_scholar import SemanticScholarClient, search_semantic_scholar
from .openalex import OpenAlexClient, search_openalex
from .crossref import CrossrefClient, search_crossref
from .core import COREClient, search_core

__all__ = [
    "BaseAPIClient",
    "SemanticScholarClient", "search_semantic_scholar",
    "OpenAlexClient", "search_openalex",
    "CrossrefClient", "search_crossref", 
    "COREClient", "search_core"
]
