from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.model_adapter import (
    DecodingConfig,
    GenerationRequest,
    ModelAdapterError,
    ModelIdentity,
    TokenModelAdapter,
)
from merit_experiment.neutral_pad import length_matched_marker_token_ids
from merit_experiment.validation import ManifestValidationError, validate_model_adapter_contract


class RecordingTokenizer:
    def __init__(self) -> None:
        self.add_special_tokens: list[bool] = []

    def encode(self, text: str, *, add_special_tokens: bool) -> list[int]:
        self.add_special_tokens.append(add_special_tokens)
        return [ord(character) for character in text]

    def decode(self, token_ids: object, *, skip_special_tokens: bool) -> str:
        return "".join(chr(token_id) for token_id in token_ids)  # type: ignore[arg-type]


class RecordingBackend:
    def __init__(self) -> None:
        self.calls: list[tuple[tuple[int, ...], DecodingConfig, int]] = []

    def generate_continuation(
        self,
        prompt_token_ids: tuple[int, ...],
        decoding: DecodingConfig,
        rollout_seed: int,
    ) -> tuple[int, ...]:
        self.calls.append((prompt_token_ids, decoding, rollout_seed))
        return (65 + rollout_seed % 2,)


class ModelAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tokenizer = RecordingTokenizer()
        self.backend = RecordingBackend()
        self.adapter = TokenModelAdapter(
            ModelIdentity("fixture-model-revision", "fixture-tokenizer-revision"),
            self.tokenizer,
            self.backend,
        )

    def test_construction_has_no_model_call(self) -> None:
        self.assertEqual(self.backend.calls, [])

    def test_encode_forces_no_special_tokens(self) -> None:
        self.assertEqual(self.adapter.encode("ab"), (97, 98))
        self.assertEqual(self.tokenizer.add_special_tokens, [False])

    def test_exact_neutral_pad_ids_reach_backend_without_reencoding(self) -> None:
        marker = self.adapter.encode("[EMPTY_MEMORY_SLOT]")
        prompt = (1, 2) + length_matched_marker_token_ids(marker, len(marker) + 3) + (3,)
        result = self.adapter.generate(
            GenerationRequest(prompt, DecodingConfig(2, False), rollout_seed=8)
        )
        self.assertEqual(self.backend.calls[0][0], prompt)
        self.assertEqual(self.tokenizer.add_special_tokens, [False])
        self.assertEqual(result.continuation_token_ids, (65,))
        self.assertEqual(result.input_token_count, len(prompt))
        self.assertEqual(result.output_token_count, 1)
        self.assertEqual(result.model_revision, "fixture-model-revision")
        self.assertEqual(result.tokenizer_revision, "fixture-tokenizer-revision")
        self.assertEqual(result.rollout_seed, 8)
        self.assertEqual(result.decoding_config_sha256, DecodingConfig(2, False).sha256)

    def test_sampled_decoding_requires_explicit_parameters(self) -> None:
        with self.assertRaises(ModelAdapterError):
            DecodingConfig(2, True)
        with self.assertRaises(ModelAdapterError):
            DecodingConfig(2, False, temperature=1.0)
        with self.assertRaises(ModelAdapterError):
            DecodingConfig(2, True, temperature=math.nan, top_p=0.9)

    def test_unresolved_revision_and_invalid_backend_output_are_rejected(self) -> None:
        with self.assertRaises(ModelAdapterError):
            ModelIdentity("USER_APPROVAL_REQUIRED", "fixture-tokenizer-revision")

        class TooLongBackend(RecordingBackend):
            def generate_continuation(self, prompt_token_ids, decoding, rollout_seed):
                return (1, 2, 3)

        adapter = TokenModelAdapter(
            ModelIdentity("fixture-model-revision", "fixture-tokenizer-revision"),
            self.tokenizer,
            TooLongBackend(),
        )
        with self.assertRaises(ModelAdapterError):
            adapter.generate(GenerationRequest((1,), DecodingConfig(2, False), 1))

    def test_contract_cannot_open_later_gates(self) -> None:
        contract = json.loads(
            (EXPERIMENT_ROOT / "configs/model-adapter.contract.20260719.json").read_text()
        )
        validate_model_adapter_contract(contract)
        contract["readiness"]["formal_r001_r002"] = "READY"
        with self.assertRaises(ManifestValidationError):
            validate_model_adapter_contract(contract)


if __name__ == "__main__":
    unittest.main()
