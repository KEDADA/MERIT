"""Model adapter contract with explicit token and generation provenance.

The module imports no model framework at import time.  A real Transformers model
and tokenizer must be injected explicitly; loading, downloading, and device
placement remain outside this adapter and outside the current engineering gate.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Protocol, Sequence

from .hashing import canonical_json_sha256


ADAPTER_REVISION = "merit-token-model-adapter-v1"
NEUTRAL_PAD_ADD_SPECIAL_TOKENS = False


class ModelAdapterError(ValueError):
    """Raised when a model request or backend response violates the contract."""


def _validate_revision(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ModelAdapterError(f"{field} must be a non-empty explicit revision")
    if value == "USER_APPROVAL_REQUIRED":
        raise ModelAdapterError(f"{field} is unresolved")


def _token_tuple(values: Sequence[int], field: str, *, allow_empty: bool) -> tuple[int, ...]:
    result = tuple(values)
    if (not allow_empty and not result) or any(
        not isinstance(token_id, int) or isinstance(token_id, bool) or token_id < 0
        for token_id in result
    ):
        qualifier = "non-empty " if not allow_empty else ""
        raise ModelAdapterError(f"{field} must be {qualifier}non-negative integer token IDs")
    return result


@dataclass(frozen=True)
class ModelIdentity:
    model_revision: str
    tokenizer_revision: str
    adapter_revision: str = ADAPTER_REVISION

    def __post_init__(self) -> None:
        _validate_revision(self.model_revision, "model_revision")
        _validate_revision(self.tokenizer_revision, "tokenizer_revision")
        if self.adapter_revision != ADAPTER_REVISION:
            raise ModelAdapterError("unsupported adapter_revision")


@dataclass(frozen=True)
class DecodingConfig:
    max_new_tokens: int
    do_sample: bool
    temperature: float | None = None
    top_p: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.do_sample, bool):
            raise ModelAdapterError("do_sample must be a boolean")
        if (
            not isinstance(self.max_new_tokens, int)
            or isinstance(self.max_new_tokens, bool)
            or self.max_new_tokens <= 0
        ):
            raise ModelAdapterError("max_new_tokens must be a positive integer")
        if self.do_sample:
            if (
                not isinstance(self.temperature, (int, float))
                or isinstance(self.temperature, bool)
                or not math.isfinite(self.temperature)
                or self.temperature <= 0.0
            ):
                raise ModelAdapterError("sampled decoding requires positive temperature")
            if (
                not isinstance(self.top_p, (int, float))
                or isinstance(self.top_p, bool)
                or not math.isfinite(self.top_p)
                or not 0.0 < self.top_p <= 1.0
            ):
                raise ModelAdapterError("sampled decoding requires 0 < top_p <= 1")
        elif self.temperature is not None or self.top_p is not None:
            raise ModelAdapterError("greedy decoding forbids sampling parameters")

    def as_dict(self) -> dict[str, int | float | bool | None]:
        return {
            "do_sample": self.do_sample,
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

    @property
    def sha256(self) -> str:
        return canonical_json_sha256(self.as_dict())


@dataclass(frozen=True)
class GenerationRequest:
    prompt_token_ids: tuple[int, ...]
    decoding: DecodingConfig
    rollout_seed: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "prompt_token_ids",
            _token_tuple(self.prompt_token_ids, "prompt_token_ids", allow_empty=False),
        )
        if not isinstance(self.rollout_seed, int) or isinstance(self.rollout_seed, bool):
            raise ModelAdapterError("rollout_seed must be an integer")


@dataclass(frozen=True)
class GenerationResult:
    continuation_token_ids: tuple[int, ...]
    text: str
    input_token_count: int
    output_token_count: int
    rollout_seed: int
    model_revision: str
    tokenizer_revision: str
    adapter_revision: str
    decoding_config_sha256: str


class TokenizerBackend(Protocol):
    def encode(self, text: str, *, add_special_tokens: bool) -> Sequence[int]: ...

    def decode(self, token_ids: Sequence[int], *, skip_special_tokens: bool) -> str: ...


class GenerationBackend(Protocol):
    def generate_continuation(
        self,
        prompt_token_ids: tuple[int, ...],
        decoding: DecodingConfig,
        rollout_seed: int,
    ) -> Sequence[int]: ...


class TokenModelAdapter:
    """Framework-neutral adapter that preserves exact token-ID interventions."""

    def __init__(
        self,
        identity: ModelIdentity,
        tokenizer: TokenizerBackend,
        backend: GenerationBackend,
    ) -> None:
        self.identity = identity
        self._tokenizer = tokenizer
        self._backend = backend

    def encode(self, text: str) -> tuple[int, ...]:
        if not isinstance(text, str):
            raise ModelAdapterError("text must be a string")
        return _token_tuple(
            self._tokenizer.encode(text, add_special_tokens=False),
            "encoded token IDs",
            allow_empty=False,
        )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        continuation = _token_tuple(
            self._backend.generate_continuation(
                request.prompt_token_ids,
                request.decoding,
                request.rollout_seed,
            ),
            "continuation_token_ids",
            allow_empty=True,
        )
        if len(continuation) > request.decoding.max_new_tokens:
            raise ModelAdapterError("backend exceeded max_new_tokens")
        text = self._tokenizer.decode(continuation, skip_special_tokens=True)
        if not isinstance(text, str):
            raise ModelAdapterError("tokenizer decode must return a string")
        return GenerationResult(
            continuation_token_ids=continuation,
            text=text,
            input_token_count=len(request.prompt_token_ids),
            output_token_count=len(continuation),
            rollout_seed=request.rollout_seed,
            model_revision=self.identity.model_revision,
            tokenizer_revision=self.identity.tokenizer_revision,
            adapter_revision=self.identity.adapter_revision,
            decoding_config_sha256=request.decoding.sha256,
        )


class TransformersCausalLMBackend:
    """Thin backend for already-loaded PyTorch/Transformers components.

    Constructing this object performs no model call.  ``generate_continuation`` is
    the only inference boundary and is intentionally not exercised by preflight or
    skeleton validation.
    """

    def __init__(self, model: Any, torch_module: Any) -> None:
        self._model = model
        self._torch = torch_module

    def generate_continuation(
        self,
        prompt_token_ids: tuple[int, ...],
        decoding: DecodingConfig,
        rollout_seed: int,
    ) -> Sequence[int]:
        device = next(self._model.parameters()).device
        input_ids = self._torch.tensor([prompt_token_ids], dtype=self._torch.long, device=device)
        attention_mask = self._torch.ones_like(input_ids)
        generator = self._torch.Generator(device=device).manual_seed(rollout_seed)
        kwargs: dict[str, Any] = {
            "attention_mask": attention_mask,
            "do_sample": decoding.do_sample,
            "generator": generator,
            "input_ids": input_ids,
            "max_new_tokens": decoding.max_new_tokens,
        }
        if decoding.do_sample:
            kwargs.update(temperature=decoding.temperature, top_p=decoding.top_p)
        output = self._model.generate(**kwargs)
        full_ids = tuple(int(token_id) for token_id in output[0].tolist())
        if full_ids[: len(prompt_token_ids)] != prompt_token_ids:
            raise ModelAdapterError("backend output does not preserve the prompt prefix")
        return full_ids[len(prompt_token_ids) :]
