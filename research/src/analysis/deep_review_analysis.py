"""
Análise Aprofundada dos Papers Incluídos na Revisão Sistemática
=================================================================

Este script realiza análise qualitativa aprofundada dos papers marcados
como 'included' no banco de dados SQLite canônico (ver `research/systematic_review.db`).
Os números exatos (total de papers incluídos) são obtidos dinamicamente a partir
do banco antes da execução; não há contagens hard-coded neste script.

Estratégias:
1. Enriquecimento via Semantic Scholar API (tldr, citations, references)
2. Análise temática via LLM (clustering, gaps, metodologias)
3. Geração de relatório Markdown estruturado
4. Visualizações de redes (co-citação, co-autoria)

Autor: Thales Ferreira
Data: Outubro 2025
"""

import io
import json
import logging
import datetime
import re
import concurrent.futures
import sqlite3
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin, quote_plus

import requests
from pypdf import PdfReader

from ..config import AppConfig, load_config
from ..ingestion.semantic_scholar import SemanticScholarClient
from ..ingestion.crossref import CrossrefClient
from ..ingestion.core import COREClient
from .html_pdf_scraper import HTMLPDFScraper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class PublisherPDFResolver:
    """Resolve PDF URLs para publishers específicos e serviços abertos."""

    PDF_LINK_PATTERN = re.compile(r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']', re.IGNORECASE)

    def __init__(self, session: requests.Session):
        self.session = session
        self.openalex_cache: Dict[str, Optional[str]] = {}
        self.semantic_scholar_cache: Dict[str, Optional[str]] = {}

    def resolve(self, paper: Dict[str, Any]) -> Optional[str]:
        doi = (paper.get('doi') or '').strip()
        if not doi:
            return None

        strategies = (
            # Publisher-specific OA patterns (highest priority - direct PDF access)
            self._resolve_ejmse,
            self._resolve_pmj,
            self._resolve_jestp,
            self._resolve_ieiespc,
            # Traditional publisher-specific resolvers
            self._resolve_ieee_stamp,
            self._resolve_intechopen,
            # API-based discovery services (check cached PDFs)
            self._resolve_semantic_scholar_cached,
            self._resolve_openalex,
            # Author/institutional repositories
            self._resolve_author_site,
            # Social academic platforms
            self._resolve_researchgate,
            self._resolve_academia_edu,
            # Generic fallbacks
            self._resolve_doi_landing,
            self._resolve_alternative_doi_services,
        )

        for strategy in strategies:
            pdf_url = strategy(doi, paper)
            if pdf_url:
                return pdf_url
        return None

    def _resolve_ieee_stamp(self, doi: str, _: Dict[str, Any]) -> Optional[str]:
        if not doi.lower().startswith('10.1109/'):
            return None
        match = re.search(r'(\d+)$', doi)
        if not match:
            return None
        arnumber = match.group(1)
        pdf_url = f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={arnumber}"
        logger.debug(f"Publisher resolver (IEEE) gerou URL {pdf_url}")
        return pdf_url

    def _resolve_intechopen(self, doi: str, _: Dict[str, Any]) -> Optional[str]:
        lower = doi.lower()
        if not lower.startswith('10.5772/intechopen.'):
            return None
        chapter_id = doi.split('.')[-1]
        if not chapter_id.isdigit():
            return None
        pdf_url = f"https://www.intechopen.com/chapter/pdf-download/{chapter_id}"
        logger.debug(f"Publisher resolver (IntechOpen) gerou URL {pdf_url}")
        return pdf_url

    def _resolve_openalex(self, doi: str, _: Dict[str, Any]) -> Optional[str]:
        if doi in self.openalex_cache:
            return self.openalex_cache[doi]

        work_id = f"https://doi.org/{doi}"
        api_url = f"https://api.openalex.org/works/{work_id}"
        try:
            response = self.session.get(api_url, timeout=15)
            if response.status_code != 200:
                self.openalex_cache[doi] = None
                return None
            data = response.json()
        except requests.RequestException:
            self.openalex_cache[doi] = None
            return None

        location = data.get('best_oa_location') or data.get('primary_location') or {}
        pdf_url = (
            location.get('url_for_pdf')
            or location.get('pdf_url')
            or location.get('landing_page_url')
        )

        if pdf_url:
            logger.debug(f"Publisher resolver (OpenAlex) retornou {pdf_url}")
            self.openalex_cache[doi] = pdf_url
            return pdf_url

        self.openalex_cache[doi] = None
        return None
    
    def _resolve_ejmse(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Resolve EJMSE (European Journal of Mathematics and Science Education) PDFs.
        
        Pattern: https://pdf.ejmse.com/EJMSE_{volume}_{issue}_{start_page}.pdf
        DOI format: 10.12973/ejmse.{volume}.{issue}.{start_page}
        Example: 10.12973/ejmse.5.2.93 -> https://pdf.ejmse.com/EJMSE_5_2_93.pdf
        """
        if not doi.lower().startswith('10.12973/ejmse.'):
            return None
        
        try:
            # Extract volume.issue.start_page from DOI
            parts = doi.split('.')
            if len(parts) >= 5:  # 10, 12973, ejmse, volume, issue, start_page
                volume = parts[3]
                issue = parts[4]
                start_page = parts[5] if len(parts) > 5 else parts[4]
                
                pdf_url = f"https://pdf.ejmse.com/EJMSE_{volume}_{issue}_{start_page}.pdf"
                logger.debug(f"Publisher resolver (EJMSE) gerou URL {pdf_url}")
                return pdf_url
        except (IndexError, ValueError) as e:
            logger.debug(f"EJMSE pattern extraction failed: {e}")
        
        return None
    
    def _resolve_pmj(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Resolve PMJ (Panamerican Mathematical Journal) PDFs.
        
        Pattern: https://internationalpubls.com/index.php/pmj/article/download/{article_id}/{file_id}/{version}
        DOI format: 10.52783/pmj.v{volume}.i{issue}.{article_id}
        Example: 10.52783/pmj.v34.i2.919 -> Need to scrape article page for download IDs
        """
        if not doi.lower().startswith('10.52783/pmj.'):
            return None
        
        try:
            # Extract article_id from DOI (last component)
            article_id = doi.split('.')[-1]
            
            # Try common download URL pattern (file_id often = article_id + offset)
            # First attempt: direct download with common file_id patterns
            for file_id_offset in [0, 643-919, 1]:  # Based on observed pattern: 919/643
                file_id = int(article_id) + file_id_offset
                for version in [1707, 1, 0]:  # Try common version numbers
                    pdf_url = f"https://internationalpubls.com/index.php/pmj/article/download/{article_id}/{file_id}/{version}"
                    logger.debug(f"Publisher resolver (PMJ) tentando URL {pdf_url}")
                    
                    # Quick HEAD request to validate
                    try:
                        head_resp = self.session.head(pdf_url, timeout=10, allow_redirects=True)
                        if head_resp.status_code == 200:
                            content_type = head_resp.headers.get('content-type', '').lower()
                            if 'pdf' in content_type or 'application/octet-stream' in content_type:
                                logger.debug(f"Publisher resolver (PMJ) validou URL {pdf_url}")
                                return pdf_url
                    except requests.RequestException:
                        continue
        except (IndexError, ValueError) as e:
            logger.debug(f"PMJ pattern extraction failed: {e}")
        
        return None
    
    def _resolve_jestp(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Resolve JESTP/ESTP (Educational Sciences: Theory & Practice) PDFs.
        
        Pattern: https://jestp.com/menuscript/index.php/estp/article/download/{article_id}/{file_id}/{version}
        DOI format: 10.12738/estp.{year}.{issue}.{article_id}
        Example: 10.12738/estp.2017.5.0634 -> https://jestp.com/menuscript/index.php/estp/article/download/426/381/754
        """
        if not doi.lower().startswith('10.12738/estp.'):
            return None
        
        try:
            # Extract article_id from DOI (last component without leading zeros)
            article_id_raw = doi.split('.')[-1]
            article_id = str(int(article_id_raw))  # Remove leading zeros: 0634 -> 634
            
            # Try common download URL patterns
            # Pattern observed: article_id in URL doesn't always match DOI suffix
            # Need to scrape the article landing page
            landing_url = f"https://jestp.com/menuscript/index.php/estp/article/view/{article_id}"
            
            try:
                response = self.session.get(landing_url, timeout=15)
                if response.status_code == 200:
                    # Look for download links in HTML
                    download_pattern = re.compile(
                        r'href="[^"]*article/download/(\d+)/(\d+)(?:/(\d+))?[^"]*"',
                        re.IGNORECASE
                    )
                    matches = download_pattern.findall(response.text)
                    if matches:
                        article_num, file_num, version_num = matches[0]
                        version = version_num if version_num else '754'  # Default version from known example
                        pdf_url = f"https://jestp.com/menuscript/index.php/estp/article/download/{article_num}/{file_num}/{version}"
                        logger.debug(f"Publisher resolver (JESTP) encontrou URL {pdf_url}")
                        return pdf_url
            except requests.RequestException as e:
                logger.debug(f"JESTP landing page scrape failed: {e}")
        except (IndexError, ValueError) as e:
            logger.debug(f"JESTP pattern extraction failed: {e}")
        
        return None
    
    def _resolve_ieiespc(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Resolve IEIESPC (International Electronics and Informatics Engineering Society in Pacific) PDFs.
        
        Pattern: Publisher website with specific download endpoints
        DOI format: 10.5573/ieiespc.{year}.{volume}.{issue}.{start_page}
        Example: 10.5573/ieiespc.2020.9.3.217
        
        Note: This publisher often has PDFs cached by SemanticScholar as well.
        """
        if not doi.lower().startswith('10.5573/ieiespc.'):
            return None
        
        try:
            # Try landing page scraping for download link
            landing_url = f"https://doi.org/{doi}"
            
            response = self.session.get(landing_url, timeout=15, allow_redirects=True)
            if response.status_code == 200:
                # Look for direct PDF download links
                pdf_patterns = [
                    re.compile(r'href="([^"]*\.pdf[^"]*)"', re.IGNORECASE),
                    re.compile(r'href="([^"]*download[^"]*pdf[^"]*)"', re.IGNORECASE),
                ]
                
                for pattern in pdf_patterns:
                    matches = pattern.findall(response.text)
                    for match in matches:
                        absolute_url = urljoin(response.url, match)
                        if absolute_url.lower().endswith('.pdf'):
                            logger.debug(f"Publisher resolver (IEIESPC) encontrou URL {absolute_url}")
                            return absolute_url
        except requests.RequestException as e:
            logger.debug(f"IEIESPC landing page scrape failed: {e}")
        
        return None
    
    def _resolve_author_site(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Resolve PDFs hosted on author personal/institutional websites.
        
        Uses author names and paper title to construct likely URLs.
        Example: CMU thesis 10.1184/r1/6715271.v1 -> https://chrismaclellan.com/media/publications/MacLellan-Camera-Ready.pdf
        """
        authors = paper.get('authors', '').strip()
        title = paper.get('title', '').strip()
        
        if not authors or not title:
            return None
        
        # Extract first author last name
        first_author = authors.split(';')[0].strip()
        # Try to get last name (assumes "First Last" or "F. Last" format)
        name_parts = first_author.split()
        if not name_parts:
            return None
        
        last_name = name_parts[-1].strip().lower()
        
        # Common academic site patterns
        domain_patterns = [
            f"https://{last_name}.com/media/publications/",
            f"https://{last_name}.github.io/papers/",
            f"https://www.{last_name}.com/papers/",
            f"https://{last_name}.net/publications/",
        ]
        
        # Try to construct filename from title (simple heuristic)
        # Remove common words, take first few significant words
        title_words = [w for w in title.replace('-', ' ').split() if len(w) > 3][:3]
        filename_base = '-'.join(title_words)
        
        for domain in domain_patterns:
            for suffix in ['.pdf', '-Camera-Ready.pdf', '-Final.pdf', '-Preprint.pdf']:
                pdf_url = f"{domain}{filename_base}{suffix}"
                logger.debug(f"Publisher resolver (Author Site) tentando URL {pdf_url}")
                
                # Quick HEAD request to validate
                try:
                    head_resp = self.session.head(pdf_url, timeout=10, allow_redirects=True)
                    if head_resp.status_code == 200:
                        content_type = head_resp.headers.get('content-type', '').lower()
                        if 'pdf' in content_type:
                            logger.debug(f"Publisher resolver (Author Site) validou URL {pdf_url}")
                            return pdf_url
                except requests.RequestException:
                    continue
        
        return None
    
    def _resolve_semantic_scholar_cached(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Resolve PDFs cached by SemanticScholar.
        
        SemanticScholar often has cached PDFs available even when the paper itself is paywalled.
        These are typically author preprints or versions hosted on institutional repositories.
        Example: 10.5573/ieiespc.2020.9.3.217 -> https://pdfs.semanticscholar.org/f929/f28e5c893999ec30a2435a5d6bc8b4fb070d.pdf
        """
        if doi in self.semantic_scholar_cache:
            return self.semantic_scholar_cache[doi]
        
        # Try SemanticScholar API to get paper details including cached PDFs
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
        params = {"fields": "openAccessPdf,isOpenAccess"}
        
        try:
            response = self.session.get(api_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Check for cached PDF
                if data.get('isOpenAccess') and data.get('openAccessPdf'):
                    pdf_url = data['openAccessPdf'].get('url')
                    if pdf_url:
                        logger.debug(f"Publisher resolver (SemanticScholar Cached) retornou {pdf_url}")
                        self.semantic_scholar_cache[doi] = pdf_url
                        return pdf_url
        except requests.RequestException as e:
            logger.debug(f"SemanticScholar cached PDF check failed: {e}")
        
        self.semantic_scholar_cache[doi] = None
        return None

    def _resolve_doi_landing(self, doi: str, _: Dict[str, Any]) -> Optional[str]:
        doi_url = f"https://doi.org/{doi}"
        try:
            response = self.session.get(
                doi_url,
                timeout=20,
                allow_redirects=True,
                headers={'Accept': 'text/html,application/xhtml+xml'}
            )
        except requests.RequestException:
            return None

        content_type = (response.headers.get('content-type') or '').lower()
        if 'html' not in content_type:
            return None

        matches = self.PDF_LINK_PATTERN.findall(response.text)
        for match in matches:
            absolute = urljoin(response.url, match)
            if absolute.lower().startswith('http'):
                logger.debug(f"Publisher resolver (DOI landing) encontrou {absolute}")
                return absolute
        return None
    
    def _resolve_researchgate(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Tenta encontrar paper no ResearchGate via DOI."""
        if not doi:
            return None
        
        # ResearchGate search by DOI
        search_url = f"https://www.researchgate.net/search/publication?q={quote_plus(doi)}"
        try:
            response = self.session.get(
                search_url,
                timeout=15,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html'
                }
            )
            if response.status_code == 200:
                # Look for publication links in results
                pub_pattern = re.compile(r'href="(/publication/\d+[^"]+)"')
                matches = pub_pattern.findall(response.text)
                if matches:
                    pub_url = f"https://www.researchgate.net{matches[0]}"
                    logger.debug(f"Publisher resolver (ResearchGate) encontrou {pub_url}")
                    return pub_url
        except requests.RequestException as e:
            logger.debug(f"ResearchGate search failed: {e}")
        return None
    
    def _resolve_academia_edu(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Tenta encontrar paper no Academia.edu via título."""
        title = paper.get('title', '').strip()
        if not title:
            return None
        
        # Academia.edu search by title
        search_url = f"https://www.academia.edu/search?q={quote_plus(title)}"
        try:
            response = self.session.get(
                search_url,
                timeout=15,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html'
                }
            )
            if response.status_code == 200:
                # Look for paper links
                paper_pattern = re.compile(r'href="(/\d+/[^"]+)"')
                matches = paper_pattern.findall(response.text)
                if matches:
                    paper_url = f"https://www.academia.edu{matches[0]}"
                    logger.debug(f"Publisher resolver (Academia.edu) encontrou {paper_url}")
                    return paper_url
        except requests.RequestException as e:
            logger.debug(f"Academia.edu search failed: {e}")
        return None
    
    def _resolve_alternative_doi_services(self, doi: str, paper: Dict[str, Any]) -> Optional[str]:
        """Try alternative DOI resolution services as last resort.
        
        Note: This includes services that may have legal implications in some jurisdictions.
        Enable only if you understand and accept the legal risks.
        """
        # Sci-Hub mirrors (use with caution - legal status varies by jurisdiction)
        # Disabled by default for legal compliance
        # Uncomment the following to enable (at your own risk):
        
        # scihub_mirrors = [
        #     "https://sci-hub.se",
        #     "https://sci-hub.st",
        #     "https://sci-hub.ru",
        # ]
        # 
        # for mirror in scihub_mirrors:
        #     try:
        #         scihub_url = f"{mirror}/{doi}"
        #         logger.debug(f"Trying alternative DOI service: {scihub_url}")
        #         response = self.session.get(scihub_url, timeout=10, allow_redirects=True)
        #         if response.status_code == 200:
        #             # Extract PDF link from page
        #             pdf_match = re.search(r'(https?://[^"\']+\.pdf[^"\']*)', response.text)
        #             if pdf_match:
        #                 pdf_url = pdf_match.group(1)
        #                 logger.debug(f"Alternative DOI service found PDF: {pdf_url}")
        #                 return pdf_url
        #     except requests.RequestException:
        #         continue
        
        # Alternative: unpaywall.org direct API (legal and recommended)
        # This is already handled in _try_get_pdf_url via UnpaywallClient
        
        return None


class DeepReviewAnalyzer:
    """Analisador aprofundado de papers da revisão sistemática."""
    
    def __init__(self, db_path: Optional[str] = None, config: Optional[AppConfig] = None):
        # Carregar configuração (ou reutilizar instância injetada)
        self.config = config or load_config()

        # Permitir override do caminho do banco; caso contrário, usar o configurado
        resolved_db_path = Path(db_path or self.config.database.db_path)
        self.db_path = resolved_db_path.resolve()
        self.papers: List[Dict[str, Any]] = []
        self.enriched_papers: List[Dict[str, Any]] = []

        # Diretório padrão de saída baseado em exports configurado (mantém compatibilidade com overrides posteriores)
        self.output_dir = Path(self.config.database.exports_dir) / "deep_analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar cliente Semantic Scholar para reutilizar infraestrutura (retry, rate limit, headers)
        self.semantic_client = SemanticScholarClient(self.config)
        
        # Reutilizar a sessão HTTP robusta do cliente
        self.session = self.semantic_client.session
        self.publisher_resolver = PublisherPDFResolver(self.session)
        
        # Configurar rate limiting para Unpaywall
        self.unpaywall_delay = 1.0  # segundos entre requests
        self.last_unpaywall_request = 0

        # Cliente Crossref para fallback de PDF
        self.crossref_client = CrossrefClient(self.config)
        
        # Cliente CORE para fallback OA repository
        self.core_client = COREClient(self.config)
        
        # HTML PDF scraper for landing pages
        self.html_scraper = HTMLPDFScraper(session=self.session)
        
        # User agent rotation pool for avoiding blocks
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        self.current_ua_index = 0

        # Overrides manuais de PDF (arquivo opcional)
        self.manual_pdf_overrides: Dict[str, str] = {}
        
        # HTML cache directory for debugging
        self.html_cache_dir = self.output_dir / "html_cache"
        self.html_cache_dir.mkdir(exist_ok=True)
        
        # Author contact tracking
        self.author_emails: Dict[str, List[str]] = {}  # doi -> [emails]
        
        # Retry configuration for network errors
        self.max_retries = 3
        self.retry_backoff_base = 2  # exponential backoff: 2^attempt seconds
        overrides_path = self.output_dir / "manual_pdf_overrides.json"
        if overrides_path.exists():
            try:
                with open(overrides_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        # normalizar chaves (DOI) para lowercase
                        self.manual_pdf_overrides = {k.lower(): v for k, v in data.items() if isinstance(v, str)}
                        logger.info(f"🔧 Overrides manuais de PDF carregados: {len(self.manual_pdf_overrides)} entradas")
            except Exception as e:
                logger.warning(f"Não foi possível carregar overrides manuais de PDF: {e}")
        
    def load_included_papers(self) -> List[Dict[str, Any]]:
        """
        Carrega os papers incluídos e não duplicados do banco.
        Usa GROUP BY doi para garantir apenas um registro por paper único.
        """
        logger.info("Carregando papers incluídos (não duplicados) do banco de dados...")
        
        db_path = self.db_path
        if not db_path.exists():
            raise FileNotFoundError(f"Banco de dados não encontrado em {db_path}")

        conn = sqlite3.connect(str(db_path))
        try:
            conn.row_factory = sqlite3.Row
            # Usar MAX(rowid) para pegar o registro mais recente de cada DOI único
            cursor = conn.execute("""
                SELECT p.*
                FROM papers p
                INNER JOIN (
                    SELECT doi, MAX(rowid) as max_rowid
                    FROM papers 
                    WHERE selection_stage = 'included' 
                      AND (is_duplicate = 0 OR is_duplicate IS NULL)
                      AND doi IS NOT NULL
                      AND doi != ''
                    GROUP BY doi
                ) unique_papers ON p.doi = unique_papers.doi AND p.rowid = unique_papers.max_rowid
                ORDER BY COALESCE(p.relevance_score, 0) DESC,
                         COALESCE(p.citation_count, 0) DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            papers = [dict(row) for row in rows]
        finally:
            conn.close()
        
        logger.info(f"✅ {len(papers)} papers únicos carregados (por DOI)")
        self.papers = papers
        return papers
    
    def _try_get_pdf_url(self, paper: Dict[str, Any]) -> Optional[str]:
        """
        Tenta obter URL do PDF usando múltiplas estratégias:
        0. Override manual (manual_pdf_overrides.json)
        1. open_access_pdf do banco (já enriquecido anteriormente)
        2. Busca no Semantic Scholar API (reutiliza cliente existente)
        3. Unpaywall API (com rate limiting)
        4. Crossref link (campo link[] content-type application/pdf)
        5. Resolvedores específicos de publishers / DOI landing pages
        6. MCP Paper Search (se disponível)
        
        Retorna None se nenhuma estratégia funcionar.
        """
        doi = paper.get('doi', '')
        title = paper.get('title', '')
        normalized_doi = (doi or '').lower().strip()
        failure_reasons: List[str] = []

        # Estratégia 0: Override manual
        if normalized_doi and normalized_doi in self.manual_pdf_overrides:
            override_url = self.manual_pdf_overrides[normalized_doi]
            logger.info(f"📄 Usando override manual de PDF para '{title}': {override_url[:80]}...")
            paper['resolved_pdf_url'] = override_url
            return override_url
        
        # Estratégia 1: Usar open_access_pdf do banco
        if paper.get('open_access_pdf'):
            url = paper['open_access_pdf']
            # Skip IEEE URLs that return HTML
            if 'ieeexplore.ieee.org' not in url:
                logger.debug(f"📄 Usando PDF do banco: {url[:80]}...")
                paper['resolved_pdf_url'] = url
                return url
            else:
                failure_reasons.append('open_access_ieee_html')
        
        # Estratégia 2: Buscar no Semantic Scholar usando infraestrutura existente
        if doi:
            try:
                df = self.semantic_client.search(f'doi:{doi}', limit=1)
                if df is not None and not df.empty:
                    open_pdf = df.iloc[0].get('open_access_pdf')
                    if open_pdf and 'ieeexplore.ieee.org' not in open_pdf:
                        logger.info(f"📥 PDF encontrado via Semantic Scholar: {open_pdf[:80]}...")
                        paper['resolved_pdf_url'] = open_pdf
                        return open_pdf
                    else:
                        failure_reasons.append('semantic_ieee_html')
            except Exception as e:
                logger.debug(f"Semantic Scholar busca falhou: {e}")
                failure_reasons.append('semantic_error')
        
        # Estratégia 3: Tentar Unpaywall API com rate limiting (expandido para todas oa_locations)
        if doi:
            try:
                time_since_last = time.time() - self.last_unpaywall_request
                if time_since_last < self.unpaywall_delay:
                    time.sleep(self.unpaywall_delay - time_since_last)
                email = self.config.apis.user_email or "research@example.com"
                unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
                response = self.session.get(unpaywall_url, timeout=12)
                self.last_unpaywall_request = time.time()
                if response.status_code == 200:
                    data = response.json()
                    if data.get('is_oa'):
                        candidate_urls = []
                        # best_oa_location primeiro
                        best = (data.get('best_oa_location') or {})
                        if best.get('url_for_pdf'):
                            candidate_urls.append(best.get('url_for_pdf'))
                        # adicionar todas as outras localizações
                        for loc in data.get('oa_locations', []) or []:
                            url_for_pdf = loc.get('url_for_pdf') or loc.get('url')
                            if url_for_pdf and url_for_pdf not in candidate_urls:
                                candidate_urls.append(url_for_pdf)
                        # Tentar validar cada candidato (HEAD -> GET) e escolher o primeiro realmente PDF
                        for cand in candidate_urls:
                            if 'ieeexplore.ieee.org' in cand:
                                continue  # ignorar HTML paywall
                            try:
                                head_ok = False
                                try:
                                    head_resp = self.session.head(cand, timeout=6, allow_redirects=True)
                                    if head_resp.status_code == 200 and 'pdf' in (head_resp.headers.get('Content-Type','').lower()):
                                        head_ok = True
                                except Exception:
                                    pass
                                if not head_ok:
                                    get_resp = self.session.get(cand, timeout=15, stream=True)
                                    ctype = get_resp.headers.get('Content-Type','').lower()
                                    if get_resp.status_code == 200 and ('pdf' in ctype or cand.lower().endswith('.pdf')):
                                        logger.info(f"📥 PDF encontrado via Unpaywall (multi): {cand[:80]}...")
                                        paper['resolved_pdf_url'] = cand
                                        return cand
                                else:
                                    logger.info(f"📥 PDF encontrado via Unpaywall (HEAD): {cand[:80]}...")
                                    paper['resolved_pdf_url'] = cand
                                    return cand
                            except Exception as e_inner:
                                logger.debug(f"Falha ao validar candidato Unpaywall '{cand}': {e_inner}")
                                continue
                        failure_reasons.append('unpaywall_no_valid_pdf')
                    else:
                        failure_reasons.append('unpaywall_no_oa')
                else:
                    failure_reasons.append(f'unpaywall_status_{response.status_code}')
            except Exception as e:
                logger.debug(f"Unpaywall falhou: {e}")
                failure_reasons.append('unpaywall_error')
        
        # Estratégia 4: Crossref link
        if doi:
            try:
                crossref_pdf = self.crossref_client.get_pdf_link(doi)
                if crossref_pdf and 'ieeexplore.ieee.org' not in crossref_pdf:
                    paper['resolved_pdf_url'] = crossref_pdf
                    logger.info(f"📥 PDF encontrado via Crossref: {crossref_pdf[:80]}...")
                    return crossref_pdf
                else:
                    failure_reasons.append('crossref_no_pdf')
            except Exception as e:
                logger.debug(f"Crossref falhou: {e}")
                failure_reasons.append('crossref_error')
        
        # Estratégia 5: CORE.ac.uk OA repository aggregator
        if doi:
            try:
                core_pdf = self.core_client.get_pdf_url_by_doi(doi)
                if core_pdf:
                    paper['resolved_pdf_url'] = core_pdf
                    logger.info(f"📥 PDF encontrado via CORE: {core_pdf[:80]}...")
                    return core_pdf
                else:
                    failure_reasons.append('core_no_pdf')
            except Exception as e:
                logger.debug(f"CORE falhou: {e}")
                failure_reasons.append('core_error')
        
        # Estratégia 6: Resolvedores específicos de publisher / DOI
        publisher_pdf = self.publisher_resolver.resolve(paper)
        if publisher_pdf:
            if 'ieeexplore.ieee.org' in publisher_pdf and 'stampPDF' not in publisher_pdf:
                logger.debug("Ignorando URL IEEE não direta para PDF")
                failure_reasons.append('publisher_ieee_html')
            else:
                logger.info(f"📥 PDF encontrado via resolvedor específico: {publisher_pdf[:80]}...")
                paper['resolved_pdf_url'] = publisher_pdf
                return publisher_pdf
        else:
            failure_reasons.append('publisher_resolver_none')
        
        # Nenhuma estratégia funcionou
        paper['pdf_failure_reasons'] = failure_reasons
        paper['resolved_pdf_url'] = None
        return None
    
    def fetch_full_text(self, only_missing: bool = False) -> List[Dict[str, Any]]:
        """Baixa e extrai texto completo.
        Parametros:
          only_missing: se True, processa apenas papers sem full_text e nao presentes no cache.
        """
        if only_missing:
            logger.info("Iniciando extração apenas para artigos faltantes...")
        else:
            logger.info("Iniciando busca e extração de texto completo...")
        
        # Garantir a presença da chave 'full_text' em todos os registros
        # Evita KeyError em consumidores que assumem a existência do campo
        for p in self.papers:
            if 'full_text' not in p:
                p['full_text'] = None

        cache_file = self.output_dir / "full_texts_cache.json"
        
        # Carregar cache existente, se houver
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                full_texts_cache = json.load(f)
        else:
            full_texts_cache = {}

        # Etapa 1: Resolver URLs (sequencial para respeitar rate limits externos)
        for i, paper in enumerate(self.papers, 1):
            doi = paper.get('doi', paper.get('title', 'NO_ID'))
            title = paper.get('title', 'N/A')[:60]
            
            # Pular se o texto já estiver no cache
            if doi in full_texts_cache:
                logger.info(f"[{i}/{len(self.papers)}] ✓ Texto para '{title}' encontrado no cache.")
                paper['full_text'] = full_texts_cache[doi]
                continue

            if only_missing and paper.get('full_text'):
                logger.debug(f"[{i}/{len(self.papers)}] Ignorando já extraído '{title}' (only_missing).")
                continue

            logger.info(f"[{i}/{len(self.papers)}] Buscando PDF para '{title}'...")
            
            # Tentar obter URL do PDF
            pdf_url = self._try_get_pdf_url(paper)
            
            if not pdf_url:
                logger.warning(f"❌ Nenhuma fonte de PDF disponível para '{title}'.")
                # Garante chave presente mesmo em falha
                paper['full_text'] = None
                continue

        # Etapa 2: Download paralelo dos PDFs resolvidos (respeita cache)
        def _download_and_extract(paper: Dict[str, Any]):
            doi_inner = paper.get('doi', paper.get('title', 'NO_ID'))
            title_inner = paper.get('title', 'N/A')[:60]
            if doi_inner in full_texts_cache:
                paper['full_text'] = full_texts_cache[doi_inner]
                return
            pdf_url_inner = paper.get('resolved_pdf_url') or paper.get('open_access_pdf')
            if not pdf_url_inner:
                return
            logger.info(f"📥 (Parallel) Baixando PDF de: {pdf_url_inner[:80]}...")
            try:
                # HEAD rápido para confirmar PDF antes de GET pesado
                head_resp = None
                try:
                    head_resp = self.session.head(
                        pdf_url_inner,
                        timeout=8,
                        allow_redirects=True,
                        headers={'Accept': 'application/pdf,application/octet-stream;q=0.9,text/html;q=0.8','User-Agent': self._get_next_user_agent()}
                    )
                except Exception:
                    paper.setdefault('pdf_failure_reasons', []).append('head_error')
                if head_resp and head_resp.status_code == 200 and 'pdf' in head_resp.headers.get('Content-Type','').lower():
                    response = self.session.get(
                        pdf_url_inner,
                        timeout=30,
                        allow_redirects=True,
                        headers={'Accept': 'application/pdf,application/octet-stream;q=0.9,text/html;q=0.8','User-Agent': self._get_next_user_agent()}
                    )
                else:
                    response = self._try_protocol_fallback(pdf_url_inner, timeout=30)
                if not response:
                    paper.setdefault('pdf_failure_reasons', []).append('connection_exhausted')
                    return
                ctype = response.headers.get('content-type','').lower()
                if 'html' in ctype:
                    if 'ieeexplore.ieee.org' in pdf_url_inner and 'stampPDF' in pdf_url_inner:
                        extracted_link = self._extract_pdf_from_ieee_html(response.text)
                        if extracted_link:
                            secondary = self._try_protocol_fallback(extracted_link, timeout=30)
                            if secondary and 'pdf' in secondary.headers.get('content-type','').lower():
                                response = secondary
                                logger.info(f"✓ IEEE fallback successful for {title_inner}")
                            else:
                                paper.setdefault('pdf_failure_reasons', []).append('ieee_no_fallback_link')
                                paper['full_text'] = None
                                return
                        else:
                            paper.setdefault('pdf_failure_reasons', []).append('ieee_no_fallback_link')
                            paper['full_text'] = None
                            return
                    else:
                        try:
                            scraped_pdf_url = self.html_scraper.extract_pdf_url(response.text, response.url)
                            if scraped_pdf_url:
                                pdf_response = self._try_protocol_fallback(scraped_pdf_url, timeout=30)
                                if pdf_response and 'pdf' in pdf_response.headers.get('content-type','').lower():
                                    response = pdf_response
                                    logger.info(f"✓ Scraper fallback successful for {title_inner}")
                                else:
                                    paper.setdefault('pdf_failure_reasons', []).append('scraped_url_not_pdf')
                                    paper['full_text'] = None
                                    return
                            else:
                                paper.setdefault('pdf_failure_reasons', []).append('html_no_pdf_link')
                                paper['full_text'] = None
                                return
                        except Exception as scrape_error:
                            paper.setdefault('pdf_failure_reasons', []).append(f'html_scrape_error:{scrape_error.__class__.__name__}')
                            paper['full_text'] = None
                            return
                if 'pdf' not in response.headers.get('content-type','').lower():
                    paper['full_text'] = None
                    paper.setdefault('pdf_failure_reasons', []).append('not_pdf_content')
                    return
                pdf_file = io.BytesIO(response.content)
                reader = PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
                if text.strip():
                    paper['full_text'] = text
                    full_texts_cache[doi_inner] = text
                else:
                    paper['full_text'] = None
                    paper.setdefault('pdf_failure_reasons', []).append('empty_extraction')
            except requests.RequestException as e:
                paper['full_text'] = None
                paper.setdefault('pdf_failure_reasons', []).append(f'download_error:{e.__class__.__name__}')
            except Exception as e:
                paper['full_text'] = None
                paper.setdefault('pdf_failure_reasons', []).append(f'process_error:{e.__class__.__name__}')

        parallel_candidates = [p for p in self.papers if p.get('resolved_pdf_url') or p.get('open_access_pdf')]
        if parallel_candidates:
            logger.info(f"⏱ Iniciando download paralelo de {len(parallel_candidates)} PDFs...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                list(executor.map(_download_and_extract, parallel_candidates))
        else:
            logger.info("Nenhum PDF resolvido para download paralelo.")

        # Salvar o cache atualizado
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(full_texts_cache, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Cache de textos completos salvo em: {cache_file}")
        logger.info(f"✅ Total extraído: {sum(1 for p in self.papers if p.get('full_text'))} de {len(self.papers)}")
        return self.papers

    def _get_next_user_agent(self) -> str:
        """Get next user agent from rotation pool."""
        ua = self.user_agents[self.current_ua_index]
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        return ua
    
    def _exponential_backoff_retry(self, url: str, timeout: int = 25, max_attempts: int = None) -> Optional[requests.Response]:
        """Retry GET with exponential backoff; HEAD pré-checagem para PDF."""
        max_attempts = max_attempts or self.max_retries
        # HEAD pré-checagem (não retentativa)
        try:
            head_resp = self.session.head(
                url,
                timeout=min(10, timeout // 2),
                allow_redirects=True,
                headers={
                    'Accept': 'application/pdf,application/octet-stream;q=0.9,text/html;q=0.8',
                    'User-Agent': self._get_next_user_agent()
                }
            )
            if head_resp.status_code == 200 and 'pdf' in head_resp.headers.get('Content-Type','').lower():
                return self.session.get(
                    url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers={
                        'Accept': 'application/pdf,application/octet-stream;q=0.9,text/html;q=0.8',
                        'User-Agent': self._get_next_user_agent()
                    }
                )
        except Exception:
            pass
        for attempt in range(max_attempts):
            try:
                response = self.session.get(
                    url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers={
                        'Accept': 'application/pdf,application/octet-stream;q=0.9,text/html;q=0.8',
                        'User-Agent': self._get_next_user_agent()
                    }
                )
                return response
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < max_attempts - 1:
                    backoff_time = self.retry_backoff_base ** attempt
                    logger.debug(f"Network error on attempt {attempt+1}/{max_attempts}, retrying in {backoff_time}s: {e}")
                    time.sleep(backoff_time)
                else:
                    logger.warning(f"Network error after {max_attempts} attempts: {e}")
                    return None
            except requests.RequestException as e:
                logger.debug(f"Request exception (no retry): {e}")
                return None
        return None
    
    def _cache_html_content(self, url: str, html_content: str) -> None:
        """Cache HTML content for debugging."""
        try:
            # Create safe filename from URL hash
            url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            cache_file = self.html_cache_dir / f"{url_hash}.html"
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(f"<!-- URL: {url} -->\n")
                f.write(html_content)
            
            logger.debug(f"HTML cached: {cache_file.name}")
        except Exception as e:
            logger.debug(f"Failed to cache HTML: {e}")
    
    def _extract_author_emails(self, paper: Dict[str, Any]) -> List[str]:
        """Extract author emails from paper metadata and full text."""
        emails = set()
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # From metadata authors field
        authors = paper.get('authors', [])
        if isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict) and 'email' in author:
                    emails.add(author['email'])
        
        # From full text (common patterns near author names)
        full_text = paper.get('full_text', '')
        if full_text:
            # Extract first 3000 chars (usually contains author section)
            header_text = full_text[:3000]
            found_emails = email_pattern.findall(header_text)
            emails.update(found_emails)
        
        return list(emails)
    
    def _try_protocol_fallback(self, url: str, timeout: int = 25) -> Optional[requests.Response]:
        """Try HTTPS first, fallback to HTTP if connection fails, with exponential backoff.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Response object if successful, None otherwise
        """
        # Try original URL first with exponential backoff
        response = self._exponential_backoff_retry(url, timeout)
        if response:
            return response
        
        # Try HTTP fallback if original was HTTPS
        if url.startswith('https://'):
            http_url = url.replace('https://', 'http://', 1)
            logger.debug(f"Trying HTTP fallback with retry: {http_url}")
            response = self._exponential_backoff_retry(http_url, timeout)
            if response:
                return response
        
        return None
        
        # DEPRECATED OLD IMPLEMENTATION - keeping for reference
        # Try original URL first, then protocol fallback
        for protocol_attempt in range(2):
            try:
                current_url = url
                if protocol_attempt == 1 and url.startswith('https://'):
                    current_url = url.replace('https://', 'http://', 1)
                    logger.debug(f"Trying HTTP fallback: {current_url}")
                
                response = self.session.get(
                    current_url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers={
                        'Accept': 'application/pdf,application/octet-stream;q=0.9,text/html;q=0.8',
                        'User-Agent': self._get_next_user_agent()
                    }
                )
                response.raise_for_status()
                return response
            except (requests.ConnectionError, requests.Timeout) as e:
                if protocol_attempt == 0:
                    logger.debug(f"Connection failed, will try protocol fallback: {e.__class__.__name__}")
                    continue
                else:
                    raise
            except requests.HTTPError:
                # Don't fallback on HTTP errors (404, 403, etc)
                raise
        
        return None

    def _extract_pdf_from_ieee_html(self, html: str) -> Optional[str]:
        """Heurística simples para localizar link direto de PDF em página stamp IEEE.
        Procura padrões '.pdf' e retorna primeiro link absoluto detectado.
        """
        if not html:
            return None
        # Padrões comuns de embed
        matches = re.findall(r'(https://ieeexplore\.ieee\.org/[^"\']+\.pdf)', html)
        if matches:
            return matches[0]
        # Algumas páginas podem ter data-pdf attribute
        data_pdf = re.search(r'data-pdf-url="(https://[^"]+\.pdf)"', html)
        if data_pdf:
            return data_pdf.group(1)
        return None


    def generate_markdown_report(self) -> str:
        """Gera um relatório sobre a extração de texto completo."""
        logger.info("Gerando relatório Markdown...")
        
        total_papers = len(self.papers)
        successful_extractions = sum(1 for p in self.papers if p.get('full_text'))
        
        report = f"""# 📖 Relatório de Extração de Texto Completo

**Data da geração**: {time.strftime('%d/%m/%Y %H:%M')}  
**Total de papers únicos analisados**: {total_papers}  
**Textos completos extraídos com sucesso**: {successful_extractions} ({successful_extractions/total_papers:.1%})

Este relatório resume o sucesso da extração automática de texto. Os textos completos
foram salvos em `full_texts_cache.json`.

---
"""
        
        sorted_papers = sorted(
            self.papers,
            key=lambda x: (x.get('relevance_score', 0)),
            reverse=True
        )
        
        for i, paper in enumerate(sorted_papers, 1):
            status = "✅ Sucesso" if paper.get('full_text') else "❌ Falha"
            pdf_link = paper.get('resolved_pdf_url') or paper.get('open_access_pdf') or 'N/A'
            failure_reasons = ", ".join(paper.get('pdf_failure_reasons', [])) or 'N/A'

            report += f"""
    ### {i}. {paper.get('title', 'N/A')}

    - **DOI**: {paper.get('doi', 'N/A')}
    - **Status da Extração**: {status}
    - **Link do PDF (se disponível)**: {pdf_link}
    - **Motivos de Falha (se aplicável)**: {failure_reasons}
    ---
    """
        return report

    def _enrich_papers_metadata(self):
        """
        Enriquece os papers com metadados adicionais (presença de texto, keywords detectadas, etc.)
        """
        logger.info("Enriquecendo metadados dos papers...")
        
        self.enriched_papers = []
        keywords_to_detect = [
            'machine learning', 'deep learning', 'neural network',
            'data mining', 'predictive analytics', 'classification',
            'regression', 'clustering', 'assessment', 'evaluation',
            'education', 'learning analytics', 'student performance'
        ]
        
        for paper in self.papers:
            enriched = paper.copy()

            # Adicionar flag de texto completo
            enriched['has_full_text'] = bool(paper.get('full_text'))

            # Calcular comprimento do texto
            if enriched['has_full_text']:
                enriched['text_length'] = len(paper.get('full_text', ''))
            else:
                enriched['text_length'] = 0

            # Fonte para keywords (texto completo ou abstract como fallback)
            detected_keywords: List[str] = []
            keyword_source = 'none'
            if enriched['has_full_text']:
                full_text_lower = paper.get('full_text', '').lower()
                for keyword in keywords_to_detect:
                    if keyword in full_text_lower:
                        detected_keywords.append(keyword)
                keyword_source = 'full_text'
            else:
                abstract = (paper.get('abstract') or '').lower()
                if abstract:
                    for keyword in keywords_to_detect:
                        if keyword in abstract:
                            detected_keywords.append(keyword)
                    if detected_keywords:
                        keyword_source = 'abstract'

            enriched['detected_keywords'] = detected_keywords
            enriched['keyword_source'] = keyword_source
            enriched['resolved_pdf_url'] = paper.get('resolved_pdf_url')
            if paper.get('pdf_failure_reasons'):
                enriched['pdf_failure_reasons'] = paper.get('pdf_failure_reasons')

            # Remover o texto completo do enriched (muito grande para o JSON)
            enriched.pop('full_text', None)

            self.enriched_papers.append(enriched)
        
        logger.info(f"✅ {len(self.enriched_papers)} papers enriquecidos com metadados")

    def _calculate_statistics(self) -> Dict[str, Any]:
        """
        Calcula estatísticas gerais sobre os papers analisados.
        """
        logger.info("Calculando estatísticas da análise...")
        
        total_papers = len(self.papers)
        successful_extractions = sum(1 for p in self.papers if p.get('full_text'))
        extraction_rate = (successful_extractions / total_papers * 100) if total_papers > 0 else 0
        
        # Estatísticas de ano
        years = [p.get('year') for p in self.papers if p.get('year')]
        year_range = f"{min(years)}-{max(years)}" if years else "N/A"
        
        from collections import Counter
        years_distribution = Counter(years)
        
        # Estatísticas de citações
        citations = [p.get('citationCount', 0) for p in self.papers if p.get('citationCount') is not None]
        avg_citations = sum(citations) / len(citations) if citations else 0
        max_citations = max(citations) if citations else 0
        total_citations = sum(citations)
        
        # Top venues
        venues = [p.get('venue', 'Unknown') for p in self.papers if p.get('venue')]
        venue_counts = Counter(venues)
        top_venues = venue_counts.most_common(10)
        
        # Técnicas detectadas
        all_keywords = []
        for p in self.enriched_papers:
            all_keywords.extend(p.get('detected_keywords', []))
        detected_techniques = Counter(all_keywords)
        
        # Cobertura de abstracts (fallback)
        abstract_only = sum(1 for p in self.papers if not p.get('full_text') and p.get('abstract'))

        # Distribuição de motivos de falha
        from collections import Counter
        failure_counter = Counter()
        for p in self.papers:
            for reason in p.get('pdf_failure_reasons', []):
                failure_counter[reason] += 1

        stats = {
            'total_papers': total_papers,
            'successful_extractions': successful_extractions,
            'extraction_rate': round(extraction_rate, 1),
            'year_range': year_range,
            'years_distribution': dict(years_distribution),
            'avg_citations': round(avg_citations, 1),
            'max_citations': max_citations,
            'total_citations': total_citations,
            'top_venues': [{'venue': v, 'count': c} for v, c in top_venues],
            'detected_techniques': dict(detected_techniques.most_common(15)),
            'abstract_only_enriched': abstract_only,
            'failure_reason_counts': dict(failure_counter),
            'generated_at': datetime.datetime.now().isoformat()
        }
        
        logger.info(f"✅ Estatísticas calculadas: {extraction_rate:.1f}% taxa de extração")
        return stats

    def _generate_deep_analysis_report(self, stats: Dict[str, Any]) -> str:
        """
        Gera relatório markdown completo da análise aprofundada.
        """
        logger.info("Gerando relatório de análise aprofundada...")
        
        report = f"""# 📊 Relatório de Análise Aprofundada - Revisão Sistemática

**Data de Geração**: {stats['generated_at']}

## 📈 Estatísticas Gerais

- **Total de Papers Analisados**: {stats['total_papers']}
- **Textos Completos Extraídos**: {stats['successful_extractions']} ({stats['extraction_rate']}%)
- **Período Coberto**: {stats['year_range']}
- **Total de Citações**: {stats['total_citations']}
- **Média de Citações por Paper**: {stats['avg_citations']}
- **Paper Mais Citado**: {stats['max_citations']} citações
- **Abstracts Usados como Fallback**: {stats['abstract_only_enriched']}

### Distribuição por Ano

"""        
        for year in sorted(stats['years_distribution'].keys()):
            count = stats['years_distribution'][year]
            report += f"- **{year}**: {count} papers\n"
        
        report += "\n## 🔬 Técnicas e Abordagens Detectadas\n\n"
        
        if stats['detected_techniques']:
            for technique, count in sorted(stats['detected_techniques'].items(), key=lambda x: x[1], reverse=True):
                report += f"- **{technique}**: mencionado em {count} papers\n"
        else:
            report += "*Nenhuma técnica específica detectada nos textos extraídos.*\n"
        
        report += "\n## 📚 Top 10 Venues/Journals\n\n"
        
        for i, venue_info in enumerate(stats['top_venues'][:10], 1):
            report += f"{i}. **{venue_info['venue']}** - {venue_info['count']} papers\n"
        
        # Seção de motivos de falha
        report += "\n## ⚠️ Motivos de Falha na Aquisição de PDF\n\n"
        if stats['failure_reason_counts']:
            for reason, count in sorted(stats['failure_reason_counts'].items(), key=lambda x: x[1], reverse=True):
                report += f"- **{reason}**: {count} ocorrências\n"
        else:
            report += "*Nenhum motivo de falha registrado.*\n"

        report += "\n## 📄 Lista Completa de Papers Analisados\n\n"
        
        # Ordenar papers por relevância (score) ou citações
        sorted_papers = sorted(
            self.enriched_papers, 
            key=lambda p: (p.get('relevance_score', 0), p.get('citationCount', 0)),
            reverse=True
        )
        
        for i, paper in enumerate(sorted_papers, 1):
            title = paper.get('title', 'N/A')
            authors = paper.get('authors', 'N/A')
            year = paper.get('year', 'N/A')
            venue = paper.get('venue', 'N/A')
            citations = paper.get('citationCount', 0)
            has_text = "✅" if paper.get('has_full_text') else "❌"
            text_len = paper.get('text_length', 0)
            keywords = ", ".join(paper.get('detected_keywords', [])) or "Nenhuma"
            keyword_source = paper.get('keyword_source', 'none')
            failure_reasons = ", ".join(paper.get('pdf_failure_reasons', [])) or "-"
            resolved_pdf = paper.get('resolved_pdf_url') or 'N/A'
            
            report += f"""### {i}. {title}

- **Autores**: {authors}
- **Ano**: {year}
- **Venue**: {venue}
- **Citações**: {citations}
- **Texto Completo**: {has_text}
- **Tamanho do Texto**: {text_len:,} caracteres
- **Keywords Detectadas**: {keywords}
- **Fonte das Keywords**: {keyword_source}
- **Link PDF Resolvido**: {resolved_pdf}
- **Falhas de PDF**: {failure_reasons}
- **DOI**: {paper.get('doi', 'N/A')}

---

"""
        
        report += """## 🔍 Notas Metodológicas

Esta análise foi realizada através do seguinte processo:

1. **Carregamento de Dados**: Papers marcados como 'included' foram carregados do banco de dados
2. **Deduplicação**: Papers duplicados (mesmo DOI) foram removidos
3. **Busca de PDFs**: Tentativa de localizar PDFs através de múltiplas estratégias:
   - Semantic Scholar Open Access
   - Unpaywall API
   - Resolvedores específicos de publishers (IEEE, IntechOpen, OpenAlex)
4. **Extração de Texto**: PDFs baixados foram processados com pypdf
5. **Análise de Keywords**: Texto completo foi analisado para detectar técnicas e abordagens
6. **Estatísticas**: Métricas agregadas foram calculadas sobre o corpus

---

*Relatório gerado automaticamente pela ferramenta de Análise Aprofundada*
"""
        
        logger.info("✅ Relatório de análise aprofundada gerado")
        return report
    
    def _generate_author_contact_file(self) -> None:
        """Gera arquivo JSON com informações para contato com autores de papers sem PDF."""
        failed_papers = [p for p in self.papers if not p.get('full_text')]
        
        if not failed_papers:
            logger.info("Todos os papers têm texto completo, não há necessidade de contato com autores")
            return
        
        contact_info = []
        
        for paper in failed_papers:
            # Extract emails from paper
            emails = self._extract_author_emails(paper)
            
            # Store in tracking dict
            doi = paper.get('doi', paper.get('title', 'UNKNOWN'))
            if emails:
                self.author_emails[doi] = emails
            
            # Build contact entry
            authors_list = paper.get('authors', [])
            if isinstance(authors_list, str):
                authors_str = authors_list
            elif isinstance(authors_list, list):
                authors_str = ", ".join([a.get('name', str(a)) if isinstance(a, dict) else str(a) for a in authors_list[:3]])
            else:
                authors_str = "Unknown"
            
            contact_entry = {
                'title': paper.get('title', 'N/A'),
                'authors': authors_str,
                'year': paper.get('year'),
                'doi': paper.get('doi'),
                'venue': paper.get('venue'),
                'extracted_emails': emails,
                'failure_reasons': paper.get('pdf_failure_reasons', []),
                'resolved_pdf_url': paper.get('resolved_pdf_url'),
                'email_template': self._generate_email_template(paper)
            }
            contact_info.append(contact_entry)
        
        # Save to JSON
        contact_file = self.output_dir / "author_contact_info.json"
        with open(contact_file, 'w', encoding='utf-8') as f:
            json.dump(contact_info, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Informações de contato com autores salvas em: {contact_file}")
        logger.info(f"📧 {len(failed_papers)} papers sem PDF, {sum(1 for c in contact_info if c['extracted_emails'])} com emails identificados")
    
    def _generate_email_template(self, paper: Dict[str, Any]) -> str:
        """Gera template de email para solicitar PDF aos autores."""
        title = paper.get('title', 'N/A')
        doi = paper.get('doi', 'N/A')
        year = paper.get('year', 'N/A')
        
        template = f"""Subject: Request for Full Text - {title[:60]}...

Dear Authors,

I am conducting a systematic review on computational thinking and would greatly appreciate access to your publication:

Title: {title}
DOI: {doi}
Year: {year}

I was unable to access the full text through institutional channels. Would you be willing to share a PDF copy for academic research purposes?

Thank you for your consideration.

Best regards,
[Your Name]
[Your Institution]
[Your Email]
"""
        return template
    
    def _update_database_with_full_texts(self):
        """Atualiza o banco SQLite com os textos completos extraídos."""
        logger.info("Atualizando banco de dados com textos completos...")
        
        conn = sqlite3.connect(str(self.db_path))
        try:
            cursor = conn.cursor()
            updated_count = 0
            
            for paper in self.papers:
                paper_id = paper.get('id')
                full_text = paper.get('full_text')
                text_length = paper.get('text_length', 0)
                
                if paper_id and full_text:
                    # Atualizar paper com texto completo
                    cursor.execute("""
                        UPDATE papers 
                        SET full_text = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (full_text, paper_id))
                    updated_count += 1
            
            conn.commit()
            logger.info(f"✅ {updated_count} papers atualizados no banco com texto completo")
        except Exception as e:
            logger.error(f"Erro ao atualizar banco de dados: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def _export_papers_json(self):
        """Exporta papers.json consolidado com textos completos integrados."""
        logger.info("Exportando papers.json consolidado...")
        
        conn = sqlite3.connect(str(self.db_path))
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM papers 
                ORDER BY 
                    CASE WHEN selection_stage = 'included' THEN 0 ELSE 1 END,
                    COALESCE(relevance_score, 0) DESC,
                    COALESCE(citation_count, 0) DESC
            """)
            rows = cursor.fetchall()
            papers = [dict(row) for row in rows]
            cursor.close()
        finally:
            conn.close()
        
        # Exportar para papers.json
        export_dir = Path(self.config.database.exports_dir) / "analysis"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        papers_json_file = export_dir / "papers.json"
        with open(papers_json_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Papers.json consolidado exportado: {papers_json_file}")
        logger.info(f"   Total de papers: {len(papers)}")
        logger.info(f"   Papers com texto completo: {sum(1 for p in papers if p.get('full_text'))}")

    def run_full_analysis(self, only_missing: bool = False):
        """Executa a análise completa.
        Parametros:
          only_missing: se True, tenta extrair texto apenas dos artigos ainda sem full_text
            (acelera iterações posteriores). Metadata e relatórios ainda são atualizados.
        """
        logger.info("=== INICIANDO ANÁLISE APROFUNDADA COMPLETA ===")
        
        # 1. Carregar papers únicos
        self.load_included_papers()
        
        if not self.papers:
            logger.warning("Nenhum paper encontrado para análise. Encerrando.")
            return {'total_papers': 0, 'message': 'Nenhum paper incluído foi encontrado.'}
            
        # 2. Tenta baixar e extrair o texto completo (modo seletivo opcional)
        self.fetch_full_text(only_missing=only_missing)
        
        # 3. Enriquecer metadados dos papers
        self._enrich_papers_metadata()
        
        # 4. Calcular estatísticas
        stats = self._calculate_statistics()
        
        # 5. Atualizar banco SQLite com textos completos
        self._update_database_with_full_texts()
        
        # 6. Exportar papers.json consolidado
        self._export_papers_json()
        
        # 7. Gerar relatórios
        extraction_report = self.generate_markdown_report()
        deep_analysis_report = self._generate_deep_analysis_report(stats)
        
        # 8. Salvar arquivos
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Relatório de extração (original)
        extraction_report_file = self.output_dir / "FULL_TEXT_EXTRACTION_REPORT.md"
        with open(extraction_report_file, 'w', encoding='utf-8') as f:
            f.write(extraction_report)
        logger.info(f"✅ Relatório de extração salvo em: {extraction_report_file}")
        
        # Relatório de análise aprofundada (novo)
        deep_analysis_file = self.output_dir / "DEEP_ANALYSIS_REPORT.md"
        with open(deep_analysis_file, 'w', encoding='utf-8') as f:
            f.write(deep_analysis_report)
        logger.info(f"✅ Relatório de análise aprofundada salvo em: {deep_analysis_file}")
        
        # Cache de papers enriquecidos (novo)
        enriched_cache_file = self.output_dir / "enriched_papers_cache.json"
        with open(enriched_cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.enriched_papers, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Cache de papers enriquecidos salvo em: {enriched_cache_file}")
        
        # Resumo de análises (novo)
        analyses_summary_file = self.output_dir / "analyses_summary.json"
        with open(analyses_summary_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Resumo de análises salvo em: {analyses_summary_file}")
        
        # Gerar arquivo de contato com autores para papers sem PDF
        self._generate_author_contact_file()
        
        # Retornar resultados expandidos
        return {
            'total_papers': len(self.papers),
            'successful_extractions': sum(1 for p in self.papers if p.get('full_text')),
            'extraction_rate': stats['extraction_rate'],
            'year_range': stats['year_range'],
            'avg_citations': stats['avg_citations'],
            'report_file': str(extraction_report_file),
            'deep_analysis_file': str(deep_analysis_file),
            'enriched_cache_file': str(enriched_cache_file),
            'analyses_summary_file': str(analyses_summary_file),
            'cache_file': str(self.output_dir / "full_texts_cache.json")
        }


if __name__ == "__main__":
    import os, sys
    only_missing_flag = False
    # Prioridade: argumento CLI --only-missing ou env var ONLY_MISSING_FULLTEXT=1
    if any(arg in ("--only-missing", "-m") for arg in sys.argv[1:]) or os.getenv("ONLY_MISSING_FULLTEXT") == "1":
        only_missing_flag = True
        print("[INFO] Executando em modo only-missing (apenas artigos sem texto).")
    analyzer = DeepReviewAnalyzer()
    results = analyzer.run_full_analysis(only_missing=only_missing_flag)
    print(f"\n✅ Análise concluída: {results}")
