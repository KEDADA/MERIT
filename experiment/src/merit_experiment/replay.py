"""Paired replay identity, seed alignment, and contribution primitives."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ReplayIdentity:
    query_id: str
    task_state_sha256: str
    bank_snapshot_sha256: str
    retrieval_order: tuple[str, ...]
    model_revision: str
    tokenizer_revision: str
    decoding_config_sha256: str
    reward_evaluator_revision: str
    rollout_seed: int


def aligned_rollout_seeds(base_seed: int, count: int) -> tuple[int, ...]:
    if not isinstance(base_seed, int) or not isinstance(count, int) or count <= 0:
        raise ValueError("base_seed must be an integer and count must be positive")
    return tuple(base_seed + index for index in range(count))


def deployment_rollout_is_reusable(
    expected_control: ReplayIdentity, observed_deployment: ReplayIdentity
) -> bool:
    """Permit the single locked reuse only under exact provenance equality."""

    return expected_control == observed_deployment


def paired_contribution(
    control_rewards: Sequence[float], loo_rewards: Sequence[float]
) -> float:
    """Mean paired removal contribution E[control - LOO]."""

    if len(control_rewards) != len(loo_rewards) or not control_rewards:
        raise ValueError("paired contribution requires equal non-empty reward vectors")
    differences: list[float] = []
    for control, loo in zip(control_rewards, loo_rewards):
        if not math.isfinite(control) or not math.isfinite(loo):
            raise ValueError("paired rewards must be finite")
        differences.append(control - loo)
    return sum(differences) / len(differences)
