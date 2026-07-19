from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from merit_experiment.baselines import (
    MemRLStyleMonteCarloCredit,
    ReasoningBankStyleCredit,
)
from merit_experiment.bootstrap import clustered_bca_interval
from merit_experiment.budget import BudgetCeilingBlocked, BudgetLedger, Cost
from merit_experiment.metrics import (
    ContributionEstimate,
    holm_adjusted_pvalues,
    ordinary_least_squares_slope,
    paired_cti,
    spearman_ccc,
    superstition_rate_at_k,
)
from merit_experiment.neutral_pad import (
    NeutralPadUnrepresentable,
    length_matched_marker_token_ids,
)
from merit_experiment.replay import (
    ReplayIdentity,
    aligned_rollout_seeds,
    deployment_rollout_is_reusable,
    paired_contribution,
)
from merit_experiment.sampling import (
    stable_train_audit_split,
    utility_usage_scores,
    weighted_sample_without_replacement,
)
from merit_experiment.validation import (
    ManifestValidationError,
    validate_dependency_inventory,
    validate_model_adapter_contract,
    validate_pilot_implementation_lock,
    validate_runtime_environment_lock,
    validate_runtime_preflight_result,
    validate_runtime_target_lock,
    validate_sanity_baseline_lock,
)


class SanityComponentTests(unittest.TestCase):
    def test_ccc_uses_tie_aware_spearman_direction(self) -> None:
        self.assertAlmostEqual(spearman_ccc([1.0, 2.0, 3.0], [3.0, 2.0, 1.0]), -1.0)
        self.assertAlmostEqual(spearman_ccc([1.0, 1.0, 2.0], [1.0, 1.0, 2.0]), 1.0)

    def test_sr_at_k_is_ci_decided_and_stably_tied(self) -> None:
        estimates = [
            ContributionEstimate("m-b", 10.0, -0.02, 0.02),
            ContributionEstimate("m-a", 10.0, 0.08, 0.12),
            ContributionEstimate("m-c", 9.0, -0.20, -0.10),
            ContributionEstimate("m-d", 8.0, -0.10, 0.10),
            ContributionEstimate("m-e", 7.0, 0.06, 0.08),
            ContributionEstimate("m-f", 6.0, -0.01, 0.01),
        ]
        result = superstition_rate_at_k(estimates)
        self.assertEqual(result.selected_ids, ("m-a", "m-b"))
        self.assertEqual(result.superstitious_count, 1)
        self.assertEqual(result.rate, 0.5)

    def test_cti_and_slope_have_locked_directions(self) -> None:
        self.assertAlmostEqual(
            paired_cti({"q1": 1.0, "q2": 1.0}, {"q1": 0.0, "q2": 1.0}), 0.5
        )
        self.assertAlmostEqual(
            ordinary_least_squares_slope(
                [100, 200, 300, 400, 500], [0.1, 0.2, 0.3, 0.4, 0.5]
            ),
            0.001,
        )

    def test_holm_adjustment_is_monotone(self) -> None:
        self.assertEqual(
            holm_adjusted_pvalues({"slope": 0.01, "ccc": 0.04}),
            {"slope": 0.02, "ccc": 0.04},
        )

    def test_clustered_bca_is_deterministic(self) -> None:
        clusters = [1.0, 2.0, 3.0, 4.0, 5.0]
        statistic = lambda sample: sum(sample) / len(sample)
        first = clustered_bca_interval(clusters, statistic, 0.90, 500, 42)
        second = clustered_bca_interval(clusters, statistic, 0.90, 500, 42)
        self.assertEqual(first, second)
        self.assertLess(first[0], 3.0)
        self.assertGreater(first[1], 3.0)

    def test_stable_split_is_disjoint_and_thirty_percent(self) -> None:
        split = stable_train_audit_split(
            {"alfworld": [f"q-{index}" for index in range(10)]}
        )["alfworld"]
        self.assertEqual(len(split.audit_ids), 3)
        self.assertEqual(split.audit_inclusion_probability, 0.3)
        self.assertFalse(set(split.train_ids).intersection(split.audit_ids))
        self.assertEqual(
            split,
            stable_train_audit_split(
                {"alfworld": [f"q-{index}" for index in range(10)]}
            )["alfworld"],
        )

    def test_train_priority_is_finite_and_without_replacement(self) -> None:
        scores = utility_usage_scores(
            {"m1": 0.0, "m2": 1.0, "m3": 2.0},
            {"m1": 10, "m2": 1, "m3": 5},
        )
        selected = weighted_sample_without_replacement(scores, 2, seed=7)
        self.assertEqual(len(selected), 2)
        self.assertEqual(len(set(selected)), 2)

    def test_neutral_pad_matches_exact_token_length(self) -> None:
        self.assertEqual(length_matched_marker_token_ids((11, 12, 13), 7), (11, 12, 13, 11, 12, 13, 11))
        with self.assertRaises(NeutralPadUnrepresentable):
            length_matched_marker_token_ids((11, 12, 13), 2)

    def test_budget_never_starts_partial_bundle(self) -> None:
        ledger = BudgetLedger(Cost(10.0, 100))
        ledger.reserve_bundle(Cost(6.0, 60))
        ledger.settle_bundle(Cost(5.0, 50))
        with self.assertRaises(BudgetCeilingBlocked):
            ledger.reserve_bundle(Cost(6.0, 51))
        self.assertEqual(ledger.realized, Cost(5.0, 50))

    def test_replay_pairing_and_exact_reuse(self) -> None:
        seeds = aligned_rollout_seeds(100, 5)
        self.assertEqual(seeds, (100, 101, 102, 103, 104))
        identity = ReplayIdentity(
            query_id="q-1",
            task_state_sha256="a" * 64,
            bank_snapshot_sha256="b" * 64,
            retrieval_order=("m-1", "m-2"),
            model_revision="model-revision",
            tokenizer_revision="tokenizer-revision",
            decoding_config_sha256="c" * 64,
            reward_evaluator_revision="reward-v1",
            rollout_seed=100,
        )
        self.assertTrue(deployment_rollout_is_reusable(identity, identity))
        changed = ReplayIdentity(**{**identity.__dict__, "rollout_seed": 101})
        self.assertFalse(deployment_rollout_is_reusable(identity, changed))
        self.assertAlmostEqual(paired_contribution([1.0, 0.5], [0.5, 0.0]), 0.5)

    def test_standardized_credit_wrappers_are_deterministic(self) -> None:
        reasoning = ReasoningBankStyleCredit()
        reasoning.update(["m1", "m2"], 1.0)
        reasoning.update(["m1"], 0.0)
        self.assertEqual(reasoning.utility, {"m1": 1.0, "m2": 1.0})

        memrl = MemRLStyleMonteCarloCredit()
        memrl.update(["m1"], 1.0)
        memrl.update(["m1"], -1.0)
        self.assertEqual(memrl.value["m1"], 0.0)

    def test_user_delegated_locks_validate_but_do_not_fake_runtime(self) -> None:
        baseline = json.loads(
            (EXPERIMENT_ROOT / "environments/baseline.json").read_text()
        )
        runtime = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-target.locked.20260719.json").read_text()
        )
        preflight = json.loads(
            (EXPERIMENT_ROOT / "environments/runtime-preflight.20260719.json").read_text()
        )
        inventory = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/dependency-inventory.20260719.attempt-002.json"
            ).read_text()
        )
        environment_lock = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/environment-lock.20260719.attempt-002.json"
            ).read_text()
        )
        passed_preflight = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/runtime-preflight.20260719.attempt-002.json"
            ).read_text()
        )
        implementation = json.loads(
            (EXPERIMENT_ROOT / "configs/pilot-implementation.locked.20260719.json").read_text()
        )
        wrapper = json.loads(
            (EXPERIMENT_ROOT / "configs/sanity-baseline.locked.20260719.json").read_text()
        )
        model_adapter = json.loads(
            (EXPERIMENT_ROOT / "configs/model-adapter.contract.20260719.json").read_text()
        )
        validate_runtime_target_lock(runtime, baseline)
        validate_runtime_preflight_result(preflight)
        validate_dependency_inventory(inventory)
        validate_runtime_environment_lock(environment_lock)
        validate_runtime_preflight_result(passed_preflight)
        validate_pilot_implementation_lock(implementation)
        validate_sanity_baseline_lock(wrapper)
        validate_model_adapter_contract(model_adapter)
        self.assertEqual(runtime["preflight"]["status"], "NOT_RUN")
        self.assertEqual(preflight["readiness"]["formal_r001_r002"], "BLOCKED")
        self.assertEqual(passed_preflight["status"], "PASS")
        self.assertEqual(
            passed_preflight["readiness"]["real_toy_adapter_engineering"],
            "READY_ENVIRONMENT_ONLY",
        )
        self.assertEqual(model_adapter["readiness"]["model_adapter"], "READY_ENGINEERING_ONLY")
        self.assertEqual(model_adapter["readiness"]["formal_r001_r002"], "BLOCKED")

    def test_dependency_inventory_rejects_install_source_metadata(self) -> None:
        inventory = json.loads(
            (
                EXPERIMENT_ROOT
                / "environments/dependency-inventory.20260719.attempt-002.json"
            ).read_text()
        )
        inventory["packages"][0]["version"] = "1.0" + "@file"
        with self.assertRaises(ManifestValidationError):
            validate_dependency_inventory(inventory)

    def test_exact_baseline_gate_cannot_be_opened_by_wrapper_lock(self) -> None:
        wrapper = json.loads(
            (EXPERIMENT_ROOT / "configs/sanity-baseline.locked.20260719.json").read_text()
        )
        wrapper["gates"]["r010_reasoningbank_exact_name"] = "READY"
        with self.assertRaises(ManifestValidationError):
            validate_sanity_baseline_lock(wrapper)


if __name__ == "__main__":
    unittest.main()
