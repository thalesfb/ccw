"""Módulo para exportação de resultados em Excel e relatórios completos."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows

from ..analysis.reports import ReportGenerator
from ..analysis.visualizations import ReviewVisualizer
from ..config import load_config

logger = logging.getLogger(__name__)


def to_excel(
    df: pd.DataFrame,
    output_path: Optional[Path] = None,
    sheet_name: str = "Papers",
    include_timestamp: bool = True,
    auto_adjust_columns: bool = True
) -> Path:
    """Exporta DataFrame para arquivo Excel formatado.
    
    Args:
        df: DataFrame com os dados
        output_path: Caminho de saída (se None, gera automaticamente)
        sheet_name: Nome da planilha
        include_timestamp: Se deve incluir timestamp no nome do arquivo
        auto_adjust_columns: Se deve ajustar largura das colunas
        
    Returns:
        Path do arquivo criado
    """
    if df.empty:
        logger.warning("DataFrame is empty, creating minimal Excel file")
    
    # Carregar configuração
    config = load_config()
    
    # Gerar nome do arquivo se necessário
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if include_timestamp else ""
        filename = f"systematic_review_{timestamp}.xlsx" if timestamp else "systematic_review.xlsx"
        output_path = Path(config.database.exports_dir) / filename
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Criar writer do pandas
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Escrever DataFrame principal
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Adicionar estatísticas em outra aba
        stats_df = create_statistics_dataframe(df)
        stats_df.to_excel(writer, sheet_name="Statistics", index=False)
        
        # Formatar as planilhas
        workbook = writer.book
        format_worksheet(workbook[sheet_name], auto_adjust_columns)
        format_worksheet(workbook["Statistics"], auto_adjust_columns)
    
    logger.info(f"Exported {len(df)} papers to {output_path}")
    return output_path


def to_excel_with_filters(
    df: pd.DataFrame,
    output_path: Optional[Path] = None,
    filters: Optional[Dict[str, List]] = None
) -> Path:
    """Exporta DataFrame para Excel com múltiplas abas baseadas em filtros.
    
    Args:
        df: DataFrame com os dados
        output_path: Caminho de saída
        filters: Dicionário com nome da aba e lista de condições
        
    Returns:
        Path do arquivo criado
    """
    config = load_config()
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(config.database.exports_dir) / f"filtered_review_{timestamp}.xlsx"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Aba com todos os dados
        df.to_excel(writer, sheet_name="All Papers", index=False)
        
        # Abas filtradas
        if filters:
            for sheet_name, conditions in filters.items():
                filtered_df = df.copy()
                for condition in conditions:
                    filtered_df = filtered_df.query(condition)
                filtered_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel limit: 31 chars
        
        # Estatísticas
        stats_df = create_statistics_dataframe(df)
        stats_df.to_excel(writer, sheet_name="Statistics", index=False)
        
        # Formatar todas as planilhas
        workbook = writer.book
        for sheet in workbook.worksheets:
            format_worksheet(sheet, True)
    
    logger.info(f"Exported filtered results to {output_path}")
    return output_path


def create_statistics_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Cria DataFrame com estatísticas dos dados.
    
    Args:
        df: DataFrame com os papers
        
    Returns:
        DataFrame com estatísticas
    """
    stats = []
    
    # Estatísticas gerais
    stats.append({"Metric": "Total Papers", "Value": len(df)})
    
    if not df.empty:
        # Por ano
        if "year" in df.columns:
            year_counts = df["year"].value_counts().sort_index()
            stats.append({"Metric": "Papers per Year", "Value": ""})
            for year, count in year_counts.items():
                stats.append({"Metric": f"  {year}", "Value": count})
        
        # Por fonte
        if "source" in df.columns:
            source_counts = df["source"].value_counts()
            stats.append({"Metric": "Papers per Source", "Value": ""})
            for source, count in source_counts.items():
                stats.append({"Metric": f"  {source}", "Value": count})
        
        # Por search engine
        if "search_engine" in df.columns:
            engine_counts = df["search_engine"].value_counts()
            stats.append({"Metric": "Papers per Search Engine", "Value": ""})
            for engine, count in engine_counts.items():
                stats.append({"Metric": f"  {engine}", "Value": count})
        
        # Campos preenchidos
        stats.append({"Metric": "Field Completeness", "Value": ""})
        for col in df.columns:
            filled = df[col].notna().sum()
            percentage = (filled / len(df)) * 100
            stats.append({"Metric": f"  {col}", "Value": f"{filled} ({percentage:.1f}%)"})
        
        # Open Access
        if "is_open_access" in df.columns:
            open_access = df["is_open_access"].sum() if df["is_open_access"].dtype == bool else 0
            stats.append({"Metric": "Open Access Papers", "Value": f"{open_access} ({open_access/len(df)*100:.1f}%)"})
    
    return pd.DataFrame(stats)


def format_worksheet(worksheet, auto_adjust: bool = True):
    """Formata uma planilha do Excel.
    
    Args:
        worksheet: Planilha do openpyxl
        auto_adjust: Se deve ajustar largura das colunas
    """
    # Formatar cabeçalho
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for cell in worksheet[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Ajustar largura das colunas
    if auto_adjust:
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)  # Máximo 50 caracteres
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # Adicionar filtros
    if worksheet.max_row > 1:
        worksheet.auto_filter.ref = worksheet.dimensions


def export_for_analysis(
    df: pd.DataFrame,
    output_dir: Optional[Path] = None,
    formats: List[str] = ["xlsx", "csv", "json"]
) -> Dict[str, Path]:
    """Exporta dados em múltiplos formatos para análise.
    
    Args:
        df: DataFrame com os dados
        output_dir: Diretório de saída
        formats: Lista de formatos desejados
        
    Returns:
        Dicionário com formato e path do arquivo
    """
    config = load_config()
    
    if output_dir is None:
        output_dir = Path(config.database.exports_dir) / "analysis"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    export_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base_name = "papers"
    
    exported_files = {}
    
    if "xlsx" in formats:
        xlsx_path = output_dir / f"{base_name}.xlsx"
        df.to_excel(xlsx_path, index=False)
        exported_files["xlsx"] = xlsx_path
        logger.info(f"Exported to Excel: {xlsx_path}")
    
    if "csv" in formats:
        csv_path = output_dir / f"{base_name}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        exported_files["csv"] = csv_path
        logger.info(f"Exported to CSV: {csv_path}")
    
    if "json" in formats:
        json_path = output_dir / f"{base_name}.json"
        # Converter int64 para int nativo antes de exportar
        df_json = df.copy()
        for col in df_json.select_dtypes(include=['int64']).columns:
            df_json[col] = df_json[col].astype(int)
        df_json.to_json(json_path, orient='records', indent=2, force_ascii=False)
        exported_files["json"] = json_path
        logger.info(f"Exported to JSON: {json_path}")
    
    return exported_files


def export_complete_review(
    df: pd.DataFrame,
    stats: Optional[Dict] = None,
    config: Optional[Dict] = None,
    output_dir: Optional[Path] = None
) -> Dict[str, Path]:
    """Export complete review with Excel, visualizations and reports.
    
    Args:
        df: DataFrame with papers
        stats: PRISMA statistics
        config: Configuration used
        output_dir: Output directory
        
    Returns:
        Dictionary with paths to generated files
    """
    cfg = load_config()
    
    if output_dir is None:
        output_dir = Path(cfg.database.exports_dir)
    
    output_dir = Path(output_dir)
    export_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info("Exporting complete review results...")
    
    exported_files = {}
    
    try:
        # 1. Excel files (sem timestamp no nome)
        excel_path = to_excel_with_filters(
            df, 
            output_dir / "revisao_sistematica.xlsx"
        )
        exported_files["excel"] = excel_path
        
        # 2. Multi-format export
        analysis_files = export_for_analysis(
            df,
            output_dir / "analysis",
            formats=["xlsx", "csv", "json"]
        )
        exported_files.update(analysis_files)
        
        # 3. Visualizations
        visualizer = ReviewVisualizer(output_dir / "visualizations")
        chart_paths = visualizer.generate_all_visualizations(df, stats)
        exported_files["charts"] = chart_paths
        
        # 4. Reports
        report_generator = ReportGenerator(output_dir / "reports")
        
        # Summary report
        summary_path = report_generator.generate_summary_report(df, stats, config)
        exported_files["summary_report"] = summary_path
        
        # Papers report (included papers only)
        if "selection_stage" in df.columns:
            papers_path = report_generator.generate_papers_report(df, "included")
            exported_files["papers_report"] = papers_path
        
        # Gap analysis
        gap_path = report_generator.generate_gap_analysis(df)
        exported_files["gap_analysis"] = gap_path
        
        logger.info(f"Complete review exported to {output_dir}")
        logger.info(f"Generated files: {list(exported_files.keys())}")
        
    except Exception as e:
        logger.error(f"Error exporting complete review: {e}")
    
    return exported_files
