#!/usr/bin/env python3
"""Read-only static validation for the stage-3 experiment skeleton."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.validation import (
    validate_artifact_manifest,
    validate_atomic_input_manifest,
    validate_atomic_sanity_run_manifest,
    validate_baseline_fidelity,
    validate_data_manifest,
    validate_dependency_inventory,
    validate_dirty_worktree_inventory,
    validate_model_adapter_contract,
    validate_pilot_implementation,
    validate_pilot_implementation_lock,
    validate_run_manifest,
    validate_runtime_designation,
    validate_runtime_environment_lock,
    validate_runtime_preflight_result,
    validate_runtime_target_lock,
    validate_sanity_baseline_lock,
    validate_real_toy_index,
)
from merit_experiment.hashing import file_sha256
from merit_experiment.provenance import dirty_entries

EXPECTED_DIRECTORIES = {
    "environments",
    "configs",
    "src",
    "scripts",
    "tests",
    "data",
    "runs",
    "results",
    "artifacts",
}
REQUIRED_IGNORE_SNIPPETS = {
    ".env",
    "*secret*",
    "*token*",
    "*Token*",
    "*.pem",
    "*.log",
    "data/raw/",
    "data/processed/",
    "*.safetensors",
    "runs/**/raw/",
    "artifacts/blobs/",
    "!data/fixtures/**",
    "!runs/**/*manifest*.json",
}


def private_prefixes() -> tuple[str, ...]:
    return tuple("".join(parts) for parts in (("/", "home", "/"), ("/", "mnt", "/"), ("/", "Users", "/"), ("/", "private", "/")))


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in EXPERIMENT_ROOT.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            files.append(path)
    return sorted(files)


def check_structure(errors: list[str]) -> None:
    present_directories = {path.name for path in EXPERIMENT_ROOT.iterdir() if path.is_dir()}
    missing = EXPECTED_DIRECTORIES.difference(present_directories)
    unexpected = present_directories.difference(EXPECTED_DIRECTORIES)
    if missing:
        errors.append(f"missing top-level directories: {sorted(missing)}")
    if unexpected:
        errors.append(f"unexpected top-level directories: {sorted(unexpected)}")
    for directory in sorted(EXPECTED_DIRECTORIES):
        if not (EXPERIMENT_ROOT / directory / "README.md").is_file():
            errors.append(f"missing README: {directory}/README.md")


def check_json_and_examples(errors: list[str]) -> int:
    parsed = 0
    for path in EXPERIMENT_ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {path.relative_to(EXPERIMENT_ROOT)}: {exc}")

    try:
        validate_run_manifest(
            json.loads((EXPERIMENT_ROOT / "runs/run_manifest.example.json").read_text())
        )
        validate_data_manifest(
            json.loads((EXPERIMENT_ROOT / "data/data_manifest.example.json").read_text())
        )
        validate_artifact_manifest(
            json.loads(
                (EXPERIMENT_ROOT / "artifacts/artifact_manifest.example.json").read_text()
            )
        )
        baseline = json.loads(
            (EXPERIMENT_ROOT / "environments/baseline.json").read_text()
        )
        runtime = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-designation.pending.json").read_text()
        )
        fidelity = json.loads(
            (EXPERIMENT_ROOT / "configs/baseline-fidelity.pending.json").read_text()
        )
        implementation = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.pending.json").read_text()
        )
        implementation_lock = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.locked.20260719.json").read_text()
        )
        implementation_lock_manifest = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.locked.20260719.manifest.json").read_text()
        )
        runtime_target = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-target.locked.20260719.json").read_text()
        )
        runtime_preflight = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-preflight.20260719.json").read_text()
        )
        dependency_inventory = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/dependency-inventory.20260719.attempt-002.json"
            ).read_text()
        )
        runtime_environment_lock = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/environment-lock.20260719.attempt-002.json"
            ).read_text()
        )
        runtime_preflight_pass = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/runtime-preflight.20260719.attempt-002.json"
            ).read_text()
        )
        sanity_baseline = json.loads(
            (EXPERIMENT_ROOT / "configs/sanity-baseline.locked.20260719.json").read_text()
        )
        model_adapter_contract = json.loads(
            (EXPERIMENT_ROOT / "configs/model-adapter.contract.20260719.json").read_text()
        )
        real_toy_manifest = json.loads(
            (EXPERIMENT_ROOT / "data/real-toy-split.20260719.manifest.json").read_text()
        )
        dirty_inventory_path = (
            EXPERIMENT_ROOT / "runs/provenance/dirty-worktree.20260719.json"
        )
        dirty_inventory = json.loads(dirty_inventory_path.read_text())
        engineering_manifest = json.loads(
            (EXPERIMENT_ROOT / "configs/sanity-engineering.locked.20260719.manifest.json").read_text()
        )
        validate_runtime_designation(runtime, baseline)
        validate_baseline_fidelity(fidelity)
        validate_pilot_implementation(implementation)
        validate_pilot_implementation_lock(implementation_lock)
        validate_runtime_target_lock(runtime_target, baseline)
        validate_runtime_preflight_result(runtime_preflight)
        validate_dependency_inventory(dependency_inventory)
        validate_runtime_environment_lock(runtime_environment_lock)
        validate_runtime_preflight_result(runtime_preflight_pass)
        validate_sanity_baseline_lock(sanity_baseline)
        validate_model_adapter_contract(model_adapter_contract)
        validate_data_manifest(real_toy_manifest)
        validate_dirty_worktree_inventory(dirty_inventory)
        if dirty_entries(EXPERIMENT_ROOT.parent) != dirty_inventory["entries"]:
            raise ValueError("current dirty worktree differs from provenance inventory")

        toy_query_ids: dict[str, set[str]] = {}
        for partition in real_toy_manifest["partitions"]:
            index_path = EXPERIMENT_ROOT / partition["path_alias"]
            index_document = json.loads(index_path.read_text(encoding="utf-8"))
            validate_real_toy_index(index_document, partition["role"])
            if file_sha256(index_path) != partition["sample_index_sha256"]:
                raise ValueError(f"real toy index SHA-256 mismatch: {partition['role']}")
            toy_query_ids[partition["role"]] = {
                sample["query_id"] for sample in index_document["samples"]
            }
        if toy_query_ids["pilot_train"].intersection(toy_query_ids["pilot_audit"]):
            raise ValueError("real toy TRAIN/AUDIT indexes overlap")

        for run_id in (
            "R001__sanity__paired-replay-real-toy__seed-pending__a001",
            "R002__sanity__metrics-real-toy__seed-pending__a001",
        ):
            run_root = EXPERIMENT_ROOT / "runs" / run_id
            run_manifest = json.loads((run_root / "run-manifest.json").read_text())
            input_manifest = json.loads((run_root / "input-manifest.json").read_text())
            artifact_manifest = json.loads((run_root / "artifact-manifest.json").read_text())
            validate_atomic_sanity_run_manifest(run_manifest)
            validate_atomic_input_manifest(input_manifest)
            validate_artifact_manifest(artifact_manifest)
            if run_manifest["git"]["dirty_paths_manifest_sha256"] != file_sha256(
                dirty_inventory_path
            ):
                raise ValueError(f"atomic dirty provenance mismatch: {run_id}")
            for reference in input_manifest["references"]:
                path = EXPERIMENT_ROOT / reference["path"]
                if reference["sha256"] != file_sha256(path):
                    raise ValueError(f"atomic input SHA-256 mismatch: {reference['path']}")
            for field, filename in (
                ("input_manifest", "input-manifest.json"),
                ("artifact_manifest", "artifact-manifest.json"),
            ):
                if run_manifest[field]["sha256"] != file_sha256(run_root / filename):
                    raise ValueError(f"atomic envelope SHA-256 mismatch: {run_id}/{filename}")

        model_adapter_environment = model_adapter_contract["environment_lock"]
        if model_adapter_environment["sha256"] != file_sha256(
            EXPERIMENT_ROOT / model_adapter_environment["path"]
        ):
            raise ValueError("model adapter environment-lock SHA-256 mismatch")

        if runtime["evidence"]["baseline_sha256"] != file_sha256(
            EXPERIMENT_ROOT / runtime["evidence"]["baseline_path"]
        ):
            raise ValueError("runtime evidence SHA-256 does not match baseline.json")
        if implementation["protocol_lock"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT / implementation["protocol_lock"]["path"]
        ):
            raise ValueError("pilot implementation SHA-256 does not match protocol lock")
        if implementation_lock["protocol_lock"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT / implementation_lock["protocol_lock"]["path"]
        ):
            raise ValueError("approved implementation SHA-256 does not match protocol lock")
        if implementation_lock_manifest["approval_lock"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT / implementation_lock_manifest["approval_lock"]["path"]
        ):
            raise ValueError("Stage 2D manifest approval-lock SHA-256 mismatch")
        if implementation_lock_manifest["protocol_document"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT.parent / "paper/01_planning/PRE_RUN_PROTOCOL.md"
        ):
            raise ValueError("Stage 2D manifest protocol-document SHA-256 mismatch")
        if runtime_target["evidence"]["baseline_sha256"] != file_sha256(
            EXPERIMENT_ROOT / runtime_target["evidence"]["baseline_path"]
        ):
            raise ValueError("runtime target SHA-256 does not match baseline.json")
        if runtime_preflight["target"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT / runtime_preflight["target"]["path"]
        ):
            raise ValueError("runtime preflight target SHA-256 mismatch")
        if runtime_preflight["evidence"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT.parent
            / "paper/02_experiments/environment/SYSTEM_PROFILE.json"
        ):
            raise ValueError("runtime preflight profile SHA-256 mismatch")
        if runtime_environment_lock["sources"]["target"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT / runtime_environment_lock["sources"]["target"]["path"]
        ):
            raise ValueError("runtime environment lock target SHA-256 mismatch")
        if runtime_environment_lock["sources"]["r000_profile"]["sha256"] != file_sha256(
            EXPERIMENT_ROOT.parent
            / "paper/02_experiments/environment/SYSTEM_PROFILE.json"
        ):
            raise ValueError("runtime environment lock profile SHA-256 mismatch")
        inventory_reference = runtime_environment_lock["dependency_inventory"]
        inventory_path = EXPERIMENT_ROOT / inventory_reference["path"]
        if inventory_reference["sha256"] != file_sha256(inventory_path):
            raise ValueError("runtime dependency inventory SHA-256 mismatch")
        if inventory_reference["package_count"] != dependency_inventory["package_count"]:
            raise ValueError("runtime dependency inventory package count mismatch")
        if runtime_environment_lock["capture"]["probe_script_sha256"] != file_sha256(
            EXPERIMENT_ROOT / runtime_environment_lock["capture"]["probe_script"]
        ):
            raise ValueError("runtime probe script SHA-256 mismatch")
        for field in ("target", "evidence", "environment_lock", "dependency_inventory"):
            reference = runtime_preflight_pass[field]
            if field == "evidence":
                referenced_path = (
                    EXPERIMENT_ROOT.parent
                    / "paper/02_experiments/environment/SYSTEM_PROFILE.json"
                )
            else:
                referenced_path = EXPERIMENT_ROOT / reference["path"]
            if reference["sha256"] != file_sha256(referenced_path):
                raise ValueError(f"successful runtime preflight {field} SHA-256 mismatch")
        profile_document = json.loads(
            (
                EXPERIMENT_ROOT.parent
                / "paper/02_experiments/environment/SYSTEM_PROFILE.json"
            ).read_text()
        )
        profile_runtime_cuda = profile_document["python"][
            "existing_isolated_environment"
        ]["torch_cuda_version"]
        expected_observed = {
            "python": runtime_target["target"]["python"],
            "pytorch": runtime_target["target"]["pytorch"],
            "pytorch_cuda_runtime": profile_runtime_cuda,
            "cuda_available": runtime_target["target"]["pytorch_cuda_available"],
            "gpu_count": runtime_target["target"]["gpu_count"],
            "gpu_models": [runtime_target["target"]["gpu_model"]],
            "cudnn": runtime_target["target"]["cudnn"],
            "nccl": runtime_target["target"]["nccl"],
        }
        if runtime_environment_lock["observed"] != expected_observed:
            raise ValueError(
                f"runtime observations diverge from target/profile facts: CUDA {profile_runtime_cuda}"
            )
        for group in ("approval_snapshots", "implementation_files"):
            for reference in engineering_manifest[group]:
                relative = Path(reference["path"])
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("engineering manifest contains a private/escaping path")
                if reference["sha256"] != file_sha256(EXPERIMENT_ROOT / relative):
                    raise ValueError(
                        f"engineering manifest SHA-256 mismatch: {reference['path']}"
                    )
        boundary = engineering_manifest["execution_boundary"]
        if any(boundary[field] != 0 for field in boundary):
            raise ValueError("engineering manifest falsely records an execution side effect")
    except (OSError, ValueError) as exc:
        errors.append(f"manifest/pending-contract validation failed: {exc}")
    return parsed


def check_content(errors: list[str]) -> tuple[int, int]:
    files = iter_text_files()
    total_bytes = 0
    key_header = "-" * 5 + "BEGIN " + "PRIVATE KEY" + "-" * 5
    credential_assignment = re.compile(
        r"(?i)(api[_-]?key|password|credential)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    )
    for path in files:
        size = path.stat().st_size
        total_bytes += size
        relative = path.relative_to(EXPERIMENT_ROOT)
        if size > 1024 * 1024:
            errors.append(f"file exceeds 1 MiB skeleton limit: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"unexpected binary file: {relative}")
            continue
        for prefix in private_prefixes():
            if prefix in text:
                errors.append(f"private absolute path text in {relative}")
        if key_header in text or credential_assignment.search(text):
            errors.append(f"possible credential material in {relative}")
    return len(files), total_bytes


def check_gitignore(errors: list[str]) -> None:
    content = (EXPERIMENT_ROOT / ".gitignore").read_text(encoding="utf-8")
    missing = sorted(item for item in REQUIRED_IGNORE_SNIPPETS if item not in content)
    if missing:
        errors.append(f".gitignore missing required patterns: {missing}")


def main() -> int:
    errors: list[str] = []
    check_structure(errors)
    json_count = check_json_and_examples(errors)
    file_count, total_bytes = check_content(errors)
    check_gitignore(errors)

    if errors:
        print("SKELETON_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SKELETON_VALIDATION: PASS")
    print(f"files_checked={file_count}")
    print(f"json_documents_checked={json_count}")
    print(f"total_bytes={total_bytes}")
    print("private_paths=0 credentials=0 oversized_files=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
