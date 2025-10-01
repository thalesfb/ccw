"""
Crossref API client.
"""
import re
import time
from typing import Optional
import requests
from crossref.restful import Works

from .base import BaseSearcher
from ..config import CONFIG
from ..models import Paper
from ..utils import exponential_backoff

# Global Works instance
works = Works()


class CrossrefSearcher(BaseSearcher):
    """Searcher for Crossref API."""
    
    def __init__(self):
        """Initialize Crossref searcher."""
        super().__init__("crossref")
        self.logger.info(
            "CrossrefSearcher inicializado, usando instância 'works' global."
        )
    
    def _request_page(self, query: str, max_results: int):
        """
        Request pages from Crossref API.
        
        Args:
            query: Search query
            max_results: Maximum results to fetch
            
        Yields:
            Raw API result items
        """
        clean_query = re.sub(r'[\"]|AND', '', query).strip()
        target_rows = min(max_results * 2, 100)
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                self.logger.debug(
                    f"Crossref Request: works.query(bibliographic='{clean_query}')"
                    f".filter(from_pub_date='{self.year_min}-01-01')"
                    f".sample({target_rows})"
                )
                
                results_generator = works.query(bibliographic=clean_query)\
                                       .filter(from_pub_date=f'{self.year_min}-01-01')\
                                       .sort('relevance').order('desc')\
                                       .sample(target_rows)
                
                count = 0
                for item in results_generator:
                    yield item
                    count += 1
                
                self.logger.debug(f"Crossref Response: Yielded {count} items")
                return
            
            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"Crossref Request failed "
                    f"(Attempt {attempt + 1}/{max_attempts}): {e}"
                )
                if attempt == max_attempts - 1:
                    self.logger.error(
                        f"Crossref falhou após {max_attempts} "
                        f"tentativas para query '{query}'."
                    )
                    return
                exponential_backoff(attempt)
            except Exception as e:
                self.logger.error(
                    f"Erro inesperado na busca Crossref "
                    f"(Attempt {attempt + 1}/{max_attempts}): {e}"
                )
                if attempt == max_attempts - 1:
                    self.logger.error(
                        f"Crossref falhou após {max_attempts} "
                        f"tentativas para query '{query}'."
                    )
                    return
                exponential_backoff(attempt)
            
            time.sleep(CONFIG[self.name]["rate_delay"])
    
    def _item_to_paper(self, item: dict, query: str) -> Optional[Paper]:
        """
        Convert Crossref item to Paper.
        
        Args:
            item: Raw API result item
            query: Original search query
            
        Returns:
            Paper object or None if conversion fails
        """
        try:
            # Extract year
            pub_date_parts = item.get(
                "published-print", {}
            ).get("date-parts", [[]])[0]
            if not pub_date_parts or not pub_date_parts[0]:
                pub_date_parts = item.get(
                    "published-online", {}
                ).get("date-parts", [[]])[0]
            
            year = None
            if pub_date_parts and len(pub_date_parts) > 0:
                try:
                    year = int(pub_date_parts[0])
                except (ValueError, TypeError):
                    year = None
            
            if not isinstance(year, int):
                self.logger.debug(
                    f"Ano inválido no item Crossref: "
                    f"{item.get('title', ['N/A'])[0]}"
                )
                return None
            
            # Extract title
            title = (item.get("title", []) or [""])[0]
            
            # Extract authors
            authors_list = []
            for author in item.get("author", []):
                name_parts = [author.get("given"), author.get("family")]
                full_name = " ".join(part for part in name_parts if part)
                if not full_name and 'name' in author:
                    full_name = author['name']
                if full_name:
                    authors_list.append(full_name)
            authors_str = ", ".join(authors_list)
            
            # Extract publication source
            source_pub = (item.get("container-title", []) or [""])[0]
            
            # Extract abstract
            abstract = item.get("abstract", "") or ""
            if abstract.startswith('<'):
                abstract = re.sub('<[^>]+>', '', abstract).strip()
            
            # Get DOI or URL
            doi = item.get("DOI", "")
            url = item.get("URL", "")
            doi_url = f"https://doi.org/{doi}" if doi else url
            
            # Check Open Access status
            is_oa = item.get("is_oa", False)
            if not is_oa:
                for license_info in item.get("license", []):
                    if 'creativecommons.org' in license_info.get('URL', ''):
                        is_oa = True
                        break
            
            return Paper(
                title=title,
                authors=authors_str,
                year=year,
                source_publication=source_pub,
                abstract=abstract,
                doi_url=doi_url,
                database=self.name,
                search_terms=query,
                is_open_access=is_oa,
            )
        except Exception as e:
            self.logger.error(
                f"Erro ao converter item Crossref para Paper: {e}"
            )
            return None
