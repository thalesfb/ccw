"""Tests for the MMAT (Mixed Methods Appraisal Tool) 2018 assessment module."""

import pytest

from src.analysis.mmat_assessment import (
    MMAT_ASSESSMENTS,
    MMAT_CRITERIA,
    VALID_RESPONSES,
    classify_study_design,
    compute_mmat_score,
    get_quality_rating,
    get_quality_rating_en,
)


class TestMmatAssessmentData:
    """Validate the integrity of the hardcoded MMAT assessment data."""

    def test_all_17_studies_assessed(self):
        """All 17 included studies must have an assessment entry."""
        assert len(MMAT_ASSESSMENTS) == 17

    def test_each_study_has_exactly_5_criteria(self):
        """Each assessment must have exactly 5 criteria (Q1-Q5)."""
        for key, entry in MMAT_ASSESSMENTS.items():
            criteria = entry["criteria"]
            assert len(criteria) == 5, f"{key} has {len(criteria)} criteria, expected 5"
            assert set(criteria.keys()) == {"Q1", "Q2", "Q3", "Q4", "Q5"}, (
                f"{key} criteria keys mismatch: {set(criteria.keys())}"
            )

    def test_scores_between_1_and_5(self):
        """All MMAT scores must be in the range [1, 5]."""
        for key, entry in MMAT_ASSESSMENTS.items():
            score = entry["score"]
            assert 1 <= score <= 5, f"{key} has score {score}, expected 1-5"

    def test_criteria_values_are_valid(self):
        """Each criterion response must be Y, N, or CT."""
        for key, entry in MMAT_ASSESSMENTS.items():
            for qk, qv in entry["criteria"].items():
                assert qv in VALID_RESPONSES, (
                    f"{key}.{qk} = '{qv}' is not a valid MMAT response"
                )

    def test_score_matches_criteria_yes_count(self):
        """Score must equal the number of 'Y' responses in criteria."""
        for key, entry in MMAT_ASSESSMENTS.items():
            expected = sum(1 for v in entry["criteria"].values() if v == "Y")
            assert entry["score"] == expected, (
                f"{key}: score={entry['score']} but Y count={expected}"
            )

    def test_each_study_has_valid_design(self):
        """Each assessment design must be a valid MMAT category."""
        valid_designs = set(MMAT_CRITERIA.keys())
        for key, entry in MMAT_ASSESSMENTS.items():
            assert entry["design"] in valid_designs, (
                f"{key} design '{entry['design']}' not in {valid_designs}"
            )

    def test_each_study_has_limitations(self):
        """Each assessment must document limitations."""
        for key, entry in MMAT_ASSESSMENTS.items():
            assert entry.get("limitations"), f"{key} is missing limitations"
            assert len(entry["limitations"]) > 10, (
                f"{key} limitations too short: '{entry['limitations']}'"
            )


class TestMmatCriteria:
    """Validate the MMAT criteria definitions."""

    def test_all_five_designs_defined(self):
        """MMAT criteria must cover all 5 study designs."""
        expected = {
            "qualitative",
            "quantitative_randomized",
            "quantitative_nonrandomized",
            "quantitative_descriptive",
            "mixed_methods",
        }
        assert set(MMAT_CRITERIA.keys()) == expected

    def test_each_design_has_5_questions(self):
        """Each design category must have exactly 5 criteria questions."""
        for design, criteria in MMAT_CRITERIA.items():
            assert len(criteria) == 5, f"{design} has {len(criteria)} criteria"
            assert set(criteria.keys()) == {"Q1", "Q2", "Q3", "Q4", "Q5"}


class TestHelperFunctions:
    """Test helper/utility functions."""

    def test_compute_mmat_score_all_yes(self):
        criteria = {"Q1": "Y", "Q2": "Y", "Q3": "Y", "Q4": "Y", "Q5": "Y"}
        assert compute_mmat_score(criteria) == 5

    def test_compute_mmat_score_all_no(self):
        criteria = {"Q1": "N", "Q2": "N", "Q3": "N", "Q4": "N", "Q5": "N"}
        assert compute_mmat_score(criteria) == 0

    def test_compute_mmat_score_mixed(self):
        criteria = {"Q1": "Y", "Q2": "CT", "Q3": "Y", "Q4": "N", "Q5": "Y"}
        assert compute_mmat_score(criteria) == 3

    def test_quality_rating_high(self):
        assert get_quality_rating(5) == "Alta"
        assert get_quality_rating(4) == "Alta"

    def test_quality_rating_moderate(self):
        assert get_quality_rating(3) == "Moderada"

    def test_quality_rating_low(self):
        assert get_quality_rating(2) == "Baixa"

    def test_quality_rating_very_low(self):
        assert get_quality_rating(1) == "Muito Baixa"
        assert get_quality_rating(0) == "Muito Baixa"

    def test_quality_rating_en(self):
        assert get_quality_rating_en(5) == "High"
        assert get_quality_rating_en(3) == "Moderate"
        assert get_quality_rating_en(2) == "Low"
        assert get_quality_rating_en(0) == "Very Low"

    def test_classify_mixed_methods(self):
        assert classify_study_design("A mixed method study", "") == "mixed_methods"

    def test_classify_qualitative(self):
        assert classify_study_design("", "qualitative interview study") == "qualitative"

    def test_classify_randomized(self):
        assert classify_study_design("A randomized controlled trial", "") == "quantitative_randomized"

    def test_classify_nonrandomized(self):
        assert classify_study_design("", "quasi-experimental design") == "quantitative_nonrandomized"

    def test_classify_default_descriptive(self):
        assert classify_study_design("Machine learning prediction", "data mining") == "quantitative_descriptive"
