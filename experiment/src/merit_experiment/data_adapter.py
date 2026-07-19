"""Read-only adapters and deterministic selection for real toy task streams."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
from zipfile import ZipFile

from .sampling import stable_train_audit_split


DATA_ADAPTER_REVISION = "merit-real-toy-data-adapter-v1"
TOY_SELECTOR_SEED = 20260719
TOY_TASKS_PER_STREAM = 10


class DataAdapterError(ValueError):
    """Raised when source data or an index violates the adapter contract."""


@dataclass(frozen=True)
class TaskReference:
    stream_id: str
    query_id: str
    source_locator: str

    def as_dict(self) -> dict[str, str]:
        return {
            "query_id": self.query_id,
            "source_locator": self.source_locator,
            "stream_id": self.stream_id,
        }


def _query_id(stream_id: str, source_identity: str) -> str:
    digest = hashlib.sha256(source_identity.encode("utf-8")).hexdigest()
    return f"{stream_id}:{digest}"


def _stable_selector_key(reference: TaskReference, seed: int) -> str:
    payload = f"{seed}\0{reference.stream_id}\0{reference.query_id}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _safe_archive_member(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not value:
        raise DataAdapterError("archive member must be a safe relative path")
    return value


class AlfworldZipAdapter:
    """Index paired official ALFWorld trajectory JSON and TextWorld games."""

    stream_id = "alfworld"

    def __init__(self, trajectory_archive: str | Path, game_archive: str | Path) -> None:
        self.trajectory_archive = Path(trajectory_archive)
        self.game_archive = Path(game_archive)

    def index(self, source_split: str = "valid_seen") -> tuple[TaskReference, ...]:
        prefix = f"json_2.1.1/{source_split}/"
        with ZipFile(self.trajectory_archive) as trajectories, ZipFile(
            self.game_archive
        ) as games:
            game_names = set(games.namelist())
            references: list[TaskReference] = []
            for member in sorted(trajectories.namelist()):
                if not member.startswith(prefix) or not member.endswith("/traj_data.json"):
                    continue
                game_member = member.removesuffix("traj_data.json") + "game.tw-pddl"
                if game_member not in game_names:
                    continue
                task_locator = member.removesuffix("/traj_data.json")
                references.append(
                    TaskReference(
                        self.stream_id,
                        _query_id(self.stream_id, task_locator),
                        _safe_archive_member(task_locator),
                    )
                )
        if len(references) < 2 or len({ref.query_id for ref in references}) != len(references):
            raise DataAdapterError("ALFWorld source needs at least two unique paired tasks")
        return tuple(references)

    def load(self, reference: TaskReference) -> dict[str, Any]:
        if reference.stream_id != self.stream_id:
            raise DataAdapterError("ALFWorld adapter received another stream")
        locator = _safe_archive_member(reference.source_locator)
        if _query_id(self.stream_id, locator) != reference.query_id:
            raise DataAdapterError("ALFWorld query ID does not match its locator")
        trajectory_member = f"{locator}/traj_data.json"
        game_member = f"{locator}/game.tw-pddl"
        with ZipFile(self.trajectory_archive) as trajectories:
            trajectory = json.loads(trajectories.read(trajectory_member))
        with ZipFile(self.game_archive) as games:
            game = games.read(game_member)
        if (
            not isinstance(trajectory, Mapping)
            or not isinstance(trajectory.get("task_id"), str)
            or not isinstance(trajectory.get("task_type"), str)
            or not game
        ):
            raise DataAdapterError("ALFWorld task is not replayable metadata plus game data")
        return {"trajectory": trajectory, "textworld_game": game}


class HotpotQATraceJsonlAdapter:
    """Index and load one-question-per-line replay traces without selecting on outcomes."""

    stream_id = "hotpotqa"

    def __init__(self, trace_path: str | Path) -> None:
        self.trace_path = Path(trace_path)

    @staticmethod
    def _question_without_trace(line: str) -> str:
        cursor = 0
        while cursor < len(line) and line[cursor].isspace():
            cursor += 1
        if cursor >= len(line) or line[cursor] != "{":
            raise DataAdapterError("HotpotQA trace line must be a JSON object")
        cursor += 1
        while cursor < len(line) and line[cursor].isspace():
            cursor += 1
        question, end = json.JSONDecoder().raw_decode(line, cursor)
        if not isinstance(question, str):
            raise DataAdapterError("HotpotQA trace object key must be a question string")
        while end < len(line) and line[end].isspace():
            end += 1
        if end >= len(line) or line[end] != ":":
            raise DataAdapterError("HotpotQA trace question must be followed by a value")
        return question

    def index(self) -> tuple[TaskReference, ...]:
        references: list[TaskReference] = []
        with self.trace_path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                question = self._question_without_trace(line)
                references.append(
                    TaskReference(
                        self.stream_id,
                        _query_id(self.stream_id, question),
                        f"line:{line_number}",
                    )
                )
        if len(references) < 2 or len({ref.query_id for ref in references}) != len(references):
            raise DataAdapterError("HotpotQA source needs at least two unique questions")
        return tuple(references)

    def load(self, reference: TaskReference) -> dict[str, Any]:
        if reference.stream_id != self.stream_id:
            raise DataAdapterError("HotpotQA adapter received another stream")
        try:
            prefix, raw_line_number = reference.source_locator.split(":", 1)
            line_number = int(raw_line_number)
        except (ValueError, TypeError) as exc:
            raise DataAdapterError("invalid HotpotQA line locator") from exc
        if prefix != "line" or line_number <= 0:
            raise DataAdapterError("invalid HotpotQA line locator")
        with self.trace_path.open(encoding="utf-8") as handle:
            for current, line in enumerate(handle, start=1):
                if current == line_number:
                    document = json.loads(line)
                    break
            else:
                raise DataAdapterError("HotpotQA line locator is out of range")
        if not isinstance(document, Mapping) or len(document) != 1:
            raise DataAdapterError("HotpotQA trace line must contain exactly one question")
        question, trace = next(iter(document.items()))
        if _query_id(self.stream_id, question) != reference.query_id:
            raise DataAdapterError("HotpotQA query ID does not match its question")
        if not isinstance(trace, list) or not trace or any(not isinstance(step, Mapping) for step in trace):
            raise DataAdapterError("HotpotQA task requires a non-empty replay trace")
        return {"question": question, "trace": trace}


def build_real_toy_split(
    references_by_stream: Mapping[str, Sequence[TaskReference]],
    tasks_per_stream: int = TOY_TASKS_PER_STREAM,
    selector_seed: int = TOY_SELECTOR_SEED,
) -> dict[str, tuple[TaskReference, ...]]:
    """Select a fixed toy universe, then apply the locked 70:30 task split."""

    if not isinstance(tasks_per_stream, int) or tasks_per_stream < 2:
        raise DataAdapterError("tasks_per_stream must be an integer of at least two")
    selected_by_stream: dict[str, tuple[TaskReference, ...]] = {}
    for stream_id in sorted(references_by_stream):
        references = tuple(references_by_stream[stream_id])
        if len(references) < tasks_per_stream or any(
            ref.stream_id != stream_id for ref in references
        ):
            raise DataAdapterError("each stream must contain enough correctly labelled tasks")
        selected_by_stream[stream_id] = tuple(
            sorted(references, key=lambda ref: (_stable_selector_key(ref, selector_seed), ref.query_id))[
                :tasks_per_stream
            ]
        )

    splits = stable_train_audit_split(
        {stream: [ref.query_id for ref in refs] for stream, refs in selected_by_stream.items()},
        selector_seed=selector_seed,
    )
    by_id = {
        ref.query_id: ref
        for references in selected_by_stream.values()
        for ref in references
    }
    train = tuple(
        sorted(
            (by_id[query_id] for stream in sorted(splits) for query_id in splits[stream].train_ids),
            key=lambda ref: (ref.stream_id, ref.query_id),
        )
    )
    audit = tuple(
        sorted(
            (by_id[query_id] for stream in sorted(splits) for query_id in splits[stream].audit_ids),
            key=lambda ref: (ref.stream_id, ref.query_id),
        )
    )
    if {ref.query_id for ref in train}.intersection(ref.query_id for ref in audit):
        raise DataAdapterError("toy TRAIN/AUDIT split overlaps")
    return {"pilot_train": train, "pilot_audit": audit}
