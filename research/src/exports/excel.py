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
from ..db import read_papers
from ..processing.dedup import normalize_doi

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


def _select_best_duplicate(group: pd.DataFrame) -> pd.Series:
    """Seleciona o melhor registro entre duplicatas baseado em critérios de qualidade.
    
    Critérios (em ordem de prioridade):
    1. Registro com abstract mais longo
    2. Maior número de citações
    3. Com open_access_pdf disponível
    4. Primeiro registro (mais antigo na coleta)
    
    Args:
        group: DataFrame com registros duplicados
        
    Returns:
        Melhor registro do grupo
    """
    if len(group) == 1:
        return group.iloc[0]
    
    # Criar score de qualidade
    scores = pd.Series(0.0, index=group.index)
    
    # 1. Abstract length (peso 40%)
    if 'abstract' in group.columns:
        abstract_len = group['abstract'].fillna('').astype(str).str.len()
        if abstract_len.max() > 0:
            scores += (abstract_len / abstract_len.max()) * 40
    
    # 2. Citation count (peso 30%)
    if 'citation_count' in group.columns:
        citations = group['citation_count'].fillna(0).astype(float)
        if citations.max() > 0:
            scores += (citations / citations.max()) * 30
    
    # 3. Open access PDF (peso 20%)
    if 'open_access_pdf' in group.columns:
        has_pdf = group['open_access_pdf'].notna() & (group['open_access_pdf'] != '')
        scores += has_pdf.astype(int) * 20
    
    # 4. Ordem de coleta (peso 10% - favorece primeiro)
    scores += (len(group) - group.reset_index(drop=True).index) * (10.0 / len(group))
    
    # Retornar registro com maior score
    best_idx = scores.idxmax()
    return group.loc[best_idx]


def _compute_prisma_stats_from_df(df: pd.DataFrame) -> dict:
    """Compute PRISMA stats from DataFrame.

    PRISMA 2020 flow correto:
    - identification: Total de registros coletados (incluindo duplicatas)
    - duplicates_removed: Registros marcados como duplicatas
    - screening: Registros únicos disponíveis para triagem
    - screening_excluded: Registros excluídos NA TRIAGEM (selection_stage='screening')
    - eligibility: Registros que PASSARAM triagem (selection_stage='eligibility' ou 'included')
    - eligibility_excluded: Registros excluídos NA ELEGIBILIDADE (selection_stage='eligibility')
    - included: Registros finalmente incluídos (selection_stage='included')
    
    IMPORTANTE: Esta função deve receber o DataFrame COMPLETO (com duplicatas) para
    calcular corretamente identification e duplicates_removed. As contagens de estágios
    (screening, eligibility, included) são calculadas apenas sobre registros únicos.
    
    Args:
        df: DataFrame com papers (incluindo duplicatas marcadas)
        
    Returns:
        Dicionário com estatísticas PRISMA
    """
    stats = {}

    total_count = int(len(df))
    stats['identification'] = total_count

    # Duplicatas removidas e criar subset de únicos
    if 'is_duplicate' in df.columns:
        dup_removed = int(df['is_duplicate'].astype(bool).sum())
        unique_df = df[~df['is_duplicate'].astype(bool)].copy()
    else:
        # Legacy fallback
        dup_removed = 0
        try:
            cfg = load_config()
            dedup_file = Path(cfg.database.exports_dir) / "analysis" / "deduplicated_rows.csv"
            if dedup_file.exists():
                dup_df = pd.read_csv(dedup_file)
                dup_removed = int(len(dup_df))
        except Exception as e:
            logger.debug(f"Could not load dedup info: {e}")
        unique_df = df.copy()
    
    stats['duplicates_removed'] = dup_removed
    stats['screening'] = int(len(unique_df))  # Registros únicos para triagem

    # Cálculo baseado em selection_stage APENAS sobre registros únicos
    if 'selection_stage' in unique_df.columns:
        # Excluídos NA TRIAGEM (ficaram em 'screening' + status='excluded')
        screening_excluded = unique_df['selection_stage'] == 'screening'
        stats['screening_excluded'] = int(screening_excluded.sum())
        
        # Passaram triagem = elegibilidade + incluídos
        passed_screening = unique_df['selection_stage'].isin(['eligibility', 'included'])
        stats['eligibility'] = int(passed_screening.sum())
        
        # Excluídos NA ELEGIBILIDADE (ficaram em 'eligibility' + status='excluded')
        eligibility_excluded = unique_df['selection_stage'] == 'eligibility'
        stats['eligibility_excluded'] = int(eligibility_excluded.sum())
        
        # Incluídos finais
        included = unique_df['selection_stage'] == 'included'
        stats['included'] = int(included.sum())
    else:
        # Sem selection_stage - defaults
        stats['screening_excluded'] = 0
        stats['eligibility'] = int(len(unique_df))
        stats['eligibility_excluded'] = 0
        stats['included'] = int(len(unique_df))

    return stats


def get_best_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna DataFrame com os melhores registros entre duplicatas.
    
    Para cada grupo de duplicatas, seleciona o registro com melhor qualidade.
    Registros únicos (is_duplicate=False) são mantidos como estão.
    
    Args:
        df: DataFrame com papers (incluindo duplicatas)
        
    Returns:
        DataFrame com melhores registros
    """
    if df.empty:
        return df
    
    # Se não tem coluna is_duplicate, retorna como está
    if 'is_duplicate' not in df.columns:
        return df
    
    # Separar únicos e duplicatas
    unique_papers = df[~df['is_duplicate'].astype(bool)].copy()
    duplicate_papers = df[df['is_duplicate'].astype(bool)].copy()
    
    if duplicate_papers.empty:
        return unique_papers
    
    # Agrupar duplicatas por duplicate_of e selecionar melhor de cada grupo
    best_duplicates = []
    for dup_ref, group in duplicate_papers.groupby('duplicate_of'):
        # Encontrar o original também
        if isinstance(dup_ref, str) and dup_ref.startswith('DOI:'):
            doi = dup_ref[4:]  # Remove 'DOI:' prefix
            original = unique_papers[unique_papers['doi'] == doi]
            if not original.empty:
                # Incluir original no grupo para comparação
                full_group = pd.concat([original, group], ignore_index=True)
                best = _select_best_duplicate(full_group)
                best_duplicates.append(best)
            else:
                # Original não encontrado, selecionar melhor das duplicatas
                best = _select_best_duplicate(group)
                best_duplicates.append(best)
        else:
            # Sem referência clara, selecionar melhor
            best = _select_best_duplicate(group)
            best_duplicates.append(best)
    
    if best_duplicates:
        best_df = pd.DataFrame(best_duplicates)
        # Remover is_duplicate flag dos melhores selecionados
        best_df['is_duplicate'] = False
        best_df['duplicate_of'] = None
        result = pd.concat([unique_papers, best_df], ignore_index=True)
    else:
        result = unique_papers
    
    return result


def export_complete_review(
    df: pd.DataFrame,
    stats: Optional[Dict] = None,
    config: Optional[Dict] = None,
    output_dir: Optional[Path] = None
) -> Dict[str, Path]:
    """Export complete review with Excel, visualizations and reports.
    
    Args:
        df: DataFrame with papers (incluindo duplicatas marcadas)
        stats: PRISMA statistics
        config: Configuration used
        output_dir: Output directory
        
    Returns:
        Dictionary with paths to generated files
    
    Note:
        Duplicatas (is_duplicate=True) são automaticamente filtradas.
        Todas as análises, visualizações e relatórios usam apenas registros únicos.
    """
    cfg = load_config()
    
    if output_dir is None:
        output_dir = Path(cfg.database.exports_dir)
    
    output_dir = Path(output_dir)
    export_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info("Exporting complete review results...")
    
    exported_files = {}
    
    try:
        # Ensure we have data from DB if empty
        if df is None or df.empty:
            try:
                df = read_papers(cfg)
                logger.info("Reloaded papers from DB for export (canonical source)")
            except Exception as e:
                logger.warning(f"Failed to reload DB for export: {e}")
                df = pd.DataFrame()

        # Data already deduplicated by pipeline - just normalize DOIs for consistency
        if not df.empty and 'doi' in df.columns:
            df = df.copy()
            df['doi'] = df['doi'].fillna('').astype(str).apply(normalize_doi)

        # ALWAYS recompute identification from DataFrame (canonical source)
        # Do NOT use historical dedup_stats.initial_count (pre-database values)
        local_stats = _compute_prisma_stats_from_df(df)
        
        # Merge with provided stats but ensure identification reflects database reality
        if stats:
            local_stats.update({k: v for k, v in stats.items() if k not in ['identification', 'duplicates_removed']})

        # CRITICAL: Filtrar APENAS registros únicos (is_duplicate=False) para todas as análises
        # Não criar registros sintéticos, usar dados reais únicos
        df_for_export = df
        if 'is_duplicate' in df.columns:
            df_for_export = df[~df['is_duplicate'].astype(bool)].copy()
            logger.info(f"Filtrando registros únicos: {len(df_for_export)} de {len(df)} (removidos {len(df) - len(df_for_export)} duplicatas)")
        
        # RECALCULAR stats baseado nos dados FILTRADOS para manter consistência
        local_stats = _compute_prisma_stats_from_df(df)  # Stats originais com duplicatas
        
        # Merge com stats fornecidos mantendo identification original
        if stats:
            local_stats.update({k: v for k, v in stats.items() if k not in ['identification', 'duplicates_removed']})

        # 1. Excel files (moved to analysis folder to avoid duplicate basenames)
        analysis_dir = output_dir / "analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        excel_path = to_excel_with_filters(
            df_for_export,
            analysis_dir / "revisao_sistematica.xlsx"
        )
        exported_files["excel"] = excel_path
        
        # 2. Multi-format export (analysis artifacts) - usa APENAS dados únicos
        analysis_dir = output_dir / "analysis"
        analysis_files = export_for_analysis(
            df_for_export,
            analysis_dir,
            formats=["xlsx", "csv", "json"]
        )
        exported_files.update(analysis_files)
        
        # 3. Visualizations (usa dados únicos + stats consistentes)
        visualizer = ReviewVisualizer(output_dir / "visualizations")
        chart_paths = visualizer.generate_all_visualizations(df_for_export, local_stats)
        exported_files["charts"] = chart_paths
        
        # 4. Reports (usa dados únicos)
        report_generator = ReportGenerator(output_dir / "reports")
        
        # Summary report (passa DataFrame filtrado e stats originais)
        summary_path = report_generator.generate_summary_report(df_for_export, local_stats, config)
        exported_files["summary_report"] = summary_path
        
        # Papers report (included papers only - já filtrado)
        if "selection_stage" in df_for_export.columns:
            papers_path = report_generator.generate_papers_report(df_for_export, "included")
            exported_files["papers_report"] = papers_path
        
        # Gap analysis
        gap_path = report_generator.generate_gap_analysis(df)
        exported_files["gap_analysis"] = gap_path

        # Optional cleanup: remove analysis-level artifacts after they have
        # been used to generate the final reports (keeps reports and visuals)
        # Default behavior: keep analysis artifacts unless explicitly requested
        # to cleanup. This preserves `papers.csv/json/xlsx` by default.
        cleanup_analysis = False if config is None else bool(config.get("cleanup_analysis", False))
        if cleanup_analysis:
            try:
                for ext in ("csv", "json", "xlsx"):
                    p = analysis_dir / f"papers.{ext}"
                    if p.exists():
                        p.unlink()
                        logger.info(f"Removed analysis artifact: {p}")
                # Also remove the separate revisao_sistematica.xlsx if present
                revisao = analysis_dir / "revisao_sistematica.xlsx"
                if revisao.exists():
                    revisao.unlink()
                    logger.info(f"Removed analysis artifact: {revisao}")
            except Exception as e:
                logger.warning(f"Failed to cleanup analysis artifacts: {e}")
        
        logger.info(f"Complete review exported to {output_dir}")
        logger.info(f"Generated files: {list(exported_files.keys())}")
        
    except Exception as e:
        logger.error(f"Error exporting complete review: {e}")
    
    return exported_files
