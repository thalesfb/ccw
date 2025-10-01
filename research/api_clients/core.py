"""
CORE API client.
"""
import time
import random
from typing import Optional
import requests

from .base import BaseSearcher
from ..config import CONFIG
from ..models import Paper


class CoreSearcher(BaseSearcher):
    """Searcher for CORE API."""
    
    def __init__(self):
        """Initialize CORE searcher."""
        super().__init__("core")
        self.api_key = CONFIG["core"]["api_key"]
        if not self.api_key:
            self.logger.warning(
                "CORE API Key não configurada. "
                "A busca pode falhar ou ser limitada."
            )
    
    def _request_page(self, query: str, max_results: int):
        """
        Request pages from CORE API.
        
        Args:
            query: Search query
            max_results: Maximum results to fetch
            
        Yields:
            Raw API result items
        """
        simplified_query = query.replace('"', '').strip()
        filter_str = (
            f"yearPublished:>={self.year_min} AND "
            f"language:({' OR '.join(self.langs)})"
        )
        fetched_count = 0
        page_token = None
        max_attempts_session = self.session.adapters['https://'].max_retries.total
        
        while fetched_count < max_results:
            payload = {
                "q": simplified_query,
                "pageSize": min(max_results - fetched_count, 1000),
                "filter": filter_str,
                "fields": "id,title,authors,yearPublished,publisher,abstract,"
                         "fullText,doi,downloadUrl,documentType,language,"
                         "topics,subjects",
            }
            if page_token:
                payload["pageToken"] = page_token
            
            try:
                url = f'{CONFIG["core"]["base_url"]}?apiKey={self.api_key}'
                self.logger.debug(f"CORE Request: POST {url} Payload: {payload}")
                response = self.session.post(url, json=payload, timeout=40)
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                page_token = data.get("nextPageToken")
                self.logger.debug(
                    f"CORE Response: {len(results)} items, "
                    f"nextPageToken: {bool(page_token)}"
                )
                
                for item in results:
                    if fetched_count < max_results:
                        yield item
                        fetched_count += 1
                    else:
                        break
                
                if not page_token or fetched_count >= max_results:
                    return
                
                time.sleep(
                    CONFIG["core"]["rate_delay"] * 0.3 +
                    random.uniform(0, 0.3)
                )
            
            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"CORE Request failed for query '{query}' "
                    f"after {max_attempts_session} retries: {e}"
                )
                return
    
    def _item_to_paper(self, item: dict, query: str) -> Optional[Paper]:
        """
        Convert CORE item to Paper.
        
        Args:
            item: Raw API result item
            query: Original search query
            
        Returns:
            Paper object or None if conversion fails
        """
        try:
            year = item.get("yearPublished") or 0
            
            if not year or not isinstance(year, int) or year < self.year_min:
                self.logger.debug(
                    f"Ano inválido no item CORE: "
                    f"{item.get('title', 'N/A')}"
                )
                return None
            
            authors_list = [
                a.get("name") for a in item.get("authors", [])
                if a.get("name")
            ]
            
            return Paper(
                title=item.get("title", ""),
                authors=", ".join(authors_list),
                year=year,
                source_publication=item.get("publisher", ""),
                abstract=item.get("abstract", "") or "",
                full_text=item.get("fullText", "") or "",
                doi_url=item.get("doi") or item.get("downloadUrl", ""),
                database=self.name,
                search_terms=query,
                is_open_access=True,  # CORE focuses on OA
                study_type=item.get("documentType", ""),
                comp_techniques=", ".join(item.get("topics", [])),
                eval_methods=", ".join(item.get("subjects", [])),
            )
        except Exception as e:
            self.logger.error(
                f"Erro ao converter item CORE para Paper: {e}"
            )
            return None
