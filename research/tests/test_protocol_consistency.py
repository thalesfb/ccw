import json
from pathlib import Path

from src.search_terms import generate_search_queries


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = RESEARCH_ROOT.parent
SUMMARY_PATH = RESEARCH_ROOT / "exports" / "reports" / "summary.json"
MANIFEST_PATH = RESEARCH_ROOT / "protocol_execution_2025.json"
RESEARCH_README = RESEARCH_ROOT / "README.md"
EXPORTS_README = RESEARCH_ROOT / "exports" / "README.md"
INTRO_PATH = REPO_ROOT / "results" / "tcc" / "conteudo" / "introducao.tex"
METHOD_PATH = REPO_ROOT / "results" / "tcc" / "conteudo" / "metodologia.tex"
REVIEW_PATH = REPO_ROOT / "results" / "tcc" / "conteudo" / "resultadosesperados.tex"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_versioned_search_strategy_has_72_canonical_queries() -> None:
    queries = generate_search_queries()
    assert len(queries) == 72
    assert len([q for q in queries if q.startswith(("mathematics ", "math "))]) == 48
    assert len([q for q in queries if q.startswith("matemática ")]) == 24


def test_preserved_summary_matches_tcc_corpus_counts() -> None:
    summary = json.loads(_read(SUMMARY_PATH))
    stats = summary["statistics"]
    assert stats["total_papers"] == 9431
    assert stats["prisma"]["duplicates_removed"] == 2517
    assert stats["prisma"]["screening"] == 6914
    assert stats["prisma"]["eligibility"] == 1883
    assert stats["prisma"]["included"] == 17
    assert stats["years"]["min"] == 2015
    assert stats["years"]["max"] == 2025
    assert stats["databases"] == {
        "crossref": 2865,
        "openalex": 1817,
        "semantic_scholar": 1786,
        "core": 446,
    }


def test_execution_manifest_records_evidence_and_limits() -> None:
    manifest = json.loads(_read(MANIFEST_PATH))
    assert manifest["status"] == "reconstructed_from_versioned_artifacts"
    assert manifest["search_strategy"]["canonical_query_count"] == 72
    assert manifest["search_strategy"]["query_count_evidence"] == (
        "versioned_strategy_not_http_request_audit"
    )
    assert manifest["eligibility"]["year_min"] == 2015
    assert manifest["eligibility"]["year_max"] == 2025
    assert manifest["counts"]["identified"] == 9431
    assert manifest["counts"]["included"] == 17
    assert manifest["limitations"]["per_query_request_log_preserved"] is False
    assert manifest["limitations"]["execution_database_versioned"] is False


def test_tcc_reports_executed_temporal_window_consistently() -> None:
    intro = _read(INTRO_PATH)
    method = _read(METHOD_PATH)
    review = _read(REVIEW_PATH)

    assert "2015 e 2025" in intro
    assert "2015 a 2025" in method
    assert "2015--2025" in review
    assert "2016 e 2025" not in intro
    assert "2016 a 2025" not in method
    assert "2016--2025" not in review


def test_documentation_does_not_preserve_stale_protocol_numbers() -> None:
    research_readme = _read(RESEARCH_README)
    exports_readme = _read(EXPORTS_README)

    assert "72 consultas canônicas" in research_readme
    assert "108 queries" not in research_readme
    assert "12.533" not in exports_readme
    assert "43 papers" not in exports_readme
    assert "systematic_review.sqlite" in research_readme
    assert "não é versionado" in research_readme
