"""Classe base para clientes de API."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import AppConfig
from ..logging_config import setup_logging_for_module

logger = setup_logging_for_module("ingestion.base")


class BaseAPIClient(ABC):
    """Classe base abstrata para clientes de API científicas."""

    def __init__(self, config: AppConfig, cache_dir: Optional[Path] = None):
        """Inicializa o cliente da API.

        Args:
            config: Configuração da aplicação
            cache_dir: Diretório para cache (compatibilidade, não usado)
        """
        self.config = config
        self.api_name = self.__class__.__name__.replace("Client", "").lower()

        # ✅ CORREÇÃO: Usar tabela cache do banco principal
        from ..database.manager import DatabaseManager
        self.db_manager = DatabaseManager()
        
        # Manter cache_dir para compatibilidade (mas não usar)
        if cache_dir is None:
            cache_dir = Path(config.database.cache_dir) / self.api_name
        self.cache_dir = cache_dir

        # Configurar sessão HTTP com retry
        self.session = self._create_session()

        # Rate limiting
        self.last_request_time = 0
        self.rate_delay = self._get_rate_delay()

        # Auditoria
        self.audit_logger = None  # Será configurado pelo pipeline

    def _create_session(self) -> requests.Session:
        """Cria sessão HTTP com retry automático."""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Headers padrão
        session.headers.update({
            "User-Agent": f"CCW-TCC/1.0 (mailto:{self.config.apis.user_email or 'user@example.com'})",
        })

        if self.config.apis.user_email:
            session.headers["From"] = self.config.apis.user_email

        return session

    @abstractmethod
    def _get_rate_delay(self) -> float:
        """Retorna o delay entre requisições em segundos."""
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 100) -> pd.DataFrame:
        """Busca artigos usando a query especificada.

        Args:
            query: String de busca
            limit: Número máximo de resultados

        Returns:
            DataFrame com os resultados normalizados
        """
        pass

    @abstractmethod
    def _normalize_result(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza um resultado da API para o formato padrão.

        Args:
            item: Item retornado pela API

        Returns:
            Dicionário normalizado com campos padrão
        """
        pass

    def set_audit_logger(self, audit_logger):
        """Configura o logger de auditoria."""
        self.audit_logger = audit_logger

    def _log_api_call(self, query: str, response_time: float, results_count: int,
                      status_code: int = 200, error: Optional[Exception] = None):
        """Registra chamada de API para auditoria."""
        if self.audit_logger:
            if error:
                self.audit_logger.log_error(
                    error, f"api_call_{self.api_name}", recoverable=True)
            else:
                self.audit_logger.log_api_call(
                    self.api_name, query, results_count, response_time, status_code
                )

    def _log_cache_hit(self, query: str, results_count: int):
        """Registra hit de cache para auditoria."""
        if self.audit_logger:
            self.audit_logger.log_user_action(f"cache_hit_{self.api_name}", {
                "query": query,
                "results_count": results_count,
                "cache_file": str(self._get_cache_path(query))
            })

    def _log_cache_miss(self, query: str):
        """Registra miss de cache para auditoria."""
        if self.audit_logger:
            self.audit_logger.log_user_action(f"cache_miss_{self.api_name}", {
                "query": query,
                "cache_file": str(self._get_cache_path(query))
            })

    def _wait_rate_limit(self):
        """Aguarda o tempo necessário para respeitar rate limit."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_delay:
            time.sleep(self.rate_delay - elapsed)
        self.last_request_time = time.time()

    def _get_cache_key(self, query: str) -> str:
        """Gera chave de cache para a query."""
        return hashlib.md5(f"{self.api_name}:{query}".encode()).hexdigest()

    def _get_cache_path(self, query: str) -> Path:
        """Retorna o caminho do arquivo de cache para a query."""
        cache_key = self._get_cache_key(query)
        return self.cache_dir / f"{cache_key}.json"

    def _load_from_cache(self, query: str) -> Optional[List[Dict]]:
        """Carrega resultados da tabela cache do banco."""
        try:
            # ✅ CORREÇÃO: Usar tabela cache do banco principal
            import hashlib
            query_hash = hashlib.md5(f"{self.api_name}:{query}".encode()).hexdigest()
            
            cached_data = self.db_manager.get_cached_results(query_hash, self.api_name)
            if cached_data:
                logger.debug(
                    f"Loaded {len(cached_data)} results from database cache for query: {query}")
                # Log de hit de cache
                self._log_cache_hit(query, len(cached_data))
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to load from database cache: {e}")
            if self.audit_logger:
                self.audit_logger.log_error(
                    e, "database_cache_load", recoverable=True)

        # Log de miss de cache
        self._log_cache_miss(query)
        return None

    def _save_to_cache(self, query: str, results: List[Dict]):
        """Salva resultados na tabela cache do banco."""
        try:
            # ✅ CORREÇÃO: Usar tabela cache do banco principal
            import hashlib
            query_hash = hashlib.md5(f"{self.api_name}:{query}".encode()).hexdigest()
            
            # Definir tempo de expiração baseado na API
            expires_hours = {
                'semantic_scholar': 24 * 7,  # 7 dias
                'openalex': 24 * 7,          # 7 dias 
                'crossref': 24 * 14,         # 14 dias
                'core': 24 * 3               # 3 dias
            }.get(self.api_name, 24)  # 1 dia padrão
            
            self.db_manager.save_cache(
                query_hash=query_hash,
                query_text=query,
                api=self.api_name,
                results=results,
                expires_in_hours=expires_hours
            )
            
            logger.debug(
                f"Saved {len(results)} results to database cache for query: {query}")

            # Log de auditoria para cache
            if self.audit_logger:
                self.audit_logger.log_user_action(f"database_cache_save_{self.api_name}", {
                    "query": query,
                    "results_count": len(results),
                    "cache_type": "database",
                    "expires_hours": expires_hours
                })
        except Exception as e:
            logger.warning(f"Failed to save to database cache: {e}")
            if self.audit_logger:
                self.audit_logger.log_error(
                    e, "database_cache_save", recoverable=True)

    def _make_request(self, url: str, params: Optional[Dict] = None, max_retries: int = 3) -> Optional[Dict]:
        """Faz uma requisição HTTP respeitando rate limits.

        Args:
            url: URL da requisição
            params: Parâmetros da query
            max_retries: Número máximo de tentativas

        Returns:
            Resposta JSON ou None se falhar
        """
        for attempt in range(max_retries):
            self._wait_rate_limit()

            start_time = time.time()
            try:
                response = self.session.get(url, params=params, timeout=30)
                response_time = time.time() - start_time

                if response.status_code == 200:
                    result = response.json()
                    # Log de sucesso
                    self._log_api_call(
                        query=str(params.get('query', 'unknown')),
                        response_time=response_time,
                        results_count=len(result.get('data', [])) if isinstance(
                            result, dict) else len(result) if isinstance(result, list) else 0,
                        status_code=response.status_code
                    )
                    return result
                    
                elif response.status_code == 429:
                    # Rate limit exceeded - backoff exponencial
                    retry_after = int(response.headers.get('Retry-After', self.rate_delay * (attempt + 2)))
                    logger.warning(f"Rate limit exceeded (429). Waiting {retry_after}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(retry_after)
                    continue
                    
                else:
                    # Log de erro HTTP
                    self._log_api_call(
                        query=str(params.get('query', 'unknown')),
                        response_time=response_time,
                        results_count=0,
                        status_code=response.status_code
                    )
                    logger.error(f"HTTP {response.status_code} for {url}")
                    return None

            except requests.exceptions.RequestException as e:
                response_time = time.time() - start_time
                # Log de erro de requisição
                self._log_api_call(
                    query=str(params.get('query', 'unknown')
                              ) if params else 'unknown',
                    response_time=response_time,
                    results_count=0,
                    status_code=0,
                    error=e
                )
                
                # Se for erro de rede temporário, tentar novamente
                if attempt < max_retries - 1:
                    backoff = self.rate_delay * (attempt + 1)
                    logger.warning(f"Request failed: {e}. Retrying in {backoff}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(backoff)
                    continue
                else:
                    logger.error(f"Request failed after {max_retries} attempts for {url}: {e}")
                    return None
        
        return None

    def normalize_dataframe(self, results: List[Dict]) -> pd.DataFrame:
        """Converte lista de resultados normalizados em DataFrame.

        Args:
            results: Lista de dicionários normalizados

        Returns:
            DataFrame com colunas padronizadas
        """
        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results)

        # Garantir que todas as colunas padrão existam
        standard_columns = [
            "doi", "title", "authors", "year", "abstract", "keywords",
            "url", "source", "search_engine", "query", "venue",
            "citation_count", "is_open_access", "publication_date"
        ]

        for col in standard_columns:
            if col not in df.columns:
                df[col] = None

        # Adicionar metadados
        df["search_engine"] = self.api_name
        df["retrieved_at"] = pd.Timestamp.now()

        return df
