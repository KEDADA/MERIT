"""Stable pilot split and TRAIN-only priority sampling primitives."""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass
from typing import Mapping, Sequence


def _stable_key(selector_seed: int, *parts: str) -> str:
    payload = "\0".join((str(selector_seed), *parts)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class StreamSplit:
    train_ids: tuple[str, ...]
    audit_ids: tuple[str, ...]
    audit_inclusion_probability: float


def stable_train_audit_split(
    query_ids_by_stream: Mapping[str, Sequence[str]],
    audit_fraction: float = 0.30,
    selector_seed: int = 20260719,
) -> dict[str, StreamSplit]:
    """Make one reproducible per-stream probability split before outcomes are read."""

    if not 0.0 < audit_fraction < 1.0:
        raise ValueError("audit_fraction must lie strictly between zero and one")
    result: dict[str, StreamSplit] = {}
    for stream_id in sorted(query_ids_by_stream):
        query_ids = list(query_ids_by_stream[stream_id])
        if len(query_ids) < 2 or len(set(query_ids)) != len(query_ids):
            raise ValueError("each stream requires at least two unique query IDs")
        audit_count = min(
            len(query_ids) - 1,
            max(1, math.floor(audit_fraction * len(query_ids) + 0.5)),
        )
        ordered = sorted(
            query_ids,
            key=lambda query_id: (
                _stable_key(selector_seed, stream_id, query_id),
                query_id,
            ),
        )
        audit = tuple(sorted(ordered[:audit_count]))
        train = tuple(sorted(ordered[audit_count:]))
        result[stream_id] = StreamSplit(
            train_ids=train,
            audit_ids=audit,
            audit_inclusion_probability=audit_count / len(query_ids),
        )
    return result


def percentile_midranks(values: Mapping[str, float]) -> dict[str, float]:
    if not values or any(not math.isfinite(value) for value in values.values()):
        raise ValueError("priority values must be non-empty and finite")
    ordered = sorted(values.items(), key=lambda item: (item[1], item[0]))
    result: dict[str, float] = {}
    cursor = 0
    count = len(ordered)
    while cursor < count:
        end = cursor + 1
        while end < count and ordered[end][1] == ordered[cursor][1]:
            end += 1
        midrank = ((cursor + 1) + end) / 2.0
        percentile = midrank / count
        for key, _ in ordered[cursor:end]:
            result[key] = percentile
        cursor = end
    return result


def utility_usage_scores(
    utility: Mapping[str, float], retrieval_count: Mapping[str, int]
) -> dict[str, float]:
    if set(utility) != set(retrieval_count) or any(value < 0 for value in retrieval_count.values()):
        raise ValueError("utility and non-negative usage counts must share IDs")
    utility_rank = percentile_midranks(utility)
    usage_rank = percentile_midranks(
        {key: math.log1p(value) for key, value in retrieval_count.items()}
    )
    return {key: 0.5 * utility_rank[key] + 0.5 * usage_rank[key] for key in utility}


def weighted_sample_without_replacement(
    scores: Mapping[str, float], sample_size: int, seed: int
) -> tuple[str, ...]:
    """PPS sample with the locked 1/N exploration floor and stable ordering."""

    if not scores or not 0 < sample_size <= len(scores):
        raise ValueError("invalid priority sample size")
    if any(not math.isfinite(value) or value < 0.0 for value in scores.values()):
        raise ValueError("priority scores must be finite and non-negative")
    generator = random.Random(seed)
    remaining = dict(scores)
    chosen: list[str] = []
    floor = 1.0 / len(scores)
    for _ in range(sample_size):
        ordered = sorted(remaining)
        weights = [remaining[key] + floor for key in ordered]
        threshold = generator.random() * sum(weights)
        cumulative = 0.0
        selected = ordered[-1]
        for key, weight in zip(ordered, weights):
            cumulative += weight
            if threshold < cumulative:
                selected = key
                break
        chosen.append(selected)
        del remaining[selected]
    return tuple(chosen)
