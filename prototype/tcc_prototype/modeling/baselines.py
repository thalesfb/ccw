"""Transparent probability baselines for next-response prediction."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class SmoothedProbabilityBaseline:
    """Estimate probabilities from global or grouped historical frequencies.

    Group estimates are shrunk toward the global training prevalence using a
    configurable prior strength. Unseen groups always fall back to that global
    prevalence.
    """

    group_columns: tuple[str, ...]
    prior_strength: float = 5.0
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
                float(row["sum"])
                + self.prior_strength * self._global_probability
            ) / (float(row["count"]) + self.prior_strength)
            self._group_probabilities[key] = probability
        return self

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
            values.append(
                self._group_probabilities.get(key, self._global_probability)
            )
        return np.asarray(values, dtype=float)
