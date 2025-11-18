#!/usr/bin/env python3
"""
Benchmark simples de performance do pipeline.
"""

import sys
import time
import os
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.run import SystematicReviewPipeline


def run_simple_benchmark():
    """Executa benchmark simples."""
    print("=== BENCHMARK DE PERFORMANCE ===")
    print("Testando performance com diferentes configurações...\n")
    
    configs = [
        {"queries": 1, "description": "Teste mínimo"},
        {"queries": 2, "description": "Teste rápido"},
        {"queries": 5, "description": "Teste médio"}
    ]
    
    results = []
    
    for config in configs:
        print(f"Executando: {config['description']} ({config['queries']} queries)")
        
        start_time = time.time()
        try:
            pipeline = SystematicReviewPipeline()
            queries = pipeline.generate_search_queries()[:config['queries']]
            df_results = pipeline.run_full_pipeline(search_queries=queries, export=False)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                'queries': config['queries'],
                'execution_time': execution_time,
                'articles_collected': len(df_results),
                'articles_per_second': len(df_results) / execution_time if execution_time > 0 else 0,
                'status': 'success'
            }
            
            results.append(result)
            
            print(f"  - Tempo: {execution_time:.2f}s")
            print(f"  - Artigos: {len(df_results)}")
            print(f"  - Performance: {result['articles_per_second']:.1f} artigos/s")
            print("  - Status: OK\n")
            
        except Exception as e:
            result = {
                'queries': config['queries'],
                'error': str(e),
                'status': 'error'
            }
            results.append(result)
            print(f"  - ERRO: {e}\n")
    
    # Resumo
    print("=== RESUMO DO BENCHMARK ===")
    successful_tests = [r for r in results if r['status'] == 'success']
    
    if successful_tests:
        print(f"Testes bem-sucedidos: {len(successful_tests)}/{len(results)}")
        
        avg_time = sum(r['execution_time'] for r in successful_tests) / len(successful_tests)
        total_articles = sum(r['articles_collected'] for r in successful_tests)
        
        print(f"Tempo médio: {avg_time:.2f}s")
        print(f"Total de artigos coletados: {total_articles}")
        print("Pipeline está funcionando corretamente!")
    else:
        print("Nenhum teste foi bem-sucedido.")
        print("Verifique a configuração do pipeline.")
    
    return results


if __name__ == "__main__":
    run_simple_benchmark()