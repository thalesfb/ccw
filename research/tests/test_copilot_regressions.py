"""Regression tests for false-positive findings raised by Copilot."""

from research.src.processing.scoring import extract_techniques
from research.src.processing.selection import PRISMASelector


def test_generic_assessment_skills_and_competencies_are_not_learning_analytics() -> None:
    text = (
        "This study assesses mathematics skills and competencies in secondary "
        "education through classroom observations."
    )

    assert "learning_analytics" not in extract_techniques(text)


def test_ai_is_matched_as_a_word_in_scoring() -> None:
    assert "machine_learning" not in extract_techniques(
        "This study aims to describe mathematics education outcomes."
    )
    assert "machine_learning" in extract_techniques(
        "This study uses AI to model mathematics learning outcomes."
    )


def test_ai_is_matched_as_a_word_in_selection() -> None:
    selector = PRISMASelector()
    paper = {
        "year": 2025,
        "title": "Aims of mathematics education",
        "abstract": (
            "This study aims to assess mathematics skills and competencies "
            "through classroom observations in secondary education."
        ),
    }

    _, criteria = selector.apply_inclusion_criteria(paper)

    assert "computational_techniques" not in criteria
