from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_formal_gate.py")
SPEC = importlib.util.spec_from_file_location("formal_gate_validator", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class FormalGateTests(unittest.TestCase):
    def test_synthetic_model_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload = b"locked-model-byte-fixture"
            (root / "fixture.bin").write_bytes(payload)
            digest = gate.sha256_file(root / "fixture.bin")
            lock = {
                "status": "MODEL_ASSET_LOCKED",
                "model_alias": gate.MODEL_ALIAS,
                "repository": "Qwen/Qwen3-32B",
                "revision": gate.REVISION,
                "file_count": 1,
                "total_size_bytes": len(payload),
                "files": [
                    {
                        "path": "fixture.bin",
                        "size_bytes": len(payload),
                        "sha256": digest,
                        "official_lfs_sha256": digest,
                    }
                ],
            }
            self.assertEqual(gate.validate_model_snapshot(lock, root), 1)

    def test_ready_is_rejected_while_bindings_are_missing(self) -> None:
        decoding = {
            "do_sample": False,
            "max_new_tokens": 256,
            "temperature": None,
            "top_p": None,
        }
        document = {
            "run_family_id": "R001",
            "status": "BLOCKED",
            "execution_authorized": False,
            "blocking_reasons": list(gate.R001_BLOCKERS),
            "resolved_bindings": {
                "model_alias": gate.MODEL_ALIAS,
                "model_revision": gate.REVISION,
                "tokenizer_revision": gate.REVISION,
                "decoding": decoding,
                "decoding_sha256": gate.canonical_sha256(decoding),
                "run_seed": 20260719,
            },
            "execution_boundary": {"formal_runs": 0, "model_calls": 0},
        }
        gate.validate_gate_document(document, "R001")
        document["status"] = "READY"
        document["execution_authorized"] = True
        with self.assertRaises(gate.GateValidationError):
            gate.validate_gate_document(document, "R001")

    def test_partial_download_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "fixture.bin.part").write_bytes(b"partial")
            lock = {
                "status": "MODEL_ASSET_LOCKED",
                "model_alias": gate.MODEL_ALIAS,
                "repository": "Qwen/Qwen3-32B",
                "revision": gate.REVISION,
                "file_count": 0,
                "total_size_bytes": 0,
                "files": [],
            }
            with self.assertRaises(gate.GateValidationError):
                gate.validate_model_snapshot(lock, root)


if __name__ == "__main__":
    unittest.main()
