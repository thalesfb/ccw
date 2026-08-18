"""Command-line interface for the TCC prototype pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .manifest import sha256_file
from .modeling.experiment import (
    ExperimentConfigError,
    load_experiment_config,
    run_baseline_experiment,
    write_baseline_artifacts,
)
from .pipeline import prepare_assistments


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tcc-prototype")
    subcommands = parser.add_subparsers(dest="command", required=True)

    prepare = subcommands.add_parser(
        "prepare-assistments",
        help="validate and normalize the corrected ASSISTments Skill Builder CSV",
    )
    prepare.add_argument("--manifest", type=Path, required=True)
    prepare.add_argument("--raw-dir", type=Path, required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)

    evaluate = subcommands.add_parser(
        "evaluate-baselines",
        help="run the frozen leakage-safe model evaluation protocol",
    )
    evaluate.add_argument("--input", type=Path, required=True)
    evaluate.add_argument("--output-dir", type=Path, required=True)
    evaluate.add_argument("--experiment-config", type=Path, required=True)
    evaluate.add_argument(
        "--split-strategy",
        choices=("student_holdout", "personalized_temporal"),
        required=True,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "prepare-assistments":
        artifacts = prepare_assistments(
            manifest_path=args.manifest,
            raw_dir=args.raw_dir,
            output_dir=args.output_dir,
        )
        print(f"parquet={artifacts.parquet_path}")
        print(f"quality_report={artifacts.report_path}")
        print(f"processed_sha256={artifacts.processed_sha256}")
        return 0

    if args.command == "evaluate-baselines":
        try:
            config = load_experiment_config(args.experiment_config)
            interactions = pd.read_parquet(args.input)
            source_sha256 = sha256_file(args.input)
            config_sha256 = sha256_file(args.experiment_config)
            for seed in config["random_seeds"]:
                result = run_baseline_experiment(
                    interactions,
                    config=config,
                    split_strategy=args.split_strategy,
                    seed=int(seed),
                )
                artifacts = write_baseline_artifacts(
                    result,
                    output_dir=args.output_dir,
                    source_sha256=source_sha256,
                    config_sha256=config_sha256,
                )
                print(f"seed={seed} metrics={artifacts.metrics_path}")
            return 0
        except (ExperimentConfigError, FileExistsError, OSError, ValueError) as error:
            raise SystemExit(f"baseline evaluation aborted: {error}") from error

    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
