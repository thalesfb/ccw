#!/usr/bin/env python3
"""
Script de teste para validar as correções implementadas.
"""

import sys
from pathlib import Path
import argparse

# Adicionar o diretório raiz do projeto (research) ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.search_terms import get_all_queries
from src.config import load_config
from src.pipeline.improved_pipeline import ImprovedSystematicReviewPipeline




def test_configuration():
    """Testa se a configuração foi carregada corretamente."""
    print("🔧 Testando configuração...")

    try:
        config = load_config()
        print(f"✅ Configuração carregada:")
        print(f"   - Semantic Scholar delay: {config.apis.semantic_scholar.get('rate_delay', 'N/A')}s")
        print(f"   - OpenAlex delay: {config.apis.open_alex.get('rate_delay', 'N/A')}s")
        print(f"   - Crossref delay: {config.apis.crossref.get('rate_delay', 'N/A')}s")
        print(f"   - CORE ativo: {config.apis.core.get('is_active', 'N/A')}")
        print(f"   - Max results per query: {config.max_results_per_query}")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {{e}}")
        return False


def test_search_terms():
    """Testa se os termos de busca foram carregados corretamente."""
    print("🔍 Testando termos de busca...")

    try:
        queries = get_all_queries()
        print(f"✅ Termos de busca carregados:")
        print(f"   - Total de combinações: {len(queries)}")
        print(f"   - Primeiras 3 combinações:")
        for i, query in enumerate(queries[:3]):
            print(f"     {i+1}. {query}")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar termos de busca: {{e}}")
        return False


def test_pipeline(limit_queries: int = None):
    """Testa o pipeline melhorado."""
    print("🚀 Testando pipeline melhorado...")

    try:
        print("🔍 Debugando inicialização do pipeline...")
        config = load_config()
        print(f"   - Tipo da config: {type(config)}")
        print(f"   - Tem database: {hasattr(config, 'database')}")
        if hasattr(config, 'database'):
            print(f"   - Tipo database: {type(config.database)}")
            print(f"   - Database path: {config.database.db_path}")
        
        pipeline = ImprovedSystematicReviewPipeline(limit_queries=limit_queries)
        print(f"✅ Pipeline inicializado com sucesso (limite de queries: {limit_queries or 'Nenhum'})")

        # Executar pipeline (pode demorar)
        print("⏳ Executando pipeline (pode demorar alguns minutos)...")
        results = pipeline.run_complete_pipeline()

        if results is None or results.empty:
            print("⚠️ O pipeline foi executado, mas não retornou resultados.")
            # Considerar isso uma falha se esperamos resultados
            return False

        print(f"✅ Pipeline executado com sucesso:")
        print(f"   - Total de artigos: {len(results)}")
        print(f"   - Colunas: {list(results.columns)}")

        return True
    except Exception as e:
        print(f"❌ Erro ao executar pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal de teste."""
    parser = argparse.ArgumentParser(
        description="Testa as correções implementadas no pipeline de revisão sistemática."
    )
    parser.add_argument(
        "--limit-queries",
        type=int,
        default=None,
        help="Limita o número de queries a serem processadas para um teste rápido."
    )
    args = parser.parse_args()

    print("🧪 Iniciando testes das correções implementadas...")
    print("=" * 60)

    # O teste de pipeline é o mais importante e demorado.
    # Os outros são verificações rápidas de sanidade.
    config_ok = test_configuration()
    terms_ok = test_search_terms()

    if not config_ok or not terms_ok:
        print("\n❌ Testes de pré-requisitos falharam. Abortando o teste do pipeline.")
        return

    pipeline_ok = test_pipeline(limit_queries=args.limit_queries)

    # Resumo dos resultados
    results = {
        "Configuração": config_ok,
        "Termos de Busca": terms_ok,
        "Pipeline Melhorado": pipeline_ok
    }

    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)

    passed = sum(results.values())
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✅ PASSOU" if passed_test else "❌ FALHOU"
        print(f"{test_name}: {status}")

    print(f"\nResultado geral: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 Todos os testes foram concluídos com sucesso!")
    else:
        print("⚠️ Alguns testes falharam.")


if __name__ == "__main__":
    import argparse
    main()
