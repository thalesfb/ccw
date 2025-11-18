import pytest

from research.src.processing.scoring import is_relevant_paper


def test_finance_paper_is_not_relevant():
    # Simulated record for the problematic paper (finance/stock market)
    paper = {
        "title": "Stock Market Prediction using Machine Learning Techniques: A Systematic Review",
        "abstract": "This review surveys stock market prediction literature using ML, forecasting, and financial indicators.",
        "year": 2021,
    }

    # No education keywords configured -> rely on EDU_MATH detection (should fail)
    keep, reason = is_relevant_paper(paper, year_min=2015, langs=["en"], keywords=[], tech_terms=[])
    assert keep is False
    assert "educacional" in reason or "Sem foco" in reason or reason != ""
