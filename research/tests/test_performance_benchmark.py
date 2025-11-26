#!/usr/bin/env python3
"""
Teste de benchmark para medir performance do pipeline.
"""

import sys
import time
import psutil
import os
from pathlib import Path
from typing import Dict, List

# Adicionar o diretório raiz do projeto ao path


from src.pipeline.run import SystematicReviewPipeline


class PerformanceBenchmark:
    """Benchmark completo de performance do pipeline."""
    
    def __init__(self):
        self.metrics = {}
        self.process = psutil.Process(os.getpid())
    
    def measure_memory_usage(self) -> Dict[str, float]:
        """Mede o uso de memória atual."""
        memory_info = self.process.memory_info()
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Memória física
            'vms_mb': memory_info.vms / 1024 / 1024,  # Memória virtual
        }
    
    def measure_cpu_usage(self) -> float:
        """Mede o uso de CPU."""
        return self.process.cpu_percent()
    
    def benchmark_pipeline_scaling(self) -> Dict[str, any]:
        """Testa performance com diferentes números de queries."""
        print("Executando benchmark de escalabilidade...")
        
        query_limits = [1, 2, 5, 10, 20]
        results = {}
        
        for limit in query_limits:
            print(f"\nTestando com {limit} queries...")
            
            # Resetar métricas
            start_memory = self.measure_memory_usage()
            start_time = time.time()
            
            try:
                pipeline = SystematicReviewPipeline()
                # Gerar queries limitadas
                queries = pipeline.generate_search_queries()[:limit]
                df_results = pipeline.run_full_pipeline(search_queries=queries, export=False)
                
                # Métricas finais
                end_time = time.time()
                end_memory = self.measure_memory_usage()
                
                execution_time = end_time - start_time
                memory_delta = end_memory['rss_mb'] - start_memory['rss_mb']
                
                results[limit] = {
                    'execution_time': execution_time,
                    'articles_collected': len(df_results),
                    'memory_used_mb': memory_delta,
                    'articles_per_second': len(df_results) / execution_time if execution_time > 0 else 0,
                    'queries_per_second': limit / execution_time if execution_time > 0 else 0
                }
                
                print(f"OK {limit} queries: {execution_time:.2f}s, {len(df_results)} artigos, {memory_delta:.1f}MB")
                
            except Exception as e:
                print(f"ERRO com {limit} queries: {e}")
                results[limit] = {'error': str(e)}
        
        return results
    
    def benchmark_api_performance(self) -> Dict[str, any]:
        """Testa performance individual de cada API."""
        print("🌐 Executando benchmark de APIs...")
        
        # Testar com uma query simples através do pipeline
        api_metrics = {}
        test_query = ["mathematics education AND adaptive learning"]
        apis_to_test = ["semantic_scholar", "openalex", "crossref", "core"]
        
        for api_name in apis_to_test:
            print(f"\n📡 Testando API: {api_name}")
            
            start_time = time.time()
            try:
                pipeline = SystematicReviewPipeline()
                results = pipeline.collect_data(queries=test_query, apis=[api_name], limit_per_query=5)
                
                end_time = time.time()
                count = len(results) if results is not None else 0
                
                api_metrics[api_name] = {
                    'response_time': end_time - start_time,
                    'results_count': count,
                    'results_per_second': count / (end_time - start_time) if (end_time - start_time) > 0 else 0,
                    'status': 'success'
                }
                
                print(f"✅ {api_name}: {end_time - start_time:.2f}s, {count} resultados")
                
            except Exception as e:
                api_metrics[api_name] = {
                    'error': str(e),
                    'status': 'failed'
                }
                print(f"❌ {api_name}: {e}")
        
        return api_metrics
    
    def benchmark_cache_performance(self) -> Dict[str, any]:
        """Testa performance do sistema de cache."""
        print("💾 Executando benchmark de cache...")
        
        cache_metrics = {}
        
        # Primeira execução (sem cache)
        print("\n🔥 Primeira execução (populando cache)...")
        start_time = time.time()
        pipeline1 = SystematicReviewPipeline()
        queries = pipeline1.generate_search_queries()[:2]
        results1 = pipeline1.run_full_pipeline(search_queries=queries, export=False)
        first_execution_time = time.time() - start_time
        
        # Segunda execução (com cache)
        print("\n⚡ Segunda execução (usando cache)...")
        start_time = time.time()
        pipeline2 = SystematicReviewPipeline()
        results2 = pipeline2.run_full_pipeline(search_queries=queries, export=False)
        second_execution_time = time.time() - start_time
        
        # Calcular métricas
        speedup = first_execution_time / second_execution_time if second_execution_time > 0 else 0
        
        cache_metrics = {
            'first_execution_time': first_execution_time,
            'second_execution_time': second_execution_time,
            'speedup_factor': speedup,
            'cache_efficiency': ((first_execution_time - second_execution_time) / first_execution_time) * 100 if first_execution_time > 0 else 0
        }
        
        print(f"✅ Cache speedup: {speedup:.1f}x mais rápido")
        print(f"✅ Eficiência do cache: {cache_metrics['cache_efficiency']:.1f}%")
        
        return cache_metrics
    
    def run_full_benchmark(self) -> Dict[str, any]:
        """Executa benchmark completo."""
        print("🏁 Iniciando benchmark completo de performance...")
        print("=" * 70)
        
        # Coletar informações do sistema
        system_info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / 1024**3,
            'python_version': sys.version,
            'platform': sys.platform
        }
        
        print(f"💻 Sistema:")
        print(f"   - CPUs: {system_info['cpu_count']}")
        print(f"   - RAM: {system_info['memory_total_gb']:.1f}GB")
        print(f"   - Platform: {system_info['platform']}")
        
        # Executar benchmarks
        benchmarks = {}
        
        try:
            benchmarks['scaling'] = self.benchmark_pipeline_scaling()
        except Exception as e:
            print(f"❌ Erro no benchmark de escalabilidade: {e}")
            benchmarks['scaling'] = {'error': str(e)}
        
        try:
            benchmarks['apis'] = self.benchmark_api_performance()
        except Exception as e:
            print(f"❌ Erro no benchmark de APIs: {e}")
            benchmarks['apis'] = {'error': str(e)}
        
        try:
            benchmarks['cache'] = self.benchmark_cache_performance()
        except Exception as e:
            print(f"❌ Erro no benchmark de cache: {e}")
            benchmarks['cache'] = {'error': str(e)}
        
        # Resultado final
        final_results = {
            'system_info': system_info,
            'benchmarks': benchmarks,
            'timestamp': time.time()
        }
        
        self.print_summary(final_results)
        
        return final_results
    
    def print_summary(self, results: Dict[str, any]):
        """Imprime resumo dos resultados."""
        print("\n" + "=" * 70)
        print("📊 RESUMO DO BENCHMARK")
        print("=" * 70)
        
        # Resumo de escalabilidade
        if 'scaling' in results['benchmarks'] and 'error' not in results['benchmarks']['scaling']:
            scaling = results['benchmarks']['scaling']
            print(f"\n🔍 Escalabilidade:")
            
            for queries, metrics in scaling.items():
                if 'error' not in metrics:
                    print(f"   - {queries:2d} queries: {metrics['execution_time']:6.2f}s, "
                          f"{metrics['articles_collected']:3d} artigos, "
                          f"{metrics['articles_per_second']:5.1f} art/s")
        
        # Resumo de APIs
        if 'apis' in results['benchmarks'] and 'error' not in results['benchmarks']['apis']:
            apis = results['benchmarks']['apis']
            print(f"\n🌐 Performance das APIs:")
            
            for api_name, metrics in apis.items():
                if metrics['status'] == 'success':
                    print(f"   - {api_name:15s}: {metrics['response_time']:6.2f}s, "
                          f"{metrics['results_count']:3d} resultados")
                else:
                    print(f"   - {api_name:15s}: ERRO")
        
        # Resumo de cache
        if 'cache' in results['benchmarks'] and 'error' not in results['benchmarks']['cache']:
            cache = results['benchmarks']['cache']
            print(f"\n💾 Eficiência do Cache:")
            print(f"   - Speedup: {cache['speedup_factor']:.1f}x mais rápido")
            print(f"   - Eficiência: {cache['cache_efficiency']:.1f}%")
        
        print(f"\n✅ Benchmark concluído!")


def main():
    """Função principal do benchmark."""
    print("Benchmark de Performance do Pipeline")
    print("Este teste pode demorar alguns minutos...\n")
    
    benchmark = PerformanceBenchmark()
    results = benchmark.run_full_benchmark()
    
    # Salvar resultados
    import json
    output_file = Path("benchmark_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Resultados salvos em: {output_file}")


if __name__ == "__main__":
    main()