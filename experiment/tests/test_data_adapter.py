from __future__ import annotations

import json
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.data_adapter import (
    AlfworldZipAdapter,
    DataAdapterError,
    HotpotQATraceJsonlAdapter,
    build_real_toy_split,
)
from merit_experiment.validation import ManifestValidationError, validate_data_manifest


class DataAdapterTests(unittest.TestCase):
    def test_real_format_adapters_and_split_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            trajectory_zip = root / "trajectory.zip"
            game_zip = root / "game.zip"
            with ZipFile(trajectory_zip, "w") as trajectories, ZipFile(game_zip, "w") as games:
                for index in range(10):
                    base = f"json_2.1.1/valid_seen/type-{index}/trial-{index}"
                    trajectories.writestr(
                        f"{base}/traj_data.json",
                        json.dumps({"task_id": f"trial-{index}", "task_type": "fixture"}),
                    )
                    games.writestr(f"{base}/game.tw-pddl", f"game-{index}")
            trace_path = root / "hotpot.jsonl"
            trace_path.write_text(
                "".join(
                    json.dumps({f"question-{index}": [{"action": "finish", "observation": "ok"}]})
                    + "\n"
                    for index in range(10)
                ),
                encoding="utf-8",
            )
            alfworld = AlfworldZipAdapter(trajectory_zip, game_zip)
            hotpot = HotpotQATraceJsonlAdapter(trace_path)
            first = build_real_toy_split(
                {"alfworld": alfworld.index(), "hotpotqa": hotpot.index()}
            )
            second = build_real_toy_split(
                {"alfworld": alfworld.index(), "hotpotqa": hotpot.index()}
            )
            self.assertEqual(first, second)
            self.assertEqual(len(first["pilot_train"]), 14)
            self.assertEqual(len(first["pilot_audit"]), 6)
            self.assertFalse(
                {ref.query_id for ref in first["pilot_train"]}.intersection(
                    ref.query_id for ref in first["pilot_audit"]
                )
            )
            for references in first.values():
                for reference in references:
                    (alfworld if reference.stream_id == "alfworld" else hotpot).load(reference)

    def test_missing_replay_pair_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with ZipFile(root / "trajectory.zip", "w") as trajectories:
                trajectories.writestr(
                    "json_2.1.1/valid_seen/type/trial/traj_data.json",
                    json.dumps({"task_id": "trial", "task_type": "fixture"}),
                )
            with ZipFile(root / "game.zip", "w"):
                pass
            with self.assertRaises(DataAdapterError):
                AlfworldZipAdapter(root / "trajectory.zip", root / "game.zip").index()

    def test_real_toy_manifest_cannot_open_run_gate(self) -> None:
        manifest = json.loads(
            (EXPERIMENT_ROOT / "data/real-toy-split.20260719.manifest.json").read_text()
        )
        validate_data_manifest(manifest)
        modified = copy.deepcopy(manifest)
        modified["readiness"]["formal_r001_r002"] = "READY"
        with self.assertRaises(ManifestValidationError):
            validate_data_manifest(modified)


if __name__ == "__main__":
    unittest.main()
