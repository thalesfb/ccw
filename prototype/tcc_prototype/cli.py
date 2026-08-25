"""Command-line interface for the TCC prototype pipeline."""

from __future__ import annotations

import argparse
import json
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
from .profile_analysis import (
    build_profile_artifacts,
    verify_profile_input_provenance,
)
from .profiles import ProfileConfigError, load_profile_config


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _load_preparation_provenance(report_path: Path, input_path: Path) -> dict[str, str]:
    """Verify that a processed input is the artifact registered by its preparation report."""

    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read preparation report {report_path}: {exc}") from exc

    required = {"dataset_id", "dataset_version", "source_sha256", "processed_sha256"}
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError("preparation report is missing fields: " + ", ".join(missing))
    if not _is_sha256(payload["source_sha256"]):
        raise ValueError("preparation report source_sha256 is invalid")
    if not _is_sha256(payload["processed_sha256"]):
        raise ValueError("preparation report processed_sha256 is invalid")

    processed_input_sha256 = sha256_file(input_path)
    if processed_input_sha256 != payload["processed_sha256"]:
        raise ValueError(
            "processed input SHA-256 mismatch: the Parquet does not match its preparation report"
        )
    return {
        "dataset_id": str(payload["dataset_id"]),
        "dataset_version": str(payload["dataset_version"]),
        "source_sha256": str(payload["source_sha256"]),
        "processed_input_sha256": processed_input_sha256,
        "preparation_report_sha256": sha256_file(report_path),
    }


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
    evaluate.add_argument("--preparation-report", type=Path, required=True)
    evaluate.add_argument("--output-dir", type=Path, required=True)
    evaluate.add_argument("--experiment-config", type=Path, required=True)
    evaluate.add_argument(
        "--split-strategy",
        choices=("student_holdout", "personalized_temporal"),
        required=True,
    )

    profile = subcommands.add_parser(
        "build-evidence-profile",
        help="derive auditable skill evidence from one frozen experiment run",
    )
    profile.add_argument("--input", type=Path, required=True)
    profile.add_argument("--experiment-run-dir", type=Path, required=True)
    profile.add_argument("--profile-config", type=Path, required=True)
    profile.add_argument("--output-dir", type=Path, required=True)
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
            provenance = _load_preparation_provenance(
                args.preparation_report,
                args.input,
            )
            interactions = pd.read_parquet(args.input)
            config_sha256 = sha256_file(args.experiment_config)
            artifact_root = (
                args.output_dir
                / f"input-{provenance['processed_input_sha256']}"
            )
            for seed in config["random_seeds"]:
                result = run_baseline_experiment(
                    interactions,
                    config=config,
                    split_strategy=args.split_strategy,
                    seed=int(seed),
                )
                artifacts = write_baseline_artifacts(
                    result,
                    output_dir=artifact_root,
                    source_sha256=provenance["source_sha256"],
                    config_sha256=config_sha256,
                )
                provenance_path = artifacts.metrics_path.parent / "input-provenance.json"
                provenance_path.write_text(
                    json.dumps(
                        {
                            **provenance,
                            "experiment_config_sha256": config_sha256,
                        },
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                print(f"seed={seed} metrics={artifacts.metrics_path}")
            return 0
        except (ExperimentConfigError, FileExistsError, OSError, ValueError) as error:
            raise SystemExit(f"baseline evaluation aborted: {error}") from error

    if args.command == "build-evidence-profile":
        try:
            config = load_profile_config(args.profile_config)
            verify_profile_input_provenance(args.input, args.experiment_run_dir)
            interactions = pd.read_parquet(args.input)
            artifacts = build_profile_artifacts(
                interactions,
                experiment_run_dir=args.experiment_run_dir,
                profile_config=config,
                profile_config_sha256=sha256_file(args.profile_config),
                output_dir=args.output_dir,
                explanation_rows=int(config.get("explanation_rows", 20)),
                permutation_repeats=int(config.get("permutation_repeats", 5)),
            )
            print(f"profile={artifacts.profile_path}")
            print(f"explanations={artifacts.explanations_path}")
            print(f"importance={artifacts.permutation_importance_path}")
            print(f"manifest={artifacts.manifest_path}")
            return 0
        except (ProfileConfigError, FileExistsError, OSError, ValueError) as error:
            raise SystemExit(f"evidence profile aborted: {error}") from error

    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
