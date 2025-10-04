from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

import argparse
import logging

import pandas as pd

from .config import load_config
from .db import get_statistics, init_db, read_papers, save_papers
from .database.manager import DatabaseManager
from .pipeline.run import SystematicReviewPipeline

logger = logging.getLogger(__name__)

# Garantir UTF-8 no Windows - método alternativo que não quebra logging
if sys.platform == "win32":
    # Configurar variável de ambiente antes de qualquer print
    import os
    os.environ["PYTHONIOENCODING"] = "utf-8"
    # Reconfigurar stdout/stderr se ainda não estiver em UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')


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
        label_map = {
            'identification': 'Identification',
            'screening_excluded': 'Screening Excluded',
            'eligibility_excluded': 'Eligibility Excluded',
            'included': 'Included'
        }
        for stage, count in stats['by_stage'].items():
            print(f"  {label_map.get(stage, stage)}: {count}")
    
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
    apis = getattr(ns, 'apis', ["semantic_scholar", "openalex", "crossref", "core"])
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
        
        # ✅ CORREÇÃO: Salvar papers no banco após seleção PRISMA
        saved = save_papers(pipeline.results, cfg)
        print(f"💾 Salvos {saved} papers no banco de dados")
        
        # ✅ CORREÇÃO: Persistir análises usando IDs reais dos papers salvos
        try:
            db_manager = DatabaseManager()
            analysis_count = 0
            
            # Buscar papers salvos com DOI/título para mapear IDs reais
            import sqlite3
            conn = sqlite3.connect('research/systematic_review.db')
            cursor = conn.cursor()
            
            for idx, row in pipeline.results.iterrows():
                if pd.notna(row.get('relevance_score')):
                    # Buscar ID real do paper usando DOI ou título
                    doi = row.get('doi')
                    title = row.get('title', '')
                    
                    paper_id = None
                    if doi:
                        cursor.execute('SELECT id FROM papers WHERE doi = ? LIMIT 1', (doi,))
                        result = cursor.fetchone()
                        if result:
                            paper_id = result[0]
                    
                    if not paper_id and title:
                        cursor.execute('SELECT id FROM papers WHERE title = ? LIMIT 1', (title,))
                        result = cursor.fetchone()
                        if result:
                            paper_id = result[0]
                    
                    if paper_id:
                        # Preparar dados da análise
                        analysis_results = {
                            'relevance_score': float(row.get('relevance_score', 0)),
                            'comp_techniques': row.get('comp_techniques'),
                            'study_type': row.get('study_type'),
                            'eval_methods': row.get('eval_methods'),
                            'selection_stage': row.get('selection_stage')
                        }
                        
                        # Salvar análise com ID real
                        db_manager.save_analysis(
                            paper_id=paper_id,
                            analysis_type='relevance_scoring',
                            results=analysis_results,
                            confidence=float(row.get('relevance_score', 0))/10.0
                        )
                        analysis_count += 1
            
            conn.close()
            print(f"📊 Salvou {analysis_count} análises no banco de dados")
        except Exception as e:
            print(f"⚠️ Erro ao salvar análises: {e}")
        
        # ✅ CORREÇÃO: Log da execução do pipeline na tabela searches
        try:
            search_log = {
                'apis_used': apis,
                'limit_per_query': limit_per_query,
                'min_score': min_score,
                'total_papers': len(pipeline.results),
                'included_papers': len(pipeline.results[pipeline.results['selection_stage'] == 'included'])
            }
            
            db_manager.save_search_log(
                query_summary=f"Pipeline completo: {len(apis)} APIs, {limit_per_query} papers/query",
                results_summary=search_log
            )
            print(f"📝 Log da execução salvo na tabela searches")
        except Exception as e:
            print(f"⚠️ Erro ao salvar log: {e}")
        
        # Exportar resultados
        # Recarregar do banco para garantir consistência com a fonte de verdade
        try:
            df_db = read_papers(cfg)
            if not df_db.empty:
                pipeline.results = df_db
        except Exception as e:
            logger.warning(f"Falha ao recarregar dados do banco antes de exportar: {e}")

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
    
    # Calcular estatísticas PRISMA para visualizações
    stats = None
    try:
        if "selection_stage" in df.columns and "status" in df.columns:
            identification = int(len(df))
            
            # Debug: distribuição de estágios
            stage_dist = df["selection_stage"].value_counts().to_dict()
            status_dist = df["status"].value_counts().to_dict()
            logger.info(f"📊 Distribuição estágios: {stage_dist}")
            logger.info(f"📋 Distribuição status: {status_dist}")
            
            # Screening: todos que passaram triagem
            screening = int(((df["selection_stage"] == "screening") & (df["status"] != "excluded")).sum())
            screening_excluded = int(((df["selection_stage"] == "screening") & (df["status"] == "excluded")).sum())
            
            # Eligibility: todos que passaram elegibilidade
            eligibility = int(((df["selection_stage"] == "eligibility") & (df["status"] != "excluded")).sum())
            eligibility_excluded = int(((df["selection_stage"] == "eligibility") & (df["status"] == "excluded")).sum())
            
            # Included: papers finais
            included = int(((df["selection_stage"] == "included") & (df["status"] == "included")).sum())
            
            # Se não há screening no banco, assumir que todos foram direto para eligibility
            # Nesse caso, screening = identification (todos passaram triagem implicitamente)
            if screening == 0 and screening_excluded == 0:
                screening = identification
                logger.warning("⚠️ Nenhum registro em 'screening' - assumindo todos passaram triagem")
            
            logger.info(f"📈 PRISMA calculado: ident={identification}, screen={screening}, "
                       f"screen_excl={screening_excluded}, elig={eligibility}, "
                       f"elig_excl={eligibility_excluded}, incl={included}")
            
            stats = {
                "identification": identification,
                "duplicates_removed": 0,  # duplicatas tratadas antes
                "screening": screening,
                "screening_excluded": screening_excluded,
                "eligibility": eligibility,
                "eligibility_excluded": eligibility_excluded,
                "included": included,
            }
    except Exception as e:
        logger.error(f"❌ Erro ao calcular PRISMA stats: {e}", exc_info=True)
    
    output_dir = Path(ns.output) if hasattr(ns, 'output') and ns.output else None
    files = export_complete_review(df, stats=stats, output_dir=output_dir)
    
    print("📊 Exportação completa realizada:")
    for file_type, path in files.items():
        if isinstance(path, list):
            print(f"  {file_type}: {len(path)} arquivos")
        else:
            print(f"  {file_type}: {path}")


def cmd_normalize_prisma(_: argparse.Namespace) -> None:
    cfg = load_config()
    db = DatabaseManager(cfg)
    res = db.normalize_prisma_stages()
    print("🔧 Normalização PRISMA concluída:")
    print(f"  screening_excluded -> screening/status=excluded: {res['screening']}")
    print(f"  eligibility_excluded -> eligibility/status=excluded: {res['eligibility']}")



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
                           default=["semantic_scholar", "openalex", "crossref", "core"],
                           help="APIs a usar na busca")
    p_pipeline.add_argument("--limit-per-query", type=int, default=50,
                           help="Limite de resultados por query por API")
    p_pipeline.set_defaults(func=cmd_run_pipeline)

    # Comando export
    p_export = sub.add_parser("export", help="Exporta dados com relatórios e visualizações")
    p_export.add_argument("-o", "--output", help="Diretório de saída")
    p_export.set_defaults(func=cmd_export)

    # Comando normalize-prisma
    p_norm = sub.add_parser("normalize-prisma", help="Normaliza estágios PRISMA legados no banco")
    p_norm.set_defaults(func=cmd_normalize_prisma)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    ns = parser.parse_args(argv)
    ns.func(ns)


if __name__ == "__main__":
    main()
