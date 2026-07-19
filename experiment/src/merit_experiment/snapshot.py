"""Immutable, canonical configuration snapshots."""

from __future__ import annotations

import json
from pathlib import Path

from .hashing import canonical_json_bytes, canonical_json_sha256


def snapshot_config(source: str | Path, destination: str | Path) -> str:
    """Write a canonical snapshot and return its SHA-256.

    Existing identical snapshots are accepted. Existing different content is never
    overwritten, preserving the run-to-config audit trail.
    """

    source_path = Path(source)
    destination_path = Path(destination)
    value = json.loads(source_path.read_text(encoding="utf-8"))
    payload = canonical_json_bytes(value) + b"\n"
    digest = canonical_json_sha256(value)

    if destination_path.exists():
        if destination_path.read_bytes() != payload:
            raise FileExistsError(f"refusing to overwrite different snapshot: {destination_path}")
        return digest

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_bytes(payload)
    return digest

