from __future__ import annotations

import argparse
import logging
import sys
import subprocess
from pathlib import Path

# Fix imports when running as script (not as module)
if __name__ == "__main__" and __package__ is None:
    # Add parent directory to path so we can import from src
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

import pandas as pd

from .config import load_config
from .db import get_statistics, init_db, read_papers, save_papers
from .database.manager import DatabaseManager
from .pipeline.run import SystematicReviewPipeline
from .analysis.deep_review_analysis import DeepReviewAnalyzer
from .exports.bibtex import export_bibtex_by_category
from .cli_audit import list_suspects, bulk_exclude, load_dois_from_csv
from .validation.reproducibility import generate_manifest
# Módulo de validações pode ter sido removido; importar de forma resiliente
try:
    from .pipelines.validations import (
        validate_exports_report,
        check_exports_consistency,
        verify_papers as vp_internal,
        regenerate_summary_from_db,
        diagnose_included as diag_internal,
    )
except Exception as import_err:  # pragma: no cover - proteção em runtime
    logger = logging.getLogger(__name__)
    logger.warning(
        "Modulo pipelines.validations ausente: algumas operações de auditoria estarão indisponíveis."
    )
    validate_exports_report = None
    check_exports_consistency = None
    vp_internal = None
    regenerate_summary_from_db = None
    diag_internal = None

# Import cross-audit functionality
import importlib.util
_audit_script = Path(__file__).resolve().parents[1] / "scripts" / "cross_audit.py"
if _audit_script.exists():
    spec = importlib.util.spec_from_file_location("cross_audit_module", _audit_script)
    _cross_audit = importlib.util.module_from_spec(spec)
    sys.modules["cross_audit_module"] = _cross_audit
    spec.loader.exec_module(_cross_audit)
    compute_db_metrics = _cross_audit.compute_db_metrics
    compute_export_metrics = _cross_audit.compute_export_metrics
    parse_ptc_numbers = _cross_audit.parse_ptc_numbers
    build_markdown = _cross_audit.build_markdown
    PTC_RESULTS = _cross_audit.PTC_RESULTS
    LOGS_DIR = _cross_audit.LOGS_DIR
else:
    compute_db_metrics = None

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
    # Note: strict require_education_term is now the default in config
    # The CLI exposes `--skip-post-filter` to disable the post-collection filter for experiments
    # Create DatabaseManager with explicit config to ensure DB path consistency
    db_manager = DatabaseManager(cfg)
    pipeline = SystematicReviewPipeline(cfg)

    # Configurações personalizadas
    apis = getattr(ns, 'apis', ["semantic_scholar", "openalex", "crossref", "core"])
    limit_per_query = getattr(ns, 'limit_per_query', 50)
    min_score = getattr(ns, 'min_score', 4.0)

    print(f"🔧 Configuração:")
    print(f"  APIs: {', '.join(apis)}")
    print(f"  Limite por query: {limit_per_query}")
    print(f"  Score mínimo: {min_score}")
    # Decide keep/cleanup behavior (default: keep True unless cleanup explicitly requested)
    keep_artifacts = True
    if hasattr(ns, 'cleanup_analysis') and ns.cleanup_analysis:
        keep_artifacts = False
    if hasattr(ns, 'keep_analysis_artifacts') and ns.keep_analysis_artifacts:
        keep_artifacts = True

    print(f"  Skip audit filter: {getattr(ns, 'skip_audit_filter', False)}")
    print(f"  Keep analysis artifacts: {keep_artifacts}")

    # Executar pipeline completo usando o método centralizado (KISS)
    try:
        pipeline.run_full_pipeline(
            search_queries=None,
            export=True,
            min_relevance_score=min_score,
            skip_audit_filter=bool(getattr(ns, 'skip_audit_filter', False)),
            keep_analysis_artifacts=keep_artifacts,
        )

        # Garantir que papers foram salvos (run_full_pipeline já chama save_papers)
        print(f"💾 Papers processados e salvos no banco de dados: {len(pipeline.results)}")

        # Persistir análises usando IDs reais dos papers salvos (usa db_manager criado acima)
        try:
            analysis_count = 0
            # Buscar papers salvos com DOI/título para mapear IDs reais
            import sqlite3
            cfg_path = cfg.database.db_path
            conn = sqlite3.connect(cfg_path)
            cursor = conn.cursor()

            for idx, row in pipeline.results.iterrows():
                if pd.notna(row.get('relevance_score')):
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
                        analysis_results = {
                            'relevance_score': float(row.get('relevance_score', 0)),
                            'comp_techniques': row.get('comp_techniques'),
                            'study_type': row.get('study_type'),
                            'eval_methods': row.get('eval_methods'),
                            'selection_stage': row.get('selection_stage')
                        }

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
                'included_papers': len(pipeline.results[pipeline.results['selection_stage'] == 'included']),
                'dedup_stats': getattr(pipeline.results, 'attrs', {}).get('dedup_stats', {})
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

        export_files = pipeline.export_results(keep_analysis_artifacts=keep_artifacts)

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

    # Full-text extraction integration (replaces separate deep-analysis command)
    fulltext_stats = None
    if hasattr(ns, 'fetch_fulltext') and ns.fetch_fulltext:
        print("\n🔬 Iniciando extração de texto completo...")
        only_missing = hasattr(ns, 'only_missing') and ns.only_missing

        try:
            analyzer = DeepReviewAnalyzer(db_path=cfg.database.db_path, config=cfg)
            # Use standard exports directory structure
            analyzer.output_dir = Path(cfg.database.exports_dir)

            # Carregar apenas papers únicos incluídos antes da extração
            try:
                analyzer.load_included_papers()
                print(f"📄 Papers únicos incluídos carregados para extração: {len(analyzer.papers)}")
            except Exception as e:
                print(f"⚠️ Falha ao carregar subconjunto incluído (usando DataFrame completo): {e}")

            # Extract full texts (updates database and returns results)
            extraction_results = analyzer.fetch_full_text(only_missing=only_missing)

            # Reload dataframe after extraction to get updated full_text field
            df = read_papers(cfg)

            # Calculate statistics for report generation
            total = len(extraction_results)
            extracted = sum(1 for p in extraction_results if p.get('full_text'))
            coverage_pct = (extracted / total * 100) if total > 0 else 0

            # Count failure reasons
            failure_counts = {}
            for paper in extraction_results:
                if not paper.get('full_text'):
                    reasons = paper.get('pdf_failure_reasons', ['unknown'])
                    for reason in reasons:
                        failure_counts[reason] = failure_counts.get(reason, 0) + 1

            # Sort by frequency
            top_failures = sorted(failure_counts.items(), key=lambda x: x[1], reverse=True)[:5]

            fulltext_stats = {
                'total_papers': total,
                'extracted': extracted,
                'failed': total - extracted,
                'coverage_pct': coverage_pct,
                'top_failures': top_failures,
                'extraction_results': extraction_results
            }

            print(f"✅ Extração concluída: {extracted}/{total} papers ({coverage_pct:.1f}%)")

        except Exception as e:
            print(f"⚠️ Erro durante extração de texto completo: {e}")
            logger.error(f"Full-text extraction failed: {e}", exc_info=True)

    from .exports.excel import export_complete_review

    # Calcular estatísticas PRISMA para visualizações
    # IMPORTANTE: Deixar export_complete_review calcular as stats corretamente do DataFrame
    # O cli apenas passa None para stats, e a função export usa _compute_prisma_stats_from_df
    stats = None

    # Debug: distribuição de estágios no DataFrame completo
    try:
        if "selection_stage" in df.columns:
            stage_dist = df["selection_stage"].value_counts().to_dict()
            logger.info(f"📊 Distribuição estágios: {stage_dist}")

        if "status" in df.columns:
            status_dist = df["status"].value_counts().to_dict()
            logger.info(f"📋 Distribuição status: {status_dist}")
    except Exception as e:
        logger.debug(f"Could not compute stage distribution: {e}")

    output_dir = Path(ns.output) if hasattr(ns, 'output') and ns.output else None
    files = export_complete_review(df, output_dir=output_dir, fulltext_stats=fulltext_stats)

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


def cmd_export_bibtex(ns: argparse.Namespace) -> None:
    """
    Exporta referências bibliográficas em formato BibTeX.

    Gera múltiplos arquivos organizados por categoria:
    - all_papers.bib: Todos os papers
    - included_papers.bib: Apenas incluídos
    - high_relevance.bib: Score >= 7.0
    - technique_*.bib: Separados por técnica
    """
    cfg = load_config()
    df = read_papers(cfg)

    if df.empty:
        print("❌ Nenhum paper encontrado no banco")
        return

    # Filtrar apenas incluídos se solicitado
    if hasattr(ns, 'included_only') and ns.included_only:
        if 'selection_stage' in df.columns:
            df = df[df['selection_stage'] == 'included']
            print(f"📋 Filtrando apenas papers incluídos: {len(df)} papers")

    cfg = load_config()
    output_dir = Path(ns.output) if hasattr(ns, 'output') and ns.output else Path(cfg.database.exports_dir) / "references"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📚 Gerando arquivos BibTeX...")
    print(f"📁 Diretório de saída: {output_dir}")

    files = export_bibtex_by_category(df, output_dir)

    print(f"\n✅ Exportação BibTeX concluída!")
    print(f"📄 {len(files)} arquivos gerados:")
    for category, path in files.items():
        file_size = path.stat().st_size / 1024  # KB
        print(f"  {category}: {path.name} ({file_size:.1f} KB)")


def cmd_audit(ns: argparse.Namespace) -> None:
    """
    Executa auditoria cruzada DB → Exports → PTC.

    Valida consistência entre:
    - SQLite DB (ground truth)
    - research/exports/ (CSV, BibTeX)
    - results/ptc/ (LaTeX documentado)

    Gera relatórios em:
    - research/logs/audit_report.json
    - research/logs/audit_report.md
    """
    if compute_db_metrics is None:
        print("❌ Módulo cross_audit não disponível")
        return

    cfg = load_config()
    if hasattr(ns, 'db') and ns.db:
        cfg.database.db_path = str(Path(ns.db).resolve())

    db = DatabaseManager(cfg)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    print("🔍 Executando auditoria cruzada...")
    print(f"📁 DB: {cfg.database.db_path}")
    print(f"📁 Logs: {LOGS_DIR}")

    dbm = compute_db_metrics(db)
    exp = compute_export_metrics()
    ptc = parse_ptc_numbers(PTC_RESULTS)

    # JSON report
    import json
    from dataclasses import asdict
    json_report = {
        "db": asdict(dbm),
        "exports": asdict(exp),
        "ptc": {"parsed": ptc.parsed, "numbers": ptc.numbers},
    }
    json_path = LOGS_DIR / "audit_report.json"
    json_path.write_text(json.dumps(json_report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Markdown report
    md = build_markdown(dbm, exp, ptc)
    md_path = LOGS_DIR / "audit_report.md"
    md_path.write_text(md, encoding="utf-8")

    print(f"\n✅ Auditoria concluída!")
    print(f"📄 Relatórios gerados:")
    print(f"  - {json_path}")
    print(f"  - {md_path}")

    # Print summary
    print(f"\n📊 Resumo:")
    print(
        f"  DB: {dbm.total_identified} identificados, "
        f"{dbm.included_unique} incluídos no estágio final "
        "(sem flag operacional)"
    )
    print(f"  Exports: {exp.bib_included_entries} BibTeX entries")
    print(f"  PTC: {'parsed OK' if ptc.parsed else 'não encontrado'}")

    # Check consistency
    mismatches = []
    if dbm.included_unique != exp.bib_included_entries:
        mismatches.append(f"included_unique ({dbm.included_unique}) != bib_entries ({exp.bib_included_entries})")
    if exp.csv_included_unique and dbm.included_unique != exp.csv_included_unique:
        mismatches.append(f"included_unique ({dbm.included_unique}) != csv_included ({exp.csv_included_unique})")

    if mismatches:
        print(f"\n⚠️  Inconsistências detectadas:")
        for m in mismatches:
            print(f"  - {m}")
    else:
        print(f"\n✅ Todos os números estão consistentes!")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def cmd_diagnose_included(ns: argparse.Namespace) -> None:
    """Diagnostica por que um paper foi incluído (usa o módulo interno)."""
    if diag_internal is None:
        print("❌ Modulo pipelines.validations ausente; restaure-o para usar diagnose-included")
        return
    if not getattr(ns, 'title', None):
        print("❌ Informe --title para diagnosticar um paper")
        return
    print("🩺 Diagnosticando paper incluído…")
    try:
        result = diag_internal(ns.title)
        if 'error' in result:
            print(f"⚠️  {result['error']}")
            return
        print("\n📌 Resultado:")
        print(f"  matched_title: {result.get('matched_title')}")
        print(f"  doi: {result.get('doi')}")
        print(f"  score: {result.get('score')}")
        print(f"  selection_stage: {result.get('selection_stage')}")
        print(f"  status: {result.get('status')}")
        if result.get('exclusion_reason'):
            print(f"  exclusion_reason: {result.get('exclusion_reason')}")
    except Exception as e:
        print(f"❌ Erro ao diagnosticar: {e}")


def cmd_validate_exports(_: argparse.Namespace) -> None:
    """Valida DB ↔ CSV ↔ summary.json usando módulo interno e grava JSON."""
    if validate_exports_report is None:
        print("❌ Modulo pipelines.validations ausente; restaure-o para usar validate-exports")
        return
    print("🔎 Validando exports (DB ↔ CSV ↔ summary.json)…")
    try:
        data = validate_exports_report()
        diffs = data.get("diffs", {})
        print("\n📊 Resumo diffs:")
        print(
            f"  total: DB={diffs.get('total',{}).get('db')} "
            f"CSV={diffs.get('total',{}).get('csv')} "
            f"SUM={diffs.get('total',{}).get('summary')}"
        )
        inc = diffs.get('included', {})
        print(
            f"  included: DB={inc.get('db')} "
            f"CSV={inc.get('csv')} "
            f"SUM_PRISMA={inc.get('summary_prisma_included')}"
        )
        # salvar saída no logs
        import json as _json
        logs = _repo_root() / "research" / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        (logs / "validate_exports_report.json").write_text(_json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n📝 Relatório JSON salvo em {logs / 'validate_exports_report.json'}")
    except Exception as e:
        print(f"❌ Erro ao validar exports: {e}")


def cmd_check_exports(_: argparse.Namespace) -> None:
    """Checa consistência de exports usando o módulo interno (inclui HTML)."""
    if check_exports_consistency is None:
        print("❌ Modulo pipelines.validations ausente; restaure-o para usar check-exports")
        return
    print("🧮 Checando consistência de exports (inclui HTML reports)…")
    try:
        out_path, content = check_exports_consistency()
        print(content)
        print(f"\n📝 Relatório salvo em {out_path}")
    except Exception as e:
        print(f"❌ Erro ao checar exports: {e}")


def cmd_verify_papers(ns: argparse.Namespace) -> None:
    """Checagens de qualidade do CSV de papers usando o módulo interno."""
    if vp_internal is None:
        print("❌ Modulo pipelines.validations ausente; restaure-o para usar verify-papers")
        return
    csv_path = Path(ns.csv) if getattr(ns, 'csv', None) else _repo_root() / "research" / "exports" / "analysis" / "papers.csv"
    out_path = Path(ns.out) if getattr(ns, 'out', None) else _repo_root() / "research" / "logs" / "verify_papers_report.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("🧪 Verificando CSV de papers…")
    try:
        summary = vp_internal(csv_path, out_path)
        print("📊 Resumo:")
        for k in [
            "total",
            "duplicate_doi_rows",
            "duplicate_title_rows",
            "missing_doi",
            "missing_abstract",
            "likely_irrelevant",
        ]:
            print(f"  {k}: {summary.get(k)}")
        print(f"📄 Relatório: {out_path}")
    except Exception as e:
        print(f"❌ Erro ao verificar CSV: {e}")


def cmd_regenerate_summary(_: argparse.Namespace) -> None:
    """Regenera summary.json a partir do DB canônico (módulo interno)."""
    if regenerate_summary_from_db is None:
        print("❌ Modulo pipelines.validations ausente; restaure-o para usar regenerate-summary")
        return
    print("♻️  Regenerando summary.json a partir do DB…")
    try:
        out = regenerate_summary_from_db()
        print(f"✅ summary.json atualizado em: {out}")
    except Exception as e:
        print(f"❌ Erro ao regenerar summary.json: {e}")


def cmd_generate_manifest(_: argparse.Namespace) -> None:
    """Gera o manifesto versionado do snapshot sem versionar o SQLite."""
    try:
        output = generate_manifest()
        print(f"✅ Manifesto de reprodutibilidade atualizado em: {output}")
    except Exception as e:
        print(f"❌ Erro ao gerar manifesto de reprodutibilidade: {e}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ccw-rs",
        description="CLI da revisão sistemática com banco SQLite e visualizações",
    )
    # Global override for DB path (useful to point at a copied .sqlite file)
    p.add_argument("--db", help="Path to SQLite DB to use (overrides config)")
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
    p_pipeline.add_argument("--skip-audit-filter", action="store_true",
                           help="Skip the post-collection auditable filter (for experiments)")
    p_pipeline.add_argument("--keep-analysis-artifacts", action="store_true",
                           help="Force keeping analysis artifacts (default behavior)")
    p_pipeline.add_argument("--cleanup-analysis", action="store_true",
                           help="Cleanup analysis artifacts after export (overrides default)")
    p_pipeline.set_defaults(func=cmd_run_pipeline)

    # Comando export
    p_export = sub.add_parser("export", help="Exporta dados com relatórios e visualizações")
    p_export.add_argument("-o", "--output", help="Diretório de saída")
    p_export.add_argument("--fetch-fulltext", action="store_true", help="Extrair texto completo dos PDFs antes de exportar")
    p_export.add_argument("--only-missing", action="store_true", help="Com --fetch-fulltext, processar apenas papers sem full_text")
    p_export.set_defaults(func=cmd_export)

    # Comando normalize-prisma
    p_norm = sub.add_parser("normalize-prisma", help="Normaliza estágios PRISMA legados no banco")
    p_norm.set_defaults(func=cmd_normalize_prisma)

    # Comando export-bibtex
    p_bib = sub.add_parser("export-bibtex", help="Exporta referências bibliográficas em formato BibTeX")
    p_bib.add_argument("-o", "--output", help="Diretório de saída (default: research/exports/references)")
    p_bib.add_argument("--included-only", action="store_true",
                       help="Exportar apenas papers incluídos")
    p_bib.set_defaults(func=cmd_export_bibtex)

    # Comando list-suspects
    p_ls = sub.add_parser("list-suspects", help="List potential exclusion candidates for manual review")
    p_ls.add_argument("--min-relevance", type=float, default=4.0, help="Maximum relevance score to consider suspect (default: 4.0)")
    p_ls.add_argument("--no-require-edu", dest="require_edu", action="store_false", help="Do not require edu_approach to be present")
    p_ls.add_argument("--limit", type=int, default=100, help="Limit number of suspects returned")
    p_ls.add_argument("-o", "--output", help="Optional CSV path to write suspects")
    p_ls.set_defaults(func=lambda ns: cmd_list_suspects(ns))

    # Comando exclude
    p_ex = sub.add_parser("exclude", help="Bulk exclude papers by DOI or title and persist reason to DB")
    p_ex.add_argument("--dois", nargs="+", help="List of DOIs or titles to exclude (space separated)")
    p_ex.add_argument("--csv", help="Path to CSV with a 'doi' or 'title' column to exclude")
    p_ex.add_argument("--reason", required=True, help="Reason for exclusion to persist in DB")
    p_ex.add_argument("--stage", default="screening", help="Selection stage to set (default: screening)")
    p_ex.add_argument("--dry-run", action="store_true", help="Show how many rows would be updated without committing changes")
    p_ex.add_argument("--yes", action="store_true", help="Apply changes without interactive confirmation")
    p_ex.set_defaults(func=lambda ns: cmd_exclude(ns))

    # Comando audit
    p_audit = sub.add_parser("audit", help="Validação cruzada DB → Exports → PTC com relatório de consistência")
    p_audit.set_defaults(func=cmd_audit)

    # Comando diagnose-included
    p_diag = sub.add_parser("diagnose-included", help="Diagnostica por que um paper foi incluído (usa título parcial)")
    p_diag.add_argument("--title", required=True, help="Título (ou parte dele)")
    p_diag.set_defaults(func=cmd_diagnose_included)

    # Comando validate-exports
    p_valexp = sub.add_parser("validate-exports", help="Valida DB ↔ CSV ↔ summary.json e grava JSON em logs")
    p_valexp.set_defaults(func=cmd_validate_exports)

    # Comando check-exports
    p_chkexp = sub.add_parser("check-exports", help="Checa consistência de exports (inclui parsing de HTML reports)")
    p_chkexp.set_defaults(func=cmd_check_exports)

    # Comando verify-papers
    p_vp = sub.add_parser("verify-papers", help="Verifica duplicatas/irrelevâncias no CSV de papers")
    p_vp.add_argument("--csv", help="Caminho do CSV de input (default: research/exports/analysis/papers.csv)")
    p_vp.add_argument("--out", help="Caminho do relatório CSV (default: research/logs/verify_papers_report.csv)")
    p_vp.set_defaults(func=cmd_verify_papers)

    # Comando regenerate-summary
    p_reg = sub.add_parser("regenerate-summary", help="Regenera research/exports/reports/summary.json a partir do DB")
    p_reg.set_defaults(func=cmd_regenerate_summary)

    # Comando generate-manifest
    p_manifest = sub.add_parser(
        "generate-manifest",
        help="Gera o manifesto do snapshot e hashes dos artefatos versionados",
    )
    p_manifest.set_defaults(func=cmd_generate_manifest)

    return p

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    ns = parser.parse_args(argv)
    # If the user passed a DB override, expose it via env var so load_config() can pick it up
    if hasattr(ns, 'db') and ns.db:
        import os
        os.environ['CCW_DB_PATH'] = str(ns.db)
    ns.func(ns)


def cmd_list_suspects(ns: argparse.Namespace) -> None:
    cfg = load_config()
    suspects = list_suspects(cfg, min_relevance=getattr(ns, 'min_relevance', 3.0), require_edu=getattr(ns, 'require_edu', True), limit=getattr(ns, 'limit', 100))
    if suspects.empty:
        print("No suspects found")
        return
    # Print a compact table
    cols = [c for c in ['doi', 'title', 'year', 'relevance_score', 'edu_approach', 'selection_stage', 'status'] if c in suspects.columns]
    print(suspects[cols].to_string(index=False))
    if hasattr(ns, 'output') and ns.output:
        out = Path(ns.output)
        suspects.to_csv(out, index=False)
        print(f"Wrote suspects CSV to: {out}")


def cmd_exclude(ns: argparse.Namespace) -> None:
    cfg = load_config()
    dois = []
    if getattr(ns, 'dois', None):
        dois.extend(ns.dois)
    if getattr(ns, 'csv', None):
        path = Path(ns.csv)
        if not path.exists():
            print(f"CSV not found: {path}")
            return
        loaded = load_dois_from_csv(path)
        dois.extend(loaded)

    if not dois:
        print("No DOIs or titles provided to exclude")
        return

    # First, compute how many would be affected (dry-run)
    would_update = bulk_exclude(dois, ns.reason, cfg=cfg, selection_stage=getattr(ns, 'stage', 'screening'), dry_run=True)
    if ns.dry_run:
        print(f"Dry-run: {would_update} rows would be updated (no changes applied)")
        return

    # Confirm with user unless --yes provided
    if not getattr(ns, 'yes', False):
        print(f"About to exclude {would_update} papers with reason: '{ns.reason}' and stage: '{getattr(ns,'stage','screening')}'")
        ans = input("Proceed? [y/N]: ")
        if not ans.lower().startswith('y'):
            print("Aborted by user")
            return

    updated = bulk_exclude(dois, ns.reason, cfg=cfg, selection_stage=getattr(ns, 'stage', 'screening'), dry_run=False)
    print(f"Applied exclusions (rows updated): {updated}")

if __name__ == "__main__":
    main()
