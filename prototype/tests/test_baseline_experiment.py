import hashlib
import json
import tomllib
from pathlib import Path

import pandas as pd
import pytest

from tcc_prototype import __version__
from tcc_prototype.cli import _load_preparation_provenance, build_parser
from tcc_prototype.modeling.experiment import (
    ExperimentConfigError,
    run_baseline_experiment,
    validate_experiment_execution_config,
    write_baseline_artifacts,
)
from tcc_prototype.modeling.features import build_history_features
from tcc_prototype.modeling.models import hashed_tree_features


def _interactions(students: int = 18, rows: int = 12) -> pd.DataFrame:
    data = []
    for student in range(students):
        for order in range(rows):
            skills = (
                ["fractions", "ratio"]
                if order == 2
                else (["fractions"] if order % 2 == 0 else ["ratio"])
            )
            data.append(
                {
                    "student_id": f"s{student}",
                    "item_id": f"i{order % 5}",
                    "skill_ids": skills,
                    "interaction_order": order,
                    "correct": (student + order) % 3 != 0,
                    "source_dataset": "synthetic",
                    "source_row_id": f"{student}-{order}",
                }
            )
    return pd.DataFrame(data)


def _config() -> dict:
    return {
        "schema_version": "1.2.0-test",
        "eligibility": {"minimum_interactions_per_student": 3},
        "random_seeds": [2026, 1701, 31415],
        "splits": {
            "student_holdout": {
                "train_fraction": 0.7,
                "validation_fraction": 0.15,
                "test_fraction": 0.15,
            },
            "personalized_temporal": {
                "train_fraction": 0.7,
                "validation_fraction": 0.15,
                "test_fraction": 0.15,
            },
        },
        "evaluation_execution": {
            "classification_threshold": 0.5,
            "calibration_bins": 5,
            "smoothing_strengths": [1.0, 5.0],
            "logistic_regression": {
                "c_values": [0.1, 1.0],
                "max_iter": 500,
            },
            "hist_gradient_boosting": {
                "learning_rate_values": [0.1],
                "max_leaf_nodes_values": [15],
                "l2_regularization_values": [0.0],
                "max_iter": 20,
                "hash_features": 8,
            },
        },
        "reporting": {
            "skill_support": {
                "minimum_test_rows": 1,
                "minimum_test_students": 1,
            },
            "subgroup_audit": {"columns": []},
            "bootstrap": {"iterations": 50},
        },
    }


def test_execution_refuses_unfrozen_dataset_specific_thresholds() -> None:
    config = _config()
    config["eligibility"]["minimum_interactions_per_student"] = None

    with pytest.raises(ExperimentConfigError, match="minimum_interactions_per_student"):
        validate_experiment_execution_config(config)


def test_experiment_compares_required_models_without_test_tuning() -> None:
    result = run_baseline_experiment(
        _interactions(),
        config=_config(),
        split_strategy="student_holdout",
        seed=2026,
    )

    assert set(result.test_metrics) == {
        "global_probability",
        "item_smoothed_probability",
        "skill_smoothed_probability",
        "student_history_smoothed_probability",
        "logistic_regression",
        "hist_gradient_boosting",
    }
    assert (
        result.selected_parameters["best_simple_historical_baseline"][
            "selection_partition"
        ]
        == "validation"
    )
    assert result.selected_parameters["logistic_regression"]["fit_partition"] == "train_only"
    assert result.selected_parameters["hist_gradient_boosting"]["early_stopping"] is False
    assert set(result.skill_metrics) == {"fractions", "ratio"}
    assert result.subgroup_metrics["status"] == "not_applicable"
    assert result.cold_start_slice is not None
    assert "H2_logistic_vs_best_simple" in result.hypothesis_comparisons


def test_nonlinear_context_hash_is_fixed_width_and_target_independent() -> None:
    frame = build_history_features(_interactions(students=2, rows=4))
    features = hashed_tree_features(frame, hash_features=8)
    changed = frame.copy()
    changed["target"] = 1 - changed["target"]

    assert features.shape == (8, 14)
    assert (features == hashed_tree_features(changed, hash_features=8)).all()


def test_cli_uses_configured_seed_set_and_preparation_provenance() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "evaluate-baselines",
            "--input",
            "data.parquet",
            "--preparation-report",
            "data.quality.json",
            "--output-dir",
            "reports",
            "--experiment-config",
            "experiment.json",
            "--split-strategy",
            "student_holdout",
        ]
    )

    assert args.split_strategy == "student_holdout"
    assert args.preparation_report == Path("data.quality.json")
    assert not hasattr(args, "seed")


def test_preparation_provenance_verifies_processed_input_hash(tmp_path: Path) -> None:
    prepared = tmp_path / "prepared.parquet"
    prepared.write_bytes(b"prepared-input")
    processed_hash = hashlib.sha256(prepared.read_bytes()).hexdigest()
    source_hash = hashlib.sha256(b"raw-source").hexdigest()
    report = tmp_path / "prepared.quality.json"
    report.write_text(
        json.dumps(
            {
                "dataset_id": "synthetic",
                "dataset_version": "v1",
                "source_sha256": source_hash,
                "processed_sha256": processed_hash,
            }
        ),
        encoding="utf-8",
    )

    provenance = _load_preparation_provenance(report, prepared)

    assert provenance["source_sha256"] == source_hash
    assert provenance["processed_input_sha256"] == processed_hash
    assert provenance["preparation_report_sha256"] == hashlib.sha256(
        report.read_bytes()
    ).hexdigest()

    prepared.write_bytes(b"changed-after-report")
    with pytest.raises(ValueError, match="processed input SHA-256 mismatch"):
        _load_preparation_provenance(report, prepared)


def test_artifacts_record_hashes_and_refuse_silent_overwrite(tmp_path: Path) -> None:
    result = run_baseline_experiment(
        _interactions(),
        config=_config(),
        split_strategy="personalized_temporal",
        seed=1701,
    )
    source_hash = hashlib.sha256(b"source").hexdigest()
    config_hash = hashlib.sha256(
        json.dumps(_config(), sort_keys=True).encode("utf-8")
    ).hexdigest()

    artifacts = write_baseline_artifacts(
        result,
        output_dir=tmp_path,
        source_sha256=source_hash,
        config_sha256=config_hash,
    )
    payload = json.loads(artifacts.metrics_path.read_text(encoding="utf-8"))

    assert payload["source_sha256"] == source_hash
    assert payload["config_sha256"] == config_hash
    assert len(payload["predictions_sha256"]) == 64
    assert len(payload["splits_sha256"]) == 64
    with pytest.raises(FileExistsError):
        write_baseline_artifacts(
            result,
            output_dir=tmp_path,
            source_sha256=source_hash,
            config_sha256=config_hash,
        )


def test_package_version_matches_pyproject() -> None:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    project = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))["project"]

    assert __version__ == project["version"]
