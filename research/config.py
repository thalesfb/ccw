"""
Configuration module for research pipeline.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
CONFIG = {
    "semantic_scholar": {
        "api_key": os.getenv("SEMANTIC_SCHOLAR_API_KEY", ""),
        "base_url": "https://api.semanticscholar.org/graph/v1/paper/search",
        "rate_delay": 3.0,
        "cache_dir": "research/cache/semantic_scholar/"
    },
    "open_alex": {
        "email": os.getenv('USER_EMAIL', ''),
        "base_url": "https://api.openalex.org/works",
        "rate_delay": 5.0,
        "cache_dir": "research/cache/open_alex/"
    },
    "crossref": {
        "email": os.getenv('USER_EMAIL', ''),
        "base_url": "https://api.crossref.org/works",
        "rate_delay": 3.0,
        "cache_dir": "research/cache/crossref/"
    },
    "core": {
        "api_key": os.getenv('CORE_API_KEY', ''),
        "base_url": "https://api.core.ac.uk/v3/search/works",
        "rate_delay": 6.0,
        "cache_dir": "research/cache/core/"
    }
}

# Search terms
FIRST_TERMS = [
    "mathematics education",
    "math learning",
    "mathematics teaching",
    "educação matemática",
    "ensino de matemática"
]

SECOND_TERMS = [
    "adaptive learning",
    "personalized learning",
    "intelligent tutoring systems",
    "learning analytics",
    "educational data mining",
    "machine learning",
    "artificial intelligence",
    "automated assessment",
    "competency identification",
    "student modeling",
    "predictive analytics"
]

# DataFrame columns
PAPER_COLUMNS = [
    'title',
    'authors',
    'year',
    'source_publication',
    'abstract',
    'full_text',
    'doi_url',
    'database',
    'search_terms',
    'is_open_access',
    'country',
    'study_type',
    'comp_techniques',
    'eval_methods',
    'math_topic',
    'main_results',
    'identified_gaps',
    'relevance_score',
    'selection_stage',
    'exclusion_reason',
    'notes'
]

# Default search parameters
DEFAULT_YEAR_MIN = 2015
DEFAULT_LANGUAGES = ["en", "pt"]
DEFAULT_MAX_RESULTS_PER_QUERY = 10

# Keywords for filtering
EDUCATION_KEYWORDS = [
    "education", "educacao", "ensino", "learning", "matematica", "mathematics"
]

TECH_KEYWORDS = [
    "adaptive", "personalized", "tutoring", "analytics", "mining",
    "machine learning", "ai", "assessment", "student modeling", "predictive",
    "intelligent tutor", "artificial intelligence"
]

# Deduplication thresholds
DEDUP_RATIO_THRESHOLD = 90
DEDUP_COSINE_THRESHOLD = 0.10
