#!/usr/bin/env python3
"""CPU-only deterministic smoke check; this does not execute R001 or R002."""

from __future__ import annotations

import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.metrics import (
    ContributionEstimate,
    ordinary_least_squares_slope,
    paired_cti,
    spearman_ccc,
    superstition_rate_at_k,
)
from merit_experiment.neutral_pad import length_matched_marker_token_ids
from merit_experiment.replay import aligned_rollout_seeds, paired_contribution
from merit_experiment.sampling import stable_train_audit_split


def main() -> int:
    if spearman_ccc([1.0, 2.0, 3.0], [3.0, 2.0, 1.0]) != -1.0:
        raise RuntimeError("CCC direction sanity failed")
    if paired_cti({"q1": 1.0}, {"q1": 0.0}) != 1.0:
        raise RuntimeError("CTI direction sanity failed")
    if ordinary_least_squares_slope([100, 500], [0.1, 0.5]) <= 0.0:
        raise RuntimeError("SR slope direction sanity failed")
    sr = superstition_rate_at_k(
        [
            ContributionEstimate("m1", 2.0, -0.01, 0.01),
            ContributionEstimate("m2", 1.0, 0.10, 0.20),
        ]
    )
    if sr.rate != 1.0:
        raise RuntimeError("SR@k classification sanity failed")
    if len(stable_train_audit_split({"s": ["q1", "q2", "q3"]})["s"].audit_ids) != 1:
        raise RuntimeError("AUDIT split sanity failed")
    if length_matched_marker_token_ids((1, 2), 5) != (1, 2, 1, 2, 1):
        raise RuntimeError("neutral-pad length sanity failed")
    if aligned_rollout_seeds(7, 3) != (7, 8, 9):
        raise RuntimeError("paired seed sanity failed")
    if paired_contribution([1.0], [0.0]) != 1.0:
        raise RuntimeError("paired contribution sanity failed")
    print("SANITY_COMPONENT_VALIDATION: PASS")
    print("formal_runs_executed=0 gpu_calls=0 model_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
