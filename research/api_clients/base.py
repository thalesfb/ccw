"""
Base API searcher class.
"""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ..models import Paper
from ..utils import (
    create_session_with_retry,
    load_from_cache,
    save_to_cache,
    is_relevant_paper
)


class BaseSearcher(ABC):
    """Abstract base class for API searchers."""
    
    def __init__(self, name: str):
        """
        Initialize the searcher.
        
        Args:
            name: Name of the API (e.g., "semantic_scholar")
        """
        self.name = name
        self.session = create_session_with_retry(
            total=5,
            backoff=3,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.logger = logging.getLogger(self.name)
        self.year_min = 2015
        self.langs = ["en", "pt"]
        self.keywords = [
            "education", "educacao", "ensino", "learning",
            "matematica", "mathematics"
        ]
        self.tech_terms = [
            "adaptive", "personalized", "tutoring", "analytics", "mining",
            "machine learning", "ai", "assessment", "student modeling",
            "predictive", "intelligent tutor", "artificial intelligence"
        ]
        self.papers = []
    
    def search(
        self,
        queries: List[str],
        max_results_per_query: int = 10,
        year_min: int = 2015,
        langs: Optional[List[str]] = None
    ) -> List[Paper]:
        """
        Search for papers across multiple queries.
        
        Args:
            queries: List of search queries
            max_results_per_query: Maximum results to fetch per query
            year_min: Minimum publication year
            langs: List of accepted languages
            
        Returns:
            List of Paper objects
        """
        self.year_min = year_min
        if langs:
            self.langs = langs
        
        self.papers = []
        total_added_from_cache = 0
        total_added_from_api = 0
        total_discarded = 0
        total_processed_from_api = 0
        
        for query in queries:
            self.logger.info(f"🔎 Iniciando busca para: '{query}'")
            cached = load_from_cache(query, self.name)
            query_added_from_cache = 0
            
            if cached:
                self.logger.info(
                    f"📋 Carregando {len(cached)} artigos do cache para '{query}'"
                )
                for item_dict in cached:
                    try:
                        paper = Paper(**item_dict)
                        relevant, reason = is_relevant_paper(
                            paper, self.year_min, self.langs,
                            self.keywords, self.tech_terms
                        )
                        if relevant:
                            self.papers.append(paper)
                            query_added_from_cache += 1
                        else:
                            self.logger.debug(
                                f"Descartado (do cache): {paper.title[:60]}... "
                                f"Motivo: {reason}"
                            )
                    except Exception as e:
                        self.logger.error(
                            f"Erro ao processar item cacheado: {e}"
                        )
                
                self.logger.info(
                    f"  -> {query_added_from_cache} artigos relevantes "
                    f"adicionados do cache para '{query}'."
                )
                total_added_from_cache += query_added_from_cache
                continue
            
            # API Call
            self.logger.info(
                f"☁️ Cache não encontrado para '{query}'. Buscando na API..."
            )
            results_api, filtered_api, discarded_api = 0, 0, 0
            papers_to_cache: List[Dict[str, Any]] = []
            
            try:
                for item in self._request_page(query, max_results_per_query):
                    results_api += 1
                    paper = self._item_to_paper(item, query)
                    
                    if not paper:
                        self.logger.debug(
                            "Item da API não pôde ser convertido em Paper"
                        )
                        discarded_api += 1
                        continue
                    
                    relevant, reason = is_relevant_paper(
                        paper, self.year_min, self.langs,
                        self.keywords, self.tech_terms
                    )
                    if relevant:
                        self.papers.append(paper)
                        papers_to_cache.append(paper.to_dict())
                        filtered_api += 1
                    else:
                        self.logger.debug(
                            f"Descartado (da API): {paper.title[:60]}... "
                            f"Motivo: {reason}"
                        )
                        discarded_api += 1
            
            except Exception as e:
                self.logger.error(
                    f"Erro durante requisição da API para query '{query}': {e}",
                    exc_info=True
                )
                continue
            
            # Caching and logging
            total_added_from_api += filtered_api
            total_discarded += discarded_api
            total_processed_from_api += results_api
            
            if papers_to_cache:
                save_to_cache(query, papers_to_cache, self.name)
                self.logger.info(
                    f"✅ {filtered_api} artigos relevantes da API salvos no cache "
                    f"para '{query}' ({discarded_api} descartados de "
                    f"{results_api} processados)."
                )
            elif results_api > 0:
                self.logger.info(
                    f"ℹ️ Nenhum artigo relevante encontrado na API para '{query}' "
                    f"({discarded_api} descartados de {results_api} processados)."
                )
            else:
                self.logger.info(
                    f"ℹ️ Nenhum resultado retornado pela API para '{query}'."
                )
        
        # Final summary
        self.logger.info("🏁 Busca concluída.")
        self.logger.info(f"  Total adicionado do cache: {total_added_from_cache}")
        self.logger.info(f"  Total adicionado da API: {total_added_from_api}")
        self.logger.info(f"  Total processado da API: {total_processed_from_api}")
        self.logger.info(f"  Total descartado: {total_discarded}")
        
        return self.papers
    
    @abstractmethod
    def _request_page(self, query: str, max_results: int):
        """
        Yield raw items from the API results. Handles pagination internally.
        
        Args:
            query: Search query
            max_results: Maximum results to fetch
            
        Yields:
            Raw API result items
        """
        pass
    
    @abstractmethod
    def _item_to_paper(self, item: dict, query: str) -> Optional[Paper]:
        """
        Convert a raw API item into a Paper object.
        
        Args:
            item: Raw API result item
            query: Original search query
            
        Returns:
            Paper object or None if conversion fails
        """
        pass
