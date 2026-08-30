import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

from src.processing.scoring import extract_techniques
from src.processing.selection import PRISMASelector
from src.search_terms import generate_search_queries


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = RESEARCH_ROOT.parent
SUMMARY_PATH = RESEARCH_ROOT / "exports" / "reports" / "summary.json"
INCLUDED_REPORT_PATH = RESEARCH_ROOT / "exports" / "reports" / "papers_report_included.html"
MANIFEST_PATH = RESEARCH_ROOT / "protocol_execution_2025.json"
REFERENCE_AUDIT_PATH = RESEARCH_ROOT / "data" / "reference_audit.csv"
SELECTION_PATH = RESEARCH_ROOT / "src" / "processing" / "selection.py"
RESEARCH_README = RESEARCH_ROOT / "README.md"
EXPORTS_README = RESEARCH_ROOT / "exports" / "README.md"
INTRO_PATH = REPO_ROOT / "results" / "tcc" / "conteudo" / "introducao.tex"
METHOD_PATH = REPO_ROOT / "results" / "tcc" / "conteudo" / "metodologia.tex"
REVIEW_PATH = REPO_ROOT / "results" / "tcc" / "conteudo" / "resultadosesperados.tex"
APPENDIX_PATH = REPO_ROOT / "results" / "tcc" / "postextuais" / "apendice.tex"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _included_report_papers() -> list[dict]:
    soup = BeautifulSoup(_read(INCLUDED_REPORT_PATH), "html.parser")
    papers: list[dict] = []
    for block in soup.select("div.paper"):
        title_node = block.select_one("div.paper-title")
        abstract_node = block.select_one("div.paper-abstract")
        meta_node = block.select_one("div.paper-meta")
        if not title_node or not abstract_node or not meta_node:
            continue
        meta = meta_node.get_text(" ", strip=True)
        year_match = re.search(r"Ano:\s*(\d{4})", meta)
        papers.append(
            {
                "title": title_node.get_text(" ", strip=True),
                "abstract": abstract_node.get_text(" ", strip=True).removeprefix("Resumo:").strip(),
                "year": int(year_match.group(1)) if year_match else None,
            }
        )
    return papers


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


def test_manifest_records_operational_selection_instead_of_idealized_criteria() -> None:
    manifest = json.loads(_read(MANIFEST_PATH))
    operational = manifest["operational_selection"]

    assert operational["required_automated_criteria"] == [
        "year_range",
        "math_focus",
        "computational_techniques",
    ]
    assert operational["language_is_required_criterion"] is False
    assert operational["peer_review_document_type_filter"] is False
    assert operational["full_text_review_enforced_by_pipeline"] is False


def test_methodology_discloses_document_type_and_language_operationalization() -> None:
    method = _read(METHOD_PATH)
    reference_audit = _read(REFERENCE_AUDIT_PATH)
    selection_source = _read(SELECTION_PATH)

    assert "doctoral dissertation" in reference_audit
    assert "book chapter" in reference_audit
    assert 'required = ["year_range", "math_focus", "computational_techniques"]' in selection_source

    assert "artigos completos revisados por pares" not in method
    assert "dissertação" in method.lower()
    assert "capítulo de livro" in method.lower()
    assert "não foi um critério obrigatório" in method.lower()
    assert "texto completo" in method.lower()
    assert "não foi exigida" in method.lower()


def test_review_limitations_and_prisma_reflect_operational_selection_limits() -> None:
    review = _read(REVIEW_PATH).lower()
    appendix = _read(APPENDIX_PATH).lower()

    assert "busca foi limitada a português e inglês" not in review
    assert "idioma não foi critério obrigatório" in review
    assert "tipo documental" in review
    assert "texto completo" in review

    assert "operacionalização" in appendix
    assert "tipo documental" in appendix
    assert "texto completo" in appendix


def test_ai_token_does_not_match_substrings_inside_ordinary_words() -> None:
    selector = PRISMASelector()
    false_positive_texts = [
        "This study aims to examine formative assessment in mathematics.",
        "Teacher training supports mathematics assessment in rural schools.",
        "Ghanaian students studied geometry with cooperative learning.",
    ]

    for abstract in false_positive_texts:
        meets, criteria = selector.apply_inclusion_criteria(
            {"title": "Mathematics education study", "abstract": abstract, "year": 2024}
        )
        assert "computational_techniques" not in criteria
        assert meets is False
        assert "machine_learning" not in extract_techniques(abstract)

    explicit_ai = "Artificial intelligence and machine learning for mathematics education."
    meets, criteria = selector.apply_inclusion_criteria(
        {"title": "Mathematics education", "abstract": explicit_ai, "year": 2024}
    )
    assert "computational_techniques" in criteria
    assert meets is True
    assert "machine_learning" in extract_techniques(explicit_ai)


def test_corrected_selector_flags_only_three_preserved_included_records_for_reaudit() -> None:
    selector = PRISMASelector()
    papers = _included_report_papers()
    assert len(papers) == 17

    flagged = {
        paper["title"]
        for paper in papers
        if not selector.apply_inclusion_criteria(paper)[0]
    }

    assert flagged == {
        "Enhancing Student Achievement in Circle Theorems: Integrating Computer Animation with the Jigsaw Cooperative Learning Model",
        "Authentic Assessment for Motivating Student Learning and Teaching Effectiveness in Rural, High-Need Secondary Schools in Manitoba, Canada",
        "Performance assessment: Improving metacognitive ability in mathematics learning",
    }
