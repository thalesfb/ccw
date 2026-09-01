import re
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


def test_repository_bibliography_does_not_use_indexers_as_urls() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    bibliography = (repository_root / "results/tcc/referencias.bib").read_text(
        encoding="utf-8"
    )

    indexer_urls = re.findall(
        r"url\s*=\s*\{https?://(?:www\.)?(?:openalex\.org|semanticscholar\.org)[^}]*\}",
        bibliography,
        flags=re.IGNORECASE,
    )

    assert indexer_urls == []


def test_priority_metadata_corrections_are_applied() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    bibliography = (repository_root / "results/tcc/referencias.bib").read_text(
        encoding="utf-8"
    )

    assert "doi = {10.3233/EFI-180221}" in bibliography
    assert "author = {Hendra Tjahyadi and Krismon N. L. Tude}" in bibliography
    assert "booktitle = {2019 IEEE Global Engineering Education Conference (EDUCON)}" in bibliography
    assert "@phdthesis{Computational2017_008" in bibliography
    assert "@article{Villegas2025_6916" in bibliography
    assert "doi = {10.1186/s40561-025-00389-y}" in bibliography
    assert "@phdthesis{Kaser2025_6918" in bibliography
    assert "@misc{Imperatrice2025_6921" in bibliography


def test_primary_technical_references_are_present_and_cited() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    bib_paths = [
        repository_root / "results/tcc/referencias.bib",
        repository_root / "results/tcc/referencias_pedagogicas.bib",
    ]
    keys = extract_bib_keys(bib_paths)
    prototype = (repository_root / "results/tcc/conteudo/prototipo.tex").read_text(
        encoding="utf-8"
    )

    required = {
        "Breiman2001",
        "CortesVapnik1995",
        "Fawcett2006",
        "NiculescuMizilCaruana2005",
        "RibeiroSinghGuestrin2016",
        "LundbergLee2017",
    }

    assert required <= keys
    for key in required:
        assert key in prototype
