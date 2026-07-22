import pandas as pd

from tcc_prototype.profiles import OrdinalThresholds, build_skill_profiles


def _predictions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "student_id": ["s1", "s1", "s1", "s1", "s1", "s2", "s2"],
            "primary_skill_id": [
                "fractions",
                "fractions",
                "fractions",
                "ratio",
                "ratio",
                "fractions",
                "fractions",
            ],
            "target": [0, 1, 0, 1, 1, 1, 1],
            "random_forest_probability": [0.25, 0.35, 0.30, 0.80, 0.75, 0.90, 0.85],
        }
    )


def test_profile_marks_groups_with_little_evidence_as_insufficient() -> None:
    profile = build_skill_profiles(
        _predictions(),
        probability_column="random_forest_probability",
        minimum_evidence=3,
    )

    s1_fractions = profile.loc[
        (profile["student_id"] == "s1")
        & (profile["skill_id"] == "fractions")
    ].iloc[0]
    s1_ratio = profile.loc[
        (profile["student_id"] == "s1") & (profile["skill_id"] == "ratio")
    ].iloc[0]

    assert s1_fractions["evidence_status"] == "estimated"
    assert s1_fractions["predicted_probability"] == 0.3
    assert s1_fractions["level"] is None
    assert s1_ratio["evidence_status"] == "insufficient_evidence"
    assert s1_ratio["level"] is None


def test_profile_applies_only_explicit_versioned_thresholds() -> None:
    thresholds = OrdinalThresholds(
        version="validation-v1",
        high_fragility_upper=0.4,
        monitoring_upper=0.6,
        developing_upper=0.8,
    )

    profile = build_skill_profiles(
        _predictions(),
        probability_column="random_forest_probability",
        minimum_evidence=2,
        thresholds=thresholds,
    )

    levels = {
        (row.student_id, row.skill_id): row.level
        for row in profile.itertuples()
    }
    assert levels[("s1", "fractions")] == "high_fragility"
    assert levels[("s1", "ratio")] == "developing"
    assert levels[("s2", "fractions")] == "probable_mastery"
    assert set(profile["threshold_version"]) == {"validation-v1"}


def test_thresholds_must_be_strictly_increasing() -> None:
    try:
        OrdinalThresholds(
            version="invalid",
            high_fragility_upper=0.6,
            monitoring_upper=0.5,
            developing_upper=0.8,
        )
    except ValueError as error:
        assert "strictly increasing" in str(error)
    else:
        raise AssertionError("invalid thresholds must fail")
