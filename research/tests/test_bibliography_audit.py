from pathlib import Path

import pytest

from src.validation.bibliography_audit import (
    AuditRow,
    extract_bib_keys,
    read_audit,
    validate_audit,
)


def test_extract_bib_keys_from_multiple_files(tmp_path: Path) -> None:
    first = tmp_path / "first.bib"
    second = tmp_path / "second.bib"
    first.write_text("@article{Alpha,\n title={A}\n}\n", encoding="utf-8")
    second.write_text("@book{Beta,\n title={B}\n}\n", encoding="utf-8")

    assert extract_bib_keys([first, second]) == {"Alpha", "Beta"}


def test_read_audit_rejects_duplicate_keys(tmp_path: Path) -> None:
    audit = tmp_path / "audit.csv"
    audit.write_text(
        "key,existence,metadata_status,use_status,canonical_identifier,decision\n"
        "Alpha,verified,verified,verified,10.1/a,keep\n"
        "Alpha,verified,verified,verified,10.1/a,keep\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate audit key"):
        read_audit(audit)


def test_validate_audit_reports_missing_and_invalid_rows() -> None:
    rows = {
        "Alpha": AuditRow(
            key="Alpha",
            existence="verified",
            metadata_status="verified",
            use_status="verified",
            canonical_identifier="https://openalex.org/work",
            decision="keep",
        ),
        "Ghost": AuditRow(
            key="Ghost",
            existence="verified",
            metadata_status="replace",
            use_status="verified",
            canonical_identifier="",
            decision="replace",
        ),
    }

    errors = validate_audit({"Alpha", "Beta"}, rows)

    assert "bibliography key has no audit decision: Beta" in errors
    assert "audit key is absent from bibliography files: Ghost" in errors
    assert "Alpha: canonical identifier points to an academic indexer" in errors
    assert "Ghost: replaced references must be marked unused" in errors


def test_repository_audit_covers_all_tcc_bibliography_keys() -> None:
    research_root = Path(__file__).resolve().parents[1]
    repository_root = research_root.parent
    bib_keys = extract_bib_keys(
        [
            repository_root / "results/tcc/referencias.bib",
            repository_root / "results/tcc/referencias_pedagogicas.bib",
        ]
    )
    rows = read_audit(research_root / "data/reference_audit.csv")

    assert validate_audit(bib_keys, rows) == []
