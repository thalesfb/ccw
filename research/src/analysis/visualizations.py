"""Módulo para criação de visualizações da revisão sistemática."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

from ..config import load_config

logger = logging.getLogger(__name__)

# Configuração do estilo
plt.style.use('default')
sns.set_palette("husl")


class ReviewVisualizer:
    """Gera visualizações para revisão sistemática."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize visualizer.
        
        Args:
            output_dir: Diretório para salvar gráficos
        """
        config = load_config()
        
        if output_dir is None:
            output_dir = Path(config.database.exports_dir) / "visualizations"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar estilo
        self._setup_style()
    
    def _setup_style(self):
        """Configure matplotlib style for academic papers."""
        plt.rcParams.update({
            'figure.figsize': (10, 6),
            'font.size': 11,
            'axes.titlesize': 12,
            'axes.labelsize': 11,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 14,
            'font.family': 'serif',
            'axes.grid': True,
            'grid.alpha': 0.3,
            'axes.spines.top': False,
            'axes.spines.right': False,
        })
    
    def prisma_flow_diagram(
        self,
        stats: Dict[str, int],
        save_path: Optional[Path] = None
    ) -> Path:
        """Create PRISMA flow diagram.
        
        Args:
            stats: Dictionary with PRISMA statistics
            save_path: Path to save the diagram
            
        Returns:
            Path to saved diagram
        """
        if save_path is None:
            save_path = self.output_dir / "prisma_flow.png"
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Colors
        box_color = '#E8F4FD'
        exclude_color = '#FFE6E6'
        text_color = '#2C3E50'
        
        # Box dimensions
        box_width = 2.5
        box_height = 0.8
        
        # Title
        ax.text(5, 9.7, 'Fluxo PRISMA da Revisão Sistemática', 
                ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Identification
        identification = int(stats.get('identification', 0))
        duplicates_removed = int(stats.get('duplicates_removed', 0))
        after_duplicates = identification - duplicates_removed

        # Usar diretamente valores progressivos fornecidos nas stats
        screening = int(stats.get('screening', max(0, after_duplicates)))
        eligibility = int(stats.get('eligibility', max(0, screening)))
        included = int(stats.get('included', 0))

        # Caixas de exclusão (informativas)
        screening_excluded = int(stats.get('screening_excluded', max(0, identification - screening)))
        eligibility_excluded = int(stats.get('eligibility_excluded', max(0, screening - eligibility)))

        logger.info(
            f"PRISMA stats used -> ident={identification}, dup_removed={duplicates_removed}, "
            f"screening={screening}, eligibility={eligibility}, included={included}, "
            f"screening_excl={screening_excluded}, eligibility_excl={eligibility_excluded}"
        )
        
        # Main flow boxes with correct PRISMA stages
        boxes = [
            (5, 8.5, f"Registros identificados\nnas bases de dados\n(n = {identification})", box_color),
            (5, 7.5, f"Registros sem duplicatas\n(n = {after_duplicates})", box_color),
            (5, 6.5, f"Registros selecionados\npara triagem\n(n = {screening})", box_color),
            (5, 5.5, f"Artigos avaliados\npara elegibilidade\n(n = {eligibility})", box_color),
            (5, 4.5, f"Estudos incluídos\nna síntese qualitativa\n(n = {included})", box_color),
        ]
        
        # Exclusion boxes with correct counts
        exclusions = [
            (8, 6.5, f"Registros excluídos\nna triagem\n(n = {screening_excluded})", exclude_color),
            (8, 5.5, f"Artigos excluídos\nna elegibilidade\n(n = {eligibility_excluded})", exclude_color),
        ]
        
        # Draw main flow boxes
        for x, y, text, color in boxes:
            rect = Rectangle((x - box_width/2, y - box_height/2), 
                           box_width, box_height, 
                           facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(rect)
            ax.text(x, y, text, ha='center', va='center', fontsize=10, color=text_color)
        
        # Draw exclusion boxes
        for x, y, text, color in exclusions:
            rect = Rectangle((x - box_width/2, y - box_height/2), 
                           box_width, box_height, 
                           facecolor=color, edgecolor='red', linewidth=1)
            ax.add_patch(rect)
            ax.text(x, y, text, ha='center', va='center', fontsize=9, color=text_color)
        
        # Draw arrows
        arrow_props = dict(arrowstyle='->', lw=2, color='black')
        
        # Main flow arrows
        for i in range(len(boxes) - 1):
            ax.annotate('', xy=(5, boxes[i+1][1] + box_height/2), 
                       xytext=(5, boxes[i][1] - box_height/2), 
                       arrowprops=arrow_props)
        
        # Exclusion arrows
        ax.annotate('', xy=(8 - box_width/2, 6.5), xytext=(5 + box_width/2, 6.5), 
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
        ax.annotate('', xy=(8 - box_width/2, 5.5), xytext=(5 + box_width/2, 5.5), 
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"PRISMA flow diagram saved to {save_path}")
        return save_path
    
    def papers_by_year(
        self,
        df: pd.DataFrame,
        save_path: Optional[Path] = None
    ) -> Path:
        """Create papers by year visualization.
        
        Args:
            df: DataFrame with papers
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        if save_path is None:
            save_path = self.output_dir / "papers_by_year.png"
        
        # Filter valid years
        df_year = df[df['year'].notna() & (df['year'] > 2000)].copy()
        
        if df_year.empty:
            logger.warning("No papers with valid years found")
            return save_path
        
        # Create year distribution
        year_counts = df_year['year'].value_counts().sort_index()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart
        bars = ax1.bar(year_counts.index, year_counts.values, 
                      color='steelblue', alpha=0.7, edgecolor='black')
        ax1.set_title('Distribuição de Artigos por Ano de Publicação')
        ax1.set_xlabel('Ano')
        ax1.set_ylabel('Número de Artigos')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, count in zip(bars, year_counts.values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom', fontsize=9)
        
        # Cumulative chart
        cumulative = year_counts.cumsum()
        ax2.plot(cumulative.index, cumulative.values, 
                marker='o', linewidth=2, markersize=6, color='darkred')
        ax2.fill_between(cumulative.index, cumulative.values, alpha=0.3, color='darkred')
        ax2.set_title('Distribuição Cumulativa por Ano')
        ax2.set_xlabel('Ano')
        ax2.set_ylabel('Número Cumulativo de Artigos')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Papers by year chart saved to {save_path}")
        return save_path
    
    def techniques_distribution(
        self,
        df: pd.DataFrame,
        save_path: Optional[Path] = None
    ) -> Path:
        """Create computational techniques distribution chart.
        
        Args:
            df: DataFrame with papers
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        if save_path is None:
            save_path = self.output_dir / "techniques_distribution.png"
        
        # Extract techniques
        techniques_data = []
        for _, row in df.iterrows():
            if pd.notna(row.get('comp_techniques')):
                techs = str(row['comp_techniques']).split(';')
                for tech in techs:
                    tech = tech.strip()
                    if tech:
                        techniques_data.append(tech)
        
        if not techniques_data:
            logger.warning("No computational techniques found")
            return save_path
        
        # Count techniques
        tech_counts = pd.Series(techniques_data).value_counts()
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = plt.cm.Set3(range(len(tech_counts)))
        bars = ax.barh(range(len(tech_counts)), tech_counts.values, color=colors)
        
        ax.set_yticks(range(len(tech_counts)))
        ax.set_yticklabels(tech_counts.index)
        ax.set_xlabel('Número de Artigos')
        ax.set_title('Distribuição de Técnicas Computacionais')
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, tech_counts.values)):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                   f'{count}', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Techniques distribution chart saved to {save_path}")
        return save_path
    
    def database_coverage(
        self,
        df: pd.DataFrame,
        save_path: Optional[Path] = None
    ) -> Path:
        """Create database coverage pie chart.
        
        Args:
            df: DataFrame with papers
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        if save_path is None:
            save_path = self.output_dir / "database_coverage.png"
        
        if 'database' not in df.columns or df['database'].isna().all():
            logger.warning("No database information found")
            return save_path
        
        # Count by database
        db_counts = df['database'].value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Pie chart
        colors = plt.cm.Set2(range(len(db_counts)))
        wedges, texts, autotexts = ax1.pie(db_counts.values, labels=db_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Cobertura por Base de Dados')
        
        # Bar chart
        bars = ax2.bar(db_counts.index, db_counts.values, color=colors)
        ax2.set_title('Número de Artigos por Base')
        ax2.set_ylabel('Número de Artigos')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, count in zip(bars, db_counts.values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Database coverage chart saved to {save_path}")
        return save_path
    
    def relevance_score_distribution(
        self,
        df: pd.DataFrame,
        save_path: Optional[Path] = None
    ) -> Path:
        """Create relevance score distribution histogram.
        
        Args:
            df: DataFrame with papers
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        if save_path is None:
            save_path = self.output_dir / "relevance_distribution.png"
        
        if 'relevance_score' not in df.columns or df['relevance_score'].isna().all():
            logger.warning("No relevance scores found")
            return save_path
        
        scores = df['relevance_score'].dropna()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram
        ax1.hist(scores, bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
        ax1.axvline(scores.mean(), color='red', linestyle='--', 
                   label=f'Média: {scores.mean():.2f}')
        ax1.axvline(scores.median(), color='blue', linestyle='--', 
                   label=f'Mediana: {scores.median():.2f}')
        ax1.set_xlabel('Score de Relevância')
        ax1.set_ylabel('Frequência')
        ax1.set_title('Distribuição dos Scores de Relevância')
        ax1.legend()
        
        # Box plot
        ax2.boxplot(scores, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7))
        ax2.set_ylabel('Score de Relevância')
        ax2.set_title('Box Plot dos Scores de Relevância')
        ax2.set_xticklabels(['Todos os Artigos'])
        
        # Add statistics text
        stats_text = f"""Estatísticas:
Min: {scores.min():.2f}
Max: {scores.max():.2f}
Média: {scores.mean():.2f}
Mediana: {scores.median():.2f}
Desvio Padrão: {scores.std():.2f}"""
        
        ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Relevance distribution chart saved to {save_path}")
        return save_path
    
    def selection_stages_funnel(
        self,
        df: pd.DataFrame,
        save_path: Optional[Path] = None
    ) -> Path:
        """Create selection stages funnel chart.
        
        Args:
            df: DataFrame with papers
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        if save_path is None:
            save_path = self.output_dir / "selection_funnel.png"

        if 'selection_stage' not in df.columns:
            logger.warning("No selection stage information found")
            return save_path

        # Calculate PRISMA progressive stages by reached stage
        identification = int(len(df))
        # Quantos chegaram à triagem (tudo que está em screening/eligibility/included)
        screened = int(df['selection_stage'].isin(['screening', 'eligibility', 'included']).sum())
        # Quantos chegaram à elegibilidade (eligibility/included)
        eligible = int(df['selection_stage'].isin(['eligibility', 'included']).sum())
        # Quantos incluídos
        included = int((df['selection_stage'] == 'included').sum())

        logger.info(
            f"Funnel counts -> ident={identification}, triagem={screened}, elegibilidade={eligible}, incluidos={included}"
        )

        # PRISMA funnel stages (cada etapa mostra quantos PASSARAM)
        funnel_stages = [
            ('Identificação', identification, '#E8F4FD'),
            ('Triagem', screened, '#B3E5FC'), 
            ('Elegibilidade', eligible, '#81C784'),
            ('Incluídos', included, '#4CAF50')
        ]

        # Filtrar stages com dados
        stages = [name for name, count, color in funnel_stages if count > 0]
        counts = [count for name, count, color in funnel_stages if count > 0]
        colors = [color for name, count, color in funnel_stages if count > 0]

        labels = [f'{stage}\n(n={count})' for stage, count in zip(stages, counts)]

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create funnel effect
        y_positions = list(range(len(stages)))
        bars = ax.barh(y_positions, counts, color=colors, alpha=0.8, edgecolor='black')

        ax.set_yticks(y_positions)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Número de Artigos')
        ax.set_title('Funil de Seleção PRISMA')

        # Add value labels
        for bar, count in zip(bars, counts):
            if count > 0:
                ax.text(
                    bar.get_width() + max(counts) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f'{count}',
                    ha='left',
                    va='center',
                    fontsize=12,
                    fontweight='bold',
                )

        # Invert y-axis to show funnel top-to-bottom
        ax.invert_yaxis()

        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Selection funnel chart saved to {save_path}")
        return save_path
    
    def generate_all_visualizations(
        self,
        df: pd.DataFrame,
        stats: Optional[Dict] = None
    ) -> List[Path]:
        """Generate all standard visualizations.
        
        Args:
            df: DataFrame with papers
            stats: PRISMA statistics
            
        Returns:
            List of paths to generated visualizations
        """
        logger.info("Generating all visualizations...")
        
        generated_files = []
        
        try:
            # PRISMA flow (requires stats)
            if stats:
                generated_files.append(self.prisma_flow_diagram(stats))
            
            # Papers by year
            generated_files.append(self.papers_by_year(df))
            
            # Techniques distribution
            generated_files.append(self.techniques_distribution(df))
            
            # Database coverage
            generated_files.append(self.database_coverage(df))
            
            # Relevance scores
            generated_files.append(self.relevance_score_distribution(df))
            
            # Selection funnel
            generated_files.append(self.selection_stages_funnel(df))
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
        
        logger.info(f"Generated {len(generated_files)} visualizations in {self.output_dir}")
        return generated_files
