"""Transparent probability baselines for next-response prediction."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .features import normalize_skill_ids


@dataclass
class SmoothedProbabilityBaseline:
    """Estimate global or grouped probabilities using training-only shrinkage."""

    group_columns: tuple[str, ...]
    prior_strength: float
    target_column: str = "target"
    _global_probability: float | None = field(default=None, init=False)
    _group_probabilities: dict[tuple[object, ...], float] = field(
        default_factory=dict, init=False
    )

    def fit(self, train: pd.DataFrame) -> "SmoothedProbabilityBaseline":
        if self.target_column not in train.columns:
            raise ValueError(f"missing target column: {self.target_column}")
        if train.empty:
            raise ValueError("cannot fit a baseline on an empty training set")
        if self.prior_strength < 0:
            raise ValueError("prior_strength must be non-negative")
        missing = sorted(set(self.group_columns).difference(train.columns))
        if missing:
            raise ValueError("missing group columns: " + ", ".join(missing))

        target = train[self.target_column].astype(float)
        self._global_probability = float(target.mean())
        self._group_probabilities = {}
        if not self.group_columns:
            return self
        grouped = (
            train.groupby(list(self.group_columns), dropna=False)[self.target_column]
            .agg(["sum", "count"])
            .reset_index()
        )
        for _, row in grouped.iterrows():
            key = tuple(row[column] for column in self.group_columns)
            probability = (
                float(row["sum"]) + self.prior_strength * self._global_probability
            ) / (float(row["count"]) + self.prior_strength)
            self._group_probabilities[key] = probability
        return self

    @property
    def global_probability(self) -> float:
        if self._global_probability is None:
            raise RuntimeError("baseline must be fit before reading global probability")
        return self._global_probability

    def predict_proba(self, frame: pd.DataFrame) -> np.ndarray:
        if self._global_probability is None:
            raise RuntimeError("baseline must be fit before prediction")
        missing = sorted(set(self.group_columns).difference(frame.columns))
        if missing:
            raise ValueError("missing group columns: " + ", ".join(missing))
        if not self.group_columns:
            return np.full(len(frame), self._global_probability, dtype=float)
        values = []
        for _, row in frame.iterrows():
            key = tuple(row[column] for column in self.group_columns)
            values.append(self._group_probabilities.get(key, self._global_probability))
        return np.asarray(values, dtype=float)


@dataclass
class MultiSkillSmoothedProbabilityBaseline:
    """Estimate overlapping per-skill frequencies without exploding training rows."""

    prior_strength: float
    target_column: str = "target"
    skill_column: str = "skill_ids"
    _global_probability: float | None = field(default=None, init=False)
    _skill_probabilities: dict[str, float] = field(default_factory=dict, init=False)

    def fit(self, train: pd.DataFrame) -> "MultiSkillSmoothedProbabilityBaseline":
        required = {self.target_column, self.skill_column}
        missing = sorted(required.difference(train.columns))
        if missing:
            raise ValueError("missing skill baseline columns: " + ", ".join(missing))
        if train.empty:
            raise ValueError("cannot fit a baseline on an empty training set")
        if self.prior_strength < 0:
            raise ValueError("prior_strength must be non-negative")

        self._global_probability = float(train[self.target_column].astype(float).mean())
        sums: dict[str, float] = defaultdict(float)
        counts: dict[str, int] = defaultdict(int)
        for _, row in train.iterrows():
            target = float(row[self.target_column])
            for skill in normalize_skill_ids(row[self.skill_column]):
                sums[skill] += target
                counts[skill] += 1
        self._skill_probabilities = {
            skill: (sums[skill] + self.prior_strength * self._global_probability)
            / (counts[skill] + self.prior_strength)
            for skill in counts
        }
        return self

    def predict_proba(self, frame: pd.DataFrame) -> np.ndarray:
        if self._global_probability is None:
            raise RuntimeError("baseline must be fit before prediction")
        if self.skill_column not in frame.columns:
            raise ValueError(f"missing skill column: {self.skill_column}")
        predictions = []
        for skills_value in frame[self.skill_column]:
            skills = normalize_skill_ids(skills_value)
            probabilities = [
                self._skill_probabilities.get(skill, self._global_probability)
                for skill in skills
            ]
            predictions.append(float(np.mean(probabilities)))
        return np.asarray(predictions, dtype=float)


def student_history_probability(
    frame: pd.DataFrame, *, prior_strength: float, global_probability: float
) -> np.ndarray:
    """Shrink a student's pre-response history toward training prevalence."""

    if prior_strength <= 0:
        raise ValueError("student history prior_strength must be positive")
    required = {"prior_student_correct", "prior_student_attempts"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError("missing student history columns: " + ", ".join(missing))
    correct = frame["prior_student_correct"].to_numpy(dtype=float)
    attempts = frame["prior_student_attempts"].to_numpy(dtype=float)
    return (correct + prior_strength * global_probability) / (
        attempts + prior_strength
    )
