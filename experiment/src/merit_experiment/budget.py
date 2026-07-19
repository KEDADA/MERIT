"""Atomic paired-bundle admission under rollout and token hard ceilings."""

from __future__ import annotations

import math
from dataclasses import dataclass


class BudgetCeilingBlocked(RuntimeError):
    """Raised before a bundle starts when its full reservation cannot fit."""


@dataclass(frozen=True)
class Cost:
    rollout_equivalents: float
    tokens: int

    def __post_init__(self) -> None:
        if (
            not math.isfinite(self.rollout_equivalents)
            or self.rollout_equivalents < 0.0
            or not isinstance(self.tokens, int)
            or self.tokens < 0
        ):
            raise ValueError("cost must be finite and non-negative")


class BudgetLedger:
    def __init__(self, ceiling: Cost) -> None:
        self.ceiling = ceiling
        self.realized = Cost(0.0, 0)
        self._reservation: Cost | None = None

    def reserve_bundle(self, worst_case: Cost) -> None:
        if self._reservation is not None:
            raise RuntimeError("only one atomic bundle reservation may be active")
        if (
            self.realized.rollout_equivalents + worst_case.rollout_equivalents
            > self.ceiling.rollout_equivalents
            or self.realized.tokens + worst_case.tokens > self.ceiling.tokens
        ):
            raise BudgetCeilingBlocked("BLOCKED_BUDGET_CEILING")
        self._reservation = worst_case

    def settle_bundle(self, realized: Cost) -> None:
        if self._reservation is None:
            raise RuntimeError("bundle was not admitted")
        if (
            realized.rollout_equivalents > self._reservation.rollout_equivalents
            or realized.tokens > self._reservation.tokens
        ):
            raise ValueError("realized bundle cost exceeds its reservation")
        self.realized = Cost(
            self.realized.rollout_equivalents + realized.rollout_equivalents,
            self.realized.tokens + realized.tokens,
        )
        self._reservation = None

    def cancel_bundle(self) -> None:
        if self._reservation is None:
            raise RuntimeError("bundle was not admitted")
        self._reservation = None
