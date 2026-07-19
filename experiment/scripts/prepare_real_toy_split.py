#!/usr/bin/env python3
"""Build real-toy sample indexes from explicit read-only external sources."""

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
    build_real_toy_split,
)
from merit_experiment.hashing import canonical_json_bytes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alfworld-json", required=True, type=Path)
    parser.add_argument("--alfworld-games", required=True, type=Path)
    parser.add_argument("--hotpot-traces", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    alfworld = AlfworldZipAdapter(args.alfworld_json, args.alfworld_games)
    hotpot = HotpotQATraceJsonlAdapter(args.hotpot_traces)
    split = build_real_toy_split(
        {"alfworld": alfworld.index(), "hotpotqa": hotpot.index()}
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for role, references in split.items():
        document = {
            "schema_version": "1.0",
            "adapter_revision": "merit-real-toy-data-adapter-v1",
            "phase": "pilot",
            "role": role,
            "samples": [reference.as_dict() for reference in references],
        }
        target = args.output_dir / f"real-toy-{role}.20260719.index.json"
        with target.open("xb") as handle:
            handle.write(canonical_json_bytes(document) + b"\n")
        print(target)
    print("REAL_TOY_SPLIT_PREPARATION: PASS")
    print("model_calls=0 gpu_calls=0 formal_runs=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
