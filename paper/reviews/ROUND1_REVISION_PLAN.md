# ROUND 1 Revision Plan — MERIT (AAAI 2027)

> **Purpose:** Turn the approved Round-1 pre-run review directions
> (`paper/reviews/PAPER_IMPROVEMENT_LOG.md`) into a concrete, file-level revision
> plan. **This is a plan only.**
> **This run writes exactly one file** (`paper/reviews/ROUND1_REVISION_PLAN.md`).
> No paper source/table/figure/bib/ledger is modified; no literature search, no
> experiment, no data backfill, no Round 2.
> **Authority order unchanged:** user instructions → AAAI Author Kit →
> `DRAFT_POLICY.md` → `NARRATIVE_REPORT.md` → `source_proposal.md` → ARIS/Claude
> output.
> **Evidence discipline still binds every future edit:** C1–C4 stay
> `PLANNED-EVIDENCE`; no fabricated numbers; only registered ledger IDs may enter
> the paper; new IDs require ledger registration + user approval **before** use.

## Legend

- **`USER_DECISION_REQUIRED`** — a parameter/scope choice not determinable from
  existing material (narrative, source, ledger, plan). Left open; not decided here.
- **`PROPOSED-PLACEHOLDER`** — a ledger ID that a fix *may* need. **Candidate name
  only; NOT created this round.** Requires ledger registration + user approval
  before it can appear in the paper.
- **`§12-CHANGE-CONTROL`** — per `DRAFT_POLICY.md` §12, this edit changes the
  scope/definition of a claim, hypothesis, table, main figure, or method element
  and must get explicit user sign-off in the fix round before implementation.
- **Work class** — `SPEC` (formal/spec rewrite, no new runs) · `REANALYSIS`
  (recompute from already-planned runs) · `NEW-RUN` (needs additional runs on
  existing datasets) · `NEW-DATA` (needs new intervention data). No class creates
  new datasets/benchmarks/backbones.

## Approved decisions applied in this revision

The user approved six decisions; they are now baked into this plan (previously open
`USER_DECISION_REQUIRED` items that they resolve have been closed):

1. **Aggregate target vs finite estimate are separated.** $\Phi_i=\mathbb{E}[\varphi_{i,t}]$
   is the *true* memory-level aggregate target; $\widetilde{\Phi}_i$ is its *finite
   RIT audit estimate*. SR@k is decided from the **confidence interval of
   $\widetilde{\Phi}_i$**, and $\widetilde{\Phi}_i$ is **not** called ground truth.
2. **Conjecture 1 stays unproven this round** — plan the rigorous bias
   decomposition only; do **not** attempt a full proof.
3. **C1 scope fixed to the evaluated memory systems and task streams** — no new
   prevalence experiment (`REANALYSIS`, not `NEW-RUN`).
4. **A2 is replaced** by a capacity-matched *observational-supervision* control
   (swapping the old raw-co-occurrence A2); **reuse existing `ABL_A2_*`**, add no
   A2 row and no new A2 placeholder.
5. **Table 1 stays the main-results table**; the method-positioning table's
   `\input` moves later so it **naturally becomes Table 5**.
6. **Still pending pre-run protocol (not guessed here):** equivalence half-width
   $\delta$, audit-split design, S2–S4 stream identities, CTI definition, and the
   statistical rules. These remain flagged, not decided.

---

## R1 — Separate φ / φ̃ / φ̂ / φ̄; scope to *immediate retrieval contribution*

**Review basis:** CRITICAL-1 (estimand & notation conflation).

**Target state.** Four distinct quantities, four distinct symbols, one explicit
estimand:

| Concept | New symbol | Macro (proposed) | Meaning |
|---|---|---|---|
| True immediate contribution (event) | $\varphi_{i,t}(q,C)$ | keep `\phicf` (`\varphi`) | interventional, time/state/history-conditioned |
| RIT finite-rollout estimate (event) | $\widetilde{\varphi}$ | **new** `\phirit` (`\widetilde{\varphi}`) | $K$-rollout Monte-Carlo label |
| ACA prediction (event) | $\widehat{\varphi}$ | keep `\phihat`, **restrict to ACA only** | amortized regressor output |
| Online running aggregate | $\bar{\varphi}$ | keep `\phibar` | EMA of $\widehat{\varphi}$ used by governance |
| **True memory-level aggregate target (estimand)** | $\Phi_i=\mathbb{E}[\varphi_{i,t}]$ | **new** `\phiagg` (`\Phi_i`) | population aggregate of the true immediate contribution over the audit distribution |
| **Finite RIT audit estimate of $\Phi_i$** | $\widetilde{\Phi}_i$ | **new** `\phiaggrit` (`\widetilde{\Phi}_i`) | audit-set estimate of $\Phi_i$ with a confidence interval; **not** ground truth |

**Estimand definition to add (§3).** Introduce outcome-with-context notation
$r_t(C;\xi)$ and
$\varphi_{i,t}(q,C)=\mathbb{E}_\xi\!\left[r_t(C;\xi)-r_t(C\setminus\{i\};\xi)\mid H_t\right]$,
with $H_t$ the deployment history/bank state. State once, prominently, that MERIT
targets **immediate retrieval contribution** (single retrieval event), not
long-horizon memory value. Per the approved direction, the long-horizon claim is
**dropped from scope** (not merely deferred); governance is justified as acting on
the running aggregate of immediate contributions, and any wording implying a
memory's multi-step value is removed.

**Memory-level SR@k definition to add (§4).** Distinguish the estimand from its
estimate. $\Phi_i=\mathbb{E}[\varphi_{i,t}]$ is the true aggregate target;
$\widetilde{\Phi}_i$ is its finite RIT audit estimate, formed over the audit
distribution over $(q,C)$ with a minimum per-memory sample count, an event
weighting, and a **confidence interval**. SR@k ranks by signal
$s\in\{\coutil,\widehat{\varphi}\}$ and classifies a memory's contribution from the
**CI of $\widetilde{\Phi}_i$** (see R3), not from a bare $\widetilde{\Phi}_i\le 0$
cut and **not** by treating $\widetilde{\Phi}_i$ as ground truth. Wording that calls
any finite estimate "true"/"ground-truth" contribution is removed.

**`USER_DECISION_REQUIRED`:** minimum per-memory audit sample count; event
weighting scheme (uniform vs recency vs retrieval-frequency); whether $\Phi_i$ is
defined on a frozen snapshot bank or a rolling window.

**`PROPOSED-PLACEHOLDER`** (not created): none for R1 — this is a `SPEC` change; it
relabels existing quantities and adds definitions. Existing pilot IDs
(`PILOT_CCC_*`, `PILOT_SR20_*`) keep their meaning but now reference $\Phi_i$ and
the signal-parameterized SR@k.

**Impact:** C1, C2, C3 statements re-worded (scope narrowed); H1–H3, H5 inherit the
sharper estimand. Definitions 1–2 in `03_problem_formulation.tex` rewritten.
`§12-CHANGE-CONTROL` (touches C1–C4 wording + Def 1).

---

## R2 — Downgrade Proposition 1 to a Conjecture / Mechanism Hypothesis

**Review basis:** CRITICAL-2 (Proposition not well posed).

**Target state.**

1. Rename the environment from **Proposition** to **Conjecture** (title
   "Mechanism Hypothesis 1"); add `\newtheorem{conjecture}{Conjecture}` in
   `main.tex` and retire the `proposition` environment (or keep it unused).
2. Restructure the statement in the order the reviewer requires:
   (a) define an **aggregate target** first (e.g. $\mathbb{E}[\varphi_i\mid i\text{ retrieved}]$);
   (b) give the **exact bias decomposition**
   $\mathbb{E}[r\mid i\text{ retrieved}]=\mathbb{E}[r^{(0)}\mid i\text{ retrieved}]+\mathbb{E}[\varphi_i\mid i\text{ retrieved}]$,
   showing the baseline-success term $r^{(0)}$ that survives even at zero
   covariance, so $\coutil$ is **not** an estimator of $\varphi$;
   (c) state **sufficient assumptions** explicitly;
   (d) specify the **feedback dynamics** (utility→retrieval-rank update rule, task
   distribution) for the superstition-equilibrium clause.
3. Soften all surrounding language: no theorem-style assertion; "we conjecture",
   "pending a formal statement and proof". Keep the formal proof slot in the
   appendix plan but label it "candidate proof of the conjecture".

**Decided (approved):** Conjecture 1 **stays unproven this round.** Plan only the
rigorous bias decomposition (aggregate target → exact decomposition → sufficient
assumptions → feedback dynamics); do **not** attempt a full proof this cycle. The
appendix proof slot remains a placeholder for a future cycle.

**`USER_DECISION_REQUIRED`:** the additive-model assumption set (which
independence/ignorability conditions to commit to for the decomposition) — this is
part of the pre-run protocol and is not guessed here.

**`PROPOSED-PLACEHOLDER`:** none (theory `SPEC`).

**Impact:** Proposition 1 → Conjecture 1 everywhere it is referenced (abstract note,
§3, §7, appendix plan, PAPER_PLAN cross-refs are out-of-scope this round but should
be reconciled later). C1's theoretical backing is reframed as a hypothesis, not a
result — consistent with its `PLANNED-EVIDENCE`/`HYPOTHESIS` status.
`§12-CHANGE-CONTROL` (changes Proposition 1 status/scope).

---

## R3 — Redesign RIT: audit split, common support, uncertainty, neutral padding, cost formula; ±0.02 governance-only

**Review basis:** CRITICAL-4 (label validity + affordability) and CRITICAL-1's SR
uncertainty.

**Target state (protocol spec added to §4 + §5.1; no runs this round).**

1. **Audit-only split.** Partition RIT samples into a **training pool** (feeds ACA)
   and a disjoint **audit pool** (feeds CCC/SR/gates), so fidelity is never scored
   on labels ACA trained on. Define the split rule and sizes.
2. **Common support.** Define the $(q,C)$ region over which interventions are
   comparable; restrict $\Phi_i$ and CCC/SR to memories/queries with adequate
   support; report coverage.
3. **Uncertainty-aware decision.** Replace the bare $\Phi_i\le 0$ SR cut with an
   **equivalence region** $[-\delta,\delta]$ and a confidence rule: classify a
   memory as *harmful*, *practically null*, or *positive* only when its interval
   excludes/includes the region. This also fixes the binary-$K{=}5$ granularity
   objection (0.2 increments vs a $\pm0.02$ cut).
4. **±0.02 is a governance hyperparameter only.** Decouple it from the SR
   ground-truth definition. It remains the eviction dead-zone in §5 governance;
   it must **not** appear as the SR "$\le 0$" threshold.
5. **Neutral-padding validation.** Add a validation step that the length-matched
   filler is neutral (removal-by-filler ≈ literal removal); report the validation
   outcome as evidence, not assumption.
6. **Explicit cost formula.** Budget RIT in **rollouts/tokens**, not task
   probability $p$. State the expected-cost formula, e.g. per sampled task
   $\text{cost}\approx (\,|\text{sampled memories}|\cdot K + K_{\text{ctrl}}\,)$
   rollout-equivalents, amortized by sampling frequency; allow sampling a **subset**
   of memories per trial, **shared controls**, and **adaptive repetitions** for
   near-zero cases. Replace "low overhead" prose with the formula + a to-be-measured
   figure.

**`USER_DECISION_REQUIRED`:**
- audit-split fraction and minimum audit sample count per memory;
- equivalence-region half-width $\delta$ for the SR/"practically null" test
  (distinct from the 0.02 governance dead-zone);
- confidence level / interval method for the uncertainty rule;
- per-trial memory-subset size, shared-control design, adaptive-repetition cap;
- the RIT budget expressed in rollouts/tokens (the source's $p=5\%$, $K=5$ are
  retained only as provisional defaults, not as the budget definition);
- neutral-pad construction (what the filler is) and its acceptance criterion.

**`PROPOSED-PLACEHOLDER`** (candidates, NOT created — need registration + approval):
| Candidate ID | For | Note |
|---|---|---|
| `RIT_ROLLOUT_EQUIV_PER_EVENT` | measured amortized cost per event | replaces vague "low overhead"; distinct from existing `RIT_TOKEN_OVERHEAD_PERCENT` |
| `PILOT_NEUTRAL_PAD_VALIDATION` | neutral-padding validation outcome | new evidence quantity |
| `PILOT_AUDIT_SUPPORT_COVERAGE` | fraction of memories with adequate common support | coverage metric |
| `PILOT_SR20_CI_T500` / `PILOT_SR20_CI_T100` | CI/width on SR@20% | if SR is reported with uncertainty bands |

Existing `PILOT_SPLITHALF_PHI_RELIABILITY` is reused for the audit reliability check.

**Impact:** C1 (SR/CCC definitions become uncertainty-aware), C2 ("held-out"
becomes the audit split), C4/H4 (efficiency claim now formula-backed). Work class:
mostly `SPEC`; the actual audit split + neutral-pad validation are `NEW-DATA`
within the already-planned RIT runs (no new datasets). `§12-CHANGE-CONTROL`
(changes SR definition and the efficiency claim basis).

---

## R4 — Replace Table 4 with atomic C1–C4 falsification gates; list pre-experiment locks

**Review basis:** CRITICAL-3 (gate map does not support "every claim has a gate").

**Target state.** Rebuild `tables/table4_hypotheses_map.tex` as **one row per atomic
claim**, each column-specified with: **estimand · comparator · audit population ·
threshold/CI rule · claim-narrowing action if failed**. Minimum atomic rows:

1. **G-C1 baseline superstition** (own row; currently missing): $\Phi$-based SR@k
   rises with $t$ on baseline banks; gate = slope CI excludes 0 and CCC below a
   stated bound; fail → narrow C1 to heterogeneous streams.
2. **G-C2 ACA fidelity**: audit-split CCC$(\widehat{\varphi},\varphi)\ge$ gate
   ($\rho\ge0.6$ from source, `USER_DECISION_REQUIRED` for CI rule); fail →
   C2 unsupported.
3. **G-C3a governance/SR** (was H1): Full-vs-A4 SR@20% slope difference; fail →
   drop governance-flattening claim.
4. **G-C3b scope/CTI** (split H3): CTI reduction under scope gating, **CTI defined
   first**; fail → drop interference claim.
5. **G-C3c reward portability** (currently no gate): substitution lift with a stated
   threshold; fail → present as null portability result.
6. **G-C4 end-task superiority** (currently no gate): AVG gain over the *defined*
   strongest baseline with a stated significance/CI rule; fail → report parity.
7. **G-H4 efficiency**: Pareto-knee **criterion defined** (not just "knee");
   fail → drop Pareto claim.
8. **G-H5 boundaries**: each boundary axis given a directional prediction + test;
   redundancy axis stays `EVIDENCE GAP` (no ledger ID).

**Pre-experiment locks to enumerate in the plan/table notes (must be fixed before
any run):** stream identities S1–S5 (S2–S4 currently unspecified), stream
construction + heterogeneity index, bank init/reset/warm-up policy, metric
normalization + macro-AVG definition, CTI definition, "strongest baseline"
selection rule, statistical unit (task vs block vs episode) + blocked/hierarchical
paired inference, multiplicity correction, and a seed-level power calculation.

**`USER_DECISION_REQUIRED`:** every locked item above (stream identities; CTI
formula; AVG aggregation; statistical unit; strongest-baseline rule; significance
level + multiplicity method; power-calc target effect size; Pareto-knee criterion;
per-gate CI rule).

**`PROPOSED-PLACEHOLDER`:** Table 4 remains **design-metadata only (no result
cells)**, so no new result IDs. If the pre-experiment locks introduce a reported
"strongest-baseline identity" or "heterogeneity index value", those are design
declarations, not ledger results.

**Impact:** All of C1–C4 and H1–H5 get an explicit, atomic gate; the paper's
"every claim has a falsification gate" statement becomes true. Work class: `SPEC`
(table + protocol text). `§12-CHANGE-CONTROL` (restructures Table 4 + claim/gate
mapping; adds a C1 gate row).

---

## R5 — A2: matched control (same ACA architecture, only the supervision label swapped)

**Review basis:** MAJOR-2 (A2 confounds interventional labels with model capacity).

**Target state.** Redefine ablation **A2** from "raw co-occurrence utility" to a
**capacity-matched supervision control**: identical ACA architecture, identical
feature groups, identical update schedule and compute budget, **only the training
label swapped** from the interventional RIT label $\widetilde{\varphi}$ to a matched
**observational/outcome label**. Both signals are evaluated on the **shared, fixed
audit set**. This isolates the value of *interventional supervision* from model
capacity. Also rename the "credit fidelity → SR/CTI → AVG" description from "causal
chain" to "**mechanism-consistent sequence**" unless formal mediation is added
(mediation is out of scope this cycle).

**Decided (approved):** A2 is **replaced** — the old raw-co-occurrence A2 is dropped
and A2 now denotes the capacity-matched observational-supervision control. The raw
co-occurrence comparison remains represented by the co-occurrence baseline already
present in Table 1 / Table 6, so it is not lost. The existing **`ABL_A2_*` ledger
IDs are reused** (their row now carries the matched-control semantics); no A2 row is
added and no new A2 placeholder is created.

**`PROPOSED-PLACEHOLDER`:** none for A2 (IDs reused, semantics redefined). The
redefinition is recorded so the ledger's human-readable description for `ABL_A2_*`
is later updated (a metadata note, not a value change).

**Impact:** C3 (signal-localization argument becomes sound); Table 3 row A2
semantics change (same `ABL_A2_*` cells, new meaning); §5 governance rationale text
updates ("A2 isolates the signal" → "A2 isolates interventional supervision at
matched capacity"). Work class: `NEW-RUN` (one matched-control training run on
existing data). `§12-CHANGE-CONTROL` (changes an ablation's definition; no new
row, no new ID).

---

## R6 — Algorithm 1 state/complexity, C1 scope, natural float numbering

**Review basis:** MAJOR-4 (Algorithm not self-contained), MAJOR-5 (C1 over-broad),
MINOR (manual counter resets), Visual-review (float order).

**R6a — Algorithm 1 (`05_method.tex`).**
- Replace "only eight objects" with a full **state list**: label pool (split into
  train/audit per R3), current trajectory, per-memory counts $n_i$, prototypes
  $\text{proto}^{\pm}_i$, quarantine status, and calibration state.
- Add an **initialization / warm-up** paragraph (cold-start behavior before the
  first recalibration).
- State that quarantine's **UCB bonus is forced exploration, separate from ranking**
  (not a ranking term).
- Clarify **merge semantics**: merged content is inherited/fixed from the baseline
  writer; only the merge *trigger* is credit-based — reconciling with the
  "write-time quality out of scope" statement.
- Add a **feature mask / fallback** for backbones without token log-probabilities
  (the closed-source row), so the usage-behavior feature group degrades gracefully.
- Change complexity wording from unqualified **$O(1)$** to **$O(kd)$ per query /
  $O(d)$ per retrieved-memory event** at fixed feature dimension $d$; keep "RIT
  collection + recalibration accounted separately".

**R6b — C1 scope (`00_abstract.tex`, `01_introduction.tex`, `04_pilot_diagnostic.tex`).**
- Scope C1 to the **evaluated memory systems and task streams**; do not assert that
  "current systems" in general breed superstition from a 2-system/2-stream
  diagnostic. Distinguish **passive co-occurrence counting** from **outcome-reward
  RL under exploration** (the latter is not "correlational" in the same sense).
- **Decided (approved):** keep the narrow, existence-scoped C1 — **no new
  prevalence experiment.** Work class `REANALYSIS` only; no broadening run on the
  planned main streams.

**R6c — Natural float numbering (`06_experiments_analysis.tex`, all `tables/*`,
`figures/placeholders/*`).**
- Remove every manual `\setcounter{table}{N}` / `\setcounter{figure}{N}` and let
  natural LaTeX numbering apply.
- **Decided (approved):** **Table 1 stays the main-results table.** The
  method-positioning table's `\input` **moves out of §2** to a later point (in §6,
  after the main/reward/ablation/hypothesis tables) so that it **naturally becomes
  Table 5.** In §2 Related Work, replace the in-place `\input` with a forward
  reference (`Table~\ref{tab:method-positioning}`) to the later float.
- Resulting natural order: Fig 1 (§1) → Fig 2 (§4) → Fig 3 (§5) → Table 1 (main) →
  Table 2 (reward) → Table 3 (ablation) → Table 4 (gates) → Fig 4 → Fig 5 →
  Table 5 (positioning) → Table 6 (efficiency) → Fig 6 (§6). (Exact float landing
  pages are set by LaTeX; the numeric order is what is fixed.)
- **Consequence to flag:** labels keep working via `\ref`, and the *displayed
  numbers* now follow reading order. All in-prose references already use `\ref{}` so
  they auto-update; **verify no caption or figure body contains a literal
  "Fig. 5"/"Table 4" string** (the fig2/fig5 placeholders already use
  `Fig.~\ref{...}` — confirm none use literal numbers).

**`PROPOSED-PLACEHOLDER`:** none (all `SPEC`/presentation).

**Impact:** C2 (complexity honesty), C1 (scope), presentation only for numbering.
`§12-CHANGE-CONTROL` applies to the C1-scope wording; the Algorithm/state and
numbering fixes are non-scope `SPEC` but still logged.

---

## R7 — Per-file change list · claim/hypothesis impact · proposed placeholders

### R7a — Per-file change list (what each future edit touches; not executed now)

| File | Planned change | Workstream | §12? |
|---|---|---|---|
| `main.tex` | add `\newtheorem{conjecture}{Conjecture}`; retire `proposition` env | R2 | yes |
| `math_commands.tex` | add `\phirit` ($\widetilde{\varphi}$), `\phiagg` ($\Phi_i$, true target), `\phiaggrit` ($\widetilde{\Phi}_i$, finite audit estimate); comment-restrict `\phihat` to ACA | R1 | yes (notation) |
| `sections/00_abstract.tex` | scope C1 to evaluated families; keep "designed to"; align headline gate wording | R6b | yes |
| `sections/01_introduction.tex` | C1 scope + passive-vs-RL distinction; soften "produces causal labels at low budget"; drop defensive meta-language | R6b, MINOR | yes |
| `sections/02_related_work.tex` | move the method-positioning table `\input` out to §6 and replace with a forward `Table~\ref{tab:method-positioning}`; (optional) add reviewer's missing families as positioning prose; avoid equating outcome-reward RL with correlational counting | R6c, R7c/positioning | no (no new claims) |
| `sections/03_problem_formulation.tex` | rewrite Def 1 as time/state-conditioned estimand; add $\Phi_i$/aggregation; Def 2 clarified; Proposition→Conjecture with bias decomposition + dynamics; "semantic retrieval **can** induce … under pilot conditions" | R1, R2 | yes |
| `sections/04_pilot_diagnostic.tex` | define $\Phi_i$ (target) vs $\widetilde{\Phi}_i$ (finite estimate); SR from the CI of $\widetilde{\Phi}_i$ (not ground truth); audit split; common support; equivalence region; neutral-pad validation; RIT cost formula; SR split into harmful/null/redundant; use $\widetilde{\varphi}$ for event labels; scope C1 to evaluated systems/streams | R1, R3, R6b, MAJOR-3 | yes |
| `sections/05_method.tex` | $\widetilde{\varphi}$ (RIT label) vs $\widehat{\varphi}$ (ACA) split; Algorithm 1 state/init/complexity; merge/feature-mask clarifications; ±0.02 governance-only; "architecturally linear" not "verified linear chain" | R1, R3, R6a | yes |
| `sections/06_experiments_analysis.tex` | A2 redefinition (reuse `ABL_A2_*`); "mechanism-consistent sequence"; drop `\setcounter` and add the positioning-table `\input` here so it becomes Table 5; lock-list prose; efficiency claim → formula-backed | R4, R5, R6c | yes |
| `sections/07_limitations_conclusion.tex` | drop long-horizon-value implication; add estimand-scope + RL-vs-correlational nuance to limitations | R1, R6b | yes |
| `tables/table3_ablation.tex` | relabel the A2 row to the capacity-matched observational-supervision control, reusing the existing `ABL_A2_*` cells; no new row | R5 | yes |
| `tables/table4_hypotheses_map.tex` | full rebuild → atomic C1–C4 gates (estimand/comparator/population/threshold/action) | R4 | yes |
| `tables/table1,2,3,5,6 + figures/*` | remove `\setcounter` resets; verify no literal float numbers in captions/bodies | R6c | no |
| `figures/placeholders/fig2,fig5*` | ensure axis captions reference $\Phi_i$ / signal-parameterized SR; keep locked-axes note | R1 | no |

> Note: `PAPER_PLAN.md`, `PLACEHOLDER_LEDGER.md`, `references.bib` are **not** in this
> plan's edit set. Ledger edits (to register any `PROPOSED-PLACEHOLDER`) are a
> separate, user-approved step; `PAPER_PLAN.md` reconciliation (Conjecture rename,
> atomic gates) should be scheduled but is out of scope here.

### R7b — Impact on C1–C4 and H1–H5

| Item | Effect of the revision |
|---|---|
| **C1** | Scope narrowed to immediate contribution + evaluated families/streams; SR made uncertainty-aware and split into harmful/null/redundant; gains its own atomic gate G-C1. Status stays `PLANNED-EVIDENCE`. |
| **C2** | "Held-out" → audit split; target clarified as $\varphi$ estimated by $\widetilde{\varphi}$, predicted by $\widehat{\varphi}$; fidelity gate G-C2 with CI rule. Status unchanged. |
| **C3** | A2 becomes a capacity-matched supervision control (sound signal-localization); CTI defined; reward portability gets gate G-C3c; "two readouts of one signal" preserved. Status unchanged. |
| **C4** | Strongest-baseline gain, AVG aggregation, statistical unit, and Pareto-knee all locked with gates G-C4/G-H4; efficiency now formula-backed. Status unchanged. |
| **H1** | Re-anchored under C3 (governance) as G-C3a; measured as Full-vs-A4 SR slope with uncertainty. |
| **H2** | G-C2; audit-split CCC with CI rule instead of bare $\rho\ge0.6$. |
| **H3** | Split into scope/CTI (G-C3b) with a defined CTI, and transfer (kept under scaling). |
| **H4** | G-H4 with an explicit Pareto-knee criterion + RIT cost formula. |
| **H5** | Each boundary axis gets a directional test; redundancy axis stays `EVIDENCE GAP`; the three-way superstition split feeds the redundancy characterization. |
| **Conjecture 1** | Former Proposition 1; explicitly unproven; provides the bias-decomposition backbone for C1 without being a result. |

### R7c — Proposed placeholders (candidates only — **NOT created this round**)

Require ledger registration + user approval before any use. None are added to the
paper now.

| Candidate ID | Category | Motivating fix | Alternative |
|---|---|---|---|
| `RIT_ROLLOUT_EQUIV_PER_EVENT` | efficiency/cost | R3 cost formula output | reuse `RIT_TOKEN_OVERHEAD_PERCENT` if expressed as % |
| `PILOT_NEUTRAL_PAD_VALIDATION` | pilot | R3 neutral-padding validation | — |
| `PILOT_AUDIT_SUPPORT_COVERAGE` | pilot | R3 common-support coverage | — |
| `PILOT_SR20_CI_T100`, `PILOT_SR20_CI_T500` | pilot | R3 uncertainty bands on SR | fold into existing SR IDs if reported as point±CI in one cell |
| `PILOT_SR20_HARMFUL_T{100,500}` | pilot | MAJOR-3 harmful subset | — |
| `PILOT_SR20_NULL_T{100,500}` | pilot | MAJOR-3 practically-null subset | — |
| `PILOT_SR20_REDUNDANT_T{100,500}` | pilot | MAJOR-3 redundant subset | ties to A7; may stay `EVIDENCE GAP` |

> **A2 needs no new placeholder** — the redefinition reuses the existing `ABL_A2_*`
> cells (approved decision 4).

**Reused (no new ID):** `PILOT_SPLITHALF_PHI_RELIABILITY` (audit reliability),
`ACA_HELDOUT_CCC_T500` (now audit-split CCC), `RIT_TOKEN_OVERHEAD_PERCENT`,
`SR_MERIT_T500`, `SR_REDUCTION_MERIT_T500_PERCENT`.

---

## Consolidated `USER_DECISION_REQUIRED` (still open — pending pre-run protocol)

> Four earlier items are now **closed by the approved decisions** (no full proof
> this round · A2 replaced/reuse `ABL_A2_*` · C1 narrow, no new prevalence run ·
> Table 1 main + positioning table → Table 5). The remainder stay open and are
> **not guessed here**:

1. Memory-level aggregation of $\Phi_i$/$\widetilde{\Phi}_i$: min audit sample count; event weighting; snapshot vs rolling window (R1).
2. Conjecture 1 assumption set for the bias decomposition — the independence/ignorability conditions to commit to (R2; full proof deferred, not attempted this round).
3. RIT: audit-split design/fraction; equivalence-region $\delta$ (distinct from the 0.02 governance dead-zone); CI level/method; per-trial memory-subset size; shared-control design; adaptive-repetition cap; RIT budget in rollouts/tokens; neutral-pad construction + acceptance criterion (R3).
4. Pre-experiment locks: S2–S4 stream identities; stream construction + heterogeneity index; bank init/reset/warm-up; metric normalization + macro-AVG; CTI formula; strongest-baseline selection rule; statistical unit + paired-inference method; multiplicity correction; power-calc target effect; Pareto-knee criterion; per-gate CI rules (R4).
5. Which `PROPOSED-PLACEHOLDER`s to register, and whether SR-uncertainty is one cell (point±CI) or separate IDs (R7c).

## Change-control & sequencing (for the future fix round, not now)

- Every row marked `§12-CHANGE-CONTROL` needs explicit user sign-off before edit,
  because it alters C1–C4/H1–H5 scope, Proposition/Conjecture status, a table, a
  main figure, or an ablation definition (`DRAFT_POLICY.md` §12).
- Suggested order when authorized: **R1 notation/estimand → R2 conjecture →
  R3 RIT/SR → R4 gates/locks → R5 A2 → R6 algorithm/scope/numbering**, because R4's
  gates depend on R1/R3 definitions and R5's control depends on R1's label split.
- Frozen regardless: no fabricated numbers; result cells stay `\tbdcell{<registered ID>}`;
  no networked citation verification; `source_proposal.md` hash must stay
  `E700D46…96CC`; ledger edits only via a separate approved step.

## Acceptance criteria for the eventual fix round (definition of done)

- Symbols $\varphi,\widetilde{\varphi},\widehat{\varphi},\bar{\varphi}$ plus the aggregate target $\Phi_i=\mathbb{E}[\varphi_{i,t}]$ and its finite audit estimate $\widetilde{\Phi}_i$ used consistently across all files; no symbol denotes two things.
- Proposition 1 no longer appears; Conjecture 1 present with the bias decomposition + feedback dynamics and **explicitly unproven** (no full proof this round).
- SR@k decided from the **CI of $\widetilde{\Phi}_i$** (never called ground truth) relative to the target $\Phi_i$; ±0.02 appears only in governance.
- Table 4 has one atomic gate row per C1–C4 sub-claim; all pre-experiment locks enumerated ($\delta$, audit split, S2–S4, CTI, statistical rules stay flagged pending pre-run protocol).
- A2 is the capacity-matched observational-supervision control, **reusing `ABL_A2_*`** (no new row/ID); "causal chain" → "mechanism-consistent sequence".
- Algorithm 1 lists full state + init; complexity stated as $O(kd)$/$O(d)$; C1 scoped to the **evaluated memory systems and task streams** (no new prevalence run).
- Floats render in natural order with **Table 1 = main results** and the method-positioning table rendering as **Table 5**; no manual `\setcounter`; no literal float numbers in prose/captions.
- Placeholder audit: every result cell is a registered ID; any new ID was registered in the ledger with user approval before use; 0 unregistered IDs.
- Clean AAAI compile; page budget re-checked against `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`.

---

**Status: plan complete. No paper/table/figure/bib/ledger modified. No literature
search, experiment, data backfill, or Round 2 initiated. Stopping.**
