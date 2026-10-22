"""Regression checks for the scientific counts shown at the defense."""

import csv
from pathlib import Path
import re

import pytest

from src.analysis import mmat_current


ROOT = Path(__file__).resolve().parents[2]


def read_rows(relative_path):
    with (ROOT / relative_path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_public_mmat_empirical_metric_matches_the_inclusion_ledger():
    scope = read_rows("research/data/current_synthesis_scope.csv")
    retained = sum(row["record_status"] == "included_empirical_core" for row in scope)
    html = (ROOT / "research/exports/analysis/mmat_current.html").read_text(encoding="utf-8")
    metric = re.search(
        r'<span class="metric-value">(\d+)</span>'
        r'<span class="metric-label">estudos empíricos mantidos provisoriamente</span>',
        html,
    )
    assert metric and int(metric[1]) == retained


def test_synthesis_slide_matches_the_provisional_corpus_not_an_undefined_subset():
    scope = read_rows("research/data/current_synthesis_scope.csv")
    retained = sum(row["record_status"] == "included_empirical_core" for row in scope)
    slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
    metric = re.search(
        r'tcc-synthesis-orbit[\s\S]*?<strong>(\d+)</strong><span>(.*?)</span>', slides
    )
    assert metric and int(metric[1]) == retained
    assert "provis" in metric[2]
    synthesis = slides.split("17 / SÍNTESE", 1)[1].split("\n---", 1)[0]
    assert "inferem proficiência" not in synthesis
    assert "categorias operacionais de desempenho" in synthesis.casefold()


def test_pending_design_keeps_screening_but_does_not_rate_undefined_criteria():
    rows = read_rows("research/data/mmat_reassessment_current.csv")
    for row in rows:
        if row["study_id"] not in {"5", "7", "14"}:
            continue
        assert row["design"] == "design_pending"
        assert row["s1"] == row["s2"] == "Y"
        assert all(not row[criterion] for criterion in mmat_current.REQUIRED_CRITERIA)
        assert len(row["criterion_evidence"].split(";")) == 2


def test_pending_design_rejects_ct_as_if_a_category_criterion_had_been_appraised(monkeypatch):
    original = mmat_current._read_csv

    def read(path):
        rows = original(path)
        if path == mmat_current.REASSESSMENT_PATH:
            row = next(item for item in rows if item["study_id"] == "5")
            for criterion in mmat_current.REQUIRED_CRITERIA:
                row[criterion] = "CT"
            row["criterion_evidence"] = (
                "S1=Y clear aim;S2=Y relevant data;"
                + ";".join(f"Q{i}=CT category not chosen" for i in range(1, 6))
            )
        return rows

    monkeypatch.setattr(mmat_current, "_read_csv", read)
    with pytest.raises(ValueError, match="unresolved MMAT design"):
        mmat_current.load_current_reassessment()


def test_qa_distinguishes_screening_from_category_specific_appraisal():
    report = mmat_current.validate_current_artifacts()
    assert report["screening_rows"] == 14
    assert report["category_appraised_rows"] == 11
    assert report["category_pending_ids"] == ["5", "7", "14"]
    assert report["empirical_evidence_rows"] == 15


def test_screening_disclosure_matches_the_recorded_operational_reasons():
    rows = read_rows("research/exports/analysis/papers.csv")
    methodology = (ROOT / "results/tcc/conteudo/metodologia.tex").read_text(encoding="utf-8")
    reasons = {"abstract_too_short", "no_methodology", "inclusion_criteria_not_met", "non_research", "off_topic"}
    counts = {reason: sum(row["exclusion_reason"] == reason for row in rows) for reason in reasons}
    assert sum(counts.values()) == 9391
    for count in counts.values():
        assert f"{count:,}".replace(",", ".") in methodology
    missing = sum(row["exclusion_reason"] == "abstract_too_short" and row["abstract"] == "Abstract não disponível" for row in rows)
    assert f"{missing:,}".replace(",", ".") in methodology
    assert "falsos negativos" in methodology


def test_requirement_origins_are_explicit_without_fabricated_empirical_support():
    matrix = (ROOT / "results/tcc/conteudo/rastreabilidade-requisitos.tex").read_text(encoding="utf-8")
    assert re.findall(r"^R(\d{2}) &", matrix, flags=re.MULTILINE) == [f"{i:02}" for i in range(1, 27)]
    assert "decisões de projeto do autor" in matrix
    assert "não como achados empíricos" in matrix
    bib = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "results/tcc").glob("*.bib"))
    bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", bib))
    for cite in re.findall(r"\\cite(?:online)?(?:\[[^]]*\])*\{([^}]+)\}", matrix):
        assert set(cite.split(",")) <= bib_keys
    prototype = (ROOT / "results/tcc/conteudo/prototipo.tex").read_text(encoding="utf-8")
    assert r"\input{conteudo/rastreabilidade-requisitos}" in prototype


def test_readme_distinguishes_shortlist_from_provisional_empirical_inclusion():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "17 candidatos empíricos provisórios" not in text
    assert "15 estudos empíricos mantidos provisoriamente" in text
    assert "14 triagens S1/S2" in text and "11 apreciações por categoria" in text
