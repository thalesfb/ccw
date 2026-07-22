import json
from pathlib import Path

import pandas as pd

from tcc_prototype.modeling.experiment import (
    run_baseline_experiment,
    write_baseline_artifacts,
)


def _synthetic_interactions() -> pd.DataFrame:
    rows = []
    for student in range(12):
        for order in range(10):
            skill = "fractions" if order % 2 == 0 else "ratio"
            correct = (student + order) % 3 != 0
            rows.append(
                {
                    "student_id": f"s{student}",
                    "item_id": f"i{order % 4}",
                    "skill_ids": [skill],
                    "interaction_order": order,
                    "correct": correct,
                    "source_row_id": f"{student}-{order}",
                }
            )
    return pd.DataFrame(rows)


def test_baseline_experiment_compares_required_models() -> None:
    result = run_baseline_experiment(
        _synthetic_interactions(),
        split_strategy="cold_start",
        seed=2026,
    )

    assert set(result.metrics) == {
        "global_probability",
        "item_probability",
        "skill_probability",
        "student_history_probability",
        "logistic_regression",
    }
    assert set(result.predictions["split"]) == {"test"}
    assert result.predictions["student_id"].nunique() > 0
    for model_name in result.metrics:
        assert f"{model_name}_probability" in result.predictions.columns
        assert 0 <= result.metrics[model_name]["brier_score"] <= 1
    assert result.skill_metrics


def test_write_baseline_artifacts_creates_auditable_outputs(tmp_path: Path) -> None:
    result = run_baseline_experiment(
        _synthetic_interactions(),
        split_strategy="temporal",
        seed=2026,
    )

    artifacts = write_baseline_artifacts(result, output_dir=tmp_path)

    assert artifacts.metrics_path.exists()
    assert artifacts.predictions_path.exists()
    assert artifacts.splits_path.exists()
    metrics = json.loads(artifacts.metrics_path.read_text(encoding="utf-8"))
    assert metrics["split_strategy"] == "temporal"
    assert metrics["seed"] == 2026
    assert metrics["models"]["global_probability"]["observations"] > 0
    persisted_predictions = pd.read_parquet(artifacts.predictions_path)
    assert len(persisted_predictions) == len(result.predictions)
