#!/usr/bin/env python3
"""Read-only validation for the R001/R002 formal execution-gate evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


REVISION = "9216db5781bf21249d130ec9da846c4624c16137"
MODEL_ALIAS = f"model://qwen/qwen3-32b-bf16@{REVISION}"
R001_BLOCKERS = (
    "R001_EXECUTABLE_TASK_DRIVER_NOT_BOUND",
    "R001_MEMORY_BANK_SNAPSHOT_NOT_BOUND",
    "R001_REWARD_EVALUATOR_NOT_BOUND",
)
R002_BLOCKERS = ("R002_SUCCESSFUL_R001_OUTPUT_NOT_AVAILABLE",)


class GateValidationError(ValueError):
    """Raised when formal-gate evidence is incomplete or unsafe."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GateValidationError(f"expected JSON object: {path.name}")
    return value


def validate_model_snapshot(lock: Mapping[str, Any], model_root: Path) -> int:
    if lock.get("status") != "MODEL_ASSET_LOCKED" or lock.get("model_alias") != MODEL_ALIAS:
        raise GateValidationError("model lock identity/status mismatch")
    if lock.get("repository") != "Qwen/Qwen3-32B" or lock.get("revision") != REVISION:
        raise GateValidationError("model repository revision mismatch")
    files = lock.get("files")
    if not isinstance(files, list) or len(files) != lock.get("file_count"):
        raise GateValidationError("model file inventory count mismatch")
    expected_names: set[str] = set()
    total = 0
    for item in files:
        if not isinstance(item, Mapping):
            raise GateValidationError("model file entry must be an object")
        name = item.get("path")
        relative = PurePosixPath(name) if isinstance(name, str) else PurePosixPath("..")
        if relative.is_absolute() or ".." in relative.parts or name in expected_names:
            raise GateValidationError("unsafe or duplicate model file path")
        expected_names.add(name)
        path = model_root / relative
        expected_size = item.get("size_bytes")
        if not path.is_file() or path.stat().st_size != expected_size:
            raise GateValidationError(f"model file size mismatch: {name}")
        observed = sha256_file(path)
        if observed != item.get("sha256"):
            raise GateValidationError(f"model file SHA-256 mismatch: {name}")
        official_lfs = item.get("official_lfs_sha256")
        if official_lfs is not None and official_lfs != observed:
            raise GateValidationError(f"official LFS SHA-256 mismatch: {name}")
        total += expected_size
    if total != lock.get("total_size_bytes"):
        raise GateValidationError("model total size mismatch")
    if any(model_root.glob("*.part")):
        raise GateValidationError("partial model downloads remain")
    return len(files)


def validate_gate_document(document: Mapping[str, Any], family: str) -> None:
    blockers = R001_BLOCKERS if family == "R001" else R002_BLOCKERS
    if document.get("run_family_id") != family:
        raise GateValidationError("gate run-family mismatch")
    if document.get("status") != "BLOCKED" or document.get("execution_authorized") is not False:
        raise GateValidationError("gate opens execution without all prerequisites")
    if tuple(document.get("blocking_reasons", ())) != blockers:
        raise GateValidationError("gate blockers differ from the audited facts")
    bindings = document.get("resolved_bindings")
    if not isinstance(bindings, Mapping):
        raise GateValidationError("resolved bindings missing")
    if bindings.get("model_alias") != MODEL_ALIAS:
        raise GateValidationError("gate model alias mismatch")
    if bindings.get("model_revision") != REVISION or bindings.get("tokenizer_revision") != REVISION:
        raise GateValidationError("gate model/tokenizer revision mismatch")
    decoding = bindings.get("decoding")
    if decoding != {
        "do_sample": False,
        "max_new_tokens": 256,
        "temperature": None,
        "top_p": None,
    }:
        raise GateValidationError("gate decoding configuration mismatch")
    if bindings.get("decoding_sha256") != canonical_sha256(decoding):
        raise GateValidationError("gate decoding hash mismatch")
    if bindings.get("run_seed") != 20260719:
        raise GateValidationError("gate run seed mismatch")
    boundary = document.get("execution_boundary")
    if not isinstance(boundary, Mapping) or any(value != 0 for value in boundary.values()):
        raise GateValidationError("gate falsely records execution")


def validate_references(document: Mapping[str, Any], experiment_root: Path) -> int:
    references = document.get("references")
    if not isinstance(references, list) or not references:
        raise GateValidationError("gate references missing")
    checked = 0
    for reference in references:
        relative = PurePosixPath(reference.get("path", ".."))
        if relative.is_absolute() or ".." in relative.parts:
            raise GateValidationError("unsafe gate reference")
        path = experiment_root / relative
        if not path.is_file() or sha256_file(path) != reference.get("sha256"):
            raise GateValidationError(f"gate reference mismatch: {relative}")
        checked += 1
    return checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", required=True, type=Path)
    args = parser.parse_args()

    gate_root = Path(__file__).resolve().parent
    experiment_root = Path(__file__).resolve().parents[3]
    r002_gate = (
        experiment_root
        / "runs/R002__sanity__metrics-real-toy__seed-pending__a001/formal-gate/formal-execution-gate.20260719.attempt-001.json"
    )
    lock_path = gate_root / "model-asset.lock.20260719.json"
    model_lock = load_json(lock_path)
    r001 = load_json(gate_root / "formal-execution-gate.20260719.attempt-001.json")
    r002 = load_json(r002_gate)
    file_count = validate_model_snapshot(model_lock, args.model_root)
    validate_gate_document(r001, "R001")
    validate_gate_document(r002, "R002")
    reference_count = validate_references(r001, experiment_root)
    reference_count += validate_references(r002, experiment_root)
    print("FORMAL_EXECUTION_GATE_VALIDATION: PASS")
    print(f"model_files={file_count} references_checked={reference_count}")
    print("R001=BLOCKED_MISSING_EXECUTION_BINDINGS R002=BLOCKED_PENDING_R001_OUTPUT")
    print("training=0 model_calls=0 benchmarks=0 gpu_stress=0 all_reduce=0 formal_runs=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
