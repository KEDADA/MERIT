#!/usr/bin/env python3
"""Read-only validation of blocked R001/R002 atomic manifests and provenance."""

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.hashing import file_sha256
from merit_experiment.provenance import dirty_entries
from merit_experiment.validation import (
    validate_artifact_manifest,
    validate_atomic_input_manifest,
    validate_atomic_sanity_run_manifest,
    validate_dirty_worktree_inventory,
)


RUN_IDS = (
    "R001__sanity__paired-replay-real-toy__seed-pending__a001",
    "R002__sanity__metrics-real-toy__seed-pending__a001",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    inventory_path = EXPERIMENT_ROOT / "runs/provenance/dirty-worktree.20260719.json"
    inventory = _load(inventory_path)
    validate_dirty_worktree_inventory(inventory)
    if dirty_entries(REPO_ROOT) != inventory["entries"]:
        raise RuntimeError("current dirty worktree differs from the captured input inventory")
    inventory_sha256 = file_sha256(inventory_path)

    references_checked = 0
    for run_id in RUN_IDS:
        run_root = EXPERIMENT_ROOT / "runs" / run_id
        run = _load(run_root / "run-manifest.json")
        inputs = _load(run_root / "input-manifest.json")
        artifacts = _load(run_root / "artifact-manifest.json")
        validate_atomic_sanity_run_manifest(run)
        validate_atomic_input_manifest(inputs)
        validate_artifact_manifest(artifacts)
        if run["git"]["dirty_paths_manifest_sha256"] != inventory_sha256:
            raise RuntimeError(f"{run_id} dirty inventory hash mismatch")
        for reference in inputs["references"]:
            referenced_path = EXPERIMENT_ROOT / reference["path"]
            if file_sha256(referenced_path) != reference["sha256"]:
                raise RuntimeError(f"{run_id} input hash mismatch: {reference['path']}")
            references_checked += 1
        for field, filename in (
            ("input_manifest", "input-manifest.json"),
            ("artifact_manifest", "artifact-manifest.json"),
        ):
            if file_sha256(run_root / filename) != run[field]["sha256"]:
                raise RuntimeError(f"{run_id} {field} hash mismatch")

    print("ATOMIC_RUN_INPUT_VALIDATION: PASS")
    print(f"atomic_manifests=2 references_checked={references_checked} dirty_entries={inventory['entry_count']}")
    print("statuses=BLOCKED execution_authorized=false model_calls=0 formal_runs=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
