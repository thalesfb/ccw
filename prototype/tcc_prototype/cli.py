"""Command-line interface for the TCC prototype pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

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
    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
