"""Módulo para exportação de resultados em Excel e relatórios completos."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


def _get_historical_dedup_stats() -> Tuple[int, int]:
    """Busca estatísticas históricas de deduplicação da tabela searches.
    
    PRISMA 2020 exige que 'Identification' mostre o total ORIGINAL coletado
    (antes de qualquer deduplicação). Como o banco atual já está limpo,
    precisamos buscar o initial_count registrado durante a coleta.
    
    Returns:
        Tuple[initial_count, total_removed]: Total original coletado e duplicatas removidas.
        Se não encontrado, retorna (0, 0).
    """
    try:
        config = load_config()
        db_path = Path(config.database.db_path)
        
        if not db_path.exists():
            return (0, 0)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buscar o registro mais recente com dedup_stats
        cursor.execute("""
            SELECT results_summary FROM searches 
            WHERE results_summary IS NOT NULL 
            ORDER BY id DESC LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            try:
                data = json.loads(row[0])
                dedup_stats = data.get('dedup_stats', {})
                initial_count = dedup_stats.get('initial_count', 0)
                total_removed = dedup_stats.get('total_removed', 0)
                
                if initial_count > 0:
                    logger.info(
                        f"Histórico de dedup encontrado: initial_count={initial_count}, "
                        f"total_removed={total_removed}"
                    )
                    return (initial_count, total_removed)
            except (json.JSONDecodeError, TypeError):
                pass
        
        return (0, 0)
        
    except Exception as e:
        logger.warning(f"Erro ao buscar histórico de dedup: {e}")
        return (0, 0)


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


def _select_best_duplicate(group: pd.DataFrame, preserve_stage: bool = True) -> pd.Series:
    """Seleciona o melhor registro entre duplicatas baseado em critérios de qualidade.
    
    Critérios (em ordem de prioridade):
    1. Registro com abstract mais longo
    2. Maior número de citações
    3. Com open_access_pdf disponível
    4. Primeiro registro (mais antigo na coleta)
    
    IMPORTANTE: Preserva selection_stage mais alto do original quando duplicate vencedor
    tiver estágio inferior (ex: duplicate com abstract melhor mas stage='screening' não
    substitui original com stage='included').
    
    Args:
        group: DataFrame com registros duplicados
        preserve_stage: Se True, propaga selection_stage mais alto do original
        
    Returns:
        Melhor registro do grupo com stage preservado se aplicável
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
    best = group.loc[best_idx].copy()
    
    # CORREÇÃO: Preservar selection_stage mais alto do original
    if preserve_stage and 'selection_stage' in group.columns:
        # Encontrar registro original (não duplicata)
        originals = group[~group['is_duplicate'].astype(bool)]
        if not originals.empty:
            original = originals.iloc[0]
            
            # Hierarquia de prioridade de estágios
            stage_priority = {'included': 3, 'eligibility': 2, 'screening': 1}
            original_priority = stage_priority.get(original.get('selection_stage'), 0)
            best_priority = stage_priority.get(best.get('selection_stage'), 0)
            
            # Propagar stage do original se for mais alto
            if original_priority > best_priority:
                old_stage = best.get('selection_stage')
                best['selection_stage'] = original['selection_stage']
                if 'status' in original.index:
                    best['status'] = original['status']
                logger.info(
                    f"Stage preservado: Duplicate vencedor tinha stage '{old_stage}' "
                    f"mas original era '{original.get('selection_stage')}' - propagando stage mais alto"
                )
    
    return best


def _compute_prisma_stats_from_df(
    df: pd.DataFrame,
    unique_subset: Optional[pd.DataFrame] = None
) -> dict:
    """Compute PRISMA stats from DataFrame.

    PRISMA 2020 flow correto:
    - identification: Total de registros coletados (incluindo duplicatas) - busca histórico
    - duplicates_removed: Registros removidos por deduplicação
    - screening: Registros únicos disponíveis para triagem
    - screening_excluded: Registros excluídos NA TRIAGEM (selection_stage='screening')
    - eligibility: Registros que PASSARAM triagem (selection_stage='eligibility' ou 'included')
    - eligibility_excluded: Registros excluídos NA ELEGIBILIDADE (selection_stage='eligibility')
    - included: Registros finalmente incluídos (selection_stage='included')
    
    IMPORTANTE: Usa histórico da tabela searches para identification (total original
    coletado antes de deduplicação), pois o banco atual já está limpo.
    
    Args:
        df: DataFrame com papers (já deduplicados)
        unique_subset: Subconjunto único para consistência (opcional)
        
    Returns:
        Dicionário com estatísticas PRISMA
    """
    stats = {}

    raw_rows = int(len(df))

    # Normalizar DOIs apenas para métricas de integridade (não para PRISMA)
    if 'doi' in df.columns:
        normalized = (
            df['doi']
            .fillna('')
            .astype(str)
            .str.strip()
            .str.lower()
        )
        distinct_dois = {d for d in normalized if d}
    else:
        distinct_dois = set()

    distinct_count = int(len(distinct_dois)) if distinct_dois else raw_rows

    stats['raw_rows'] = raw_rows
    stats['distinct_doi'] = distinct_count
    
    # Subconjunto único para cálculos de estágios (define antes de usar)
    if unique_subset is not None:
        unique_df = unique_subset.copy()
    elif 'is_duplicate' in df.columns:
        duplicate_mask = df['is_duplicate'].fillna(False).astype(bool)
        unique_df = df[~duplicate_mask].copy()
    else:
        unique_df = df.copy()

    # PRISMA 2020: Identification deve ser o total ORIGINAL coletado (antes de dedup)
    # Buscar do histórico da tabela searches
    historical_initial, historical_removed = _get_historical_dedup_stats()

    # Contagem única efetiva após deduplicação
    screening_count = int(len(unique_df))

    if historical_initial > 0:
        stats['identification'] = historical_initial

        computed_removed = max(0, historical_initial - screening_count)
        stats['duplicates_removed'] = computed_removed

        # Se o valor histórico não bate com o cálculo atual, registrar divergência
        if historical_removed and historical_removed != computed_removed:
            delta = computed_removed - historical_removed
            logger.warning(
                "PRISMA: divergência entre histórico e banco atual. "
                f"historical_removed={historical_removed}, computed_removed={computed_removed}, delta={delta}"
            )
        else:
            logger.info(
                f"PRISMA usando histórico: identification={historical_initial}, "
                f"duplicates_removed={computed_removed}"
            )
    else:
        # Fallback: usar contagem atual garantindo coerência com screening
        stats['identification'] = raw_rows
        stats['duplicates_removed'] = max(0, stats['identification'] - screening_count)
        logger.warning(
            "Histórico de dedup não encontrado - usando contagem atual do DataFrame. "
            "PRISMA identification pode estar subestimado."
        )

    stats['screening'] = screening_count  # Registros únicos disponíveis para triagem

    # Cálculo baseado em selection_stage APENAS sobre registros únicos
    if not unique_df.empty and 'selection_stage' in unique_df.columns:
        stage_series = unique_df['selection_stage'].fillna('').astype(str).str.lower()
        if 'status' in unique_df.columns:
            status_series = unique_df['status'].fillna('').astype(str).str.lower()
        else:
            status_series = pd.Series('', index=unique_df.index)

        # Excluídos na triagem exigem status de exclusão
        screening_mask = stage_series == 'screening'
        screening_excluded = screening_mask & status_series.str.contains('exclu')
        stats['screening_excluded'] = int(screening_excluded.sum())

        # Passaram triagem: elegibilidade ou incluídos
        passed_screening = stage_series.isin(['eligibility', 'included'])
        stats['eligibility'] = int(passed_screening.sum())

        # Excluídos na elegibilidade
        eligibility_mask = stage_series == 'eligibility'
        eligibility_excluded = eligibility_mask & status_series.str.contains('exclu')
        stats['eligibility_excluded'] = int(eligibility_excluded.sum())

        # Incluídos finais
        included_mask = stage_series == 'included'
        stats['included'] = int(included_mask.sum())
    else:
        stats['screening_excluded'] = 0
        stats['eligibility'] = int(len(unique_df))
        stats['eligibility_excluded'] = 0
        stats['included'] = int(len(unique_df))

    # AUDITORIA: Métricas de validação para preservação de stage
    if unique_subset is not None:
        raw_included = len(df[df['selection_stage'] == 'included'])
        unique_included = stats['included']
        duplicates_included = len(df[
            (df['selection_stage'] == 'included') & 
            (df['is_duplicate'].astype(bool))
        ])
        
        expected_delta = duplicates_included
        actual_delta = raw_included - unique_included
        
        stats['_audit'] = {
            'raw_included_total': raw_included,
            'duplicates_marked_included': duplicates_included,
            'unique_included': unique_included,
            'expected_delta': expected_delta,
            'actual_delta': actual_delta
        }
        
        if actual_delta != expected_delta:
            logger.warning(
                f"⚠️ VALIDAÇÃO FALHOU: Esperava remover {expected_delta} papers 'included' duplicados, "
                f"mas removeu {actual_delta}. Delta incorreto: {actual_delta - expected_delta} papers perdidos."
            )
        else:
            logger.info(
                f"✓ Validação passou: Removidos {actual_delta} papers 'included' duplicados conforme esperado"
            )

    return stats


def get_best_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna DataFrame com os melhores registros entre duplicatas.
    
    Para cada grupo de duplicatas, seleciona o registro com melhor qualidade.
    Registros únicos (is_duplicate=False) são mantidos como estão.
    
    CORREÇÃO (2025-11-24): Agora remove originals quando um duplicate melhor é encontrado.
    
    Args:
        df: DataFrame com papers (incluindo duplicatas)
        
    Returns:
        DataFrame com melhores registros (duplicatas removidas, originals substituídos se necessário)
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
    
    # Track DOIs being replaced (originals que serão removidos)
    processed_dois = set()
    
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
                
                # Se o melhor é um duplicate (não o original), marcar DOI para remoção
                if best.get('is_duplicate', False):
                    processed_dois.add(doi)
                
                best_duplicates.append(best)
            else:
                # Original não encontrado, selecionar melhor das duplicatas
                best = _select_best_duplicate(group)
                best_duplicates.append(best)
        else:
            # Sem referência clara, selecionar melhor
            best = _select_best_duplicate(group)
            best_duplicates.append(best)
    
    # CORREÇÃO: Remover originals que foram substituídos por duplicates melhores
    if processed_dois:
        originals_to_remove = unique_papers[unique_papers['doi'].isin(processed_dois)]
        logger.info(f"Removing {len(processed_dois)} originals replaced by better duplicates")
        
        # AUDITORIA: Registrar distribuição de stages dos originals removidos
        if 'selection_stage' in originals_to_remove.columns:
            removed_stages = originals_to_remove['selection_stage'].value_counts()
            logger.info(f"Originals removidos por stage: {removed_stages.to_dict()}")
            
            # Aviso se perdendo papers included/eligibility
            critical_stages = ['included', 'eligibility']
            for stage in critical_stages:
                if stage in removed_stages.index:
                    logger.warning(
                        f"⚠️ Removidos {removed_stages[stage]} papers '{stage}' durante deduplicação - "
                        f"verificar se lógica de preservação de stage funcionou corretamente"
                    )
        
        unique_papers = unique_papers[~unique_papers['doi'].isin(processed_dois)]
    
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
    output_dir: Optional[Path] = None,
    fulltext_stats: Optional[Dict] = None
) -> Dict[str, Path]:
    """Export complete review with Excel, visualizations and reports.
    
    Args:
        df: DataFrame with papers (incluindo duplicatas marcadas)
        stats: PRISMA statistics
        config: Configuration used
        output_dir: Output directory
        fulltext_stats: Full-text extraction statistics (optional)
        
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

        raw_df = df

        # AUDITORIA: Capturar contagens de stage antes da deduplicação
        raw_stages = raw_df['selection_stage'].value_counts().to_dict() if 'selection_stage' in raw_df.columns else {}
        
        # Selecionar melhores duplicatas em vez de descartar totalmente (qualidade)
        df_best = get_best_duplicates(raw_df) if 'is_duplicate' in raw_df.columns else raw_df
        if 'is_duplicate' in df_best.columns:
            # Após seleção de melhores duplicatas, garantir flag consistente
            df_best = df_best.copy()
            if 'is_duplicate' in df_best.columns:
                # Recalcular flag (todos agora únicos)
                df_best['is_duplicate'] = False
                df_best['duplicate_of'] = None
        df_for_export = df_best
        logger.info(f"Registros para export (após melhor duplicata): {len(df_for_export)}")
        
        # AUDITORIA: Comparar contagens de stage após deduplicação
        if raw_stages and 'selection_stage' in df_for_export.columns:
            export_stages = df_for_export['selection_stage'].value_counts().to_dict()
            logger.info(f"Contagem de stages antes dedup: {raw_stages}")
            logger.info(f"Contagem de stages após dedup: {export_stages}")
            
            # Avisos para perdas em stages críticos
            for stage in ['included', 'eligibility']:
                raw_count = raw_stages.get(stage, 0)
                export_count = export_stages.get(stage, 0)
                delta = raw_count - export_count
                
                if delta > 0:
                    logger.warning(
                        f"⚠️ Stage '{stage}' perdeu {delta} papers durante deduplicação "
                        f"({raw_count} -> {export_count})"
                    )
                elif delta < 0:
                    logger.error(
                        f"❌ Stage '{stage}' GANHOU papers durante deduplicação - problema de integridade! "
                        f"({raw_count} -> {export_count})"
                    )

        # Calcular estatísticas uma única vez (inclui raw_rows/distinct_doi)
        local_stats = _compute_prisma_stats_from_df(raw_df, df_for_export)
        if stats:
            prisma_keys = {
                'identification', 'duplicates_removed', 'screening',
                'screening_excluded', 'eligibility', 'eligibility_excluded', 'included'
            }
            for k, v in stats.items():
                if k not in prisma_keys:
                    local_stats[k] = v

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
        
        # Summary report (passa DataFrame filtrado e stats originais + fulltext_stats)
        summary_path = report_generator.generate_summary_report(df_for_export, local_stats, config, fulltext_stats=fulltext_stats)
        exported_files["summary_report"] = summary_path
        
        # Papers report (included papers only - já filtrado) - passa fulltext_stats para incluir dados de extração
        if "selection_stage" in df_for_export.columns:
            papers_path = report_generator.generate_papers_report(df_for_export, "included", fulltext_stats=fulltext_stats)
            exported_files["papers_report"] = papers_path
        
        # Gap analysis
        gap_path = report_generator.generate_gap_analysis(df_for_export)
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
