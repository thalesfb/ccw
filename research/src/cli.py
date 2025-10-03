from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .config import load_config
from .db import get_statistics, init_db, read_papers, save_papers
from .pipeline.run import SystematicReviewPipeline


def cmd_init_db(_: argparse.Namespace) -> None:
    cfg = load_config()
    db_path = init_db(cfg)
    print(f"Banco inicializado em: {db_path}")


def cmd_show(_: argparse.Namespace) -> None:
    cfg = load_config()
    df = read_papers(cfg)
    print(df.head(20).to_string(index=False))
    print(f"\nTotal de registros: {len(df)}")


def cmd_import_csv(ns: argparse.Namespace) -> None:
    cfg = load_config()
    csv_path = Path(ns.csv)
    if not csv_path.exists():
        raise SystemExit(f"Arquivo CSV não encontrado: {csv_path}")
    df = pd.read_csv(csv_path)
    inserted = save_papers(df, cfg)
    print(f"Inseridos {inserted} novos registros a partir de {csv_path}")


def cmd_stats(_: argparse.Namespace) -> None:
    cfg = load_config()
    stats = get_statistics(cfg)
    
    print("📊 Estatísticas do Banco de Dados")
    print("=" * 40)
    print(f"Total de papers: {stats['total_papers']}")
    
    if stats.get('by_stage'):
        print("\n📋 Por estágio de seleção:")
        for stage, count in stats['by_stage'].items():
            print(f"  {stage}: {count}")
    
    if stats.get('by_database'):
        print("\n🗃️ Por base de dados:")
        for db, count in stats['by_database'].items():
            print(f"  {db}: {count}")
    
    if stats.get('by_year'):
        print("\n📅 Por ano (últimos 10):")
        for year, count in stats['by_year'].items():
            print(f"  {year}: {count}")
    
    if stats.get('cache'):
        cache_stats = stats['cache']
        print(f"\n💾 Cache: {cache_stats['total_entries']} entradas, {cache_stats['total_hits']} hits")


def cmd_run_pipeline(ns: argparse.Namespace) -> None:
    cfg = load_config()
    pipeline = SystematicReviewPipeline(cfg)
    
    # Configurações personalizadas
    apis = getattr(ns, 'apis', ["semantic_scholar", "openalex", "crossref"])
    limit_per_query = getattr(ns, 'limit_per_query', 50)
    min_score = getattr(ns, 'min_score', 4.0)
    
    print(f"🔧 Configuração:")
    print(f"  APIs: {', '.join(apis)}")
    print(f"  Limite por query: {limit_per_query}")
    print(f"  Score mínimo: {min_score}")
    
    # Executar pipeline com configurações
    try:
        # Execução passo a passo para usar configurações customizadas
        pipeline.generate_search_queries()
        pipeline.collect_data(apis=apis, limit_per_query=limit_per_query)
        pipeline.process_data()
        pipeline.apply_selection_criteria(min_score)
        
        # Exportar resultados
        export_files = pipeline.export_results()
        
        print(f"\n✅ Pipeline concluído!")
        print(f"📄 Total processado: {len(pipeline.results)} papers")
        
        if "selection_stage" in pipeline.results.columns:
            stage_counts = pipeline.results["selection_stage"].value_counts()
            print("\n📊 Resultados por estágio:")
            for stage, count in stage_counts.items():
                print(f"  {stage}: {count}")
        
        # Mostrar arquivos gerados
        if isinstance(export_files, dict):
            print(f"\n📁 Arquivos gerados:")
            for file_type, path in export_files.items():
                if isinstance(path, list):
                    print(f"  {file_type}: {len(path)} arquivos")
                else:
                    print(f"  {file_type}: {path}")
    
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        logger.error(f"Pipeline failed: {e}", exc_info=True)


def cmd_export(ns: argparse.Namespace) -> None:
    cfg = load_config()
    df = read_papers(cfg)
    
    if df.empty:
        print("❌ Nenhum paper encontrado no banco")
        return
    
    from .exports.excel import export_complete_review
    
    output_dir = Path(ns.output) if hasattr(ns, 'output') and ns.output else None
    files = export_complete_review(df, output_dir=output_dir)
    
    print("📊 Exportação completa realizada:")
    for file_type, path in files.items():
        if isinstance(path, list):
            print(f"  {file_type}: {len(path)} arquivos")
        else:
            print(f"  {file_type}: {path}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ccw-rs",
        description="CLI da revisão sistemática com banco SQLite e visualizações",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # Comando init-db
    p_init = sub.add_parser("init-db", help="Inicializa o banco de dados SQLite")
    p_init.set_defaults(func=cmd_init_db)

    # Comando show
    p_show = sub.add_parser("show", help="Mostra amostra dos registros na tabela papers")
    p_show.set_defaults(func=cmd_show)

    # Comando stats
    p_stats = sub.add_parser("stats", help="Mostra estatísticas do banco de dados")
    p_stats.set_defaults(func=cmd_stats)

    # Comando import-csv
    p_import = sub.add_parser("import-csv", help="Importa resultados de busca (CSV) para o banco")
    p_import.add_argument("csv", help="Caminho para o arquivo CSV com colunas incluindo 'doi'")
    p_import.set_defaults(func=cmd_import_csv)

    # Comando run-pipeline
    p_pipeline = sub.add_parser("run-pipeline", help="Executa o pipeline completo de revisão sistemática")
    p_pipeline.add_argument("--min-score", type=float, default=4.0, 
                           help="Score mínimo de relevância (padrão: 4.0)")
    p_pipeline.add_argument("--apis", nargs="+", 
                           choices=["semantic_scholar", "openalex", "crossref", "core"],
                           default=["semantic_scholar", "openalex", "crossref"],
                           help="APIs a usar na busca")
    p_pipeline.add_argument("--limit-per-query", type=int, default=50,
                           help="Limite de resultados por query por API")
    p_pipeline.set_defaults(func=cmd_run_pipeline)

    # Comando export
    p_export = sub.add_parser("export", help="Exporta dados com relatórios e visualizações")
    p_export.add_argument("-o", "--output", help="Diretório de saída")
    p_export.set_defaults(func=cmd_export)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    ns = parser.parse_args(argv)
    ns.func(ns)


if __name__ == "__main__":
    main()
