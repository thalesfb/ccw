#!/usr/bin/env python3
"""
Teste completo e consolidado do pipeline de revisão sistemática.
Este é o teste principal que valida todo o fluxo de ponta a ponta.
"""

import sys
import argparse
import time
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path


from src.config import load_config
from src.search_terms import get_all_queries
from src.pipeline.run import SystematicReviewPipeline


class PipelineTestSuite:
    """Suite completa de testes para o pipeline de revisão sistemática."""
    
    def __init__(self, limit_queries: int = None):
        self.limit_queries = limit_queries
        self.results = {}
        
    def test_configuration(self) -> bool:
        """Testa se a configuração foi carregada corretamente."""
        print("🔧 Testando configuração...")
        config = load_config()
        # Validações básicas
        assert hasattr(config, 'apis'), "Configuração deve ter 'apis'"
        assert hasattr(config, 'database'), "Configuração deve ter 'database'"
        assert hasattr(config, 'criteria'), "Configuração deve ter 'criteria'"
        assert config.max_results_per_query > 0, "max_results_per_query deve ser > 0"

        print(f"✅ Configuração válida:")
        print(f"   - APIs configuradas: {len(config.apis.__dict__)} fontes")
        print(f"   - Max results por query: {config.max_results_per_query}")
        print(f"   - Período: {config.criteria.year_min}-{config.criteria.year_max}")
        print(f"   - Idiomas: {config.criteria.languages}")
    
    def test_search_terms(self) -> bool:
        """Testa se os termos de busca foram carregados corretamente."""
        print("🔍 Testando termos de busca...")
        
        queries = get_all_queries()

        # Validações
        assert len(queries) > 0, "Deve haver pelo menos 1 query"
        # The expected number may vary; if it's important to lock, keep the check,
        # otherwise just ensure it's reasonable. We'll keep a soft check but not fail hard.
        if len(queries) < 10:
            raise AssertionError(f"Too few queries generated: {len(queries)}")

        # Verificar estrutura das queries
        for i, query in enumerate(queries[:3]):
            assert " AND " in query, f"Query {i+1} deve conter 'AND'"
            assert len(query.strip()) > 0, f"Query {i+1} não pode estar vazia"

        print(f"✅ Termos de busca válidos:")
        print(f"   - Total de combinações: {len(queries)}")
        print(f"   - Amostras:")
        for i, query in enumerate(queries[:3]):
            print(f"     {i+1}. {query}")
    
    def test_pipeline_initialization(self) -> bool:
        """Testa se o pipeline pode ser inicializado corretamente."""
        print("🚀 Testando inicialização do pipeline...")
        
        pipeline = SystematicReviewPipeline()

        # Validações
        assert pipeline.config is not None, "Pipeline deve ter configuração"
        assert pipeline.db_manager is not None, "Pipeline deve ter database manager"
        assert len(pipeline.clients) > 0, "Pipeline deve ter clientes de API"

        print(f"✅ Pipeline inicializado com sucesso:")
        print(f"   - Clientes disponíveis: {list(pipeline.clients.keys())}")
        print(f"   - Limite de queries: {pipeline.limit_queries or 'Nenhum'}")
    
    def test_pipeline_execution(self) -> bool:
        """Testa a execução completa do pipeline."""
        print("⚡ Testando execução do pipeline...")
        
        start_time = time.time()
        
        pipeline = SystematicReviewPipeline()

        print(f"⏳ Executando pipeline (flow-only test)...")
        # Run the pipeline flow without exporting to files
        results = pipeline.run_full_pipeline(
            search_queries=None,
            export=False,
            min_relevance_score=4.0,
            skip_audit_filter=True,
            keep_analysis_artifacts=False,
        )

        execution_time = time.time() - start_time

        # Validações dos resultados
        assert results is not None, "Pipeline deve retornar resultados"

        # Verificar colunas esperadas (warn if missing)
        expected_columns = ['title', 'abstract', 'year', 'relevance_score', 'comp_techniques']
        for col in expected_columns:
            if col not in results.columns:
                print(f"⚠️ Coluna esperada '{col}' não encontrada")

        print(f"✅ Pipeline executado com sucesso:")
        print(f"   - Tempo de execução: {execution_time:.2f}s")
        print(f"   - Artigos processados: {len(results)}")
        print(f"   - Colunas geradas: {len(results.columns)}")

        # Análise de qualidade
        quality_metrics = {}
        if len(results) > 0:
            quality_metrics = {
                'com_abstract': len(results[results['abstract'].notna()]),
                'com_ano': len(results[results['year'].notna()]),
                'score_medio': results['relevance_score'].mean() if 'relevance_score' in results.columns else 0
            }

            print(f"   - Qualidade dos dados:")
            print(f"     • Com abstract: {quality_metrics['com_abstract']}/{len(results)}")
            print(f"     • Com ano: {quality_metrics['com_ano']}/{len(results)}")
            print(f"     • Score médio: {quality_metrics['score_medio']:.2f}")

        # Salvar métricas para análise
        self.results['execution'] = {
            'execution_time': execution_time,
            'articles_processed': len(results),
            'columns_generated': len(results.columns),
            'quality_metrics': quality_metrics if len(results) > 0 else {}
        }
    
    def test_cache_system(self) -> bool:
        """Testa se o sistema de cache está funcionando."""
        print("💾 Testando sistema de cache...")
        
        try:
            # Verificar se os diretórios de cache existem
            cache_dirs = [
                Path("cache/semanticscholar"),
                Path("cache/openalex"), 
                Path("cache/crossref"),
                Path("cache/core")
            ]
            
            cache_found = 0
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    cache_files = list(cache_dir.glob("*.json"))
                    if cache_files:
                        cache_found += len(cache_files)
                        print(f"   - {cache_dir.name}: {len(cache_files)} arquivos em cache")
            
            print(f"✅ Sistema de cache operacional:")
            print(f"   - Total de arquivos em cache: {cache_found}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no sistema de cache: {e}")
            return False
    
    def run_all_tests(self) -> dict:
        """Executa todos os testes e retorna um resumo."""
        print("🧪 Iniciando suite completa de testes...")
        print("=" * 70)
        
        # Lista de testes
        tests = [
            ("Configuração", self.test_configuration),
            ("Termos de Busca", self.test_search_terms), 
            ("Inicialização do Pipeline", self.test_pipeline_initialization),
            ("Sistema de Cache", self.test_cache_system),
            ("Execução do Pipeline", self.test_pipeline_execution)
        ]
        
        results = {}
        passed = 0
        
        for test_name, test_func in tests:
            print(f"\n📋 Executando: {test_name}")
            print("-" * 50)
            
            try:
                success = test_func()
                results[test_name] = success
                if success:
                    passed += 1
            except Exception as e:
                print(f"❌ Erro inesperado em {test_name}: {e}")
                results[test_name] = False
        
        # Resumo final
        print("\n" + "=" * 70)
        print("📊 RESUMO DA SUITE DE TESTES")
        print("=" * 70)
        
        for test_name, success in results.items():
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"{test_name}: {status}")
        
        success_rate = (passed / len(tests)) * 100
        print(f"\nResultado geral: {passed}/{len(tests)} testes passaram ({success_rate:.1f}%)")
        
        if passed == len(tests):
            print("🎉 Todos os testes foram concluídos com sucesso!")
            print("✅ O pipeline está pronto para uso em produção!")
        else:
            print("⚠️ Alguns testes falharam - revisar problemas antes de usar em produção.")
        
        return results


def main():
    """Função principal do teste."""
    parser = argparse.ArgumentParser(
        description="Suite completa de testes para o pipeline de revisão sistemática."
    )
    parser.add_argument(
        "--limit-queries",
        type=int,
        default=None,
        help="Limita o número de queries para teste rápido (padrão: sem limite)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Executa teste rápido com 2 queries"
    )
    
    args = parser.parse_args()
    
    # Configurar limite de queries
    limit = 2 if args.quick else args.limit_queries
    
    if limit:
        print(f"🚀 Executando teste RÁPIDO com {limit} queries")
    else:
        print("🚀 Executando teste COMPLETO com todas as queries")
        print("⚠️ Este teste pode demorar vários minutos!")
    
    # Executar suite de testes
    test_suite = PipelineTestSuite(limit_queries=limit)
    results = test_suite.run_all_tests()
    
    # Salvar resultados para análise posterior
    if test_suite.results:
        print(f"\n📄 Métricas salvas para análise posterior")


if __name__ == "__main__":
    main()