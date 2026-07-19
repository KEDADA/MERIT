# ROUND 2 Revision Plan — MERIT (AAAI 2027)

> **Purpose.** Turn the Round 2 review (`reviews/ROUND2_REVIEW.md`) and the
> detect-only kill-argument exercise (`reviews/KILL_ARGUMENT.md`) into a merged,
> de-duplicated, prioritized, file-level revision plan.
> **This run creates one file** (`reviews/ROUND2_REVISION_PLAN.md`). No ARIS skill
> is invoked; no paper source/table/figure/ledger/protocol is modified; no compile,
> no network, no experiments; not implemented.
> **Evidence discipline still binds every future edit:** C1–C4 stay
> `PLANNED-EVIDENCE`; no fabricated numbers; only ledger-registered placeholders may
> enter the paper; new IDs need ledger registration + user approval **before** use.
> **Authority order unchanged.** `source_proposal.md` SHA-256 `E700D46…96CC` frozen.

## Legend (fix-type + status tags)

- **`DIRECT`** — wording / relabel / notation / caption / algorithm-text edit; no method or protocol change.
- **`METHOD/PROTOCOL`** — changes an algorithm rule, estimand, statistic, or the experimental protocol; touches C1–C4/H-scope, so `§12-CHANGE-CONTROL` (DRAFT_POLICY §12) — needs explicit user sign-off before editing.
- **`USER_DECISION`** — a value/scope the plan must not decide (carries an open `USER_APPROVAL_REQUIRED`).
- **`MAYBE-NEW-EXPERIMENT`** — retained as a classification label for rejected
  alternatives only. The approved scope adds no experimental arm in this fix round.

---

## Approved decisions applied (2026-07-19)

The user has approved the following change-control decisions for the eventual
Round-2 fix round:

1. The theoretical target remains the **literal removal effect**. RIT may receive
   a removal interpretation only after the pre-registered neutral-pad equivalence
   validation passes; otherwise all empirical wording automatically downgrades to
   **pad-replacement contribution**.
2. Do **not** add a no-pad experimental arm in this draft and do **not** create
   `PILOT_NOPAD_REMOVAL_DELTA`.
3. Drop individual-Shapley claims. Keep LOO as the primary estimand; discuss group
   interaction only as a no-numerical-guarantee limitation and an exploratory A7
   analysis, not as a core allocation claim.
4. Relabel the affected case as **redundant/substitutable**, not complementary.
5. Remove causal verbs such as "causes" and "breeds"; use "accumulates under" or
   "is associated with" for the correlational-credit setting.
6. Governance must use a conservative uncertainty bound plus repeated evidence,
   rather than a point estimate alone. Numerical bound/count choices remain open.
7. Use four disjoint data roles: **fit / calibration / development / sealed
   final-audit**.
8. Keep reward-swap and H3--H5 in the main paper for now, but label them secondary;
   do not move them to an appendix until the AAAI page limit is known.
9. The inferential unit is **seed/deployment run**. The formal seed count is
   computed from the independent pilot power analysis, not guessed in advance.
10. S2--S4 identities, CTI A/B pairs, and every numerical threshold remain
    `USER_APPROVAL_REQUIRED`.

These decisions close the corresponding scope alternatives below. They do not
authorize paper edits yet.

---

## Part A — Merged & de-duplicated issue register

Round 2 weaknesses (C1–C4, M1–M7, MINOR) merged with kill-argument findings; kill
items deduped against Round 2.

| Merged ID | Source(s) | Dedup note |
|---|---|---|
| **RC1** Interaction / Shapley / group-credit coherence + case-study relabel | R2 **C1** + kill **AS3** + kill **obj1(part)** | kill "complementary≠redundant" is the *same* defect as R2 C1; merged. |
| **RC2** Removal vs pad-replacement estimand (conditional) | R2 **C2(a)** + kill **obj headline(part)** | one item; conditional scheme below. |
| **RC3** Audit distribution / aggregation / finite estimator spec | R2 **C2(b)** | ties to PRE_RUN_PROTOCOL §1 (not yet stated in the paper). |
| **RC4** Scope & causal-wording consistency (estimand naming, "breeds", "full-lifecycle credit", "missing primitive"; Conjecture split; "biased estimator") | R2 **C3** + kill **headline** + kill **obj2** + R2 **MINOR(conjecture)** | kill headline (critical) + obj2 (major) + R2 C3 (critical) all target over-generalized/causal wording; merged into one scope-wording workstream. |
| **RC5** Protocol executability + CTI definition | R2 **C4** | S2–S4 / thresholds are `USER_DECISION`; CTI *definition* is derivable from source §7. |
| **RM1** Strengthen claim gates | R2 **M1** | Table 4 + §6. |
| **RM2** Dependence / multiplicity / inferential unit | R2 **M2** | overlaps PRE_RUN_PROTOCOL §4.4/§4.6 (paper must state it). |
| **RM3** Uncertainty-aware governance | R2 **M3** | method change. |
| **RM4** Algorithm 1 completeness (write/update, forced exploration, shadow-RIT, pools, warm-start, group fallback) | R2 **M4** | method/algorithm. |
| **RM5** Fit / calibration / development / final-audit role separation | R2 **M5** | extends PRE_RUN_PROTOCOL §3.1 audit split to 4 roles. |
| **RM6** One claim vocabulary; de-diffuse secondary branches; RL positioning as complementary | R2 **M6** + kill **obj5** | reward-swap/H3/H4/H5 remain in the main paper but are secondary; RL complementarity. |
| **RM7** Baseline-fidelity protocol | R2 **M7** + kill **obj5(part)** | name-faithful vs standardized wrappers. |
| **Rm1..Rm7** Minor wording / notation / figures / presentation | R2 **MINOR** + R2 **§7 visual** | see Part C. |

---

## Part B — Implementation order (CRITICAL → MAJOR → MINOR)

### CRITICAL (do first; RC4 is foundational — everything references the target name)

#### RC4 — Scope & causal-wording consistency `DIRECT` (+ one `METHOD/PROTOCOL` sub-part)
- **Files:** `00_abstract`, `01_introduction`, `02_related_work`, `03_problem_formulation`, `07_limitations_conclusion`, `main.tex` (theorem env).
- **Changes:**
  1. Rename the target consistently to **"immediate conditional retrieval contribution"** in abstract, intro, contribution bullets, related work, conclusion. Remove **"full-lifecycle credit"** (`02_related_work`), qualify **"missing primitive of self-evolution"** and **"a memory's value is defined only counterfactually"** to the evaluated immediate-credit setting (`01_introduction`, `07`). State governance/scope are **empirically tested consumers** of the signal, not causal estimators of retention value.
  2. Remove C1 causal verbs: **"breeds / causes"** → **"accumulates under / is associated with"** (`00`,`01`,`04`). Describe A2 and Full-vs-A4 as matched or mechanism-consistent contrasts, not as proof of causation unless their assignment is explicitly randomized. Also soften residual policy-sensitive phrasing ("diagnoses the failure", "unchanged superstition mechanism").
  3. **Conjecture split** (`§12-CHANGE-CONTROL`): the decomposition **identity** is not conjectural — present it as an inline **Observation/Lemma** (add `\newtheorem{observation}` or state inline), with the consequence "$\coutil_i$ is a **composite signal that can be misaligned with immediate contribution**" (drop "biased estimator" unless Û is explicitly posited as an estimator of the contribution estimand). Keep a **narrower Conjecture** only for the **feedback superstition-equilibrium**.
- **C/H impact:** C1 scope + framing; Conjecture status refined (identity vs equilibrium). C1–C4 stay `PLANNED-EVIDENCE`.
- **Acceptance:** no occurrence of "full-lifecycle credit"; "missing primitive" qualified; C1 uses non-causal verbs; A2/Full-vs-A4 are described only at the strength warranted by their assignment; identity stated as an observation, only equilibrium labelled Conjecture; "biased estimator" removed or justified.

#### RC2 — Removal vs pad-replacement estimand (conditional scheme) `METHOD/PROTOCOL` / `USER_DECISION`
- **Files:** `03_problem_formulation` (Def 1), `04_pilot_diagnostic`, `05_method`, `tables/table4` (gate wording), figures `fig2/fig5` text.
- **Conditional plan (per user directive):**
  - **Target = removal effect** (Def 1 as written, $r(C)-r(C\setminus\{m_i\})$).
  - **The RIT implementation may be interpreted as estimating removal only if** the neutral-pad **equivalence validation** (`PILOT_NEUTRAL_PAD_VALIDATION`) passes a pre-registered equivalence test (pad-replacement outcome statistically indistinguishable from literal removal within the pre-fixed band).
  - **Else (validation fails / not run):** explicitly **downgrade the estimand to "pad-replacement contribution"** everywhere (Def 1 note, §4 label, §5, gates, figure axes), and state that literal removal remains unvalidated future work.
  - **Approved scope:** do not add a no-pad arm in this draft and do not create a removal–pad-gap placeholder.
- **C/H impact:** C1/C2 estimand precision; G-C1/G-C2 gate wording.
- **Acceptance:** the paper states the removal target, the equivalence-validation precondition, and the automatic downgrade rule; no unconditional "removal" interpretation appears without the validation clause.

#### RC3 — Audit distribution / aggregation / finite estimator specification `METHOD/PROTOCOL` / `USER_DECISION`
- **Files:** `03_problem_formulation`, `04_pilot_diagnostic`.
- **Changes:** state, in the paper (mirroring PRE_RUN_PROTOCOL §1), the audit distribution over $(q,C)$, the conditioning/window, the event weighting, and an explicit finite estimator for $\phiaggrit_i$; state that $\phibar_i$, $\coutil_i$, and $\phiaggrit_i$ are compared **on the same audit population / context distribution** (or name the differences). Values (min sample, weighting, window) remain `USER_DECISION` (PRE_RUN_PROTOCOL open items) — do **not** guess.
- **C/H impact:** C1/C2 estimand rigor; underpins G-C1/G-C2.
- **Acceptance:** $\phiagg_i$ has an explicit population + finite estimator in the paper; a sentence asserts common audit population for the three signals.

#### RC1 — Interaction / Shapley / group-credit coherence + case-study relabel `METHOD/PROTOCOL` (+ `DIRECT` relabel)
- **Files:** `03_problem_formulation` (AS3 + the Shapley sentence), `05_method` (governance: how group credit acts), `06_experiments_analysis` (case study), `07` (AS3 limitation).
- **Changes:**
  1. Keep **removal (LOO) as the primary target** and state that LOO is a distinct,
     legitimate estimand rather than an error against Shapley. **Delete individual
     Shapley claims** and the "Shapley first-order approximation / error
     controllable" framing.
  2. **AS3** becomes an explicit interaction caveat with no numerical guarantee.
     Group interaction is discussed only as a limitation and exploratory A7
     analysis; it is not part of the core allocation or governance guarantee.
  3. **Case study relabel** (`DIRECT`): the "two complementary memories each holding half a procedure" example is mislabeled — near-zero individual LOO + positive group value is the **redundant/substitutable** case; rename it, and describe the group-intervention fallback as recovering **group** value for redundant/substitutable memories.
- **C/H impact:** AS3, H5 (redundancy axis), case study (Fig 6), C3 governance semantics.
- **Acceptance:** no individual-Shapley or LOO-as-Shapley-approximation claim remains;
  AS3 is an explicit no-guarantee caveat; group interaction is secondary A7 work;
  the case study uses "redundant/substitutable".

#### RC5 — Protocol executability + CTI definition `DIRECT` (CTI) / `USER_DECISION` (identities/thresholds)
- **Files:** `06_experiments_analysis` (add CTI math def + a Reproducibility/Protocol paragraph or appendix), `07` (pointer).
- **Changes:** add the **mathematical CTI definition** (derivable from source §7: $\mathrm{CTI}=\mathrm{Acc}_B(\text{B-only})-\mathrm{Acc}_B(\text{A}\cup\text{B})$, $\ge 0$ = interference). Add a reproducibility protocol block that **enumerates the items to be locked** (datasets/versions, backbones, stream construction + ordering, bank schedule, split policy, judge protocol, baseline adapters, A/B pairs) as `USER_APPROVAL_REQUIRED` placeholders/text — **do not invent S2–S4, A/B pairs, or thresholds.**
- **C/H impact:** C3 (CTI now defined for G-C3b), C4 reproducibility.
- **Acceptance:** CTI has a formula; a protocol/reproducibility block lists every unresolved lock as `USER_APPROVAL_REQUIRED` with no guessed values.

### MAJOR

#### RM1 — Strengthen claim gates `METHOD/PROTOCOL` / `USER_DECISION`
- **Files:** `tables/table4`, `06_experiments_analysis`.
- **Changes:** make **G-C2 conjunctive** (lower-CI ACA-over-baseline improvement AND event-level CCC AND memory-level CCC$(\phibar,\phiaggrit)$ AND calibration AND a cost ceiling); **join G-C4** end-task gain **with** the low-token-overhead gate; replace "with a CI rule" by an **exact one-sided / equivalence rule**; make **G-C1** use the interval, not the point 0.5; **add an H3 gate row**. Exact thresholds/α remain `USER_DECISION`.
- **C/H impact:** C2, C4, H3 gates.
- **Acceptance:** every gate has an explicit decision rule; G-C2 and G-C4 are conjunctive; H3 has a gate.

#### RM2 — Dependence / multiplicity / inferential unit `METHOD/PROTOCOL` / `USER_DECISION`
- **Files:** `06_experiments_analysis` (setup), pointer to PRE_RUN_PROTOCOL §4.4/§4.6.
- **Changes:** state the approved **inferential unit = seed/deployment run**, use
  **hierarchical/block resampling** for streams, predefine the multiplicity family,
  and compute the formal seed count from the independent-pilot power analysis.
  Multiplicity parameters and the computed post-pilot count remain unresolved;
  neither is guessed in the draft. Note task-clustered BCa alone does not cover
  run-level variation.
- **C/H impact:** C4 inference validity.
- **Acceptance:** setup names the unit, resampling scheme, multiplicity family, and power basis.

#### RM3 — Uncertainty-aware governance `METHOD/PROTOCOL` / `USER_DECISION`
- **Files:** `05_method` (governance), `tables/table3` (A-variant note if needed).
- **Changes:** base eviction/merge on an approved combination of **a conservative
  calibrated bound and repeated evidence** (e.g., an interval for $\phibar_i$
  excluding the governance dead-zone on repeated updates), never on a point estimate
  alone. The exact confidence level, repetition count, and other numerical settings
  remain `USER_DECISION`.
- **C/H impact:** C3 governance, H1.
- **Acceptance:** governance rule references an interval/bound, consistent with the CI-based audit policy.

#### RM4 — Algorithm 1 completeness `METHOD/PROTOCOL`
- **Files:** `05_method` (Algorithm 1 + prose).
- **Changes:** add the **write/update** operation (baseline writer, content out of scope), a **dedicated forced-exploration / randomized forced-inclusion** step (distinct from the non-ranking quarantine bonus), **shadow (non-mutating) RIT** semantics, **fit/calibration/development/sealed-final-audit pool assignment**, and **warm-start** details. Keep any group-intervention fallback outside the core loop as exploratory A7 work with no guarantee. Fix line-9 spacing.
- **C/H impact:** method self-containedness (C2/C3); no claim change.
- **Acceptance:** Algorithm 1 is a complete retrieve–execute–**write** loop with exploration and pool assignment; quarantine bonus and forced inclusion are distinct.

#### RM5 — Fit / calibration / development / final-audit separation `METHOD/PROTOCOL`
- **Files:** `04_pilot_diagnostic`, `05_method`; mirrors PRE_RUN_PROTOCOL §3.1 (extend audit split → 4 roles).
- **Changes:** use the approved four disjoint roles **fit / calibration / development / sealed final-audit**; state that final audit is **blind** to model, threshold, calibration, and stopping selection. Split fractions and label budgets remain unresolved until the approved sizing procedure is run.
- **C/H impact:** C2 fidelity honesty, all gates.
- **Acceptance:** four disjoint roles stated; final audit sealed.

#### RM6 — One claim vocabulary + de-diffuse `DIRECT`
- **Files:** `06_experiments_analysis`; `01`/`02` positioning.
- **Changes:** keep **C1–C4 as the only claim vocabulary**; present reward portability, H3 transfer, H4 Pareto, and H5 boundary trends as **secondary analyses**, not new claims. Keep them in the main paper for now; do not create or move material to an appendix until the AAAI page limit is known. Position MERIT and exploratory outcome-reward RL as complementary, and claim superiority only where the eventual evidence supports it.
- **C/H impact:** H3/H4/H5 demoted to secondary; C3 reward-portability framed as check.
- **Acceptance:** contribution vocabulary = C1–C4 only; RL described as complementary; secondary analyses are labelled as such and remain in the main paper in this round.

#### RM7 — Baseline-fidelity protocol `DIRECT` / `USER_DECISION`
- **Files:** `04_pilot_diagnostic`, `06_experiments_analysis`.
- **Changes:** add a **baseline-fidelity checklist**; distinguish **source-faithful reproductions** from **standardized credit-variant wrappers**; do not report "in the style of ReasoningBank/MemRL" under exact method names unless source-faithful.
- **C/H impact:** C4 comparability.
- **Acceptance:** fidelity checklist present; exact method names used only for faithful reproductions.

### MINOR / presentation (`DIRECT`)

- **Rm1** Conjecture identity/equilibrium split — folded into RC4(3).
- **Rm2** Figures 2/5 label finite RIT outputs $\phi$ → $\widetilde\phi$ (`fig2`,`fig5` placeholder text).
- **Rm3** Fix "two readouts of the same $\phibar$" (`05_method`) — prototypes come from event-level $\phihat$; retrieval score uses $\phibar$; state precisely.
- **Rm4** $R(q)$ → time/state-indexed $R_t(q;\bank_t,\phibar,S)$ (`03`,`05`).
- **Rm5** Qualify $O(1)$ → "fixed $d,k$, per retrieved-memory event" (`00`/`01`/`05`; already partly in §5).
- **Rm6** Residual policy-sensitive wording — folded into RC4(2).
- **Rm7 (visual)** Table 1: add an S1–S5 / W-A/LME/LCM **key**; simplify **Table 4 in place** (do not move it to an appendix this round); keep all floats before Limitations and Fig. 6 with the case study, so no float appears after the conclusion begins and the conclusion text is not stranded. (`tables/table1`, `table4`, `06`/`07` ordering.)

---

## Part C — Removal vs neutral-pad conditional scheme (explicit)

1. **Primary target:** removal effect $\varphi_{i,t}(q,C)=\E[r(C)-r(C\setminus\{m_i\})]$ (Def 1).
2. **Precondition for the removal interpretation:** the neutral-pad equivalence validation (`PILOT_NEUTRAL_PAD_VALIDATION`) must pass a **pre-registered equivalence test** (pad-replacement vs literal removal within the pre-fixed band; band + test are `USER_APPROVAL_REQUIRED`).
3. **If it passes:** RIT labels are interpreted as removal contribution; wording unchanged.
4. **If it fails or is not yet run:** the estimand is **explicitly the
   "pad-replacement contribution"**; every empirical "removal" interpretation is
   downgraded (Def 1 note, §4, §5, gates, Fig. 2/5 axes), and literal removal is
   stated as unvalidated future work.
5. **Approved scope:** no no-pad arm is added in this draft and no removal–pad-gap
   placeholder is created.
6. **No guessing:** the neutral-pad content, equivalence band, test, and decision
   rule remain `USER_APPROVAL_REQUIRED`.

---

## Part D — Consolidated `USER_APPROVAL_REQUIRED` (carried + new)

**Carried from `PRE_RUN_PROTOCOL.md` (still open):** δ, MEI + target power + CI half-width; audit split fraction/design; per-trial subset + TRAIN priority; neutral-pad content + acceptance band; RIT budget ε; **S2–S4 identities + heterogeneity bins**; **CTI A/B domain pairs**; max-baseline contrast statistic; Holm α + FDR q; warm-up $W$; Pareto-knee τ; per-gate CI/threshold rules; formal $K$ / $n^{\text{audit}}$ / seed count (computed post-pilot).

**Round-2 decisions now closed by approval:**

- Removal target with a mandatory neutral-pad equivalence precondition and automatic
  pad-replacement downgrade; no no-pad arm.
- Drop individual-Shapley claims; interaction is only a no-guarantee limitation and
  exploratory A7 analysis; relabel the case redundant/substitutable.
- Use non-causal C1 wording.
- Use conservative bounds plus repeated evidence for governance.
- Use four disjoint data roles.
- Keep secondary analyses in the main paper for now.
- Use seed/deployment run as the inferential unit and compute the seed count from
  independent-pilot power analysis.

**Round-2 details still `USER_APPROVAL_REQUIRED`:**

1. Neutral-pad content, equivalence band, and exact equivalence decision rule.
2. Exact governance confidence bound, repetition rule, and numerical dead-zone if
   it changes from the provisional protocol value.
3. Four-role split fractions and resulting label budgets.
4. Hierarchical/block resampling details, multiplicity-family membership, max-
   baseline statistic, Holm/FDR settings, target power, and target CI half-width.
5. S2–S4 identities and heterogeneity bins; CTI A/B domain pairs and all gate
   thresholds.
6. Formal $K$, $n^{\text{audit}}$, and seed count after the independent pilot;
   these are computed outputs, not discretionary guesses.

---

## Part E — Placeholder impact (**ledger not modified**)

**No new placeholder is proposed for the approved Round-2 scope.** In particular,
`PILOT_NOPAD_REMOVAL_DELTA` must not be created because the no-pad arm was declined.

**Reused (no new ID):** `PILOT_NEUTRAL_PAD_VALIDATION` (pad equivalence), `PILOT_AUDIT_SUPPORT_COVERAGE`, `ABL_*_CTI` (CTI cells), `ABL_A7_*` (group/redundancy), efficiency IDs (cost-ceiling gate), `ABL_A2_*` (matched control). **No new IDs are required for** gate strengthening (Table 4 is design metadata), CTI definition (text), multiplicity/unit (text), or the wording/scope fixes. **Redundancy** trend stays `EVIDENCE GAP` (no ID).

---

## Part F — Acceptance criteria for the eventual fix round (definition of done)

- Target named "immediate conditional retrieval contribution" consistently; no "full-lifecycle credit"; "missing primitive" qualified; C1 verbs non-causal; matched contrasts are not described as causal without randomized assignment.
- Decomposition presented as an Observation/identity; only the feedback equilibrium is a Conjecture; "biased estimator" removed or justified.
- Removal-vs-pad conditional stated with the validation precondition and automatic downgrade rule; no unconditional removal claim.
- $\phiagg_i$ has an explicit audit population + finite estimator; the three signals compared on a common population.
- Case study relabelled "redundant/substitutable"; individual-Shapley claims are absent; AS3 is an explicit no-guarantee caveat and group interaction is secondary A7 work.
- CTI defined mathematically; reproducibility block lists all locks as `USER_APPROVAL_REQUIRED` with no guessed values.
- Gates: every one has an exact decision rule; G-C2 and G-C4 conjunctive; H3 gated.
- Inferential unit is seed/deployment run; multiplicity and power procedure are stated without guessed values; governance uses a conservative bound plus repeated evidence; four label roles end in a sealed final audit.
- Algorithm 1 is a complete retrieve–execute–**write** loop with distinct forced exploration and pool assignment.
- Claim vocabulary = C1–C4 only; secondary analyses remain in the main paper but are clearly labelled; RL is positioned as complementary.
- Notation fixes (Rm2–Rm5) applied; Table 1 key added; Table 4 simplified in place; no float appears after the conclusion begins.
- Placeholder audit: every result cell a registered ID; any new ID registered in the ledger with approval **before** use; 0 unregistered.
- Clean AAAI compile; page budget re-checked vs `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`.

---

**Status: plan complete and approved decisions recorded. Only
`paper/reviews/ROUND2_REVISION_PLAN.md` modified in this decision-recording step. No
paper/table/figure/ledger/protocol modified; no ARIS skill invoked; no compile,
network, or experiment; not implemented. Stopping.**
