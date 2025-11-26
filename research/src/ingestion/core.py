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
    
    BASE_URL = "https://api.core.ac.uk/v3/search/outputs"
    
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
            # Filtrar None antes de criar DataFrame
            normalized = [self._normalize_result(item) for item in cached]
            normalized = [r for r in normalized if r is not None]
            df = self.normalize_dataframe(normalized)
            df["database"] = "core"
            df["query"] = query
            return df
        
        # Verificar se API key está disponível
        if not self.api_key:
            logger.warning(f"CORE API key not available, skipping query: {query}")
            return pd.DataFrame()
        
        # Simplificar query (CORE é sensível a sintaxe complexa)
        simplified_query = query.replace('"', '').strip()
        
        # Filtros simples para CORE API v3
        filter_str = f"yearPublished:>={self.config.review.year_min}"
        
        logger.info(f"[CORE] Searching CORE for: {query}")
        logger.debug(f"[CORE] Simplified query: {simplified_query}")
        logger.debug(f"[CORE] Filter: {filter_str}")
        
        results = []
        fetched_count = 0
        page_token = None
        max_attempts = 3
        
        while fetched_count < limit:
            # Payload para CORE API v3
            payload = {
                "q": simplified_query,
                "limit": min(limit - fetched_count, 100),  # Usar 'limit' não 'pageSize'
                "exclude": ["fullText"],  # Excluir fullText para reduzir payload
            }
            
            # Adicionar filtro se definido
            if filter_str:
                payload["filter"] = filter_str
            
            if page_token:
                payload["pageToken"] = page_token
            
            for attempt in range(max_attempts):
                try:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    
                    logger.debug(f"CORE Request: POST {self.BASE_URL}")
                    response = self.session.post(self.BASE_URL, json=payload, headers=headers, timeout=40)
                    
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
        
        # Normalizar e retornar (filtrar None)
        normalized = [self._normalize_result(item) for item in results]
        normalized = [r for r in normalized if r is not None]
        df = self.normalize_dataframe(normalized)
        
        # Adicionar fonte e query
        df["database"] = "core"
        df["query"] = query
        
        logger.info(f"[CORE] Found {len(df)} results from CORE")
        logger.debug(f"[CORE] Total API results collected: {len(results)}, After normalization: {len(df)}")
        return df
    
    def _normalize_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normaliza um resultado do CORE.
        
        Args:
            item: Item retornado pela API
            
        Returns:
            Dicionário normalizado ou None se inválido
        """
        # Verificar se item é válido
        if item is None:
            logger.warning("Received None item in _normalize_result")
            return None
        if not isinstance(item, dict):
            logger.warning(f"Received non-dict item: {type(item)}")
            return None
            
        try:
            # Verificar se está deletado
            if item.get("deleted") == "DELETED" or item.get("disabled", False):
                return None
            
            # Verificar ano válido (pode vir como string)
            year_published = item.get("yearPublished", 0)
            if isinstance(year_published, str):
                try:
                    year = int(year_published)
                except (ValueError, TypeError):
                    return None
            else:
                year = year_published or 0
                
            if not year or year < self.config.review.year_min:
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


    def get_pdf_url_by_doi(self, doi: str) -> Optional[str]:
        """Get PDF URL from CORE by DOI.
        
        Args:
            doi: Paper DOI (with or without https://doi.org/ prefix)
            
        Returns:
            PDF download URL if found, None otherwise
        """
        if not doi:
            return None
            
        if not self.api_key:
            logger.debug("CORE API key not available, skipping DOI lookup")
            return None
        
        # Normalize DOI
        clean_doi = doi.replace("https://doi.org/", "").strip()
        
        # Query CORE for this specific DOI
        payload = {
            "q": f'doi:"{clean_doi}"',
            "limit": 5,
            "exclude": ["fullText"]  # Don't need full text for URL resolution
        }
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            logger.debug(f"CORE DOI lookup: {clean_doi}")
            
            response = self.session.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
                timeout=15
            )
            
            if response.status_code != 200:
                logger.debug(f"CORE DOI lookup failed with status {response.status_code}")
                return None
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                logger.debug(f"No CORE results for DOI: {clean_doi}")
                return None
            
            # Check each result for download URL
            for item in results:
                # Skip deleted or disabled
                if item.get("deleted") == "DELETED" or item.get("disabled", False):
                    continue
                
                # Try downloadUrl first (direct PDF link)
                download_url = item.get("downloadUrl", "").strip()
                if download_url and download_url.lower().endswith(".pdf"):
                    logger.info(f"✓ CORE found PDF URL for {clean_doi}: {download_url}")
                    return download_url
                
                # Try links array
                links = item.get("links", [])
                for link in links:
                    if isinstance(link, dict):
                        link_url = link.get("url", "").strip()
                        link_type = link.get("type", "").lower()
                        if link_url and (link_type == "download" or link_url.lower().endswith(".pdf")):
                            logger.info(f"✓ CORE found PDF link for {clean_doi}: {link_url}")
                            return link_url
                
                # Fallback to downloadUrl even if not .pdf extension
                if download_url:
                    logger.info(f"✓ CORE found download URL for {clean_doi}: {download_url}")
                    return download_url
            
            logger.debug(f"CORE results exist but no PDF URL found for {clean_doi}")
            return None
            
        except Exception as e:
            logger.error(f"CORE DOI lookup error for {clean_doi}: {e}")
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
