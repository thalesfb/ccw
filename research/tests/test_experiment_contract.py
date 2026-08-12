import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_PATH = REPO_ROOT / "prototype" / "config" / "experiment.json"
INTERACTION_SCHEMA_PATH = (
    REPO_ROOT / "prototype" / "contracts" / "interaction.schema.json"
)
DESIGN_PATH = REPO_ROOT / "docs" / "TCC_EXPERIMENTAL_DESIGN.md"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_experiment_target_has_explicit_prediction_anchor() -> None:
    experiment = _load_json(EXPERIMENT_PATH)
    target = experiment["target"]

    assert target["name"] == "correct_next"
    assert target["horizon"] == "one_eligible_interaction_ahead"
    assert target["prediction_anchor"] == "immediately_before_target_response"
    assert target["label_source"] == "correct field of the target interaction"
    assert {"item_id", "skill_ids"} <= set(
        target["target_context_known_before_response"]
    )


def test_target_event_outcomes_are_forbidden_as_primary_features() -> None:
    experiment = _load_json(EXPERIMENT_PATH)
    forbidden = set(experiment["target"]["forbidden_target_event_features"])

    assert {
        "correct",
        "answer",
        "attempt_count",
        "hint_count",
        "elapsed_time_ms",
    } <= forbidden


def test_interaction_schema_matches_experiment_required_columns() -> None:
    experiment = _load_json(EXPERIMENT_PATH)
    interaction_schema = _load_json(INTERACTION_SCHEMA_PATH)

    assert set(experiment["required_columns"]) == set(interaction_schema["required"])
    assert interaction_schema["properties"]["correct"]["type"] == "boolean"
    assert "unavailable at prediction time" in interaction_schema["properties"]["correct"][
        "description"
    ]


def test_primary_splits_preserve_student_and_temporal_structure() -> None:
    experiment = _load_json(EXPERIMENT_PATH)
    splits = experiment["splits"]

    assert set(splits) == {"student_holdout", "personalized_temporal"}
    assert splits["student_holdout"]["strategy"] == "group_by_student"
    assert (
        splits["student_holdout"]["model_parameters_may_use_held_out_students"]
        is False
    )
    assert (
        splits["personalized_temporal"]["strategy"]
        == "chronological_within_student"
    )
    assert "no random row split in the primary protocol" in experiment["guardrails"]


def test_eligibility_threshold_is_deferred_until_dataset_characterization() -> None:
    experiment = _load_json(EXPERIMENT_PATH)
    eligibility = experiment["eligibility"]

    assert eligibility["minimum_interactions_per_student"] is None
    assert (
        eligibility["threshold_freeze_stage"]
        == "after_dataset_characterization_before_split_generation"
    )
    assert eligibility["threshold_rationale_required"] is True
    assert (
        "eligibility thresholds are justified and frozen before split generation"
        in experiment["guardrails"]
    )


def test_test_support_thresholds_are_not_selected_from_test_performance() -> None:
    experiment = _load_json(EXPERIMENT_PATH)
    support = experiment["reporting"]["skill_support"]

    assert support["minimum_test_rows"] is None
    assert support["minimum_test_students"] is None
    assert support["freeze_stage"] == "after_dataset_selection_before_test_evaluation"
    assert support["below_threshold_behavior"] == "report_insufficient_evidence"


def test_predefined_seeds_cannot_be_cherry_picked() -> None:
    experiment = _load_json(EXPERIMENT_PATH)

    assert len(experiment["random_seeds"]) >= 2
    assert (
        experiment["seed_policy"]
        == "report_all_predefined_seeds_without_best_seed_selection"
    )


def test_documented_design_contains_core_inference_boundaries() -> None:
    design = DESIGN_PATH.read_text(encoding="utf-8")

    required_markers = [
        "## Âncora e horizonte de previsão",
        "`correct_next`",
        "`student_holdout`",
        "## Conclusões permitidas e proibidas",
        "não equivale necessariamente a `cold start`",
    ]

    for marker in required_markers:
        assert marker in design
