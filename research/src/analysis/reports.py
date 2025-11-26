"""Módulo para geração de relatórios da revisão sistemática."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from .visualizations import ReviewVisualizer
from ..config import load_config
from ..database.manager import DatabaseManager

logger = logging.getLogger(__name__)

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
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def _footer_html(self) -> str:
        """Footer HTML consistent with research/index.html.

        Returns:
            HTML string to be injected at the end of pages.
        """
        return (
            '<div class="footer" style="text-align:center;color:white;margin-top:40px;opacity:0.9;padding:20px;'
            'background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);">\n'
            '    <p><strong>Conclusion Course Work (CCW)</strong></p>\n'
            '    <p>Trabalho de Conclusão de Curso - Ciência da Computação</p>\n'
            '    <p>Instituto Federal Catarinense - Campus Videira</p>\n'
            '    <p>© 2025 Thales Ferreira | <a href="https://github.com/thalesfb/ccw" style="color:#fff;text-decoration:underline;">GitHub</a></p>\n'
            '</div>'
        )
    
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
                        'url': row.get('url') or ''
                    })
        
        # Create report content
        report_data = {
            'title': 'Relatório da Revisão Sistemática',
            'subtitle': 'Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais',
            'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'statistics': report_stats,
            'charts': [{'name': p.stem, 'path': p} for p in chart_paths],
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
        html_content = self._create_papers_html(papers_data, stage)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
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
        
        html_content = self._create_gap_analysis_html(gaps)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
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
            
            # PRISMA requer contar apenas registros ÚNICOS após Identificação
            # Identificação: total com duplicatas
            # Triagem em diante: apenas únicos (is_duplicate = 0)
            if 'is_duplicate' in df.columns:
                # Filtrar apenas únicos para os estágios pós-identificação
                unique_df = df[df['is_duplicate'] == 0]
                status_series = unique_df.get('status', pd.Series([None] * len(unique_df), index=unique_df.index)).fillna('')
                screening_excluded_df = int(((unique_df['selection_stage'] == 'screening') & (status_series == 'excluded')).sum())
                eligibility_excluded_df = int(((unique_df['selection_stage'] == 'eligibility') & (status_series == 'excluded')).sum())
                included_df = int((unique_df['selection_stage'] == 'included').sum())
                screened_df = int(len(unique_df))  # Total de únicos
                eligibility_df = int(unique_df['selection_stage'].isin(['eligibility', 'included']).sum())
                # Duplicatas removidas (não sobrescrever se já fornecido em stats)
                if 'duplicates_removed' not in prisma_stats:
                    try:
                        duplicates_removed_df = int(df['is_duplicate'].astype(bool).sum())
                    except Exception:
                        duplicates_removed_df = identification_df - screened_df
                else:
                    duplicates_removed_df = int(prisma_stats.get('duplicates_removed', 0))
            else:
                # Fallback se não tiver is_duplicate
                status_series = df.get('status', pd.Series([None] * len(df), index=df.index)).fillna('')
                screening_excluded_df = int(((df['selection_stage'] == 'screening') & (status_series == 'excluded')).sum())
                eligibility_excluded_df = int(((df['selection_stage'] == 'eligibility') & (status_series == 'excluded')).sum())
                included_df = int((df['selection_stage'] == 'included').sum())
                screened_df = int(df['selection_stage'].isin(['screening', 'eligibility', 'included']).sum())
                eligibility_df = int(df['selection_stage'].isin(['eligibility', 'included']).sum())
                # Sem coluna de duplicatas -> se já vier de stats mantém
                duplicates_removed_df = int(prisma_stats.get('duplicates_removed', 0))

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
        included_unique = int(prisma_stats.get('included', 0))

        integrity_block = {
            'raw_rows': raw_rows,
            'distinct_doi': distinct_doi,
            'duplicates_removed': duplicates_removed,
            'included_unique': included_unique,
        }

        report_stats = {
            'total_papers': int(prisma_stats.get('identification', len(df))),
            'prisma': prisma_stats,
            'integrity': integrity_block,
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

            report_stats['selection_stages'] = {
                'Identificação': identification,
                'Triagem': screening_remaining,
                'Elegibilidade': eligibility_remaining,
                'Incluídos': included,
                'Excluídos na Triagem': screening_excluded,
                'Excluídos na Elegibilidade': eligibility_excluded,
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
            'geographical_gaps': []
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
                # Find years with low publication counts
                mean_count = year_counts.mean()
                low_years = year_counts[year_counts < mean_count * 0.5]
                gaps['temporal_gaps'] = [
                    f"Baixo número de publicações em {int(year)} ({int(count)} artigos)"
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
        
        # Technical gaps
        if 'comp_techniques' in df.columns:
            all_techniques = set()
            for _, row in df.iterrows():
                if pd.notna(row['comp_techniques']):
                    techniques = [t.strip() for t in str(row['comp_techniques']).split(';')]
                    all_techniques.update(techniques)
            
            # Expected techniques that might be missing
            expected_techniques = {
                'reinforcement_learning', 'nlp', 'computer_vision',
                'blockchain', 'IoT', 'augmented_reality'
            }
            
            missing = expected_techniques - all_techniques
            gaps['technical_gaps'] = [
                f"Pouca representação de {tech.replace('_', ' ').title()}"
                for tech in missing
            ]
        
        # Methodological gaps
        if 'study_type' in df.columns:
            study_types = df['study_type'].value_counts()
            total = len(df)
            
            if study_types.get('experimental', 0) / total < 0.3:
                gaps['methodological_gaps'].append("Poucos estudos experimentais rigorosos")
            
            if study_types.get('longitudinal', 0) / total < 0.1:
                gaps['methodological_gaps'].append("Falta de estudos longitudinais")
        
        return gaps
    
    def _generate_html_report(self, report_data: Dict) -> Path:
        """Generate HTML report from data.
        
        Args:
            report_data: Report data
            
        Returns:
            Path to HTML file
        """
        html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; line-height: 1.6; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .navbar-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .navbar-title { color: white; font-size: 1.2rem; font-weight: 600; }
        .navbar-links { display: flex; gap: 1.5rem; }
        .navbar-links a { color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; transition: background 0.2s; }
        .navbar-links a:hover { background: rgba(255,255,255,0.2); }
        .navbar-links a.active { background: rgba(255,255,255,0.3); }
        .content { margin: 40px; }
        .header { text-align: center; margin-bottom: 40px; }
        .section { margin: 30px 0; padding: 20px; border-left: 4px solid #4CAF50; background: #f9f9f9; }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .chart-grid { display: grid; grid-template-columns: 1fr; gap: 24px; }
        .chart-card { text-align: center; background: white; padding: 16px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .chart-card img { width: 100%; max-width: 1200px; height: auto; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; font-weight: bold; }
        .highlight { background-color: #fff3cd; padding: 10px; border-radius: 4px; }
        .paper-item { background: white; padding: 14px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 10px; }
        .paper-title { font-weight: 600; color: #2c3e50; }
        .paper-meta { color: #7f8c8d; font-size: 0.95em; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-content">
            <div class="navbar-title">📚 Revisão Sistemática</div>
            <div class="navbar-links">
                <a href="summary_report.html" class="active">🔍 Sumário</a>
                <a href="papers_report_included.html">📄 Artigos</a>
                <a href="gap_analysis.html">📊 Análise de Lacunas</a>
            </div>
        </div>
    </nav>
    
    <div class="content">
    <div class="header">
        <h1>{{ title }}</h1>
        <h2>{{ subtitle }}</h2>
        <p><em>Gerado em: {{ generated_at }}</em></p>
    </div>

    <div class="section">
        <h2>📊 Estatísticas Gerais</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <h3>Total de Artigos</h3>
                <h2 style="color: #4CAF50;">{{ statistics.total_papers }}</h2>
            </div>
            
            {% if statistics.prisma %}
            <div class="stat-card">
                <h3>Identificados</h3>
                <h2 style="color: #2196F3;">{{ statistics.prisma.identification or 0 }}</h2>
            </div>
            <div class="stat-card">
                <h3>Incluídos</h3>
                <h2 style="color: #FF9800;">{{ statistics.prisma.included or 0 }}</h2>
            </div>
            {% endif %}
            
            {% if statistics.relevance %}
            <div class="stat-card">
                <h3>Score Médio</h3>
                <h2 style="color: #9C27B0;">{{ statistics.relevance.mean }}</h2>
            </div>
            {% endif %}
        </div>
    </div>

    {% if fulltext_stats %}
    <div class="section">
        <h2>📄 Extração de Texto Completo</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <h3>Cobertura</h3>
                <h2 style="color: {% if fulltext_stats.coverage_pct >= 70 %}#4CAF50{% elif fulltext_stats.coverage_pct >= 40 %}#FF9800{% else %}#f44336{% endif %};">
                    {{ "%.1f"|format(fulltext_stats.coverage_pct) }}%
                </h2>
                <p style="color: #7f8c8d; font-size: 0.9em;">{{ fulltext_stats.extracted }}/{{ fulltext_stats.total_papers }} artigos</p>
            </div>
            <div class="stat-card">
                <h3>Extraídos</h3>
                <h2 style="color: #4CAF50;">{{ fulltext_stats.extracted }}</h2>
            </div>
            <div class="stat-card">
                <h3>Falhas</h3>
                <h2 style="color: #f44336;">{{ fulltext_stats.failed }}</h2>
            </div>
        </div>
        {% if fulltext_stats.top_failures %}
        <h3 style="margin-top: 20px;">Top Causas de Falha:</h3>
        <table style="max-width: 600px;">
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
        <h2>📈 Visualizações</h2>
        <div class="chart-grid">
            {% for chart in charts %}
            <div class="chart-card">
                <h3>{{ chart.name
                    .replace('_', ' ')
                    .replace('prisma', 'Fluxo PRISMA')
                    .replace('selection', 'Funil de Seleção')
                    .replace('funnel', '')
                    .replace('papers by year', 'Artigos por Ano')
                    .replace('techniques distribution', 'Distribuição de Técnicas')
                    .replace('database coverage', 'Cobertura por Base de Dados')
                    .replace('relevance distribution', 'Distribuição de Relevância')
                    .title() }}</h3>
                <img src="visualizations/{{ chart.path.name }}" alt="{{ chart.name }}">
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if included_list %}
    <div class="section">
        <h2>✅ Artigos Incluídos (Top {{ included_list|length }})</h2>
        {% for p in included_list %}
        <div class="paper-item">
            <div class="paper-title">{{ p.title }}</div>
            <div class="paper-meta">
                <strong>Autores:</strong> {{ p.authors }} | <strong>Ano:</strong> {{ p.year }} | <strong>Venue:</strong> {{ p.venue }}
                {% if p.doi %}| <strong>DOI:</strong> {{ p.doi }}{% endif %}
                {% if p.url %}| <a href="{{ p.url }}" target="_blank">Link</a>{% endif %}
            </div>
        </div>
        {% endfor %}
        <p><em>Lista limitada aos 50 primeiros. Consulte o relatório de artigos para a lista completa.</em></p>
    </div>
    {% endif %}

    {% if statistics.techniques %}
    <div class="section">
        <h2>💻 Técnicas Computacionais</h2>
        <table>
            <tr><th>Técnica</th><th>Frequência</th></tr>
            {% for technique, count in statistics.techniques.items() %}
            <tr><td>{{ technique.replace('_', ' ').title() }}</td><td>{{ count }}</td></tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}

    <div class="section">
        <h2>ℹ️ Informações do Processo</h2>
        <div class="highlight">
            <p><strong>Data de Geração:</strong> {{ generated_at }}</p>
            <p><strong>Critérios de Seleção:</strong> Aplicados conforme protocolo PRISMA</p>
            <p><strong>Scoring:</strong> Baseado em relevância multi-critério</p>
        </div>
    </div>
    </div>
</body>
</html>
        """
        
        template = self.env.from_string(html_template)
        html_content = template.render(**report_data)
        
        report_path = self.output_dir / "summary_report.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
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
        
        # Also save HTML report
        html_path = self.output_dir / "summary_report.html"
        html_content = self._create_summary_html(report_data)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Summary report generated: {html_path}")
        return html_path
    
    def _create_summary_html(self, report_data: Dict) -> str:
        """Create HTML content for summary report.
        
        Args:
            report_data: Dictionary with report data
            
        Returns:
            HTML content
        """
        stats = report_data.get('statistics', {})
        prisma = stats.get('prisma', {})
        
        html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; line-height: 1.6; background: #f5f5f5; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .navbar-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .navbar-title { color: white; font-size: 1.5rem; font-weight: 600; }
        .navbar-links { display: flex; gap: 1.5rem; }
        .navbar-links a { color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; transition: background 0.2s; }
        .navbar-links a:hover { background: rgba(255,255,255,0.2); }
        .navbar-links a.active { background: rgba(255,255,255,0.3); }
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; }
        .hero h1 { font-size: 2.5rem; margin: 0 0 1rem 0; }
        .hero p { font-size: 1.2rem; opacity: 0.9; }
        .content { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        .card { background: white; border-radius: 8px; padding: 30px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-card h3 { font-size: 2.5rem; margin: 0; }
        .stat-card p { margin: 10px 0 0 0; opacity: 0.9; }
        .chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; margin-top: 20px; }
        .chart-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .chart-card img { width: 100%; height: auto; border-radius: 4px; }
        .chart-card h3 { margin-top: 0; color: #333; }
        h2 { color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }
        .footer { text-align: center; padding: 20px; margin-top: 40px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-content">
            <a href="../../../index.html" class="navbar-title" style="text-decoration:none;">Revisão Sistemática - CCW</a>
            <div class="navbar-links">
                <a href="summary_report.html" class="active">📈 Resumo</a>
                <a href="papers_report_included.html">📄 Artigos Incluídos</a>
                <a href="gap_analysis.html">🔍 Análise de Lacunas</a>
            </div>
        </div>
    </nav>
    
    <div class="hero">
        <h1>{{ title }}</h1>
        <p>{{ subtitle }}</p>
        <p style="font-size: 0.9rem; margin-top: 20px;">Gerado em: {{ generated_at }}</p>
    </div>
    
    <div class="content">
        <div class="card">
            <h2>📊 Estatísticas Gerais</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>{{ stats.total_papers }}</h3>
                    <p>Total de Papers</p>
                </div>
                <div class="stat-card">
                    <h3>{{ prisma.included }}</h3>
                    <p>Papers Incluídos</p>
                </div>
                <div class="stat-card">
                    <h3>{{ stats.years.min }}-{{ stats.years.max }}</h3>
                    <p>Intervalo de Anos</p>
                </div>
                <div class="stat-card">
                    <h3>{{ stats.databases|length }}</h3>
                    <p>Bases de Dados</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>🔍 Fluxo PRISMA</h2>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background: #f8f9fa;">
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6;">Estágio</th>
                    <th style="padding: 12px; text-align: right; border-bottom: 2px solid #dee2e6;">Quantidade</th>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">📚 Identificação</td>
                    <td style="padding: 12px; text-align: right; border-bottom: 1px solid #dee2e6;">{{ prisma.identification }}</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">🔍 Triagem (aprovados)</td>
                    <td style="padding: 12px; text-align: right; border-bottom: 1px solid #dee2e6;">{{ prisma.screening }}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; padding-left: 40px; border-bottom: 1px solid #dee2e6;">❌ Excluídos na triagem</td>
                    <td style="padding: 12px; text-align: right; border-bottom: 1px solid #dee2e6; color: #dc3545;">{{ prisma.screening_excluded }}</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">📖 Elegibilidade (aprovados)</td>
                    <td style="padding: 12px; text-align: right; border-bottom: 1px solid #dee2e6;">{{ prisma.eligibility }}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; padding-left: 40px; border-bottom: 1px solid #dee2e6;">❌ Excluídos na elegibilidade</td>
                    <td style="padding: 12px; text-align: right; border-bottom: 1px solid #dee2e6; color: #dc3545;">{{ prisma.eligibility_excluded }}</td>
                </tr>
                <tr style="background: #d4edda;">
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6; font-weight: bold;">✅ Incluídos (final)</td>
                    <td style="padding: 12px; text-align: right; border-bottom: 1px solid #dee2e6; font-weight: bold; color: #28a745;">{{ prisma.included }}</td>
                </tr>
            </table>
        </div>
        
        <div class="card">
            <h2>📈 Visualizações</h2>
            <div class="chart-grid">
                <div class="chart-card">
                    <h3>Fluxo PRISMA</h3>
                    <img src="../visualizations/prisma_flow.png" alt="PRISMA Flow">
                </div>
                <div class="chart-card">
                    <h3>Funil de Seleção</h3>
                    <img src="../visualizations/selection_funnel.png" alt="Selection Funnel">
                </div>
                <div class="chart-card">
                    <h3>Distribuição por Ano</h3>
                    <img src="../visualizations/papers_by_year.png" alt="Papers by Year">
                </div>
                <div class="chart-card">
                    <h3>Técnicas Identificadas</h3>
                    <img src="../visualizations/techniques_distribution.png" alt="Techniques">
                </div>
                <div class="chart-card">
                    <h3>Cobertura por Base</h3>
                    <img src="../visualizations/database_coverage.png" alt="Database Coverage">
                </div>
                <div class="chart-card">
                    <h3>Distribuição de Relevância</h3>
                    <img src="../visualizations/relevance_distribution.png" alt="Relevance Distribution">
                </div>
            </div>
        </div>
    </div>
    
    {{ footer_html | safe }}
</body>
</html>
        """
        
        template = self.env.from_string(html_template)
        return template.render(**report_data, stats=stats, prisma=prisma, footer_html=self._footer_html())
    
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Artigos - {{ stage.title() }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; line-height: 1.6; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .navbar-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .navbar-title { color: white; font-size: 1.2rem; font-weight: 600; }
        .navbar-links { display: flex; gap: 1.5rem; }
        .navbar-links a { color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; transition: background 0.2s; }
        .navbar-links a:hover { background: rgba(255,255,255,0.2); }
        .navbar-links a.active { background: rgba(255,255,255,0.3); }
        .content { margin: 40px; max-width: 1200px; margin: 0 auto; padding: 40px; }
        .paper { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .paper-title { color: #2c3e50; font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .paper-meta { color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px; }
        .paper-abstract { text-align: justify; margin: 15px 0; }
        .paper-techniques { background: #ecf0f1; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .paper-criteria { background: #d4edda; padding: 10px; border-radius: 4px; margin: 10px 0; border-left: 4px solid #28a745; }
        .score { float: right; background: #27ae60; color: white; padding: 5px 10px; border-radius: 15px; }
    </style>
</head>
<body>
     <nav class="navbar">
         <div class="navbar-content">
             <a href="../../../index.html" class="navbar-title" style="text-decoration:none;">Revisão Sistemática - CCW</a>
             <div class="navbar-links">
                 <a href="summary_report.html">📈 Resumo</a>
                 <a href="papers_report_included.html" class="active">📄 Artigos Incluídos</a>
                 <a href="gap_analysis.html">📊 Análise de Lacunas</a>
             </div>
         </div>
     </nav>    <div class="content">
    <h1>Relatório de Artigos - {{ stage.title() }}</h1>
    <p><em>{{ papers_data|length }} artigos encontrados</em></p>
    
    {% for paper in papers_data %}
    <div class="paper">
        {% if paper.relevance_score %}
        <div class="score">Score: {{ paper.relevance_score }}</div>
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
            <strong>URL:</strong> <a href="{{ paper.url }}" target="_blank" rel="noopener">{{ paper.url[:60] }}{{ '...' if paper.url|length > 60 else '' }}</a>
            {% endif %}
        </div>
        
        {% if paper.abstract %}
        <div class="paper-abstract">
            <strong>Resumo:</strong> {{ paper.abstract }}
        </div>
        {% endif %}
        
        {% if paper.inclusion_criteria_met %}
        <div class="paper-criteria">
            <strong>✅ Critérios de Inclusão Atendidos:</strong> {{ paper.inclusion_criteria_met }}
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
        <div class="paper-fulltext" style="background: {% if paper.fulltext_extracted %}#d1ecf1{% else %}#f8d7da{% endif %}; padding: 10px; border-radius: 4px; margin: 10px 0; border-left: 4px solid {% if paper.fulltext_extracted %}#17a2b8{% else %}#dc3545{% endif %};">
            <strong>📄 Extração de Texto Completo:</strong>
            {% if paper.fulltext_extracted %}
                <span style="color: #155724; font-weight: bold;">✅ Extraído</span>
                {% if paper.fulltext_size %}
                <br><strong>Tamanho:</strong> {{ "%.1f"|format(paper.fulltext_size / 1024) }} KB
                {% endif %}
                {% if paper.fulltext_keywords %}
                <br><strong>Palavras-chave detectadas:</strong> {{ paper.fulltext_keywords | join(', ') }}
                {% endif %}
            {% else %}
                <span style="color: #721c24; font-weight: bold;">❌ Não extraído</span>
                {% if paper.pdf_failure_reasons %}
                <br><strong>Motivo:</strong> {{ paper.pdf_failure_reasons | join(', ') | replace('_', ' ') | title }}
                {% endif %}
            {% endif %}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    </div>
    {{ footer_html | safe }}
</body>
</html>
        """
        
        template = self.env.from_string(html_template)
        return template.render(papers_data=papers_data, stage=stage, footer_html=self._footer_html())
    
    def _create_gap_analysis_html(self, gaps: Dict) -> str:
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
    <title>Análise de Lacunas da Revisão Sistemática</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; line-height: 1.6; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .navbar-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .navbar-title { color: white; font-size: 1.2rem; font-weight: 600; }
        .navbar-links { display: flex; gap: 1.5rem; }
        .navbar-links a { color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; transition: background 0.2s; }
        .navbar-links a:hover { background: rgba(255,255,255,0.2); }
        .navbar-links a.active { background: rgba(255,255,255,0.3); }
        .content { max-width: 1200px; margin: 0 auto; padding: 40px; }
        .gap-section { margin: 30px 0; padding: 20px; border-left: 4px solid #e74c3c; background: #fdf2f2; }
        ul { padding-left: 20px; }
        li { margin: 10px 0; }
        .no-gaps { color: #27ae60; font-style: italic; }
    </style>
</head>
<body>
     <nav class="navbar">
         <div class="navbar-content">
             <a href="../../../index.html" class="navbar-title" style="text-decoration:none;">Revisão Sistemática - CCW</a>
             <div class="navbar-links">
                 <a href="summary_report.html">📈 Resumo</a>
                 <a href="papers_report_included.html">📄 Artigos Incluídos</a>
                 <a href="gap_analysis.html" class="active">📊 Análise de Lacunas</a>
             </div>
         </div>
     </nav>    <div class="content">
    <h1>Análise de Lacunas da Revisão Sistemática</h1>
    
    {% for gap_type, gap_list in gaps.items() %}
    <div class="gap-section">
        <h2>{{ gap_type.replace('_', ' ').title() }}</h2>
        {% if gap_list %}
        <ul>
            {% for gap in gap_list %}
            <li>{{ gap }}</li>
            {% endfor %}
        </ul>
        {% else %}
        <p class="no-gaps">Nenhuma lacuna significativa identificada nesta categoria.</p>
        {% endif %}
    </div>
    {% endfor %}
    
    <div class="gap-section">
        <h2>Recomendações para Pesquisas Futuras</h2>
        <ul>
            <li>Realizar mais estudos experimentais longitudinais</li>
            <li>Explorar técnicas emergentes como aprendizado por reforço</li>
            <li>Desenvolver métricas padronizadas de avaliação</li>
            <li>Investigar aspectos de usabilidade e aceitação pelos professores</li>
        </ul>
    </div>
    </div>
    {{ footer_html | safe }}
</body>
</html>
        """
        
        template = self.env.from_string(html_template)
        return template.render(gaps=gaps, footer_html=self._footer_html())
