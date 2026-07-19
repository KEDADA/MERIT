"""Manifest validation for traceability and pilot/confirmatory isolation."""

from __future__ import annotations

import re
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Mapping

from .constants import (
    CONFIRMATORY_ROLES,
    EXECUTABLE_STATUSES,
    FAILURE_TYPES,
    PILOT_ROLES,
    RUN_STATUSES,
    USER_APPROVAL_REQUIRED,
)

RUN_ID_RE = re.compile(
    r"^(R[0-9]{3})__[a-z0-9-]+__[a-z0-9-]+__seed-(pending|-?[0-9]+)__a[0-9]{3}$"
)
FAMILY_ID_RE = re.compile(r"^R[0-9]{3}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
PACKAGE_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PACKAGE_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.!+_~-]*$")
REAL_TOY_QUERY_ID_RE = re.compile(r"^(alfworld|hotpotqa):[a-f0-9]{64}$")

RUNTIME_PREFLIGHT_IDS = frozenset(
    {
        "python-version",
        "pytorch-version",
        "cuda-visibility",
        "gpu-inventory",
        "dependency-lock-consistency",
    }
)

RUNTIME_SUCCESS_PREFLIGHT_IDS = frozenset(
    {
        "runtime-reference-resolution",
        "python",
        "pytorch",
        "pytorch-cuda-runtime",
        "cuda-available",
        "gpu-count",
        "gpu-models",
        "cudnn",
        "nccl",
        "dependency-inventory",
    }
)

BASELINE_APPROVAL_FIELDS = frozenset(
    {
        "implementation_mode",
        "source_reference",
        "source_revision",
        "license_verification",
        "model_revision",
        "dataset_revision",
        "adapter_entrypoint",
        "fidelity_checklist_path",
        "deviations_manifest_path",
        "shared_retrieval_and_budget_contract",
    }
)

PILOT_IMPLEMENTATION_RULE_FIELDS = {
    "fixed-heldout-audit-query-set": frozenset(
        {"construction_algorithm", "sample_size", "sample_id_manifest_contract"}
    ),
    "train-priority-score-contract": frozenset(
        {"uncertainty_score", "utility_usage_score", "normalization", "tie_breaking"}
    ),
    "neutral-pad-token-length-matching": frozenset(
        {"tokenizer_revision", "exact_matching_algorithm", "impossible_match_behavior"}
    ),
    "paired-bundle-budget-ceiling": frozenset(
        {"bundle_admission_policy", "worst_case_cost_estimator", "ceiling_hit_status"}
    ),
    "sr-slope-clustered-interval": frozenset(
        {"slope_estimator", "task_clustered_resampling", "holm_interval_construction"}
    ),
    "shared-control-and-deployment-reuse": frozenset(
        {
            "shared_control_rollout_count",
            "deployment_rollout_reuse_eligibility",
            "reuse_accounting_and_provenance",
        }
    ),
}


class ManifestValidationError(ValueError):
    """Raised when a skeleton manifest violates a hard invariant."""


def _require_fields(value: Mapping[str, Any], fields: set[str], context: str) -> None:
    missing = sorted(fields.difference(value))
    if missing:
        raise ManifestValidationError(f"{context} missing fields: {', '.join(missing)}")


def _is_path_alias(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute():
        return False
    return True


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA256_RE.fullmatch(value))


def _contains_pending(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(_contains_pending(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_pending(item) for item in value)
    return value in {USER_APPROVAL_REQUIRED, "NOT_COMPUTED_TEMPLATE"}


def _contains_literal(value: Any, literal: str) -> bool:
    if isinstance(value, Mapping):
        return any(
            key == literal or _contains_literal(item, literal)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_literal(item, literal) for item in value)
    return value == literal


def validate_run_manifest(manifest: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "run_id",
        "run_family_id",
        "phase",
        "status",
        "failure",
        "seed",
        "git",
        "config_snapshot",
        "environment_snapshot",
        "data_manifest",
        "logs",
        "raw_outputs",
        "artifact_manifest",
        "timestamps",
    }
    _require_fields(manifest, required, "run manifest")

    match = RUN_ID_RE.fullmatch(str(manifest["run_id"]))
    if not match:
        raise ManifestValidationError("invalid atomic run_id")
    family = str(manifest["run_family_id"])
    if not FAMILY_ID_RE.fullmatch(family) or family != match.group(1):
        raise ManifestValidationError("run_family_id does not match run_id")
    if manifest["phase"] not in {"sanity", "pilot", "confirmatory", "secondary"}:
        raise ManifestValidationError("invalid run phase")
    if manifest["status"] not in RUN_STATUSES:
        raise ManifestValidationError("invalid run status")

    failure = manifest["failure"]
    if not isinstance(failure, Mapping):
        raise ManifestValidationError("failure must be an object")
    _require_fields(failure, {"type", "message"}, "failure")
    if failure["type"] not in FAILURE_TYPES:
        raise ManifestValidationError("invalid failure type")
    if manifest["status"] == "SUCCEEDED" and failure["type"] != "NONE":
        raise ManifestValidationError("SUCCEEDED requires failure.type=NONE")
    if manifest["status"] == "FAILED" and failure["type"] == "NONE":
        raise ManifestValidationError("FAILED requires a non-NONE failure type")

    git_record = manifest["git"]
    timestamps = manifest["timestamps"]
    if not isinstance(git_record, Mapping) or not isinstance(timestamps, Mapping):
        raise ManifestValidationError("git and timestamps must be objects")
    _require_fields(
        git_record,
        {"base_commit", "code_commit", "dirty_worktree", "dirty_paths_manifest_sha256"},
        "git",
    )
    _require_fields(timestamps, {"created_at", "started_at", "finished_at"}, "timestamps")
    if not isinstance(manifest["logs"], list) or not isinstance(manifest["raw_outputs"], list):
        raise ManifestValidationError("logs and raw_outputs must be arrays")

    if manifest["status"] in EXECUTABLE_STATUSES:
        if not isinstance(manifest["seed"], int):
            raise ManifestValidationError("an executable run requires an integer seed")
        if match.group(2) != str(manifest["seed"]):
            raise ManifestValidationError("run_id seed does not match manifest seed")
        if _contains_pending(manifest):
            raise ManifestValidationError("an executable run contains unresolved/template values")
        for field in ("config_snapshot", "environment_snapshot", "data_manifest", "artifact_manifest"):
            reference = manifest[field]
            if not isinstance(reference, Mapping):
                raise ManifestValidationError(f"{field} must be an object")
            _require_fields(reference, {"path", "sha256"}, field)
            if not _is_path_alias(reference["path"]) or not _is_sha256(reference["sha256"]):
                raise ManifestValidationError(f"invalid executable reference: {field}")


def validate_dirty_worktree_inventory(document: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "inventory_id",
        "provenance_revision",
        "base_commit",
        "head_commit",
        "dirty_worktree",
        "content_identity",
        "generated_envelope_exclusions",
        "entries",
        "entry_count",
    }
    if set(document) != required:
        raise ManifestValidationError("dirty worktree inventory fields are invalid")
    if (
        document["inventory_id"] != "dirty-worktree-20260719-v1"
        or document["provenance_revision"] != "merit-dirty-worktree-inventory-v1"
        or document["base_commit"] != "4280484e035191b66f77618b7729dbd465d8b828"
        or document["head_commit"] != document["base_commit"]
        or document["dirty_worktree"] is not True
    ):
        raise ManifestValidationError("dirty worktree inventory identity is invalid")
    expected_exclusions = [
        "experiment/runs/provenance/dirty-worktree.20260719.json",
        "experiment/runs/R001__sanity__paired-replay-real-toy__seed-pending__a001/",
        "experiment/runs/R002__sanity__metrics-real-toy__seed-pending__a001/",
    ]
    if document["generated_envelope_exclusions"] != expected_exclusions:
        raise ManifestValidationError("dirty inventory exclusions are not the locked envelope set")
    entries = document["entries"]
    if not isinstance(entries, list) or document["entry_count"] != len(entries) or not entries:
        raise ManifestValidationError("dirty worktree entry count is invalid")
    observed_paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != {
            "kind",
            "path",
            "sha256",
            "size_bytes",
            "status",
        }:
            raise ManifestValidationError("dirty worktree entry fields are invalid")
        path = entry["path"]
        if (
            not _is_path_alias(path)
            or ".." in PurePosixPath(path).parts
            or entry["kind"] not in {"file", "symlink"}
            or not _is_sha256(entry["sha256"])
            or not isinstance(entry["size_bytes"], int)
            or entry["size_bytes"] < 0
            or not isinstance(entry["status"], str)
            or len(entry["status"]) != 2
        ):
            raise ManifestValidationError("dirty worktree entry identity is invalid")
        observed_paths.append(path)
    if observed_paths != sorted(set(observed_paths)):
        raise ManifestValidationError("dirty worktree paths must be unique and sorted")


def validate_atomic_input_manifest(document: Mapping[str, Any]) -> None:
    _require_fields(
        document,
        {
            "schema_version",
            "manifest_id",
            "run_id",
            "status",
            "references",
            "resolved_reference_count",
            "unresolved_execution_bindings",
            "readiness",
            "execution_boundary",
        },
        "atomic input manifest",
    )
    if (
        document["status"] != "COMPLETE_STRUCTURAL_PROVENANCE_EXECUTION_BINDING_REQUIRED"
        or not RUN_ID_RE.fullmatch(str(document["run_id"]))
        or document["run_id"].split("__", 1)[0] not in {"R001", "R002"}
    ):
        raise ManifestValidationError("atomic input manifest identity is invalid")
    references = document["references"]
    if (
        not isinstance(references, list)
        or len(references) < 8
        or document["resolved_reference_count"] != len(references)
    ):
        raise ManifestValidationError("atomic input reference inventory is incomplete")
    paths: set[str] = set()
    kinds: set[str] = set()
    for reference in references:
        if not isinstance(reference, Mapping) or set(reference) != {"kind", "path", "sha256"}:
            raise ManifestValidationError("atomic input reference fields are invalid")
        if (
            not isinstance(reference["kind"], str)
            or not _is_path_alias(reference["path"])
            or ".." in PurePosixPath(reference["path"]).parts
            or not _is_sha256(reference["sha256"])
            or reference["path"] in paths
        ):
            raise ManifestValidationError("atomic input reference identity is invalid")
        paths.add(reference["path"])
        kinds.add(reference["kind"])
    required_kinds = {
        "atomic_config",
        "environment_lock",
        "real_toy_data_manifest",
        "pilot_protocol_lock",
        "pilot_implementation_lock",
        "sanity_baseline_lock",
        "implementation_source",
        "dirty_worktree_inventory",
    }
    if not required_kinds.issubset(kinds):
        raise ManifestValidationError("atomic input reference kinds are incomplete")
    unresolved = document["unresolved_execution_bindings"]
    if not isinstance(unresolved, list) or len(unresolved) < 2 or len(set(unresolved)) != len(unresolved):
        raise ManifestValidationError("atomic input execution bindings are not explicit")
    if document["readiness"] != {
        "atomic_manifest_and_input_provenance": "READY_STRUCTURAL_ONLY",
        "formal_execution_gate": "BLOCKED_NOT_EVALUATED",
    }:
        raise ManifestValidationError("atomic input manifest overstates readiness")
    boundary = document["execution_boundary"]
    if not isinstance(boundary, Mapping) or set(boundary) != {
        "training_runs",
        "model_inference_calls",
        "benchmarks",
        "gpu_stress_tests",
        "collective_communication_tests",
        "formal_r001_r002_runs",
    } or any(value != 0 for value in boundary.values()):
        raise ManifestValidationError("atomic input manifest records a prohibited action")


def validate_atomic_sanity_run_manifest(document: Mapping[str, Any]) -> None:
    validate_run_manifest(document)
    _require_fields(
        document,
        {"input_manifest", "execution_authorized", "readiness", "execution_gate"},
        "atomic sanity run manifest",
    )
    expected_ids = {
        "R001__sanity__paired-replay-real-toy__seed-pending__a001",
        "R002__sanity__metrics-real-toy__seed-pending__a001",
    }
    if (
        document["run_id"] not in expected_ids
        or document["status"] != "BLOCKED"
        or document["seed"] != "FORMAL_GATE_REQUIRED"
        or document["failure"] != {
            "type": "USER_APPROVAL_REQUIRED",
            "message": "Formal R001/R002 execution gate has not been evaluated; this atomic manifest is not executable.",
        }
        or document["execution_authorized"] is not False
    ):
        raise ManifestValidationError("atomic sanity manifest is executable or misidentified")
    git_record = document["git"]
    if (
        git_record.get("base_commit") != "4280484e035191b66f77618b7729dbd465d8b828"
        or git_record.get("code_commit") != git_record.get("base_commit")
        or git_record.get("dirty_worktree") is not True
        or not _is_sha256(git_record.get("dirty_paths_manifest_sha256"))
    ):
        raise ManifestValidationError("atomic sanity git provenance is invalid")
    for field in (
        "config_snapshot",
        "environment_snapshot",
        "data_manifest",
        "input_manifest",
        "artifact_manifest",
    ):
        reference = document[field]
        if (
            not isinstance(reference, Mapping)
            or set(reference) != {"path", "sha256"}
            or not _is_path_alias(reference["path"])
            or not _is_sha256(reference["sha256"])
        ):
            raise ManifestValidationError(f"atomic sanity {field} reference is invalid")
    if document["logs"] or document["raw_outputs"]:
        raise ManifestValidationError("blocked atomic sanity manifest cannot record outputs")
    if document["readiness"] != {
        "atomic_manifest_and_input_provenance": "READY_STRUCTURAL_ONLY",
        "formal_execution_gate": "BLOCKED_NOT_EVALUATED",
    } or document["execution_gate"] != {
        "status": "NOT_EVALUATED",
        "next_step": "formal-r001-r002-execution-gate",
    }:
        raise ManifestValidationError("atomic sanity manifest opens the formal gate early")


def validate_data_manifest(manifest: Mapping[str, Any]) -> None:
    _require_fields(
        manifest,
        {"schema_version", "manifest_id", "partitions", "disjointness_checks"},
        "data manifest",
    )
    partitions = manifest["partitions"]
    checks = manifest["disjointness_checks"]
    if not isinstance(partitions, list) or not isinstance(checks, list):
        raise ManifestValidationError("partitions and disjointness_checks must be arrays")

    partition_ids: set[str] = set()
    sample_indexes: set[str] = set()
    for partition in partitions:
        if not isinstance(partition, Mapping):
            raise ManifestValidationError("partition must be an object")
        _require_fields(
            partition,
            {"partition_id", "phase", "role", "path_alias", "sha256", "sample_index_sha256"},
            "partition",
        )
        partition_id = str(partition["partition_id"])
        if not partition_id or partition_id in partition_ids:
            raise ManifestValidationError("partition_id must be non-empty and unique")
        partition_ids.add(partition_id)

        phase = partition["phase"]
        role = partition["role"]
        if phase == "pilot" and role not in PILOT_ROLES:
            raise ManifestValidationError("pilot partition has a confirmatory role")
        if phase == "confirmatory" and role not in CONFIRMATORY_ROLES:
            raise ManifestValidationError("confirmatory partition has a pilot role")
        if phase not in {"pilot", "confirmatory"}:
            raise ManifestValidationError("invalid data phase")
        if role == "sealed_final_audit" and partition.get("selection_blind") is not True:
            raise ManifestValidationError("sealed_final_audit must declare selection_blind=true")
        if not _is_path_alias(partition["path_alias"]):
            raise ManifestValidationError("data paths must be non-private path aliases")
        if not _is_sha256(partition["sha256"]) or not _is_sha256(partition["sample_index_sha256"]):
            raise ManifestValidationError("partition SHA-256 fields are invalid")
        if partition["sample_index_sha256"] in sample_indexes:
            raise ManifestValidationError("two roles reuse the same sample index")
        sample_indexes.add(partition["sample_index_sha256"])

    observed_pairs: set[frozenset[str]] = set()
    for check in checks:
        if not isinstance(check, Mapping):
            raise ManifestValidationError("disjointness check must be an object")
        _require_fields(
            check,
            {"left_partition_id", "right_partition_id", "overlap_count", "checked_by", "checked_at"},
            "disjointness check",
        )
        left = str(check["left_partition_id"])
        right = str(check["right_partition_id"])
        if left == right or left not in partition_ids or right not in partition_ids:
            raise ManifestValidationError("disjointness check references invalid partitions")
        if check["overlap_count"] != 0:
            raise ManifestValidationError("role leakage detected: overlap_count is not zero")
        observed_pairs.add(frozenset({left, right}))

    expected_pairs = {
        frozenset({left, right})
        for index, left in enumerate(sorted(partition_ids))
        for right in sorted(partition_ids)[index + 1 :]
    }
    if observed_pairs != expected_pairs:
        raise ManifestValidationError("pairwise role-disjointness proof is incomplete")

    if manifest.get("status") == "REAL_TOY_SPLIT_READY":
        validate_real_toy_data_manifest(manifest)


def validate_real_toy_index(document: Mapping[str, Any], expected_role: str) -> None:
    if set(document) != {"schema_version", "adapter_revision", "phase", "role", "samples"}:
        raise ManifestValidationError("real toy index fields are invalid")
    if (
        document["schema_version"] != "1.0"
        or document["adapter_revision"] != "merit-real-toy-data-adapter-v1"
        or document["phase"] != "pilot"
        or document["role"] != expected_role
        or expected_role not in {"pilot_train", "pilot_audit"}
    ):
        raise ManifestValidationError("real toy index identity is invalid")
    samples = document["samples"]
    expected_per_stream = 7 if expected_role == "pilot_train" else 3
    if not isinstance(samples, list) or len(samples) != 2 * expected_per_stream:
        raise ManifestValidationError("real toy index record count is invalid")
    query_ids: set[str] = set()
    stream_counts = {"alfworld": 0, "hotpotqa": 0}
    for sample in samples:
        if not isinstance(sample, Mapping) or set(sample) != {
            "query_id",
            "source_locator",
            "stream_id",
        }:
            raise ManifestValidationError("real toy sample exposes payload or misses identity")
        query_id = sample["query_id"]
        stream_id = sample["stream_id"]
        locator = sample["source_locator"]
        if (
            not isinstance(query_id, str)
            or not REAL_TOY_QUERY_ID_RE.fullmatch(query_id)
            or query_id in query_ids
            or stream_id not in stream_counts
            or not isinstance(locator, str)
            or not locator
            or PurePosixPath(locator).is_absolute()
            or PureWindowsPath(locator).is_absolute()
            or ".." in PurePosixPath(locator).parts
        ):
            raise ManifestValidationError("real toy sample identity or locator is invalid")
        if not query_id.startswith(f"{stream_id}:"):
            raise ManifestValidationError("real toy query ID does not match stream")
        query_ids.add(query_id)
        stream_counts[stream_id] += 1
    if any(count != expected_per_stream for count in stream_counts.values()):
        raise ManifestValidationError("real toy split is not balanced per stream")


def validate_real_toy_data_manifest(document: Mapping[str, Any]) -> None:
    _require_fields(
        document,
        {
            "schema_version",
            "manifest_id",
            "status",
            "base_commit",
            "captured_at_utc",
            "adapter_revision",
            "sources",
            "selection",
            "partitions",
            "disjointness_checks",
            "readiness",
            "execution_boundary",
        },
        "real toy data manifest",
    )
    if (
        document["manifest_id"] != "r001-r002-real-toy-split-20260719-v1"
        or document["status"] != "REAL_TOY_SPLIT_READY"
        or document["base_commit"] != "4280484e035191b66f77618b7729dbd465d8b828"
        or document["adapter_revision"] != "merit-real-toy-data-adapter-v1"
    ):
        raise ManifestValidationError("real toy data manifest identity is invalid")
    sources = document["sources"]
    expected_source_ids = {
        "alfworld_trajectory_archive",
        "alfworld_game_archive",
        "hotpotqa_trace_jsonl",
    }
    if (
        not isinstance(sources, list)
        or any(not isinstance(source, Mapping) for source in sources)
        or {source.get("source_id") for source in sources} != expected_source_ids
    ):
        raise ManifestValidationError("real toy source inventory is incomplete")
    for source in sources:
        _require_fields(
            source,
            {"source_id", "path_alias", "source_uri", "source_revision", "license", "sha256", "size_bytes"},
            "real toy source",
        )
        if (
            not _is_path_alias(source["path_alias"])
            or not isinstance(source["source_uri"], str)
            or not source["source_uri"].startswith("https://")
            or not isinstance(source["source_revision"], str)
            or not source["source_revision"]
            or not isinstance(source["license"], str)
            or not source["license"]
            or not _is_sha256(source["sha256"])
            or not isinstance(source["size_bytes"], int)
            or source["size_bytes"] <= 0
        ):
            raise ManifestValidationError("real toy source provenance is invalid")
    selection = document["selection"]
    if (
        not isinstance(selection, Mapping)
        or selection.get("selector_seed") != 20260719
        or selection.get("eligible_universe_count") != {"alfworld": 140, "hotpotqa": 100}
        or selection.get("toy_tasks_per_stream") != 10
        or selection.get("outcomes_or_rewards_used_for_selection") is not False
    ):
        raise ManifestValidationError("real toy selection violates the locked design")
    partitions = document["partitions"]
    by_role = {partition.get("role"): partition for partition in partitions}
    if set(by_role) != {"pilot_train", "pilot_audit"}:
        raise ManifestValidationError("real toy partitions must be TRAIN and AUDIT only")
    expected_counts = {"pilot_train": (14, 7), "pilot_audit": (6, 3)}
    for role, (record_count, per_stream) in expected_counts.items():
        partition = by_role[role]
        expected_path = f"data/indexes/real-toy-{role}.20260719.index.json"
        if (
            partition.get("path_alias") != expected_path
            or partition.get("record_count") != record_count
            or partition.get("stream_counts") != {"alfworld": per_stream, "hotpotqa": per_stream}
            or partition.get("sha256") != partition.get("sample_index_sha256")
        ):
            raise ManifestValidationError("real toy partition metadata is invalid")
    readiness = document["readiness"]
    if readiness != {
        "model_adapter": "READY_ENGINEERING_ONLY",
        "data_adapter": "READY_ENGINEERING_ONLY",
        "real_toy_split": "READY",
        "atomic_run_manifest_and_input_provenance": "BLOCKED",
        "formal_r001_r002": "BLOCKED",
    }:
        raise ManifestValidationError("real toy manifest overstates readiness")
    boundary = document["execution_boundary"]
    expected_boundary = {
        "data_archives_downloaded": 2,
        "real_task_payloads_committed_to_repo": 0,
        "training_runs": 0,
        "model_inference_calls": 0,
        "benchmarks": 0,
        "gpu_stress_tests": 0,
        "collective_communication_tests": 0,
        "formal_r001_r002_runs": 0,
    }
    if boundary != expected_boundary:
        raise ManifestValidationError("real toy manifest records a prohibited action")


def validate_artifact_manifest(manifest: Mapping[str, Any]) -> None:
    _require_fields(manifest, {"schema_version", "run_id", "artifacts"}, "artifact manifest")
    if not RUN_ID_RE.fullmatch(str(manifest["run_id"])):
        raise ManifestValidationError("artifact manifest has an invalid run_id")
    if not isinstance(manifest["artifacts"], list):
        raise ManifestValidationError("artifacts must be an array")
    artifact_ids: set[str] = set()
    for artifact in manifest["artifacts"]:
        if not isinstance(artifact, Mapping):
            raise ManifestValidationError("artifact must be an object")
        _require_fields(
            artifact,
            {"artifact_id", "kind", "path_alias", "sha256", "size_bytes", "created_by"},
            "artifact",
        )
        artifact_id = str(artifact["artifact_id"])
        if not artifact_id or artifact_id in artifact_ids:
            raise ManifestValidationError("artifact_id must be non-empty and unique")
        artifact_ids.add(artifact_id)
        if not _is_path_alias(artifact["path_alias"]):
            raise ManifestValidationError("artifact paths must be non-private path aliases")
        if not _is_sha256(artifact["sha256"]):
            raise ManifestValidationError("artifact SHA-256 is invalid")
        if not isinstance(artifact["size_bytes"], int) or artifact["size_bytes"] < 0:
            raise ManifestValidationError("artifact size_bytes is invalid")


def validate_runtime_designation(
    document: Mapping[str, Any], baseline: Mapping[str, Any] | None = None
) -> None:
    """Validate the deliberately non-executable runtime designation template."""

    _require_fields(
        document,
        {
            "schema_version",
            "candidate_id",
            "status",
            "evidence",
            "confirmed_facts",
            "designation",
            "required_preflight",
            "readiness",
            "non_claims",
        },
        "runtime designation",
    )
    if document["status"] != "BLOCKED":
        raise ManifestValidationError("pending runtime designation must remain BLOCKED")

    evidence = document["evidence"]
    if not isinstance(evidence, Mapping):
        raise ManifestValidationError("runtime evidence must be an object")
    _require_fields(evidence, {"baseline_path", "baseline_sha256"}, "runtime evidence")
    if evidence["baseline_path"] != "environments/baseline.json":
        raise ManifestValidationError("runtime evidence must reference the committed path alias")
    if not _is_sha256(evidence["baseline_sha256"]):
        raise ManifestValidationError("runtime baseline SHA-256 is invalid")

    facts = document["confirmed_facts"]
    designation = document["designation"]
    if not isinstance(facts, Mapping) or not isinstance(designation, Mapping):
        raise ManifestValidationError("runtime facts and designation must be objects")
    expected_designation_fields = {
        "project_runtime_alias",
        "environment_snapshot_path",
        "environment_snapshot_sha256",
        "dependency_lockfile_path",
        "dependency_lockfile_sha256",
        "installation_source_policy",
        "container_image_digest",
    }
    _require_fields(designation, expected_designation_fields, "runtime designation fields")
    if set(designation) != expected_designation_fields or any(
        value != USER_APPROVAL_REQUIRED for value in designation.values()
    ):
        raise ManifestValidationError("pending runtime designation contains an invented lock value")

    if baseline is not None:
        expected_facts = {
            "gpu_model": baseline["hardware"]["gpu_model"],
            "gpu_count": baseline["hardware"]["gpu_count"],
            "python": baseline["software"]["python"],
            "pytorch": baseline["software"]["pytorch"],
            "pytorch_cuda_available_at_r000": baseline["software"]["cuda_available_in_pytorch"],
            "cuda_driver_reported": baseline["software"]["cuda_driver_reported"],
            "cudnn": baseline["software"]["cudnn"],
            "nccl": baseline["software"]["nccl"],
        }
        if dict(facts) != expected_facts:
            raise ManifestValidationError("runtime confirmed facts diverge from the R000 baseline")

    checks = document["required_preflight"]
    if not isinstance(checks, list):
        raise ManifestValidationError("required_preflight must be an array")
    observed_ids: set[str] = set()
    for check in checks:
        if not isinstance(check, Mapping):
            raise ManifestValidationError("runtime preflight check must be an object")
        _require_fields(check, {"check_id", "expected_from", "status"}, "runtime preflight")
        check_id = str(check["check_id"])
        if check_id in observed_ids or check["status"] != "NOT_RUN":
            raise ManifestValidationError("pending runtime preflight must be unique and NOT_RUN")
        observed_ids.add(check_id)
    if observed_ids != RUNTIME_PREFLIGHT_IDS:
        raise ManifestValidationError("runtime preflight checklist is incomplete")

    readiness = document["readiness"]
    if not isinstance(readiness, Mapping) or readiness.get("r001_r002") != "BLOCKED":
        raise ManifestValidationError("pending runtime must block R001/R002")


def validate_baseline_fidelity(document: Mapping[str, Any]) -> None:
    """Validate representative-baseline provenance without asserting fidelity."""

    _require_fields(
        document,
        {"schema_version", "template_id", "status", "reporting_policy", "baselines", "gate"},
        "baseline fidelity",
    )
    if document["status"] != "BLOCKED":
        raise ManifestValidationError("pending baseline fidelity must remain BLOCKED")
    policy = document["reporting_policy"]
    if not isinstance(policy, Mapping):
        raise ManifestValidationError("baseline reporting policy must be an object")
    if (
        policy.get("exact_method_name_requires") != "source_faithful_checklist_pass"
        or policy.get("otherwise_label_as") != "standardized_credit_variant_wrapper"
        or policy.get("allowed_implementation_modes")
        != ["source_faithful", "standardized_credit_variant_wrapper"]
    ):
        raise ManifestValidationError("baseline reporting-mode distinction was weakened")

    baselines = document["baselines"]
    if not isinstance(baselines, list):
        raise ManifestValidationError("baselines must be an array")
    expected = {
        "reasoningbank-style": "ReasoningBank-style",
        "memrl-style": "MemRL-style",
    }
    observed: dict[str, str] = {}
    for baseline in baselines:
        if not isinstance(baseline, Mapping):
            raise ManifestValidationError("baseline entry must be an object")
        _require_fields(
            baseline,
            set(BASELINE_APPROVAL_FIELDS)
            | {"baseline_id", "approved_class_label", "affected_run_families"},
            "baseline entry",
        )
        baseline_id = str(baseline["baseline_id"])
        if baseline_id in observed:
            raise ManifestValidationError("baseline_id must be unique")
        observed[baseline_id] = str(baseline["approved_class_label"])
        if any(baseline[field] != USER_APPROVAL_REQUIRED for field in BASELINE_APPROVAL_FIELDS):
            raise ManifestValidationError("pending baseline contains an invented fidelity value")
        families = baseline["affected_run_families"]
        if not isinstance(families, list) or not families or not all(
            FAMILY_ID_RE.fullmatch(str(family)) for family in families
        ):
            raise ManifestValidationError("baseline affected_run_families is invalid")
    if observed != expected:
        raise ManifestValidationError("representative baseline set or labels changed")

    gate = document["gate"]
    if not isinstance(gate, Mapping) or any(
        gate.get(field) != "BLOCKED" for field in ("m0_r001", "m1_r010_r011")
    ):
        raise ManifestValidationError("unresolved baseline fidelity must block M0/M1 paths")


def validate_pilot_implementation(document: Mapping[str, Any]) -> None:
    """Validate all six unresolved Stage-2C engineering contracts and invariants."""

    _require_fields(
        document,
        {"schema_version", "template_id", "status", "protocol_lock", "rules", "invariants"},
        "pilot implementation",
    )
    if document["status"] != "BLOCKED":
        raise ManifestValidationError("pending pilot implementation must remain BLOCKED")
    protocol = document["protocol_lock"]
    if not isinstance(protocol, Mapping):
        raise ManifestValidationError("protocol_lock must be an object")
    _require_fields(protocol, {"path", "sha256"}, "protocol_lock")
    if protocol["path"] != "configs/pilot-protocol.locked.20260719.json" or not _is_sha256(
        protocol["sha256"]
    ):
        raise ManifestValidationError("pilot implementation protocol reference is invalid")

    rules = document["rules"]
    if not isinstance(rules, list):
        raise ManifestValidationError("pilot implementation rules must be an array")
    observed: set[str] = set()
    for rule in rules:
        if not isinstance(rule, Mapping):
            raise ManifestValidationError("pilot implementation rule must be an object")
        _require_fields(rule, {"rule_id", "status", "required_resolution", "blocks"}, "rule")
        rule_id = str(rule["rule_id"])
        if rule_id in observed or rule_id not in PILOT_IMPLEMENTATION_RULE_FIELDS:
            raise ManifestValidationError("pilot implementation rule is duplicate or unknown")
        observed.add(rule_id)
        if rule["status"] != USER_APPROVAL_REQUIRED:
            raise ManifestValidationError("unapproved implementation rule lost its marker")
        resolution = rule["required_resolution"]
        if not isinstance(resolution, Mapping):
            raise ManifestValidationError("required_resolution must be an object")
        if set(resolution) != set(PILOT_IMPLEMENTATION_RULE_FIELDS[rule_id]) or any(
            value != USER_APPROVAL_REQUIRED for value in resolution.values()
        ):
            raise ManifestValidationError("implementation resolution is incomplete or invented")
        if not isinstance(rule["blocks"], list) or not rule["blocks"]:
            raise ManifestValidationError("implementation rule must name a blocked path")
    if observed != set(PILOT_IMPLEMENTATION_RULE_FIELDS):
        raise ManifestValidationError("the six Stage-2C implementation rules are incomplete")

    invariants = document["invariants"]
    expected_invariants = {
        "no_pilot_confirmatory_overlap": True,
        "no_no_pad_main_arm": True,
        "redundancy_axis": "EVIDENCE GAP",
        "formal_k_n_audit_seed_count": "POST_PILOT_COMPUTED_THEN_USER_LOCKED",
        "governance_dead_zone": USER_APPROVAL_REQUIRED,
        "huber_delta": USER_APPROVAL_REQUIRED,
    }
    if not isinstance(invariants, Mapping) or dict(invariants) != expected_invariants:
        raise ManifestValidationError("pilot/confirmatory or protocol invariants changed")
    forbidden_no_pad_placeholder = "_".join(("PILOT", "NOPAD", "REMOVAL", "DELTA"))
    if _contains_literal(document, forbidden_no_pad_placeholder):
        raise ManifestValidationError("forbidden no-pad placeholder detected")


def validate_pilot_implementation_lock(document: Mapping[str, Any]) -> None:
    """Validate the user-delegated lock without treating computed facts as approved."""

    _require_fields(
        document,
        {
            "schema_version",
            "lock_id",
            "status",
            "approval_date",
            "base_commit",
            "approval_basis",
            "protocol_lock",
            "rules",
            "invariants",
        },
        "pilot implementation lock",
    )
    if document["status"] != "USER_APPROVED_LOCKED":
        raise ManifestValidationError("pilot implementation lock is not approved")
    if document["base_commit"] != "4280484e035191b66f77618b7729dbd465d8b828":
        raise ManifestValidationError("pilot implementation lock has the wrong base commit")
    rules = document["rules"]
    expected_rules = {
        "fixed_heldout_audit_query_set",
        "train_priority_score_contract",
        "neutral_pad_token_length_matching",
        "paired_bundle_budget_ceiling",
        "sr_slope_clustered_interval",
        "shared_control_and_deployment_reuse",
    }
    if not isinstance(rules, Mapping) or set(rules) != expected_rules:
        raise ManifestValidationError("approved implementation lock does not contain six rules")
    for name, rule in rules.items():
        if not isinstance(rule, Mapping) or not rule:
            raise ManifestValidationError(f"approved implementation rule is empty: {name}")
        if _contains_pending(rule):
            raise ManifestValidationError(f"approved implementation rule remains pending: {name}")

    pad = rules["neutral_pad_token_length_matching"]
    if "[EMPTY_MEMORY_SLOT]" not in str(pad.get("algorithm", "")):
        raise ManifestValidationError("neutral-pad lock lost the approved literal")
    budget = rules["paired_bundle_budget_ceiling"]
    if "do not start" not in str(budget.get("ceiling_behavior", "")):
        raise ManifestValidationError("budget lock no longer prevents partial bundles")
    slope = rules["sr_slope_clustered_interval"]
    if "10,000" not in str(slope.get("resampling", "")) or "Holm" not in str(
        slope.get("multiplicity", "")
    ):
        raise ManifestValidationError("G-C1 resampling or multiplicity contract changed")
    reuse = rules["shared_control_and_deployment_reuse"]
    if "K_ctrl=5" not in str(reuse.get("shared_control_rollout_count", "")):
        raise ManifestValidationError("pilot shared-control count changed")

    invariants = document["invariants"]
    if not isinstance(invariants, Mapping):
        raise ManifestValidationError("pilot implementation invariants must be an object")
    expected_invariants = {
        "pilot_confirmatory_overlap_allowed": False,
        "no_pad_main_arm_allowed": False,
        "neutral_pad_failure_downgrade": "pad-replacement contribution",
        "redundancy_axis": "EVIDENCE GAP",
        "formal_k_n_audit_seed_count": "POST_PILOT_COMPUTED_THEN_USER_LOCKED",
        "governance_dead_zone": USER_APPROVAL_REQUIRED,
        "huber_delta": USER_APPROVAL_REQUIRED,
    }
    if dict(invariants) != expected_invariants:
        raise ManifestValidationError("approved implementation invariants changed")
    forbidden_no_pad_placeholder = "_".join(("PILOT", "NOPAD", "REMOVAL", "DELTA"))
    if _contains_literal(document, forbidden_no_pad_placeholder):
        raise ManifestValidationError("forbidden no-pad placeholder detected")


def validate_runtime_target_lock(
    document: Mapping[str, Any], baseline: Mapping[str, Any]
) -> None:
    _require_fields(
        document,
        {
            "schema_version",
            "lock_id",
            "status",
            "approval_date",
            "base_commit",
            "target_alias",
            "evidence",
            "target",
            "dependency_policy",
            "container_policy",
            "preflight",
            "readiness",
        },
        "runtime target lock",
    )
    if document["status"] != "USER_APPROVED_TARGET_PENDING_PREFLIGHT":
        raise ManifestValidationError("runtime target lock has an invalid status")
    target = document["target"]
    expected = {
        "gpu_model": baseline["hardware"]["gpu_model"],
        "gpu_count": baseline["hardware"]["gpu_count"],
        "python": baseline["software"]["python"],
        "pytorch": baseline["software"]["pytorch"],
        "pytorch_cuda_available": baseline["software"]["cuda_available_in_pytorch"],
        "cuda_driver_reported": baseline["software"]["cuda_driver_reported"],
        "cudnn": baseline["software"]["cudnn"],
        "nccl": baseline["software"]["nccl"],
    }
    if not isinstance(target, Mapping) or dict(target) != expected:
        raise ManifestValidationError("runtime target diverges from confirmed R000 facts")
    dependency = document["dependency_policy"]
    if not isinstance(dependency, Mapping) or any(
        dependency.get(field) != "NOT_CAPTURED" for field in ("lock_path", "lock_sha256")
    ):
        raise ManifestValidationError("uncaptured dependency lock must not be fabricated")
    preflight = document["preflight"]
    readiness = document["readiness"]
    if (
        not isinstance(preflight, Mapping)
        or preflight.get("status") != "NOT_RUN"
        or not isinstance(readiness, Mapping)
        or readiness.get("formal_r001_r002")
        != "BLOCKED_PENDING_PREFLIGHT_AND_DEPENDENCY_LOCK"
    ):
        raise ManifestValidationError("runtime target falsely claims formal readiness")


def validate_dependency_inventory(document: Mapping[str, Any]) -> None:
    """Validate that a captured inventory contains safe names and versions only."""

    _require_fields(
        document,
        {
            "schema_version",
            "inventory_id",
            "captured_at_utc",
            "runtime_identifier",
            "capture_method",
            "scope",
            "package_count",
            "packages",
            "excluded_metadata",
            "redaction",
        },
        "dependency inventory",
    )
    if (
        document["runtime_identifier"]
        != "merit-r000-h20-py312-torch211-cu130"
        or document["capture_method"]
        != "python-importlib.metadata-name-version-only"
    ):
        raise ManifestValidationError("dependency inventory has an invalid runtime or method")
    packages = document["packages"]
    if not isinstance(packages, list) or document["package_count"] != len(packages):
        raise ManifestValidationError("dependency inventory package count is inconsistent")
    observed: set[tuple[str, str]] = set()
    for package in packages:
        if not isinstance(package, Mapping) or set(package) != {"name", "version"}:
            raise ManifestValidationError("dependency inventory entry has unsafe fields")
        name = str(package["name"])
        version = str(package["version"])
        if not PACKAGE_NAME_RE.fullmatch(name) or not PACKAGE_VERSION_RE.fullmatch(version):
            raise ManifestValidationError("dependency inventory contains unsafe metadata")
        pair = (name, version)
        if pair in observed:
            raise ManifestValidationError("dependency inventory contains a duplicate entry")
        observed.add(pair)
    redaction = document["redaction"]
    if (
        not isinstance(redaction, Mapping)
        or redaction.get("name_and_version_only") is not True
        or any(
            redaction.get(field) is not False
            for field in (
                "private_runtime_path_recorded",
                "url_recorded",
                "credential_recorded",
                "machine_identity_recorded",
            )
        )
    ):
        raise ManifestValidationError("dependency inventory redaction contract failed")


def validate_runtime_environment_lock(document: Mapping[str, Any]) -> None:
    """Validate an empirical runtime lock without claiming formal-run readiness."""

    _require_fields(
        document,
        {
            "schema_version",
            "lock_id",
            "status",
            "captured_at_utc",
            "base_commit",
            "runtime_alias",
            "sources",
            "observed",
            "dependency_inventory",
            "capture",
            "safety_boundary",
            "readiness",
        },
        "runtime environment lock",
    )
    if (
        document["status"] != "RUNTIME_ENVIRONMENT_LOCKED"
        or document["base_commit"] != "4280484e035191b66f77618b7729dbd465d8b828"
        or document["runtime_alias"]
        != "runtime://merit-r000-h20-py312-torch211-cu130"
    ):
        raise ManifestValidationError("runtime environment lock identity is invalid")
    sources = document["sources"]
    if not isinstance(sources, Mapping) or set(sources) != {"target", "r000_profile"}:
        raise ManifestValidationError("runtime environment lock sources are incomplete")
    for reference in sources.values():
        if (
            not isinstance(reference, Mapping)
            or not _is_path_alias(reference.get("path"))
            or not _is_sha256(reference.get("sha256"))
        ):
            raise ManifestValidationError("runtime environment lock source is invalid")
    inventory = document["dependency_inventory"]
    if (
        not isinstance(inventory, Mapping)
        or inventory.get("path")
        != "environments/dependency-inventory.20260719.attempt-002.json"
        or not _is_sha256(inventory.get("sha256"))
        or not isinstance(inventory.get("package_count"), int)
    ):
        raise ManifestValidationError("runtime dependency inventory reference is invalid")
    observed = document["observed"]
    expected_observed_fields = {
        "python",
        "pytorch",
        "pytorch_cuda_runtime",
        "cuda_available",
        "gpu_count",
        "gpu_models",
        "cudnn",
        "nccl",
    }
    if not isinstance(observed, Mapping) or set(observed) != expected_observed_fields:
        raise ManifestValidationError("runtime environment observations are incomplete")
    capture = document["capture"]
    if (
        not isinstance(capture, Mapping)
        or capture.get("metadata_only") is not True
        or capture.get("private_executable_reference_recorded") is not False
        or not _is_sha256(capture.get("probe_script_sha256"))
    ):
        raise ManifestValidationError("runtime environment capture boundary is invalid")
    safety = document["safety_boundary"]
    if not isinstance(safety, Mapping) or any(value != 0 for value in safety.values()):
        raise ManifestValidationError("runtime environment lock records a prohibited action")
    readiness = document["readiness"]
    if (
        not isinstance(readiness, Mapping)
        or readiness.get("metadata_runtime") != "READY"
        or readiness.get("real_toy_adapter_engineering") != "READY_ENVIRONMENT_ONLY"
        or readiness.get("formal_r001_r002")
        != "BLOCKED_PENDING_MODEL_DATA_ADAPTER_AND_RUN_MANIFEST"
    ):
        raise ManifestValidationError("runtime environment lock overstates readiness")


def validate_sanity_baseline_lock(document: Mapping[str, Any]) -> None:
    _require_fields(
        document,
        {
            "schema_version",
            "lock_id",
            "status",
            "approval_date",
            "base_commit",
            "scope",
            "implementation_mode",
            "reporting_label",
            "source_reference",
            "source_revision",
            "upstream_code_imported",
            "license_verification",
            "model_revision",
            "dataset_revision",
            "adapter_contract",
            "fidelity_claim",
            "gates",
        },
        "sanity baseline lock",
    )
    if (
        document["status"] != "USER_APPROVED_LOCKED"
        or document["implementation_mode"] != "standardized_credit_variant_wrapper"
        or document["upstream_code_imported"] is not False
        or document["fidelity_claim"] != "NO_EXACT_METHOD_FIDELITY_CLAIM"
        or "style" not in str(document["reporting_label"]).lower()
    ):
        raise ManifestValidationError("sanity wrapper makes an unsupported fidelity claim")
    gates = document["gates"]
    if not isinstance(gates, Mapping) or any(
        "BLOCKED" not in str(gates.get(field, ""))
        for field in (
            "r010_reasoningbank_exact_name",
            "r011_memrl_exact_name",
            "m2_baseline_execution",
        )
    ):
        raise ManifestValidationError("exact-name or pilot baseline gates were opened early")


def validate_model_adapter_contract(document: Mapping[str, Any]) -> None:
    _require_fields(
        document,
        {
            "schema_version",
            "contract_id",
            "status",
            "base_commit",
            "environment_lock",
            "implementation",
            "binding",
            "invariants",
            "readiness",
            "execution_boundary",
        },
        "model adapter contract",
    )
    if (
        document["contract_id"] != "model-adapter-contract-20260719-v1"
        or document["status"] != "ENGINEERING_READY_BINDING_REQUIRED"
        or document["base_commit"] != "4280484e035191b66f77618b7729dbd465d8b828"
    ):
        raise ManifestValidationError("model adapter contract identity is invalid")
    environment = document["environment_lock"]
    if (
        not isinstance(environment, Mapping)
        or environment.get("path")
        != "environments/environment-lock.20260719.attempt-002.json"
        or not _is_sha256(environment.get("sha256"))
    ):
        raise ManifestValidationError("model adapter environment reference is invalid")
    implementation = document["implementation"]
    if not isinstance(implementation, Mapping) or implementation != {
        "adapter_revision": "merit-token-model-adapter-v1",
        "entrypoint": "merit_experiment.model_adapter:TokenModelAdapter",
        "backend_entrypoint": "merit_experiment.model_adapter:TransformersCausalLMBackend",
    }:
        raise ManifestValidationError("model adapter implementation binding is invalid")
    binding = document["binding"]
    if not isinstance(binding, Mapping) or binding != {
        "model_revision": "RUN_MANIFEST_REQUIRED",
        "tokenizer_revision": "RUN_MANIFEST_REQUIRED",
        "model_loading": "EXTERNAL_EXPLICIT_INJECTION_ONLY",
        "run_binding": "BLOCKED_PENDING_ATOMIC_RUN_MANIFEST",
    }:
        raise ManifestValidationError("model adapter prematurely binds a model or tokenizer")
    invariants = document["invariants"]
    if (
        not isinstance(invariants, list)
        or any(not isinstance(item, str) for item in invariants)
        or len(set(invariants)) < 6
    ):
        raise ManifestValidationError("model adapter invariants are incomplete")
    readiness = document["readiness"]
    if not isinstance(readiness, Mapping) or readiness != {
        "model_adapter": "READY_ENGINEERING_ONLY",
        "data_adapter_and_real_toy_split": "BLOCKED",
        "atomic_run_manifest": "BLOCKED",
        "formal_r001_r002": "BLOCKED",
    }:
        raise ManifestValidationError("model adapter contract overstates readiness")
    boundary = document["execution_boundary"]
    expected_boundary = {
        "training_runs",
        "model_inference_calls",
        "benchmarks",
        "gpu_stress_tests",
        "collective_communication_tests",
        "dependencies_installed_or_downloaded",
    }
    if (
        not isinstance(boundary, Mapping)
        or set(boundary) != expected_boundary
        or any(value != 0 for value in boundary.values())
    ):
        raise ManifestValidationError("model adapter contract records a prohibited action")


def validate_runtime_preflight_result(document: Mapping[str, Any]) -> None:
    _require_fields(
        document,
        {
            "schema_version",
            "preflight_id",
            "status",
            "target",
            "evidence",
            "checks",
            "redaction",
            "prohibited_actions",
            "readiness",
        },
        "runtime preflight result",
    )
    if document["status"] not in {"BLOCKED_RUNTIME_REFERENCE_UNAVAILABLE", "PASS"}:
        raise ManifestValidationError("recorded runtime preflight status is invalid")
    target = document["target"]
    evidence = document["evidence"]
    if (
        not isinstance(target, Mapping)
        or target.get("path") != "environments/runtime-target.locked.20260719.json"
        or not _is_sha256(target.get("sha256"))
        or not isinstance(evidence, Mapping)
        or not _is_sha256(evidence.get("sha256"))
    ):
        raise ManifestValidationError("runtime preflight evidence reference is invalid")
    checks = document["checks"]
    if not isinstance(checks, list):
        raise ManifestValidationError("runtime preflight checklist is incomplete")
    statuses = {str(check.get("check_id")): check.get("status") for check in checks}
    if len(statuses) != len(checks):
        raise ManifestValidationError("runtime preflight check ids are not unique")
    if document["status"] == "BLOCKED_RUNTIME_REFERENCE_UNAVAILABLE":
        if len(checks) != 6 or statuses.get("runtime-reference-resolution") != "FAILED" or any(
            statuses.get(check_id) != "NOT_RUN"
            for check_id in (
                "python-version",
                "pytorch-version",
                "cuda-visibility",
                "gpu-inventory",
                "dependency-lock-capture",
            )
        ):
            raise ManifestValidationError("runtime preflight overstates executed checks")
    elif set(statuses) != set(RUNTIME_SUCCESS_PREFLIGHT_IDS) or any(
        status != "PASS" for status in statuses.values()
    ):
        raise ManifestValidationError("successful runtime preflight is incomplete")
    redaction = document["redaction"]
    prohibited = document["prohibited_actions"]
    readiness = document["readiness"]
    if (
        not isinstance(redaction, Mapping)
        or any(value is not False for value in redaction.values())
        or not isinstance(prohibited, Mapping)
        or any(value is not False for value in prohibited.values())
        or not isinstance(readiness, Mapping)
        or (
            document["status"] == "BLOCKED_RUNTIME_REFERENCE_UNAVAILABLE"
            and readiness.get("formal_r001_r002") != "BLOCKED"
        )
        or (
            document["status"] == "PASS"
            and readiness.get("formal_r001_r002")
            != "BLOCKED_PENDING_MODEL_DATA_ADAPTER_AND_RUN_MANIFEST"
        )
    ):
        raise ManifestValidationError("runtime preflight violates redaction or readiness boundary")
    if document["status"] == "PASS":
        for field in ("environment_lock", "dependency_inventory"):
            reference = document.get(field)
            if (
                not isinstance(reference, Mapping)
                or not _is_path_alias(reference.get("path"))
                or not _is_sha256(reference.get("sha256"))
            ):
                raise ManifestValidationError(f"runtime preflight {field} reference is invalid")
