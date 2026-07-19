"""Internal standardized credit wrappers; these are not exact upstream methods."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class ReasoningBankStyleCredit:
    """Co-occurrence accumulator used only by the standardized R001 wrapper."""

    utility: dict[str, float] = field(default_factory=dict)

    def update(self, retrieved_memory_ids: Sequence[str], success: float) -> None:
        if not math.isfinite(success):
            raise ValueError("success must be finite")
        for memory_id in retrieved_memory_ids:
            self.utility[memory_id] = self.utility.get(memory_id, 0.0) + success


@dataclass
class MemRLStyleMonteCarloCredit:
    """Sample-mean return credit used only by the standardized wrapper."""

    value: dict[str, float] = field(default_factory=dict)
    count: dict[str, int] = field(default_factory=dict)

    def update(self, retrieved_memory_ids: Sequence[str], episode_return: float) -> None:
        if not math.isfinite(episode_return):
            raise ValueError("episode_return must be finite")
        for memory_id in retrieved_memory_ids:
            old_count = self.count.get(memory_id, 0)
            new_count = old_count + 1
            old_value = self.value.get(memory_id, 0.0)
            self.value[memory_id] = old_value + (episode_return - old_value) / new_count
            self.count[memory_id] = new_count
