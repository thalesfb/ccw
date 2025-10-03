"""Cliente para a API do Semantic Scholar."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import pandas as pd

from .base import BaseAPIClient

logger = logging.getLogger(__name__)


class SemanticScholarClient(BaseAPIClient):
    """Cliente para buscar artigos no Semantic Scholar."""
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def _get_rate_delay(self) -> float:
        """Retorna o delay configurado para Semantic Scholar."""
        return self.config.apis.semantic_scholar_rate_delay_s
    
    def search(self, query: str, limit: int = 100) -> pd.DataFrame:
        """Busca artigos no Semantic Scholar.
        
        Args:
            query: String de busca
            limit: Número máximo de resultados (máx 100 por página)
            
        Returns:
            DataFrame com os resultados normalizados
        """
        # Verificar cache primeiro
        cached = self._load_from_cache(query)
        if cached is not None:
            return self.normalize_dataframe([self._normalize_result(item) for item in cached])
        
        # Campos a retornar
        fields = [
            "paperId", "title", "abstract", "year", "authors",
            "venue", "publicationTypes", "fieldsOfStudy", "citationCount",
            "influentialCitationCount", "isOpenAccess", "openAccessPdf",
            "externalIds", "url", "publicationDate"
        ]
        
        # Parâmetros da busca
        params = {
            "query": query,
            "fields": ",".join(fields),
            "limit": min(limit, 100)  # Máximo 100 por página
        }
        
        url = f"{self.BASE_URL}/paper/search"
        logger.info(f"Searching Semantic Scholar for: {query}")
        
        response = self._make_request(url, params)
        if not response:
            return pd.DataFrame()
        
        results = response.get("data", [])
        
        # Paginação se necessário
        offset = len(results)
        while offset < limit and response.get("next"):
            params["offset"] = offset
            response = self._make_request(url, params)
            if response:
                new_results = response.get("data", [])
                results.extend(new_results)
                offset += len(new_results)
            else:
                break
        
        # Salvar no cache
        self._save_to_cache(query, results)
        
        # Normalizar e retornar
        normalized = [self._normalize_result(item) for item in results]
        df = self.normalize_dataframe(normalized)
        df["query"] = query
        
        logger.info(f"Found {len(df)} results from Semantic Scholar")
        return df
    
    def _normalize_result(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza um resultado do Semantic Scholar.
        
        Args:
            item: Item retornado pela API
            
        Returns:
            Dicionário normalizado
        """
        # Extrair DOI se disponível
        doi = None
        external_ids = item.get("externalIds", {})
        if external_ids:
            doi = external_ids.get("DOI")
        
        # Formatar autores
        authors = []
        for author in item.get("authors", []):
            name = author.get("name", "")
            if name:
                authors.append(name)
        authors_str = "; ".join(authors) if authors else None
        
        # Formatar keywords/fields
        fields = item.get("fieldsOfStudy", [])
        keywords = "; ".join(fields) if fields else None
        
        # URL do artigo
        url = item.get("url")
        if not url and item.get("paperId"):
            url = f"https://www.semanticscholar.org/paper/{item['paperId']}"
        
        # Verificar open access
        is_open_access = item.get("isOpenAccess", False)
        open_pdf = None
        if is_open_access and item.get("openAccessPdf"):
            open_pdf = item["openAccessPdf"].get("url")
        
        return {
            "doi": doi,
            "title": item.get("title"),
            "authors": authors_str,
            "year": item.get("year"),
            "abstract": item.get("abstract"),
            "keywords": keywords,
            "url": url,
            "source": "Semantic Scholar",
            "venue": item.get("venue"),
            "citation_count": item.get("citationCount"),
            "influential_citation_count": item.get("influentialCitationCount"),
            "is_open_access": is_open_access,
            "open_access_pdf": open_pdf,
            "publication_date": item.get("publicationDate"),
            "publication_types": "; ".join(item.get("publicationTypes", [])),
            "paper_id": item.get("paperId"),
        }


def search_semantic_scholar(query: str, config: AppConfig, limit: int = 100) -> pd.DataFrame:
    """Função conveniente para buscar no Semantic Scholar.
    
    Args:
        query: String de busca
        config: Configuração da aplicação
        limit: Número máximo de resultados
        
    Returns:
        DataFrame com os resultados
    """
    client = SemanticScholarClient(config)
    return client.search(query, limit)
