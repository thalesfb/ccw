import pandas as pd

from tcc_prototype.modeling.baselines import SmoothedProbabilityBaseline


def test_global_baseline_predicts_training_prevalence() -> None:
    train = pd.DataFrame({"target": [1, 1, 0, 0, 1]})
    test = pd.DataFrame(index=[10, 11])

    model = SmoothedProbabilityBaseline(group_columns=()).fit(train)
    predictions = model.predict_proba(test)

    assert predictions.tolist() == [0.6, 0.6]


def test_group_baseline_smooths_known_groups_and_falls_back_to_global() -> None:
    train = pd.DataFrame(
        {
            "primary_skill_id": ["fractions", "fractions", "ratio", "ratio"],
            "target": [1, 1, 0, 0],
        }
    )
    test = pd.DataFrame(
        {"primary_skill_id": ["fractions", "ratio", "geometry"]}
    )

    model = SmoothedProbabilityBaseline(
        group_columns=("primary_skill_id",),
        prior_strength=2.0,
    ).fit(train)
    predictions = model.predict_proba(test)

    assert predictions.tolist() == [0.75, 0.25, 0.5]


def test_baseline_rejects_prediction_before_fit() -> None:
    model = SmoothedProbabilityBaseline(group_columns=())

    try:
        model.predict_proba(pd.DataFrame(index=[0]))
    except RuntimeError as error:
        assert "fit" in str(error)
    else:
        raise AssertionError("prediction before fit must fail")
