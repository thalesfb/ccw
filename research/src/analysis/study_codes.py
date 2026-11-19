"""Load and render the reader-facing codes for the original study selection."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CODES_PATH = ROOT / "research/data/study_codes_current.csv"
SCOPE_PATH = ROOT / "research/data/current_synthesis_scope.csv"
OUTPUT_PATH = ROOT / "research/exports/references/study_codes_tcc.tex"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_study_codes(root: Path = ROOT) -> list[dict[str, str]]:
    """Validate that the code registry covers exactly the 15 historical inclusions."""

    codes = _read_csv(root / "research/data/study_codes_current.csv")
    scope = [
        row for row in _read_csv(root / "research/data/current_synthesis_scope.csv")
        if row["synthesis_role"] == "empirical_evidence"
    ]
    expected_codes = [f"E{index:02d}" for index in range(1, 16)]
    if [row.get("code") for row in codes] != expected_codes:
        raise ValueError("Study codes must be consecutive E01–E15 in reference order")
    if len({row.get("study_key") for row in codes}) != len(codes):
        raise ValueError("Study code registry contains duplicate study keys")
    if len({row.get("study_id") for row in codes}) != len(codes):
        raise ValueError("Study code registry contains duplicate study IDs")
    scope_by_key = {row["study_key"]: row["study_id"] for row in scope}
    codes_by_key = {row["study_key"]: row["study_id"] for row in codes}
    if codes_by_key != scope_by_key:
        missing = sorted(set(scope_by_key) - set(codes_by_key))
        extra = sorted(set(codes_by_key) - set(scope_by_key))
        mismatched = sorted(
            key for key in set(scope_by_key) & set(codes_by_key)
            if scope_by_key[key] != codes_by_key[key]
        )
        raise ValueError(
            f"Study codes must match the 15 original inclusions; missing={missing}, "
            f"extra={extra}, mismatched_ids={mismatched}"
        )
    return codes


def code_by_key(root: Path = ROOT) -> dict[str, str]:
    return {row["study_key"]: row["code"] for row in load_study_codes(root)}


def code_by_id(root: Path = ROOT) -> dict[str, str]:
    return {row["study_id"]: row["code"] for row in load_study_codes(root)}


def render_latex_mapping(root: Path = ROOT) -> str:
    rows = load_study_codes(root)
    lines = [
        "% Arquivo gerado de research/data/study_codes_current.csv; não editar manualmente.",
        r"\newcommand{\estudo}[1]{\csname TCCstudy@#1\endcsname}",
        r"\newcommand{\estudocite}[2][]{\estudo{#2}~\if\relax\detokenize{#1}\relax\citeonline{#2}\else\citeonline[#1]{#2}\fi}",
    ]
    lines.extend(
        rf"\expandafter\def\csname TCCstudy@{row['study_key']}\endcsname{{{row['code']}}}"
        for row in rows
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render_latex_mapping()
    if args.check:
        actual = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if actual != expected:
            raise SystemExit(f"Generated study-code mapping is stale: {OUTPUT_PATH}")
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
    print("Study code registry is current (15 studies, E01–E15).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
