"""Deterministic task-clustered BCa bootstrap for paired sanity analyses."""

from __future__ import annotations

import math
import random
from statistics import NormalDist
from typing import Callable, Sequence, TypeVar

Cluster = TypeVar("Cluster")


def _quantile(values: Sequence[float], probability: float) -> float:
    if not values or not 0.0 <= probability <= 1.0:
        raise ValueError("invalid quantile request")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def clustered_bca_interval(
    clusters: Sequence[Cluster],
    statistic: Callable[[Sequence[Cluster]], float],
    confidence_level: float,
    replicates: int,
    seed: int,
) -> tuple[float, float]:
    """Resample whole task clusters and return a two-sided BCa interval."""

    if len(clusters) < 2:
        raise ValueError("BCa requires at least two task clusters")
    if not 0.0 < confidence_level < 1.0 or replicates < 100:
        raise ValueError("invalid confidence level or too few bootstrap replicates")
    observed = statistic(clusters)
    if not math.isfinite(observed):
        raise ValueError("observed statistic is non-finite")

    generator = random.Random(seed)
    bootstrap: list[float] = []
    for _ in range(replicates):
        sample = [clusters[generator.randrange(len(clusters))] for _ in clusters]
        value = statistic(sample)
        if not math.isfinite(value):
            raise ValueError("bootstrap statistic is non-finite")
        bootstrap.append(value)

    less = sum(value < observed for value in bootstrap)
    equal = sum(value == observed for value in bootstrap)
    proportion = (less + 0.5 * equal) / replicates
    clamp = 0.5 / replicates
    proportion = min(1.0 - clamp, max(clamp, proportion))
    normal = NormalDist()
    bias = normal.inv_cdf(proportion)

    jackknife = [
        statistic([cluster for index, cluster in enumerate(clusters) if index != omitted])
        for omitted in range(len(clusters))
    ]
    if any(not math.isfinite(value) for value in jackknife):
        raise ValueError("jackknife statistic is non-finite")
    jackknife_mean = sum(jackknife) / len(jackknife)
    differences = [jackknife_mean - value for value in jackknife]
    squared_sum = sum(value**2 for value in differences)
    acceleration = 0.0
    if squared_sum > 0.0:
        acceleration = sum(value**3 for value in differences) / (
            6.0 * squared_sum**1.5
        )

    alpha = (1.0 - confidence_level) / 2.0

    def adjusted_probability(probability: float) -> float:
        z_alpha = normal.inv_cdf(probability)
        denominator = 1.0 - acceleration * (bias + z_alpha)
        if denominator == 0.0:
            raise ValueError("BCa acceleration produced a singular adjustment")
        return normal.cdf(bias + (bias + z_alpha) / denominator)

    lower_probability = adjusted_probability(alpha)
    upper_probability = adjusted_probability(1.0 - alpha)
    return (
        _quantile(bootstrap, lower_probability),
        _quantile(bootstrap, upper_probability),
    )
