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
            cache_dir: Diretório para cache (padrão: research/cache/{api_name})
        """
        self.config = config
        self.api_name = self.__class__.__name__.replace("Client", "").lower()

        # Configurar cache
        if cache_dir is None:
            cache_dir = Path(__file__).parents[3] / "cache" / self.api_name
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

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
        """Carrega resultados do cache se existirem."""
        cache_key = self._get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.debug(
                        f"Loaded {len(data)} results from cache for query: {query}")
                    # Log de hit de cache
                    self._log_cache_hit(query, len(data))
                    return data
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
                if self.audit_logger:
                    self.audit_logger.log_error(
                        e, "cache_load", recoverable=True)

        # Log de miss de cache
        self._log_cache_miss(query)
        return None

    def _save_to_cache(self, query: str, results: List[Dict]):
        """Salva resultados no cache."""
        cache_key = self._get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                logger.debug(
                    f"Saved {len(results)} results to cache for query: {query}")

                # Log de auditoria para cache
                if self.audit_logger:
                    self.audit_logger.log_user_action(f"cache_save_{self.api_name}", {
                        "query": query,
                        "results_count": len(results),
                        "cache_file": str(cache_file),
                        "file_size_bytes": cache_file.stat().st_size if cache_file.exists() else 0
                    })
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
            if self.audit_logger:
                self.audit_logger.log_error(e, "cache_save", recoverable=True)

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Faz uma requisição HTTP respeitando rate limits.

        Args:
            url: URL da requisição
            params: Parâmetros da query

        Returns:
            Resposta JSON ou None se falhar
        """
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
            logger.error(f"Request failed for {url}: {e}")
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
