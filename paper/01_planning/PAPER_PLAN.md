# Paper Plan — MERIT (AAAI 2027 anonymous preliminary draft)

> **Status:** `DRAFT PLAN — CROSS-REVIEWED (Codex gpt-5.6-sol, xhigh)`
> **Evidence state:** experiments **not** executed. Every quantitative result is an unresolved `[[TBD:...]]` placeholder from the registered ledger, never a measured value. C1–C4 are `PLANNED-EVIDENCE`; Proposition 1 is a `HYPOTHESIS`.
> **Authority order:** user task instructions → `.agents/docs/AAAI-AuthorKit27/` → `DRAFT_POLICY.md` → `NARRATIVE_REPORT.md` → `source_proposal.md` → ARIS/Claude output. This plan is advisory and does not override any of the first five.
> **Governing constraints:** `paper/01_planning/STEP4_ARIS_PAPER_PLAN_GUARDRAILS.md` and `paper/01_planning/DRAFT_POLICY.md`. On any conflict, those two win over the ARIS skill defaults (e.g. the skill's built-in "AAAI = 7 pages" is **not** used here).
> **Source integrity at planning time:** `source_proposal.md` SHA-256 `E700D46BDD1B4F83A2D45466EDBDB2112D2FAB3EFDCC912A7AED2F5BDFC496CC` (`MATCH`).

---

## 1. Working Title

- **Primary:** *MERIT: Retrieval Is Not Contribution — Counterfactual Credit Assignment for Self-Evolving Agent Memory*
- **Alternative 1 (analysis-leaning):** *Superstitious Memories: How Correlational Credit Corrupts Self-Evolving Agents, and How to Fix It*
- **Alternative 2 (conservative method-style):** *Counterfactual Memory Attribution for Self-Evolving LLM Agents*
- **Naming check (deferred executor task, not run now):** search "MERIT + LLM/memory/agent" to confirm no name collision; on collision, switch to reserved names "CREDO / VERITY" and globally replace. Title must follow AAAI Title Case (Chicago) rules.

## 2. One-Sentence Contribution

Causal (counterfactual) credit — not better heuristics — is the missing primitive of self-evolving agent memory, and MERIT is **designed to make** it affordable online via randomized interventional trials amortized into an O(1)-per-event attributor whose single signal is directly consumed by memory governance and scope-gated retrieval.

*(Wording is deliberately design-scoped: "designed to make" not "makes." Affordability, accuracy, and end-to-end overhead are `PLANNED-EVIDENCE`.)*

## 3. Venue, Paper Type, Evidence State, Conditional Page Budget

- **Venue:** AAAI 2027 (anonymous preliminary draft). Track and page limit are **unverified** → `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`.
- **Format source:** `.agents/docs/AAAI-AuthorKit27/` (`aaai2027.sty`, `aaai2027.bst`). Two-column US-letter; `natbib` `\citep`/`\citet`; `\setcounter{secnumdepth}{0}` default (section numbers optional). **Do not** modify the style file or use forbidden packages (`geometry`, `hyperref`, `titlesec`, `setspace`, …) or page-break/space-compression tricks. Anonymous author block placeholder only; no acknowledgments/grant IDs until camera-ready.
- **Paper type:** primary **T1 (new method)** + auxiliary **T2 (new insight)**. Single narrative prototype: **Type A repair/fix**.
- **Evidence state:** all headline numbers are planned. C1–C4 = `PLANNED-EVIDENCE`; Proposition 1 = `HYPOTHESIS`; O(1) online scoring = `SUPPORTED-BY-DESIGN`; all thresholds/hyperparameters = `provisional hyperparameter` / `planned configuration`.
- **Conditional page budget (proportional; do NOT hard-code 7 or 9 pages):** plan by share of body text (Abstract excluded from the body-proportion pool). Let `N` = number of technical-content pages the AAAI 2027 call ultimately allows (references/appendix counted per the official call, currently `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`). Then target pages per section ≈ `share × N`.

  | Section | Body share | Conditional pages |
  |---|---:|---|
  | §1 Introduction | 13% | `0.13 · N` |
  | §2 Related Work | 8% | `0.08 · N` |
  | §3 Problem Formulation & Superstitious-Memory Hypothesis | 10% | `0.10 · N` |
  | §4 Pilot / Diagnostic Study | 12% | `0.12 · N` |
  | §5 Method: MERIT | 25% | `0.25 · N` |
  | §6 Experiments & Analysis | 27% | `0.27 · N` |
  | §7 Limitations & Conclusion | 5% | `0.05 · N` |

  **Method + Ablation/Mechanism battleground:** §5 (25%) + a reserved 15–18 points of §6 ≈ **40–43%** of the body, honoring the source's "Method + ablation are the main battleground." **Pilot is held to 12%** (diagnostic only). Sections sum to 100%. Table/figure count (6 + 6) is the real page-pressure source, not prose — see appendix-first demotions in §11.

## 4. Claims–Evidence Matrix (C1–C4)

Overall status of every claim is `PLANNED-EVIDENCE`. No planned mechanism is written as an observed result. Result cells cite only registered `[[TBD:...]]` IDs.

| Claim | Statement (evidence-disciplined) | Planned evidence (experiment → metric/artifact) | Falsification gate | Status | Locus |
|---|---|---|---|---|---|
| **C1** (T2) | Correlational credit systematically breeds *superstitious memories* (zero/negative-φ memories in the top-utility set) whose fraction rises with deployment time; the RIT audit + statistics `CCC` and `SR@k` measure this interventionally. | Pilot on ReasoningBank- & MemRL-style banks over replayable streams → `CCC` and `SR@k` vs deployment length (Fig 2); two alt-explanation controls: split-half reliability `[[TBD:PILOT_SPLITHALF_PHI_RELIABILITY]]`, φ>0-subset removal drop `[[TBD:PILOT_UTILITY_SUBSET_REMOVAL_DROP]]`. | If `CCC > 0.5` **or** `SR@k` does not rise with `t`, the attribution hypothesis is falsified → narrow claim to heterogeneous streams; do not force-write. | `PLANNED-EVIDENCE` | §4 Pilot; Fig 2; Prop 1 |
| **C2** (T1, core) | ACA amortizes RIT labels into an O(1)-per-event attributor with periodic recalibration; we **test whether** it makes counterfactual credit affordable and recovers causal credit better than the correlational baseline. | Held-out `CCC` of ACA `[[TBD:ACA_HELDOUT_CCC_T500]]` vs baseline `[[TBD:PILOT_CCC_REASONINGBANK_T500]]` (Fig 5a); calibration (reliability diagram, ECE `[[TBD:ECE_ACA_HELDOUT]]`); split-half; recalibration ablation A1; usage-feature ablation A5. | H2 gate: held-out `CCC` `ρ < 0.6` undercuts C2. | `PLANNED-EVIDENCE` (O(1) is `SUPPORTED-BY-DESIGN`; accuracy/cost are planned) | §5.2 Method; §6 Mechanism & Calibration; Fig 5a |
| **C3** (T1) | One causal-credit signal is **directly consumable**: two minimal readouts — threshold governance and per-memory scope-gated retrieval — respectively **test whether** superstition accumulation flattens and cross-task interference (CTI) reduces; the same signal is **tested** as a per-operation RL reward. | Ablations A2 (swap causal→co-occurrence; test whether gain vanishes), A3 (no scope), A4 (no governance); `CTI` measurement; signal-portability check (reward substitution) → Table 2. | A2 gate: if gain persists after swapping causal→co-occurrence, the contribution is **not** localized to the signal. | `PLANNED-EVIDENCE` | §5.3 Method; §6 Ablation; §6 signal-portability check; Table 2 |
| **C4** (empirical) | Across 4 benchmark categories, 3 backbones, 3 seeds, we **test whether** MERIT improves average performance over the strongest baseline at low token overhead and whether closed-loop `CCC`/`SR@k` recover. | Main table (Table 1), ablations (Table 3), efficiency Pareto (Table 6, Fig 4), scaling/transfer — all pending execution. | Standard: no significant avg gain under paired bootstrap → revise scope. | `PLANNED-EVIDENCE` | §6 Experiments (entire) |

**Additional theoretical commitment (not a numbered contribution):** **Proposition 1** — `HYPOTHESIS`, formal statement + proof deferred to appendix; must not be described as proven until the proof is written and human-checked.

## 5. Hypotheses–Evidence Map (H1–H5)

> **Label-collision fix (adopted from cross-review):** the source reuses `A1/A2/A3` for **both** formulation assumptions and ablation variants. In this plan and in `/paper-write`, the **formulation assumptions are relabeled `AS1–AS3`**; ablation variants keep `A1–A7`. Source mapping preserved: `AS1`=observable outcome, `AS2`=local replayability, `AS3`=low-order interaction. This is a label-only disambiguation (no scope/semantic change); flagged for user confirmation in the Review Integration Log.

| Hyp. | Statement (reconstructed) | Primary metric | Experiment locus | Related claim | Status |
|---|---|---|---|---|---|
| **H1** | Threshold governance flattens superstition accumulation over the stream. | `SR@20%` **slope** over deployment (read from the Fig 5b trajectory, Full vs A4 across checkpoints — not a single endpoint) | Ablation A4 / Mechanism | C3 | `HYPOTHESIS` |
| **H2** | ACA recovers causal credit at O(1) cost. | Held-out `CCC` (Spearman); source gate `ρ ≥ 0.6` | Mechanism & Calibration; Fig 5a | C2 | `HYPOTHESIS` |
| **H3** | Scope gating removes cross-task interference and transfers zero-shot. | `CTI`; transfer `CCC` `[[TBD:ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA]]` | Ablation A3 / Scaling & transfer | C3 | `HYPOTHESIS` |
| **H4** | RIT budget saturates at small `p`; MERIT is Pareto-efficient. | AVG vs token cost; `p`-sweep `p ∈ {1,2,5,10}%` | Efficiency Study (with body-level `p`-sweep) | C4 | `HYPOTHESIS` |
| **H5** | Gain has boundaries: near-zero for small banks, single-domain short streams, high redundancy. | gain vs bank size `[[TBD:H5_GAIN_SMALL_BANK_LT100]]`, vs heterogeneity `[[TBD:H5_GAIN_SINGLE_DOMAIN]]`, vs injected-redundancy ratio (**redundancy-gain has no ledger ID → `EVIDENCE GAP`, kept exploratory**) | Boundary & Scaling; Case Study | C4 (+ scope note) | `HYPOTHESIS` |

**Signal parameterization (adopted from cross-review):** define `CCC(s, φ)` = Spearman between signal `s` and RIT true `φ`, and `SR@k(s)` = fraction of top-`k%`-by-`s` memories with `φ ≤ 0`, where `s = Û` (correlational utility) for the baseline and `s = φ̂_ACA` for MERIT. This keeps Fig 2 (baseline `s=Û`) and Fig 5 (MERIT `s=φ̂`) comparable while making the ranking signal explicit.

## 6. Section Architecture (7 body sections + Abstract)

Each section lists: **goal · paragraph-level logic · claims relied on · evidence status · tables/figures · citation slots · body share · appendix-movable content.**

### §0 Abstract (150–250 words, not in body-proportion pool)
- **Goal / 5-part structure:** (1) *what*: identify superstitious memories and give the first affordable counterfactual credit for self-evolving memory; (2) *why hard*: per-memory intervention appears unaffordable online, non-stationary, closed-loop; (3) *how*: RIT → ACA (O(1)) → two consumers; (4) *evidence plan*: one planned-evidence sentence covering credit **fidelity**, **consumer effects** (governance/scope), and **efficiency**; (5) *headline*: single registered placeholder only, e.g. average gain `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`.
- **Discipline:** no undefined acronyms, no citations, no observed-result verbs. End on planned-evidence + registered placeholder (adopted from cross-review).
- **Evidence status:** frames C1–C4 as planned. **Self-contained check:** yes.

### §1 Introduction (13%)
- **Goal:** make *What / Why / So What* explicit before the method; front-load for skim reviewers.
- **Paragraph logic:** (a) hook — *retrieval ≠ use ≠ contribution*; correlational credit turns memory banks into Skinner boxes `[[TBD:CITATION_SKINNER_SUPERSTITION]]`; (b) gap — among the compared, to-be-verified systems, credit is characterized as correlational (**pending bibliographic verification**); prior work does not directly measure counterfactual value because per-memory intervention appears unaffordable; (c) one-sentence contribution (§2 above); (d) approach overview — RIT → ACA → consumers, strictly linear; (e) contribution bullets = **C1–C4** (specific, falsifiable, planned); (f) results preview stated as *planned tests*, not findings; (g) hero figure = Fig 1.
- **Contribution bullets (front-matter fix — one C3 bullet):**
  1. *We reveal and quantify superstitious memories …* (C1)
  2. *We introduce ACA, an O(1)-per-event counterfactual attributor …* (C2)
  3. *We show one causal-credit signal is directly consumable …* (C3) — governance, scope gating, and reward substitution are listed as **evaluations** of this one bullet, never as three contributions.
  4. *We plan a systematic evaluation across 4 categories / 3 backbones / 3 seeds …* (C4)
- **Claims:** C1–C4. **Evidence status:** planned. **Figure:** Fig 1. **Citation slots:** `[[TBD:CITATION_SKINNER_SUPERSTITION]]`, `[[TBD:CITATION_REASONINGBANK]]`, `[[TBD:CITATION_MEMRL]]` (motivation). **Front-loading check:** main claim legible by end of intro. **Appendix-movable:** none.

### §2 Related Work (8%)
- **Goal:** synthesize, not list; organize by methodological family; position MERIT against each.
- **Paragraph logic (3 families, each ≥ substantive synthesis):**
  1. *Self-evolving memory & experience distillation* → C1: Mem0, A-MEM, AWM, ReasoningBank, SkeMex, MemEvolve. Positioning (verification-pending): existing approaches **in our comparison** commonly use correlational/heuristic credit; no verified prior work audits causal validity interventionally.
  2. *Learned memory management* → C3: Memory-R1, Mem-α, MemRL, MemSkill (policy is learned; signal stays outcome-level/MC co-occurrence); EDV (write-time consensus, orthogonal/composable).
  3. *Data valuation & context attribution* → C2: Data Shapley, Influence Functions, TracIn (static/offline training data); ContextCite / RAG attribution (single-generation). Gap: online, non-stationary, closed-loop attribution that changes the data distribution — needs amortization + recalibration.
- **Also named:** Evo-Memory, EEVEE (CTI); Reflexion, MaTTS (orthogonal test-time reasoning baselines). **Concurrency clause** reserved (arXiv sweep 2 weeks pre-submission; reserved phrasing only).
- **Claims:** C1–C3 positioning. **Table:** Table 5 (all ✓/✗/partial cells **verification-pending**; see re-expression note in Table Plan). **Citation slots:** all `[[TBD:CITATION_*]]` for the above. **Rule:** no unqualified first/only/never; use "among the compared, bibliographically verified instantiations …". **Appendix-movable:** extended positioning prose.

### §3 Problem Formulation & Superstitious-Memory Hypothesis (10%)
- **Goal:** formal setup + the one theoretical commitment.
- **Paragraph logic:** (a) 8 symbols (task stream `{(q_t,r_t)}`, bank `M_t`, retrieval `R(q_t)`, policy `π`, attributor `g_θ`, running credit `φ̄_i`, scope `S_i`); (b) **Definition 1** counterfactual contribution `φ_i(q) ≜ E[r|q,R(q)] − E[r|q,R(q)∖{m_i}]`; (c) **Definition 2** co-occurrence utility `Û` (baseline signal); (d) **Proposition 1 (informal, `HYPOTHESIS`)** — under `Cov ≠ 0`, `Û` is asymptotically biased for `φ`, and a stable superstition equilibrium exists; formal statement + proof in appendix; **must not be called proven**; (e) **assumptions AS1** (observable outcome), **AS2** (local replayability — only RIT label collection needs it, ACA online scoring does not), **AS3** (low-order interaction — bounds LOO-vs-Shapley error); (f) optimization objects + budget constraint `ε = [[TBD:RIT_BUDGET_EPSILON_PERCENT]]` (provisional).
- **Claims:** underpins C1/C2. **Evidence status:** Prop 1 `HYPOTHESIS`; defs are `SUPPORTED-BY-DESIGN`. **Figure/Table:** none. **Citation slots:** valuation/attribution refs deferred to §2. **Appendix-movable:** full Prop 1 proof (mandatory appendix), extended assumption discussion.

### §4 Pilot / Diagnostic Study — "Why Does Memory Credit Go Wrong?" (12%; delivers C1)
- **Opening line (second-story guard, adopted):** "This section diagnoses the failure that MERIT is designed to address; it introduces no second method."
- **Goal:** interventional evidence that correlational credit does not self-correct and superstition grows with deployment.
- **Paragraph logic:** (a) systems — reproduce ReasoningBank (heuristic) + MemRL (MC-learned) on the unified codebase, backbone Qwen3-32B; (b) streams — two replayable (ALFWorld, HotpotQA), 500 tasks, 3 seeds (replayability required for paired rollouts); (c) **RIT intervention protocol** (first appearance) — freeze snapshots `t ∈ {100,200,300,400,500}`, sample 300 (query, retrieved-set) pairs, paired LOO `K=5` fixed-seed rollouts, `φ̂_i = success-rate difference` (counts are `planned configuration`); (d) statistics `CCC` and `SR@k`; (e) two alt-explanation controls; (f) **falsification gate** kept honestly.
- **Closing paragraph (hand-off to method, adopted):** "The diagnostic yields two method requirements — approximate RIT credit online, and expose the same credit signal to downstream consumers — realized by MERIT (Fig 3)."
- **Claims:** C1. **Evidence status:** `PLANNED-EVIDENCE`. **Figure:** Fig 2. **Placeholders:** `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`, `[[TBD:PILOT_CCC_MEMRL_T500]]`, `[[TBD:PILOT_SR20_T100]]`, `[[TBD:PILOT_SR20_T500]]`, `[[TBD:PILOT_SPLITHALF_PHI_RELIABILITY]]`, `[[TBD:PILOT_UTILITY_SUBSET_REMOVAL_DROP]]`, `[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]`, `[[TBD:PILOT_TOTAL_TOKEN_COST]]`. **Citation slots:** `[[TBD:CITATION_REASONINGBANK]]`, `[[TBD:CITATION_MEMRL]]`. **Appendix-movable:** reproduction details, per-snapshot budget/cost table (keep body to protocol + Fig 2 + controls + gate).

### §5 Method: MERIT (25%; C2, C3)
- **Opening line (target-continuity guard, adopted):** "ACA predicts the same `φ` audited in Fig 2 (the diagnostic target), not a new quantity."
- **Goal:** the affordable, directly-consumable causal-credit mechanism; one pipeline, no parallel tricks.
- **§5.1 Overview (Fig 3):** RIT → ACA → consumers on the retrieve–execute–write loop; strict upstream→downstream dependency; recalibration feedback edge.
- **§5.2 RIT sampling → labels:** trial probability `p = [[TBD:RIT_SAMPLING_PROB_PERCENT]]` (provisional; source default 5%), paired LOO `K=5`, position-confound control (filler placeholder), emit `(q, m_i, traj, φ̂_i)`; sampling only on AS2-satisfying tasks. Naive "LLM self-judge" retained as ablation `A-judge`.
- **§5.3 ACA (core, → C2):** feature groups — query rep, memory rep (`Qwen3-Embedding-4B` frozen), **usage-behavior features** (n-gram/edit overlap, citation markers, position/rank, log-likelihood gain); 2-layer MLP regressing `φ̂ ∈ [−1,1]`; Huber loss (`δ=0.1` provisional); **periodic recalibration** every 100 tasks + isotonic; online EMA update of `φ̄_i`, proto±.
- **§5.4 Consumers (→ C3) — two readouts of the same `φ̂`:**
  - *Credit governance:* evict (`φ̄<−0.02`, `n≥8`), merge (sim>0.9 & both φ̄>0), quarantine (UCB bonus, `n_min=3`); thresholds provisional; ±0.02 dead-zone tied to calibration.
  - *Scope-gated retrieval:* `score = α·rel + β·(sim(q,proto⁺)−sim(q,proto⁻)) + γ·φ̄`, `(α,β,γ)=(1.0,0.5,0.3)` provisional.
- **§5.5 Cost/complexity commitments:** dependency check `RIT→ACA→consumers`; O(1) scope statement (**adopted**): "ACA inference is O(1) in bank size at fixed feature dimension; RIT collection and periodic recalibration are accounted for separately." One-sentence body overhead with placeholders `[[TBD:ACA_SCORING_LATENCY_MS]]`, `[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]`, `[[TBD:TOKEN_OVERHEAD_PERCENT]]`, `[[TBD:ACA_VRAM_OVERHEAD_GB]]`; full table in appendix.
- **Algorithm 1** (main loop, structure retained). **Claims:** C2, C3. **Evidence status:** design properties `SUPPORTED-BY-DESIGN`; accuracy/cost `PLANNED-EVIDENCE`. **Figure:** Fig 3 (drawable now, no data). **Placeholders:** as listed. **Appendix-movable:** design-choice justification table, full cost table, isotonic/recalibration detail.

### §6 Experiments & Analysis (27%; reserve 15–18 pts for Ablation + Mechanism)
- **§6.1 Setup:** backbones `Qwen3-32B` (primary), `Qwen3-235B-A22B` (scale point), `GPT-5.1` (closed-source row); ACA `Qwen3-Embedding-4B`+MLP, trainable params `[[TBD:ACA_TRAINABLE_PARAMS]]`; `EvolveLab` unified codebase; 4 benchmark **categories** (Evo-Memory streams, WebArena-Lite, LongMemEval, LoCoMo; pilot uses ALFWorld + HotpotQA); fairness (same retriever, `top-k=4`, equal budget; seeds `{13,42,2026}`, mean±std, paired bootstrap 10⁴, p-values, per-point CIs); judge-bias control (`GPT-5.1` judge, 200 human-checked, κ `[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]`); hardware 8×A100-80G, `[[TBD:MAIN_GPU_HOURS_PER_RUN]]`.
- **§6.2 Main results (Table 1):** narrative written as falsifiable tests — (i) whether gain grows with heterogeneity (`[[TBD:MAIN_GAIN_SINGLE_DOMAIN]]`→`[[TBD:MAIN_GAIN_MIXED_STREAM]]`); (ii) whether learned-credit baselines beat heuristic ones; (iii) whether MERIT reaches `[[TBD:MERIT_FRACTION_OF_RITFULL_GAIN]]` of the RIT-Full reference gain. Headline `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`.
- **§6.3 Ablation (Table 3):** A1–A7, A-judge; organized as a causal chain (**adopted analysis layout**): credit fidelity (`CCC`) → SR/CTI change → task outcome (AVG). A2 is the key signal-localization test.
- **§6.4 Mechanism & Calibration recovery (Fig 5; H1, H2):** Fig 5 **reuses Fig 2 axes + stats**; (a) baseline `CCC` vs ACA `CCC`; (b) `SR@20%` trajectory, MERIT vs baseline — **H1 slope read here (Full vs A4 across checkpoints)**; calibration (reliability, ECE `[[TBD:ECE_ACA_HELDOUT]]`, per-domain, split-half; sign-instability near φ≈0).
- **§6.5 Signal-portability check: reward substitution (→ nested under Mechanism/Ablation; Table 2):** replace Memory-R1 / Mem-α reward with `φ̂`, GRPO unchanged; expected lifts `[[TBD:REWARD_SWAP_MEMORY_R1_GAIN]]`, `[[TBD:REWARD_SWAP_MEMALPHA_GAIN]]`. Framed as portability of one signal, **not** a separate method. Compact body summary; full Table 2 appendix-first.
- **§6.6 Boundary & Scaling (H3, H5):** 32B→235B scaling (`[[TBD:SCALING_GAIN_32B]]`→`[[TBD:SCALING_GAIN_235B]]`); zero-shot transfer `CCC` `[[TBD:ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA]]`; boundary trend lines (bank size, heterogeneity, redundancy — redundancy-gain = `EVIDENCE GAP`).
- **§6.7 Efficiency (Table 6, Fig 4; H4):** Pareto (x=relative token cost log, y=AVG); `p`-sweep shown in body (Fig 4 inset, curve labeled *prediction/planned comparison*); knee test.
- **§6.8 Case study (Fig 6; AS3 boundary):** success vs superstitious memory; complementary-memory failure + group-intervention fallback; residual-failure `[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]`. **Appendix-first candidate.**
- **Claims:** C2, C3, C4. **Evidence status:** all `PLANNED-EVIDENCE`. **Tables:** 1, 2 (summary), 3, 6. **Figures:** 4, 5, 6. **Appendix-movable:** full Table 2, Fig 6, three-backbone/three-seed per-slice panels, reproduction detail.

### §7 Limitations & Conclusion (5%)
- **Goal:** honest scope + restated contributions.
- **Paragraph logic:** AS2 dependency (non-replayable environments); AS3 dependency (LOO underestimates under redundancy; group fallback cost); H5 gain boundary (medicine for long-term deployment, not short sessions); scope statement (credit for extant memories; what-to-write out of scope; MERIT composes); broader-impact / rebuttal-sensitive risk (memory-poisoning "credit laundering" attack surface); restated C1–C4 (rephrased, not copy-pasted); 1–2 concrete future directions.
- **Claims:** all. **Evidence status:** honest limitations. **Appendix-movable:** extended rebuttal-risk two-layer defenses.

## 7. Table Plan (Table 1–6, all retained; structure inherited from `NARRATIVE_REPORT.md`; no fabricated numbers)

| ID | Title | Rows / Columns (inherited) | Result-cell placeholders | Body vs Appendix | Priority |
|---|---|---|---|---|---|
| **Table 1** | Main benchmark comparison | 13 method rows (No-Memory ReAct … MERIT (ours), RIT-Full) × {S1–S5, WebArena-Lite, LongMemEval, LoCoMo, AVG}; **S2–S4 identities `NOT SPECIFIED IN SOURCE`** | `[[TBD:MAIN_*]]` (per cell), headline `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]` | Body | HIGH |
| **Table 2** | Reward substitution (signal portability) | Memory-R1 / Mem-α × {orig reward, φ̂ reward} × {AVG, Δ} | `[[TBD:PLUGIN_*]]`, `[[TBD:REWARD_SWAP_*]]` | **Compact summary in body; full table appendix-first** | MEDIUM |
| **Table 3** | Ablation matrix | Full, A1, A2, A3, A4, A5, A-judge, A7 × {AVG, ΔAVG, SR@20%(t=500), CCC(held-out), CTI} | `[[TBD:ABL_*]]` | Body | HIGH |
| **Table 4** | Hypotheses→experiments mapping | H1–H5 × {metric, experiment, claim, status} + **benchmark→category & backbone-aggregation rules (added per cross-review)** | none (design metadata only) | **Appendix-first** | LOW |
| **Table 5** | Method positioning | 9 method rows × {causal signal, O(1) online, closed-loop recalibration, scope rep, audit protocol} | none — cells are ✓/✗/partial | Body | HIGH |
| **Table 6** | Efficiency / cost | baseline (1×), MERIT, A1, RIT-Full × {rel token cost, AVG, ACA latency/event, extra VRAM, RIT overhead} | `[[TBD:EFF_*]]`, `[[TBD:*_TOKEN_COST]]`, `[[TBD:ACA_SCORING_LATENCY_MS]]`, `[[TBD:ACA_VRAM_OVERHEAD_GB]]`, `[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]`, `[[TBD:FULL_RIT_COST_MULTIPLIER]]` | Body | HIGH |

**Table 1 framing note:** the row `RIT-Full (upper bound)` is inherited verbatim from the source structure; in prose it is described as an **"RIT-Full intervention reference,"** and called a ceiling **only for quantities where that status follows by construction** (adopted from cross-review; the table row label itself is not altered, per the guardrail that Table 1–6 inherit source row/column design).

**Table 5 discipline (guardrail + cross-review):** every ✓/✗/partial/— requires **item-by-item bibliographic verification** before use. In `/paper-write`, cells will be **re-expressed as `reported` / `not reported` / `unclear`** tied to the corresponding `[[TBD:CITATION_*]]`; a `not reported` cell is **never** read as "the method cannot do this." Fixed reference cells (MERIT's own row) reflect design, still verification-gated for competitor rows.

**Bold/rank discipline:** no bold-as-best, underline, ranking, or significance marks until data reach `VERIFIED`. The method name "MERIT (ours)" may be bold for identity only.

## 8. Figure Plan (Fig 1–6, all retained)

| ID | Type | Purpose / panels | Comparisons | Future data source | Placeholders | Body vs Appendix |
|---|---|---|---|---|---|---|
| **Fig 1** | Hero schematic | 2 panels: left = correlational credit → Skinner-box superstition; **right = "MERIT mechanism and testable prediction"** (RIT→ACA→consumers), prediction curve **dashed + labeled `prediction`** (front-matter fix) | correlational vs counterfactual credit | pilot SR@k + mechanism analysis | `[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]` | Body (HIGH) |
| **Fig 2** | Diagnostic (baseline) | (a) `Û` vs `φ` scatter; (b) `SR@20%` vs deployment. **Axis ranges + stats LOCKED to match Fig 5.** | ReasoningBank, MemRL | pilot/diagnostic | `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`, `[[TBD:PILOT_SR20_T100]]`, `[[TBD:PILOT_SR20_T500]]` | Body (HIGH) |
| **Fig 3** | Architecture (schematic) | RIT→ACA→consumers on retrieve–execute–write loop; recalibration edge | standard loop vs MERIT loop | none (schematic) | none | Body (HIGH) — **drawable now** |
| **Fig 4** | Streaming curve | cumulative success vs task index; **+ `p`-sweep inset labeled `planned comparison`** (H4, adopted) | MERIT, strongest baselines, RIT-Full reference | main streaming logs; sensitivity `p`-sweep | `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`, `[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]` (p-sweep values = `EVIDENCE GAP`, no ledger ID) | Body (MEDIUM) |
| **Fig 5** | Mechanism recovery (MERIT) | (a) `φ̂` vs `φ`; (b) `SR@20%` vs deployment. **Identical axis ranges + stats to Fig 2 (mandated).** H1 slope + H2 read here. | ACA (MERIT) vs correlational baseline | mechanism & calibration | `[[TBD:ACA_HELDOUT_CCC_T500]]`, `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`, `[[TBD:SR_MERIT_T500]]`, `[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]` | Body (HIGH) |
| **Fig 6** | Case study (AS3 boundary) | success vs superstitious memory timeline; complementary-memory failure + group fallback | correlational accumulation vs RIT vs governance | case-study logs | `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]` | **Appendix-first** |

**Fig 2 ↔ Fig 5 lock (hard):** identical axis ranges **and** identical statistical definitions (`CCC(s,φ)`, `SR@k(s)`); any change must be applied to both simultaneously. **Result figures plan data fields + to-be-tested trends only — no invented curves, bar heights, error bands, or scatter positions.** Schematic/projected curves are labeled `prediction` / `planned comparison`. **Hero-figure justification:** Fig 1 lets a skim reviewer grasp the *retrieval ≠ contribution* claim and the RIT→ACA→consumers fix before the method; it must not introduce a second narrative.

## 9. Citation Plan (existing IDs only; all pending bibliographic verification)

- **§1 Intro (motivation):** `[[TBD:CITATION_SKINNER_SUPERSTITION]]`, `[[TBD:CITATION_REASONINGBANK]]`, `[[TBD:CITATION_MEMRL]]`.
- **§2 Family 1 (self-evolving memory):** `[[TBD:CITATION_MEM0]]`, `[[TBD:CITATION_A_MEM]]`, `[[TBD:CITATION_AWM]]`, `[[TBD:CITATION_REASONINGBANK]]`, `[[TBD:CITATION_SKEMEX]]`, `[[TBD:CITATION_MEMEVOLVE]]`.
- **§2 Family 2 (learned memory management):** `[[TBD:CITATION_MEMORY_R1]]`, `[[TBD:CITATION_MEM_ALPHA]]`, `[[TBD:CITATION_MEMRL]]`, `[[TBD:CITATION_MEMSKILL]]`, `[[TBD:CITATION_EDV]]`.
- **§2 Family 3 (data valuation & context attribution):** `[[TBD:CITATION_DATA_SHAPLEY]]`, `[[TBD:CITATION_INFLUENCE_FUNCTIONS]]`, `[[TBD:CITATION_TRACIN]]`, `[[TBD:CITATION_CONTEXTCITE]]`.
- **§2 Also named / baselines:** `[[TBD:CITATION_EVO_MEMORY]]`, `[[TBD:CITATION_EEVEE]]`, `[[TBD:CITATION_REFLEXION]]`, `[[TBD:CITATION_MATTS]]`.
- **Table 5:** all of the above valuation/memory rows.
- **Rules:** never generate BibTeX/DOI/authors/years/venue from memory; verify each (title, authors, year, venue, stable URL/DOI); prefer published over arXiv; no unqualified first/only/never/no-prior-work until a systematic search + per-item verification is complete; use qualified phrasing until then. Replacement only after ledger status reaches `VERIFIED`.

## 10. Appendix Plan

- **A. Proposition 1** — formal statement + full proof (mandatory; currently `HYPOTHESIS`).
- **B. Full cost/complexity** — token/GPU-hour/latency/VRAM tables (`[[TBD:PILOT_TOTAL_TOKEN_COST]]`, `[[TBD:MAIN_GPU_HOURS_PER_RUN]]`, `[[TBD:FULL_RIT_COST_MULTIPLIER]]`, …).
- **C. Extra sensitivity** — `K∈{1,3,5,10}`, `p∈{1,2,5,10}%`, `(α,β,γ)` grid, `top-k∈{2,4,8}`.
- **D. Design-choice justification table** — LOO-vs-Shapley, usage-behavior features, isotonic recalibration (rows with two empty columns are deleted).
- **E. A7 group/sampled-Shapley variant** (AS3 boundary fallback; H5).
- **F. Full Table 2** (reward substitution), **Fig 6** (case study), **Table 4** (hypotheses map), three-backbone/three-seed per-slice panels — demoted here to protect body page budget.
- **G. Judge–human agreement** (`[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]`), reproduction details.
- **Note:** AAAI content appendices count toward page limits and are subject to the same review; supplementary-material policy is `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`-dependent (confirm from the official call).

## 11. Evidence Gaps and Falsification Gates

**Falsification gates (kept honestly; do not hide negative results):**
- **Pilot / C1 gate:** `CCC > 0.5` **or** `SR@k` flat over `t` ⇒ attribution hypothesis falsified ⇒ narrow claim to heterogeneous streams.
- **H2 / C2 gate:** held-out `CCC` `ρ < 0.6` ⇒ C2 undercut.
- **A2 / C3 gate:** gain persists after swapping causal→co-occurrence ⇒ contribution not localized to the signal.
- **C4:** no significant avg gain under paired bootstrap ⇒ revise scope.

**Evidence gaps (no ledger ID — written as plain text, never a new placeholder):**
- Stream **S2–S4 identities** — `NOT SPECIFIED IN SOURCE`.
- H5 **injected-redundancy-ratio gain** — `EVIDENCE GAP` (no registered ID; exploratory; no new redundancy metric introduced).
- Fig 4 **`p`-sweep curve values** — `EVIDENCE GAP` (drawn from planned sensitivity runs; labeled `planned comparison`).
- Per-checkpoint A4 `SR@20%` values behind the H1 **slope** — `EVIDENCE GAP` beyond the registered `t=500` endpoints; slope is a derived read of Fig 5b, not a new cell.
- **Proposition 1** — unproven (`HYPOTHESIS`).
- **Cross-modality transfer** beyond text/agentic environments — `NOT SPECIFIED IN SOURCE`, flagged OPEN QUESTION, excluded from C1–C4.

**Placeholder lifecycle reminder:** any `[[TBD:...]]` may be replaced **only** after its ledger status reaches `VERIFIED`, with data path, script, metric definition, aggregation, unit, direction, reviewer, and date recorded, and a global consistency re-check. The same semantic quantity reuses the same ID across section/table/figure plans (234 registered IDs; none added or modified here).

## 12. Reviewer Feedback (Codex `gpt-5.6-sol`, `xhigh`)

Independent cross-review received on the full outline + evidence constraints; **no external style reference passed** (reviewer isolation preserved).

| Criterion | Score |
|---|---:|
| 1. Logical flow / story build | 8/10 |
| 2. Claim–evidence alignment | 7/10 |
| 3. Missing experiments/analysis (re-scope only) | 7/10 |
| 4. Positioning vs prior work | 5/10 |
| 5. Conditional page-budget feasibility | 6/10 |
| 6. Front-matter strength | 7/10 |
| 7. Placeholder discipline | 8/10 |
| 8. Second-story risk | 6/10 |

**Top-priority fixes flagged:** (i) rename formulation assumptions `AS1–AS3` (disambiguate from ablations `A1–A7`); (ii) parameterize `CCC(s,φ)` / `SR@k(s)` by ranking signal; (iii) align H1 to `SR@20%` **slope** and H4 to a body-level `p`-sweep; (iv) demote reward-swap to a **signal-portability check** nested under Mechanism/Ablation.

**Other minimum fixes:** hand-off paragraph from Pilot to Method; "ACA predicts the same φ" opener in §5; T5 cells re-expressed as `reported`/`not reported`/`unclear` (never "cannot"); "existing approaches **in our comparison** commonly use correlational signals"; reserve 15–18 body-pts for Ablation+Mechanism; move Table 4 / Fig 6 / full Table 2 appendix-first; Fig 1 right panel = "mechanism and testable prediction" with dashed prediction; "MERIT **is designed to** make it affordable"; abstract ends on planned-evidence + registered placeholder; one C3 bullet with governance/scope/reward as evaluations beneath; draft-wide rule "we test whether …" for outcome verbs; O(1) scope statement; mark H5 redundancy `EVIDENCE GAP`.

## 13. Review Integration Log

| # | Reviewer fix | Decision | Rationale / where applied |
|---|---|---|---|
| 1 | Rename assumptions `AS1–AS3` | **Adopt (pending user confirm)** | Label-only disambiguation of a real source collision; source mapping preserved (§5 map, §3). No scope/status change to C1–C4/H1–H5/Prop 1, so it does not trip the DRAFT_POLICY §12 gate; flagged for confirmation as it touches assumption symbols (DRAFT_POLICY §9). |
| 2 | Parameterize `CCC(s,φ)`, `SR@k(s)` | **Adopt** | §5 signal parameterization; makes Fig 2 (`s=Û`) vs Fig 5 (`s=φ̂`) rigorous. No new metric. |
| 3 | H1 = `SR@20%` slope; H4 = body `p`-sweep | **Adopt** | §5 H-map + §6.4/§6.7; slope read from Fig 5b (existing checkpoints), `p`-sweep from existing sensitivity runs — no new experiments; missing per-checkpoint values marked `EVIDENCE GAP`. |
| 4 | Reward-swap → "signal-portability check," nested, table appendix-first | **Adopt** | §6.5; kills the clearest second-story risk; Table 2 still listed (compact body summary + full appendix), satisfying "Table 1–6 not deleted." |
| 5 | Pilot hand-off paragraph + "introduces no second method" opener | **Adopt** | §4; ties pilot to method, prevents pilot-as-second-paper. |
| 6 | §5 opener "ACA predicts the same φ" | **Adopt** | §5; continuity of the diagnostic target. |
| 7 | T5 cells → `reported`/`not reported`/`unclear`; never "cannot" | **Partial-adopt** | Table row/column structure and ✓/✗/partial are **inherited** per guardrail §9 and marked verification-pending; the reviewer's re-expression is recorded as the drafting-time semantics for `/paper-write`, avoiding capability-claims. |
| 8 | "existing approaches in our comparison commonly use correlational signals" | **Adopt** | §1, §2; respects DRAFT_POLICY §8 priority-claim discipline. |
| 9 | Reserve 15–18 body-pts for Ablation+Mechanism; move Table 4 / Fig 6 / full Table 2 to appendix | **Partial-adopt** | Body budget note (§3) + appendix plan (§10 F). Nothing deleted (guardrail §8/§9): all 6 tables + 6 figures remain listed; only placement changes, which is a planning decision, not a §12 delete. |
| 10 | Fig 1 right panel "mechanism + testable prediction," dashed prediction | **Adopt** | Figure plan Fig 1; prevents planned effect reading as observed. |
| 11 | "MERIT is designed to make it affordable" | **Adopt** | §2 one-sentence contribution; design-scoped wording. |
| 12 | Abstract ends on planned-evidence + registered placeholder | **Adopt** | §0. |
| 13 | One C3 bullet; governance/scope/reward as evaluations | **Adopt** | §1 contribution bullets; enforces single-story. |
| 14 | Draft-wide "we test whether …" for outcome verbs | **Adopt** | Applies across §4–§6; matches DRAFT_POLICY §5. |
| 15 | O(1) precise scope statement | **Adopt** | §5.5. |
| 16 | Mark H5 high-redundancy `EVIDENCE GAP`; no new redundancy metric | **Adopt** | §5 H-map, §11; respects no-new-metric rule. |
| 17 | Rename Table 1 "RIT-Full upper bound" | **Partial-adopt** | Prose calls it "RIT-Full intervention reference" and a ceiling only by construction; the inherited **table row label is unchanged** per guardrail §9. |
| 18 | Benchmark→category & backbone-aggregation rules in T4 | **Adopt** | Table 4 columns; design metadata only, no data cells. |

**Rejected:** none outright. No reviewer suggestion required adding a model/dataset/baseline/metric/theorem or a new placeholder ID; all fixes are re-scoping, relabeling, or placement.

## 14. Acceptance Checklist

- [x] Only `paper/01_planning/PAPER_PLAN.md` written; no LaTeX/BibTeX/figures/MANIFEST/timestamped copies/root-level file created.
- [x] Working Title + One-sentence Contribution present.
- [x] Venue/Type/Evidence-State/Conditional Page Budget present; page limit kept as `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`; **neither 7 nor 9 pages assumed**.
- [x] Claims–Evidence Matrix C1–C4 (all `PLANNED-EVIDENCE`); Prop 1 `HYPOTHESIS`.
- [x] Hypotheses–Evidence Map H1–H5 (all `HYPOTHESIS`).
- [x] 7 body sections + Abstract; per-section goal/logic/claims/evidence/tables/figures/citations/proportion/appendix-movable.
- [x] Table Plan 1–6 all listed (none deleted); Table 1 rows/cols inherited; S2–S4 = `NOT SPECIFIED IN SOURCE`.
- [x] Figure Plan 1–6 all listed; **Fig 2 ↔ Fig 5 identical axes + stats** stated; Fig 3 drawable now.
- [x] Citation Plan uses only existing `[[TBD:CITATION_*]]`, all verification-pending; Table 5 cells verification-gated.
- [x] Appendix Plan (Prop 1 proof, cost, sensitivity, A7/group-Shapley, demoted artifacts).
- [x] Evidence Gaps & Falsification Gates present.
- [x] Reviewer Feedback (scores + fixes) + Review Integration Log present.
- [x] No new/altered placeholder IDs; gaps use `NOT SPECIFIED IN SOURCE` / `EVIDENCE GAP`.
- [x] No planned/hypothesis written as observed/proven; no unqualified first/only/never; no WebSearch/WebFetch used.
- [x] `source_proposal.md` SHA-256 unchanged (`MATCH`).

## 15. Next Steps (suggested; NOT executed — user approval gate per DRAFT_POLICY §11)

- [ ] User reviews and confirms this plan (required before any writing).
- [ ] Confirm AAAI 2027 track + page limit from the official call → resolve `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`.
- [ ] `/paper-figure` — Fig 3 (schematic, drawable now); other figures remain framed placeholders until data are `VERIFIED`.
- [ ] `/paper-write` — LaTeX skeleton on `aaai2027.sty`, applying the drafting-time rules recorded here (`natbib`, "we test whether …", `AS1–AS3`, one C3 bullet, dashed-prediction Fig 1).
- [ ] `/paper-compile` — at least one clean compile per stage.
- [ ] Bibliographic verification pass before any `[[TBD:CITATION_*]]` or Table 5 cell is resolved.

*Do not proceed past this plan without explicit user confirmation.*
