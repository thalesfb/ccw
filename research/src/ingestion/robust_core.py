"""
Robust client wrapper for CORE API with fallbacks.

This implementation satisfies the abstract requirements of BaseAPIClient and
delegates to fallbacks (Semantic Scholar, OpenAlex) when CORE is disabled or
fails, matching the original notebook behavior.
"""

import requests
import time
import random
import logging
from typing import Dict, List, Any, Optional
import pandas as pd

from .base import BaseAPIClient
from .semantic_scholar import SemanticScholarClient
from .openalex import OpenAlexClient

logger = logging.getLogger(__name__)


class RobustCOREClient(BaseAPIClient):
    """
    Cliente robusto para CORE API com fallbacks.
    Baseado nas configurações do notebook original.
    """
    BASE_URL = "https://api.core.ac.uk/v3/search/works"

    def __init__(self, config, cache_dir=None):
        super().__init__(config, cache_dir)
        # Read from ApiConfig compatibility helpers
        self.api_key = getattr(config.apis, "core_api_key",
                               None) or config.apis.core.get("api_key")
        self.rate_delay = getattr(config.apis, "core_rate_delay_s", 6.0)
        self.is_active = getattr(config.apis, "is_core_active", False)

        # Fallbacks baseados no notebook original
        self.fallbacks = [
            SemanticScholarClient(config, cache_dir),
            OpenAlexClient(config, cache_dir)
        ]
        logger.info(
            f"Robust CORE client initialized with {len(self.fallbacks)} fallbacks")

    def _get_rate_delay(self) -> float:
        """Return per-request delay for CORE.

        Note: This method is called during BaseAPIClient.__init__, before
        this class's __init__ runs. Therefore, it must not depend on
        attributes set in this class's __init__.
        """
        return float(getattr(self.config.apis, "core_rate_delay_s", 6.0) or 6.0)

    def _normalize_result(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize CORE result to standard schema. Minimal mapping here; the
        full mapping is handled by the dedicated CORE client in core.py.
        """
        # Reuse normalization from dedicated CORE client when available by
        # importing lazily to avoid circulars.
        try:
            from .core import COREClient
            temp = COREClient(self.config, self.cache_dir)
            return temp._normalize_result(item)  # type: ignore[attr-defined]
        except Exception:
            # Fallback minimal normalization
            return {
                "doi": item.get("doi"),
                "title": item.get("title"),
                "authors": None,
                "year": item.get("yearPublished"),
                "abstract": item.get("abstract"),
                "keywords": None,
                "url": item.get("downloadUrl") or item.get("id"),
                "source": "CORE",
                "venue": item.get("publisher"),
                "citation_count": None,
                "is_open_access": True,
                "publication_date": None,
            }

    def search(self, query: str, limit: int = 100) -> pd.DataFrame:
        """
        Search CORE, or transparently use fallbacks when CORE is disabled.

        Parameters
        ----------
        query : str
            Search string.
        limit : int
            Maximum results to return.

        Returns
        -------
        pandas.DataFrame
            Normalized results.
        """
        if not self.is_active or not self.api_key:
            logger.warning(
                "CORE disabled or missing API key - using fallbacks")
            return self._search_with_fallbacks(query, limit)

        # If CORE were active, we could delegate to the dedicated CORE client
        try:
            from .core import COREClient
            client = COREClient(self.config, self.cache_dir)
            return client.search(query, limit)
        except Exception as e:
            logger.error(f"CORE client failed, using fallbacks: {e}")
            return self._search_with_fallbacks(query, limit)

    def _search_with_fallbacks(self, query: str, limit: int) -> pd.DataFrame:
        """Run fallbacks and merge normalized DataFrames."""
        frames = []
        for fb in self.fallbacks:
            try:
                df = fb.search(query, limit=max(
                    1, limit // len(self.fallbacks)))
                if df is not None and not df.empty:
                    frames.append(df)
            except Exception as e:
                logger.error(f"Fallback {fb.__class__.__name__} failed: {e}")
        if frames:
            return pd.concat(frames, ignore_index=True)
        return pd.DataFrame()
