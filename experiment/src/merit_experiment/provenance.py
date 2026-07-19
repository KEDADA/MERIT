"""Content-addressed dirty-worktree provenance without staging or mutation."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Sequence


PROVENANCE_REVISION = "merit-dirty-worktree-inventory-v1"
GENERATED_ENVELOPE_EXCLUSIONS = (
    "experiment/runs/provenance/dirty-worktree.20260719.json",
    "experiment/runs/R001__sanity__paired-replay-real-toy__seed-pending__a001/",
    "experiment/runs/R002__sanity__metrics-real-toy__seed-pending__a001/",
)


class ProvenanceError(ValueError):
    """Raised when a worktree cannot be captured safely and deterministically."""


def _git(repo_root: Path, *arguments: str) -> bytes:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def _is_excluded(path: str, exclusions: Sequence[str]) -> bool:
    return any(path == exclusion or (exclusion.endswith("/") and path.startswith(exclusion)) for exclusion in exclusions)


def _content_identity(path: Path) -> tuple[str, int, str]:
    digest = hashlib.sha256()
    if path.is_symlink():
        payload = ("symlink:" + path.readlink().as_posix()).encode("utf-8")
        digest.update(payload)
        return digest.hexdigest(), len(payload), "symlink"
    if not path.is_file():
        raise ProvenanceError(f"dirty path is not a file or symlink: {path.name}")
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size, "file"


def dirty_entries(
    repo_root: str | Path,
    exclusions: Sequence[str] = GENERATED_ENVELOPE_EXCLUSIONS,
) -> list[dict[str, Any]]:
    root = Path(repo_root).resolve()
    raw = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    tokens = raw.decode("utf-8", errors="strict").split("\0")
    entries: list[dict[str, Any]] = []
    index = 0
    while index < len(tokens) and tokens[index]:
        record = tokens[index]
        if len(record) < 4 or record[2] != " ":
            raise ProvenanceError("unexpected git porcelain record")
        status = record[:2]
        relative = record[3:]
        if "R" in status or "C" in status:
            raise ProvenanceError("rename/copy status requires an explicit provenance revision")
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ProvenanceError("git emitted an unsafe dirty path")
        if not _is_excluded(relative, exclusions):
            digest, size, kind = _content_identity(root / relative)
            entries.append(
                {
                    "kind": kind,
                    "path": relative,
                    "sha256": digest,
                    "size_bytes": size,
                    "status": status,
                }
            )
        index += 1
    entries.sort(key=lambda entry: entry["path"])
    return entries


def capture_dirty_worktree(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    head = _git(root, "rev-parse", "HEAD").decode("ascii").strip()
    entries = dirty_entries(root)
    if not entries:
        raise ProvenanceError("expected a dirty worktree but captured no inputs")
    return {
        "schema_version": "1.0",
        "inventory_id": "dirty-worktree-20260719-v1",
        "provenance_revision": PROVENANCE_REVISION,
        "base_commit": "4280484e035191b66f77618b7729dbd465d8b828",
        "head_commit": head,
        "dirty_worktree": True,
        "content_identity": "regular-file SHA-256; symlink SHA-256 over UTF-8 'symlink:' plus relative target",
        "generated_envelope_exclusions": list(GENERATED_ENVELOPE_EXCLUSIONS),
        "entries": entries,
        "entry_count": len(entries),
    }
