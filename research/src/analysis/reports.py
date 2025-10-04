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

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Gera relatórios completos da revisão sistemática."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize report generator.
        
        Args:
            output_dir: Diretório para salvar relatórios
        """
        config = load_config()
        
        if output_dir is None:
            output_dir = Path(config.database.exports_dir) / "reports"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize visualizer
        self.visualizer = ReviewVisualizer(self.output_dir.parent / "visualizations")
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_summary_report(
        self,
        df: pd.DataFrame,
        stats: Optional[Dict] = None,
        config: Optional[Dict] = None
    ) -> Path:
        """Generate summary report with key statistics.
        
        Args:
            df: DataFrame with papers
            stats: PRISMA statistics
            config: Configuration used
            
        Returns:
            Path to generated report
        """
        logger.info("Generating summary report...")
        
        # Generate statistics
        report_stats = self._calculate_statistics(df, stats)
        
        # Generate visualizations
        chart_paths = self.visualizer.generate_all_visualizations(df, stats)

        # Build included papers list (limit to 50 for readability)
        included_list = []
        if 'selection_stage' in df.columns:
            included_df = df[df['selection_stage'] == 'included'].copy()
            for _, row in included_df.head(50).iterrows():
                included_list.append({
                    'title': row.get('title') or 'Título não disponível',
                    'authors': row.get('authors') or 'N/A',
                    'year': int(row.get('year')) if pd.notna(row.get('year')) else 'N/A',
                    'venue': row.get('venue') or row.get('source_publication') or 'N/A',
                    'doi': row.get('doi') or '',
                    'url': row.get('url') or ''
                })
        
        # Create report content
        report_data = {
            'title': 'Relatório da Revisão Sistemática',
            'subtitle': 'Técnicas Computacionais na Educação Matemática',
            'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'statistics': report_stats,
            'charts': [{'name': p.stem, 'path': p} for p in chart_paths],
            'config': config or {},
            'included_list': included_list
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
        fields: Optional[List[str]] = None
    ) -> Path:
        """Generate detailed papers report.
        
        Args:
            df: DataFrame with papers
            stage: Selection stage to include
            fields: Fields to include in report
            
        Returns:
            Path to generated report
        """
        if fields is None:
            fields = [
                'title', 'authors', 'year', 'venue', 'abstract',
                'relevance_score', 'comp_techniques', 'study_type'
            ]
        
        # Filter by stage
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
        report_path = self.output_dir / f"papers_report_{stage}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        papers_data = []
        for _, row in papers_df.iterrows():
            paper_data = {}
            for field in fields:
                if field in row.index:
                    value = row[field]
                    if pd.isna(value):
                        value = "N/A"
                    paper_data[field] = value
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
        report_path = self.output_dir / f"gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
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
        # Normalizar PRISMA com ints nativos
        prisma_stats = {}
        if stats:
            for k, v in stats.items():
                try:
                    prisma_stats[k] = int(v) if v is not None else 0
                except Exception:
                    prisma_stats[k] = v

        report_stats = {
            'total_papers': int(len(df)),
            'prisma': prisma_stats,
        }
        
        # Year statistics
        if 'year' in df.columns:
            years = df['year'].dropna()
            if not years.empty:
                # Converter int64 para int nativo antes de serializar
                year_dist = years.value_counts().to_dict()
                report_stats['years'] = {
                    'min': int(years.min()),
                    'max': int(years.max()),
                    'mean': round(float(years.mean()), 1),
                    'distribution': {int(k): int(v) for k, v in year_dist.items()}
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
            identification = int(len(df))
            status_series = df.get('status', pd.Series([None] * len(df), index=df.index)).fillna('')
            screening_excluded = int(((df['selection_stage'] == 'screening') & (status_series == 'excluded')).sum())
            eligibility_excluded = int(((df['selection_stage'] == 'eligibility') & (status_series == 'excluded')).sum())
            included = int((df['selection_stage'] == 'included').sum())
            screening_remaining = identification - screening_excluded
            eligibility_remaining = screening_remaining - eligibility_excluded

            report_stats['selection_stages'] = {
                'Identificação': identification,
                'Triagem': screening_remaining,
                'Elegibilidade': eligibility_remaining,
                'Incluídos': included,
                'Excluídos na Triagem': screening_excluded,
                'Excluídos na Elegibilidade': eligibility_excluded,
            }
        
        return report_stats
    
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
            years = df['year'].dropna()
            if not years.empty:
                year_counts = years.value_counts().sort_index()
                # Find years with low publication counts
                mean_count = year_counts.mean()
                low_years = year_counts[year_counts < mean_count * 0.5]
                gaps['temporal_gaps'] = [
                    f"Baixo número de publicações em {year} ({count} artigos)"
                    for year, count in low_years.items()
                ]
        
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
                <a href="index.html" class="active">🔍 Sumário</a>
                <a href="papers.html">📄 Artigos</a>
                <a href="gap-analysis.html">📊 Análise de Lacunas</a>
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
        
        report_path = self.output_dir / f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
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
        
        json_path = self.output_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
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
        .score { float: right; background: #27ae60; color: white; padding: 5px 10px; border-radius: 15px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-content">
            <div class="navbar-title">📚 Revisão Sistemática</div>
            <div class="navbar-links">
                <a href="index.html">🔍 Sumário</a>
                <a href="papers.html" class="active">📄 Artigos</a>
                <a href="gap-analysis.html">📊 Análise de Lacunas</a>
            </div>
        </div>
    </nav>
    
    <div class="content">
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
            <strong>Venue:</strong> {{ paper.venue or 'N/A' }}
        </div>
        
        {% if paper.abstract %}
        <div class="paper-abstract">
            <strong>Resumo:</strong> {{ paper.abstract[:500] }}{% if paper.abstract|length > 500 %}...{% endif %}
        </div>
        {% endif %}
        
        {% if paper.comp_techniques %}
        <div class="paper-techniques">
            <strong>Técnicas:</strong> {{ paper.comp_techniques }}
        </div>
        {% endif %}
        
        {% if paper.study_type %}
        <div class="paper-meta">
            <strong>Tipo de Estudo:</strong> {{ paper.study_type }}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    </div>
</body>
</html>
        """
        
        template = self.env.from_string(html_template)
        return template.render(papers_data=papers_data, stage=stage)
    
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
            <div class="navbar-title">📚 Revisão Sistemática</div>
            <div class="navbar-links">
                <a href="index.html">🔍 Sumário</a>
                <a href="papers.html">📄 Artigos</a>
                <a href="gap-analysis.html" class="active">📊 Análise de Lacunas</a>
            </div>
        </div>
    </nav>
    
    <div class="content">
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
</body>
</html>
        """
        
        template = self.env.from_string(html_template)
        return template.render(gaps=gaps)
