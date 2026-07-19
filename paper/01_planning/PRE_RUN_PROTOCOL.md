# Pre-Run Protocol — MERIT (AAAI 2027)

> **Purpose.** Resolve the open pre-run items left by
> `paper/reviews/ROUND1_REVISION_PLAN.md` into a concrete experimental protocol,
> **before any experiment is run**. For each open item this document gives a
> **recommendation + rationale + alternative(s)** and a status tag.
> **This run writes exactly one file** (`paper/01_planning/PRE_RUN_PROTOCOL.md`).
> No paper source, ledger, or revision plan is modified; no literature search, no
> experiment, no data backfill, no draft edits, no Round 2.
> **Evidence discipline still binds.** Every value below is a *protocol
> configuration*, never a result. No fabricated measurements. New ledger IDs are
> only **proposed** here (Section 6); creation requires ledger registration + user
> approval later.

## Status legend

- **`SOURCE-DEFAULT`** — derivable from `NARRATIVE_REPORT.md` / `source_proposal.md`
  (carried as the recommended default; still a provisional configuration).
- **`DESIGN-REC`** — a methodological best-practice recommendation not fixed by the
  source; recommended with rationale, but requires user sign-off before use
  (`USER_APPROVAL_REQUIRED` to *finalize*).
- **`USER_APPROVAL_REQUIRED`** — a fact or value **not derivable** from the source
  (e.g., dataset identities, thresholds absent from the proposal). Candidate options
  are listed, but none is asserted; the user must choose. **Not guessed.**

> Authority order unchanged: user → AAAI Author Kit → `DRAFT_POLICY.md` →
> `NARRATIVE_REPORT.md` → `source_proposal.md` → ARIS/Claude output.
> `source_proposal.md` integrity to preserve: SHA-256 `E700D46…96CC`.

---

## 1. Aggregation of $\Phi_i$ / $\widetilde{\Phi}_i$: population, weighting, minimum sample

Recall (from the revision plan): $\Phi_i=\mathbb{E}[\varphi_{i,t}]$ is the *true*
memory-level aggregate target; $\widetilde{\Phi}_i$ is its *finite RIT audit
estimate* with a confidence interval; SR@k is decided from the **CI of
$\widetilde{\Phi}_i$**, which is never called ground truth.

### 1.1 Audit population (the distribution $\Phi_i$ aggregates over)
- **Recommendation `DESIGN-REC`:** define $\Phi_i$ over the **retrieval-conditioned
  query distribution of $m_i$ on a frozen bank snapshot**, restricted to the
  common-support region (Section 3.2). I.e., aggregate the event-level
  $\varphi_{i,t}(q,C)$ over the audit events in which $m_i$ was actually retrieved,
  at fixed snapshot points $t\in\{100,200,300,400,500\}$ (`SOURCE-DEFAULT` snapshot
  grid).
- **Rationale:** the claim is "how much this memory contributes *when it is
  retrieved*," so conditioning on $m_i$'s realized retrieval events is the faithful
  estimand; a frozen snapshot removes the closed-loop feedback confound during the
  audit itself.
- **Alternatives:** (a) uniform over a fixed held-out query set (changes the
  estimand to "contribution if force-retrieved," decouples from retrieval
  frequency); (b) rolling window (tracks drift but conflates time with contribution).

### 1.2 Event weighting
- **Recommendation `DESIGN-REC`:** **uniform weight per audited retrieval event**
  within the snapshot window.
- **Rationale:** matches SR@k's "fraction of memories" semantics and prevents
  high-frequency memories from dominating their own aggregate; keeps $\Phi_i$
  interpretable as a mean effect per retrieval.
- **Alternatives:** retrieval-frequency weighting (weights deployment-relevant
  impact, but couples $\Phi_i$ to popularity); inverse-propensity weighting to
  correct common-support imbalance (more robust, more variance).

### 1.3 Per-memory sample size (two-stage fixed design with a strict timeline)
- **Recommendation `DESIGN-REC`:** a **two-stage fixed design** with an explicit
  timeline:
  - **Pre-pilot (substantive, data-free):** fix the equivalence band $\delta$
    (§3.2) and the minimal effect of interest MEI (§4.7) from substantive judgment,
    plus the pilot $K=5$, the sampling/split rules (§3.1/§3.4), the pilot budget
    (§3.7), and the neutral-pad candidate + validation rule (§3.6).
  - **Stage 1 (independent pilot, $K=5$):** estimate the variance of
    $\widetilde{\Phi}_i$ (and of AVG for §4.7) on a **separate pilot sample**.
  - **Stage 2 (post-pilot / pre-confirmatory):** **compute and freeze** the formal
    per-memory $n^{\text{audit}}$, the formal $K$, and the seed count from the
    independent pilot variance, so the target CI half-width is below the pre-fixed
    $\delta$ (and power $\ge$ target at the pre-fixed MEI). No adaptive stopping.
  - **Confirmatory run:** uses the frozen values on data **disjoint from the Stage-1
    pilot.**
- **Independence rule (hard):** **Stage-1 pilot data must not enter the final
  confirmatory gate estimates.** The pilot is used only to size $K$, $n^{\text{audit}}$,
  and seeds; reusing it in the gates would invalidate the frozen-design CIs.
- **Rationale:** separating the meaningfulness thresholds ($\delta$, MEI) — fixed
  before data — from the precision sizing ($K$, $n$, seeds) — computed from an
  independent pilot — avoids both optional-stopping bias and data-driven threshold
  selection.
- **`USER_APPROVAL_REQUIRED`:** the target CI half-width and target power used by the
  Stage-2 sizing formula (the frozen $K$, $n^{\text{audit}}$, and seed count are then
  *computed*, not guessed). Pre-pilot $\delta$ and MEI are covered in §3.2/§4.7.
- **Alternative:** stratified allocation (larger $n$ for high-variance strata),
  still frozen after Stage 1.

### 1.4 Two distinct credit–contribution correlations (do not conflate)
- **Event-level ACA fidelity:** $\mathrm{CCC}\big(\widehat{\varphi}_{i,t},\widetilde{\varphi}_{i,t}\big)$
  — Spearman correlation between the ACA prediction and the per-event RIT estimate,
  over audit events. This measures whether ACA reproduces the interventional label
  it was trained to predict.
- **Memory-level credit audit:** $\mathrm{CCC}\big(\coutil_i\ \text{or}\ \phibar_i,\ \widetilde{\Phi}_i\big)$
  — Spearman correlation between a memory-level signal (co-occurrence utility for the
  baseline, running credit $\phibar_i$ for MERIT) and the memory-level audit
  aggregate $\widetilde{\Phi}_i$. This measures whether the *ranking signal used by
  governance/retrieval* tracks the aggregated causal contribution.
- **Rationale:** the two answer different questions (per-event predictor accuracy vs
  memory-ranking validity) and must be reported separately; the diagnostic (G-C1)
  is memory-level on the baseline signal, ACA fidelity (G-C2) is event-level, and
  the memory-level MERIT variant is a complementary check.

---

## 2. Conjecture 1 — minimal assumption set (bias decomposition only; no proof this round)

$\varphi_i$ is **defined directly as the removal difference under the identical
context** (R1 estimand): $\varphi_{i,t}(q,C)=\mathbb{E}_\xi[r_t(C;\xi)-r_t(C\setminus\{i\};\xi)\mid H_t]$.
No additivity or no-interference assumption is imposed; higher-order memory
interactions are **out of scope of this decomposition and are handled separately by
AS3 (low-order interaction) and the A7 group intervention.**

Because $\varphi_i$ is a definitional difference, the decomposition
$$\mathbb{E}[r(C)\mid i\text{ retrieved}]=\underbrace{\mathbb{E}[r(C\setminus\{i\})\mid i\text{ retrieved}]}_{\text{leave-one-out baseline}}+\underbrace{\mathbb{E}[\varphi_i\mid i\text{ retrieved}]}_{\text{mean contribution}}$$
is an **identity** — it needs no assumption. Consequently $\coutil_i=\mathbb{E}[r(C)\mid i\text{ retrieved}]$
(Def. 2) **mixes** the leave-one-out baseline success with the mean contribution, and
differs from $\mathbb{E}[\varphi_i\mid i\text{ retrieved}]$ by exactly the
leave-one-out baseline term. **Whenever that baseline term is nonzero, $\coutil_i$ is
not a pure estimator of contribution** — this holds generically and does not require
any retrieval–solvability condition.

- **Recommended minimal set for the *bias* clause (`DESIGN-REC`):**
  - **(B1) Counterfactual decomposition identity.** The displayed decomposition
    above holds by definition of $\varphi_i$; no assumption is needed.
  - **(B2) Mixing / non-pure-estimator.** $\coutil_i$ mixes the leave-one-out
    baseline success and the mean contribution; whenever
    $\mathbb{E}[r(C\setminus\{i\})\mid i\text{ retrieved}]\neq 0$, $\coutil_i$ is not
    a pure estimator of $\mathbb{E}[\varphi_i\mid i\text{ retrieved}]$, with bias
    equal to that baseline term. **No additivity/SUTVA assumption is used (K1
    removed).**
  - **(Mechanism, not an assumption) Retrieval–solvability dependence.** If retrieval
    of $m_i$ is statistically dependent on the leave-one-out baseline success (the
    "easy-query free-riding" condition), this **amplifies and systematizes** the bias
    — it ties the baseline term to retrieval so superstition accumulates. It is
    **not** a necessary condition for the bias to exist or for the B1 identity to
    hold; it only governs the bias's magnitude and direction.
- **Additional model for the *equilibrium* clause (`DESIGN-REC`, informal only):**
  - **(B3) Monotone feedback + stationarity.** Retrieval rank is nondecreasing in the
    current utility estimate, the utility update is a consistent estimator of
    $\coutil$, and the task distribution is stationary — giving a fixed point where
    $\coutil_i>0$ while $\varphi_i=0$.
- **Decision:** commit **formally to B1–B2** (identity + mixing) this cycle; treat
  retrieval–solvability dependence as an amplifying mechanism and B3's dynamics as an
  informal feedback model. **No full proof is attempted this round** (approved
  decision). **B2 is not a user-decision item** — the mixing/non-pure-estimator claim
  follows from the B1 identity and requires no conditioning-form choice. **B3 remains
  informal** (decided; not a modeling commitment this cycle).
- **Alternative:** a signed-bias variant that additionally assumes a one-sided
  ("no anti-correlation") retrieval–solvability mechanism, if a directional
  superstition claim is wanted.

---

## 3. RIT audit protocol

### 3.1 Train/audit split and audit sampling design
- **Recommendation `DESIGN-REC`:** partition RIT-sampled events into a **TRAIN pool**
  (feeds ACA) and a disjoint **AUDIT pool** (feeds CCC / SR / gates), split at the
  **task level** (all events of a task go to one side) to prevent leakage across
  autocorrelated within-task events.
- **AUDIT sampling (design-based):** the AUDIT pool is drawn by **random or
  stratified-random sampling with known inclusion probabilities**, so
  $\widetilde{\Phi}_i$ and the memory-level CCC/SR admit **design-based (e.g.
  Horvitz–Thompson) unbiased estimation**. Priority/importance sampling (high
  uncertainty, high utility) is **restricted to the TRAIN pool only** and must not
  touch the AUDIT pool, or the audit estimates become biased.
- **Rationale:** fidelity and SR must be scored on labels ACA never trained on, and
  on a probability sample with known inclusion so the audit aggregate is unbiased;
  informative (priority) sampling is fine for training but would bias any audit
  statistic.
- **Alternatives:** **cross-fitting (k-fold at task level)** — rigorous, uses all
  data for honest held-out estimates; temporal split (later tasks = audit) —
  additionally probes drift. Both keep the AUDIT side probability-sampled.
- **`USER_APPROVAL_REQUIRED`:** the split fraction (or fold count $k$) and the AUDIT
  stratification design.

### 3.2 Equivalence region $\delta$ (SR / "practically null") — fixed **pre-pilot**
- **Recommendation `DESIGN-REC` + `USER_APPROVAL_REQUIRED` for the value:** $\delta$
  is the **minimum practically meaningful memory-level contribution**, a substantive
  effect-size judgment **fixed before the pilot runs**. It is **not** chosen from the
  pilot's noise floor — that would let the data set the meaningfulness threshold. The
  pilot variance is used only to size $K$/$n^{\text{audit}}$ so the CI half-width
  falls below this pre-fixed $\delta$ (Section 1.3). Classify a memory *harmful* if
  its CI is entirely below $-\delta$, *practically null* if its CI
  $\subseteq[-\delta,\delta]$, *positive* if entirely above $\delta$, and
  *undetermined* otherwise.
- **Rationale:** the equivalence band encodes what counts as a negligible
  contribution — a scientific commitment that must precede seeing any data; letting
  pilot noise pick $\delta$ conflates "meaningfully null" with "below our current
  precision."
- **Hard separation:** $\delta$ is **distinct from** the governance dead-zone
  $\pm0.02$ (`SOURCE-DEFAULT`, which stays a governance hyperparameter only) and from
  the Huber $\delta=0.1$ (`SOURCE-DEFAULT`, an ACA loss parameter). The three must
  not be conflated.
- **`USER_APPROVAL_REQUIRED`:** the numeric $\delta$ (a pre-pilot substantive
  choice).

### 3.3 CI method
- **Recommendation `DESIGN-REC`:** **task-clustered paired BCa bootstrap**,
  resampling at the task level and pairing each LOO comparison against its shared
  control; applied **once on the frozen Stage-2 sample** (no optional stopping).
- **Rationale:** streaming events are autocorrelated within a task, so iid intervals
  (Wilson/Clopper–Pearson) understate uncertainty; the paired, task-clustered BCa
  respects both the dependence and the paired LOO design, and a single pass on a
  frozen sample keeps the interval's coverage valid.
- **Alternatives:** Wilson/Clopper–Pearson (binary, ignores clustering — not
  recommended as primary); Bayesian credible intervals with a weakly-informative
  Beta prior (coherent small-sample behavior).

### 3.4 Number of memories sampled per trial + shared control
- **Recommendation `DESIGN-REC`:** sample a **subset** (1–2) of the retrieved
  memories per RIT trial and **share one full-set control** per sampled task across
  all its LOO comparisons, reusing the actually-observed deployment rollout as one
  control sample. **Priority (high-uncertainty / high-utility) subset selection is
  used for TRAIN trials only;** AUDIT-pool coverage of memories follows the
  random/stratified inclusion-probability design of Section 3.1 (never priority
  selection).
- **Rationale:** the reviewer showed all-$k$ ($k=4$) LOO with $K=5$ is ~1.2 extra
  rollout-equivalents per event — not "low overhead"; subset sampling + shared,
  reused controls roughly halves this while still covering every memory over time.
  Keeping priority selection out of the AUDIT pool preserves unbiased audit
  estimates.
- **`SOURCE-DEFAULT` baseline:** the proposal samples all $k$ retrieved memories;
  this is retained only as the high-cost reference (`RIT-Full`).
- **`USER_APPROVAL_REQUIRED`:** subset size per trial and the TRAIN-pool priority
  rule parameters.

### 3.5 Rollout count (two-stage fixed; no adaptive stopping)
- **Recommendation `DESIGN-REC`:** **two-stage fixed design.** Stage 1 uses $K=5$
  (`SOURCE-DEFAULT`) on an independent pilot to estimate variance; Stage 2 **computes
  and freezes a single formal $K$** (together with $n^{\text{audit}}$) so the CI
  half-width meets the **pre-pilot** $\delta$ (§3.2). $\delta$ is not set here — it is
  fixed before the pilot. **No adaptive or sequential stopping**, and **pilot data do
  not enter the confirmatory gates** (§1.3).
- **Rationale:** a frozen rollout budget removes optional-stopping bias and makes the
  Stage-2 CI valid; the pilot sizes the budget once against a pre-fixed threshold.
- **Alternative:** keep $K=5$ throughout if the Stage-1 variance is already small
  enough relative to the pre-fixed $\delta$.
- **Note:** the frozen formal $K$ is *computed* from the Stage-1 pilot (§1.3), not a
  free parameter.

### 3.6 Neutral-padding validation
- **Recommendation `DESIGN-REC`:** on a validation subset, compare LOO-with-neutral-pad
  against literal removal (empty slot); accept the pad iff the CI of (pad $-$
  removal) lies within a pre-stated equivalence band. Report the outcome as evidence
  (proposed ID `PILOT_NEUTRAL_PAD_VALIDATION`, Section 6).
- **Rationale:** the filler estimates "replacement-by-filler," not literal removal,
  unless neutrality is demonstrated; this converts an assumption into a check.
- **`USER_APPROVAL_REQUIRED`:** the pad **content** (what neutral text/token block is
  inserted) and the acceptance band — neither is derivable from the source.

### 3.7 Cost formula (rollout/token budgeting)
- **Recommendation `DESIGN-REC`:** budget RIT in **rollout-equivalents per
  deployment event**, not task probability. Symbolic form:
  $$\text{cost}_{\text{per event}} \approx p_{\text{task}}\cdot\frac{m\cdot K + K_{\text{ctrl}} - r_{\text{reuse}}}{E_{\text{task}}},$$
  where $m$ = memories sampled per trial (3.4), $K$ = the **frozen formal** rollouts
  per LOO (3.5, two-stage fixed), $K_{\text{ctrl}}$ = shared control rollouts,
  $r_{\text{reuse}}$ = reused deployment rollouts, $E_{\text{task}}$ = retrieval
  events per task, $p_{\text{task}}$ = trial-sampling rate (`SOURCE-DEFAULT` $5\%$).
  Report the realized value as proposed ID `RIT_ROLLOUT_EQUIV_PER_EVENT` (Section 6).
- **Rationale:** makes the affordability claim falsifiable by a formula + one
  measured number instead of the phrase "low overhead."
- **`USER_APPROVAL_REQUIRED`:** the target budget ceiling
  ($\varepsilon = \tbd{RIT_BUDGET_EPSILON_PERCENT}$ is the ledger slot for it).

---

## 4. Experiment population and statistics

### 4.1 Stream identities S1–S5 and construction
- **`SOURCE-DEFAULT`:** **S1 = single-domain ALFWorld**; **S5 = mixed** (most
  heterogeneous). Streams ordered by increasing heterogeneity via the Evo-Memory
  mixed-stream protocol.
- **`USER_APPROVAL_REQUIRED`:** **S2, S3, S4 identities are `NOT SPECIFIED IN
  SOURCE`** — must be chosen by the user, not guessed. (Candidate axis only: intermediate
  mixtures between S1 and S5; the specific domain compositions are undetermined.)
- **Heterogeneity index `DESIGN-REC`:** Shannon entropy of the per-stream domain-label
  distribution, used to order S1→S5 and as the x-axis of the H5 heterogeneity trend.
  **`USER_APPROVAL_REQUIRED`:** bin boundaries.

### 4.2 CTI
- **`SOURCE-DEFAULT`:** adopt the source §7 definition verbatim —
  $\mathrm{CTI}=\mathrm{Acc}_B(\text{B-only bank})-\mathrm{Acc}_B(\text{A}\cup\text{B mixed bank})$;
  $\mathrm{CTI}\ge0$ indicates interference; A/B pairs built along the Evo-Memory
  protocol.
- **`USER_APPROVAL_REQUIRED`:** the specific A/B domain pairs (not fully enumerated
  in the source).

### 4.3 AVG aggregation (two-stage macro-average) — **approved**
- **Approved decision:** **two-stage macro-average.** First aggregate the
  five Evo-Memory streams **S1–S5 into a single Evo-Memory category score** (equal
  weight across S1–S5); then take the **equal-weight average across the four
  benchmark categories** — Evo-Memory, WebArena-Lite, LongMemEval, LoCoMo. Report the
  per-category scores alongside the final AVG.
- **Rationale:** without the first stage the five Evo-Memory streams would outvote
  the three single-benchmark categories 5:1; two-stage macro-averaging gives each
  benchmark *category* equal say and matches the "four benchmark categories" framing.
- **Alternative:** micro-average (task-weighted) reported as a secondary number, if
  the community norm for these benchmarks is per-task.

### 4.4 Statistical unit and paired inference
- **Recommendation `DESIGN-REC`:** primary unit = **(stream × seed)**; compare
  methods with **hierarchical / blocked paired inference** (block = stream, pairing
  = seed), and within-stream use **task-clustered** paired bootstrap. Do not treat
  autocorrelated streaming tasks as iid.
- **Rationale:** the reviewer flagged that per-point bootstrap over streaming tasks
  can treat dependent tasks as independent; blocking by stream and pairing by seed
  respects the design.
- **`SOURCE-DEFAULT`:** seeds $\{13,42,2026\}$; paired bootstrap $10^4$ resamples.
- **`USER_APPROVAL_REQUIRED`:** whether 3 seeds suffice (see 4.7).

### 4.5 Comparison against the strongest baseline (no post-hoc selection)
- **Recommendation `DESIGN-REC`:** **do not select the strongest baseline from the
  test results.** The confirmatory main analysis is a **simultaneous max-baseline
  comparison**: test MERIT against the maximum over all baselines jointly (a
  step-down max-$T$ / min-$p$ contrast that accounts for the maximization), with
  **Holm correction** across the benchmark-category family.
- **Rationale:** picking the "best baseline" after seeing results invites a
  winner's-curse bias; a simultaneous comparison with Holm controls the family-wise
  error while still asking "does MERIT beat the best competitor?".
- **Alternative:** a single pre-registered comparator fixed before analysis (also
  bias-free, but less informative than the simultaneous contrast).
- **`USER_APPROVAL_REQUIRED`:** the exact max-baseline contrast statistic.

### 4.6 Multiplicity
- **Recommendation `DESIGN-REC`:** **Holm–Bonferroni (FWER)** for the confirmatory
  main analysis (the C1–C4 gates and the max-baseline comparison of §4.5);
  **Benjamini–Hochberg FDR is reserved for exploratory analyses only** (e.g., H5
  boundary sweeps, sensitivity grids).
- **Rationale:** confirmatory claims warrant strict family-wise error control;
  FDR's higher power is appropriate only where findings are explicitly exploratory.
- **`USER_APPROVAL_REQUIRED`:** the confirmatory $\alpha$ (FWER) and the exploratory
  $q$ (FDR).

### 4.7 Power analysis (MEI pre-pilot; seeds computed from an independent pilot)
- **Recommendation `DESIGN-REC`:** the minimal effect of interest **MEI on AVG is
  pre-registered before the pilot** (a substantive smallest-worthwhile effect, not
  read from pilot data). The **independent Stage-1 pilot** estimates AVG variance;
  the seed count (and any seeds added beyond the source default of 3) is then
  **computed and frozen** for power $\ge 0.8$ at the pre-fixed MEI. **Stage-1 pilot
  data are excluded from the confirmatory estimates** (§1.3).
- **Rationale:** 3 seeds may not support cross-backbone conclusions (reviewer
  MAJOR-1); fixing the MEI before data prevents a data-driven effect target, while
  the independent pilot supplies only the variance needed to size seeds.
- **`USER_APPROVAL_REQUIRED`:** the pre-pilot MEI on AVG and the target power (the
  seed count is then computed, not chosen).

### 4.8 Bank reset / warm-up
- **Recommendation `DESIGN-REC`:** each stream starts from an **empty bank (cold
  start)** with a **warm-up prefix of $W$ tasks excluded from scoring** (same $W$ for
  all methods) so every method reaches steady state before measurement.
- **Rationale:** MERIT's benefit is hypothesized to concentrate late in the stream;
  a shared, excluded warm-up prevents cold-start artifacts from confounding the
  comparison.
- **Alternative:** shared pre-seeded bank (removes the write-time confound but
  changes the "self-evolution from scratch" story).
- **`USER_APPROVAL_REQUIRED`:** the warm-up length $W$.

### 4.9 Pareto-knee criterion (H4)
- **Recommendation `DESIGN-REC`:** define the knee operationally as the smallest RIT
  budget at which the **marginal AVG gain per doubling of relative token cost falls
  below a threshold $\tau_{\text{knee}}$**; report the budget–AVG curve so the knee is
  auditable.
- **Rationale:** "Pareto knee" is otherwise subjective; a marginal-gain rule makes
  H4 falsifiable.
- **Alternative:** maximum-curvature (Kneedle) point on the budget–AVG curve.
- **`USER_APPROVAL_REQUIRED`:** $\tau_{\text{knee}}$ (or the Kneedle sensitivity).

---

## 5. Table 4 — explicit rule per atomic falsification gate

Each row: **estimand · comparator · audit population · decision rule · failure
action.** Thresholds marked `SOURCE-DEFAULT` are from the proposal; others are
`USER_APPROVAL_REQUIRED` and must be locked before running.

| Gate | Estimand | Comparator | Audit population | Decision rule | Failure action |
|---|---|---|---|---|---|
| **G-C1** baseline superstition | slope of $\mathrm{SR@}20\%(\coutil)$ over $t$; **memory-level** $\mathrm{CCC}(\coutil_i,\widetilde{\Phi}_i)$ | baseline banks (ReasoningBank-, MemRL-style) | pilot AUDIT pool (probability sample), snapshot grid | slope CI **excludes 0** (rises) **and** memory-level CCC below bound `USER_APPROVAL_REQUIRED` (source names $\mathrm{CCC}>0.5$ as the *falsifier*) | narrow C1 to heterogeneous streams |
| **G-C2** ACA fidelity | **event-level** $\mathrm{CCC}(\widehat{\varphi}_{i,t},\widetilde{\varphi}_{i,t})$ (primary); **memory-level** $\mathrm{CCC}(\phibar_i,\widetilde{\Phi}_i)$ (complementary) | correlational baseline | held-out AUDIT pool | event-level $\rho \ge 0.6$ (`SOURCE-DEFAULT` gate) with CI rule `USER_APPROVAL_REQUIRED` | C2 unsupported / revise |
| **G-C3a** governance flattens SR | Full-vs-A4 $\mathrm{SR@}20\%$ **slope** difference | A4 (no governance) | mechanism audit, checkpoints | slope-difference CI excludes 0 (Full flatter), Holm-adjusted | drop governance-flattening claim |
| **G-C3b** scope reduces interference | $\mathrm{CTI}$ (§4.2) with vs without scope gating | A3 (no scope) | A/B mixed-stream audit | $\mathrm{CTI}$ reduction CI excludes 0, Holm-adjusted | drop interference claim |
| **G-C3c** reward portability | AVG lift from $\widehat{\varphi}$-reward substitution | manager's original reward | reward-swap runs | lift CI excludes 0 at threshold `USER_APPROVAL_REQUIRED`, Holm-adjusted | report as null portability |
| **G-C4** end-task superiority | AVG gain over the **simultaneous max** of all baselines (§4.5) | max-baseline contrast | main runs, two-stage macro-AVG (§4.3) | MERIT $>$ max-baseline, **Holm-corrected** (§4.6); CI excludes 0 | report parity |
| **G-H4** efficiency | Pareto knee (§4.9) | budget sweep | efficiency runs | knee exists per $\tau_{\text{knee}}$ rule | drop Pareto claim |
| **G-H5** boundaries | directional gain vs bank size / heterogeneity / redundancy | within-axis | boundary runs | each axis's predicted sign holds (CI); **redundancy axis stays `EVIDENCE GAP`** (no ledger ID) | scope H5 to axes that pass |

**Pre-experiment locks (phased by the two-stage timeline):**

- **Pre-pilot (fix before the pilot runs):** $\delta$ (§3.2), MEI on AVG (§4.7),
  pilot $K=5$ (§3.5), the AUDIT random/stratified sampling + train/audit split rules
  (§3.1), the per-trial memory-subset rule (§3.4), the pilot budget (§3.7), and the
  neutral-pad candidate + validation rule (§3.6).
- **Post-pilot / pre-confirmatory (computed from the independent pilot variance,
  then frozen):** formal $K$, $n^{\text{audit}}$, and seed count (§1.3/§3.5/§4.7).
- **Pre-confirmatory design registrations (independent of the pilot):** S2–S4
  identities + heterogeneity bins (§4.1), CTI A/B pairs (§4.2), two-stage macro-AVG
  (§4.3, approved), statistical unit + inference (§4.4), max-baseline contrast
  (§4.5), multiplicity levels (§4.6), warm-up $W$ (§4.8), Pareto-knee criterion
  (§4.9), per-gate CI/threshold rules (this table), and the RIT budget ceiling
  $\varepsilon$ (§3.7).
- **Hard independence rule:** the Stage-1 pilot data are **excluded from all
  confirmatory gate estimates** (§1.3).

---

## 6. Placeholder inventory (proposed to add vs reuse) — **not created this round**

Creation of any new ID requires ledger registration + user approval (a separate,
authorized step). Nothing below is written into the paper or the ledger now.

### 6.1 Proposed new IDs (candidates)
| Candidate ID | Category | Feeds | Note |
|---|---|---|---|
| `RIT_ROLLOUT_EQUIV_PER_EVENT` | efficiency/cost | §3.7 cost formula output | distinct from `RIT_TOKEN_OVERHEAD_PERCENT` |
| `PILOT_NEUTRAL_PAD_VALIDATION` | pilot | §3.6 pad-neutrality check | new evidence quantity |
| `PILOT_AUDIT_SUPPORT_COVERAGE` | pilot | §3.1/§1.1 common-support coverage | coverage metric |
| `PILOT_SR20_CI_T100`, `PILOT_SR20_CI_T500` | pilot | §3.2 SR uncertainty bands | or fold into existing SR IDs as point±CI |
| `PILOT_SR20_HARMFUL_T{100,500}` | pilot | §3.2 harmful subset | MAJOR-3 three-way split |
| `PILOT_SR20_NULL_T{100,500}` | pilot | §3.2 practically-null subset | MAJOR-3 |
| `PILOT_SR20_REDUNDANT_T{100,500}` | pilot | §3.2 redundant subset | ties to A7; may stay `EVIDENCE GAP` |

### 6.2 Reused existing IDs (no new ID needed)
- `RIT_BUDGET_EPSILON_PERCENT` — RIT budget ceiling (§3.7).
- `RIT_SAMPLING_PROB_PERCENT` — trial-sampling rate $p_{\text{task}}$ (§3.4).
- `PILOT_SPLITHALF_PHI_RELIABILITY` — audit reliability (§3.1).
- `ACA_HELDOUT_CCC_T500` — audit-split CCC for G-C2 (§5).
- `PILOT_CCC_REASONINGBANK_T500`, `PILOT_CCC_MEMRL_T500`, `PILOT_SR20_T100`,
  `PILOT_SR20_T500` — baseline diagnostic for G-C1 (§5).
- `SR_MERIT_T500`, `SR_REDUCTION_MERIT_T500_PERCENT` — mechanism recovery.
- `ABL_A2_*` — **reused** for the capacity-matched observational-supervision control
  (approved decision; ledger *description* to be updated later, values unchanged).
- Efficiency IDs (`EFF_*`, `MERIT_RELATIVE_TOKEN_COST`, `RITFULL_RELATIVE_TOKEN_COST`,
  `FULL_RIT_COST_MULTIPLIER`) — G-H4.
- `AAAI2027_TRACK_PAGE_LIMIT` — venue metadata (unchanged).

### 6.3 Explicitly no-new-ID
- **A2** matched control reuses `ABL_A2_*` (approved decision 4) — no new row/ID.
- **Redundancy** boundary axis remains plain-text `EVIDENCE GAP` — no ID.

---

## Consolidated `USER_APPROVAL_REQUIRED` (grouped by the two-stage timeline)

**Pre-pilot (substantive, fixed before the pilot; data-free):**
1. $\delta$ = minimum practically meaningful memory-level contribution (§3.2).
2. MEI on AVG + target power (§4.7).
3. Target CI half-width used by the Stage-2 sizing formula (§1.3).
4. Train/audit split fraction (or fold count $k$) + AUDIT stratification design (§3.1).
5. Per-trial memory-subset size + **TRAIN-pool** priority-rule parameters (§3.4).
6. Neutral-pad content + acceptance band (§3.6).
7. RIT budget ceiling $\varepsilon$ / pilot budget (§3.7 / `RIT_BUDGET_EPSILON_PERCENT`).

**Pre-confirmatory design registrations (independent of the pilot):**
8. **S2–S4 stream identities** and heterogeneity bin boundaries (§4.1) — `NOT SPECIFIED IN SOURCE`.
9. CTI A/B domain pairs (§4.2).
10. The simultaneous max-baseline contrast statistic (§4.5).
11. Confirmatory $\alpha$ (Holm) and exploratory $q$ (BH-FDR) levels (§4.6).
12. Warm-up length $W$ (§4.8).
13. Pareto-knee threshold $\tau_{\text{knee}}$ (§4.9).
14. Per-gate CI/threshold rules left open in the Table-4 gate rows (§5).

**Post-pilot (computed, not chosen — listed for transparency):**
15. Formal $K$, $n^{\text{audit}}$, and seed count are **computed** from the independent Stage-1 pilot variance and frozen (§1.3/§3.5/§4.7); only the sizing criteria (items 2–3) require approval, not these values.

**Other:**
16. Which proposed placeholders (§6.1) to register, and SR-uncertainty as one cell (point±CI) vs separate IDs.

> **Closed by approval (no longer open):** two-stage macro-AVG (§4.3); B2 mixing is
> not a conditioning-form decision and B3 stays informal (§2).

---

**Status: pre-run protocol complete. Only `paper/01_planning/PRE_RUN_PROTOCOL.md`
written. No paper source, ledger, or revision plan modified; no literature search,
experiment, data backfill, draft edit, or Round 2 initiated. Stopping.**
