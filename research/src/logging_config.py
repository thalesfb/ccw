"""
Configuração de logs para auditoria do pipeline de revisão sistemática.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json
import traceback

class AuditLogger:
    """
    Logger especializado para auditoria do pipeline de revisão sistemática.
    """

    def __init__(self, name: str = "systematic_review", log_dir: Optional[str] = None):
        self.name = name
        # Usar config se log_dir não fornecido
        if log_dir is None:
            from .config import load_config
            cfg = load_config()
            log_dir = cfg.database.logs_dir
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configurar logger principal
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Evitar duplicação de handlers
        if not self.logger.handlers:
            self._setup_handlers()

        # Dicionário para armazenar métricas de auditoria
        self.audit_metrics = {
            "start_time": None,
            "end_time": None,
            "total_articles_collected": 0,
            "total_articles_selected": 0,
            "api_calls": {},
            "errors": [],
            "warnings": [],
            "performance_metrics": {}
        }

    def _setup_handlers(self):
        """Configura handlers de log otimizados (1 arquivo rotativo + console)."""
        # Formatter unificado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para console (apenas INFO e acima)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Rotating file handler único
        rotating_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "systematic_review.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=3,  # Mantém 3 backups (30MB total máximo)
            encoding='utf-8'
        )
        rotating_handler.setLevel(logging.DEBUG)  # Captura tudo no arquivo
        rotating_handler.setFormatter(formatter)
        self.logger.addHandler(rotating_handler)

    def start_pipeline(self, config: Dict[str, Any]):
        """Registra o início do pipeline."""
        self.audit_metrics["start_time"] = datetime.now().isoformat()

        self.logger.info("🚀 INÍCIO DO PIPELINE DE REVISÃO SISTEMÁTICA")
        self.logger.info(
            f"📋 Configuração: {json.dumps(config, indent=2, ensure_ascii=False)}")
        self.logger.info("=" * 80)

    def end_pipeline(self, results: Dict[str, Any]):
        """Registra o fim do pipeline."""
        self.audit_metrics["end_time"] = datetime.now().isoformat()

        self.logger.info("=" * 80)
        self.logger.info("✅ FIM DO PIPELINE DE REVISÃO SISTEMÁTICA")
        self.logger.info(
            f"📊 Resultados: {json.dumps(results, indent=2, ensure_ascii=False)}")

        # Salvar relatório de auditoria
        self._save_audit_report()

    def log_api_call(self, api_name: str, query: str, results_count: int,
                     response_time: float, status_code: int = 200):
        """Registra chamada de API para auditoria."""
        if api_name not in self.audit_metrics["api_calls"]:
            self.audit_metrics["api_calls"][api_name] = {
                "total_calls": 0,
                "total_results": 0,
                "total_time": 0,
                "errors": 0,
                "queries": []
            }

        api_metrics = self.audit_metrics["api_calls"][api_name]
        api_metrics["total_calls"] += 1
        api_metrics["total_results"] += results_count
        api_metrics["total_time"] += response_time
        api_metrics["queries"].append({
            "query": query,
            "results": results_count,
            "response_time": response_time,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        })

        if status_code != 200:
            api_metrics["errors"] += 1

        self.logger.info(
            f"📡 API {api_name}: '{query}' -> {results_count} resultados "
            f"({response_time:.2f}s, status={status_code})"
        )

    def log_article_collection(self, source: str, count: int, total: int):
        """Registra coleta de artigos."""
        self.audit_metrics["total_articles_collected"] += count

        self.logger.info(
            f"📥 Coleta de {source}: {count} artigos "
            f"(Total acumulado: {self.audit_metrics['total_articles_collected']})"
        )

    def log_article_selection(self, stage: str, input_count: int, output_count: int,
                              criteria: Dict[str, Any]):
        """Registra seleção de artigos."""
        self.logger.info(
            f"🎯 Seleção {stage}: {input_count} -> {output_count} artigos "
            f"(Critérios: {json.dumps(criteria, ensure_ascii=False)})"
        )

        if stage == "final":
            self.audit_metrics["total_articles_selected"] = output_count

    def log_error(self, error: Exception, context: str = "", recoverable: bool = True):
        """Registra erro para auditoria."""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "recoverable": recoverable,
            "traceback": traceback.format_exc()
        }

        self.audit_metrics["errors"].append(error_info)

        level = logging.WARNING if recoverable else logging.ERROR
        self.logger.log(
            level,
            f"❌ Erro em {context}: {type(error).__name__}: {str(error)}"
        )

        if not recoverable:
            self.logger.error(
                f"🔍 Traceback completo:\n{traceback.format_exc()}")

    def log_warning(self, message: str, context: str = ""):
        """Registra aviso para auditoria."""
        warning_info = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "context": context
        }

        self.audit_metrics["warnings"].append(warning_info)
        self.logger.warning(f"⚠️ {context}: {message}")

    def log_performance(self, operation: str, duration: float,
                        details: Optional[Dict[str, Any]] = None):
        """Registra métricas de performance."""
        if operation not in self.audit_metrics["performance_metrics"]:
            self.audit_metrics["performance_metrics"][operation] = []

        perf_data = {
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "details": details or {}
        }

        self.audit_metrics["performance_metrics"][operation].append(perf_data)

        self.logger.info(f"⏱️ Performance {operation}: {duration:.2f}s")
        if details:
            self.logger.debug(
                f"📊 Detalhes: {json.dumps(details, ensure_ascii=False)}")

    def log_data_quality(self, stage: str, data_info: Dict[str, Any]):
        """Registra informações sobre qualidade dos dados."""
        self.logger.info(
            f"📊 Qualidade de dados - {stage}: {json.dumps(data_info, ensure_ascii=False)}")

    def log_user_action(self, action: str, details: Dict[str, Any]):
        """Registra ações do usuário."""
        self.logger.info(
            f"👤 Ação do usuário: {action} - {json.dumps(details, ensure_ascii=False)}")

    def _save_audit_report(self):
        """Salva relatório completo de auditoria."""
        report_file = self.log_dir / "audit_report.json"
        self.audit_metrics["report_generated_at"] = datetime.now().isoformat()

        # Calcular duração total
        if self.audit_metrics["start_time"] and self.audit_metrics["end_time"]:
            start = datetime.fromisoformat(self.audit_metrics["start_time"])
            end = datetime.fromisoformat(self.audit_metrics["end_time"])
            duration = (end - start).total_seconds()
            self.audit_metrics["total_duration_seconds"] = duration

        # Calcular estatísticas das APIs
        for api_name, api_data in self.audit_metrics["api_calls"].items():
            if api_data["total_calls"] > 0:
                api_data["avg_response_time"] = api_data["total_time"] / \
                    api_data["total_calls"]
                api_data["avg_results_per_call"] = api_data["total_results"] / \
                    api_data["total_calls"]
                api_data["error_rate"] = api_data["errors"] / \
                    api_data["total_calls"]

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.audit_metrics, f, indent=2, ensure_ascii=False)

        self.logger.info(f"📋 Relatório de auditoria salvo: {report_file}")

        # Log resumo executivo
        self._log_executive_summary()

    def _log_executive_summary(self):
        """Log resumo executivo da auditoria."""
        self.logger.info("=" * 80)
        self.logger.info("📊 RESUMO EXECUTIVO DA AUDITORIA")
        self.logger.info("=" * 80)

        # Duração
        if "total_duration_seconds" in self.audit_metrics:
            duration = self.audit_metrics["total_duration_seconds"]
            self.logger.info(
                f"⏱️ Duração total: {duration:.2f} segundos ({duration/60:.2f} minutos)")

        # Artigos
        self.logger.info(
            f"📥 Artigos coletados: {self.audit_metrics['total_articles_collected']}")
        self.logger.info(
            f"🎯 Artigos selecionados: {self.audit_metrics['total_articles_selected']}")

        # APIs
        total_api_calls = sum(api["total_calls"]
                              for api in self.audit_metrics["api_calls"].values())
        total_api_results = sum(api["total_results"]
                                for api in self.audit_metrics["api_calls"].values())
        self.logger.info(f"📡 Total de chamadas de API: {total_api_calls}")
        self.logger.info(f"📊 Total de resultados de API: {total_api_results}")

        # Erros e avisos
        self.logger.info(
            f"❌ Total de erros: {len(self.audit_metrics['errors'])}")
        self.logger.info(
            f"⚠️ Total de avisos: {len(self.audit_metrics['warnings'])}")

        # Performance
        if self.audit_metrics["performance_metrics"]:
            self.logger.info("⏱️ Métricas de performance:")
            for operation, metrics in self.audit_metrics["performance_metrics"].items():
                if metrics:
                    avg_duration = sum(m["duration"]
                                       for m in metrics) / len(metrics)
                    self.logger.info(
                        f"   {operation}: {avg_duration:.2f}s (média)")

        self.logger.info("=" * 80)


def get_audit_logger(name: str = "systematic_review") -> AuditLogger:
    """
    Factory function para obter logger de auditoria.
    """
    return AuditLogger(name)


def setup_logging_for_module(module_name: str) -> logging.Logger:
    """
    Configura logging para um módulo específico.
    """
    logger = logging.getLogger(f"systematic_review.{module_name}")

    # Se o logger já tem handlers, não adicionar novos
    if not logger.handlers:
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Handler para arquivo
        from .config import load_config
        cfg = load_config()
        log_dir = Path(cfg.database.logs_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / f"{module_name}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)
    return logger