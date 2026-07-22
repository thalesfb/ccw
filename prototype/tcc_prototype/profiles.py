"""Build conservative student skill profiles from held-out predictions."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class OrdinalThresholds:
    """Explicit, versioned thresholds for optional profile labels."""

    version: str
    high_fragility_upper: float
    monitoring_upper: float
    developing_upper: float

    def __post_init__(self) -> None:
        values = (
            self.high_fragility_upper,
            self.monitoring_upper,
            self.developing_upper,
        )
        if not self.version.strip():
            raise ValueError("threshold version is required")
        if not 0 < values[0] < values[1] < values[2] < 1:
            raise ValueError(
                "ordinal thresholds must be strictly increasing between zero and one"
            )

    def classify(self, probability: float) -> str:
        if probability < self.high_fragility_upper:
            return "high_fragility"
        if probability < self.monitoring_upper:
            return "monitoring"
        if probability < self.developing_upper:
            return "developing"
        return "probable_mastery"


def _wilson_interval(successes: int, observations: int, z: float = 1.96) -> tuple[float, float]:
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
    thresholds: OrdinalThresholds | None = None,
) -> pd.DataFrame:
    """Aggregate held-out predictions by student and skill.

    Ordinal labels are produced only when explicit versioned thresholds are
    supplied and the group reaches the minimum evidence count.
    """

    required = {
        "student_id",
        "primary_skill_id",
        "target",
        probability_column,
    }
    missing = sorted(required.difference(predictions.columns))
    if missing:
        raise ValueError("missing profile columns: " + ", ".join(missing))
    if minimum_evidence < 1:
        raise ValueError("minimum_evidence must be positive")

    rows: list[dict[str, object]] = []
    for (student_id, skill_id), group in predictions.groupby(
        ["student_id", "primary_skill_id"], sort=True, dropna=False
    ):
        evidence_count = len(group)
        successes = int(group["target"].astype(int).sum())
        predicted_probability = float(group[probability_column].mean())
        lower, upper = _wilson_interval(successes, evidence_count)
        evidence_status = (
            "estimated"
            if evidence_count >= minimum_evidence
            else "insufficient_evidence"
        )
        level = None
        if evidence_status == "estimated" and thresholds is not None:
            level = thresholds.classify(predicted_probability)

        rows.append(
            {
                "student_id": str(student_id),
                "skill_id": str(skill_id),
                "evidence_count": evidence_count,
                "predicted_probability": predicted_probability,
                "prediction_std": float(group[probability_column].std(ddof=0)),
                "observed_accuracy": successes / evidence_count,
                "observed_accuracy_lower": lower,
                "observed_accuracy_upper": upper,
                "evidence_status": evidence_status,
                "level": level,
                "threshold_version": thresholds.version if thresholds else None,
                "interpretation_limit": (
                    "Profile derived from available interactions and model estimates; "
                    "it is not a definitive diagnosis of competence or learning."
                ),
            }
        )
    return pd.DataFrame(rows)
