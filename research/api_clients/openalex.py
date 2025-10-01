"""
OpenAlex API client.
"""
import time
import random
from typing import Optional
import requests

from .base import BaseSearcher
from ..config import CONFIG
from ..models import Paper
from ..utils import exponential_backoff


class OpenAlexSearcher(BaseSearcher):
    """Searcher for OpenAlex API."""
    
    def __init__(self):
        """Initialize OpenAlex searcher."""
        super().__init__("open_alex")
        self.email = CONFIG["open_alex"]["email"]
        if not self.email or "@" not in self.email:
            self.logger.warning(
                "Email não configurado para OpenAlex. Usando placeholder."
            )
            self.email = "placeholder@example.com"
        self.headers = {
            "User-Agent": f"ScholarGPT-Research/1.0 (mailto:{self.email})",
            "Accept": "application/json"
        }
    
    def _request_page(self, query: str, max_results: int):
        """
        Request pages from OpenAlex API.
        
        Args:
            query: Search query
            max_results: Maximum results to fetch
            
        Yields:
            Raw API result items
        """
        clean_query = query.replace('"', '')
        page = 1
        fetched_count = 0
        max_attempts = 3
        per_page = min(max_results, 50)
        
        while fetched_count < max_results:
            params = {
                "filter": f"publication_year:>{self.year_min-1}",
                "search": clean_query,
                "per-page": per_page,
                "page": page,
                "select": "id,doi,title,publication_year,authorships,host_venue,"
                         "abstract_inverted_index,open_access,concepts,topics,keywords"
            }
            
            for attempt in range(max_attempts):
                try:
                    self.logger.debug(
                        f"OpenAlex Request: GET {CONFIG[self.name]['base_url']} "
                        f"Params: {params}"
                    )
                    response = self.session.get(
                        CONFIG[self.name]["base_url"],
                        headers=self.headers,
                        params=params,
                        timeout=25
                    )
                    response.raise_for_status()
                    data = response.json()
                    results = data.get("results", [])
                    self.logger.debug(
                        f"OpenAlex Response: {len(results)} items on page {page}"
                    )
                    
                    if not results:
                        return
                    
                    for item in results:
                        if fetched_count < max_results:
                            yield item
                            fetched_count += 1
                        else:
                            break
                    
                    if fetched_count >= max_results:
                        return
                    
                    page += 1
                    time.sleep(
                        CONFIG[self.name]["rate_delay"] * 0.5 +
                        random.uniform(0, 0.5)
                    )
                    break
                
                except requests.exceptions.RequestException as e:
                    self.logger.error(
                        f"OpenAlex Request failed "
                        f"(Attempt {attempt + 1}/{max_attempts}): {e}"
                    )
                    if attempt == max_attempts - 1:
                        self.logger.error(
                            f"OpenAlex falhou após {max_attempts} tentativas "
                            f"para query '{query}', page {page}."
                        )
                        return
                    exponential_backoff(attempt)
            else:
                self.logger.error(
                    f"OpenAlex falhou em obter a página {page} "
                    f"para query '{query}' após {max_attempts} tentativas."
                )
                return
    
    def _item_to_paper(self, item: dict, query: str) -> Optional[Paper]:
        """
        Convert OpenAlex item to Paper.
        
        Args:
            item: Raw API result item
            query: Original search query
            
        Returns:
            Paper object or None if conversion fails
        """
        try:
            year = item.get("publication_year")
            if not isinstance(year, int):
                return None
            
            authorships = item.get("authorships", [])
            authors = []
            for authorship in authorships:
                if isinstance(authorship, dict) and 'author' in authorship:
                    author_name = authorship['author'].get('display_name', '')
                    if author_name:
                        authors.append(author_name)
            
            # Reconstruct abstract from inverted index
            abstract_inverted = item.get('abstract_inverted_index')
            abstract = ""
            if abstract_inverted and isinstance(abstract_inverted, dict):
                word_positions = []
                for word, positions in abstract_inverted.items():
                    for pos in positions:
                        word_positions.append((pos, word))
                word_positions.sort()
                abstract = " ".join([word for pos, word in word_positions])
            
            return Paper(
                title=item.get("title", ""),
                authors=", ".join(authors),
                year=year,
                source_publication=item.get("host_venue", {}).get(
                    "display_name", ""
                ),
                abstract=abstract,
                doi_url=item.get("doi", ""),
                database=self.name,
                search_terms=query,
                is_open_access=item.get("open_access", {}).get("is_oa", False),
                country=item.get("host_venue", {}).get("country_code", ""),
                study_type=item.get("type", ""),
                comp_techniques=", ".join([
                    c.get("display_name", "") for c in item.get("concepts", [])
                ]),
            )
        except Exception as e:
            self.logger.error(
                f"Erro ao converter item OpenAlex para Paper: {e}"
            )
            return None
