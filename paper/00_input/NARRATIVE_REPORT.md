# Narrative Report: MERIT — Retrieval Is Not Contribution

- **Document status:** `PRELIMINARY NARRATIVE WITH PLACEHOLDERS`
- **Evidence status:** experiments have **not** been executed or verified. Every quantitative result in this document is a planned/expected quantity encoded as a unique `[[TBD:...]]` placeholder, not a measured value.
- **Target format:** AAAI 2027 anonymous preliminary draft.
- **Authoritative source snapshot:** `paper/00_input/source_proposal.md` (SHA-256 `E700D46BDD1B4F83A2D45466EDBDB2112D2FAB3EFDCC912A7AED2F5BDFC496CC`, integrity `MATCH`).
- **Venue override:** This writing task uses **AAAI 2027**. The source proposal's recorded venue strategy (primary NeurIPS 2027 / ICML 2027, fallback AAAI-28) is retained only as source background and must **not** override the current AAAI 2027 targeting.

> Scope note: This is a structured English narrative report to be consumed downstream by ARIS `/paper-plan`. It is **not** the formal paper body. Section-locator titles may keep the source proposal's bilingual headings. No LaTeX, figures, bibliography, or experiment code are produced here.

---

## Core Story

Self-evolving LLM agents improve over time by distilling interaction trajectories into a persistent memory bank, and the quality of that self-improvement loop depends heavily on **how credit is assigned to individual memories**. The source proposal characterizes the credit signals in systems such as ReasoningBank, SkeMex, and MemRL as *correlational*; that characterization requires bibliographic verification. When a task succeeds and a memory was retrieved, the relevant family of signals increments that memory's utility. This report argues that **retrieval is not contribution** — retrieval ≠ use ≠ genuine causal help — and advances the hypothesis that such credit can behave like the reinforcement schedule in Skinner's pigeon experiments: memories that merely *co-occur* with success may be persistently strengthened, producing *superstitious memories* (cargo-cult memories) with zero or negative causal effect.

We propose **MERIT**, a method that replaces correlational bookkeeping with counterfactual credit while keeping it affordable in an online, non-stationary, closed-loop setting. MERIT adds three tightly coupled components on top of the standard retrieve–execute–write loop: (1) **Randomized Interventional Trials (RIT)**, a small-budget paired leave-one-out (LOO) protocol that produces causal labels; (2) **Amortized Counterfactual Attribution (ACA)**, an O(1)-per-event attributor trained on those labels and periodically recalibrated to track closed-loop distribution drift; and (3) two deliberately simple **consumers** of the resulting credit — threshold-based **credit governance** (evict / merge / quarantine) and **scope-gated retrieval** that learns *where* each memory applies. The dependency chain is strictly linear: `RIT → ACA → consumers`.

The intended contribution is that **causal credit — not better heuristics — is the missing primitive of self-evolution**. The narrative's sharpest opening is a diagnostic phenomenon (superstitious memories accumulate over deployment time), but the paper's weight is the mechanism that makes counterfactual signals affordable and directly consumable, plus a demonstration that *swapping the signal alone* repairs the phenomenon. All headline numbers below are unmeasured and are represented as placeholders pending real experiments.

---

## Problem and Key Observation

- **Setting.** LLM agents are moving from stateless to experience-driven self-evolution: systems distill trajectories into persistent memory and use learned or heuristic signals to manage memory lifecycle (write / merge / evict / retrieve). The implicit premise of the whole paradigm is that the system knows *which memory deserves credit*.
- **Two named failure modes.**
  1. **Superstitious Memory** — memories that only co-occur with success, contribute nothing causally, yet are persistently reinforced and occupy retrieval slots.
  2. **Cross-Task Interference (CTI)** — a memory genuinely useful on task family A is indiscriminately retrieved into task family B and causes harm ("the prescription is right, the patient is wrong").
- **Key observation (the hook).** *Retrieval is not contribution.* A memory's value is defined only counterfactually — by how much outcomes degrade when it is removed. Based on the source proposal and pending bibliographic verification, the systems considered here do not directly measure this quantity, because per-memory intervention appears unaffordable. The planned hypothesis is that correlational credit does not self-correct and that the superstition fraction **grows** with deployment length (see the planned pilot in the Experiments section).
- **Why the source proposal argues prior work does not solve it.** Subject to bibliographic verification, the proposal characterizes ReasoningBank's success-trajectory distillation, SkeMex's environment-feedback utility, and MemRL's Monte-Carlo updates as observational, co-occurrence-based credit. It hypothesizes that retrieval probability correlates with query difficulty ("easy-question free-riding") and that high utility feeds back into higher retrieval probability (a Matthew effect), producing a Skinner-box reinforcement loop. This mechanism is stated as an informal, not-yet-proven Proposition 1 below.

---

## Contribution Type and Narrative Prototype

- **Contribution type:** primary **T1 (new method)** + auxiliary **T2 (new insight)**.
  - Primary T1: MERIT replaces the correlational credit signal in self-evolving memory with randomized interventional trials + amortized counterfactual attribution.
  - Auxiliary T2: reveal and quantify the *superstitious memories* phenomenon.
  - Why T2 is not primary: "correlation ≠ causation" is common knowledge in causal inference; the paper's substance is the complete mechanism that makes counterfactual signals affordable and consumable in a closed-loop system, and the demonstration that swapping the signal repairs the phenomenon.
- **Narrative prototype:** **Type A (repair / fix)**, single prototype throughout. Skeleton: self-evolving memory degrades over deployment → root cause is that the credit signal is correlational (retrieval ≠ use ≠ contribution) → upgrade credit from an "observational study" to a "randomized controlled trial," amortized to O(1) online estimation.
- **Resource-allocation constraint carried from source (executor must honor):** Method + ablation are the main battleground (~45% of the body combined); the Pilot is held to ~1–1.5 pages; only one theoretical result (Proposition 1) is kept, with its proof deferred to an appendix. No second story: cross-task interference and RL-reward replacement are narrated strictly as *two consumers of the causal credit signal*, not as separate contributions.
- **Subtraction decisions retained from source (must not be reversed):**
  - Using φ̂ to train a GRPO/RL memory-management policy is **downgraded**; only threshold rules consume φ̂ in the main method. The RL variant survives only as the reward-swap plugin study.
  - Full Shapley sampling over inter-memory interactions is **downgraded** to a boundary discussion (H5) plus an appendix variant.

---

## Claims and Evidence Status

Four core contributions `C1`–`C4` are retained and numbered. `Status` is one of `SUPPORTED-BY-DESIGN`, `PLANNED-EVIDENCE`, or `HYPOTHESIS`. No design rationale is written as experimental confirmation; no expected mechanism is written as an observed fact.

### C1 — Reveal and quantify superstitious memories (T2)
- **Statement:** Correlational credit (co-occurrence between retrieval and success) systematically breeds *superstitious memories* — zero/negative-contribution memories among the top-utility set — whose fraction increases with deployment time; and the RIT audit protocol plus two named statistics (CCC, SR@k) can measure this with interventional evidence.
- **Status:** `PLANNED-EVIDENCE` (the phenomenon requires the not-yet-run pilot to be demonstrated).
- **Required evidence:** Pilot/diagnostic study on ReasoningBank- and MemRL-style banks over replayable streams; CCC and SR@k curves vs. deployment length; the two alternative-explanation controls (split-half reliability of φ̂; removal of the φ>0 subset).
- **Planned paper location:** Pilot / Diagnostic Study section; Fig. 2; Proposition 1.
- **Source anchor:** `source_proposal.md` §3 P6 (C1), §4 (Pilot), §3.5 (Fig.2), §5 (Prop.1).

### C2 — Amortized counterfactual attribution (ACA), the method core (T1)
- **Statement:** ACA amortizes RIT labels into an O(1)-per-retrieval-event attributor with periodic recalibration; planned experiments will test whether it makes counterfactual credit practically affordable and recovers causal credit substantially better than the correlational baseline.
- **Status:** `PLANNED-EVIDENCE`.
- **Design note:** O(1) online scoring and amortization are architectural properties supported by the design; attribution accuracy and practical cost still require planned evidence.
- **Required evidence:** Held-out CCC of ACA vs. baseline; calibration (reliability diagram, ECE); split-half re-test; recalibration ablation (A1) and usage-behavior-feature ablation (A5).
- **Planned paper location:** Method §6.2; Mechanism and Calibration Analysis; Fig. 5a.
- **Source anchor:** `source_proposal.md` §3 P6 (C2), §6.2, §8.5, §3.5 (Fig.5).

### C3 — Causal credit is directly consumable (T1)
- **Statement:** Planned experiments will test whether two minimal consumers — threshold governance and per-memory scope-gated retrieval — respectively flatten superstition accumulation and reduce cross-task interference, and whether the same causal signal transfers as a per-operation reward that improves an RL-style manager (Memory-R1 / Mem-α).
- **Status:** `PLANNED-EVIDENCE`.
- **Required evidence:** Governance ablation (A2: swap causal credit back to co-occurrence utility and test whether the gain vanishes), scope-gating ablation (A3), governance ablation (A4); CTI measurement; reward-swap plugin table.
- **Planned paper location:** Method §6.3; Ablation Study; Reward-Swap Plugin Study; main table / CTI analysis.
- **Source anchor:** `source_proposal.md` §3 P6 (C3), §6.3, §8.4, §8.3 (Table 2).

### C4 — Systematic empirical evaluation (empirical)
- **Statement:** Across four benchmark categories, three backbones, and three seeds, planned experiments will test whether MERIT improves average performance over the strongest baseline at low token overhead and whether the mechanism statistics (CCC, SR@k) recover in closed loop.
- **Status:** `PLANNED-EVIDENCE`.
- **Required evidence:** Full main results table, ablations, efficiency Pareto study, scaling/transfer study — all pending execution.
- **Planned paper location:** entire Experiments section.
- **Source anchor:** `source_proposal.md` §3 P6 (C4), §8.

> Additional theoretical commitment (not a numbered contribution): **Proposition 1** is a `HYPOTHESIS` / analytical commitment pending a formal statement and proof in the appendix. It is retained exactly as scoped in the source; no new theorems or proof conclusions are introduced, and it must not be described as proven until the proof is completed and checked.

---

## Problem Formulation and Theoretical Commitments

**Symbols (8, all used in the method).** Task stream `{(q_t, r_t)}` with query/task `q_t` and outcome signal `r_t ∈ [0,1]`; memory bank `M_t = {m_i}`; retrieval operator `R(q_t) ⊆ M_t` (top-k); agent policy `π(y | q, R(q))`; attributor `g_θ`; per-memory running credit `φ̄_i`; scope representation `S_i`.

**Definition 1 (counterfactual contribution).** `φ_i(q) ≜ E[r | q, R(q)] − E[r | q, R(q)∖{m_i}]`, expectation over policy and environment randomness. Generalization: `φ` is the single-point interventional effect on the retrieved set; the full inter-memory value is a Shapley value, and single-point LOO is its first-order approximation (approximation quality characterized in the H5 boundary study).

**Definition 2 (co-occurrence utility, the baseline signal).** `Û(m_i) = Σ_t 1[m_i ∈ R(q_t)]·r_t / Σ_t 1[m_i ∈ R(q_t)]`.

**Proposition 1 (informal; formal statement and proof in appendix).** If retrieval events are correlated with the baseline solvability of the query (`Cov ≠ 0`), then `Û` is an asymptotically biased estimator of `φ`; and under the positive feedback where utility participates in retrieval ranking, a stable *superstition equilibrium* exists (`Û` high while `φ = 0`). Real-world correspondence: semantic retrieval naturally satisfies the correlation condition. **No extension of this result beyond the source is made here.**

**Assumptions (numbered for rebuttal).**
- **A1 (observable outcome):** each task has a usable `r_t` (environment success signal or consistency-checked LLM-judge score).
- **A2 (local replayability):** a task subset can be replayed from a fixed initial state (docker snapshots / text environments satisfy this natively); **only RIT label collection requires A2**, ACA online scoring does not.
- **A3 (low-order interaction):** interaction effects within a retrieved set are bounded, so LOO's error against Shapley is controllable; A3-violating cases (redundant memory pairs) are actively surfaced in the H5 boundary study with a group-intervention fallback.

**Optimization objects.** Learn `g_θ` minimizing regression loss on RIT labels `E[(g_θ(x_i(q)) − φ̂_i(q))²]`; the system objective maximizes streaming cumulative success `Σ r_t` subject to a token-budget constraint (retrieval + RIT sampling ≤ baseline × (1 + ε), with `ε = [[TBD:RIT_BUDGET_EPSILON_PERCENT]]` as a `provisional hyperparameter`).

---

## Proposed Method: MERIT

**Overview (Fig. 3).** MERIT adds three things to the standard retrieve–execute–write loop: (C1) low-budget RIT sampling continuously produces causal labels; (C2) ACA amortizes those labels into an O(1) per-event contribution score and periodically recalibrates to adapt to closed-loop distribution drift; (C3) the score is used by two minimal consumers — threshold governance updates memory retention, and scope-gated retrieval corrects retrieval ranking. Modules form a strict upstream→downstream dependency `RIT → ACA → consumers`, with **no parallel tricks** and **no unrelated module stacking**.

### Randomized Interventional Trials (RIT) → C1
- **Why:** Proposition 1 hypothesizes that co-occurrence utility is biased; the proposal further hypothesizes that the naive alternative "let the LLM self-judge whether a memory helped" can reproduce a self-confirmation trap, so it is retained as ablation variant `A-judge`.
- **How (planned configuration):** sample tasks into the trial group with probability `p = [[TBD:RIT_SAMPLING_PROB_PERCENT]]` (`provisional hyperparameter`; source-proposal planned default 5%); for each memory in the retrieved set do a paired LOO with `K = 5` fixed-seed rollouts (`planned configuration`); to control position confounding, keep the remaining context order and insert a filler placeholder when a memory is removed; emit `(q, m_i, trajectory, φ̂_i)` quadruples into the label pool. Sampling runs only on A2-satisfying tasks.
- **Link:** C1; the audit protocol is independently usable as a community tool for diagnosing deployed memory banks.

### Amortized Counterfactual Attribution (ACA) → C2 (core of the approach)
- **Why:** full RIT cost is an unmeasured `[[TBD:FULL_RIT_COST_MULTIPLIER]]`; amortization compresses causal credit to O(1). ACA learns "what kind of memory, on what kind of query, used in what way, produces genuine contribution" — the *usage-behavior* feature group is key: it distinguishes "retrieved but ignored" from "actually executed."
- **How (planned configuration):** input features `x_i(q)` in three groups — query representation, memory representation (`Qwen3-Embedding-4B`, frozen), and **usage-behavior features** (n-gram / edit overlap between memory content and output, explicit model citation markers, context position and retrieval rank, log-likelihood gain on memory tokens); head is a 2-layer MLP regressing `φ̂ ∈ [−1, 1]`. Training: Huber loss on the label pool (`δ = 0.1`, `provisional hyperparameter`); **periodic recalibration** every 100 tasks (`planned configuration`) fine-tunes on the newest labels plus isotonic-regression calibration (closed-loop retrieval distribution is changed by C3, so recalibration prevents attributor drift). Online inference: score each of the top-k memories per retrieval event, update running credit `φ̄_i` (EMA) and the positive/negative query sample sets.
- **Link:** C2 / H2; calibration quality recovered in Fig. 5a and the reliability analysis.

### Credit Governance → C3
- **Why:** an unconsumed signal is only an audit; governance is intended to flatten superstition accumulation (SR). Threshold **rules rather than RL** are used deliberately so that ablation A2 can test whether the gain comes from the *signal* (same rules with co-occurrence utility; measure whether the gain vanishes).
- **How (three rules; planned configuration / provisional thresholds):**
  - **Evict:** `φ̄_i < −0.02` and sample count `n_i ≥ 8`.
  - **Merge:** embedding similarity `> 0.9` and both `φ̄ > 0` → LLM-summary merge (credit combined by weighting).
  - **Quarantine:** new memories enter quarantine; first `n_min = 3` retrievals carry a UCB-style exploration bonus (`c = 0.5`) to avoid cold-start death, and do not contribute a ranking bonus.
  - All thresholds are `provisional hyperparameter`s; the ±0.02 dead-zone is a deliberate design choice tied to the calibration analysis (sign judgment is least stable near φ ≈ 0).

### Scope-Gated Retrieval → C3
- **Why:** solves the "prescription right, patient wrong" cross-task interference by learning *where* each memory applies.
- **How (planned configuration):** each memory maintains positive/negative query prototypes (mean embedding of queries with `φ̂ > τ⁺` / `φ̂ < τ⁻`); retrieval score `= α·(semantic relevance) + β·(sim(q, proto⁺) − sim(q, proto⁻)) + γ·φ̄_i`, with default `(α, β, γ) = (1.0, 0.5, 0.3)` as `provisional hyperparameter`s (sensitivity in the boundary/scaling analysis).
- **Link:** C3 / H1 / H3; plugin behavior (φ̂ as a per-operation reward replacing Memory-R1's outcome reward, GRPO setup unchanged) reported separately in the reward-swap study.

### Cost and Complexity Commitments
- **Dependency check:** `RIT → ACA → consumers` is a verified linear chain; subtracted modules are recorded in the subtraction decisions above.
- **Overhead (one sentence in body, full table in appendix; all values planned/unmeasured):** ACA scoring `[[TBD:ACA_SCORING_LATENCY_MS]]` per event (4B encoder batched); RIT sampling amortized over the stream `[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]` token; gating and governance add zero extra LLM calls; total `[[TBD:TOKEN_OVERHEAD_PERCENT]]` token and `[[TBD:ACA_VRAM_OVERHEAD_GB]]` VRAM (attributor resident).
- **Design-choice table (appendix D, example rows):** `LOO not full Shapley | sampled Shapley | cost lower vs 1×, error bounded under A3 | ablation A7`; `usage-behavior features | (q,m) semantic features only | distinguish "retrieved-not-used" | ablation A5`; `isotonic recalibration | no calibration | closed-loop drift | sensitivity S3`. Any row with two empty columns → delete the design.

**Algorithm 1 (main loop, retained verbatim in structure from source):**
```
Input: stream {q_t}, bank M, retriever R, policy π, attributor g_θ, budget p
for t = 1,2,...:
    C ← R(q_t)   # scope-gated: α·rel + β·scope + γ·credit, quarantine exploration bonus
    y_t, traj ← π(q_t, C);  r_t ← env/judge(y_t)
    for m_i in C:  φ̂_i ← g_θ(x_i(q_t, traj));  update φ̄_i, proto±_i
    if replayable(q_t) and rand() < p:            # RIT sampling
        for m_i in C: label ← paired_LOO(q_t, C, m_i, K=5); pool.add(label)
    governance(M): evict / merge / quarantine by rules(φ̄, n)
    if t % 100 == 0: recalibrate g_θ on pool (Huber + isotonic)
```

---

## Hypotheses-to-Experiments Mapping

> Note: The source enumerates "H1–H5" in its §7 mapping table but spells out each only partially across §6.3 / §8.5 / figure captions. The statements below are reconstructed from those anchors; where the source does not spell out a hypothesis label explicitly it is marked. **CTI definition (from source §7):** `CTI = Acc_B(B-only bank) − Acc_B(A∪B mixed bank)`, `≥ 0` indicates interference; A/B domain pairs are built along the Evo-Memory mixed-stream protocol.

| Hyp. | Statement (reconstructed) | Primary metric | Experiment locus | Related claim | Status |
|------|---------------------------|----------------|------------------|---------------|--------|
| H1 | Threshold governance flattens superstition accumulation over the stream | SR@20% curve slope | Ablation A4 / Mechanism analysis | C3 | `HYPOTHESIS` (label inferred; source anchor §6.3/§8.5) |
| H2 | ACA recovers causal credit at O(1) cost | Held-out CCC (Spearman) | Mechanism & Calibration, Fig. 5a | C2 | `HYPOTHESIS` (source gate: CCC ρ ≥ 0.6) |
| H3 | Scope gating removes cross-task interference and transfers zero-shot | CTI; transfer CCC | Ablation A3 / Scaling & transfer | C3 | `HYPOTHESIS` |
| H4 | RIT budget saturates at small p; MERIT is Pareto-efficient | AVG vs. token cost; p-sweep | Efficiency Study | C4 | `HYPOTHESIS` (source: p=5% saturates) |
| H5 | Gain has boundaries: vanishes for small banks, single-domain short streams, high redundancy | gain vs. bank size / heterogeneity / redundancy | Boundary & Scaling; Case Study | C4 (+ scope note) | `HYPOTHESIS` |

---

## Experiments

> All numeric result cells are unmeasured placeholders. Pilot, main, ablation, and efficiency experiments are described in future/planned wording throughout.

### Setup
- **Backbones (planned configuration):** `Qwen3-32B` (primary); `Qwen3-235B-A22B` (scale-trend point); `GPT-5.1` (closed-source generalization point, main-table extra row only).
- **ACA model:** `Qwen3-Embedding-4B` frozen encoder + 2-layer MLP, trainable parameters `[[TBD:ACA_TRAINABLE_PARAMS]]` (unmeasured; to be verified from the implementation).
- **Codebase:** `EvolveLab` unified memory-system implementation for baseline fairness.
- **Benchmarks (4 categories):** Evo-Memory streaming task streams (dialogue + agentic), `WebArena-Lite`, `LongMemEval`, `LoCoMo`. Pilot uses replayable `ALFWorld` (embodied text) and `HotpotQA` (multi-hop retrieval).
- **Fairness (planned):** same backbone, same retriever (`bge-m3` or `Qwen3-Embedding`, unified), same `top-k = 4`, same token budget (baselines given equal budget for their own mechanism or idle-burn; both accountings reported); seeds `{13, 42, 2026}`, report mean±std; paired bootstrap significance (10⁴ resamples, report p-values); streaming curves report per-point confidence bands.
- **Judge-bias control:** some HotpotQA/LoCoMo subtasks use LLM-as-judge (`GPT-5.1`, cross-source from the Qwen3 backbone); 200 examples human-checked, target Cohen's κ `[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]` (source target ≥ 0.8).
- **Hardware (planned):** 8×A100-80G; single main run (1 backbone × 1 benchmark × 3 seeds) `[[TBD:MAIN_GPU_HOURS_PER_RUN]]`; API cost table in appendix.

### Pilot / Diagnostic Study — "Why Does Memory Credit Go Wrong?"
- **Systems:** reproduce ReasoningBank (heuristic credit) and MemRL (MC-learned credit) on the unified codebase; backbone Qwen3-32B (execution temp 0.7, greedy evaluation).
- **Streams:** two replayable streams (ALFWorld, HotpotQA), 500 tasks each, 3 seeds. Replayable environments are required because interventions must re-run paired rollouts from the identical initial state.
- **Intervention protocol (RIT's first appearance):** freeze memory-bank snapshots at `t ∈ {100, 200, 300, 400, 500}`; for each retrieval event in the following 50 tasks, sample 300 `(query, retrieved-set)` pairs; for each memory do paired LOO (full context vs. removed), `K = 5` fixed-seed rollouts each; `φ̂_i(q) = success-rate difference`. (Counts 300 / K=5 / snapshot points are `planned configuration`.)
- **Budget note (anti-"fabricated pilot"):** total `[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]` rollouts per snapshot point and `[[TBD:PILOT_TOTAL_TOKEN_COST]]` total token cost; both are unmeasured and will be reported in an appendix cost table.
- **Named statistics (2):**
  - **CCC (Credit–Contribution Correlation):** Spearman between system credit and RIT true φ. Planned/expected: ReasoningBank `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`, MemRL `[[TBD:PILOT_CCC_MEMRL_T500]]`.
  - **SR@k (Superstition Rate):** fraction of top-k% utility memories with `φ ≤ 0`. Planned test: determine whether SR@20% rises from `[[TBD:PILOT_SR20_T100]]` at t=100 to `[[TBD:PILOT_SR20_T500]]` at t=500, as hypothesized by the superstition-accumulation account.
- **Alternative-explanation controls:**
  - Control 1 ("φ measurement is too noisy"): split-half re-test of φ̂ gives reliability `[[TBD:PILOT_SPLITHALF_PHI_RELIABILITY]]` — measurement is reliable, low CCC is not a noise artifact.
  - Control 2 ("memory is useless overall, attribution is moot"): measure the success change `[[TBD:PILOT_UTILITY_SUBSET_REMOVAL_DROP]]` after removing the entire `φ > 0` subset; a sufficiently large drop would support the interpretation that memory has value while its credit assignment is defective.
- **Gate (from source, retained honestly):** if CCC > 0.5 or SR does not rise with time, the attribution hypothesis is falsified → revise the idea card (narrow the claim to heterogeneous streams), do not force-write.

### Main Results Plan
- Structure: rows = methods ordered by lineage (Vanilla → structured heuristic credit → learned credit → orthogonal → upper bound), MERIT second-to-last, RIT-Full upper bound last (grey); columns = 5 Evo-Memory streams ordered by increasing heterogeneity (single-domain ALFWorld → mixed) → WebArena-Lite → LongMemEval → LoCoMo → AVG.
- Planned narrative (to be verified against real numbers): (i) gain grows monotonically with stream heterogeneity (single-domain `[[TBD:MAIN_GAIN_SINGLE_DOMAIN]]` → mixed `[[TBD:MAIN_GAIN_MIXED_STREAM]]`); (ii) learned-credit baselines are not reliably better than heuristic ones (wrong signal learned); (iii) MERIT reaches `[[TBD:MERIT_FRACTION_OF_RITFULL_GAIN]]` of the RIT-Full upper-bound gain at a fraction of its cost.
- The full skeleton is in Planned Tables → Table 1.

### Reward-Swap Plugin Study
- Replace Memory-R1 / Mem-α's original reward with φ̂, GRPO setup unchanged; expected lifts `[[TBD:REWARD_SWAP_MEMORY_R1_GAIN]]` and `[[TBD:REWARD_SWAP_MEMALPHA_GAIN]]` respectively — evidence that MERIT fixes the *signal*, not the pipeline (directly answers the "increment over MemRL/Memory-R1 too small" attack). Skeleton in Table 2.

### Ablation Study
- Per-contribution removal + alternative-signal controls: A1 (no recalibration / static attributor), A2 (swap causal credit → co-occurrence utility), A3 (no scope gating), A4 (no governance), A5 (no usage-behavior features), A-judge (LLM self-judge instead of RIT), A7 (LOO → group/sampled-Shapley intervention). Skeleton in Table 3.

### Mechanism and Calibration Analysis (closed-loop recovery)
- **Mechanism recovery (H2):** Fig. 5 reuses Fig. 2's statistics and axis ranges — (a) compare baseline CCC `[[TBD:PILOT_CCC_REASONINGBANK_T500]]` with ACA `[[TBD:ACA_HELDOUT_CCC_T500]]`; (b) test whether the baseline reaches SR@20% `[[TBD:PILOT_SR20_T500]]` while MERIT remains at `[[TBD:SR_MERIT_T500]]`, a difference of `[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]`.
- **Calibration (answers the top risk "attribution noise"):** held-out RIT reliability diagram + ECE `[[TBD:ECE_ACA_HELDOUT]]`; per-domain calibration; split-half re-test; test the hypothesized failure mode that the sign is least stable near φ ≈ 0 (connected to the ±0.02 governance dead-zone).
- **Sensitivity:** `K ∈ {1,3,5,10}`, RIT budget `p ∈ {1,2,5,10}%`, `(α,β,γ)` grid, `top-k ∈ {2,4,8}` — test the H4 hypothesis that performance saturates near the source-proposal default p=5%.

### Boundary and Scaling Analysis
- **Scaling/transfer:** backbone 32B → 235B, gain expected to hold (`[[TBD:SCALING_GAIN_32B]]` → `[[TBD:SCALING_GAIN_235B]]`, baselines stronger but superstition mechanism unchanged); ACA trained on ALFWorld+HotpotQA, zero-shot transfer to WebArena CCC `[[TBD:ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA]]` (H3).
- **Boundary characterization (H5):** three planned trend lines — gain vs. bank size (the `< 100`-entry analysis bin has unmeasured gain `[[TBD:H5_GAIN_SMALL_BANK_LT100]]`), vs. stream heterogeneity (single-domain gain `[[TBD:H5_GAIN_SINGLE_DOMAIN]]`), and vs. injected-redundancy ratio. The hypotheses are that LOO underestimation grows with redundancy and that the A7 variant mitigates it; the explanations will be assessed against the measured trends.

### Case Study
- Success example: a HotpotQA memory ("search entity aliases before relations") vs. a superstitious memory ("re-issue the same query once when retrieval returns empty") — planned to test whether the latter's inflated utility accumulation is assigned near-zero RIT credit and leads to eviction at task `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]`, while the former's credit and scope (multi-hop queries only) are characterized correctly.
- Failure example: two complementary memories each holding half a procedure — planned to test whether individual LOO is near zero for both and governance nearly removes both; the group-intervention fallback (cluster by similarity, intervene as a group) will test whether their joint credit can be recovered, honestly displaying the A3 boundary (Fig. 6).
- Residual-failure analysis: `[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]` of MERIT's remaining failures are expected to stem from the bank simply lacking relevant experience (no credit can help without material).

### Efficiency Study
- Pareto plot: x = relative token cost (log axis), y = AVG success; points: co-occurrence baseline (`1×`), MERIT (`[[TBD:MERIT_RELATIVE_TOKEN_COST]]`), A1 (`[[TBD:A1_RELATIVE_TOKEN_COST]]`), RIT-Full (`[[TBD:RITFULL_RELATIVE_TOKEN_COST]]`). Test whether MERIT sits at the Pareto-frontier knee. A label-budget vs. performance curve (p-sweep) is attached. Skeleton in Table 6.

---

## Planned Tables

All unknown experimental cells use unique `[[TBD:...]]` placeholders. Headers, method rows, metric columns, and caption intent are complete.

### Table 1 — Main benchmark comparison
Caption intent, conditional on eventual evidence: test whether MERIT outperforms the strongest baseline on average, whether the gain widens as stream heterogeneity increases, and whether learned-credit baselines are reliably better than heuristic ones. Stream columns S1→S5 increase in heterogeneity (S1 = single-domain ALFWorld, S5 = mixed); **S2–S4 domain identities are `NOT SPECIFIED IN SOURCE`.**

| Method (lineage) | S1 (ALFWorld) | S2 | S3 | S4 | S5 (mixed) | WebArena-Lite | LongMemEval | LoCoMo | AVG |
|---|---|---|---|---|---|---|---|---|---|
| No-Memory ReAct | [[TBD:MAIN_NOMEM_S1]] | [[TBD:MAIN_NOMEM_S2]] | [[TBD:MAIN_NOMEM_S3]] | [[TBD:MAIN_NOMEM_S4]] | [[TBD:MAIN_NOMEM_S5]] | [[TBD:MAIN_NOMEM_WAL]] | [[TBD:MAIN_NOMEM_LME]] | [[TBD:MAIN_NOMEM_LCM]] | [[TBD:MAIN_NOMEM_AVG]] |
| Full-History Stuffing | [[TBD:MAIN_FULLHIST_S1]] | [[TBD:MAIN_FULLHIST_S2]] | [[TBD:MAIN_FULLHIST_S3]] | [[TBD:MAIN_FULLHIST_S4]] | [[TBD:MAIN_FULLHIST_S5]] | [[TBD:MAIN_FULLHIST_WAL]] | [[TBD:MAIN_FULLHIST_LME]] | [[TBD:MAIN_FULLHIST_LCM]] | [[TBD:MAIN_FULLHIST_AVG]] |
| Mem0 | [[TBD:MAIN_MEM0_S1]] | [[TBD:MAIN_MEM0_S2]] | [[TBD:MAIN_MEM0_S3]] | [[TBD:MAIN_MEM0_S4]] | [[TBD:MAIN_MEM0_S5]] | [[TBD:MAIN_MEM0_WAL]] | [[TBD:MAIN_MEM0_LME]] | [[TBD:MAIN_MEM0_LCM]] | [[TBD:MAIN_MEM0_AVG]] |
| A-MEM | [[TBD:MAIN_AMEM_S1]] | [[TBD:MAIN_AMEM_S2]] | [[TBD:MAIN_AMEM_S3]] | [[TBD:MAIN_AMEM_S4]] | [[TBD:MAIN_AMEM_S5]] | [[TBD:MAIN_AMEM_WAL]] | [[TBD:MAIN_AMEM_LME]] | [[TBD:MAIN_AMEM_LCM]] | [[TBD:MAIN_AMEM_AVG]] |
| AWM | [[TBD:MAIN_AWM_S1]] | [[TBD:MAIN_AWM_S2]] | [[TBD:MAIN_AWM_S3]] | [[TBD:MAIN_AWM_S4]] | [[TBD:MAIN_AWM_S5]] | [[TBD:MAIN_AWM_WAL]] | [[TBD:MAIN_AWM_LME]] | [[TBD:MAIN_AWM_LCM]] | [[TBD:MAIN_AWM_AVG]] |
| ReasoningBank | [[TBD:MAIN_RBANK_S1]] | [[TBD:MAIN_RBANK_S2]] | [[TBD:MAIN_RBANK_S3]] | [[TBD:MAIN_RBANK_S4]] | [[TBD:MAIN_RBANK_S5]] | [[TBD:MAIN_RBANK_WAL]] | [[TBD:MAIN_RBANK_LME]] | [[TBD:MAIN_RBANK_LCM]] | [[TBD:MAIN_RBANK_AVG]] |
| SkeMex | [[TBD:MAIN_SKEMEX_S1]] | [[TBD:MAIN_SKEMEX_S2]] | [[TBD:MAIN_SKEMEX_S3]] | [[TBD:MAIN_SKEMEX_S4]] | [[TBD:MAIN_SKEMEX_S5]] | [[TBD:MAIN_SKEMEX_WAL]] | [[TBD:MAIN_SKEMEX_LME]] | [[TBD:MAIN_SKEMEX_LCM]] | [[TBD:MAIN_SKEMEX_AVG]] |
| Memory-R1 | [[TBD:MAIN_MEMR1_S1]] | [[TBD:MAIN_MEMR1_S2]] | [[TBD:MAIN_MEMR1_S3]] | [[TBD:MAIN_MEMR1_S4]] | [[TBD:MAIN_MEMR1_S5]] | [[TBD:MAIN_MEMR1_WAL]] | [[TBD:MAIN_MEMR1_LME]] | [[TBD:MAIN_MEMR1_LCM]] | [[TBD:MAIN_MEMR1_AVG]] |
| Mem-α | [[TBD:MAIN_MEMALPHA_S1]] | [[TBD:MAIN_MEMALPHA_S2]] | [[TBD:MAIN_MEMALPHA_S3]] | [[TBD:MAIN_MEMALPHA_S4]] | [[TBD:MAIN_MEMALPHA_S5]] | [[TBD:MAIN_MEMALPHA_WAL]] | [[TBD:MAIN_MEMALPHA_LME]] | [[TBD:MAIN_MEMALPHA_LCM]] | [[TBD:MAIN_MEMALPHA_AVG]] |
| MemRL | [[TBD:MAIN_MEMRL_S1]] | [[TBD:MAIN_MEMRL_S2]] | [[TBD:MAIN_MEMRL_S3]] | [[TBD:MAIN_MEMRL_S4]] | [[TBD:MAIN_MEMRL_S5]] | [[TBD:MAIN_MEMRL_WAL]] | [[TBD:MAIN_MEMRL_LME]] | [[TBD:MAIN_MEMRL_LCM]] | [[TBD:MAIN_MEMRL_AVG]] |
| Reflexion | [[TBD:MAIN_REFLEXION_S1]] | [[TBD:MAIN_REFLEXION_S2]] | [[TBD:MAIN_REFLEXION_S3]] | [[TBD:MAIN_REFLEXION_S4]] | [[TBD:MAIN_REFLEXION_S5]] | [[TBD:MAIN_REFLEXION_WAL]] | [[TBD:MAIN_REFLEXION_LME]] | [[TBD:MAIN_REFLEXION_LCM]] | [[TBD:MAIN_REFLEXION_AVG]] |
| ReasoningBank+MaTTS | [[TBD:MAIN_RBANKMATTS_S1]] | [[TBD:MAIN_RBANKMATTS_S2]] | [[TBD:MAIN_RBANKMATTS_S3]] | [[TBD:MAIN_RBANKMATTS_S4]] | [[TBD:MAIN_RBANKMATTS_S5]] | [[TBD:MAIN_RBANKMATTS_WAL]] | [[TBD:MAIN_RBANKMATTS_LME]] | [[TBD:MAIN_RBANKMATTS_LCM]] | [[TBD:MAIN_RBANKMATTS_AVG]] |
| **MERIT (ours)** | [[TBD:MAIN_MERIT_S1]] | [[TBD:MAIN_MERIT_S2]] | [[TBD:MAIN_MERIT_S3]] | [[TBD:MAIN_MERIT_S4]] | [[TBD:MAIN_MERIT_S5]] | [[TBD:MAIN_MERIT_WAL]] | [[TBD:MAIN_MERIT_LME]] | [[TBD:MAIN_MERIT_LCM]] | [[TBD:MAIN_MERIT_AVG]] |
| RIT-Full (upper bound) | [[TBD:MAIN_RITFULL_S1]] | [[TBD:MAIN_RITFULL_S2]] | [[TBD:MAIN_RITFULL_S3]] | [[TBD:MAIN_RITFULL_S4]] | [[TBD:MAIN_RITFULL_S5]] | [[TBD:MAIN_RITFULL_WAL]] | [[TBD:MAIN_RITFULL_LME]] | [[TBD:MAIN_RITFULL_LCM]] | [[TBD:MAIN_RITFULL_AVG]] |

Derived headline: average gain over best baseline `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`.

### Table 2 — Reward-swap plugin comparison
Caption intent, conditional on eventual evidence: test whether the causal signal is portable and whether using it as a per-operation reward lifts RL-style managers, which would support (but not by itself prove) that the improvement originates at the signal layer.

| Manager | Reward signal | AVG | Δ vs. original |
|---|---|---|---|
| Memory-R1 | original outcome reward | [[TBD:PLUGIN_MEMR1_ORIG_AVG]] | — (reference) |
| Memory-R1 | φ̂ (MERIT) reward | [[TBD:PLUGIN_MEMR1_PHI_AVG]] | [[TBD:REWARD_SWAP_MEMORY_R1_GAIN]] |
| Mem-α | original RL reward | [[TBD:PLUGIN_MEMALPHA_ORIG_AVG]] | — (reference) |
| Mem-α | φ̂ (MERIT) reward | [[TBD:PLUGIN_MEMALPHA_PHI_AVG]] | [[TBD:REWARD_SWAP_MEMALPHA_GAIN]] |

### Table 3 — Ablation matrix
Caption intent, conditional on eventual evidence: test the necessity of each MERIT component; in particular, test whether swapping causal credit back to co-occurrence utility (A2) removes the gain and thereby localizes the contribution to the signal.

| Variant | AVG | ΔAVG vs. full | SR@20% (t=500) | CCC (held-out) | CTI |
|---|---|---|---|---|---|
| Full MERIT | [[TBD:ABL_FULL_AVG]] | 0 (reference) | [[TBD:ABL_FULL_SR20]] | [[TBD:ABL_FULL_CCC]] | [[TBD:ABL_FULL_CTI]] |
| A1: no recalibration (static attributor) | [[TBD:ABL_A1_AVG]] | [[TBD:ABL_A1_DELTA]] | [[TBD:ABL_A1_SR20]] | [[TBD:ABL_A1_CCC]] | [[TBD:ABL_A1_CTI]] |
| A2: causal credit → co-occurrence utility | [[TBD:ABL_A2_AVG]] | [[TBD:ABL_A2_DELTA]] | [[TBD:ABL_A2_SR20]] | [[TBD:ABL_A2_CCC]] | [[TBD:ABL_A2_CTI]] |
| A3: no scope gating | [[TBD:ABL_A3_AVG]] | [[TBD:ABL_A3_DELTA]] | [[TBD:ABL_A3_SR20]] | [[TBD:ABL_A3_CCC]] | [[TBD:ABL_A3_CTI]] |
| A4: no governance | [[TBD:ABL_A4_AVG]] | [[TBD:ABL_A4_DELTA]] | [[TBD:ABL_A4_SR20]] | [[TBD:ABL_A4_CCC]] | [[TBD:ABL_A4_CTI]] |
| A5: no usage-behavior features | [[TBD:ABL_A5_AVG]] | [[TBD:ABL_A5_DELTA]] | [[TBD:ABL_A5_SR20]] | [[TBD:ABL_A5_CCC]] | [[TBD:ABL_A5_CTI]] |
| A-judge: LLM self-judge instead of RIT | [[TBD:ABL_AJUDGE_AVG]] | [[TBD:ABL_AJUDGE_DELTA]] | [[TBD:ABL_AJUDGE_SR20]] | [[TBD:ABL_AJUDGE_CCC]] | [[TBD:ABL_AJUDGE_CTI]] |
| A7: LOO → group/sampled-Shapley | [[TBD:ABL_A7_AVG]] | [[TBD:ABL_A7_DELTA]] | [[TBD:ABL_A7_SR20]] | [[TBD:ABL_A7_CCC]] | [[TBD:ABL_A7_CTI]] |

### Table 4 — Hypotheses-to-experiments mapping
(See the Hypotheses-to-Experiments Mapping section above; this is its planned-table form. No experimental data cells — all cells are design metadata or hypothesis labels; status column carries `HYPOTHESIS`.)

| Hyp. | Metric | Experiment | Claim | Status |
|---|---|---|---|---|
| H1 | SR@20% slope | Ablation A4 / Mechanism | C3 | HYPOTHESIS |
| H2 | held-out CCC | Fig. 5a / Calibration | C2 | HYPOTHESIS |
| H3 | CTI; transfer CCC | Ablation A3 / Transfer | C3 | HYPOTHESIS |
| H4 | AVG vs. token cost | Efficiency Study | C4 | HYPOTHESIS |
| H5 | gain vs. bank/heterogeneity/redundancy | Boundary & Case Study | C4 | HYPOTHESIS |

### Table 5 — Method comparison / related-work positioning
Caption intent: among the methods currently listed in this report, the planned positioning is that MERIT combines a causal signal, O(1) online scoring, closed-loop recalibration, per-memory scope, and a standalone audit protocol. This positioning and every ✓ / ✗ / — cell require bibliographic verification before use in the paper.

| Method | Causal signal | O(1) online | Closed-loop recalibration | Scope representation | Audit protocol |
|---|---|---|---|---|---|
| Data Shapley `[[TBD:CITATION_DATA_SHAPLEY]]` | ✓ | ✗ | ✗ | ✗ | ✗ |
| Influence Functions `[[TBD:CITATION_INFLUENCE_FUNCTIONS]]` | ✓ | ✗ | ✗ | ✗ | ✗ |
| TracIn `[[TBD:CITATION_TRACIN]]` | ✓ | ✗ | ✗ | ✗ | ✗ |
| ContextCite `[[TBD:CITATION_CONTEXTCITE]]` | partial | ✗ | ✗ | ✗ | ✗ |
| ReasoningBank `[[TBD:CITATION_REASONINGBANK]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| SkeMex `[[TBD:CITATION_SKEMEX]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| Memory-R1 `[[TBD:CITATION_MEMORY_R1]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| MemRL `[[TBD:CITATION_MEMRL]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| **MERIT (ours)** | ✓ | ✓ | ✓ | ✓ | ✓ |

### Table 6 — Efficiency / cost comparison
Caption intent, conditional on eventual evidence: test whether MERIT recovers most of the full-intervention gain at near-baseline token cost and sits at the Pareto-frontier knee.

| Config | Relative token cost | AVG success | ACA latency/event | Extra VRAM | RIT sampling overhead |
|---|---|---|---|---|---|
| Co-occurrence baseline | 1× | [[TBD:EFF_BASELINE_AVG]] | — | — | 0 |
| MERIT | [[TBD:MERIT_RELATIVE_TOKEN_COST]] | [[TBD:EFF_MERIT_AVG]] | [[TBD:ACA_SCORING_LATENCY_MS]] | [[TBD:ACA_VRAM_OVERHEAD_GB]] | [[TBD:RIT_TOKEN_OVERHEAD_PERCENT]] |
| A1 (static attributor) | [[TBD:A1_RELATIVE_TOKEN_COST]] | [[TBD:EFF_A1_AVG]] | [[TBD:ACA_SCORING_LATENCY_MS]] | [[TBD:ACA_VRAM_OVERHEAD_GB]] | [[TBD:RIT_TOKEN_OVERHEAD_PERCENT]] |
| RIT-Full (upper bound) | [[TBD:RITFULL_RELATIVE_TOKEN_COST]] | [[TBD:EFF_RITFULL_AVG]] | — | — | [[TBD:FULL_RIT_COST_MULTIPLIER]] |

---

## Planned Figures

No images are generated here. Each figure has a full textual specification. **Fig. 2 and Fig. 5 must use identical axis ranges** to support the mechanism-closure comparison.

### Fig. 1 — Problem + solution schematic
- **Purpose:** motivate the paper — correlational credit turns memory banks into Skinner boxes; MERIT replaces co-occurrence bookkeeping with randomized-trial evidence.
- **Panel layout:** two panels (left: problem / baseline; right: MERIT).
- **Visual entities:** left — top-utility memories, fraction with no causal effect highlighted; right — RIT→ACA→consumers pipeline flattening superstition.
- **Compared stages:** correlational credit vs. counterfactual credit.
- **Intended takeaway:** `[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]` of top-utility memories have no causal effect (left); MERIT flattens superstition accumulation (right).
- **Future data source:** pilot SR@k and main mechanism analysis.
- **Placeholders required:** `[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]`.
- **Source anchor:** §3.5 Fig.1.

### Fig. 2 — Diagnostic evidence (baseline)
- **Purpose:** show system-assigned utility barely tracks true counterfactual contribution, and superstition grows with deployment.
- **Panel layout:** (a) scatter/correlation of utility vs. φ; (b) SR@20% vs. deployment length.
- **Axes:** (a) x = system utility, y = counterfactual φ; (b) x = task index t (100→500), y = SR@20% (%). **Axis ranges locked to match Fig. 5.**
- **Compared methods:** ReasoningBank, MemRL.
- **Intended takeaway:** (a) measure CCC `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`; (b) test whether SR grows from `[[TBD:PILOT_SR20_T100]]` to `[[TBD:PILOT_SR20_T500]]`, as predicted if correlational credit does not self-correct.
- **Future data source:** pilot/diagnostic study.
- **Placeholders required:** `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`, `[[TBD:PILOT_SR20_T100]]`, `[[TBD:PILOT_SR20_T500]]`.
- **Source anchor:** §3.5 Fig.2, §4.

### Fig. 3 — MERIT architecture / method
- **Purpose:** show the `RIT → ACA → consumers` pipeline on the retrieve–execute–write loop.
- **Panel layout:** single left-to-right pipeline diagram with the base loop and the three added modules.
- **Visual entities:** RIT sampling (paired LOO), ACA attributor (features → φ̂), two consumers (governance, scope-gated retrieval); the recalibration feedback edge.
- **Compared stages:** standard loop vs. MERIT-augmented loop.
- **Intended takeaway:** the additions are minimal and strictly linear; the ablations test whether any gain comes from the signal rather than pipeline complexity.
- **Future data source:** none (schematic).
- **Placeholders required:** none (no data).
- **Source anchor:** §6.0 Fig.3.

### Fig. 4 — Streaming cumulative success curve
- **Purpose:** show MERIT's advantage widens over the stream, concentrated in the late, most-polluted portion.
- **Panel layout:** single line plot, cumulative success vs. task index; MERIT vs. baselines.
- **Axes:** x = task index (1→500+), y = cumulative success rate.
- **Compared methods:** MERIT, strongest baselines, RIT-Full.
- **Intended takeaway:** test what share `[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]` of the average gain `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]` comes from the last portion of the stream.
- **Future data source:** main results streaming logs.
- **Placeholders required:** `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`, `[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]`.
- **Source anchor:** §3.5 Fig.4, §8.3.

### Fig. 5 — Mechanism recovery (MERIT)
- **Purpose:** test whether amortized attribution recovers causal credit at O(1) cost and eliminates the superstition growth hypothesized in Fig. 2.
- **Panel layout:** (a) reliability/correlation of φ̂ vs. φ; (b) SR@20% vs. deployment length, MERIT vs. baseline.
- **Axes:** identical ranges to Fig. 2 (mandated). (a) x = φ̂, y = φ; (b) x = t (100→500), y = SR@20% (%).
- **Compared methods:** ACA (MERIT) vs. correlational baseline.
- **Intended takeaway:** (a) CCC `[[TBD:ACA_HELDOUT_CCC_T500]]` vs. `[[TBD:PILOT_CCC_REASONINGBANK_T500]]` in Fig. 2a; (b) SR flattened to `[[TBD:SR_MERIT_T500]]` (`[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]` at t=500).
- **Future data source:** mechanism & calibration analysis.
- **Placeholders required:** `[[TBD:ACA_HELDOUT_CCC_T500]]`, `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`, `[[TBD:SR_MERIT_T500]]`, `[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]`.
- **Source anchor:** §3.5 Fig.5, §8.5.

### Fig. 6 — Intuition / case study (A3 boundary)
- **Purpose:** convey intuition via a success memory vs. a superstitious memory, and the complementary-memory failure that exposes the A3 boundary.
- **Panel layout:** two mini-timelines (success example; failure example with group-intervention fallback).
- **Visual entities:** utility trajectory vs. RIT φ over tasks; eviction event; scope characterization.
- **Compared stages:** correlational accumulation vs. RIT judgment vs. governance action.
- **Intended takeaway:** superstitious memory's inflated utility is caught and evicted at task `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]`; complementary memories require the group fallback (honest A3 limit).
- **Future data source:** case study logs.
- **Placeholders required:** `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]`.
- **Source anchor:** §8.6 Fig.6, §5 (A3).

---

## Known Weaknesses, Assumptions, and Scope Boundaries

- **A2 dependency (local replayability):** fully non-replayable physical/single-shot environments cannot yield RIT labels. Forward-looking: world-model-simulated replay or off-policy evaluation as a substitute for real interventions.
- **A3 dependency (LOO underestimates credit under high redundancy):** the group-intervention fallback adds cost. Forward-looking: structure-aware interaction attribution.
- **Gain boundary (H5):** single-domain short streams and small banks yield near-zero benefit — MERIT is medicine for long-term deployment, not short sessions. `[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]` of residual failures are expected to stem from missing experience rather than mis-credit (complementary to the "what to write" direction).
- **Scope statement (retained from source):** "We focus on credit assignment for extant memories and leave what-to-write policies (write-time quality) out of scope; MERIT composes with them."
- **Broader impact / rebuttal-sensitive risk:** causal audit improves interpretability and governability; risk — if attribution scores can be manipulated by external content, this becomes a new attack surface (memory-poisoning "credit laundering").
- **Rebuttal-sensitive risks explicitly tracked (source §11):** (1) intervention cost realism; (2) attribution noise / φ̂ trustworthiness; (3) "just Data Shapley/ContextCite on memory"; (4) increment over MemRL/Memory-R1; (5) "only holds in text replayable environments." Each has a design + experiment two-layer defense planned.
- **OPEN QUESTION (not a claim):** whether ACA transfers across fundamentally different modalities beyond the tested text/agentic environments is `NOT SPECIFIED IN SOURCE` and is flagged as an open question, excluded from C1–C4.

---

## Related Work Map

Only method/paper families named by the source are retained; all citation metadata `requires bibliographic verification` and uses `[[TBD:CITATION_<NAME>]]`. No BibTeX/DOI/author lists/paper conclusions are invented. No work is claimed to have "never been done" without qualification.

- **Self-evolving memory & experience distillation (→ C1):** Mem0 `[[TBD:CITATION_MEM0]]`, A-MEM `[[TBD:CITATION_A_MEM]]`, AWM `[[TBD:CITATION_AWM]]`, ReasoningBank `[[TBD:CITATION_REASONINGBANK]]`, SkeMex `[[TBD:CITATION_SKEMEX]]`, MemEvolve `[[TBD:CITATION_MEMEVOLVE]]`. The source proposal characterizes their credit signals as heuristic or co-occurrence based; this characterization requires bibliographic verification. Planned positioning (also requiring verification): the report has not yet identified prior work that audits these signals' causal validity with interventional evidence — this is the gap targeted by C1.
- **Learned memory management (→ C3):** Memory-R1 `[[TBD:CITATION_MEMORY_R1]]`, Mem-α `[[TBD:CITATION_MEM_ALPHA]]`, MemRL `[[TBD:CITATION_MEMRL]]`, MemSkill `[[TBD:CITATION_MEMSKILL]]` — what is learned is the policy; the signal remains outcome-level or MC co-occurrence. EDV `[[TBD:CITATION_EDV]]` uses multi-agent consensus to fix write-time judgment — orthogonal to and composable with fixing full-lifecycle credit.
- **Data valuation & context attribution (→ C2):** Data Shapley `[[TBD:CITATION_DATA_SHAPLEY]]`, Influence Functions `[[TBD:CITATION_INFLUENCE_FUNCTIONS]]`, TracIn `[[TBD:CITATION_TRACIN]]` target training data (static, offline); ContextCite `[[TBD:CITATION_CONTEXTCITE]]` and RAG attribution target single-generation explanations. Positioning (requires verification): the online, non-stationary, closed-loop setting where attribution changes the data distribution — requiring amortization + recalibration — is the gap C2 targets.
- **Related observations named by source:** Evo-Memory `[[TBD:CITATION_EVO_MEMORY]]` and EEVEE `[[TBD:CITATION_EEVEE]]` (cross-task interference); Reflexion `[[TBD:CITATION_REFLEXION]]` and MaTTS `[[TBD:CITATION_MATTS]]` (test-time reasoning, orthogonal-direction baselines); the Skinner superstition analogy `[[TBD:CITATION_SKINNER_SUPERSTITION]]`.
- **Concurrency clause (retained):** an arXiv sweep 2 weeks before submission is planned; reserved phrasing: "Concurrent work [X] explores ..., differing from ours in that their signal remains observational / their attribution is not closed-loop."

---

## Proposed Title

- **Primary:** *MERIT: Retrieval Is Not Contribution — Counterfactual Credit Assignment for Self-Evolving Agent Memory*
- **Alternative 1 (analysis-leaning):** *Superstitious Memories: How Correlational Credit Corrupts Self-Evolving Agents, and How to Fix It*
- **Alternative 2 (conservative method-style):** *Counterfactual Memory Attribution for Self-Evolving LLM Agents*
- **Naming check (executor task before submission):** search "MERIT + LLM/memory/agent" to confirm no name collision; on collision, switch to the reserved names "CREDO / VERITY" and globally replace.

---

## Target Venue

- **AAAI 2027** anonymous preliminary draft. The applicable track and page limit are `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]` and must be confirmed from the corresponding AAAI 2027 call; the Author Kit states that page limits are event-specific.
- Source background only (does **not** override the current task): source proposal's primary NeurIPS 2027 / ICML 2027 with AAAI-28 fallback.

---

## Source Traceability Map

Every object below maps back to a specific section of `paper/00_input/source_proposal.md`. Where the source does not explicitly provide a detail, it is marked `NOT SPECIFIED IN SOURCE`.

- **C1** → §3 P6 (C1), §4 Pilot, §3.5 Fig.2, §5 Prop.1.
- **C2** → §3 P6 (C2), §6.2, §8.5, §3.5 Fig.5.
- **C3** → §3 P6 (C3), §6.3, §8.4, §8.3 Table 2.
- **C4** → §3 P6 (C4), §8.
- **Proposition 1** → §5 (informal statement), appendix C (formal proof, referenced).
- **A1 (observable outcome)** → §5 Assumptions A1.
- **A2 (local replayability)** → §5 Assumptions A2; §4 (replayable streams); §6.1 (sampling only on A2 tasks).
- **A3 (low-order interaction)** → §5 Assumptions A3; §8.5/§8.6 (boundary), Fig.6.
- **RIT module** → §6.1; first appearance §4 (intervention protocol).
- **ACA module** → §6.2; §8.5 (calibration).
- **Credit Governance** → §6.3 (three rules); §0 (RL manager downgraded).
- **Scope-Gated Retrieval** → §6.3 (gating); §7 (CTI definition).
- **Cost/Complexity** → §6.4; §8.1 (hardware); appendix B/E (cost tables).
- **H1** → label inferred; source anchors §6.3 (governance) / §8.5 (SR recovery), §7 mapping table (not spelled out).
- **H2** → §8.5 (CCC recovery, ρ≥0.6 gate), §6.2; §3.5 Fig.5a.
- **H3** → §8.5 (transfer, CTI), §6.3; §7 (CTI definition).
- **H4** → §8.7 (efficiency), §8.5 (p-sweep saturation).
- **H5** → §4 (boundary note), §8.5 (three trend lines), §10 (limitations).
- **Table 1 (main)** → §8.3 (Table 1 structure). Stream S2–S4 identities `NOT SPECIFIED IN SOURCE`.
- **Table 2 (plugin)** → §8.3 (Table 2), §6.3.
- **Table 3 (ablation)** → §8.4 (A1–A7, A-judge), §6.4 (design-choice rows).
- **Table 4 (hypotheses)** → §7; §12 (assumption-closure checklist).
- **Table 5 (positioning)** → §9 (comparison table columns).
- **Table 6 (efficiency)** → §8.7 (Pareto plot).
- **Fig. 1** → §3.5 Fig.1.
- **Fig. 2** → §3.5 Fig.2, §4.
- **Fig. 3** → §6.0.
- **Fig. 4** → §3.5 Fig.4, §8.3.
- **Fig. 5** → §3.5 Fig.5, §8.5.
- **Fig. 6** → §8.6, §5 (A3).
- **Limitations** → §10 (three limitations), §11 (rebuttal risks).
- **Rebuttal-sensitive risks** → §11 (five attack points), §8.5 (calibration defense).
- **Subtraction decisions (RL manager, full Shapley downgraded)** → §0.
- **Venue** → §-1 header / 用法说明 (source primary NeurIPS/ICML 2027, fallback AAAI-28); current task venue override to AAAI 2027 is a task-level instruction, `NOT SPECIFIED IN SOURCE`.
