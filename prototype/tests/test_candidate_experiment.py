import json
from pathlib import Path

from tcc_prototype.modeling.candidate_experiment import (
    run_candidate_experiment,
    write_candidate_artifacts,
)
from test_baseline_experiment import _synthetic_interactions


def test_candidate_experiment_adds_model_explanations_and_profiles() -> None:
    result = run_candidate_experiment(
        _synthetic_interactions(),
        split_strategy="cold_start",
        seed=2026,
        n_estimators=25,
        min_samples_leaf=1,
        minimum_profile_evidence=3,
        explanation_rows=3,
        permutation_repeats=2,
    )

    assert "random_forest" in result.metrics
    assert "random_forest_probability" in result.predictions.columns
    assert len(result.permutation_importance) > 0
    assert len(result.logistic_explanations) == 3
    assert not result.skill_profiles.empty
    assert set(result.skill_profiles["evidence_status"]) == {"estimated"}
    assert result.skill_profiles["level"].isna().all()


def test_candidate_artifacts_are_machine_readable(tmp_path: Path) -> None:
    result = run_candidate_experiment(
        _synthetic_interactions(),
        split_strategy="temporal",
        seed=2026,
        n_estimators=20,
        min_samples_leaf=1,
        minimum_profile_evidence=1,
        explanation_rows=2,
        permutation_repeats=2,
    )

    artifacts = write_candidate_artifacts(result, output_dir=tmp_path)

    assert artifacts.metrics_path.exists()
    assert artifacts.predictions_path.exists()
    assert artifacts.importance_path.exists()
    assert artifacts.profiles_path.exists()
    assert artifacts.explanations_path.exists()
    metrics = json.loads(artifacts.metrics_path.read_text(encoding="utf-8"))
    explanations = json.loads(
        artifacts.explanations_path.read_text(encoding="utf-8")
    )
    assert metrics["models"]["random_forest"]["observations"] > 0
    assert explanations[0]["interpretation_limit"]
