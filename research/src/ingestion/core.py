"""Cliente para a API do CORE."""

from __future__ import annotations

import logging
import random
import time
from typing import Any, Dict, List, Optional

import pandas as pd

from .base import BaseAPIClient

logger = logging.getLogger(__name__)


class COREClient(BaseAPIClient):
    """Cliente para buscar artigos no CORE."""
    
    BASE_URL = "https://api.core.ac.uk/v3/search/works"
    
    def __init__(self, config, cache_dir=None):
        """Initialize CORE client.
        
        Args:
            config: Application configuration
            cache_dir: Cache directory
        """
        super().__init__(config, cache_dir)
        
        # Configurar API key
        self.api_key = config.apis.core_api_key
        if not self.api_key:
            logger.warning("CORE API Key não configurada. A busca pode falhar ou ser limitada.")
    
    def _get_rate_delay(self) -> float:
        """Retorna o delay configurado para CORE."""
        return 2.0  # CORE API é mais instável, usar delay fixo
    
    def search(self, query: str, limit: int = 100) -> pd.DataFrame:
        """Busca artigos no CORE.
        
        Args:
            query: String de busca
            limit: Número máximo de resultados
            
        Returns:
            DataFrame com os resultados normalizados
        """
        # Verificar cache primeiro
        cached = self._load_from_cache(query)
        if cached is not None:
            return self.normalize_dataframe([self._normalize_result(item) for item in cached])
        
        # Verificar se API key está disponível
        if not self.api_key:
            logger.warning(f"CORE API key not available, skipping query: {query}")
            return pd.DataFrame()
        
        # Simplificar query (CORE é sensível a sintaxe complexa)
        simplified_query = query.replace('"', '').strip()
        
        # Filtros para CORE
        language_filter = " OR ".join(self.config.review.languages)
        filter_str = f"yearPublished:>={self.config.review.year_min} AND language:({language_filter})"
        
        logger.info(f"Searching CORE for: {query}")
        
        results = []
        fetched_count = 0
        page_token = None
        max_attempts = 3
        
        while fetched_count < limit:
            # Payload para CORE API v3
            payload = {
                "q": simplified_query,
                "pageSize": min(limit - fetched_count, 100),  # CORE max pageSize
                "filter": filter_str,
                "fields": "id,title,authors,yearPublished,publisher,abstract,fullText,doi,downloadUrl,documentType,language,topics,subjects",
            }
            
            if page_token:
                payload["pageToken"] = page_token
            
            for attempt in range(max_attempts):
                try:
                    url = f'{self.BASE_URL}?apiKey={self.api_key}'
                    
                    logger.debug(f"CORE Request: POST {url}")
                    response = self.session.post(url, json=payload, timeout=40)
                    
                    # CORE API tem histórico de instabilidade
                    if response.status_code == 500:
                        logger.warning(f"CORE API returned 500 error for query: {query}")
                        if attempt == max_attempts - 1:
                            logger.error(f"CORE API persistently failing with 500 errors")
                            return pd.DataFrame()
                        time.sleep(self.rate_delay * (attempt + 1))
                        continue
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    page_results = data.get("results", [])
                    page_token = data.get("nextPageToken")
                    
                    logger.debug(f"CORE Response: {len(page_results)} items, nextPageToken: {bool(page_token)}")
                    
                    for item in page_results:
                        if fetched_count < limit:
                            results.append(item)
                            fetched_count += 1
                        else:
                            break
                    
                    # Parar se não há mais páginas ou atingiu limite
                    if not page_token or fetched_count >= limit:
                        break
                    
                    # Delay antes da próxima página
                    time.sleep(self.rate_delay * 0.3 + random.uniform(0, 0.3))
                    break  # Sucesso
                    
                except Exception as e:
                    logger.error(f"CORE request failed (attempt {attempt + 1}/{max_attempts}): {e}")
                    if attempt == max_attempts - 1:
                        logger.error(f"CORE failed after {max_attempts} attempts for query '{query}'")
                        return pd.DataFrame()
                    time.sleep(self.rate_delay * (attempt + 1))
            else:
                # Todos os attempts falharam
                logger.error(f"CORE failed for query '{query}' after {max_attempts} attempts")
                break
            
            # Quebrar o loop se não conseguiu fazer a requisição
            if not page_results:
                break
        
        # Salvar no cache apenas se obteve resultados
        if results:
            self._save_to_cache(query, results)
        
        # Normalizar e retornar
        normalized = [self._normalize_result(item) for item in results if self._normalize_result(item)]
        df = self.normalize_dataframe(normalized)
        df["query"] = query
        
        logger.info(f"Found {len(df)} results from CORE")
        return df
    
    def _normalize_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normaliza um resultado do CORE.
        
        Args:
            item: Item retornado pela API
            
        Returns:
            Dicionário normalizado ou None se inválido
        """
        try:
            # Verificar ano válido
            year = item.get("yearPublished") or 0
            if not year or not isinstance(year, int) or year < self.config.review.year_min:
                return None
            
            # Extrair autores
            authors_list = []
            for author in item.get("authors", []):
                if isinstance(author, dict):
                    name = author.get("name", "").strip()
                    if name:
                        authors_list.append(name)
                elif isinstance(author, str):
                    # Às vezes autores vêm como strings
                    name = author.strip()
                    if name:
                        authors_list.append(name)
            
            authors_str = "; ".join(authors_list) if authors_list else None
            
            # Verificar idioma
            language_data = item.get("language")
            language_name = ""
            if isinstance(language_data, dict):
                language_name = language_data.get("name", "").lower()
            elif isinstance(language_data, str):
                language_name = language_data.lower()
            
            # Abstract e full text
            abstract = item.get("abstract", "") or ""
            full_text = item.get("fullText", "") or ""
            
            # DOI e URL
            doi = item.get("doi", "")
            download_url = item.get("downloadUrl", "")
            paper_url = doi if doi else download_url
            
            # Extrair tópicos e assuntos
            topics = item.get("topics", []) or []
            subjects = item.get("subjects", []) or []
            
            # Tipo de documento
            doc_type = item.get("documentType", "")
            
            return {
                "doi": doi.replace("https://doi.org/", "") if doi and doi.startswith("https://doi.org/") else doi,
                "title": item.get("title", ""),
                "authors": authors_str,
                "year": year,
                "abstract": abstract,
                "keywords": "; ".join(topics[:5]) if topics else None,  # Usar tópicos como keywords
                "url": paper_url,
                "source": "CORE",
                "venue": item.get("publisher", ""),
                "citation_count": None,  # CORE não fornece contagem de citações
                "is_open_access": True,  # CORE foca em open access
                "publication_date": None,  # CORE não fornece data específica
                "paper_id": item.get("id"),
                "full_text": full_text[:1000] if full_text else None,  # Limitar texto completo
                "document_type": doc_type,
                "language": language_name,
                "subjects": "; ".join(subjects[:3]) if subjects else None,
            }
        
        except Exception as e:
            logger.error(f"Error normalizing CORE result: {e}")
            return None


def search_core(query: str, config, limit: int = 100) -> pd.DataFrame:
    """Função conveniente para buscar no CORE.
    
    Args:
        query: String de busca
        config: Configuração da aplicação
        limit: Número máximo de resultados
        
    Returns:
        DataFrame com os resultados
    """
    client = COREClient(config)
    return client.search(query, limit)
