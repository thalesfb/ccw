"""Cliente para a API do Crossref."""

from __future__ import annotations

import logging
import re
import time
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from crossref.restful import Works

from .base import BaseAPIClient

logger = logging.getLogger(__name__)


class CrossrefClient(BaseAPIClient):
    """Cliente para buscar artigos no Crossref."""
    
    def __init__(self, config, cache_dir=None):
        """Initialize Crossref client.
        
        Args:
            config: Application configuration
            cache_dir: Cache directory
        """
        super().__init__(config, cache_dir)
        
        # Configurar Works instance com polite pool
        self.works = Works()
        
        # Configurar headers para polite pool
        if self.config.apis.user_email:
            self.session.headers.update({
                "User-Agent": f"CCW-TCC/1.0 (mailto:{self.config.apis.user_email})",
                "From": self.config.apis.user_email
            })
    
    def _get_rate_delay(self) -> float:
        """Retorna o delay configurado para Crossref."""
        return self.config.apis.crossref_rate_delay_s
    
    def search(self, query: str, limit: int = 100) -> pd.DataFrame:
        """Busca artigos no Crossref.
        
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
            df["database"] = "crossref"
            df["query"] = query
            return df
        
        # Limpar query
        clean_query = re.sub(r'[\"]|AND', '', query).strip()
        
        logger.info(f"Searching Crossref for: {query}")
        
        results = []
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # Usar query bibliographic para melhor matching
                search_results = (self.works
                                .query(bibliographic=clean_query)
                                .filter(from_pub_date=f'{self.config.review.year_min}-01-01',
                                       until_pub_date=f'{self.config.review.year_max}-12-31')
                                .sort('relevance')
                                .order('desc')
                                .sample(min(limit * 2, 200)))  # Buscar mais para filtrar depois
                
                # Coletar resultados
                count = 0
                for item in search_results:
                    try:
                        if count >= limit:
                            break
                        # Verificar se item é válido (crossref.restful pode retornar None)
                        if item is None:
                            logger.warning("Crossref returned None item, skipping")
                            continue
                        if not isinstance(item, dict):
                            logger.warning(f"Crossref returned non-dict item: {type(item)}, skipping")
                            continue
                        results.append(item)
                        count += 1
                    except Exception as item_error:
                        logger.warning(f"Error processing Crossref item: {item_error}, skipping")
                        continue
                
                logger.debug(f"Crossref returned {len(results)} items")
                break  # Sucesso
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Crossref request failed (attempt {attempt + 1}/{max_attempts}): {e}")
                if attempt == max_attempts - 1:
                    logger.error(f"Crossref failed after {max_attempts} attempts for query '{query}'")
                    return pd.DataFrame()
                time.sleep(self.rate_delay * (attempt + 1))
                
            except Exception as e:
                logger.error(f"Unexpected error in Crossref search (attempt {attempt + 1}/{max_attempts}): {e}")
                if attempt == max_attempts - 1:
                    logger.error(f"Crossref failed after {max_attempts} attempts for query '{query}'")
                    return pd.DataFrame()
                time.sleep(self.rate_delay * (attempt + 1))
        
        # Salvar no cache
        self._save_to_cache(query, results)
        
        # Normalizar e retornar
        normalized = [self._normalize_result(item) for item in results if self._normalize_result(item)]
        df = self.normalize_dataframe(normalized)
        df["database"] = "crossref"
        df["query"] = query
        
        logger.info(f"Found {len(df)} results from Crossref")
        return df
    
    def _normalize_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normaliza um resultado do Crossref.
        
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
            logger.warning(f"Received non-dict item in _normalize_result: {type(item)}")
            return None
            
        try:
            # Extrair ano de published-print ou published-online
            year = self._extract_year(item)
            if not year or year < self.config.review.year_min:
                return None
            
            # Extrair título (pode ser uma lista)
            title = self._extract_title(item)
            if not title:
                return None
            
            # Extrair autores
            authors_str = self._extract_authors(item)
            
            # Extrair venue (journal/conference)
            venue = self._extract_venue(item)
            
            # Extrair abstract e limpar HTML/XML
            abstract = self._extract_abstract(item)
            
            # Extrair DOI e URL
            doi = item.get("DOI", "")
            url = item.get("URL", "")
            paper_url = f"https://doi.org/{doi}" if doi else url
            
            # Verificar open access
            is_open_access = self._check_open_access(item)
            
            # Extrair contagem de citações se disponível
            citation_count = item.get("is-referenced-by-count")
            
            # Extrair data de publicação
            pub_date = self._extract_publication_date(item)
            
            return {
                "doi": doi,
                "title": title,
                "authors": authors_str,
                "year": year,
                "abstract": abstract,
                "keywords": None,  # Crossref raramente tem keywords
                "url": paper_url,
                "source": "Crossref",
                "venue": venue,
                "citation_count": citation_count,
                "is_open_access": is_open_access,
                "publication_date": pub_date,
                "paper_id": doi,  # Usar DOI como ID
                "publisher": item.get("publisher"),
                "type": item.get("type"),
            }
        
        except Exception as e:
            logger.error(f"Error normalizing Crossref result: {e}")
            return None
    
    def _extract_year(self, item: Dict) -> Optional[int]:
        """Extrai ano de publicação."""
        if not item:
            return None
            
        # Tentar published-print primeiro
        pub_date_parts = item.get("published-print", {}).get("date-parts", [[]])
        if not pub_date_parts or not pub_date_parts[0]:
            # Tentar published-online
            pub_date_parts = item.get("published-online", {}).get("date-parts", [[]])
        
        if pub_date_parts and len(pub_date_parts[0]) > 0:
            try:
                return int(pub_date_parts[0][0])
            except (ValueError, TypeError, IndexError):
                pass
        
        return None
    
    def _extract_title(self, item: Dict) -> Optional[str]:
        """Extrai título."""
        if not item:
            return None
        title_list = item.get("title", [])
        if title_list and isinstance(title_list, list):
            return title_list[0].strip() if title_list[0] else None
        return None
    
    def _extract_authors(self, item: Dict) -> Optional[str]:
        """Extrai autores."""
        if not item:
            return None
        authors_list = []
        for author in item.get("author", []):
            # Diferentes estruturas de nomes
            name_parts = []
            if author.get("given"):
                name_parts.append(author["given"])
            if author.get("family"):
                name_parts.append(author["family"])
            
            full_name = " ".join(name_parts)
            
            # Estrutura alternativa
            if not full_name and author.get("name"):
                full_name = author["name"]
            
            if full_name:
                authors_list.append(full_name)
        
        return "; ".join(authors_list) if authors_list else None
    
    def _extract_venue(self, item: Dict) -> Optional[str]:
        """Extrai venue (journal/conference)."""
        if not item:
            return None
        container_title = item.get("container-title", [])
        if container_title and isinstance(container_title, list):
            return container_title[0] if container_title[0] else None
        return None
    
    def _extract_abstract(self, item: Dict) -> Optional[str]:
        """Extrai e limpa abstract."""
        if not item:
            return None
        abstract = item.get("abstract", "")
        if not abstract:
            return None
        
        # Limpar tags XML/HTML se presente
        if abstract.startswith('<'):
            abstract = re.sub('<[^>]+>', '', abstract)
        
        abstract = abstract.strip()
        return abstract if abstract else None
    
    def _check_open_access(self, item: Dict) -> bool:
        """Verifica se é open access."""
        if not item:
            return False
        # Verificar flag direto se disponível
        if item.get("is_oa"):
            return True
        
        # Verificar licenças Creative Commons
        for license_info in item.get("license", []):
            license_url = license_info.get("URL", "").lower()
            if "creativecommons.org" in license_url or "cc-by" in license_url:
                return True
        
        return False
    
    def _extract_publication_date(self, item: Dict) -> Optional[str]:
        """Extrai data de publicação completa."""
        if not item:
            return None
        # Tentar published-print primeiro
        pub_date_parts = item.get("published-print", {}).get("date-parts", [[]])
        if not pub_date_parts or not pub_date_parts[0]:
            # Tentar published-online
            pub_date_parts = item.get("published-online", {}).get("date-parts", [[]])
        
        if pub_date_parts and len(pub_date_parts[0]) >= 3:
            try:
                year, month, day = pub_date_parts[0][:3]
                return f"{year:04d}-{month:02d}-{day:02d}"
            except (ValueError, TypeError, IndexError):
                pass
        elif pub_date_parts and len(pub_date_parts[0]) >= 2:
            try:
                year, month = pub_date_parts[0][:2]
                return f"{year:04d}-{month:02d}"
            except (ValueError, TypeError, IndexError):
                pass
        
        return None

    # === PDF LINK RESOLUTION ===
    def get_pdf_link(self, doi: str) -> Optional[str]:
        """Tenta obter um link direto de PDF para um DOI via Crossref.

        Busca o registro do DOI e inspeciona a chave 'link' procurando
        entradas com content-type 'application/pdf'. Retorna a primeira encontrada.
        """
        if not doi:
            return None
        try:
            record = self.works.doi(doi)
            if not record or not isinstance(record, dict):
                return None
            links = record.get("link", []) or []
            for link in links:
                if link.get("content-type") == "application/pdf" and link.get("URL"):
                    pdf_url = link["URL"].strip()
                    logger.info(f"📥 Crossref forneceu link de PDF para DOI {doi}: {pdf_url}")
                    return pdf_url
        except Exception as e:
            logger.debug(f"Crossref get_pdf_link falhou para {doi}: {e}")
            return None
        return None


def search_crossref(query: str, config, limit: int = 100) -> pd.DataFrame:
    """Função conveniente para buscar no Crossref.
    
    Args:
        query: String de busca
        config: Configuração da aplicação
        limit: Número máximo de resultados
        
    Returns:
        DataFrame com os resultados
    """
    client = CrossrefClient(config)
    return client.search(query, limit)
