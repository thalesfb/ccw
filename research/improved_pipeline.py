"""
Main pipeline for systematic review automation.

This script orchestrates the complete systematic review process:
1. Search across multiple academic APIs
2. Deduplicate results
3. Save to database
4. Generate exports and reports
"""
import logging
import pandas as pd
from typing import List

from research.config import (
    FIRST_TERMS,
    SECOND_TERMS,
    DEFAULT_YEAR_MIN,
    DEFAULT_LANGUAGES,
    DEFAULT_MAX_RESULTS_PER_QUERY,
    PAPER_COLUMNS
)
from research.models import Paper
from research.utils import queries_generator, ensure_cache_dirs
from research.api_clients import (
    SemanticScholarSearcher,
    OpenAlexSearcher,
    CrossrefSearcher,
    CoreSearcher
)
from research.deduplication import deduplicate_articles
from research.database import DatabaseManager
from research.exports import ExportManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler('research/logs/pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("pipeline")


def search_all_apis(
    queries: List[str],
    max_results_per_query: int = DEFAULT_MAX_RESULTS_PER_QUERY,
    year_min: int = DEFAULT_YEAR_MIN,
    langs: List[str] = None
) -> pd.DataFrame:
    """
    Search for papers across all configured APIs.
    
    Args:
        queries: List of search queries
        max_results_per_query: Maximum results per query per API
        year_min: Minimum publication year
        langs: List of accepted languages
        
    Returns:
        DataFrame with all papers found
    """
    if langs is None:
        langs = DEFAULT_LANGUAGES
    
    all_papers = []
    
    # Search Semantic Scholar
    try:
        logger.info("--- Iniciando busca no Semantic Scholar ---")
        searcher = SemanticScholarSearcher()
        papers = searcher.search(queries, max_results_per_query, year_min, langs)
        all_papers.extend(papers)
        logger.info(f"Semantic Scholar retornou {len(papers)} artigos.")
    except Exception as e:
        logger.error(f"Erro ao acessar Semantic Scholar: {e}", exc_info=True)
    
    # Search OpenAlex
    try:
        logger.info("--- Iniciando busca no OpenAlex ---")
        searcher = OpenAlexSearcher()
        papers = searcher.search(queries, max_results_per_query, year_min, langs)
        all_papers.extend(papers)
        logger.info(f"OpenAlex retornou {len(papers)} artigos.")
    except Exception as e:
        logger.error(f"Erro ao acessar OpenAlex: {e}", exc_info=True)
    
    # Search Crossref
    try:
        logger.info("--- Iniciando busca no CrossRef ---")
        searcher = CrossrefSearcher()
        papers = searcher.search(queries, max_results_per_query, year_min, langs)
        all_papers.extend(papers)
        logger.info(f"CrossRef retornou {len(papers)} artigos.")
    except Exception as e:
        logger.error(f"Erro ao acessar CrossRef: {e}", exc_info=True)
    
    # Search CORE
    try:
        logger.info("--- Iniciando busca no CORE ---")
        searcher = CoreSearcher()
        papers = searcher.search(queries, max_results_per_query, year_min, langs)
        all_papers.extend(papers)
        logger.info(f"CORE retornou {len(papers)} artigos.")
    except Exception as e:
        logger.error(f"Erro ao acessar CORE: {e}", exc_info=True)
    
    # Convert to DataFrame
    if not all_papers:
        logger.warning("Nenhum artigo encontrado em nenhuma base de dados.")
        return pd.DataFrame(columns=PAPER_COLUMNS)
    
    logger.info(f"Total de artigos brutos coletados: {len(all_papers)}")
    df = pd.DataFrame([paper.to_dict() for paper in all_papers])
    
    # Ensure all columns exist
    for col in PAPER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    df = df[PAPER_COLUMNS]
    return df


def run_pipeline(
    max_results_per_query: int = DEFAULT_MAX_RESULTS_PER_QUERY,
    year_min: int = DEFAULT_YEAR_MIN,
    save_to_db: bool = True,
    export_excel: bool = True,
    export_csv: bool = True,
    generate_report: bool = True
) -> pd.DataFrame:
    """
    Run the complete systematic review pipeline.
    
    Args:
        max_results_per_query: Maximum results per query per API
        year_min: Minimum publication year
        save_to_db: Whether to save results to database
        export_excel: Whether to export to Excel
        export_csv: Whether to export to CSV
        generate_report: Whether to generate summary report
        
    Returns:
        DataFrame with deduplicated papers
    """
    logger.info("🚀 Iniciando pipeline de revisão sistemática")
    
    # Ensure directories exist
    ensure_cache_dirs()
    
    # Generate search queries
    queries = queries_generator(FIRST_TERMS, SECOND_TERMS)
    logger.info(f"📝 Geradas {len(queries)} combinações de termos de busca")
    
    # Search all APIs
    df_raw = search_all_apis(queries, max_results_per_query, year_min)
    
    if df_raw.empty:
        logger.warning("⚠️ Pipeline finalizado sem resultados.")
        return df_raw
    
    logger.info(f"📊 Total de artigos brutos: {len(df_raw)}")
    
    # Deduplicate
    logger.info("🔄 Iniciando deduplicação...")
    df_dedup = deduplicate_articles(df_raw, logger)
    logger.info(f"✨ Total após deduplicação: {len(df_dedup)}")
    
    # Save to database
    if save_to_db:
        logger.info("💾 Salvando artigos no banco de dados...")
        db_manager = DatabaseManager()
        papers = [Paper(**row) for _, row in df_dedup.iterrows()]
        saved_count = db_manager.save_papers(papers)
        logger.info(f"✅ {saved_count} artigos salvos no banco de dados")
    
    # Export results
    export_manager = ExportManager()
    
    if export_excel:
        logger.info("📄 Exportando para Excel...")
        excel_path = export_manager.export_to_excel(df_dedup)
        logger.info(f"✅ Excel exportado: {excel_path}")
    
    if export_csv:
        logger.info("📄 Exportando para CSV...")
        csv_path = export_manager.export_to_csv(df_dedup)
        logger.info(f"✅ CSV exportado: {csv_path}")
    
    if generate_report:
        logger.info("📊 Gerando relatório resumido...")
        report_path = export_manager.generate_summary_report(df_dedup)
        logger.info(f"✅ Relatório gerado: {report_path}")
    
    logger.info("🎉 Pipeline concluído com sucesso!")
    return df_dedup


if __name__ == "__main__":
    # Run pipeline with default settings
    df_results = run_pipeline()
    print(f"\n✨ Pipeline finalizado. Total de artigos: {len(df_results)}")
