"""Validate and synchronize visualization assets derived from the review.

The review pipeline writes its canonical charts to
``research/exports/visualizations``.  The TCC and the Slidev presentation
consume copies of those charts from different directories.  This module keeps
those copies byte-identical and records a stable fingerprint of the versioned
research inputs that produced them.

The manifest deliberately contains no timestamps and no SQLite metadata.  A
fresh pipeline/export run can therefore be reproduced from the versioned
snapshot, while CI can still detect that a source change requires regenerated
derived assets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = 1
ASSET_NAMES = (
    "database_coverage.png",
    "papers_by_year.png",
    "prisma_flow.png",
    "relevance_distribution.png",
    "selection_funnel.png",
    "techniques_distribution.png",
)

CANONICAL_DIR = Path("research/exports/visualizations")
CONSUMER_DIRS = {
    "tcc": Path("results/tcc/images"),
    "presentation": Path("presentation/public/images"),
}
MANIFEST_PATH = Path("research/exports/reports/derived_assets_manifest.json")


class DerivedAssetError(RuntimeError):
    """Raised when canonical visualization assets cannot be synchronized."""


def repository_root() -> Path:
    """Return the repository root for this source file."""

    # derived_assets.py -> validation -> src -> research -> repository root
    return Path(__file__).resolve().parents[3]


def _sha256(path: Path, *, normalize_text: bool = False) -> str:
    if normalize_text:
        # Source fingerprints must be identical on Windows and Linux.  The
        # generated PNGs continue to use the raw-byte hash below.
        content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        return hashlib.sha256(content).hexdigest()

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iter_source_files(repo_root: Path) -> Iterable[Path]:
    """Yield versioned source/snapshot inputs that can affect the charts.

    The source set is intentionally conservative: all research Python source
    and structured versioned research data are included.  This means a change
    in a processing stage, renderer, or adjudicated input cannot silently
    leave a previously generated chart paired with new code.
    """

    candidates: set[Path] = set()
    source_root = repo_root / "research" / "src"
    if source_root.exists():
        candidates.update(path for path in source_root.rglob("*.py") if path.is_file())

    data_root = repo_root / "research" / "data"
    if data_root.exists():
        candidates.update(
            path
            for path in data_root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".csv", ".json", ".yaml", ".yml"}
        )

    # This is the row-level versioned representation consumed by the
    # adjudicated replay and the report/visualization generation path.
    papers_csv = repo_root / "research" / "exports" / "analysis" / "papers.csv"
    if papers_csv.is_file():
        candidates.add(papers_csv)

    return sorted(candidates, key=lambda path: path.relative_to(repo_root).as_posix())


def _source_fingerprint(repo_root: Path) -> dict[str, object]:
    paths: list[str] = []
    digest = hashlib.sha256()

    for path in _iter_source_files(repo_root):
        relative = path.relative_to(repo_root).as_posix()
        file_hash = _sha256(path, normalize_text=True)
        paths.append(relative)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")

    return {
        "algorithm": "sha256",
        "sha256": digest.hexdigest(),
        "paths": paths,
    }


def _asset_entry(repo_root: Path, name: str) -> dict[str, object]:
    canonical = repo_root / CANONICAL_DIR / name
    canonical_hash = _sha256(canonical) if canonical.is_file() else None
    copies = []
    for consumer, relative_dir in CONSUMER_DIRS.items():
        target = repo_root / relative_dir / name
        copies.append(
            {
                "consumer": consumer,
                "path": (relative_dir / name).as_posix(),
                "sha256": _sha256(target) if target.is_file() else None,
            }
        )

    return {
        "name": name,
        "canonical_path": (CANONICAL_DIR / name).as_posix(),
        "canonical_sha256": canonical_hash,
        "copies": copies,
    }


def build_manifest(repo_root: Path | None = None) -> dict[str, object]:
    """Build the deterministic manifest for the current repository state."""

    root = (repo_root or repository_root()).resolve()
    return {
        "schema_version": SCHEMA_VERSION,
        "canonical_source": CANONICAL_DIR.as_posix(),
        "consumer_directories": {
            name: path.as_posix() for name, path in CONSUMER_DIRS.items()
        },
        "source_fingerprint": _source_fingerprint(root),
        "assets": [_asset_entry(root, name) for name in ASSET_NAMES],
    }


def _asset_errors(repo_root: Path) -> list[str]:
    errors: list[str] = []

    for name in ASSET_NAMES:
        canonical = repo_root / CANONICAL_DIR / name
        if not canonical.is_file():
            errors.append(f"missing canonical asset: {CANONICAL_DIR / name}")
            continue

        canonical_hash = _sha256(canonical)
        for consumer, relative_dir in CONSUMER_DIRS.items():
            target = repo_root / relative_dir / name
            if not target.is_file():
                errors.append(f"missing {consumer} copy: {relative_dir / name}")
                continue
            target_hash = _sha256(target)
            if target_hash != canonical_hash:
                errors.append(
                    f"{consumer} copy differs from canonical {name}: "
                    f"{target_hash[:12]} != {canonical_hash[:12]}"
                )

    return errors


def validate_derived_assets(repo_root: Path | None = None) -> list[str]:
    """Return actionable errors, or an empty list when assets are current."""

    root = (repo_root or repository_root()).resolve()
    errors = _asset_errors(root)
    manifest_path = root / MANIFEST_PATH

    if not manifest_path.is_file():
        errors.append(f"missing derived asset manifest: {MANIFEST_PATH}")
        return errors

    try:
        actual = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid derived asset manifest {MANIFEST_PATH}: {exc}")
        return errors

    expected = build_manifest(root)
    if actual != expected:
        if actual.get("source_fingerprint") != expected["source_fingerprint"]:
            errors.append(
                "derived asset manifest source fingerprint is stale; "
                "the pipeline or versioned research inputs changed"
            )
        if actual.get("assets") != expected["assets"]:
            errors.append("derived asset manifest does not match current asset hashes")
        if (
            actual.get("schema_version") != expected["schema_version"]
            or actual.get("canonical_source") != expected["canonical_source"]
            or actual.get("consumer_directories") != expected["consumer_directories"]
        ):
            errors.append("derived asset manifest schema or directory mapping is stale")

    return errors


def sync_derived_assets(repo_root: Path | None = None) -> Path:
    """Copy canonical charts to all consumers and write the stable manifest."""

    root = (repo_root or repository_root()).resolve()
    canonical_dir = root / CANONICAL_DIR
    missing = [name for name in ASSET_NAMES if not (canonical_dir / name).is_file()]
    if missing:
        raise DerivedAssetError(
            "Cannot synchronize derived assets; missing canonical files: "
            + ", ".join(missing)
        )

    for relative_dir in CONSUMER_DIRS.values():
        target_dir = root / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in ASSET_NAMES:
            shutil.copyfile(canonical_dir / name, target_dir / name)

    manifest_path = root / MANIFEST_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        build_manifest(root),
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    temporary_path = manifest_path.with_suffix(f"{manifest_path.suffix}.tmp")
    temporary_path.write_text(payload, encoding="utf-8", newline="\n")
    temporary_path.replace(manifest_path)
    return manifest_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check",
        action="store_true",
        help="Fail when copies or the stable manifest differ from canonical output.",
    )
    group.add_argument(
        "--sync",
        action="store_true",
        help="Copy canonical charts to consumers and update the manifest.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root (defaults to the root inferred from this module).",
    )
    args = parser.parse_args(argv)
    root = args.repo_root.resolve() if args.repo_root else repository_root()

    try:
        if args.sync:
            manifest_path = sync_derived_assets(root)
            print(f"Synchronized {len(ASSET_NAMES)} derived assets.")
            print(f"Manifest: {manifest_path.relative_to(root).as_posix()}")
            return 0

        errors = validate_derived_assets(root)
        if errors:
            print("Derived asset validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            print(
                "Run: python -m research.src.validation.derived_assets --sync",
                file=sys.stderr,
            )
            return 1

        print(f"Derived asset validation passed ({len(ASSET_NAMES)} assets).")
        return 0
    except (DerivedAssetError, OSError) as exc:
        print(f"Derived asset operation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
