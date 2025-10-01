"""
Semantic Scholar API client.
"""
import time
from typing import Optional
import requests

from .base import BaseSearcher
from ..config import CONFIG
from ..models import Paper
from ..utils import exponential_backoff


class SemanticScholarSearcher(BaseSearcher):
    """Searcher for Semantic Scholar API."""
    
    def __init__(self):
        """Initialize Semantic Scholar searcher."""
        super().__init__("semantic_scholar")
        self.api_key = CONFIG["semantic_scholar"]["api_key"]
        self.headers = {"User-Agent": "ScholarGPT-Research/1.0"}
        if self.api_key:
            self.headers["x-api-key"] = self.api_key
    
    def _request_page(self, query: str, max_results: int):
        """
        Request pages from Semantic Scholar API.
        
        Args:
            query: Search query
            max_results: Maximum results to fetch
            
        Yields:
            Raw API result items
        """
        params = {
            "query": query,
            "limit": max_results * 2,
            "fields": "paperId,title,authors.name,year,venue,url,abstract,"
                     "isOpenAccess,tldr,fieldsOfStudy"
        }
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                self.logger.debug(
                    f"SemanticScholar Request: GET "
                    f"{CONFIG[self.name]['base_url']} Params: {params}"
                )
                response = self.session.get(
                    CONFIG[self.name]["base_url"],
                    headers=self.headers,
                    params=params,
                    timeout=20
                )
                response.raise_for_status()
                data = response.json().get("data", [])
                self.logger.debug(f"SemanticScholar Response: {len(data)} items")
                
                for item in data:
                    yield item
                return
            
            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"SemanticScholar Request failed "
                    f"(Attempt {attempt + 1}/{max_attempts}): {e}"
                )
                if attempt == max_attempts - 1:
                    self.logger.error(
                        f"Semantic Scholar falhou após {max_attempts} "
                        f"tentativas para query '{query}'."
                    )
                    return
                exponential_backoff(attempt)
            
            time.sleep(CONFIG[self.name]["rate_delay"])
    
    def _item_to_paper(self, item: dict, query: str) -> Optional[Paper]:
        """
        Convert Semantic Scholar item to Paper.
        
        Args:
            item: Raw API result item
            query: Original search query
            
        Returns:
            Paper object or None if conversion fails
        """
        try:
            year = item.get("year")
            if not isinstance(year, int):
                try:
                    year = int(year)
                except (ValueError, TypeError):
                    self.logger.debug(
                        f"Ano inválido no item SemanticScholar: "
                        f"{item.get('title', 'N/A')}"
                    )
                    return None
            
            return Paper(
                title=item.get("title", ""),
                authors=", ".join([
                    a.get("name", "") for a in item.get("authors", [])
                ]),
                year=year,
                source_publication=item.get("venue", ""),
                abstract=item.get("abstract", "") or "",
                doi_url=item.get("url", ""),
                database=self.name,
                search_terms=query,
                is_open_access=item.get("isOpenAccess", False),
                math_topic=", ".join(item.get("fieldsOfStudy", [])),
            )
        except Exception as e:
            self.logger.error(
                f"Erro ao converter item SemanticScholar para Paper: {e}"
            )
            return None
