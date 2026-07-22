"""Generate traceable LaTeX artifacts from an integrity-checked real run."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


class AcademicArtifactError(RuntimeError):
    """Raised when a run is not eligible for academic integration."""


@dataclass(frozen=True)
class AcademicArtifacts:
    model_comparison_path: Path
    data_quality_path: Path
    skill_summary_path: Path
    provenance_path: Path


MODEL_NAMES = {
    "global_probability": "Probabilidade global",
    "item_probability": "Probabilidade por item",
    "skill_probability": "Probabilidade por habilidade",
    "student_history_probability": "Histórico do estudante",
    "logistic_regression": "Regressão logística",
    "random_forest": "Random Forest",
}
LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def _latex_escape(value: object) -> str:
    text = str(value)
    return "".join(LATEX_REPLACEMENTS.get(char, char) for char in text)


def _number(value: Any, digits: int = 3) -> str:
    if value is None:
        return "--"
    number = float(value)
    if math.isnan(number) or math.isinf(number):
        return "--"
    return f"{number:.{digits}f}".replace(".", "{,}")


def _integer(value: Any) -> str:
    return f"{int(value):,}".replace(",", ".")


def _safe_artifact_path(run_dir: Path, relative: str) -> Path:
    candidate = (run_dir / relative).resolve()
    try:
        candidate.relative_to(run_dir.resolve())
    except ValueError as exc:
        raise AcademicArtifactError(
            f"artifact path escapes the run directory: {relative}"
        ) from exc
    return candidate


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _load_and_validate_run(run_manifest_path: Path) -> tuple[dict[str, Any], Path]:
    try:
        manifest = json.loads(run_manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AcademicArtifactError(f"unable to read run manifest: {exc}") from exc
    run_dir = run_manifest_path.parent.resolve()
    if manifest.get("dataset", {}).get("raw_data_included") is not False:
        raise AcademicArtifactError("run manifest must explicitly exclude raw data")
    configuration = manifest.get("configuration", {})
    if configuration.get("binary_alert_enabled"):
        raise AcademicArtifactError(
            "binary alerts must remain disabled before academic integration"
        )
    if configuration.get("ordinal_levels_enabled"):
        raise AcademicArtifactError(
            "ordinal levels must remain disabled before threshold validation"
        )
    commit = str(manifest.get("git_commit", ""))
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise AcademicArtifactError("run manifest contains an invalid Git commit")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise AcademicArtifactError("run manifest has no content-addressed artifacts")
    for record in artifacts:
        relative = str(record.get("path", ""))
        path = _safe_artifact_path(run_dir, relative)
        if not path.is_file():
            raise AcademicArtifactError(f"missing run artifact: {relative}")
        actual_size = path.stat().st_size
        if actual_size != int(record.get("size_bytes", -1)):
            raise AcademicArtifactError(
                f"size mismatch for {relative}: expected {record.get('size_bytes')}, "
                f"found {actual_size}"
            )
        actual_hash = _sha256(path)
        expected_hash = str(record.get("sha256", ""))
        if actual_hash != expected_hash:
            raise AcademicArtifactError(
                f"SHA-256 mismatch for {relative}: expected {expected_hash}, "
                f"found {actual_hash}"
            )
    return manifest, run_dir


def _approved_source(
    approved_sources_path: Path, dataset_id: str
) -> dict[str, Any]:
    try:
        config = json.loads(approved_sources_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AcademicArtifactError(f"unable to read approved sources: {exc}") from exc
    source = next(
        (
            record
            for record in config.get("sources", [])
            if str(record.get("id")) == dataset_id
        ),
        None,
    )
    if source is None:
        raise AcademicArtifactError(
            f"dataset {dataset_id!r} is not approved for the prototype"
        )
    if "mathematics" not in str(source.get("domain", "")).lower():
        raise AcademicArtifactError(
            f"dataset {dataset_id!r} is not approved as a mathematics source"
        )
    if str(source.get("role", "")) not in {"primary", "replication"}:
        raise AcademicArtifactError(
            f"dataset {dataset_id!r} is not approved for academic result generation"
        )
    return source


def _artifact_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(record) for record in manifest["artifacts"]]


def _find_artifact(
    manifest: dict[str, Any],
    run_dir: Path,
    *,
    suffix: str,
    contains: tuple[str, ...] = (),
) -> Path:
    matches = []
    for record in _artifact_records(manifest):
        relative = str(record["path"])
        if relative.endswith(suffix) and all(token in relative for token in contains):
            matches.append(_safe_artifact_path(run_dir, relative))
    if len(matches) != 1:
        raise AcademicArtifactError(
            f"expected one artifact ending with {suffix!r} and containing {contains}, "
            f"found {len(matches)}"
        )
    return matches[0]


def _load_experiment_metrics(
    manifest: dict[str, Any], run_dir: Path
) -> list[tuple[str, int, dict[str, Any]]]:
    loaded = []
    experiments = manifest.get("experiments", [])
    if not experiments:
        raise AcademicArtifactError("run manifest has no experiments")
    for experiment in experiments:
        relative = str(experiment.get("candidate_metrics", ""))
        path = _safe_artifact_path(run_dir, relative)
        if not path.is_file():
            raise AcademicArtifactError(f"candidate metrics are missing: {relative}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        split = str(experiment.get("split_strategy"))
        seed = int(experiment.get("seed"))
        if payload.get("split_strategy") != split or int(payload.get("seed")) != seed:
            raise AcademicArtifactError(
                f"metrics metadata differs from experiment declaration: {relative}"
            )
        loaded.append((split, seed, payload))
    return loaded


def _write_model_comparison(
    experiments: list[tuple[str, int, dict[str, Any]]], output: Path
) -> None:
    lines = [
        r"\begin{table}[htb]",
        r"\centering",
        r"\caption{Comparação técnica dos modelos por protocolo e semente}",
        r"\label{tab:prototype-model-comparison}",
        r"\small",
        r"\begin{tabular}{llrrrrr}",
        r"\toprule",
        r"Protocolo & Modelo & Semente & Log-loss & Brier & ROC-AUC & ECE \\",
        r"\midrule",
    ]
    for split, seed, payload in sorted(experiments, key=lambda item: (item[0], item[1])):
        for model_key, values in payload.get("models", {}).items():
            lines.append(
                "{} & {} & {} & {} & {} & {} & {} \\\\".format(
                    _latex_escape(split),
                    _latex_escape(MODEL_NAMES.get(model_key, model_key)),
                    seed,
                    _number(values.get("log_loss")),
                    _number(values.get("brier_score")),
                    _number(values.get("roc_auc")),
                    _number(values.get("expected_calibration_error")),
                )
            )
        lines.append(r"\addlinespace")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\fonte{Elaboração própria a partir dos artefatos reproduzíveis do experimento.}",
            r"\end{table}",
            "",
            "% As métricas descrevem desempenho preditivo e não demonstram eficácia pedagógica.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_data_quality(quality: dict[str, Any], output: Path) -> None:
    rows = [
        ("Registros de entrada", quality.get("input_rows")),
        ("Duplicatas removidas", quality.get("duplicate_rows_removed")),
        ("Registros inválidos removidos", quality.get("invalid_rows_removed")),
        ("Interações processadas", quality.get("output_rows")),
        ("Estudantes", quality.get("students")),
        ("Itens", quality.get("items")),
        ("Habilidades", quality.get("skills")),
    ]
    lines = [
        r"\begin{table}[htb]",
        r"\centering",
        r"\caption{Resumo de qualidade e abrangência da base processada}",
        r"\label{tab:prototype-data-quality}",
        r"\begin{tabular}{lr}",
        r"\toprule",
        r"Indicador & Quantidade \\",
        r"\midrule",
    ]
    lines.extend(
        f"{_latex_escape(label)} & {_integer(value)} \\\\"
        for label, value in rows
        if value is not None
    )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\fonte{Elaboração própria a partir do relatório automatizado de qualidade.}",
            r"\end{table}",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_skill_summary(profiles: pd.DataFrame, output: Path) -> None:
    required = {
        "student_id",
        "skill_id",
        "evidence_count",
        "predicted_probability",
        "evidence_status",
    }
    missing = sorted(required.difference(profiles.columns))
    if missing:
        raise AcademicArtifactError(
            "skill profile is missing columns: " + ", ".join(missing)
        )
    summary = (
        profiles.groupby("skill_id", sort=True)
        .agg(
            students=("student_id", "nunique"),
            evidence=("evidence_count", "sum"),
            mean_probability=("predicted_probability", "mean"),
            insufficient=(
                "evidence_status",
                lambda values: int((values == "insufficient_evidence").sum()),
            ),
        )
        .reset_index()
    )
    lines = [
        r"\begin{table}[htb]",
        r"\centering",
        r"\caption{Síntese descritiva dos perfis por habilidade na execução selecionada}",
        r"\label{tab:prototype-skill-summary}",
        r"\small",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Habilidade & Estudantes & Evidências & Probabilidade média & Evidência insuficiente \\",
        r"\midrule",
    ]
    for row in summary.itertuples(index=False):
        lines.append(
            "{} & {} & {} & {} & {} \\\\".format(
                _latex_escape(row.skill_id),
                _integer(row.students),
                _integer(row.evidence),
                _number(row.mean_probability),
                _integer(row.insufficient),
            )
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\fonte{Elaboração própria. As probabilidades são estimativas operacionais e não diagnósticos definitivos.}",
            r"\end{table}",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_provenance(manifest: dict[str, Any], output: Path) -> None:
    dataset = manifest["dataset"]
    configuration = manifest["configuration"]
    text = "\n".join(
        [
            r"\begin{quote}",
            r"\small",
            "Execução reproduzível \texttt{{{}}}, gerada em {}, a partir do commit "
            "\texttt{{{}}}. A fonte declarada foi \texttt{{{}}}, versão {}, com "
            "SHA-256 de origem \texttt{{{}}}. Foram executadas as estratégias {} "
            "com as sementes {}. Os níveis ordinais e os alertas binários permaneceram "
            "desabilitados. As métricas apresentadas descrevem o desempenho preditivo "
            "no conjunto analisado e não demonstram eficácia pedagógica.".format(
                _latex_escape(manifest["run_id"]),
                _latex_escape(manifest["generated_at"]),
                _latex_escape(manifest["git_commit"][:12]),
                _latex_escape(dataset["dataset_id"]),
                _latex_escape(dataset["version"]),
                _latex_escape(dataset["source_sha256"][:16]),
                _latex_escape(", ".join(configuration["split_strategies"])),
                _latex_escape(", ".join(str(seed) for seed in configuration["seeds"])),
            ),
            r"\end{quote}",
        ]
    )
    output.write_text(text + "\n", encoding="utf-8")


def generate_academic_artifacts(
    *,
    run_manifest_path: Path,
    approved_sources_path: Path,
    output_dir: Path,
) -> AcademicArtifacts:
    """Validate a run and generate LaTeX inputs without rewriting TCC prose."""

    manifest, run_dir = _load_and_validate_run(run_manifest_path)
    dataset_id = str(manifest["dataset"]["dataset_id"])
    _approved_source(approved_sources_path, dataset_id)
    source_manifest_path = _safe_artifact_path(
        run_dir, str(manifest["dataset"]["source_manifest"])
    )
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    if source_manifest.get("dataset_id") != dataset_id:
        raise AcademicArtifactError("source manifest and run manifest disagree on dataset")
    if source_manifest.get("license_or_terms", "").lower().startswith("synthetic"):
        raise AcademicArtifactError("synthetic fixtures cannot generate academic results")

    experiments = _load_experiment_metrics(manifest, run_dir)
    quality_path = _find_artifact(manifest, run_dir, suffix=".quality.json")
    quality = json.loads(quality_path.read_text(encoding="utf-8"))
    preferred = manifest.get("teacher_report", {})
    split = str(preferred.get("split_strategy"))
    seed = str(preferred.get("seed"))
    profiles_path = _find_artifact(
        manifest,
        run_dir,
        suffix=".skill_profiles.parquet",
        contains=(f"/{split}/", f"seed-{seed}/"),
    )
    profiles = pd.read_parquet(profiles_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = AcademicArtifacts(
        model_comparison_path=output_dir / "prototype_model_comparison.tex",
        data_quality_path=output_dir / "prototype_data_quality.tex",
        skill_summary_path=output_dir / "prototype_skill_summary.tex",
        provenance_path=output_dir / "prototype_provenance.tex",
    )
    existing = [path for path in paths.__dict__.values() if path.exists()]
    if existing:
        raise AcademicArtifactError(
            "academic artifacts already exist and will not be overwritten: "
            + ", ".join(path.as_posix() for path in existing)
        )

    _write_model_comparison(experiments, paths.model_comparison_path)
    _write_data_quality(quality, paths.data_quality_path)
    _write_skill_summary(profiles, paths.skill_summary_path)
    _write_provenance(manifest, paths.provenance_path)
    return paths
