"""Conservative continuous evidence profiles derived from held-out predictions."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

from .modeling.features import normalize_skill_ids


class ProfileConfigError(ValueError):
    """Raised when profile-specific choices have not been frozen safely."""


def load_profile_config(path: Path) -> dict[str, Any]:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileConfigError(f"unable to read profile config {path}: {exc}") from exc
    validate_profile_config(config)
    return config


def validate_profile_config(config: dict[str, Any]) -> None:
    """Require profile choices that must be justified before test-derived output."""

    if not str(config.get("schema_version", "")).strip():
        raise ProfileConfigError("schema_version is required")

    probability_source = config.get("probability_source")
    if not isinstance(probability_source, str) or not probability_source.strip():
        raise ProfileConfigError(
            "probability_source must be frozen from validation before profile generation"
        )

    minimum_evidence = config.get("minimum_student_skill_interactions")
    if (
        not isinstance(minimum_evidence, int)
        or isinstance(minimum_evidence, bool)
        or minimum_evidence < 1
    ):
        raise ProfileConfigError(
            "minimum_student_skill_interactions must be a frozen positive integer"
        )

    if config.get("ordinal_levels", {}).get("enabled") is not False:
        raise ProfileConfigError(
            "ordinal_levels must remain disabled until separately justified and validated"
        )
    if config.get("binary_alert", {}).get("enabled") is not False:
        raise ProfileConfigError(
            "binary_alert must remain disabled until separately justified and validated"
        )


def _wilson_interval(
    successes: int,
    observations: int,
    z: float = 1.96,
) -> tuple[float, float]:
    if observations <= 0:
        return (0.0, 1.0)
    proportion = successes / observations
    denominator = 1 + z**2 / observations
    center = (proportion + z**2 / (2 * observations)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / observations
            + z**2 / (4 * observations**2)
        )
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def build_skill_profiles(
    predictions: pd.DataFrame,
    *,
    probability_column: str,
    minimum_evidence: int,
) -> pd.DataFrame:
    """Aggregate held-out prediction evidence by student and every mapped skill."""

    required = {
        "student_id",
        "skill_ids",
        "source_row_id",
        "target",
        probability_column,
    }
    missing = sorted(required.difference(predictions.columns))
    if missing:
        raise ValueError("missing profile columns: " + ", ".join(missing))
    if minimum_evidence < 1:
        raise ValueError("minimum_evidence must be positive")

    probability = pd.to_numeric(predictions[probability_column], errors="raise")
    if probability.isna().any() or not probability.between(0, 1).all():
        raise ValueError("profile probabilities must be finite values between zero and one")
    target = pd.to_numeric(predictions["target"], errors="raise")
    if target.isna().any() or not target.isin([0, 1]).all():
        raise ValueError("profile target must be binary")

    evidence_rows: list[dict[str, object]] = []
    for row in predictions.itertuples(index=False):
        for skill_id in normalize_skill_ids(getattr(row, "skill_ids")):
            evidence_rows.append(
                {
                    "student_id": str(getattr(row, "student_id")),
                    "skill_id": skill_id,
                    "source_row_id": str(getattr(row, "source_row_id")),
                    "target": int(getattr(row, "target")),
                    "probability": float(getattr(row, probability_column)),
                }
            )

    rows: list[dict[str, object]] = []
    evidence = pd.DataFrame(evidence_rows)
    for (student_id, skill_id), group in evidence.groupby(
        ["student_id", "skill_id"], sort=True, dropna=False
    ):
        evidence_count = int(group["source_row_id"].nunique())
        successes = int(group["target"].sum())
        lower, upper = _wilson_interval(successes, evidence_count)
        rows.append(
            {
                "student_id": str(student_id),
                "skill_id": str(skill_id),
                "evidence_count": evidence_count,
                "mean_predicted_correct_probability": float(group["probability"].mean()),
                "predicted_probability_dispersion": float(
                    group["probability"].std(ddof=0)
                ),
                "observed_accuracy": successes / evidence_count,
                "observed_accuracy_lower": lower,
                "observed_accuracy_upper": upper,
                "evidence_status": (
                    "reported"
                    if evidence_count >= minimum_evidence
                    else "insufficient_evidence"
                ),
                "probability_source": probability_column,
                "interpretation_limit": (
                    "Continuous profile derived from held-out interaction evidence; "
                    "mean predicted correct probability is not a measure of mastery, "
                    "competence, learning, or causal effect."
                ),
            }
        )
    return pd.DataFrame(rows)
