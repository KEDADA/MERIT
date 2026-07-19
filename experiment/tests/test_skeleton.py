from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.hashing import canonical_json_sha256, file_sha256
from merit_experiment.snapshot import snapshot_config
from merit_experiment.validation import (
    ManifestValidationError,
    validate_artifact_manifest,
    validate_baseline_fidelity,
    validate_data_manifest,
    validate_pilot_implementation,
    validate_run_manifest,
    validate_runtime_designation,
)


def valid_data_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "manifest_id": "synthetic-isolation-test",
        "partitions": [
            {
                "partition_id": "synthetic-pilot-audit",
                "phase": "pilot",
                "role": "pilot_audit",
                "path_alias": "fixture://synthetic/pilot-audit",
                "sha256": "a" * 64,
                "sample_index_sha256": "b" * 64,
            },
            {
                "partition_id": "synthetic-sealed-audit",
                "phase": "confirmatory",
                "role": "sealed_final_audit",
                "selection_blind": True,
                "path_alias": "fixture://synthetic/sealed-audit",
                "sha256": "c" * 64,
                "sample_index_sha256": "d" * 64,
            },
        ],
        "disjointness_checks": [
            {
                "left_partition_id": "synthetic-pilot-audit",
                "right_partition_id": "synthetic-sealed-audit",
                "overlap_count": 0,
                "checked_by": "unit-test",
                "checked_at": "2026-07-19T00:00:00Z",
            }
        ],
    }


class SkeletonTests(unittest.TestCase):
    def test_example_manifests_are_valid_blocked_templates(self) -> None:
        run = json.loads((EXPERIMENT_ROOT / "runs/run_manifest.example.json").read_text())
        data = json.loads((EXPERIMENT_ROOT / "data/data_manifest.example.json").read_text())
        artifacts = json.loads(
            (EXPERIMENT_ROOT / "artifacts/artifact_manifest.example.json").read_text()
        )
        validate_run_manifest(run)
        validate_data_manifest(data)
        validate_artifact_manifest(artifacts)
        self.assertEqual(run["status"], "BLOCKED")

    def test_executable_run_rejects_unapproved_seed(self) -> None:
        run = json.loads((EXPERIMENT_ROOT / "runs/run_manifest.example.json").read_text())
        run["status"] = "READY"
        with self.assertRaises(ManifestValidationError):
            validate_run_manifest(run)

    def test_failure_status_consistency_is_enforced(self) -> None:
        run = json.loads((EXPERIMENT_ROOT / "runs/run_manifest.example.json").read_text())
        run["status"] = "FAILED"
        run["failure"] = {"type": "NONE", "message": "synthetic inconsistency"}
        with self.assertRaises(ManifestValidationError):
            validate_run_manifest(run)

    def test_data_roles_are_disjoint(self) -> None:
        validate_data_manifest(valid_data_manifest())

    def test_data_overlap_is_rejected(self) -> None:
        manifest = valid_data_manifest()
        manifest["disjointness_checks"][0]["overlap_count"] = 1
        with self.assertRaises(ManifestValidationError):
            validate_data_manifest(manifest)

    def test_incomplete_disjointness_proof_is_rejected(self) -> None:
        manifest = valid_data_manifest()
        manifest["disjointness_checks"] = []
        with self.assertRaises(ManifestValidationError):
            validate_data_manifest(manifest)

    def test_sealed_audit_requires_blindness_declaration(self) -> None:
        manifest = valid_data_manifest()
        del manifest["partitions"][1]["selection_blind"]
        with self.assertRaises(ManifestValidationError):
            validate_data_manifest(manifest)

    def test_private_absolute_artifact_path_is_rejected(self) -> None:
        manifest = {
            "schema_version": "1.0",
            "run_id": "R001__sanity__synthetic__seed-0__a000",
            "artifacts": [
                {
                    "artifact_id": "bad-path",
                    "kind": "log",
                    "path_alias": "/" + "private/machine/path.log",
                    "sha256": "e" * 64,
                    "size_bytes": 1,
                    "created_by": "unit-test",
                }
            ],
        }
        with self.assertRaises(ManifestValidationError):
            validate_artifact_manifest(manifest)

    def test_config_snapshot_is_canonical_and_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.json"
            destination = root / "snapshot.json"
            source.write_text('{"z": 1, "a": "值"}\n', encoding="utf-8")
            digest = snapshot_config(source, destination)
            expected = canonical_json_sha256({"a": "值", "z": 1})
            self.assertEqual(digest, expected)
            self.assertEqual(snapshot_config(source, destination), expected)

            changed = copy.deepcopy({"a": "值", "z": 2})
            source.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaises(FileExistsError):
                snapshot_config(source, destination)

    def test_synthetic_fixture_has_content_hash(self) -> None:
        digest = file_sha256(EXPERIMENT_ROOT / "tests/fixtures/synthetic_events.jsonl")
        self.assertRegex(digest, r"^[a-f0-9]{64}$")

    def test_runtime_candidate_matches_r000_and_stays_blocked(self) -> None:
        baseline = json.loads(
            (EXPERIMENT_ROOT / "environments/baseline.json").read_text()
        )
        runtime = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-designation.pending.json").read_text()
        )
        validate_runtime_designation(runtime, baseline)
        self.assertEqual(runtime["status"], "BLOCKED")
        self.assertTrue(
            all(check["status"] == "NOT_RUN" for check in runtime["required_preflight"])
        )

    def test_runtime_candidate_rejects_invented_designation(self) -> None:
        baseline = json.loads(
            (EXPERIMENT_ROOT / "environments/baseline.json").read_text()
        )
        runtime = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-designation.pending.json").read_text()
        )
        runtime["designation"]["project_runtime_alias"] = "runtime://invented"
        with self.assertRaises(ManifestValidationError):
            validate_runtime_designation(runtime, baseline)

    def test_baseline_fidelity_preserves_reporting_distinction(self) -> None:
        fidelity = json.loads(
            (EXPERIMENT_ROOT / "configs/baseline-fidelity.pending.json").read_text()
        )
        validate_baseline_fidelity(fidelity)
        fidelity["reporting_policy"]["exact_method_name_requires"] = "style-label-only"
        with self.assertRaises(ManifestValidationError):
            validate_baseline_fidelity(fidelity)

    def test_baseline_fidelity_rejects_unverified_source_claim(self) -> None:
        fidelity = json.loads(
            (EXPERIMENT_ROOT / "configs/baseline-fidelity.pending.json").read_text()
        )
        fidelity["baselines"][0]["implementation_mode"] = "source_faithful"
        with self.assertRaises(ManifestValidationError):
            validate_baseline_fidelity(fidelity)

    def test_pilot_implementation_has_exact_six_open_rules(self) -> None:
        implementation = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.pending.json").read_text()
        )
        validate_pilot_implementation(implementation)
        self.assertEqual(len(implementation["rules"]), 6)

    def test_pilot_implementation_rejects_missing_rule(self) -> None:
        implementation = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.pending.json").read_text()
        )
        implementation["rules"].pop()
        with self.assertRaises(ManifestValidationError):
            validate_pilot_implementation(implementation)

    def test_pilot_implementation_rejects_no_pad_placeholder(self) -> None:
        implementation = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.pending.json").read_text()
        )
        forbidden = "_".join(("PILOT", "NOPAD", "REMOVAL", "DELTA"))
        implementation["rules"][0]["blocks"].append(forbidden)
        with self.assertRaises(ManifestValidationError):
            validate_pilot_implementation(implementation)


if __name__ == "__main__":
    unittest.main()
