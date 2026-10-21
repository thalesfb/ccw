"""Check the committed canonical PDF without editing files or Git history."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PDF = "results/tcc/main.pdf"
SOURCES = (
    "results/tcc",
    ":(exclude)results/tcc/main.pdf",
    ":(exclude)results/tcc/index.html",
    ":(exclude)results/tcc/README.md",
    ":(exclude)results/tcc/presentation",
)


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=False,
    )


def require_success(result: subprocess.CompletedProcess[str]) -> str:
    if result.returncode:
        raise ValueError(result.stderr.strip() or "Git could not verify the canonical PDF")
    return result.stdout.strip()


def require_unchanged(root: Path, revision: str, paths: tuple[str, ...]) -> None:
    result = git(root, "diff", "--quiet", revision, "--", *paths)
    if result.returncode == 1:
        raise ValueError(
            "Canonical PDF is stale or uncommitted. Compile, inspect and commit "
            "the PDF with the corresponding sources; CI never creates commits."
        )
    require_success(result)


def check(root: Path) -> None:
    if require_success(git(root, "rev-parse", "--is-shallow-repository")) != "false":
        raise ValueError("Full Git history is required to check the canonical PDF")
    require_success(git(root, "ls-files", "--error-unmatch", "--", PDF))
    with (root / PDF).open("rb") as source:
        if source.read(5) != b"%PDF-":
            raise ValueError("Canonical PDF is missing a valid PDF header")
    pdf_commit = require_success(git(root, "log", "-1", "--format=%H", "--", PDF))
    if not pdf_commit:
        raise ValueError("Canonical PDF has no committed provenance")
    require_success(git(root, "merge-base", "--is-ancestor", pdf_commit, "HEAD"))
    require_unchanged(root, "HEAD", (PDF,))
    require_unchanged(root, "HEAD", SOURCES)
    require_unchanged(root, f"{pdf_commit}..HEAD", SOURCES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        check(args.repo.resolve())
    except (OSError, ValueError) as error:
        print(f"Canonical PDF validation failed: {error}", file=sys.stderr)
        return 1
    print("Canonical PDF provenance passed; no files or commits changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
