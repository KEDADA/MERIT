#!/usr/bin/env python3
"""Exclusively create a content-addressed dirty-worktree inventory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.hashing import canonical_json_bytes, file_sha256
from merit_experiment.provenance import capture_dirty_worktree


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    document = capture_dirty_worktree(REPO_ROOT)
    payload = canonical_json_bytes(document) + b"\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as handle:
        handle.write(payload)
    print("DIRTY_WORKTREE_CAPTURE: PASS")
    print(f"entries={document['entry_count']} sha256={file_sha256(args.output)}")
    print("staged=0 committed=0 pushed=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
