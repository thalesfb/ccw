"""Validate coverage and consistency of the TCC bibliography audit.

The audit is intentionally machine-readable so bibliography changes can be
reviewed independently from the prose of the TCC. This module uses only the
Python standard library and can run before the research dependencies are
installed.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BIB_KEY_PATTERN = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
ALLOWED_EXISTENCE = {"verified", "unverified"}
ALLOWED_METADATA = {"verified", "metadata_fix", "update_version", "replace"}
ALLOWED_USE = {
    "verified",
    "scope_limited",
    "editorial_caution",
    "unused",
}
ALLOWED_DECISIONS = {
    "keep",
    "normalize",
    "retain_with_caution",
    "retain_unused",
    "replace",
}
INDEXER_HOSTS = ("openalex.org", "semanticscholar.org")


@dataclass(frozen=True)
class AuditRow:
    """One reference audit decision."""

    key: str
    existence: str
    metadata_status: str
    use_status: str
    canonical_identifier: str
    decision: str


def extract_bib_keys(paths: Iterable[Path]) -> set[str]:
    """Return all BibTeX keys found in the supplied files."""

    keys: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        keys.update(BIB_KEY_PATTERN.findall(text))
    return keys


def read_audit(path: Path) -> dict[str, AuditRow]:
    """Read and validate the audit CSV structure."""

    rows: dict[str, AuditRow] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "key",
            "existence",
            "metadata_status",
            "use_status",
            "canonical_identifier",
            "decision",
        }
        missing_columns = required.difference(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(
                "audit CSV is missing columns: " + ", ".join(sorted(missing_columns))
            )

        for line_number, raw in enumerate(reader, start=2):
            key = raw["key"].strip()
            if not key:
                raise ValueError(f"empty key at CSV line {line_number}")
            if key in rows:
                raise ValueError(f"duplicate audit key: {key}")

            row = AuditRow(
                key=key,
                existence=raw["existence"].strip(),
                metadata_status=raw["metadata_status"].strip(),
                use_status=raw["use_status"].strip(),
                canonical_identifier=raw["canonical_identifier"].strip(),
                decision=raw["decision"].strip(),
            )
            rows[key] = row
    return rows


def validate_audit(bib_keys: set[str], rows: dict[str, AuditRow]) -> list[str]:
    """Return human-readable validation errors."""

    errors: list[str] = []
    audited_keys = set(rows)

    for key in sorted(bib_keys - audited_keys):
        errors.append(f"bibliography key has no audit decision: {key}")
    for key in sorted(audited_keys - bib_keys):
        errors.append(f"audit key is absent from bibliography files: {key}")

    for key, row in sorted(rows.items()):
        if row.existence not in ALLOWED_EXISTENCE:
            errors.append(f"{key}: invalid existence status {row.existence!r}")
        if row.metadata_status not in ALLOWED_METADATA:
            errors.append(
                f"{key}: invalid metadata status {row.metadata_status!r}"
            )
        if row.use_status not in ALLOWED_USE:
            errors.append(f"{key}: invalid use status {row.use_status!r}")
        if row.decision not in ALLOWED_DECISIONS:
            errors.append(f"{key}: invalid decision {row.decision!r}")

        canonical = row.canonical_identifier.lower()
        if any(host in canonical for host in INDEXER_HOSTS):
            errors.append(
                f"{key}: canonical identifier points to an academic indexer"
            )
        if row.metadata_status == "verified" and row.decision == "normalize":
            errors.append(
                f"{key}: verified metadata cannot simultaneously require normalization"
            )
        if row.decision == "replace" and row.use_status != "unused":
            errors.append(f"{key}: replaced references must be marked unused")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit",
        type=Path,
        default=Path("data/reference_audit.csv"),
        help="path to the machine-readable audit CSV",
    )
    parser.add_argument(
        "--bib",
        type=Path,
        action="append",
        default=None,
        help="BibTeX file; may be supplied more than once",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    bib_paths = args.bib or [
        Path("../results/tcc/referencias.bib"),
        Path("../results/tcc/referencias_pedagogicas.bib"),
    ]
    bib_keys = extract_bib_keys(bib_paths)
    rows = read_audit(args.audit)
    errors = validate_audit(bib_keys, rows)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {len(rows)} bibliography entries have explicit audit decisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
