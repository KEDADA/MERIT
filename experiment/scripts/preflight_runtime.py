#!/usr/bin/env python3
"""Resolve and probe the approved runtime without exposing machine-private data."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ROOT = REPOSITORY_ROOT / "experiment"
PROFILE = REPOSITORY_ROOT / "paper/02_experiments/environment/SYSTEM_PROFILE.json"
TARGET = EXPERIMENT_ROOT / "environments/runtime-target.locked.20260719.json"

RUNTIME_ALIAS = "runtime://merit-r000-h20-py312-torch211-cu130"
RUNTIME_IDENTIFIER = "merit-r000-h20-py312-torch211-cu130"
SNAPSHOT_TAG = "20260719.attempt-002"
INVENTORY_RELATIVE = Path(
    f"environments/dependency-inventory.{SNAPSHOT_TAG}.json"
)
LOCK_RELATIVE = Path(f"environments/environment-lock.{SNAPSHOT_TAG}.json")
PREFLIGHT_RELATIVE = Path(f"environments/runtime-preflight.{SNAPSHOT_TAG}.json")

SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SAFE_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.!+_~-]*$")


def _canonical_bytes(document: dict[str, Any]) -> bytes:
    return (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_version(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return ".".join(str(part) for part in value)
    digits = str(value)
    if digits.isdigit() and len(digits) == 5:
        return f"{int(digits[:-4])}.{int(digits[-4:-2])}.{int(digits[-2:])}"
    return digits


def _candidate_paths(profile: dict[str, Any]) -> list[Path]:
    """Find existing interpreters; paths remain process-local and are never returned in output."""

    candidates: list[Path] = []

    def add(raw: str | os.PathLike[str] | None) -> None:
        if not raw:
            return
        path = Path(raw).expanduser()
        if path.is_dir():
            path = path / "bin/python"
        if path.is_file() and path not in candidates:
            candidates.append(path)

    recorded = str(profile["python"]["existing_isolated_environment"]["path"])
    if not (recorded.startswith("<") and recorded.endswith(">")):
        add(recorded)
    add(os.environ.get("MERIT_RUNTIME_PYTHON"))
    add(sys.executable)
    add(shutil.which("python3"))
    add(shutil.which("python"))

    home = Path.home()
    for registry in (
        home / ".conda/environments.txt",
        home / ".config/conda/environments.txt",
    ):
        try:
            prefixes = registry.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for prefix in prefixes:
            if prefix.strip():
                add(Path(prefix.strip()) / "bin/python")

    uv = shutil.which("uv")
    if uv:
        safe_environment = dict(os.environ)
        safe_environment.update({"UV_OFFLINE": "1", "UV_NO_MANAGED_PYTHON": "1"})
        try:
            completed = subprocess.run(
                [uv, "python", "list", "--only-installed", "--output-format", "json"],
                check=False,
                capture_output=True,
                text=True,
                timeout=20,
                env=safe_environment,
            )
            records = json.loads(completed.stdout) if completed.returncode == 0 else []
            for record in records:
                add(record.get("path") or record.get("executable"))
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, TypeError):
            pass
    return candidates


def _run_json(executable: Path, code: str, timeout: int = 30) -> dict[str, Any] | None:
    try:
        completed = subprocess.run(
            [str(executable), "-I", "-c", code],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if completed.returncode != 0:
            return None
        return json.loads(completed.stdout.strip().splitlines()[-1])
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, IndexError):
        return None


def _resolve_runtime(
    profile: dict[str, Any], target: dict[str, Any]
) -> tuple[Path | None, dict[str, Any]]:
    expected = target["target"]
    expected_cuda = profile["python"]["existing_isolated_environment"][
        "torch_cuda_version"
    ]
    code = (
        "import json,sys;"
        "out={'python':'.'.join(map(str,sys.version_info[:3]))};"
        "exec(\"try:\\n import torch\\n out.update({'pytorch':torch.__version__,"
        "'torch_cuda':torch.version.cuda})\\nexcept Exception:\\n pass\");"
        "print(json.dumps(out,sort_keys=True))"
    )
    candidates = _candidate_paths(profile)
    for candidate in candidates:
        observed = _run_json(candidate, code)
        if observed == {
            "python": expected["python"],
            "pytorch": expected["pytorch"],
            "torch_cuda": expected_cuda,
        }:
            return candidate, {
                "candidates_checked": len(candidates),
                "resolution_source": "existing-runtime-registry",
                "private_path_emitted": False,
            }
    return None, {
        "candidates_checked": len(candidates),
        "resolution_source": "unavailable",
        "private_path_emitted": False,
    }


def _probe_runtime(executable: Path) -> dict[str, Any] | None:
    code = r'''
import importlib.metadata as metadata
import json
import re
import sys
import torch

safe_name = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
safe_version = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.!+_~-]*$")
packages = set()
unsafe_metadata_count = 0
for distribution in metadata.distributions():
    name = distribution.metadata.get("Name", "")
    version = distribution.version or ""
    if safe_name.fullmatch(name) and safe_version.fullmatch(version):
        normalized = re.sub(r"[-_.]+", "-", name).lower()
        packages.add((normalized, version))
    else:
        unsafe_metadata_count += 1

available = torch.cuda.is_available()
count = torch.cuda.device_count() if available else 0
models = sorted({torch.cuda.get_device_name(index) for index in range(count)})
nccl = torch.cuda.nccl.version() if available else None
print(json.dumps({
    "python": ".".join(map(str, sys.version_info[:3])),
    "pytorch": torch.__version__,
    "pytorch_cuda_runtime": torch.version.cuda,
    "cuda_available": available,
    "gpu_count": count,
    "gpu_models": models,
    "cudnn": torch.backends.cudnn.version(),
    "nccl": nccl,
    "packages": [{"name": name, "version": version} for name, version in sorted(packages)],
    "unsafe_metadata_count": unsafe_metadata_count,
}, sort_keys=True))
'''
    return _run_json(executable, code, timeout=45)


def _check(check_id: str, observed: Any, expected: Any) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "PASS" if observed == expected else "MISMATCH",
        "observed": observed,
        "expected": expected,
    }


def _build_documents(
    profile: dict[str, Any],
    target: dict[str, Any],
    observed: dict[str, Any],
    resolution: dict[str, Any],
) -> tuple[bytes, bytes, bytes, dict[str, Any]]:
    target_facts = target["target"]
    profile_runtime = profile["python"]["existing_isolated_environment"]
    observed_safe = {
        "python": str(observed["python"]),
        "pytorch": str(observed["pytorch"]),
        "pytorch_cuda_runtime": str(observed["pytorch_cuda_runtime"]),
        "cuda_available": bool(observed["cuda_available"]),
        "gpu_count": int(observed["gpu_count"]),
        "gpu_models": list(observed["gpu_models"]),
        "cudnn": _normalize_version(observed["cudnn"]),
        "nccl": _normalize_version(observed["nccl"]),
    }
    expected = {
        "python": target_facts["python"],
        "pytorch": target_facts["pytorch"],
        "pytorch_cuda_runtime": profile_runtime["torch_cuda_version"],
        "cuda_available": target_facts["pytorch_cuda_available"],
        "gpu_count": target_facts["gpu_count"],
        "gpu_models": [target_facts["gpu_model"]],
        "cudnn": target_facts["cudnn"],
        "nccl": target_facts["nccl"],
    }
    checks = [
        _check("runtime-reference-resolution", True, True),
        *[
            _check(f"{key.replace('_', '-')}", observed_safe[key], expected[key])
            for key in expected
        ],
    ]
    packages = observed.get("packages")
    if (
        not isinstance(packages, list)
        or observed.get("unsafe_metadata_count") != 0
        or any(
            not isinstance(item, dict)
            or not SAFE_NAME.fullmatch(str(item.get("name", "")))
            or not SAFE_VERSION.fullmatch(str(item.get("version", "")))
            for item in packages
        )
    ):
        raise ValueError("UNSAFE_OR_INVALID_PACKAGE_METADATA")

    captured_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    inventory = {
        "schema_version": "1.0",
        "inventory_id": "dependency-inventory-20260719-attempt-002",
        "captured_at_utc": captured_at,
        "runtime_identifier": RUNTIME_IDENTIFIER,
        "capture_method": "python-importlib.metadata-name-version-only",
        "scope": "all installed distributions visible to the isolated runtime",
        "package_count": len(packages),
        "packages": packages,
        "excluded_metadata": [
            "absolute paths",
            "direct URLs",
            "download locations",
            "installer configuration",
            "credentials",
            "host and user identity",
        ],
        "redaction": {
            "name_and_version_only": True,
            "private_runtime_path_recorded": False,
            "url_recorded": False,
            "credential_recorded": False,
            "machine_identity_recorded": False,
        },
    }
    inventory_bytes = _canonical_bytes(inventory)
    inventory_sha256 = _sha256_bytes(inventory_bytes)

    source_references = {
        "target": {
            "path": "environments/runtime-target.locked.20260719.json",
            "sha256": _file_sha256(TARGET),
        },
        "r000_profile": {
            "path": "repository://paper/02_experiments/environment/SYSTEM_PROFILE.json",
            "sha256": _file_sha256(PROFILE),
        },
    }
    environment_lock = {
        "schema_version": "1.0",
        "lock_id": "environment-lock-20260719-attempt-002",
        "status": "RUNTIME_ENVIRONMENT_LOCKED",
        "captured_at_utc": captured_at,
        "base_commit": target["base_commit"],
        "runtime_alias": RUNTIME_ALIAS,
        "sources": source_references,
        "observed": observed_safe,
        "dependency_inventory": {
            "path": INVENTORY_RELATIVE.as_posix(),
            "sha256": inventory_sha256,
            "package_count": len(packages),
            "fields": ["normalized package name", "version"],
        },
        "capture": {
            "probe_script": "scripts/preflight_runtime.py",
            "probe_script_sha256": _file_sha256(Path(__file__)),
            "resolution_source": resolution["resolution_source"],
            "metadata_only": True,
            "private_executable_reference_recorded": False,
        },
        "safety_boundary": {
            "training_runs": 0,
            "model_inference_calls": 0,
            "benchmarks": 0,
            "gpu_stress_tests": 0,
            "collective_communication_tests": 0,
            "dependencies_installed_or_downloaded": 0,
            "formal_r001_r002_runs": 0,
        },
        "readiness": {
            "metadata_runtime": "READY",
            "real_toy_adapter_engineering": "READY_ENVIRONMENT_ONLY",
            "formal_r001_r002": "BLOCKED_PENDING_MODEL_DATA_ADAPTER_AND_RUN_MANIFEST",
        },
    }
    lock_bytes = _canonical_bytes(environment_lock)
    lock_sha256 = _sha256_bytes(lock_bytes)

    checks.append(
        {
            "check_id": "dependency-inventory",
            "status": "PASS",
            "observed": {
                "path": INVENTORY_RELATIVE.as_posix(),
                "sha256": inventory_sha256,
                "package_count": len(packages),
            },
            "expected": "safe name/version inventory with SHA-256",
        }
    )
    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "MISMATCH"
    preflight = {
        "schema_version": "1.0",
        "preflight_id": "runtime-preflight-20260719-attempt-002",
        "status": status,
        "captured_at_utc": captured_at,
        "target": source_references["target"],
        "evidence": source_references["r000_profile"],
        "environment_lock": {
            "path": LOCK_RELATIVE.as_posix(),
            "sha256": lock_sha256,
        },
        "dependency_inventory": {
            "path": INVENTORY_RELATIVE.as_posix(),
            "sha256": inventory_sha256,
        },
        "resolution": resolution,
        "checks": checks,
        "redaction": {
            "private_runtime_path_recorded": False,
            "hostname_recorded": False,
            "username_recorded": False,
            "ip_address_recorded": False,
            "gpu_uuid_recorded": False,
            "credential_recorded": False,
            "url_recorded": False,
        },
        "prohibited_actions": {
            "installation": False,
            "download": False,
            "training": False,
            "model_inference": False,
            "benchmark": False,
            "gpu_stress": False,
            "all_reduce_or_collective": False,
            "formal_run": False,
        },
        "readiness": environment_lock["readiness"],
    }
    preflight_bytes = _canonical_bytes(preflight)
    summary = {
        "status": status,
        "observed": observed_safe,
        "package_count": len(packages),
        "inventory_sha256": inventory_sha256,
        "environment_lock_sha256": lock_sha256,
        "private_path_emitted": False,
        "benchmark_run": False,
        "formal_run": False,
    }
    return inventory_bytes, lock_bytes, preflight_bytes, summary


def _write_snapshots(contents: tuple[bytes, bytes, bytes]) -> None:
    targets = [
        EXPERIMENT_ROOT / INVENTORY_RELATIVE,
        EXPERIMENT_ROOT / LOCK_RELATIVE,
        EXPERIMENT_ROOT / PREFLIGHT_RELATIVE,
    ]
    if any(path.exists() for path in targets):
        raise FileExistsError("IMMUTABLE_SNAPSHOT_ALREADY_EXISTS")
    for path, content in zip(targets, contents):
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture",
        action="store_true",
        help="write the fixed attempt-002 snapshots using exclusive creation",
    )
    arguments = parser.parse_args()
    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        target = json.loads(TARGET.read_text(encoding="utf-8"))
        executable, resolution = _resolve_runtime(profile, target)
        if executable is None:
            print(
                json.dumps(
                    {
                        "status": "BLOCKED_RUNTIME_REFERENCE_UNAVAILABLE",
                        **resolution,
                        "probe_started": False,
                    },
                    sort_keys=True,
                )
            )
            return 2
        observed = _probe_runtime(executable)
        if observed is None:
            print(
                json.dumps(
                    {
                        "status": "BLOCKED_RUNTIME_PROBE_FAILED",
                        "private_path_emitted": False,
                        "probe_started": True,
                    },
                    sort_keys=True,
                )
            )
            return 2
        inventory, lock, preflight, summary = _build_documents(
            profile, target, observed, resolution
        )
        if arguments.capture:
            _write_snapshots((inventory, lock, preflight))
            summary["snapshots_written"] = [
                INVENTORY_RELATIVE.as_posix(),
                LOCK_RELATIVE.as_posix(),
                PREFLIGHT_RELATIVE.as_posix(),
            ]
        else:
            summary["snapshots_written"] = []
        print(json.dumps(summary, sort_keys=True))
        return 0 if summary["status"] == "PASS" else 2
    except (OSError, ValueError, KeyError, TypeError, FileExistsError) as error:
        message = str(error)
        safe_reason = (
            message
            if message in {
                "UNSAFE_OR_INVALID_PACKAGE_METADATA",
                "IMMUTABLE_SNAPSHOT_ALREADY_EXISTS",
            }
            else "NORMALIZED_PREFLIGHT_FAILURE"
        )
        print(
            json.dumps(
                {
                    "status": "BLOCKED_RUNTIME_PREFLIGHT_INTERNAL_ERROR",
                    "reason": safe_reason,
                    "private_path_emitted": False,
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
