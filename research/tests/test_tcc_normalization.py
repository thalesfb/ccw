from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TCC_ROOT = REPO_ROOT / "results" / "tcc"


def _entries(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"@\w+\{([^,]+),(.*?)(?=\n@|\Z)", text, flags=re.DOTALL)


def test_tcc_selects_normal_capitalization_for_author_date_citations() -> None:
    style = (TCC_ROOT / "abnetx2" / "abntex2-alf.bst").read_text(
        encoding="utf-8"
    )

    assert "#1 'abnt.cite.style :=" in style


def test_tcc_bibliography_marks_doi_urls_as_doi() -> None:
    style = (TCC_ROOT / "abnetx2" / "abntex2-alf.bst").read_text(
        encoding="utf-8"
    )

    assert '"DOI: "' in style
    assert '"https://doi.org/"' in style


def test_non_doi_online_references_record_access_dates() -> None:
    for bibliography in ("referencias.bib", "referencias_pedagogicas.bib"):
        for key, body in _entries(TCC_ROOT / bibliography):
            if "url =" not in body or "doi =" in body:
                continue
            assert "urlaccessdate =" in body, key


def test_pdf_metadata_is_declared_after_document_metadata_is_known() -> None:
    cover = (TCC_ROOT / "pretextuais" / "capa.tex").read_text(encoding="utf-8")

    assert "pdftitle={Ensino Personalizado de Matemática" in cover
    assert "pdfauthor={Thales Ferreira Batista}" in cover
