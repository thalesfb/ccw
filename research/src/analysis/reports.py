"""Módulo para geração de relatórios da revisão sistemática."""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlsplit

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from .visualizations import ReviewVisualizer
from ..config import load_config
from ..database.manager import DatabaseManager
from ..processing.dedup import (
    audit_duplicate_candidates,
    deterministic_identity_duplicate_mask,
)

logger = logging.getLogger(__name__)

_CHART_PRESENTATION = {
    "prisma_flow": (
        "Fluxo operacional de seleção",
        "Representação operacional da seleção; não corresponde ao diagrama PRISMA 2020 completo.",
    ),
    "selection_funnel": (
        "Funil de registros do export operacional",
        "Etapas operacionais do export; não representa decisão científica de elegibilidade.",
    ),
    "papers_by_year": (
        "Registros por ano de publicação",
        "Distribuição temporal dos registros presentes no export operacional.",
    ),
    "techniques_distribution": (
        "Rótulos de técnicas no export",
        "Frequência de rótulos de técnicas extraídos dos registros do export.",
    ),
    "database_coverage": (
        "Registros por base de dados",
        "Distribuição dos registros pelas fontes de indexação consultadas.",
    ),
    "relevance_distribution": (
        "Distribuição dos escores operacionais",
        "Escores de priorização do export; não são medida de qualidade metodológica.",
    ),
}


def _normalise_external_url(value: object) -> str:
    """Return an HTTP(S) URL safe to expose as a report link.

    Some API records store a bare DOI in ``url``. Rendering that value as a
    relative HTML link produces a broken link, so normalize DOI-shaped values
    while rejecting unsupported schemes and malformed URLs.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    url = str(value).strip()
    if not url:
        return ""
    if re.match(r"^10\.\d{4,9}/\S+$", url, flags=re.IGNORECASE):
        return f"https://doi.org/{url}"
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in url):
        return ""
    try:
        parsed = urlsplit(url)
        if parsed.port == 0:
            return ""
    except ValueError:
        return ""
    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.netloc
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        return ""
    return url


def _normalise_html_whitespace(value: str) -> str:
    """Keep generated HTML stable and free of whitespace-only line changes."""
    return "\n".join(line.rstrip() for line in value.splitlines()).rstrip() + "\n"


def _format_pt_br_integer(value: int | float) -> str:
    """Format an integer count with Brazilian Portuguese thousands separators."""
    return f"{int(value):,}".replace(",", ".")

class ReportGenerator:
    """Gera relatórios completos da revisão sistemática."""

    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize report generator.

        Args:
            output_dir: Diretório para salvar relatórios
        """
        self.config = load_config()

        if output_dir is None:
            output_dir = Path(self.config.database.exports_dir) / "reports"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize visualizer
        self.visualizer = ReviewVisualizer(self.output_dir.parent / "visualizations")

        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    def _footer_html(self) -> str:
        """Return the shared public-site footer for generated reports."""
        return (
            '<footer class="site-footer"><div class="site-shell site-footer-inner">'
            '<p>Trabalho de Conclusão de Curso · Ciência da Computação · IFC Campus Videira</p>'
            '<p><a href="../../../results/tcc/index.html">TCC</a> · '
            '<a href="https://github.com/thalesfb/ccw" target="_blank" rel="noopener">Repositório</a></p>'
            '</div></footer>'
        )

    def _site_header_html(self) -> str:
        """Return the canonical responsive navigation used by public pages."""
        links = [
            ("Visão geral", "../../../", None),
            ("Revisão sistemática", "../../index.html", "page"),
            ("MMAT", "../analysis/mmat_current.html", None),
            ("Apresentação", "../../../presentation/", None),
            ("PTC", "../../../results/ptc/index.html", None),
            ("TCC", "../../../results/tcc/index.html", None),
            ("Repositório", "https://github.com/thalesfb/ccw", None),
        ]

        def render_links(class_name: str) -> str:
            rendered = []
            for label, href, current in links:
                current_attr = ' aria-current="page"' if current else ""
                target_attrs = ' target="_blank" rel="noopener"' if href.startswith("https://") else ""
                rendered.append(f'<a href="{href}"{current_attr}{target_attrs}>{label}</a>')
            return f'<nav class="site-nav {class_name}" aria-label="Navegação principal">{"".join(rendered)}</nav>'

        desktop_nav = render_links("site-nav-desktop")
        mobile_nav = render_links("site-nav-mobile").replace(
            "<nav ", '<nav id="site-primary-nav" ', 1
        )
        return (
            '<header class="site-header"><div class="site-shell site-header-inner">'
            '<a class="site-brand" href="../../../" aria-label="CCW — voltar à visão geral">'
            '<img src="../../../public-site/assets/ifc-campus-videira-horizontal.png" '
            'alt="Instituto Federal Catarinense — Campus Videira">'
            '<span class="site-brand-copy"><strong>CCW</strong><small>Pesquisa versionada<br>Ciência da Computação</small></span>'
            '</a>'
            f'{desktop_nav}'
            '<details class="site-menu"><summary class="site-menu-toggle" aria-label="Menu principal" '
            'aria-controls="site-primary-nav">Menu</summary>'
            f'{mobile_nav}'
            '</details></div></header>'
        )

    def _report_tabs_html(self, active_report: str) -> str:
        """Return the secondary navigation shared by the three report pages."""
        reports = [
            ("Resumo operacional", "summary_report.html", "summary"),
            ("Registros do export", "papers_report_included.html", "papers"),
            ("Exploração automatizada", "gap_analysis.html", "gaps"),
        ]
        links = []
        for label, href, key in reports:
            current_attr = ' aria-current="page"' if key == active_report else ""
            links.append(f'<a href="{href}"{current_attr}>{label}</a>')
        return f'<nav class="report-tabs" aria-label="Relatórios do processamento">{"".join(links)}</nav>'

    def generate_summary_report(
        self,
        df: pd.DataFrame,
        stats: Optional[Dict] = None,
        config: Optional[Dict] = None,
        fulltext_stats: Optional[Dict] = None
    ) -> Path:
        """Generate summary report with key statistics.

        Args:
            df: DataFrame with papers
            stats: PRISMA statistics
            config: Configuration used
            fulltext_stats: Full-text extraction statistics (optional)

        Returns:
            Path to generated report
        """
        logger.info("Generating summary report...")

        # Generate statistics
        report_stats = self._calculate_statistics(df, stats)

        # Generate visualizations (pass calculated PRISMA stats)
        chart_paths = self.visualizer.generate_all_visualizations(df, report_stats.get('prisma'))

        # Build included papers list (limit to 50 for readability)
        included_list = []
        if 'selection_stage' in df.columns:
            included_df = df[df['selection_stage'] == 'included'].copy()
            # Data already deduplicated by pipeline - just limit display
            if not included_df.empty:
                included_df = included_df.head(50)

                for _, row in included_df.iterrows():
                    year_val = row.get('year')
                    try:
                        year_out = int(year_val) if pd.notna(year_val) else 'N/A'
                    except Exception:
                        year_out = 'N/A'

                    included_list.append({
                        'title': row.get('title') or 'Título não disponível',
                        'authors': row.get('authors') or 'N/A',
                        'year': year_out,
                        'venue': row.get('venue') or row.get('source_publication') or 'N/A',
                        'doi': row.get('doi') or '',
                        'url': _normalise_external_url(row.get('url'))
                    })

        # Create report content
        report_data = {
            'title': 'Resumo operacional da revisão sistemática',
            'subtitle': 'Ensino Personalizado de Matemática: revisão sistemática de técnicas computacionais e especificação de um protótipo de apoio à interpretação docente',
            'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'data_scope': {
                'interpretation': (
                    'Este JSON preserva contagens do export operacional e uma sobreposição de recuperação reconciliada. '
                    'Para a seleção científica histórica, consulte o registro de escopo; para a recuperação de fontes, '
                    'consulte o registro de situação atual. Os contadores operacionais não substituem esses registros.'
                ),
                'selection_source': 'research/data/current_synthesis_scope.csv',
                'retrieval_source': 'research/data/selection_status_current.json',
            },
            'statistics': report_stats,
            'charts': [
                {
                    'name': p.stem,
                    'path': p,
                    'label': _CHART_PRESENTATION.get(
                        p.stem,
                        (p.stem.replace('_', ' ').capitalize(), p.stem.replace('_', ' ')),
                    )[0],
                    'alt': _CHART_PRESENTATION.get(
                        p.stem,
                        (p.stem.replace('_', ' ').capitalize(), p.stem.replace('_', ' ')),
                    )[1],
                }
                for p in chart_paths
            ],
            'config': config or {},
            'included_list': included_list,
            'fulltext_stats': fulltext_stats  # Add fulltext statistics for template
        }

        # Generate HTML report
        html_path = self._generate_html_report(report_data)

        # Generate JSON summary
        json_path = self._generate_json_summary(report_data)

        logger.info(f"Summary report generated: {html_path}")
        return html_path

    def generate_papers_report(
        self,
        df: pd.DataFrame,
        stage: str = "included",
        fields: Optional[List[str]] = None,
        fulltext_stats: Optional[Dict] = None
    ) -> Path:
        """Generate detailed papers report.

        Args:
            df: DataFrame with papers
            stage: Selection stage to include
            fields: Fields to include in report
            fulltext_stats: Full-text extraction statistics (optional)

        Returns:
            Path to generated report
        """
        if fields is None:
            fields = [
                'title', 'authors', 'year', 'venue', 'abstract',
                'relevance_score', 'comp_techniques', 'study_type',
                'inclusion_criteria_met', 'exclusion_reason', 'doi', 'url'
            ]

        # Filter by stage (data already deduplicated by pipeline)
        if 'selection_stage' in df.columns:
            papers_df = df[df['selection_stage'] == stage].copy()
        else:
            papers_df = df.copy()

        if papers_df.empty:
            logger.warning(f"No papers found for stage: {stage}")
            return Path()

        # Sort by relevance score
        if 'relevance_score' in papers_df.columns:
            papers_df = papers_df.sort_values('relevance_score', ascending=False)

        # Generate detailed report
        report_path = self.output_dir / f"papers_report_{stage}.html"

        papers_data = []
        for _, row in papers_df.iterrows():
            paper_data = {}
            for field in fields:
                if field in row.index:
                    value = row[field]
                    if pd.isna(value):
                        value = "N/A"
                    elif field == 'url':
                        value = _normalise_external_url(value)
                    paper_data[field] = value

            # Add full_text field if present
            if 'full_text' in row.index:
                paper_data['full_text'] = row['full_text']

            # Add full-text extraction info if available
            if fulltext_stats and 'extraction_results' in fulltext_stats:
                # Find matching paper in extraction results by DOI or title
                paper_doi = row.get('doi', '')
                paper_title = row.get('title', '')

                for extracted in fulltext_stats['extraction_results']:
                    if (paper_doi and extracted.get('doi') == paper_doi) or \
                       (paper_title and extracted.get('title') == paper_title):
                        paper_data['fulltext_extracted'] = bool(extracted.get('full_text'))
                        paper_data['fulltext_size'] = len(extracted.get('full_text', '')) if extracted.get('full_text') else 0
                        paper_data['pdf_failure_reasons'] = extracted.get('pdf_failure_reasons', [])
                        # Extract keywords from full_text if available
                        if extracted.get('full_text'):
                            paper_data['fulltext_keywords'] = self._extract_keywords(extracted['full_text'])
                        break

            papers_data.append(paper_data)

        # Create HTML content
        # Keep the operational stage distinct from final scientific
        # adjudication in the public report.  The current retained population
        # includes provisional empirical candidates and one contextual record.
        html_content = self._create_papers_html(papers_data, stage)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(_normalise_html_whitespace(html_content))

        logger.info(f"Papers report generated: {report_path}")
        return report_path

    def generate_gap_analysis(
        self,
        df: pd.DataFrame
    ) -> Path:
        """Generate gap analysis report.

        Args:
            df: DataFrame with papers

        Returns:
            Path to generated report
        """
        logger.info("Generating gap analysis...")

        gaps = self._identify_research_gaps(df)

        # Create gap analysis report
        report_path = self.output_dir / "gap_analysis.html"

        html_content = self._create_gap_analysis_html(gaps, record_count=len(df))

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(_normalise_html_whitespace(html_content))

        logger.info(f"Gap analysis generated: {report_path}")
        return report_path

    def _calculate_statistics(
        self,
        df: pd.DataFrame,
        stats: Optional[Dict] = None
    ) -> Dict:
        """Calculate comprehensive statistics.

        Args:
            df: DataFrame with papers
            stats: Existing PRISMA stats

        Returns:
            Dictionary with statistics
        """
        # Normalizar PRISMA com ints nativos (começa a partir de `stats` se fornecido)
        prisma_stats = {}
        if stats:
            for k, v in stats.items():
                try:
                    prisma_stats[k] = int(v) if v is not None else 0
                except Exception:
                    prisma_stats[k] = v

        # If selection stage information is available in the DataFrame, we can
        # derive PRISMA counts from it. However, when canonical stats are
        # provided (from DB snapshot), we should NOT override them. Only fill
        # missing keys to preserve the canonical truth.
        if 'selection_stage' in df.columns:
            identification_df = int(len(df))

            # PRISMA requires identity deduplication after identification.
            # Exact normalized DOI/URL identities are removed; title-only
            # matches remain an audit candidate and are not removed here.
            if 'is_duplicate' in df.columns:
                # Filtrar identidades determinísticas; a auditoria de título é
                # reportada à parte.
                unique_df = df[~deterministic_identity_duplicate_mask(df)]
                status_series = unique_df.get('status', pd.Series([None] * len(unique_df), index=unique_df.index)).fillna('')
                screening_excluded_df = int(((unique_df['selection_stage'] == 'screening') & (status_series == 'excluded')).sum())
                eligibility_excluded_df = int(((unique_df['selection_stage'] == 'eligibility') & (status_series == 'excluded')).sum())
                included_df = int((unique_df['selection_stage'] == 'included').sum())
                screened_df = int(len(unique_df))  # Linhas sem identidade duplicada
                eligibility_df = int(unique_df['selection_stage'].isin(['eligibility', 'included']).sum())
                # Duplicatas removidas (não sobrescrever se já fornecido em stats)
                if 'duplicates_removed' not in prisma_stats:
                    duplicates_removed_df = identification_df - screened_df
                else:
                    duplicates_removed_df = int(prisma_stats.get('duplicates_removed', 0))
            else:
                # Fallback para DataFrames externos sem a coluna persistida.
                fallback_duplicate = deterministic_identity_duplicate_mask(df)
                unique_df = df[~fallback_duplicate]
                status_series = unique_df.get('status', pd.Series([None] * len(unique_df), index=unique_df.index)).fillna('')
                screening_excluded_df = int(((unique_df['selection_stage'] == 'screening') & (status_series == 'excluded')).sum())
                eligibility_excluded_df = int(((unique_df['selection_stage'] == 'eligibility') & (status_series == 'excluded')).sum())
                included_df = int((unique_df['selection_stage'] == 'included').sum())
                screened_df = int(unique_df['selection_stage'].isin(['screening', 'eligibility', 'included']).sum())
                eligibility_df = int(unique_df['selection_stage'].isin(['eligibility', 'included']).sum())
                duplicates_removed_df = int(prisma_stats.get('duplicates_removed', len(df) - len(unique_df)))

            df_prisma = {
                # Não sobrescrever identificação se fornecida (usa distinct_doi do export)
                'identification': identification_df,
                'screening': screened_df,
                'screening_excluded': screening_excluded_df,
                'eligibility': eligibility_df,
                'eligibility_excluded': eligibility_excluded_df,
                'included': included_df,
                'duplicates_removed': duplicates_removed_df,
            }

            # Only set keys that are not already present in prisma_stats
            for k, v in df_prisma.items():
                if k not in prisma_stats:
                    prisma_stats[k] = v

        # Construir bloco de integridade (auditoria)
        # Usa chaves adicionadas em export (raw_rows, distinct_doi)
        raw_rows = int(prisma_stats.get('raw_rows', len(df)))
        distinct_doi = int(prisma_stats.get('distinct_doi', raw_rows))
        duplicates_removed = int(prisma_stats.get('duplicates_removed', raw_rows - distinct_doi))
        included_count = int(prisma_stats.get('included', 0))
        deduplication_audit = prisma_stats.get('deduplication_audit')
        if not isinstance(deduplication_audit, dict):
            deduplication_audit = audit_duplicate_candidates(df)

        identification = int(prisma_stats.get('identification', raw_rows))
        eligibility = int(prisma_stats.get('eligibility', 0))
        stage_percentages = prisma_stats.get('stage_percentages')
        if not isinstance(stage_percentages, dict):
            stage_percentages = {
                'screening_excluded_of_identification': round(
                    100 * int(prisma_stats.get('screening_excluded', 0)) / identification, 2
                ) if identification else 0.0,
                'screening_advanced_of_identification': round(
                    100 * eligibility / identification, 2
                ) if identification else 0.0,
                'eligibility_excluded_of_eligibility': round(
                    100 * int(prisma_stats.get('eligibility_excluded', 0)) / eligibility, 2
                ) if eligibility else 0.0,
                'included_of_eligibility': round(
                    100 * included_count / eligibility, 2
                ) if eligibility else 0.0,
                'included_of_identification': round(
                    100 * included_count / identification, 2
                ) if identification else 0.0,
            }

        integrity_block = {
            'raw_rows': raw_rows,
            'distinct_doi': distinct_doi,
            'duplicates_removed': duplicates_removed,
            'included_without_operational_flag': included_count,
            'operationally_flagged_rows': int(
                deduplication_audit.get('operationally_flagged_rows', 0)
            ),
            'deterministic_identity_duplicate_rows': int(
                deduplication_audit.get('deterministic_identity_duplicate_rows', 0)
            ),
            'adjudicated_same_report_duplicate_rows': int(
                deduplication_audit.get('adjudicated_same_report_duplicate_rows', 0)
            ),
            'confirmed_semantic_duplicates': int(
                deduplication_audit.get('confirmed_semantic_duplicates', 0)
            ),
        }

        report_stats = {
            'total_papers': int(prisma_stats.get('identification', len(df))),
            'prisma': prisma_stats,
            'integrity': integrity_block,
            'deduplication_audit': deduplication_audit,
            'stage_percentages': stage_percentages,
        }

        # Year statistics: coerce to int, exclude out-of-range years from per-year
        # distribution (but report how many were excluded).
        if 'year' in df.columns:
            # Coerce to numeric years
            years_num = pd.to_numeric(df['year'], errors='coerce').dropna().astype(int)
            if not years_num.empty:
                ymin = int(self.config.review.year_min)
                ymax = int(self.config.review.year_max)

                in_range_mask = (years_num >= ymin) & (years_num <= ymax)
                in_range_years = years_num[in_range_mask]
                out_of_range_years = years_num[~in_range_mask]

                year_dist = in_range_years.value_counts().to_dict() if not in_range_years.empty else {}

                if in_range_years.empty:
                    report_stats['years'] = {
                        'min': None,
                        'max': None,
                        'mean': None,
                        'distribution': {},
                        'out_of_range_count': int(len(out_of_range_years))
                    }
                else:
                    report_stats['years'] = {
                        'min': int(in_range_years.min()),
                        'max': int(in_range_years.max()),
                        'mean': round(float(in_range_years.mean()), 1),
                        'distribution': {int(k): int(v) for k, v in year_dist.items()},
                        'out_of_range_count': int(len(out_of_range_years))
                    }

        # Database statistics
        if 'database' in df.columns:
            db_counts = df['database'].value_counts()
            # Converter int64 para int nativo
            report_stats['databases'] = {str(k): int(v) for k, v in db_counts.to_dict().items()}

        # Techniques statistics
        if 'comp_techniques' in df.columns:
            techniques = []
            for _, row in df.iterrows():
                if pd.notna(row['comp_techniques']):
                    techniques.extend([t.strip() for t in str(row['comp_techniques']).split(';')])

            if techniques:
                tech_counts = pd.Series(techniques).value_counts()
                # Converter int64 para int nativo
                report_stats['techniques'] = {str(k): int(v) for k, v in tech_counts.head(10).to_dict().items()}

        # Relevance scores
        if 'relevance_score' in df.columns:
            scores = df['relevance_score'].dropna()
            if not scores.empty:
                report_stats['relevance'] = {
                    'min': round(float(scores.min()), 2),
                    'max': round(float(scores.max()), 2),
                    'mean': round(float(scores.mean()), 2),
                    'median': round(scores.median(), 2),
                    'std': round(scores.std(), 2),
                    'high_relevance': len(scores[scores >= 7.0]),
                    'medium_relevance': len(scores[(scores >= 4.0) & (scores < 7.0)]),
                    'low_relevance': len(scores[scores < 4.0])
                }

        # Selection stages (PRISMA-friendly derived stats)
        if 'selection_stage' in df.columns:
            identification_df = int(len(df))
            status_series = df.get('status', pd.Series([None] * len(df), index=df.index)).fillna('')
            screening_excluded_df = int(((df['selection_stage'] == 'screening') & (status_series == 'excluded')).sum())
            eligibility_excluded_df = int(((df['selection_stage'] == 'eligibility') & (status_series == 'excluded')).sum())
            included_df = int((df['selection_stage'] == 'included').sum())

            identification = int(prisma_stats.get('identification', identification_df))
            screening_excluded = int(prisma_stats.get('screening_excluded', screening_excluded_df))
            eligibility_excluded = int(prisma_stats.get('eligibility_excluded', eligibility_excluded_df))
            included = int(prisma_stats.get('included', included_df))
            screening_remaining = int(prisma_stats.get('screening', identification - screening_excluded))
            eligibility_remaining = int(prisma_stats.get('eligibility', screening_remaining - eligibility_excluded))

            if 'reports_sought' in prisma_stats:
                retrieval = prisma_stats.get('current_source_retrieval') or {}
                report_stats['selection_stages'] = {
                    'Identificação': identification,
                    'Registros após deduplicação': screening_remaining,
                    'Excluídos na triagem inicial': screening_excluded,
                    'Registros submetidos à priorização histórica': int(prisma_stats['prioritization']),
                    'Não avançaram na priorização histórica': int(prisma_stats['prioritization_excluded']),
                    'Selecionados para leitura de resumo': int(prisma_stats['shortlisted']),
                    'Excluídos após leitura de resumo': int(prisma_stats['abstract_screening_excluded']),
                    'Relatórios buscados': int(prisma_stats['reports_sought']),
                    'Relatórios não recuperados': int(
                        retrieval.get('reports_not_retrieved', prisma_stats['reports_not_retrieved'])
                    ),
                    'Textos integrais avaliados': int(
                        retrieval.get('reports_assessed_at_full_text', eligibility)
                    ),
                    'Relatórios empíricos recuperados': int(
                        retrieval.get('recovered_empirical_reports', included)
                    ),
                    'Excluídos após texto integral': int(
                        retrieval.get('full_text_exclusions', eligibility_excluded)
                    ),
                    'Estudos da seleção histórica': included,
                }
            else:
                report_stats['selection_stages'] = {
                    'Identificação': identification,
                    'Triagem': screening_remaining,
                    'Priorização operacional': eligibility_remaining,
                    'Incluídos': included,
                    'Excluídos na Triagem': screening_excluded,
                    'Excluídos na priorização operacional': eligibility_excluded,
                }

        return report_stats

    def _extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extract top keywords from full text using simple frequency analysis.

        Args:
            text: Full text to analyze
            top_n: Number of top keywords to return

        Returns:
            List of top keywords
        """
        if not text or not isinstance(text, str):
            return []

        # Common stop words (Portuguese + English)
        stop_words = {
            'o', 'a', 'de', 'da', 'do', 'que', 'e', 'para', 'com', 'em', 'os', 'as', 'dos', 'das',
            'um', 'uma', 'por', 'no', 'na', 'nos', 'nas', 'ao', 'aos', 'à', 'às', 'pelo', 'pela',
            'the', 'is', 'are', 'was', 'were', 'of', 'in', 'to', 'and', 'or', 'for', 'with', 'on',
            'at', 'by', 'from', 'as', 'an', 'be', 'been', 'has', 'have', 'had', 'that', 'this'
        }

        # Split into words and filter
        words = text.lower().split()
        words = [w.strip('.,;:!?()[]{}"\'-') for w in words]
        words = [w for w in words if len(w) > 3 and w not in stop_words and w.isalpha()]

        # Count frequencies
        from collections import Counter
        word_counts = Counter(words)

        # Return top N
        return [word for word, _ in word_counts.most_common(top_n)]

    def _identify_research_gaps(self, df: pd.DataFrame) -> Dict:
        """Identify research gaps from the literature.

        Args:
            df: DataFrame with papers

        Returns:
            Dictionary with identified gaps
        """
        gaps = {
            'temporal_gaps': [],
            'methodological_gaps': [],
            'technical_gaps': [],
            'geographical_gaps': [
                'A distribuição geográfica não é calculada pelo gerador e não foi avaliada nesta exploração.'
            ]
        }

        # Temporal gaps
        if 'year' in df.columns:
            # Filter years to only consider those within the configured scope
            ymin = int(self.config.review.year_min)
            ymax = int(self.config.review.year_max)

            years = pd.to_numeric(df['year'], errors='coerce').dropna()
            years_in_scope = years[(years >= ymin) & (years <= ymax)]

            if not years_in_scope.empty:
                year_counts = years_in_scope.value_counts().sort_index()
                # Flag descriptive counts only; this is not an estimate of
                # research production or coverage across the literature.
                mean_count = year_counts.mean()
                mean_count_display = f"{mean_count:.1f}".replace(".", ",")
                low_years = year_counts[year_counts < mean_count * 0.5]
                gaps['temporal_gaps'] = [
                    f"{int(year)}: {_format_pt_br_integer(count)} "
                    f"{'registro' if int(count) == 1 else 'registros'} no export, abaixo da metade da média "
                    f"dos anos observados ({mean_count_display}). "
                    "O sinal depende da cobertura da busca "
                    "e não comprova baixa produção na literatura."
                    for year, count in low_years.items()
                ]

                # Identify years with no publications in scope
                all_years_in_scope = set(range(ymin, ymax + 1))
                years_with_data = set(year_counts.index.astype(int))
                missing_years = sorted(all_years_in_scope - years_with_data)

                if missing_years:
                    # Group consecutive years for better readability
                    if len(missing_years) <= 3:
                        gaps['temporal_gaps'].extend([
                            f"Nenhuma publicação encontrada em {year}"
                            for year in missing_years
                        ])
                    else:
                        gaps['temporal_gaps'].append(
                            f"Nenhuma publicação encontrada em {len(missing_years)} anos: "
                            f"{missing_years[0]}-{missing_years[-1]}"
                        )

        # Exact-label absence is reported as an export-field signal, not as an
        # absence of a technique from the studies or literature.
        if 'comp_techniques' in df.columns:
            all_techniques = set()
            for _, row in df.iterrows():
                if pd.notna(row['comp_techniques']):
                    techniques = [
                        t.strip().casefold()
                        for t in str(row['comp_techniques']).split(';')
                    ]
                    all_techniques.update(techniques)

            expected_techniques = {
                'reinforcement_learning': 'aprendizado por reforço',
                'nlp': 'processamento de linguagem natural (PLN)',
                'computer_vision': 'visão computacional',
                'blockchain': 'blockchain',
                'iot': 'Internet das Coisas',
                'augmented_reality': 'realidade aumentada',
            }

            gaps['technical_gaps'] = [
                f"O rótulo de {label} não aparece exatamente no campo comp_techniques do export. "
                "Isso não indica ausência da técnica nos estudos."
                for code, label in expected_techniques.items()
                if code not in all_techniques
            ]

        # Methodological gaps
        if 'study_type' in df.columns:
            total = len(df)
            study_types = df['study_type'].fillna('').astype(str).str.strip().str.casefold()
            missing_types = int(study_types.eq('').sum())
            experimental_count = int(study_types.eq('experimental').sum())
            longitudinal_count = int(study_types.eq('longitudinal').sum())

            if total and experimental_count / total < 0.3:
                gaps['methodological_gaps'].append(
                    f"A etiqueta operacional “experimental” aparece em {_format_pt_br_integer(experimental_count)} "
                    f"de {_format_pt_br_integer(total)} registros; a frequência fica abaixo do limite "
                    "descritivo de 30%. "
                    "Esse rótulo não avalia rigor metodológico."
                )

            if total and longitudinal_count / total < 0.1:
                if longitudinal_count == 0:
                    longitudinal_sentence = (
                        f"Nenhum dos {_format_pt_br_integer(total)} registros recebeu a etiqueta "
                        "operacional “longitudinal”."
                    )
                else:
                    longitudinal_sentence = (
                        f"A etiqueta operacional “longitudinal” aparece em "
                        f"{_format_pt_br_integer(longitudinal_count)} de {_format_pt_br_integer(total)} registros."
                    )
                gaps['methodological_gaps'].append(
                    f"{longitudinal_sentence} A frequência fica abaixo do limite descritivo de 10%. "
                    f"{_format_pt_br_integer(missing_types)} registros não têm tipo preenchido; por isso, o sinal não demonstra "
                    "ausência de estudos longitudinais."
                )

        return gaps

    def _generate_html_report(self, report_data: Dict) -> Path:
        """Generate HTML report from data.

        Args:
            report_data: Report data

        Returns:
            Path to HTML file
        """
        statistics = report_data.setdefault("statistics", {})
        statistics.setdefault(
            "integrity",
            {
                "deterministic_identity_duplicate_rows": 0,
                "adjudicated_same_report_duplicate_rows": 0,
            },
        )

        html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="icon" type="image/svg+xml" href="../../../public-site/assets/site-favicon.svg">
    <link rel="stylesheet" href="../../../public-site/assets/site.css">
</head>
<body class="generated-report">
    {{ site_header | safe }}
    <main class="generated-report-main">
    <div class="site-shell">
    <p class="breadcrumb"><a href="../../../">Visão geral</a> / <a href="../../index.html">Revisão sistemática</a> / <strong>Resumo operacional</strong></p>
    {{ report_tabs | safe }}
    <section class="page-hero" aria-labelledby="page-title">
        <span class="eyebrow">Exportação operacional · snapshot da revisão</span>
        <h1 id="page-title">{{ title }}</h1>
        <h2>{{ subtitle }}</h2>
        <p class="report-generated">Snapshot do export operacional: {{ generated_at }}</p>
    </section>
    <aside class="report-notice" role="note">
        <p><strong>Escopo desta página:</strong> este relatório descreve um export operacional e a seleção histórica. Para a apreciação MMAT por critério, consulte o <a href="../analysis/mmat_current.html">registro atual do MMAT</a>; para a síntese acadêmica, consulte o <a href="../../../results/tcc/index.html">TCC</a>.</p>
        <p>{{ data_scope.interpretation if data_scope is defined else 'As contagens operacionais não substituem os registros versionados de escopo e recuperação.' }} Consulte também o <a href="../../data/current_synthesis_scope.csv">registro de escopo</a> e o <a href="../../data/selection_status_current.json">registro de recuperação</a>.</p>
    </aside>

    <div class="section">
        <h2>Estatísticas do export</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <h3>Registros identificados</h3>
                <h2>{{ statistics.total_papers }}</h2>
            </div>

            {% if statistics.prisma %}
            <div class="stat-card">
                <h3>Identificados</h3>
                <h2>{{ statistics.prisma.identification or 0 }}</h2>
            </div>
            <div class="stat-card">
                <h3>Registros retidos</h3>
                <h2>{{ statistics.prisma.included or 0 }}</h2>
            </div>
            {% endif %}

            {% if statistics.relevance %}
            <div class="stat-card">
                <h3>Score médio operacional</h3>
                <h2>{{ statistics.relevance.mean }}</h2>
                <p class="report-muted">Sobre os registros após a remoção determinística; não é qualidade metodológica.</p>
            </div>
            {% endif %}
        </div>
    </div>

    {% if statistics.stage_percentages %}
    <div class="section">
        <h2>Percentuais das etapas operacionais</h2>
        <table>
            <tr><th>Relação</th><th>Percentual</th></tr>
            {% if statistics.prisma.reports_sought is defined %}
            <tr><td>Excluídos na triagem inicial / registros após deduplicação</td><td>{{ statistics.stage_percentages.screening_excluded_of_screened_records }}%</td></tr>
            <tr><td>Submetidos à priorização histórica / registros após deduplicação</td><td>{{ statistics.stage_percentages.prioritization_passed_of_screened_records }}%</td></tr>
            <tr><td>Não avançaram na priorização histórica / registros priorizados</td><td>{{ statistics.stage_percentages.prioritization_excluded_of_prioritization }}%</td></tr>
            <tr><td>Excluídos após resumo / shortlist</td><td>{{ statistics.stage_percentages.abstract_screening_excluded_of_shortlist }}%</td></tr>
            <tr><td>Relatórios não recuperados / relatórios buscados</td><td>{{ statistics.prisma.current_source_retrieval.stage_percentages.reports_not_retrieved_of_reports_sought if statistics.prisma.current_source_retrieval is defined else statistics.stage_percentages.reports_not_retrieved_of_reports_sought }}%</td></tr>
            <tr><td>Excluídos após texto integral / textos avaliados</td><td>{{ statistics.prisma.current_source_retrieval.stage_percentages.full_text_exclusions_of_assessed if statistics.prisma.current_source_retrieval is defined else statistics.stage_percentages.full_text_excluded_of_assessed }}%</td></tr>
            <tr><td>Relatórios empíricos recuperados / textos avaliados</td><td>{{ statistics.prisma.current_source_retrieval.stage_percentages.recovered_empirical_reports_of_assessed if statistics.prisma.current_source_retrieval is defined else statistics.stage_percentages.included_of_assessed }}%</td></tr>
            {% else %}
            <tr><td>Excluídos na triagem / identificação</td><td>{{ statistics.stage_percentages.screening_excluded_of_identification }}%</td></tr>
            <tr><td>Avançaram da triagem / identificação</td><td>{{ statistics.stage_percentages.screening_advanced_of_identification }}%</td></tr>
            <tr><td>Excluídos na priorização operacional / submetidos à priorização</td><td>{{ statistics.stage_percentages.eligibility_excluded_of_eligibility }}%</td></tr>
            <tr><td>Retidos operacionalmente / submetidos à priorização</td><td>{{ statistics.stage_percentages.included_of_eligibility }}%</td></tr>
            {% endif %}
            <tr><td>Incluídos / identificação</td><td>{{ statistics.stage_percentages.included_of_identification }}%</td></tr>
        </table>
        <p>A seleção por corte 4,0 permanece histórica e inalterada. A priorização por metadados e resumos não equivale à elegibilidade em texto completo. O fluxo de recuperação atual registra {{ statistics.prisma.current_source_retrieval.reports_not_retrieved if statistics.prisma.current_source_retrieval is defined else statistics.prisma.reports_not_retrieved }} relatório(s) não recuperado(s), {{ statistics.prisma.current_source_retrieval.reports_assessed_at_full_text if statistics.prisma.current_source_retrieval is defined else statistics.prisma.eligibility }} avaliado(s) e {{ statistics.prisma.current_source_retrieval.recovered_empirical_reports if statistics.prisma.current_source_retrieval is defined else statistics.prisma.included }} relatório(s) empírico(s) recuperado(s). Sokkhey permanece apenas como inclusão histórica sem cópia verificável; relatórios não recuperados não são exclusões após leitura integral.</p>
    </div>
    {% endif %}

    {% if statistics.deduplication_audit %}
    <div class="section">
        <h2>Auditoria de identidade bibliográfica</h2>
        <p>DOI/URL exatos são deduplicados como identidade de registro no fluxo PRISMA. A linha de título bruto inclui sobreposição com essas identidades; a linha de título-only mostra os candidatos restantes depois da remoção determinística. Nenhum título é removido automaticamente por igualdade textual.</p>
        <table>
            <tr><th>Indicador</th><th>Grupos</th><th>Linhas repetidas</th><th>Excedentes</th></tr>
            <tr><td>DOI normalizado</td><td>{{ statistics.deduplication_audit.doi.repeated_groups }}</td><td>{{ statistics.deduplication_audit.doi.repeated_rows }}</td><td>{{ statistics.deduplication_audit.doi.excess_rows }}</td></tr>
            <tr><td>URL exata</td><td>{{ statistics.deduplication_audit.url.repeated_groups }}</td><td>{{ statistics.deduplication_audit.url.repeated_rows }}</td><td>{{ statistics.deduplication_audit.url.excess_rows }}</td></tr>
            <tr><td>Título normalizado</td><td>{{ statistics.deduplication_audit.title.repeated_groups }}</td><td>{{ statistics.deduplication_audit.title.repeated_rows }}</td><td>{{ statistics.deduplication_audit.title.excess_rows }}</td></tr>
            {% if statistics.deduplication_audit.title_only is defined %}
            <tr><td>Título-only após DOI/URL</td><td>{{ statistics.deduplication_audit.title_only.repeated_groups }}</td><td>{{ statistics.deduplication_audit.title_only.repeated_rows }}</td><td>{{ statistics.deduplication_audit.title_only.excess_rows }}</td></tr>
            {% endif %}
        </table>
        <p><strong>Registros removidos por identidade DOI/URL:</strong> {{ statistics.deduplication_audit.deterministic_identity_duplicate_rows }}. <strong>Relatórios repetidos confirmados em revisão manual:</strong> {{ statistics.deduplication_audit.adjudicated_same_report_duplicate_rows }}. <strong>Flags persistidas no snapshot:</strong> {{ statistics.deduplication_audit.operationally_flagged_rows }}. <strong>Duplicatas semanticamente confirmadas por título:</strong> {{ statistics.deduplication_audit.confirmed_semantic_duplicates }}.</p>
    </div>
    {% endif %}

        <aside class="report-notice report-history" role="note">
        <h2>Contexto histórico da deduplicação</h2>
        <p>A execução histórica documentava 9.431 registros, 2.517 duplicatas removidas,
        6.914 registros únicos e 17 incluídos. O único log histórico preservado no
        banco informa <code>total_removed=2494</code>; a execução que resolveria essa
        divergência não está arquivada. Esses valores são mantidos como contexto
        histórico e não são usados para calcular o fluxo atual: 11.904 registros
        brutos, {{ statistics.integrity.deterministic_identity_duplicate_rows }} remoções por identidade DOI/URL e
        {{ statistics.integrity.adjudicated_same_report_duplicate_rows }} relatórios repetidos confirmados manualmente
        ({{ statistics.prisma.duplicates_removed or 0 }} no total), seguidos por
        {{ statistics.prisma.screening or 0 }} registros na triagem. O corte de priorização 4,0 e a
        seleção histórica de 15 estudos permanecem inalterados.</p>
    </aside>

    {% if fulltext_stats %}
    <div class="section">
        <h2>Extração automática de texto</h2>
        <p class="report-muted">A extração automática não comprova recuperação documentada nem leitura do texto para avaliar elegibilidade.</p>
        <div class="stat-grid">
            <div class="stat-card">
                <h3>Cobertura</h3>
                <h2>
                    {{ "%.1f"|format(fulltext_stats.coverage_pct) }}%
                </h2>
                <p class="report-muted">{{ fulltext_stats.extracted }}/{{ fulltext_stats.total_papers }} registros</p>
            </div>
            <div class="stat-card">
                <h3>Extraídos</h3>
                <h2>{{ fulltext_stats.extracted }}</h2>
            </div>
            <div class="stat-card">
                <h3>Falhas</h3>
                <h2>{{ fulltext_stats.failed }}</h2>
            </div>
        </div>
        {% if fulltext_stats.top_failures %}
        <h3>Principais causas de falha</h3>
        <table class="report-compact-table">
            <tr><th>Causa</th><th>Ocorrências</th></tr>
            {% for reason, count in fulltext_stats.top_failures %}
            <tr>
                <td>{{ reason.replace('_', ' ').title() }}</td>
                <td>{{ count }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
    </div>
    {% endif %}

    {% if charts %}
    <div class="section">
        <h2>Visualizações</h2>
        <div class="chart-grid">
            {% for chart in charts %}
            <div class="chart-card">
                <h3>{{ chart.label }}</h3>
                <img src="../visualizations/{{ chart.path.name }}" alt="{{ chart.alt }}">
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if included_list %}
    <div class="section">
        <h2>Registros do estágio operacional ({{ included_list|length }})</h2>
        <p>Esta lista representa os registros com etapa operacional <code>included</code> no export. A população inclui candidatos empíricos provisórios e um protocolo contextual; consulte a seleção histórica e o registro MMAT para a interpretação científica.</p>
        {% for p in included_list %}
        <div class="paper-item">
            <div class="paper-title">{{ p.title }}</div>
            <div class="paper-meta">
                <strong>Autores:</strong> {{ p.authors }} | <strong>Ano:</strong> {{ p.year }} | <strong>Venue:</strong> {{ p.venue }}
                {% if p.doi %}| <strong>DOI:</strong> {{ p.doi }}{% endif %}
                {% if p.url %}| <a href="{{ p.url }}" target="_blank" rel="noopener noreferrer">Link</a>{% endif %}
            </div>
        </div>
        {% endfor %}
        <p><em>Lista limitada aos 50 primeiros. Consulte o relatório de registros retidos para a lista completa.</em></p>
    </div>
    {% endif %}

    {% if statistics.techniques %}
    <div class="section">
        <h2>💻 Técnicas Computacionais no snapshot</h2>
        <p>Frequências calculadas sobre os registros após a remoção determinística (n={{ statistics.prisma.screening or 0 }}); as categorias podem se sobrepor e não representam apenas os registros retidos nem qualidade ou eficácia.</p>
        <table>
            <tr><th>Técnica</th><th>Frequência</th></tr>
            {% for technique, count in statistics.techniques.items() %}
            <tr><td>{{ technique.replace('_', ' ').title() }}</td><td>{{ count }}</td></tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}

    <div class="section">
        <h2>Informações do processo</h2>
        <div class="highlight">
            <p><strong>Snapshot do export:</strong> {{ generated_at }}</p>
            <p><strong>Relato:</strong> PRISMA 2020 foi usado como diretriz; consulte o checklist para itens e desvios documentados.</p>
            <p><strong>Filtro operacional:</strong> escore de relevância multicritério sobre metadados e resumos; não equivale à avaliação de elegibilidade de relatórios em texto completo nem substitui a adjudicação científica da população retida.</p>
        </div>
    </div>
    </div>
    </main>
    {{ footer_html | safe }}
</body>
</html>
        """

        template = self.env.from_string(html_template)
        html_content = template.render(
            **report_data,
            site_header=self._site_header_html(),
            report_tabs=self._report_tabs_html("summary"),
            footer_html=self._footer_html(),
        )

        report_path = self.output_dir / "summary_report.html"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(_normalise_html_whitespace(html_content))

        return report_path

    def _generate_json_summary(self, report_data: Dict) -> Path:
        """Generate JSON summary of the report.

        Args:
            report_data: Report data

        Returns:
            Path to JSON file
        """
        # Remove non-serializable data
        json_data = {k: v for k, v in report_data.items() if k != 'charts'}

        # Save JSON with timestamp inside content, not filename
        json_path = self.output_dir / "summary.json"

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # The HTML report is generated by ``_generate_html_report`` before
        # this JSON export. Do not overwrite it with the legacy compact
        # renderer: doing so silently discarded the PRISMA percentages and
        # the duplicate-candidate audit from the published report.
        return json_path

    def _create_papers_html(self, papers_data: List[Dict], stage: str) -> str:
        """Create HTML content for papers report.

        Args:
            papers_data: List of paper dictionaries
            stage: Selection stage

        Returns:
            HTML content
        """
        html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ stage_label }} · CCW</title>
    <link rel="icon" type="image/svg+xml" href="../../../public-site/assets/site-favicon.svg">
    <link rel="stylesheet" href="../../../public-site/assets/site.css">
</head>
<body class="generated-report">
    {{ site_header | safe }}
    <main class="generated-report-main">
    <div class="site-shell">
    <p class="breadcrumb"><a href="../../../">Visão geral</a> / <a href="../../index.html">Revisão sistemática</a> / <strong>Registros operacionais</strong></p>
    {{ report_tabs | safe }}
    <section class="page-hero" aria-labelledby="page-title">
        <span class="eyebrow">Exportação operacional · {{ papers_data|length }} registros</span>
        <h1 id="page-title">{{ stage_label }}</h1>
        <p class="lede">Registros selecionados pelo campo de etapa do processamento automatizado.</p>
    </section>
    <aside class="report-notice" role="note">
        <p><strong>Como interpretar:</strong> a etapa operacional <code>included</code> não equivale à seleção científica do TCC nem à apreciação MMAT. A lista pode incluir candidatos provisórios e registros contextuais; o escore é de priorização e não mede qualidade metodológica ou eficácia.</p>
        <p>Consulte o <a href="../analysis/mmat_current.html">registro MMAT</a> e o <a href="../../../results/tcc/index.html">TCC</a> para o estado e a interpretação acadêmica.</p>
        <p class="source-note">Fonte: <a href="../analysis/papers.csv">export versionado de registros</a>. A extração automática de texto mostrada em cada registro não comprova recuperação nem avaliação integral no TCC.</p>
    </aside>
    {% if stage == 'included' %}
    <h2>Registros desta etapa operacional</h2>
    {% endif %}

    {% for paper in papers_data %}
    <div class="paper">
        {% if paper.relevance_score %}
        <div class="score">Score operacional: {{ paper.relevance_score }}</div>
        {% endif %}

        <div class="paper-title">{{ paper.title or 'Título não disponível' }}</div>

        <div class="paper-meta">
            <strong>Autores:</strong> {{ paper.authors or 'N/A' }}<br>
            <strong>Ano:</strong> {{ paper.year or 'N/A' }}<br>
            <strong>Venue:</strong> {{ paper.venue or 'N/A' }}<br>
            {% if paper.doi %}
            <strong>DOI:</strong> <a href="https://doi.org/{{ paper.doi }}" target="_blank" rel="noopener">{{ paper.doi }}</a><br>
            {% endif %}
            {% if paper.url %}
            <strong>URL:</strong> <a href="{{ paper.url }}" target="_blank" rel="noopener noreferrer">{{ paper.url[:60] }}{{ '...' if paper.url|length > 60 else '' }}</a>
            {% endif %}
        </div>

        {% if paper.abstract %}
        <div class="paper-abstract">
            <strong>Resumo:</strong> {{ paper.abstract }}
        </div>
        {% endif %}

        {% if paper.inclusion_criteria_met %}
        <div class="paper-criteria">
            <strong>Sinais operacionais registrados:</strong> {{ paper.inclusion_criteria_met }}
        </div>
        {% endif %}

        {% if paper.comp_techniques %}
        <div class="paper-techniques">
            <strong>Técnicas Computacionais:</strong> {{ paper.comp_techniques }}
        </div>
        {% endif %}

        {% if paper.study_type %}
        <div class="paper-meta">
            <strong>Tipo de Estudo:</strong> {{ paper.study_type }}
        </div>
        {% endif %}

        {% if paper.get('fulltext_extracted') is not none %}
        <div class="paper-fulltext">
            <strong>Extração automática de texto:</strong>
            {% if paper.fulltext_extracted %}
                <span class="tag tag-green">Extraído</span>
                {% if paper.fulltext_size %}
                <br><strong>Tamanho:</strong> {{ "%.1f"|format(paper.fulltext_size / 1024) }} KB
                {% endif %}
                {% if paper.fulltext_keywords %}
                <br><strong>Palavras-chave detectadas:</strong> {{ paper.fulltext_keywords | join(', ') }}
                {% endif %}
            {% else %}
                <span class="tag tag-red">Não extraído</span>
                {% if paper.pdf_failure_reasons %}
                <br><strong>Motivo:</strong> {{ paper.pdf_failure_reasons | join(', ') | replace('_', ' ') | title }}
                {% endif %}
            {% endif %}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    </div>
    </main>
    {{ footer_html | safe }}
</body>
</html>
        """

        template = self.env.from_string(html_template)
        stage_label = "Registros retidos no export operacional" if stage == "included" else f"Registros — {stage.title()}"
        return template.render(
            papers_data=papers_data,
            stage=stage,
            stage_label=stage_label,
            site_header=self._site_header_html(),
            report_tabs=self._report_tabs_html("papers"),
            footer_html=self._footer_html(),
        )

    def _create_gap_analysis_html(self, gaps: Dict, record_count: int) -> str:
        """Create HTML content for gap analysis.

        Args:
            gaps: Dictionary with identified gaps

        Returns:
            HTML content
        """
        html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exploração automatizada do export operacional · CCW</title>
    <link rel="icon" type="image/svg+xml" href="../../../public-site/assets/site-favicon.svg">
    <link rel="stylesheet" href="../../../public-site/assets/site.css">
</head>
<body class="generated-report">
    {{ site_header | safe }}
    <main class="generated-report-main">
    <div class="site-shell">
    <p class="breadcrumb"><a href="../../../">Visão geral</a> / <a href="../../index.html">Revisão sistemática</a> / <strong>Exploração automatizada</strong></p>
    {{ report_tabs | safe }}
    <section class="page-hero" aria-labelledby="page-title">
        <span class="eyebrow">Exploração automatizada · export operacional</span>
        <h1 id="page-title">Sinais descritivos dos registros exportados</h1>
        <p class="lede">Esta página não é uma síntese das lacunas da literatura. Ela mostra resultados de regras simples aplicadas a campos operacionais do export.</p>
    </section>
    <aside class="report-notice" role="note">
        <p><strong>Limite de interpretação:</strong> os sinais dependem da cobertura da busca e do preenchimento das etiquetas. Eles não confirmam ausência de temas na literatura, não avaliam qualidade metodológica e não integram as conclusões do TCC.</p>
        <p>O export versionado contém {{ record_count }} registros. Para a síntese acadêmica, consulte o <a href="../../../results/tcc/index.html">TCC</a> e o <a href="../analysis/mmat_current.html">registro MMAT</a>.</p>
        <p class="source-note">A regra destaca anos com contagem inferior à metade da média dos anos observados entre {{ year_min }} e {{ year_max }}; classifica etiquetas de tipo abaixo de 30% (experimental) ou 10% (longitudinal), usando todas as linhas como denominador; e procura termos técnicos predefinidos no campo <code>comp_techniques</code>. Campos vazios e variações de rótulo limitam esses sinais. A dimensão geográfica não é calculada.</p>
    </aside>

    {% for gap_type, gap_list in gaps.items() %}
    <div class="gap-section">
        <h2>{{ gap_titles[gap_type] }}</h2>
        {% if gap_list %}
        <ul>
            {% for gap in gap_list %}
            <li>{{ gap }}</li>
            {% endfor %}
        </ul>
        {% else %}
        <p class="no-gaps">Nenhum sinal foi produzido para esta categoria pelos campos disponíveis.</p>
        {% endif %}
    </div>
    {% endfor %}
    </div>
    </main>
    {{ footer_html | safe }}
</body>
</html>
        """

        template = self.env.from_string(html_template)
        return template.render(
            gaps=gaps,
            gap_titles={
                "temporal_gaps": "Distribuição temporal no export",
                "methodological_gaps": "Etiquetas de tipo de estudo",
                "technical_gaps": "Rótulos de técnicas computacionais",
                "geographical_gaps": "Distribuição geográfica",
            },
            record_count=_format_pt_br_integer(record_count),
            year_min=self.config.review.year_min,
            year_max=self.config.review.year_max,
            site_header=self._site_header_html(),
            report_tabs=self._report_tabs_html("gaps"),
            footer_html=self._footer_html(),
        )
