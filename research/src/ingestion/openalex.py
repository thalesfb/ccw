"""Cliente para a API do OpenAlex."""

from __future__ import annotations

import logging
import random
import time
from typing import Any, Dict, List, Optional

import pandas as pd

from .base import BaseAPIClient

logger = logging.getLogger(__name__)


class OpenAlexClient(BaseAPIClient):
    """Cliente para buscar artigos no OpenAlex."""
    
    BASE_URL = "https://api.openalex.org/works"
    
    def _get_rate_delay(self) -> float:
        """Retorna o delay configurado para OpenAlex."""
        return self.config.apis.open_alex_rate_delay_s
    
    def search(self, query: str, limit: int = 100) -> pd.DataFrame:
        """Busca artigos no OpenAlex.
        
        Args:
            query: String de busca
            limit: Número máximo de resultados
            
        Returns:
            DataFrame com os resultados normalizados
        """
        # Verificar cache primeiro
        cached = self._load_from_cache(query)
        if cached is not None:
            normalized = [self._normalize_result(item) for item in cached]
            normalized = [r for r in normalized if r is not None]
            df = self.normalize_dataframe(normalized)
            df["database"] = "openalex"
            df["query"] = query
            return df
        
        # Limpar query
        clean_query = query.replace('"', '').strip()
        
        # Configurar cabeçalhos com email para polite pool
        if self.config.apis.user_email:
            self.session.headers.update({
                "User-Agent": f"CCW-TCC/1.0 (mailto:{self.config.apis.user_email})",
                "From": self.config.apis.user_email
            })
        
        logger.info(f"Searching OpenAlex for: {query}")
        
        results = []
        page = 1
        per_page = min(limit, 200)  # OpenAlex máximo por página
        
        while len(results) < limit:
            # Parâmetros da busca
            params = {
                "filter": f"publication_year:{self.config.review.year_min}-{self.config.review.year_max}",
                "search": clean_query,
                "per-page": per_page,
                "page": page,
                "select": "id,doi,title,publication_year,authorships,primary_location,abstract_inverted_index,open_access,concepts,topics,keywords,cited_by_count"
            }
            
            response = self._make_request(self.BASE_URL, params)
            if not response:
                break
            
            page_results = response.get("results", [])
            if not page_results:
                break
            
            results.extend(page_results)
            
            # Verificar se há mais páginas
            if len(page_results) < per_page or len(results) >= limit:
                break
            
            page += 1
            
            # Delay entre páginas
            time.sleep(self.rate_delay * 0.5 + random.uniform(0, 0.5))
        
        # Limitar ao número solicitado
        results = results[:limit]
        
        # Salvar no cache
        self._save_to_cache(query, results)
        
        # Normalizar e retornar
        normalized = [self._normalize_result(item) for item in results if self._normalize_result(item)]
        df = self.normalize_dataframe(normalized)
        df["database"] = "openalex"
        df["query"] = query
        
        logger.info(f"Found {len(df)} results from OpenAlex")
        return df
    
    def _normalize_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normaliza um resultado do OpenAlex.
        
        Args:
            item: Item retornado pela API
            
        Returns:
            Dicionário normalizado ou None se inválido
        """
        try:
            # Verificar ano válido
            year = item.get("publication_year")
            if not isinstance(year, int) or year < self.config.review.year_min:
                return None
            
            # Extrair autores
            authorships = item.get("authorships", [])
            authors = []
            for authorship in authorships:
                if isinstance(authorship, dict) and 'author' in authorship:
                    author_name = authorship['author'].get('display_name', '')
                    if author_name:
                        authors.append(author_name)
            authors_str = "; ".join(authors) if authors else None
            
            # Reconstruir abstract do índice invertido
            abstract = self._reconstruct_abstract(item.get('abstract_inverted_index'))
            
            # Extrair DOI
            doi = item.get("doi", "")
            if doi and doi.startswith("https://doi.org/"):
                doi = doi[16:]  # Remove o prefixo
            
            # Venue (journal/conference) - use primary_location instead of deprecated host_venue
            primary_location = item.get("primary_location", {}) or {}
            source = primary_location.get("source", {}) or {}
            venue = source.get("display_name", "")
            
            # Open access status
            open_access = item.get("open_access", {}) or {}
            is_open_access = open_access.get("is_oa", False)
            
            # Conceitos e tópicos
            concepts = item.get("concepts", []) or []
            concept_names = [c.get("display_name", "") for c in concepts if c.get("display_name")]
            
            topics = item.get("topics", []) or []
            topic_names = [t.get("display_name", "") for t in topics if t.get("display_name")]
            
            # URL do paper
            url = f"https://openalex.org/{item.get('id', '').split('/')[-1]}" if item.get('id') else ""
            
            return {
                "doi": doi,
                "title": item.get("title"),
                "authors": authors_str,
                "year": year,
                "abstract": abstract,
                "keywords": "; ".join(concept_names[:5]) if concept_names else None,  # Limitar a 5
                "url": url,
                "source": "OpenAlex",
                "venue": venue,
                "citation_count": item.get("cited_by_count"),
                "is_open_access": is_open_access,
                "publication_date": None,  # OpenAlex não fornece data específica
                "paper_id": item.get("id"),
                "topics": "; ".join(topic_names[:3]) if topic_names else None,  # Tópicos como campo extra
            }
        
        except Exception as e:
            logger.error(f"Error normalizing OpenAlex result: {e}")
            return None
    
    def _reconstruct_abstract(self, abstract_inverted: Optional[Dict]) -> Optional[str]:
        """Reconstrói abstract do índice invertido do OpenAlex.
        
        Args:
            abstract_inverted: Dicionário com índice invertido do abstract
            
        Returns:
            Abstract reconstruído ou None
        """
        if not abstract_inverted or not isinstance(abstract_inverted, dict):
            return None
        
        try:
            # Criar lista de (posição, palavra)
            word_positions = []
            for word, positions in abstract_inverted.items():
                if isinstance(positions, list):
                    for pos in positions:
                        if isinstance(pos, int):
                            word_positions.append((pos, word))
            
            # Ordenar por posição e reconstruir
            word_positions.sort()
            abstract = " ".join([word for pos, word in word_positions])
            
            return abstract.strip() if abstract.strip() else None
        
        except Exception as e:
            logger.error(f"Error reconstructing abstract: {e}")
            return None


def search_openalex(query: str, config, limit: int = 100) -> pd.DataFrame:
    """Função conveniente para buscar no OpenAlex.
    
    Args:
        query: String de busca
        config: Configuração da aplicação
        limit: Número máximo de resultados
        
    Returns:
        DataFrame com os resultados
    """
    client = OpenAlexClient(config)
    return client.search(query, limit)
