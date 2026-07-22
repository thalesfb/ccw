"""Command-line interface for the TCC prototype pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .modeling.experiment import run_baseline_experiment, write_baseline_artifacts
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
    prepare.add_argument(
        "--skill-separator",
        default=None,
        help="optional separator used when one source field contains multiple skills",
    )

    evaluate = subcommands.add_parser(
        "evaluate-baselines",
        help="run leakage-safe probability baselines on canonical interactions",
    )
    evaluate.add_argument("--input", type=Path, required=True)
    evaluate.add_argument("--output-dir", type=Path, required=True)
    evaluate.add_argument(
        "--split-strategy",
        choices=("cold_start", "temporal"),
        required=True,
    )
    evaluate.add_argument("--seed", type=int, default=2026)
    evaluate.add_argument("--minimum-skill-rows", type=int, default=100)
    return parser


def main() -> int:
    args = build_parser().parse_args()
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

    if args.command == "evaluate-baselines":
        interactions = pd.read_parquet(args.input)
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

    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
