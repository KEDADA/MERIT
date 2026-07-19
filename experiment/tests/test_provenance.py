from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.validation import (
    ManifestValidationError,
    validate_atomic_sanity_run_manifest,
    validate_dirty_worktree_inventory,
)


class ProvenanceTests(unittest.TestCase):
    def test_dirty_inventory_has_only_relative_content_addressed_paths(self) -> None:
        inventory = json.loads(
            (EXPERIMENT_ROOT / "runs/provenance/dirty-worktree.20260719.json").read_text()
        )
        validate_dirty_worktree_inventory(inventory)

    def test_atomic_manifests_are_structurally_ready_but_not_executable(self) -> None:
        for run_id in (
            "R001__sanity__paired-replay-real-toy__seed-pending__a001",
            "R002__sanity__metrics-real-toy__seed-pending__a001",
        ):
            manifest = json.loads(
                (EXPERIMENT_ROOT / "runs" / run_id / "run-manifest.json").read_text()
            )
            validate_atomic_sanity_run_manifest(manifest)
            self.assertEqual(manifest["status"], "BLOCKED")
            self.assertFalse(manifest["execution_authorized"])
            modified = copy.deepcopy(manifest)
            modified["status"] = "READY"
            with self.assertRaises(ManifestValidationError):
                validate_atomic_sanity_run_manifest(modified)


if __name__ == "__main__":
    unittest.main()
