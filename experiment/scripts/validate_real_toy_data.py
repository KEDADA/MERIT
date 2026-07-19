#!/usr/bin/env python3
"""Validate external real-toy sources against committed content-free indexes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.data_adapter import (
    AlfworldZipAdapter,
    HotpotQATraceJsonlAdapter,
    TaskReference,
    build_real_toy_split,
)
from merit_experiment.hashing import file_sha256
from merit_experiment.validation import validate_data_manifest


def _references(path: Path) -> tuple[TaskReference, ...]:
    document = json.loads(path.read_text(encoding="utf-8"))
    return tuple(TaskReference(**sample) for sample in document["samples"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alfworld-json", required=True, type=Path)
    parser.add_argument("--alfworld-games", required=True, type=Path)
    parser.add_argument("--hotpot-traces", required=True, type=Path)
    args = parser.parse_args()

    manifest_path = EXPERIMENT_ROOT / "data/real-toy-split.20260719.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_data_manifest(manifest)
    paths = {
        "alfworld_trajectory_archive": args.alfworld_json,
        "alfworld_game_archive": args.alfworld_games,
        "hotpotqa_trace_jsonl": args.hotpot_traces,
    }
    for source in manifest["sources"]:
        path = paths[source["source_id"]]
        if path.stat().st_size != source["size_bytes"] or file_sha256(path) != source["sha256"]:
            raise RuntimeError(f"source mismatch: {source['source_id']}")

    alfworld = AlfworldZipAdapter(args.alfworld_json, args.alfworld_games)
    hotpot = HotpotQATraceJsonlAdapter(args.hotpot_traces)
    expected = build_real_toy_split(
        {"alfworld": alfworld.index(), "hotpotqa": hotpot.index()}
    )
    for role in ("pilot_train", "pilot_audit"):
        index_path = EXPERIMENT_ROOT / f"data/indexes/real-toy-{role}.20260719.index.json"
        observed = _references(index_path)
        if observed != expected[role]:
            raise RuntimeError(f"stored {role} index is not reproducible")
        partition = next(item for item in manifest["partitions"] if item["role"] == role)
        if file_sha256(index_path) != partition["sample_index_sha256"]:
            raise RuntimeError(f"stored {role} index hash mismatch")
        for reference in observed:
            (alfworld if reference.stream_id == "alfworld" else hotpot).load(reference)

    print("REAL_TOY_DATA_VALIDATION: PASS")
    print("streams=2 tasks=20 pilot_train=14 pilot_audit=6 overlap=0")
    print("model_calls=0 gpu_calls=0 formal_runs=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
