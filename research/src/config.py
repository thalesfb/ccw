"""
Application configuration for the systematic review project.

Notes
-----
This module exposes a stable configuration interface expected by the
ingestion, processing and pipeline modules. It intentionally provides
compatibility properties (e.g., ``config.review`` and
``config.apis.user_email``) to match existing imports across the codebase.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Carregar .env do diretório research/
_research_dir = Path(__file__).resolve().parents[1]  # config.py -> src/ -> research/ (parents[1])
_env_path = _research_dir / ".env"
load_dotenv(_env_path)


def _get_research_dir() -> Path:
    """Retorna o diretório research/ de forma absoluta."""
    return Path(__file__).resolve().parents[1]  # config.py -> src/ -> research/ (parents[1])


@dataclass
class DatabaseConfig:
    """
    Database configuration.

    Parameters
    ----------
    db_path : str
        SQLite database file path.
    cache_dir : str
        Base directory for on-disk API caches.
    exports_dir : str
        Base directory for exports (CSV, Excel, reports, visualizations).
    """

    db_path: str = ""
    cache_dir: str = ""
    exports_dir: str = ""
    logs_dir: str = ""
    
    def __post_init__(self):
        """Inicializa paths absolutos baseados no diretório research/."""
        research_dir = _get_research_dir()
        if not self.db_path:
            self.db_path = str(research_dir / "systematic_review.db")
        if not self.cache_dir:
            self.cache_dir = str(research_dir / "cache")
        if not self.exports_dir:
            self.exports_dir = str(research_dir / "exports")
        if not self.logs_dir:
            self.logs_dir = str(research_dir / "logs")


@dataclass
class ApiConfig:
    """
    API configuration with compatibility helpers.

    This wraps raw per-API dictionaries and exposes convenience properties
    used throughout the codebase (e.g., ``user_email``,
    ``semantic_scholar_rate_delay_s``).

    Parameters
    ----------
    semantic_scholar : dict
        Raw Semantic Scholar configuration mapping.
    open_alex : dict
        Raw OpenAlex configuration mapping.
    crossref : dict
        Raw Crossref configuration mapping.
    core : dict
        Raw CORE configuration mapping.
    user_email : str, optional
        Contact email used for polite pools (derived automatically when not
        provided).
    """

    semantic_scholar: Dict[str, Any]
    open_alex: Dict[str, Any]
    crossref: Dict[str, Any]
    core: Dict[str, Any]
    user_email: Optional[str] = None

    # ---- Compatibility helpers (properties expected elsewhere) ----
    @property
    def semantic_scholar_rate_delay_s(self) -> float:
        """Delay between requests (seconds) for Semantic Scholar."""
        return float(self.semantic_scholar.get("rate_delay", 4.0))

    @property
    def open_alex_rate_delay_s(self) -> float:
        """Delay between requests (seconds) for OpenAlex."""
        return float(self.open_alex.get("rate_delay", 6.0))

    @property
    def crossref_rate_delay_s(self) -> float:
        """Delay between requests (seconds) for Crossref."""
        return float(self.crossref.get("rate_delay", 4.0))

    @property
    def core_rate_delay_s(self) -> float:
        """Delay between requests (seconds) for CORE."""
        return float(self.core.get("rate_delay", 6.0))

    @property
    def core_api_key(self) -> Optional[str]:
        """API key for CORE (if provided)."""
        return self.core.get("api_key")

    @property
    def semantic_scholar_api_key(self) -> Optional[str]:
        """API key for Semantic Scholar (if provided)."""
        return self.semantic_scholar.get("api_key")

    @property
    def is_core_active(self) -> bool:
        """Whether CORE API usage is enabled."""
        return bool(self.core.get("is_active", False))


@dataclass
class ReviewCriteria:
    """
    Review criteria based on the original notebook.

    Parameters
    ----------
    year_min : int
        Minimum publication year.
    year_max : int
        Maximum publication year.
    languages : list of str, optional
        Allowed languages (ISO codes or names).
    keywords : list of str, optional
        Domain keywords.
    tech_terms : list of str, optional
        Technology-related terms.
    abstract_required : bool
        Whether an abstract is required in selection.
    relevance_threshold : float
        Default relevance score threshold used in selection.
    """

    year_min: int = 2015
    year_max: int = 2025
    languages: List[str] = None
    keywords: List[str] = None
    tech_terms: List[str] = None
    abstract_required: bool = False
    relevance_threshold: float = 4.0

    def __post_init__(self):
        if self.languages is None:
            self.languages = ["en", "pt"]
        if self.keywords is None:
            self.keywords = ["education", "educacao", "ensino",
                             "learning", "matematica", "mathematics"]
        if self.tech_terms is None:
            self.tech_terms = [
                "adaptive", "personalized", "tutoring", "analytics", "mining",
                "machine learning", "ai", "assessment", "student modeling", "predictive",
                "intelligent tutor", "artificial intelligence"
            ]


@dataclass
class AppConfig:
    """
    Application configuration container.

    Parameters
    ----------
    database : DatabaseConfig
        Database settings.
    apis : ApiConfig
        API settings.
    criteria : ReviewCriteria
        Review criteria (alias exposed as ``review`` for compatibility).
    max_results_per_query : int
        Soft cap for results per query.
    max_workers : int
        Parallelism level for processing.
    """

    database: DatabaseConfig
    apis: ApiConfig
    criteria: ReviewCriteria
    max_results_per_query: int = 10
    max_workers: int = 6

    # Backwards-compatibility alias used across modules
    @property
    def review(self) -> ReviewCriteria:
        """Compatibility alias to access review criteria as ``config.review``."""
        return self.criteria


def load_config() -> AppConfig:
    """
    Load configuration based on the original notebook.

    Returns
    -------
    AppConfig
        Fully-populated application configuration.
    """

    # Configurações das APIs do notebook original
    api_config = ApiConfig(
        semantic_scholar={
            "api_key": os.getenv("SEMANTIC_SCHOLAR_API_KEY", ""),
            "base_url": "https://api.semanticscholar.org/graph/v1/paper/search",
            "rate_delay": 4.0,
            "cache_dir": "cache/semantic_scholar/",
            "fields_expanded": [
                "paperId", "title", "authors.name", "year", "venue", "url",
                "abstract", "isOpenAccess", "tldr", "fieldsOfStudy",
                "publicationTypes", "citationCount", "influentialCitationCount"
            ]
        },
        open_alex={
            "email": os.getenv("USER_EMAIL"),
            "base_url": "https://api.openalex.org/works",
            "rate_delay": 6.0,
            "cache_dir": "cache/open_alex/",
            "use_polite_pool": True,
            "fields_expanded": [
                "id", "doi", "title", "publication_year", "authorships",
                "host_venue", "abstract_inverted_index", "open_access",
                "concepts", "topics", "keywords", "type", "language", "cited_by_count"
            ]
        },
        crossref={
            "email": os.getenv("USER_EMAIL"),
            "base_url": "https://api.crossref.org/works",
            "rate_delay": 4.0,
            "cache_dir": "cache/crossref/",
            "use_polite_pool": True
        },
        core={
            "api_key": os.getenv("CORE_API_KEY"),
            "base_url": "https://api.core.ac.uk/v3/search/works",
            "rate_delay": 6.0,
            "cache_dir": "cache/core/",
            "is_active": False  # Desabilitada no notebook original
        }
    )

    # Derive a global polite email for APIs when available
    api_config.user_email = (
        api_config.open_alex.get("email")
        or api_config.crossref.get("email")
        or os.getenv("USER_EMAIL")
    )

    return AppConfig(
        database=DatabaseConfig(),
        apis=api_config,
        criteria=ReviewCriteria(),
    )
