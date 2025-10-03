"""
Pipeline melhorado baseado no notebook original.
"""

import logging
import pandas as pd
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from ..config import load_config
from ..search_terms import get_all_queries
from ..filtering_patterns import normalize_text, calculate_relevance_score
from ..ingestion.robust_core import RobustCOREClient
from ..ingestion.semantic_scholar import SemanticScholarClient
from ..ingestion.openalex import OpenAlexClient
from ..ingestion.crossref import CrossrefClient
from ..processing.adaptive_selection import AdaptiveSelection
from ..processing.dedup import deduplicate
from ..database.manager import DatabaseManager
from ..logging_config import get_audit_logger, setup_logging_for_module

# Configurar logger para este módulo
logger = setup_logging_for_module("pipeline")


class ImprovedSystematicReviewPipeline:
    """
    Pipeline melhorado baseado no notebook original.
    """

    def __init__(self, limit_queries: Optional[int] = None):
        self.config = load_config()
        self.db_manager = DatabaseManager(self.config)
        self.adaptive_selection = AdaptiveSelection(
            target_size=100, min_size=20)
        self.limit_queries = limit_queries

        # Inicializar sistema de auditoria
        self.audit_logger = get_audit_logger("systematic_review_pipeline")

        # Inicializar clientes de API
        self.clients = {
            'semantic_scholar': SemanticScholarClient(self.config),
            'open_alex': OpenAlexClient(self.config),
            'crossref': CrossrefClient(self.config),
            'core': RobustCOREClient(self.config)
        }

        # Configurar audit loggers nos clientes
        for client_name, client in self.clients.items():
            client.set_audit_logger(self.audit_logger)

        logger.info("Pipeline melhorado inicializado")
        self.audit_logger.log_user_action("pipeline_initialized", {
            "config_summary": {
                "max_results_per_query": self.config.max_results_per_query,
                "year_min": self.config.criteria.year_min,
                "year_max": self.config.criteria.year_max,
                "languages": self.config.criteria.languages
            }
        })

    def run_complete_pipeline(self) -> pd.DataFrame:
        """
        Executa o pipeline completo baseado no notebook original.
        """
        pipeline_start_time = time.time()

        # Iniciar auditoria
        config_summary = {
            "max_results_per_query": self.config.max_results_per_query,
            "year_range": (self.config.criteria.year_min, self.config.criteria.year_max),
            "languages": self.config.criteria.languages,
            "target_size": self.adaptive_selection.target_size,
            "min_size": self.adaptive_selection.min_size
        }
        self.audit_logger.start_pipeline(config_summary)

        logger.info("🚀 Iniciando pipeline completo...")

        try:
            # 1. Coleta de dados
            logger.info("📥 Etapa 1: Coleta de dados...")
            collection_start = time.time()
            raw_articles = self._collect_data()
            collection_duration = time.time() - collection_start

            self.audit_logger.log_performance("data_collection", collection_duration, {
                "articles_collected": len(raw_articles),
                "sources_used": list(self.clients.keys())
            })
            logger.info(f"✅ Coletados {{len(raw_articles)}} artigos brutos")

            # 2. Deduplicação
            logger.info("🔄 Etapa 2: Deduplicação...")
            dedup_start = time.time()
            df_raw = pd.DataFrame(raw_articles)
            df_deduplicated = deduplicate(df_raw)
            dedup_duration = time.time() - dedup_start

            self.audit_logger.log_performance("deduplication", dedup_duration, {
                "input_count": len(df_raw),
                "output_count": len(df_deduplicated),
                "duplicates_removed": len(df_raw) - len(df_deduplicated)
            })
            logger.info(
                f"✅ Após deduplicação: {{len(df_deduplicated)}} artigos")

            # 3. Enriquecimento
            logger.info("🔧 Etapa 3: Enriquecimento...")
            enrichment_start = time.time()
            df_enriched = self._enrich_data(df_deduplicated)
            enrichment_duration = time.time() - enrichment_start

            self.audit_logger.log_performance("enrichment", enrichment_duration, {
                "input_count": len(df_deduplicated),
                "output_count": len(df_enriched),
                "fields_added": ["relevance_score", "comp_techniques", "main_results", "identified_gaps"]
            })
            logger.info(f"✅ Após enriquecimento: {{len(df_enriched)}} artigos")

            # 4. Seleção adaptativa
            logger.info("🎯 Etapa 4: Seleção adaptativa...")
            selection_start = time.time()
            selected_articles = self.adaptive_selection.select_articles(
                df_enriched.to_dict('records'))
            df_selected = pd.DataFrame(selected_articles)
            selection_duration = time.time() - selection_start

            self.audit_logger.log_performance("adaptive_selection", selection_duration, {
                "input_count": len(df_enriched),
                "output_count": len(df_selected),
                "selection_ratio": len(df_selected) / len(df_enriched) if len(df_enriched) > 0 else 0
            })
            logger.info(f"✅ Artigos selecionados: {{len(df_selected)}}")

            # 5. Salvar no banco de dados
            logger.info("💾 Etapa 5: Salvando no banco de dados...")
            db_start = time.time()
            
            # Converter para PaperRecord objects se necessário
            paper_records = []
            for record in df_selected.to_dict('records'):
                # Criar PaperRecord com campos mapeados
                paper_record = {
                    'title': record.get('title', ''),
                    'abstract': record.get('abstract', ''),
                    'year': record.get('year'),
                    'authors': record.get('authors', ''),
                    'venue': record.get('venue', ''),
                    'doi': record.get('doi', ''),
                    'url': record.get('url', ''),
                    'database': record.get('source', 'unknown'),
                    'relevance_score': record.get('relevance_score', 0),
                    'comp_techniques': record.get('comp_techniques', ''),
                    'main_results': record.get('main_results', ''),
                    'identified_gaps': record.get('identified_gaps', '')
                }
                paper_records.append(paper_record)
            
            saved_count = self.db_manager.insert_papers_bulk(paper_records)
            db_duration = time.time() - db_start

            self.audit_logger.log_performance("database_save", db_duration, {
                "articles_saved": saved_count
            })

            # 6. Exportar resultados
            logger.info("📤 Etapa 6: Exportando resultados...")
            export_start = time.time()
            export_file = self._export_results(df_selected)
            export_duration = time.time() - export_start

            self.audit_logger.log_performance("export", export_duration, {
                "export_file": str(export_file),
                "articles_exported": len(df_selected)
            })

            # Finalizar auditoria
            pipeline_duration = time.time() - pipeline_start_time
            results_summary = {
                "total_articles_collected": len(raw_articles),
                "total_articles_selected": len(df_selected),
                "pipeline_duration_seconds": pipeline_duration,
                "export_file": str(export_file),
                "data_quality": {
                    "missing_abstracts": int(df_selected['abstract'].isna().sum()),
                    "missing_years": int(df_selected['year'].isna().sum()),
                    "avg_relevance_score": float(df_selected['relevance_score'].mean()) if 'relevance_score' in df_selected.columns else 0
                }
            }

            self.audit_logger.end_pipeline(results_summary)
            logger.info("✅ Pipeline completo concluído!")

            return df_selected

        except Exception as e:
            self.audit_logger.log_error(
                e, "pipeline_execution", recoverable=False)
            logger.error(f"❌ Erro fatal no pipeline: {{e}}")
            raise

    def _collect_data(self) -> List[Dict[str, Any]]:
        """
        Coleta dados usando estratégia do notebook original.
        """
        all_articles = []
        queries = get_all_queries()

        if self.limit_queries:
            queries = queries[:self.limit_queries]
            logger.warning(f"⚠️ Coleta de dados limitada a {self.limit_queries} queries.")

        logger.info(f"🔍 Iniciando coleta com {len(queries)} queries...")
        self.audit_logger.log_user_action("data_collection_started", {
            "total_queries": len(queries),
            "max_results_per_query": self.config.max_results_per_query,
            "year_min": self.config.criteria.year_min,
            "languages": self.config.criteria.languages
        })

        for client_name, client in self.clients.items():
            try:
                logger.info(f"📡 Coletando dados de {client_name}...")
                client_start_time = time.time()

                client_articles = []
                for query in queries:
                    try:
                        # Cada cliente search aceita uma query por vez
                        query_results = client.search(
                            query=query,
                            limit=self.config.max_results_per_query
                        )
                        # Converter DataFrame para lista de dicts se necessário
                        if hasattr(query_results, 'to_dict'):
                            query_articles = query_results.to_dict('records')
                        else:
                            query_articles = query_results
                        
                        client_articles.extend(query_articles)
                        
                    except Exception as e:
                        logger.warning(f"Erro na query '{query}' para {client_name}: {e}")
                        continue

                client_duration = time.time() - client_start_time
                all_articles.extend(client_articles)

                # Log de auditoria para cada cliente
                self.audit_logger.log_article_collection(
                    client_name, len(client_articles), len(all_articles))
                self.audit_logger.log_performance(f"api_collection_{client_name}", client_duration, {
                    "queries_processed": len(queries),
                    "articles_collected": len(client_articles),
                    "avg_articles_per_query": len(client_articles) / len(queries) if queries else 0
                })

                logger.info(
                    f"✅ {client_name}: {len(client_articles)} artigos coletados")

            except Exception as e:
                self.audit_logger.log_error(
                    e, f"data_collection_{client_name}", recoverable=True)
                logger.error(f"❌ Erro na coleta de {client_name}: {e}")

        # Log de qualidade dos dados coletados
        if all_articles:
            data_quality = {
                "total_articles": len(all_articles),
                "articles_with_title": sum(1 for a in all_articles if a.get('title')),
                "articles_with_abstract": sum(1 for a in all_articles if a.get('abstract')),
                "articles_with_year": sum(1 for a in all_articles if a.get('year')),
                "articles_with_doi": sum(1 for a in all_articles if a.get('doi_url')),
                "unique_sources": len(set(a.get('source', 'unknown') for a in all_articles))
            }
            self.audit_logger.log_data_quality("raw_collection", data_quality)

        return all_articles

    def _enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriquece dados usando heurísticas robustas do notebook original.
        """
        df_enriched = df.copy()

        # Calcular scores de relevância
        df_enriched['relevance_score'] = df_enriched.apply(
            lambda row: calculate_relevance_score(row.to_dict()), axis=1
        )

        # Preencher campos faltantes com heurísticas - verificar se existem primeiro
        if 'abstract' not in df_enriched.columns:
            df_enriched['abstract'] = 'Abstract não disponível'
        else:
            df_enriched['abstract'] = df_enriched['abstract'].fillna('Abstract não disponível')

        if 'year' not in df_enriched.columns:
            df_enriched['year'] = 2020
        else:
            df_enriched['year'] = df_enriched['year'].fillna(2020)

        # Extrair técnicas computacionais
        df_enriched['comp_techniques'] = df_enriched.apply(
            self._extract_comp_techniques, axis=1
        )

        # Extrair principais resultados
        df_enriched['main_results'] = df_enriched.apply(
            self._extract_main_results, axis=1
        )

        # Identificar lacunas
        df_enriched['identified_gaps'] = df_enriched.apply(
            self._identify_gaps, axis=1
        )

        return df_enriched

    def _extract_comp_techniques(self, row: pd.Series) -> str:
        """
        Extrai técnicas computacionais do texto.
        """
        title = str(row.get('title', '')).lower()
        abstract = str(row.get('abstract', '')).lower()
        text = title + ' ' + abstract

        techniques = []
        tech_mapping = {
            'Machine Learning': ['machine learning', 'ml', 'neural network', 'deep learning'],
            'Learning Analytics': ['learning analytics', 'educational data mining'],
            'Intelligent Tutoring': ['intelligent tutoring', 'tutoring system'],
            'Adaptive Learning': ['adaptive learning', 'personalized learning'],
            'AI/Artificial Intelligence': ['artificial intelligence', 'ai '],
            'Assessment': ['assessment', 'evaluation', 'testing'],
            'Predictive Analytics': ['predictive', 'prediction', 'forecasting']
        }

        for category, terms in tech_mapping.items():
            if any(term in text for term in terms):
                techniques.append(category)

        return ', '.join(techniques) if techniques else 'Não especificado'

    def _extract_main_results(self, row: pd.Series) -> str:
        """
        Extrai principais resultados do abstract.
        """
        abstract = str(row.get('abstract', ''))
        title = str(row.get('title', ''))

        result_keywords = ['improved', 'increased',
                           'enhanced', 'better', 'effective', 'significant']

        results = []
        for keyword in result_keywords:
            if keyword in abstract.lower():
                sentences = abstract.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        results.append(sentence.strip())
                        break

        if results:
            return '. '.join(results[:2])
        elif 'review' in title.lower():
            return 'Revisão da literatura sobre o tema'
        elif 'system' in title.lower():
            return 'Desenvolvimento/avaliação de sistema'
        else:
            return 'Resultados não explicitamente mencionados'

    def _identify_gaps(self, row: pd.Series) -> str:
        """
        Identifica lacunas mencionadas no abstract.
        """
        abstract = str(row.get('abstract', ''))

        gap_keywords = ['limitation', 'challenge',
                        'future work', 'further research', 'need for']

        gaps = []
        for keyword in gap_keywords:
            if keyword in abstract.lower():
                sentences = abstract.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        gaps.append(sentence.strip())
                        break

        return '. '.join(gaps[:2]) if gaps else 'Lacunas não explicitamente mencionadas'

    def _export_results(self, df: pd.DataFrame) -> Path:
        """
        Exporta resultados para Excel.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"revisao_sistematica_improved_{timestamp}.xlsx"

        # Criar diretório exports se não existir
        Path("exports").mkdir(exist_ok=True)

        filepath = Path("exports") / filename
        df.to_excel(filepath, index=False)

        logger.info(f"✅ Resultados exportados para: {{filepath}}")

        # Log de auditoria para exportação
        self.audit_logger.log_user_action("results_exported", {
            "export_file": str(filepath),
            "articles_exported": len(df),
            "columns_exported": list(df.columns),
            "file_size_mb": filepath.stat().st_size / (1024 * 1024) if filepath.exists() else 0
        })

        return filepath
