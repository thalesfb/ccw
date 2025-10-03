"""Pipeline principal para execução da revisão sistemática."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from ..config import AppConfig, load_config
from ..db import init_db, read_papers, save_papers
from ..exports.excel import export_complete_review
from ..ingestion import search_semantic_scholar, search_openalex, search_crossref, search_core
from ..processing.dedup import deduplicate
from ..processing.scoring import compute_relevance_scores
from ..processing.selection import apply_prisma_selection

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SystematicReviewPipeline:
    """Pipeline para execução completa da revisão sistemática."""

    def __init__(self, config: Optional[AppConfig] = None):
        """Inicializa o pipeline.

        Args:
            config: Configuração da aplicação (se None, carrega do ambiente)
        """
        self.config = config or load_config()
        self.results = pd.DataFrame()
        self.search_queries = []

        # Inicializar banco de dados
        init_db(self.config)
        logger.info("Pipeline initialized")

    def generate_search_queries(
        self,
        base_terms: Optional[List[str]] = None,
        technique_terms: Optional[List[str]] = None,
        education_terms: Optional[List[str]] = None
    ) -> List[str]:
        """Gera combinações de termos de busca.

        Args:
            base_terms: Termos base (ex: ["mathematics", "math"])
            technique_terms: Termos de técnicas (ex: ["machine learning", "AI"])
            education_terms: Termos educacionais (ex: ["education", "learning"])

        Returns:
            Lista de queries geradas
        """
        if base_terms is None:
            base_terms = [
                "mathematics",
                "math",
                "matemática"
            ]

        if technique_terms is None:
            technique_terms = [
                "machine learning",
                "artificial intelligence",
                "AI",
                "deep learning",
                "data mining",
                "learning analytics",
                "educational data mining"
            ]

        if education_terms is None:
            education_terms = [
                "education",
                "teaching",
                "learning",
                "assessment",
                "personalization",
                "adaptive learning",
                "intelligent tutoring"
            ]

        queries = []

        # Gerar combinações
        for base in base_terms:
            for tech in technique_terms:
                # Base + Técnica
                queries.append(f"{base} AND {tech}")

                # Base + Técnica + Educação
                for edu in education_terms:
                    queries.append(f"{base} AND {tech} AND {edu}")

        self.search_queries = queries
        logger.info(f"Generated {len(queries)} search queries")
        return queries

    def collect_data(
        self,
        queries: Optional[List[str]] = None,
        apis: List[str] = ["semantic_scholar", "openalex",
                           "crossref"],  # CORE removido por instabilidade
        limit_per_query: int = 50  # Reduzido para múltiplas APIs
    ) -> pd.DataFrame:
        """Coleta dados das APIs configuradas.

        Args:
            queries: Lista de queries (se None, usa as geradas)
            apis: Lista de APIs a usar
            limit_per_query: Limite de resultados por query por API

        Returns:
            DataFrame com todos os resultados coletados
        """
        if queries is None:
            queries = self.search_queries or self.generate_search_queries()

        all_results = []
        total_queries = len(queries)

        # Mapear APIs para funções
        api_functions = {
            "semantic_scholar": search_semantic_scholar,
            "openalex": search_openalex,
            "crossref": search_crossref,
            "core": search_core,
        }

        for i, query in enumerate(queries, 1):
            logger.info(
                f"Processing query {i}/{total_queries}: {query[:50]}...")

            for api_name in apis:
                if api_name not in api_functions:
                    logger.warning(f"Unknown API: {api_name}")
                    continue

                try:
                    search_func = api_functions[api_name]
                    df = search_func(query, self.config, limit_per_query)

                    if not df.empty:
                        all_results.append(df)
                        logger.info(f"  {api_name.title()}: {len(df)} results")
                    else:
                        logger.info(f"  {api_name.title()}: 0 results")

                except Exception as e:
                    logger.error(f"  {api_name.title()} failed: {e}")

        if all_results:
            self.results = pd.concat(all_results, ignore_index=True)

            # Log estatísticas por API
            if "database" in self.results.columns:
                api_counts = self.results["database"].value_counts()
                logger.info("Results by API:")
                for api, count in api_counts.items():
                    logger.info(f"  {api}: {count} papers")

            logger.info(
                f"Collected {len(self.results)} total results from {len(apis)} APIs")
        else:
            self.results = pd.DataFrame()
            logger.warning("No results collected from any API")

        return self.results

    def process_data(
        self,
        deduplicate_data: bool = True,
        compute_scores: bool = True,
        save_to_db: bool = True
    ) -> pd.DataFrame:
        """Processa os dados coletados.

        Args:
            deduplicate_data: Se deve deduplicar
            compute_scores: Se deve calcular scores de relevância
            save_to_db: Se deve salvar no banco

        Returns:
            DataFrame processado
        """
        if self.results.empty:
            logger.warning("No data to process")
            return self.results

        initial_count = len(self.results)

        # Deduplicar
        if deduplicate_data:
            self.results = deduplicate(self.results)
            logger.info(f"After deduplication: {len(self.results)} papers")

        # Calcular scores de relevância
        if compute_scores:
            self.results = compute_relevance_scores(self.results)
            logger.info("Relevance scores computed")

        # Salvar no banco
        if save_to_db:
            saved = save_papers(self.results, self.config)
            logger.info(f"Saved {saved} new papers to database")

        return self.results

    def apply_selection_criteria(
        self,
        min_relevance_score: Optional[float] = None,
        max_papers: Optional[int] = None,
        *,
        min_score: Optional[float] = None,
    ) -> pd.DataFrame:
        """Aplica critérios de seleção PRISMA aos resultados.

        Args:
            min_relevance_score: Score mínimo de relevância
            max_papers: Número máximo de papers a incluir
            min_score: Alias compatível para ``min_relevance_score`` (para testes)

        Returns:
            DataFrame com seleção aplicada
        """
        if self.results.empty:
            return self.results

        # Compatibilidade: permitir ``min_score`` vindo dos testes
        threshold = min_score if min_score is not None else (
            min_relevance_score if min_relevance_score is not None else self.config.review.relevance_threshold
        )

        # Aplicar seleção PRISMA
        self.results = apply_prisma_selection(
            self.results,
            self.config,
            threshold,
            max_papers
        )

        # Contar por estágio
        if "selection_stage" in self.results.columns:
            stage_counts = self.results["selection_stage"].value_counts()
            logger.info("Selection results:")
            for stage, count in stage_counts.items():
                logger.info(f"  {stage}: {count} papers")

        return self.results

    def export_results(
        self,
        output_dir: Optional[Path] = None,
        include_visualizations: bool = True
    ) -> Dict[str, Path]:
        """Exporta os resultados completos com relatórios e visualizações.

        Args:
            output_dir: Diretório de saída
            include_visualizations: Se deve incluir gráficos e relatórios

        Returns:
            Dicionário com paths dos arquivos gerados
        """
        if output_dir is None:
            output_dir = Path(__file__).parents[3] / "exports"

        # Calcular estatísticas PRISMA
        stats = {}
        if "selection_stage" in self.results.columns:
            stage_counts = self.results["selection_stage"].value_counts()
            stats = {
                "identification": len(self.results),
                "screening": stage_counts.get("screening", 0),
                "screening_excluded": stage_counts.get("screening_excluded", 0),
                "eligibility": stage_counts.get("eligibility", 0),
                "eligibility_excluded": stage_counts.get("eligibility_excluded", 0),
                "included": stage_counts.get("included", 0),
                "duplicates_removed": 0  # Would need to track this
            }

        # Configuração usada
        config_dict = {
            "year_range": f"{self.config.review.year_min}-{self.config.review.year_max}",
            "languages": list(self.config.review.languages),
            "abstract_required": self.config.review.abstract_required,
            "relevance_threshold": self.config.review.relevance_threshold
        }

        if include_visualizations:
            return export_complete_review(self.results, stats, config_dict, output_dir)
        else:
            # Exportação básica em Excel apenas
            from ..exports.excel import to_excel_with_filters
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_path = to_excel_with_filters(
                self.results,
                output_dir / f"systematic_review_{timestamp}.xlsx"
            )
            return {"excel": excel_path}

    def run_full_pipeline(
        self,
        search_queries: Optional[List[str]] = None,
        export: bool = True,
        min_relevance_score: float = 4.0
    ) -> pd.DataFrame:
        """Executa o pipeline completo.

        Args:
            search_queries: Queries de busca (se None, gera automaticamente)
            export: Se deve exportar os resultados
            min_relevance_score: Score mínimo de relevância para inclusão

        Returns:
            DataFrame com os resultados finais
        """
        logger.info("=" * 60)
        logger.info("🔬 REVISÃO SISTEMÁTICA - PIPELINE COMPLETO")
        logger.info("=" * 60)

        # 1. Gerar ou usar queries
        if search_queries is None:
            logger.info("\n📝 Phase 1: Query Generation")
            self.generate_search_queries()
        else:
            self.search_queries = search_queries
            logger.info(
                f"\n📝 Phase 1: Using {len(search_queries)} provided queries")

        # 2. Coletar dados
        logger.info("\n📥 Phase 2: Data Collection")
        self.collect_data()

        # 3. Processar dados
        logger.info("\n🔄 Phase 3: Data Processing & Scoring")
        self.process_data()

        # 4. Aplicar critérios de seleção PRISMA
        logger.info("\n🔍 Phase 4: PRISMA Selection")
        self.apply_selection_criteria(min_relevance_score)

        # 5. Exportar resultados
        if export:
            logger.info("\n💾 Phase 5: Export & Visualization")
            export_files = self.export_results()

            if isinstance(export_files, dict):
                logger.info("📊 Generated files:")
                for file_type, path in export_files.items():
                    if isinstance(path, list):
                        logger.info(f"  {file_type}: {len(path)} files")
                    else:
                        logger.info(f"  {file_type}: {path}")
            else:
                logger.info(f"📊 Results exported to: {export_files}")

        # Estatísticas finais
        included_papers = len(
            self.results[self.results.get("selection_stage", "") == "included"])
        total_papers = len(self.results)

        logger.info("\n" + "=" * 60)
        logger.info(f"✅ PIPELINE CONCLUÍDO")
        logger.info(f"📄 Total de papers processados: {total_papers}")
        logger.info(f"✨ Papers incluídos na revisão: {included_papers}")
        if total_papers > 0:
            logger.info(
                f"📊 Taxa de inclusão: {included_papers/total_papers*100:.1f}%")
        logger.info("=" * 60)

        return self.results


def run_systematic_review(
    queries: Optional[List[str]] = None,
    config: Optional[AppConfig] = None,
    export: bool = True
) -> pd.DataFrame:
    """Função conveniente para executar a revisão sistemática.

    Args:
        queries: Lista de queries de busca
        config: Configuração (se None, carrega do ambiente)
        export: Se deve exportar os resultados

    Returns:
        DataFrame com os resultados
    """
    pipeline = SystematicReviewPipeline(config)
    return pipeline.run_full_pipeline(queries, export)


if __name__ == "__main__":
    # Exemplo de execução
    results = run_systematic_review()
    print(f"\nFinal results: {len(results)} papers")

    if not results.empty:
        print("\nSample of results:")
        print(results[["title", "year", "doi"]].head())
