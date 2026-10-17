#!/usr/bin/env python3
"""
Script de teste para validar as correções implementadas.
"""

import sys
from pathlib import Path
import argparse
import pytest

# Adicionar o diretório raiz do projeto (research) ao path


from src.search_terms import get_all_queries
from src.config import load_config
from src.pipeline.run import SystematicReviewPipeline

def test_configuration():
    """Testa se a configuração foi carregada corretamente."""
    print("🔧 Testando configuração...")
    config = load_config()
    print(f"✅ Configuração carregada:")
    # Basic sanity assertions for configuration
    assert config is not None
    assert hasattr(config, 'apis')
    # access some common keys to ensure structure
    assert hasattr(config.apis, 'semantic_scholar')
    assert hasattr(config.apis, 'open_alex')
    assert hasattr(config.apis, 'crossref')
    assert hasattr(config.apis, 'core')
    assert hasattr(config, 'max_results_per_query')


def test_search_terms():
    """Testa se os termos de busca foram carregados corretamente."""
    print("🔍 Testando termos de busca...")
    queries = get_all_queries()
    print(f"✅ Termos de busca carregados:")
    # Basic checks
    assert queries is not None
    assert isinstance(queries, (list, tuple))
    assert len(queries) > 0
    print(f"   - Total de combinações: {len(queries)}")
    print(f"   - Primeiras 3 combinações:")
    for i, query in enumerate(queries[:3]):
        print(f"     {i+1}. {query}")


@pytest.mark.integration
def test_pipeline(limit_queries: int = None):
    """Testa o pipeline melhorado."""
    print("🚀 Testando pipeline melhorado...")
    print("🔍 Debugando inicialização do pipeline...")
    config = load_config()
    print(f"   - Tipo da config: {type(config)}")
    print(f"   - Tem database: {hasattr(config, 'database')}")
    if hasattr(config, 'database'):
        print(f"   - Tipo database: {type(config.database)}")
        print(f"   - Database path: {config.database.db_path}")

    pipeline = SystematicReviewPipeline()
    queries = None
    if limit_queries:
        queries = pipeline.generate_search_queries()[:limit_queries]
    print(f"✅ Pipeline inicializado com sucesso (limite de queries: {limit_queries or 'Nenhum'})")

    # Executar pipeline (pode demorar)
    print("⏳ Executando pipeline (pode demorar alguns minutos)...")
    results = pipeline.run_full_pipeline(search_queries=queries, export=False)

    assert results is not None, "Pipeline returned None"
    assert not getattr(results, 'empty', False), "Pipeline returned empty results"

    print(f"✅ Pipeline executado com sucesso:")
    print(f"   - Total de artigos: {len(results)}")
    print(f"   - Colunas: {list(results.columns)}")


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
    # Run tests but keep main script semantics: catch assertion failures and
    # convert them into boolean results so the CLI-friendly main() continues
    try:
        test_configuration()
        config_ok = True
    except Exception:
        config_ok = False

    try:
        test_search_terms()
        terms_ok = True
    except Exception:
        terms_ok = False

    if not config_ok or not terms_ok:
        print("\n❌ Testes de pré-requisitos falharam. Abortando o teste do pipeline.")
        return

    try:
        test_pipeline(limit_queries=args.limit_queries)
        pipeline_ok = True
    except Exception:
        pipeline_ok = False

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
