"""
Enhanced HTML PDF link extractor using BeautifulSoup.
Extracts PDF download links from publisher landing pages.
"""

import logging
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class HTMLPDFScraper:
    """Scrapes HTML landing pages to find embedded PDF download links."""
    
    # Common patterns for PDF links in various publishers
    PDF_LINK_PATTERNS = [
        # Direct PDF links
        r'\.pdf$',
        r'/pdf/',
        r'/download/',
        r'getPDF',
        r'download.*pdf',
        r'pdf.*download',
        # Publisher-specific
        r'fulltext',
        r'article/view',
        r'content/pdf',
        r'render.*type.*pdf',
    ]
    
    # CSS selectors for common PDF link locations
    PDF_SELECTORS = [
        'a[href*=".pdf"]',
        'a[href*="/pdf"]',
        'a[href*="download"]',
        'a.pdf-link',
        'a.download-link',
        'a[title*="PDF"]',
        'a[title*="Download"]',
        'button[onclick*="pdf"]',
        'meta[name="citation_pdf_url"]',
        'meta[property="og:url"][content*=".pdf"]',
    ]
    
    # Keywords indicating PDF download buttons/links
    PDF_KEYWORDS = [
        'download pdf',
        'view pdf',
        'full text pdf',
        'download article',
        'get pdf',
        'pdf full',
        'article pdf',
        'télécharger pdf',
        'descargar pdf',
    ]
    
    def __init__(self, session=None):
        """
        Initialize scraper.
        
        Args:
            session: Optional requests.Session for HTTP requests
        """
        self.session = session
    
    def extract_pdf_url(self, html_content: str, base_url: str) -> Optional[str]:
        """
        Extract PDF URL from HTML content.
        
        Args:
            html_content: HTML page content
            base_url: Base URL for resolving relative links
            
        Returns:
            Absolute PDF URL if found, None otherwise
        """
        if not html_content:
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Strategy 1: Check meta tags (highest priority)
            pdf_url = self._extract_from_meta_tags(soup, base_url)
            if pdf_url:
                logger.debug(f"Found PDF in meta tags: {pdf_url}")
                return pdf_url
            
            # Strategy 2: Look for links with PDF patterns
            pdf_url = self._extract_from_links(soup, base_url)
            if pdf_url:
                logger.debug(f"Found PDF in links: {pdf_url}")
                return pdf_url
            
            # Strategy 3: Search for buttons with PDF keywords
            pdf_url = self._extract_from_buttons(soup, base_url)
            if pdf_url:
                logger.debug(f"Found PDF in buttons: {pdf_url}")
                return pdf_url
            
            # Strategy 4: Check iframe sources (some publishers embed PDFs)
            pdf_url = self._extract_from_iframes(soup, base_url)
            if pdf_url:
                logger.debug(f"Found PDF in iframe: {pdf_url}")
                return pdf_url
            
            logger.debug("No PDF URL found in HTML content")
            return None
            
        except Exception as e:
            logger.error(f"Error parsing HTML for PDF extraction: {e}")
            return None
    
    def _extract_from_meta_tags(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract PDF URL from meta tags."""
        # Check citation_pdf_url (common in academic publishers)
        meta_citation = soup.find('meta', attrs={'name': 'citation_pdf_url'})
        if meta_citation and meta_citation.get('content'):
            return self._resolve_url(meta_citation['content'], base_url)
        
        # Check DC.identifier or DC.relation
        for dc_name in ['DC.identifier', 'DC.relation']:
            meta_dc = soup.find('meta', attrs={'name': dc_name})
            if meta_dc and meta_dc.get('content'):
                content = meta_dc['content']
                if '.pdf' in content.lower():
                    return self._resolve_url(content, base_url)
        
        return None
    
    def _extract_from_links(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract PDF URL from anchor tags."""
        # Try CSS selectors
        for selector in self.PDF_SELECTORS:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href and self._is_likely_pdf_url(href):
                        return self._resolve_url(href, base_url)
            except Exception:
                continue
        
        # Search all links for PDF patterns
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip().lower()
            
            # Check href matches PDF pattern
            if self._is_likely_pdf_url(href):
                return self._resolve_url(href, base_url)
            
            # Check link text contains PDF keywords
            for keyword in self.PDF_KEYWORDS:
                if keyword in text:
                    if href and not href.startswith('#'):
                        return self._resolve_url(href, base_url)
        
        return None
    
    def _extract_from_buttons(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract PDF URL from buttons with onclick handlers."""
        for button in soup.find_all(['button', 'input'], type=['button', 'submit']):
            onclick = button.get('onclick', '')
            text = button.get_text().strip().lower()
            
            # Check if button text suggests PDF
            pdf_related = any(kw in text for kw in self.PDF_KEYWORDS)
            
            if pdf_related and onclick:
                # Try to extract URL from onclick handler
                url_match = re.search(r'(?:window\.location|href)\s*=\s*[\'"]([^\'"]+)[\'"]', onclick)
                if url_match:
                    return self._resolve_url(url_match.group(1), base_url)
        
        return None
    
    def _extract_from_iframes(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract PDF URL from iframe sources."""
        for iframe in soup.find_all('iframe', src=True):
            src = iframe['src']
            if self._is_likely_pdf_url(src):
                return self._resolve_url(src, base_url)
        
        return None
    
    def _is_likely_pdf_url(self, url: str) -> bool:
        """Check if URL likely points to a PDF."""
        if not url:
            return False
        
        url_lower = url.lower()
        
        # Direct .pdf extension
        if url_lower.endswith('.pdf'):
            return True
        
        # Check patterns
        for pattern in self.PDF_LINK_PATTERNS:
            if re.search(pattern, url_lower):
                return True
        
        return False
    
    def _resolve_url(self, url: str, base_url: str) -> str:
        """Resolve relative URL to absolute."""
        if not url:
            return url
        
        # Already absolute
        if url.startswith(('http://', 'https://')):
            return url
        
        # Resolve relative to base
        return urljoin(base_url, url)
    
    def scrape_landing_page(self, url: str, timeout: int = 15) -> Optional[str]:
        """
        Fetch landing page and extract PDF URL.
        
        Args:
            url: Landing page URL
            timeout: Request timeout in seconds
            
        Returns:
            PDF URL if found, None otherwise
        """
        if not self.session:
            logger.warning("No session available for scraping")
            return None
        
        try:
            logger.debug(f"Scraping landing page: {url}")
            response = self.session.get(url, timeout=timeout)
            
            if response.status_code != 200:
                logger.debug(f"Landing page returned status {response.status_code}")
                return None
            
            # Check if we got redirected to a PDF directly
            if response.headers.get('Content-Type', '').startswith('application/pdf'):
                return response.url
            
            # Parse HTML and extract PDF link
            return self.extract_pdf_url(response.text, url)
            
        except Exception as e:
            logger.debug(f"Error scraping landing page {url}: {e}")
            return None
