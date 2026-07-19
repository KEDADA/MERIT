"""Deterministic, dependency-free sanity metrics for R002 engineering checks."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class ContributionEstimate:
    memory_id: str
    assigned_utility: float
    ci_low: float
    ci_high: float


@dataclass(frozen=True)
class SuperstitionRate:
    selected_ids: tuple[str, ...]
    rate: float
    superstitious_count: int
    undetermined_count: int


def _finite(values: Sequence[float], context: str) -> None:
    if not values or any(not math.isfinite(value) for value in values):
        raise ValueError(f"{context} requires non-empty finite values")


def midranks(values: Sequence[float]) -> list[float]:
    """Return one-based average ranks, preserving input order and handling ties."""

    _finite(values, "midranks")
    ordered = sorted(enumerate(values), key=lambda item: (item[1], item[0]))
    result = [0.0] * len(values)
    cursor = 0
    while cursor < len(ordered):
        end = cursor + 1
        while end < len(ordered) and ordered[end][1] == ordered[cursor][1]:
            end += 1
        rank = ((cursor + 1) + end) / 2.0
        for original_index, _ in ordered[cursor:end]:
            result[original_index] = rank
        cursor = end
    return result


def spearman_ccc(left: Sequence[float], right: Sequence[float]) -> float:
    """Spearman correlation used by the protocol's CCC sanity path."""

    if len(left) != len(right) or len(left) < 2:
        raise ValueError("CCC requires paired vectors with at least two values")
    left_ranks = midranks(left)
    right_ranks = midranks(right)
    left_mean = sum(left_ranks) / len(left_ranks)
    right_mean = sum(right_ranks) / len(right_ranks)
    numerator = sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left_ranks, right_ranks)
    )
    left_ss = sum((value - left_mean) ** 2 for value in left_ranks)
    right_ss = sum((value - right_mean) ** 2 for value in right_ranks)
    denominator = math.sqrt(left_ss * right_ss)
    if denominator == 0.0:
        raise ValueError("CCC is undefined for a constant rank vector")
    return numerator / denominator


def classify_contribution(ci_low: float, ci_high: float, delta_sr: float = 0.05) -> str:
    if not all(math.isfinite(value) for value in (ci_low, ci_high, delta_sr)):
        raise ValueError("contribution classification requires finite values")
    if ci_low > ci_high or delta_sr <= 0.0:
        raise ValueError("invalid contribution interval or delta_sr")
    if ci_high < -delta_sr:
        return "harmful"
    if ci_low >= -delta_sr and ci_high <= delta_sr:
        return "practically_null"
    if ci_low > delta_sr:
        return "positive"
    return "undetermined"


def superstition_rate_at_k(
    estimates: Sequence[ContributionEstimate],
    top_fraction: float = 0.20,
    delta_sr: float = 0.05,
) -> SuperstitionRate:
    """Compute conservative CI-decided SR@k with stable memory-ID tie breaking."""

    if not estimates or not (0.0 < top_fraction <= 1.0):
        raise ValueError("SR@k requires estimates and 0 < top_fraction <= 1")
    if len({estimate.memory_id for estimate in estimates}) != len(estimates):
        raise ValueError("memory_id values must be unique")
    if any(not math.isfinite(estimate.assigned_utility) for estimate in estimates):
        raise ValueError("assigned utility must be finite")

    top_count = max(1, math.ceil(len(estimates) * top_fraction))
    selected = sorted(
        estimates, key=lambda estimate: (-estimate.assigned_utility, estimate.memory_id)
    )[:top_count]
    classes = [
        classify_contribution(estimate.ci_low, estimate.ci_high, delta_sr)
        for estimate in selected
    ]
    superstitious_count = sum(
        value in {"harmful", "practically_null"} for value in classes
    )
    undetermined_count = sum(value == "undetermined" for value in classes)
    return SuperstitionRate(
        selected_ids=tuple(estimate.memory_id for estimate in selected),
        rate=superstitious_count / top_count,
        superstitious_count=superstitious_count,
        undetermined_count=undetermined_count,
    )


def paired_cti(
    b_only: Mapping[str, float], mixed_a_b: Mapping[str, float]
) -> float:
    """CTI = paired mean accuracy(B-only) - paired mean accuracy(A+B)."""

    if set(b_only) != set(mixed_a_b) or not b_only:
        raise ValueError("CTI requires the same non-empty task IDs in both conditions")
    differences: list[float] = []
    for task_id in sorted(b_only):
        left = b_only[task_id]
        right = mixed_a_b[task_id]
        if not math.isfinite(left) or not math.isfinite(right):
            raise ValueError("CTI outcomes must be finite")
        differences.append(left - right)
    return sum(differences) / len(differences)


def ordinary_least_squares_slope(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("slope requires paired vectors with at least two values")
    _finite(x, "slope x")
    _finite(y, "slope y")
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    denominator = sum((value - x_mean) ** 2 for value in x)
    if denominator == 0.0:
        raise ValueError("slope is undefined for constant x")
    return sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x, y)
    ) / denominator


def holm_adjusted_pvalues(pvalues: Mapping[str, float]) -> dict[str, float]:
    """Return monotone Holm step-down adjusted p-values."""

    if not pvalues:
        raise ValueError("Holm adjustment requires at least one p-value")
    if any(not math.isfinite(value) or not 0.0 <= value <= 1.0 for value in pvalues.values()):
        raise ValueError("p-values must be finite and within [0,1]")
    ordered = sorted(pvalues.items(), key=lambda item: (item[1], item[0]))
    count = len(ordered)
    running = 0.0
    adjusted: dict[str, float] = {}
    for index, (name, value) in enumerate(ordered):
        running = max(running, (count - index) * value)
        adjusted[name] = min(1.0, running)
    return adjusted
