"""
Utility functions for research pipeline.
"""
import hashlib
import json
import os
import time
import random
import unicodedata
import itertools
from typing import List, Optional, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import CONFIG
from ..models import Paper


def normalize_text(text: str) -> str:
    """
    Normalize text by converting to lowercase and removing accents.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text


def queries_generator(first: List[str], second: List[str]) -> List[str]:
    """
    Generate all combinations of primary and secondary search terms.
    
    Args:
        first: List of primary terms
        second: List of secondary terms
        
    Returns:
        List of query strings combining all terms
    """
    queries = [
        f'"{p}" AND "{s}"'
        for p, s in itertools.product(first, second)
    ]
    return queries


def get_cache_filename(query: str, api_name: str) -> str:
    """
    Generate a cache filename based on the query and API name.
    
    Args:
        query: The search query
        api_name: The name of the API
        
    Returns:
        The cache filename path
    """
    query_hash = hashlib.md5(query.encode()).hexdigest()
    return f"{CONFIG[api_name]['cache_dir']}{query_hash}.json"


def load_from_cache(query: str, api_name: str) -> Optional[list]:
    """
    Load results from cache if available.
    
    Args:
        query: The search query
        api_name: The name of the API
        
    Returns:
        The cached results if available, otherwise None
    """
    cache_file = get_cache_filename(query, api_name)
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_to_cache(query: str, data: list, api_name: str) -> None:
    """
    Save results to cache.
    
    Args:
        query: The search query
        data: The data to be cached
        api_name: The name of the API
    """
    cache_file = get_cache_filename(query, api_name)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_session_with_retry(
    total: int = 3,
    backoff: int = 2,
    status_forcelist: List[int] = None
) -> requests.Session:
    """
    Create requests session with retry strategy.
    
    Args:
        total: Total number of retries
        backoff: Backoff factor for delay between retries
        status_forcelist: List of HTTP status codes that force a retry
        
    Returns:
        Configured session with retry strategy
    """
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]
    
    session = requests.Session()
    retries = Retry(
        total=total,
        backoff_factor=backoff,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST"],
        respect_retry_after_header=True
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def exponential_backoff(attempt: int, base_delay: int = 3) -> None:
    """
    Implements exponential backoff strategy for retrying requests.
    
    Args:
        attempt: The current attempt number (0-indexed)
        base_delay: The base delay in seconds
    """
    delay = base_delay * (2 ** attempt) + random.uniform(0, 1.5)
    time.sleep(delay)


def is_relevant_paper(
    paper: Paper,
    year_min: int,
    langs: List[str],
    keywords: List[str],
    tech_terms: List[str]
) -> Tuple[bool, str]:
    """
    Filter papers based on relevance criteria.
    
    Args:
        paper: Paper object to check
        year_min: Minimum publication year
        langs: List of accepted languages
        keywords: Required education keywords
        tech_terms: Required technology terms
        
    Returns:
        Tuple of (is_relevant, exclusion_reason)
    """
    # Year check
    if not isinstance(paper.year, int) or paper.year < year_min:
        return False, f"Ano < {year_min}"
    
    # Title or abstract empty
    if not paper.title and not paper.abstract:
        return False, "Título e Resumo vazios"
    
    text_to_check = normalize_text(paper.title + " " + paper.abstract)
    
    # Education keywords check
    if keywords and not any(normalize_text(k) in text_to_check for k in keywords):
        return False, "Sem palavra-chave de educação"
    
    # Technology terms check
    if tech_terms and not any(normalize_text(t) in text_to_check for t in tech_terms):
        return False, "Sem termo de tecnologia"
    
    return True, ""


def ensure_cache_dirs() -> None:
    """Create cache directories if they don't exist."""
    for source in CONFIG:
        os.makedirs(CONFIG[source]["cache_dir"], exist_ok=True)
