"""Pipeline principal para execução da revisão sistemática."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from ..config import AppConfig, load_config
from ..logging_config import get_audit_logger
from ..db import init_db, read_papers, save_papers, get_db_manager
from ..exports.excel import export_complete_review
from ..processing.dedup import find_duplicates
from ..processing.scoring import compute_relevance_scores
from ..processing.enrichment import enrich_dataframe
from ..processing.selection import apply_prisma_selection, apply_post_collection_filter
from ..search_terms import generate_search_queries  # Import canonical query generator
from ..ingestion import search_semantic_scholar, search_openalex, search_crossref, search_core

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
        self.audit = get_audit_logger("pipeline")

        # Inicializar banco de dados
        init_db(self.config)
        logger.info("Pipeline initialized")

    def generate_search_queries(self) -> List[str]:
        """Gera lista de queries usando gerador canônico bilingue.

        Nova lógica: gera apenas triplas (base AND técnica AND educação) separadas
        por idioma conforme `search_terms.generate_search_queries`.

        Returns
        -------
        list[str]
            Lista de queries geradas.
        """
        queries = generate_search_queries()
        self.search_queries = queries
        logger.info(f"Generated {len(queries)} bilingual triple queries (base AND tech AND edu)")
        return queries

    def collect_data(
        self,
        queries: Optional[List[str]] = None,
        apis: List[str] = ["semantic_scholar", "openalex", "crossref", "core"],
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
                f"🔎 Processando query {i}/{total_queries}: {query[:80]}...")

            for api_name in apis:
                if api_name not in api_functions:
                    logger.warning(f"Unknown API: {api_name}")
                    continue

                try:
                    search_func = api_functions[api_name]
                    df = search_func(query, self.config, limit_per_query)

                    if not df.empty:
                        all_results.append(df)
                        logger.info(f"  ✅ {api_name.title()}: {len(df)} resultados")
                    else:
                        logger.info(f"  ⚪ {api_name.title()}: 0 resultados")

                except Exception as e:
                    logger.error(f"  ❌ {api_name.title()} falhou: {e}")

        if all_results:
            self.results = pd.concat(all_results, ignore_index=True)

            # Log estatísticas por API
            if "database" in self.results.columns:
                api_counts = self.results["database"].value_counts()
                logger.info("Results by API:")
                for api, count in api_counts.items():
                    logger.info(f"  {api}: {count} papers")

            logger.info(
                f"📥 Coletados {len(self.results)} resultados totais de {len(apis)} APIs")
        else:
            self.results = pd.DataFrame()
            logger.warning("⚠️ Nenhum resultado coletado de nenhuma API")

        return self.results

    def process_data(
        self,
        deduplicate_data: bool = True,
        compute_scores: bool = True,
        save_to_db: bool = False,  # ❌ MUDANÇA: Não salvar por padrão
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

        # Deduplicação não-destrutiva: marcar duplicatas, não remover
        if deduplicate_data:
            self.results = find_duplicates(self.results)
            try:
                total = int(len(self.results))
                dup_removed = int(self.results.get('is_duplicate', pd.Series(dtype=bool)).astype(bool).sum())
                self.results.attrs = getattr(self.results, 'attrs', {}) or {}
                self.results.attrs['dedup_stats'] = {
                    'initial_count': total,
                    'removed_by_doi': None,
                    'removed_by_url': None,
                    'removed_by_title': None,
                    'total_removed': dup_removed,
                }
                self.dedup_stats = self.results.attrs['dedup_stats']
            except Exception:
                self.dedup_stats = None

            # Persist analysis artifact with identified duplicates
            try:
                analysis_dir = Path(self.config.database.exports_dir) / "analysis"
                analysis_dir.mkdir(parents=True, exist_ok=True)
                dup_df = self.results[self.results.get('is_duplicate', False) == True]
                dup_df.to_csv(analysis_dir / "deduplicated_rows.csv", index=False, encoding='utf-8-sig')
                logger.info(f"🧹 Deduplicação não-destrutiva: marcadas {len(dup_df)} duplicatas (artefato salvo)")
            except Exception as e:
                logger.warning(f"Falha ao salvar artefato de duplicatas: {e}")

        # Calcular scores de relevância
        if compute_scores:
            self.results = compute_relevance_scores(self.results)
            logger.info("📈 Scores de relevância calculados")

            # Enrichment: add descriptive fields (comp_techniques, main_results, identified_gaps)
            try:
                self.results = enrich_dataframe(self.results)
                logger.info("🔧 Enrichment applied (comp_techniques, main_results, identified_gaps)")
            except Exception as e:
                logger.warning(f"Enrichment step failed: {e}")

        # Ensure dedup_stats survive transformations
        try:
            if getattr(self, 'dedup_stats', None):
                self.results.attrs = getattr(self.results, 'attrs', {}) or {}
                self.results.attrs['dedup_stats'] = self.dedup_stats
        except Exception:
            pass

        # Salvar no banco
        if save_to_db:
            saved = save_papers(self.results, self.config)
            logger.info(f"💾 Salvos {saved} novos papers no banco de dados")

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

        # Ensure PRISMA has access to dedup identification stats
        try:
            if getattr(self, 'dedup_stats', None):
                self.results.attrs = getattr(self.results, 'attrs', {}) or {}
                self.results.attrs['dedup_stats'] = self.dedup_stats
        except Exception:
            pass

        # Aplicar seleção PRISMA
        self.results, selection_stats = apply_prisma_selection(
            self.results,
            self.config,
            threshold,
            max_papers
        )
        # Guardar stats no objeto para uso posterior
        self.selection_stats = selection_stats

        # Contar por estágio
        if "selection_stage" in self.results.columns:
            stage_counts = self.results["selection_stage"].value_counts()
            logger.info("🎯 Resultados da seleção:")
            for stage, count in stage_counts.items():
                logger.info(f"  {stage}: {count} artigos")

        return self.results

    def export_results(
        self,
        output_dir: Optional[Path] = None,
        include_visualizations: bool = True
    , keep_analysis_artifacts: bool = True) -> Dict[str, Path]:
        """Exporta os resultados completos com relatórios e visualizações.

        Args:
            output_dir: Diretório de saída
            include_visualizations: Se deve incluir gráficos e relatórios

        Returns:
            Dicionário com paths dos arquivos gerados
        """
        if output_dir is None:
            output_dir = Path(self.config.database.exports_dir)

        # Calcular estatísticas PRISMA (progressivas e consistentes)
        stats = {}
        # Preferir stats do selector quando disponíveis
        if hasattr(self, 'selection_stats') and self.selection_stats:
            stats = {
                "identification": int(self.selection_stats.get("identification", len(self.results))),
                "duplicates_removed": int(self.selection_stats.get("duplicates_removed", 0)),
                "screening": int(self.selection_stats.get("screening", 0) + self.selection_stats.get("eligibility", 0) + self.selection_stats.get("included", 0)) if False else int(self.selection_stats.get("screening", 0) + self.selection_stats.get("eligibility", 0) + self.selection_stats.get("included", 0))
            }
            # As stats internas já têm elegibilidade e incluídos exatos
            screened = int(self.results['selection_stage'].isin(['screening', 'eligibility', 'included']).sum()) if "selection_stage" in self.results.columns else stats.get("screening", 0)
            eligibility = int(self.selection_stats.get("eligibility", 0))
            included = int(self.selection_stats.get("included", 0))
            # Derivar excluídos consistentes
            screening_excluded = max(0, screened - eligibility)
            eligibility_excluded = max(0, eligibility - included)
            stats.update({
                "screening": screened,
                "screening_excluded": screening_excluded,
                "eligibility": eligibility,
                "eligibility_excluded": eligibility_excluded,
                "included": included,
            })
        elif "selection_stage" in self.results.columns:
            identification = int(len(self.results))
            screened = int(self.results['selection_stage'].isin(['screening', 'eligibility', 'included']).sum())
            eligible = int(self.results['selection_stage'].isin(['eligibility', 'included']).sum())
            included = int((self.results['selection_stage'] == 'included').sum())
            screening_excluded = max(0, screened - eligible)
            eligibility_excluded = max(0, eligible - included)
            stats = {
                "identification": identification,
                "duplicates_removed": 0,
                "screening": screened,
                "screening_excluded": screening_excluded,
                "eligibility": eligible,
                "eligibility_excluded": eligibility_excluded,
                "included": included,
            }

        # Configuração usada
        config_dict = {
            "year_range": f"{self.config.review.year_min}-{self.config.review.year_max}",
            "languages": list(self.config.review.languages),
            "abstract_required": self.config.review.abstract_required,
            "relevance_threshold": self.config.review.relevance_threshold
        }
        # Control cleanup behaviour: when keep_analysis_artifacts is True, we
        # instruct exporter to NOT cleanup analysis files
        config_dict["cleanup_analysis"] = not bool(keep_analysis_artifacts)

        # Ensure we generate visuals/reports from the canonical DB source.
        # Prefer the persisted DB table as the single source of truth when available.
        try:
            # Harmonize DB selection fields to avoid export/DB mismatches
            try:
                get_db_manager(self.config).normalize_consistency()
            except Exception:
                pass
            df_db = read_papers(self.config)
            if df_db is not None and not df_db.empty:
                df_to_export = df_db
            else:
                df_to_export = self.results
        except Exception:
            df_to_export = self.results

        if include_visualizations:
            return export_complete_review(df_to_export, stats, config_dict, output_dir)
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
        min_relevance_score: float = 4.0,
        *,
        skip_audit_filter: bool = False,
        keep_analysis_artifacts: bool = True,
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
        # Início auditoria
        self.audit.start_pipeline({
            "year_range": f"{self.config.review.year_min}-{self.config.review.year_max}",
            "languages": list(self.config.review.languages),
            "relevance_threshold": self.config.review.relevance_threshold,
        })
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
        self.audit.log_article_collection("APIs", len(self.results), len(self.results))

        # 3. Processar dados
        logger.info("\n🔄 Phase 3: Data Processing & Scoring")
        self.process_data()
        self.audit.log_data_quality("pos-processamento", {
            "total": len(self.results),
            "colunas": list(self.results.columns),
        })

        # 4. Aplicar critérios de seleção PRISMA
        logger.info("\n🔍 Phase 4: PRISMA Selection")
        self.apply_selection_criteria(min_relevance_score)
        selected_count = int((self.results.get("selection_stage", pd.Series()) == "included").sum())
        self.audit.log_article_selection("final", len(self.results), selected_count, {
            "min_relevance_score": min_relevance_score
        })
        
        # 4.5 Post-collection auditable filter (minimal)
        if not skip_audit_filter:
            try:
                analysis_dir = Path(self.config.database.exports_dir) / "analysis"
                # persist_decisions True -> annotate decisions and persist exclusions
                # to the canonical DB (cfg passed) so exclusion decisions are
                # recorded even if the in-memory DataFrame is replaced by the
                # kept-subset returned by the function.
                self.results = apply_post_collection_filter(
                    self.results,
                    analysis_dir,
                    persist_decisions=True,
                    cfg=self.config,
                )
                logger.info("Applied post-collection audit filter (decisions annotated)")
            except Exception as e:
                logger.warning(f"Post-collection filter failed: {e}")

        # Salvar papers com selection_stage e decisões de filtro atualizados
        saved = save_papers(self.results, self.config)
        logger.info(f"Updated {saved} papers with selection stages and filter decisions")

        # 5. Exportar resultados
        if export:
            logger.info("\n💾 Phase 5: Export & Visualization")
            export_files = self.export_results(keep_analysis_artifacts=keep_analysis_artifacts)

            if isinstance(export_files, dict):
                logger.info("📊 Arquivos gerados:")
                for file_type, path in export_files.items():
                    if isinstance(path, list):
                        logger.info(f"  {file_type}: {len(path)} arquivos")
                    else:
                        logger.info(f"  {file_type}: {path}")
            else:
                logger.info(f"📊 Resultados exportados para: {export_files}")

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

        # Finalizar auditoria
        self.audit.end_pipeline({
            "total": total_papers,
            "incluidos": included_papers,
        })
        return self.results


def run_systematic_review(
    queries: Optional[List[str]] = None,
    config: Optional[AppConfig] = None,
    export: bool = True,
    *,
    skip_audit_filter: bool = False,
    keep_analysis_artifacts: bool = False,
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
    return pipeline.run_full_pipeline(
        queries,
        export,
        min_relevance_score=4.0,
        skip_audit_filter=skip_audit_filter,
        keep_analysis_artifacts=keep_analysis_artifacts,
    )


if __name__ == "__main__":
    # Exemplo de execução
    results = run_systematic_review()
    print(f"\nFinal results: {len(results)} papers")

    if not results.empty:
        print("\nSample of results:")
        print(results[["title", "year", "doi"]].head())
