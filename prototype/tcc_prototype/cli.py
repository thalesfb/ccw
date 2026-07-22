"""Command-line interface for the TCC prototype pipeline."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

from .academic import generate_academic_artifacts
from .acquisition import acquire_assistments
from .modeling.candidate_experiment import (
    run_candidate_experiment,
    write_candidate_artifacts,
)
from .modeling.experiment import run_baseline_experiment, write_baseline_artifacts
from .pipeline import prepare_assistments
from .reporting.teacher_report import build_teacher_report
from .workflow import run_autonomous_workflow


def _add_experiment_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--split-strategy",
        choices=("cold_start", "temporal"),
        required=True,
    )
    parser.add_argument("--seed", type=int, default=2026)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tcc-prototype")
    subcommands = parser.add_subparsers(dest="command", required=True)

    acquire = subcommands.add_parser(
        "acquire-assistments",
        help="download the corrected ASSISTments dataset after explicit terms acceptance",
    )
    acquire.add_argument("--raw-dir", type=Path, required=True)
    acquire.add_argument("--manifest-dir", type=Path, required=True)
    acquire.add_argument(
        "--purpose",
        required=True,
        help="specific scientific purpose recorded in the provenance manifest",
    )
    acquire.add_argument(
        "--accept-terms",
        action="store_true",
        help="confirm acceptance of the official non-reidentification and non-redistribution terms",
    )

    prepare = subcommands.add_parser(
        "prepare-assistments",
        help="validate and normalize the corrected ASSISTments Skill Builder CSV",
    )
    prepare.add_argument("--manifest", type=Path, required=True)
    prepare.add_argument("--raw-dir", type=Path, required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)
    prepare.add_argument(
        "--skill-separator",
        default=None,
        help="optional separator used when one source field contains multiple skills",
    )

    evaluate = subcommands.add_parser(
        "evaluate-baselines",
        help="run leakage-safe probability baselines on canonical interactions",
    )
    _add_experiment_arguments(evaluate)
    evaluate.add_argument("--minimum-skill-rows", type=int, default=100)

    candidate = subcommands.add_parser(
        "evaluate-candidate",
        help="compare a random forest and generate explanations and skill profiles",
    )
    _add_experiment_arguments(candidate)
    candidate.add_argument("--n-estimators", type=int, default=300)
    candidate.add_argument("--min-samples-leaf", type=int, default=5)
    candidate.add_argument("--minimum-profile-evidence", type=int, default=5)
    candidate.add_argument("--explanation-rows", type=int, default=20)
    candidate.add_argument("--permutation-repeats", type=int, default=5)

    report = subcommands.add_parser(
        "build-teacher-report",
        help="generate a standalone privacy-preserving HTML teacher report",
    )
    report.add_argument("--profiles", type=Path, required=True)
    report.add_argument("--metrics", type=Path, required=True)
    report.add_argument("--importance", type=Path, required=True)
    report.add_argument("--output", type=Path, required=True)
    report.add_argument("--dataset-label", required=True)
    report.add_argument("--model-version", required=True)
    report.add_argument(
        "--pseudonym-salt",
        default=None,
        help="secret salt; alternatively set TCC_PSEUDONYM_SALT",
    )

    workflow = subcommands.add_parser(
        "run-all",
        help="prepare data, execute all declared experiments, build the report, and freeze a run manifest",
    )
    workflow.add_argument("--source-manifest", type=Path, required=True)
    workflow.add_argument("--raw-dir", type=Path, required=True)
    workflow.add_argument("--output-root", type=Path, required=True)
    workflow.add_argument("--run-id", required=True)
    workflow.add_argument("--git-commit", required=True)
    workflow.add_argument("--seeds", type=int, nargs="+", default=[2026, 1701, 31415])
    workflow.add_argument(
        "--split-strategies",
        nargs="+",
        choices=("cold_start", "temporal"),
        default=["cold_start", "temporal"],
    )
    workflow.add_argument("--dataset-label", required=True)
    workflow.add_argument("--model-version", required=True)
    workflow.add_argument("--n-estimators", type=int, default=300)
    workflow.add_argument("--min-samples-leaf", type=int, default=5)
    workflow.add_argument("--minimum-profile-evidence", type=int, default=5)
    workflow.add_argument("--minimum-skill-rows", type=int, default=100)
    workflow.add_argument("--explanation-rows", type=int, default=20)
    workflow.add_argument("--permutation-repeats", type=int, default=5)
    workflow.add_argument(
        "--preferred-report-split",
        choices=("cold_start", "temporal"),
        default="temporal",
    )
    workflow.add_argument("--preferred-report-seed", type=int, default=2026)
    workflow.add_argument(
        "--pseudonym-salt",
        default=None,
        help="secret salt; alternatively set TCC_PSEUDONYM_SALT",
    )

    academic = subcommands.add_parser(
        "generate-academic-artifacts",
        help="validate a completed run and generate traceable LaTeX tables without rewriting TCC prose",
    )
    academic.add_argument("--run-manifest", type=Path, required=True)
    academic.add_argument("--approved-sources", type=Path, required=True)
    academic.add_argument("--output-dir", type=Path, required=True)
    return parser


def _resolve_salt(argument: str | None) -> str:
    salt = argument or os.environ.get("TCC_PSEUDONYM_SALT")
    if not salt:
        raise SystemExit(
            "pseudonym salt is required through --pseudonym-salt "
            "or TCC_PSEUDONYM_SALT"
        )
    return salt


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "acquire-assistments":
        result = acquire_assistments(
            raw_dir=args.raw_dir,
            manifest_dir=args.manifest_dir,
            purpose=args.purpose,
            accept_terms=args.accept_terms,
        )
        print(f"raw_file={result.raw_path}")
        print(f"manifest={result.manifest_path}")
        print(f"sha256={result.sha256}")
        return 0

    if args.command == "prepare-assistments":
        artifacts = prepare_assistments(
            manifest_path=args.manifest,
            raw_dir=args.raw_dir,
            output_dir=args.output_dir,
            skill_separator=args.skill_separator,
        )
        print(f"parquet={artifacts.parquet_path}")
        print(f"quality_report={artifacts.report_path}")
        print(f"processed_sha256={artifacts.processed_sha256}")
        return 0

    if args.command == "build-teacher-report":
        profiles = pd.read_parquet(args.profiles)
        metrics = json.loads(args.metrics.read_text(encoding="utf-8"))
        importance = pd.read_csv(args.importance)
        output = build_teacher_report(
            profiles=profiles,
            metrics=metrics,
            importance=importance,
            output_path=args.output,
            pseudonym_salt=_resolve_salt(args.pseudonym_salt),
            dataset_label=args.dataset_label,
            model_version=args.model_version,
        )
        print(f"teacher_report={output}")
        return 0

    if args.command == "run-all":
        result = run_autonomous_workflow(
            source_manifest_path=args.source_manifest,
            raw_dir=args.raw_dir,
            output_root=args.output_root,
            run_id=args.run_id,
            git_commit=args.git_commit,
            seeds=args.seeds,
            split_strategies=args.split_strategies,
            pseudonym_salt=_resolve_salt(args.pseudonym_salt),
            dataset_label=args.dataset_label,
            model_version=args.model_version,
            n_estimators=args.n_estimators,
            min_samples_leaf=args.min_samples_leaf,
            minimum_profile_evidence=args.minimum_profile_evidence,
            minimum_skill_rows=args.minimum_skill_rows,
            explanation_rows=args.explanation_rows,
            permutation_repeats=args.permutation_repeats,
            preferred_report_split=args.preferred_report_split,
            preferred_report_seed=args.preferred_report_seed,
        )
        print(f"run_directory={result.run_directory}")
        print(f"run_manifest={result.manifest_path}")
        print(f"teacher_report={result.teacher_report_path}")
        return 0

    if args.command == "generate-academic-artifacts":
        artifacts = generate_academic_artifacts(
            run_manifest_path=args.run_manifest,
            approved_sources_path=args.approved_sources,
            output_dir=args.output_dir,
        )
        print(f"model_comparison={artifacts.model_comparison_path}")
        print(f"data_quality={artifacts.data_quality_path}")
        print(f"skill_summary={artifacts.skill_summary_path}")
        print(f"provenance={artifacts.provenance_path}")
        return 0

    interactions = pd.read_parquet(args.input)
    if args.command == "evaluate-baselines":
        result = run_baseline_experiment(
            interactions,
            split_strategy=args.split_strategy,
            seed=args.seed,
            minimum_skill_rows=args.minimum_skill_rows,
        )
        artifacts = write_baseline_artifacts(result, output_dir=args.output_dir)
        print(f"metrics={artifacts.metrics_path}")
        print(f"predictions={artifacts.predictions_path}")
        print(f"splits={artifacts.splits_path}")
        return 0

    if args.command == "evaluate-candidate":
        result = run_candidate_experiment(
            interactions,
            split_strategy=args.split_strategy,
            seed=args.seed,
            n_estimators=args.n_estimators,
            min_samples_leaf=args.min_samples_leaf,
            minimum_profile_evidence=args.minimum_profile_evidence,
            explanation_rows=args.explanation_rows,
            permutation_repeats=args.permutation_repeats,
        )
        artifacts = write_candidate_artifacts(result, output_dir=args.output_dir)
        print(f"metrics={artifacts.metrics_path}")
        print(f"predictions={artifacts.predictions_path}")
        print(f"importance={artifacts.importance_path}")
        print(f"profiles={artifacts.profiles_path}")
        print(f"explanations={artifacts.explanations_path}")
        return 0

    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
