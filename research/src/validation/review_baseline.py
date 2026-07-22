"""Freeze, verify, and compare systematic-review baselines.

The current review is treated as an immutable baseline before any update search
is executed. A later search produces a candidate corpus that is compared with
the baseline instead of silently replacing it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ENTRY_PATTERN = re.compile(
    r"@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,\s]+)\s*,(?P<body>.*?)(?=\n\s*@|\Z)",
    re.DOTALL,
)
FIELD_PATTERN = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*=\s*(?:\{(?P<braced>.*?)\}|\"(?P<quoted>.*?)\")\s*,?",
    re.DOTALL,
)
DOI_PREFIX_PATTERN = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", re.I)


@dataclass(frozen=True)
class CorpusEntry:
    """Normalized bibliographic record used to compare review executions."""

    key: str
    entry_type: str
    title: str
    year: str
    doi: str

    @property
    def identity(self) -> str:
        if self.doi:
            return f"doi:{self.doi}"
        normalized_title = normalize_text(self.title)
        return f"title:{normalized_title}|year:{self.year}"

    def as_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "entry_type": self.entry_type,
            "title": self.title,
            "year": self.year,
            "doi": self.doi,
            "identity": self.identity,
        }


def normalize_text(value: str) -> str:
    """Normalize text for stable identity matching without external packages."""

    decomposed = unicodedata.normalize("NFKD", value)
    without_marks = "".join(char for char in decomposed if not unicodedata.combining(char))
    alphanumeric = re.sub(r"[^a-z0-9]+", " ", without_marks.lower())
    return " ".join(alphanumeric.split())


def normalize_doi(value: str) -> str:
    value = DOI_PREFIX_PATTERN.sub("", value.strip()).strip().lower()
    return value.rstrip(".,; ")


def _clean_field(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    while value.startswith("{") and value.endswith("}"):
        value = value[1:-1].strip()
    return value


def read_bibtex_corpus(path: Path) -> list[CorpusEntry]:
    """Read the fields required for corpus identity and update comparison."""

    text = path.read_text(encoding="utf-8")
    entries: list[CorpusEntry] = []
    keys: set[str] = set()
    for match in ENTRY_PATTERN.finditer(text):
        key = match.group("key").strip()
        if key in keys:
            raise ValueError(f"duplicate BibTeX key in corpus: {key}")
        keys.add(key)
        fields: dict[str, str] = {}
        for field in FIELD_PATTERN.finditer(match.group("body")):
            raw_value = field.group("braced")
            if raw_value is None:
                raw_value = field.group("quoted") or ""
            fields[field.group("name").lower()] = _clean_field(raw_value)
        title = fields.get("title", "")
        year = fields.get("year", "")
        doi = normalize_doi(fields.get("doi", ""))
        if not title:
            raise ValueError(f"BibTeX entry has no title: {key}")
        entries.append(
            CorpusEntry(
                key=key,
                entry_type=match.group("type").lower(),
                title=title,
                year=year,
                doi=doi,
            )
        )
    if not entries:
        raise ValueError(f"no BibTeX entries found in {path}")
    return sorted(entries, key=lambda entry: entry.key)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_record(path: Path, repository_root: Path) -> dict[str, Any]:
    relative = path.relative_to(repository_root).as_posix()
    record: dict[str, Any] = {
        "path": relative,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        with path.open(encoding="utf-8") as handle:
            line_count = sum(1 for line in handle if line.strip())
        record["nonempty_lines"] = line_count
        record["data_rows"] = max(0, line_count - 1)
    elif suffix == ".bib":
        record["bib_entries"] = len(read_bibtex_corpus(path))
    return record


def load_baseline_config(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "baseline_id",
        "source_commit",
        "corpus_bib",
        "artifacts",
        "reported_counts",
        "temporal_scope",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError("review baseline config is missing: " + ", ".join(missing))
    commit = str(payload["source_commit"])
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("source_commit must be a full 40-character Git SHA")
    if not isinstance(payload["artifacts"], list) or not payload["artifacts"]:
        raise ValueError("artifacts must be a non-empty list")
    return payload


def build_review_manifest(
    *,
    config: dict[str, Any],
    repository_root: Path,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a content-addressed manifest for the declared review baseline."""

    generated_at = generated_at or datetime.now(UTC)
    if generated_at.tzinfo is None:
        generated_at = generated_at.replace(tzinfo=UTC)
    artifact_paths = [repository_root / str(path) for path in config["artifacts"]]
    missing = [path for path in artifact_paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "review baseline artifacts are missing: "
            + ", ".join(path.as_posix() for path in missing)
        )
    corpus_path = repository_root / str(config["corpus_bib"])
    corpus = read_bibtex_corpus(corpus_path)
    expected_included = config.get("reported_counts", {}).get("included")
    if expected_included is not None and len(corpus) != int(expected_included):
        raise ValueError(
            f"corpus count mismatch: expected {expected_included}, found {len(corpus)}"
        )

    return {
        "schema_version": "1.0.0",
        "baseline_id": str(config["baseline_id"]),
        "source_commit": str(config["source_commit"]),
        "generated_at": generated_at.isoformat(),
        "reported_counts": config["reported_counts"],
        "temporal_scope": config["temporal_scope"],
        "search_execution": config.get("search_execution", {}),
        "artifacts": [
            _artifact_record(path, repository_root)
            for path in sorted(artifact_paths, key=lambda value: value.as_posix())
        ],
        "corpus": {
            "path": str(config["corpus_bib"]),
            "entry_count": len(corpus),
            "entries": [entry.as_dict() for entry in corpus],
        },
        "update_policy": config.get("update_policy", {}),
    }


def verify_review_manifest(
    manifest: dict[str, Any], repository_root: Path
) -> list[str]:
    """Return integrity errors for a baseline manifest and working tree."""

    errors: list[str] = []
    for artifact in manifest.get("artifacts", []):
        path = repository_root / str(artifact["path"])
        if not path.is_file():
            errors.append(f"missing baseline artifact: {artifact['path']}")
            continue
        actual_size = path.stat().st_size
        if actual_size != int(artifact["size_bytes"]):
            errors.append(
                f"size mismatch for {artifact['path']}: "
                f"expected {artifact['size_bytes']}, found {actual_size}"
            )
        actual_hash = sha256_file(path)
        if actual_hash != artifact["sha256"]:
            errors.append(
                f"SHA-256 mismatch for {artifact['path']}: "
                f"expected {artifact['sha256']}, found {actual_hash}"
            )
    corpus_path = repository_root / str(manifest.get("corpus", {}).get("path", ""))
    if corpus_path.is_file():
        actual_corpus = read_bibtex_corpus(corpus_path)
        if len(actual_corpus) != int(manifest["corpus"]["entry_count"]):
            errors.append("corpus entry count differs from baseline manifest")
    else:
        errors.append(f"missing corpus bibliography: {corpus_path}")
    return errors


def _entry_map(entries: list[CorpusEntry] | list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        record = entry.as_dict() if isinstance(entry, CorpusEntry) else dict(entry)
        identity = str(record.get("identity") or "")
        if not identity:
            doi = normalize_doi(str(record.get("doi", "")))
            identity = (
                f"doi:{doi}"
                if doi
                else f"title:{normalize_text(str(record.get('title', '')))}|year:{record.get('year', '')}"
            )
            record["identity"] = identity
        if identity in result:
            raise ValueError(f"duplicate corpus identity: {identity}")
        result[identity] = record
    return result


def compare_corpora(
    baseline: list[CorpusEntry] | list[dict[str, Any]],
    candidate: list[CorpusEntry] | list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Compare two corpora by DOI, falling back to normalized title and year."""

    baseline_map = _entry_map(baseline)
    candidate_map = _entry_map(candidate)
    baseline_ids = set(baseline_map)
    candidate_ids = set(candidate_map)
    added = [candidate_map[key] for key in sorted(candidate_ids - baseline_ids)]
    removed = [baseline_map[key] for key in sorted(baseline_ids - candidate_ids)]
    changed: list[dict[str, Any]] = []
    unchanged: list[dict[str, Any]] = []
    for identity in sorted(baseline_ids & candidate_ids):
        before = baseline_map[identity]
        after = candidate_map[identity]
        comparable_fields = ("key", "entry_type", "title", "year", "doi")
        if any(before.get(field) != after.get(field) for field in comparable_fields):
            changed.append({"identity": identity, "before": before, "after": after})
        else:
            unchanged.append(before)
    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    freeze = subcommands.add_parser("freeze")
    freeze.add_argument("--config", type=Path, required=True)
    freeze.add_argument("--repository-root", type=Path, default=Path(".."))
    freeze.add_argument("--output", type=Path, required=True)

    check_config = subcommands.add_parser("check-config")
    check_config.add_argument("--config", type=Path, required=True)
    check_config.add_argument("--repository-root", type=Path, default=Path(".."))

    verify = subcommands.add_parser("verify")
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--repository-root", type=Path, default=Path(".."))

    compare = subcommands.add_parser("compare")
    compare.add_argument("--baseline", type=Path, required=True)
    compare.add_argument("--candidate-bib", type=Path, required=True)
    compare.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command in {"freeze", "check-config"}:
        config = load_baseline_config(args.config)
        manifest = build_review_manifest(
            config=config,
            repository_root=args.repository_root.resolve(),
        )
        errors = verify_review_manifest(manifest, args.repository_root.resolve())
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        if args.command == "freeze":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            print(f"baseline_manifest={args.output}")
        else:
            print(
                f"PASS: baseline config resolves {manifest['corpus']['entry_count']} studies "
                f"and {len(manifest['artifacts'])} artifacts"
            )
        return 0

    if args.command == "verify":
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors = verify_review_manifest(manifest, args.repository_root.resolve())
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("PASS: review baseline content matches the manifest")
        return 0

    if args.command == "compare":
        baseline_manifest = json.loads(args.baseline.read_text(encoding="utf-8"))
        comparison = compare_corpora(
            baseline_manifest["corpus"]["entries"],
            read_bibtex_corpus(args.candidate_bib),
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(comparison, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(
            "comparison="
            f"added:{len(comparison['added'])},"
            f"removed:{len(comparison['removed'])},"
            f"changed:{len(comparison['changed'])},"
            f"unchanged:{len(comparison['unchanged'])}"
        )
        return 0

    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
