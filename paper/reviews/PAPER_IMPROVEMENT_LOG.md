# Paper Improvement Log — MERIT (AAAI 2027)

> **Mode:** Round 1 independent review ONLY. `HUMAN_CHECKPOINT = true`.
> **Status:** `PAUSED — awaiting user + Codex acceptance of the review before any fix is implemented.`
> **Constraints honored this run:** no paper edits, no literature search, no citation additions, no experiments, no Round 2. All new artifacts written under `paper/reviews/` only.
> **Reviewer:** Codex `gpt-5.6-sol`, reasoning effort `xhigh`, fresh zero-context thread (Reviewer Independence Protocol).
> **Reviewer threadId (recovery bookkeeping only — NOT to be reused for Round 2 prompting):** `019f757c-6176-7352-850b-888e14d5d34f`
> **Reviewed artifact:** `reviews/main_round0_original.pdf` (8 pages) + current `sections/`, `tables/`, `figures/placeholders/` source at review time.

## Score Progression

| Round | Score | Verdict | Notes |
|-------|-------|---------|-------|
| Round 0 (current draft) | **4/10** (weak reject) | **Almost** | Reviewer did NOT deduct for intentional `[TBD]` placeholders or disabled bibliography. Projected **6/10** if planned evidence lands as hypothesized; **7/10** with the 3 pre-run fixes below. |
| Round 1 fixes | — | — | NOT implemented (paused at checkpoint by user constraint). |

## Reviewer's three highest-leverage pre-run changes

1. **Fix the estimand + notation.** Define a time/state-conditioned interventional effect and use *separate* symbols for the true effect $\phi$, the finite-rollout RIT label $\tilde\phi$, the ACA prediction $\hat\phi$, and the running aggregate $\bar\phi$; define how event-level effects aggregate into a per-memory SR@k; narrow the claim to *immediate retrieval contribution*.
2. **Redesign the RIT audit before execution.** Uncertainty-aware labels (K=5 binary → 0.2 increments vs a ±0.02 dead-zone is inconsistent), audit-only split, common support, neutral-pad validation, and an explicit token-cost formula (current p=5%·k=4·K=5 is not obviously "low overhead").
3. **Replace Table 4 with atomic C1–C4 falsification gates** and lock every stream identity, CTI/AVG definition, statistical unit, "strongest baseline", and failure action before running experiments.

## Weakness inventory (by severity)

**CRITICAL**
1. Causal estimand and notation internally inconsistent (Def 1 uses conditional not interventional notation; omits time/bank-state/history; one symbol $\hat\phi$ = both RIT label and ACA prediction; event-level $\phi$ used for memory-level SR@k and long-run retention). — *Formal re-scope, no new experiments (if narrowed to immediate contribution).*
2. Proposition 1 not well posed (co-occurrence utility is an average reward, not an estimator of the task-specific difference; baseline-success term survives even at zero covariance; equilibrium clause lacks update rule/dynamics; "Proposition" too strong → rename Conjecture/Hypothesis). — *Theory rewrite only.*
3. "Every claim has a falsification gate" not supported by Table 4 (C1 has no row; H1 maps to C3; C4 gain has no gate; reward portability no gate; H5 is axes not a test). — *Re-scope planned work; reserve an audit-only RIT split.*
4. RIT protocol threatens label validity + affordability (binary K=5 granularity vs ±0.02 dead-zone; filler estimates replacement-by-filler not removal; cost ≈ ~1.2 extra rollout-equivalents/event). — *Modified intervention data within planned experiments; no new datasets.*

**MAJOR**
1. Experiment population + statistical unit not locked (S2–S4 unspecified; CTI/heterogeneity/AVG/"strongest baseline"/resets/warm-up undefined; per-point bootstrap may treat autocorrelated stream tasks as independent; 3 seeds may not support cross-backbone claims).
2. Ablations don't isolate "causal supervision" (A2 compares raw co-occurrence vs a full ACA model with representations+usage features — confounds labels with model capacity; component ablations change the future bank → "causal chain" is mechanism-consistent, not mediation proof). — *New ablation runs on existing data.*
3. "Superstitious" collapses three cases (harmful / practically-null / redundant-but-useful); redundancy can contaminate the C1 headline. — *Mostly reanalysis + planned A7 audit subset.*
4. Algorithm 1 not self-contained ("only eight objects" omits label pool, trajectory, counts, prototypes, quarantine, calibration state; missing init/warm-up; merge semantics vs write-time-out-of-scope tension; log-likelihood feature unavailable for closed backbone; report $O(kd)$/$O(d)$ not unqualified $O(1)$).
5. C1 general claim broader than the 2-system/2-stream diagnostic population; outcome-reward RL under exploration is not "correlational" in the same sense as passive co-occurrence. — *No new experiments if scoped.*

**MINOR**
- C4 is an evaluation plan, not a contribution → move to "Evaluation overview".
- Defensive meta-language ("strictly linear", "no second method", "verified linear chain", "source gate/default") reads process-generated and wastes space.
- "Semantic retrieval naturally induces" the covariance → "can induce, under conditions tested in the pilot".
- "produces causal labels at low budget" / "verified linear chain" prematurely assert validity → "interventional outcome-difference labels" / "architecturally linear".
- Manual table/figure counter resets render Table 5 before Table 1 and Figure 5 before Figure 4 — confusing/fragile.

## Positioning families the reviewer flags for eventual coverage

Sequential causal inference / online experimentation / causal bandits / doubly-robust OPE; retrieval valuation & context selection in IR/RAG; RL credit assignment (counterfactual baselines, difference rewards, advantage estimation); continual/lifelong learning (drift, interference, consolidation); cooperative-game interaction attribution (group Shapley, interaction indices); LLM context attribution beyond static data valuation; memory-poisoning / adaptive-data security. **Key risk named:** equating all outcome-reward learning with passive correlational bookkeeping.

## Visual review (from the 8-page PDF)

Crisp, legible, no clipping/overfull in the final log (only underfull-line warnings). Issues: hero figure appears on page 3 — too late for skim reviewers; **float order wrong** (Table 5 before Table 1; Figure 5 before Figure 4) due to manual `\setcounter` resets; page 7 dense, page 8 has a large blank region (bibliography disabled); Table 1's nine mean±SD columns unlikely to fit once real numbers land (plan to split by benchmark family or move secondary streams to appendix); captions still say "skeleton"/"planned"/"source unspecified"; Algorithm 1 retrieval comment + paired-LOO line wrap awkwardly; body already fills 8 pages before references — verify the AAAI 2027 content-page rule.

## Planned-vs-observed language audit

Policy largely obeyed — no invented measured gain or ranking. Slips to soften/justify: Proposition 1's theorem-style assertion; "semantic retrieval naturally induces"; "produces causal labels at low budget"; "verified linear chain"; categorical "learned managers' reward is correlational".

## Verdict

**Almost.** Even with favorable numbers inserted into the current protocol unchanged, the result would be hard to interpret causally until the estimand, RIT audit, and per-claim gates are fixed.

---

<details>
<summary>Full raw GPT-5.6-Sol xhigh review (Round 1, verbatim)</summary>

## 1. Overall score

- **Current preliminary draft: 4/10 — weak reject.** The problem and paper architecture are promising, but the central estimand, proposition, audit protocol, and claim-to-gate map are not yet rigorous enough to make the eventual numbers unambiguous.
- **Projected if the planned evidence lands as hypothesized: 6/10 — weak accept.** With the three pre-run fixes in the verdict below, I would project **7/10 — accept**.

I am not deducting for the intentionally unresolved numerical cells or bibliography.

## 2. Summary

MERIT has a coherent, memorable thesis: retrieval co-occurrence is not causal contribution, so sparse interventions should supervise an amortized credit signal that governs memory. The story is singular rather than two-paper-like, and the proposed mechanism analysis is unusually well planned. However, the draft currently conflates the true causal effect, its Monte Carlo label, its learned prediction, and its memory-level aggregate; this propagates into Proposition 1, SR@k, the ablations, and the long-run governance claim.

## 3. Strengths

1. **Excellent central hook and singular story.** "Retrieval is not contribution" is easy to retain, and RIT → ACA → consumers is a coherent dependency rather than a bag of modules.

2. **Strong evidence-discipline.** The draft clearly distinguishes planned tests from measurements, includes failure readings, and avoids invented results. I found no fabricated empirical conclusion.

3. **Good mechanism-closure intent.** Reusing CCC/SR axes between the diagnostic and full system, adding calibration, split-half reliability, A2 signal substitution, no-governance/no-gating ablations, and RIT-Full is the right overall evidence shape.

4. **Honest boundary conditions.** AS2 replayability, AS3 interactions, the redundancy failure case, and the possibility that memory is simply missing are substantive limitations, not generic boilerplate.

5. **Strong front matter.** The title and abstract expose the problem, mechanism, cost question, and planned end metric rapidly. The scope exclusion for write-time quality also helps preserve one story.

## 4. Weaknesses

### Claim-to-evidence audit

| Claim | Planned evidence | Assessment |
|---|---|---|
| C1: superstition | Pilot CCC, SR slope, reliability, subset removal | Falsifiable in principle, but absent from Table 4; event-level contribution is not yet converted into a defined memory-level SR statistic. |
| C2: ACA recovers credit | Held-out CCC ≥ 0.6, calibration, A1/A5, transfer | Good plan shape, but "held-out" is underspecified and the target is a noisy RIT estimate, not observed \(\phi\). |
| C3: consumers help | A4/SR, A3/CTI, A2, reward substitution | Partial. CTI is undefined, reward substitution has no gate, and A2 is not an architecture-matched supervision control. |
| C4: systematic benefit at low cost | Main table, efficiency, H4/H5 | Broad coverage, but dataset identities, AVG aggregation, statistical unit, superiority gate, and "Pareto knee" criterion are not locked. |

No empirical claim is inherently unfalsifiable after formalization. As written, however, H5 and the "stable superstition equilibrium" are too underspecified to falsify cleanly.

### CRITICAL

1. **The causal estimand and notation are internally inconsistent.**

   Definition 1 (sections/03_problem_formulation.tex:16) uses conditional rather than interventional notation and omits time, current bank state, the realized retrieved set, and history. The same \(\widehat\phi\) denotes both the finite-rollout RIT label and ACA's prediction. Meanwhile, \(\phi_i(q)\) is event-level, but SR@k ranks memories without defining how event effects become one contribution per memory. Finally, a one-task removal effect is called "a memory's value" and then used for long-run retention.

   **Minimum fix:** Define \(r_t(C;\xi)\) and
   \[
   \phi_{i,t}(q,C)=\mathbb E_\xi[r_t(C;\xi)-r_t(C\setminus\{i\};\xi)\mid H_t].
   \]
   Use separate symbols for true effect \(\phi\), RIT estimate \(\widetilde\phi\), ACA prediction \(\widehat\phi\), and running aggregate \(\bar\phi\). Define the snapshot/audit distribution, minimum sample count, weighting, and uncertainty used to construct memory-level SR@k. Explicitly call this **immediate retrieval contribution**.

   **Work classification:** Fixable by formal re-scoping with no new experiments if the claim is narrowed to immediate contribution. Retaining a claim about long-horizon memory value requires new multi-step intervention data.

2. **Proposition 1 is not mathematically well posed in its present form.**

   Co-occurrence utility is an average observed reward, while \(\phi_i(q)\) is a task-specific difference. Thus \(\widehat U_i\) is not even an estimator of the stated target. Under an additive model,
   \[
   \mathbb E[r\mid i\text{ retrieved}]
   =\mathbb E[r^{(0)}\mid i\text{ retrieved}]
   +\mathbb E[\phi_i\mid i\text{ retrieved}],
   \]
   so a baseline-success term remains even when the stated covariance is zero. The equilibrium clause also lacks an update rule, task distribution, and retrieval dynamics.

   **Minimum fix:** Define an aggregate target first, derive the exact bias decomposition, state sufficient assumptions, and specify the feedback dynamics. Rename it **Conjecture/Hypothesis 1** until a checked theorem exists; "Proposition" plus assertive theorem text is too strong despite the surrounding disclaimer.

   **Work classification:** Theory rewrite/proof only; no new experiments.

3. **The paper claims every C1–C4 claim has a falsification gate, but the map does not support that statement.**

   In Table 4 (tables/table4_hypotheses_map.tex:9), C1 has no row; H1 maps to C3; H3 combines CTI and transfer CCC; C4's strongest-baseline gain has no explicit gate; reward portability has no gate; and H5 is a collection of axes rather than a test.

   **Minimum fix:** Replace Table 4 with one row per atomic claim containing estimand, comparator, audit population, threshold/CI rule, and mandatory claim-narrowing action. Add separate rows for baseline superstition, ACA fidelity, governance, scope/CTI, reward portability, end-task superiority, efficiency, and boundaries.

   **Work classification:** Re-scope existing planned work; reserve part of the existing RIT budget as an audit-only split. No new benchmark is needed.

4. **The current RIT protocol threatens both label validity and the central affordability claim.**

   With binary success and \(K=5\), the raw success difference has increments of 0.2, yet the paper classifies \(\phi\le0\) and uses a \(\pm0.02\) dead zone. Split-half reliability does not make near-zero signs trustworthy. The filler intervention also estimates replacement-by-filler, not literal removal, unless neutrality is validated.

   Cost is also concerning: with \(p=5\%\), \(k=4\), and \(K=5\), sharing one five-rollout full-set control still requires about 20 ablations plus control rollouts on every sampled task—roughly 1.2 additional rollout-equivalents per normal event if the observed rollout is reused. That is not obviously "low overhead."

   **Minimum fix:** Budget RIT in tokens/rollouts rather than task probability; sample one or a subset of memories per trial; share controls; use adaptive repetitions for near-zero cases; define an equivalence region and uncertainty-aware SR; and validate a length-matched neutral pad. State the exact expected-cost formula before running the sweep.

   **Work classification:** Requires modified/new intervention data within the planned experiments, but no new datasets or benchmark family.

### MAJOR

1. **The experiment population and statistical unit are not yet locked.**

   S2–S4 are explicitly unspecified; CTI, heterogeneity, AVG aggregation, "strongest baseline," stream resets, and warm-up are undefined. Per-point bootstrap bands may treat autocorrelated streaming tasks as independent, and three seeds may not support the intended cross-backbone conclusions.

   **Minimum fix:** Name every stream before execution; define its order/construction and heterogeneity index; specify bank initialization/reset policy, metric normalization, macro-AVG, CTI, selection of the strongest baseline, blocked or hierarchical paired inference, and multiplicity handling. Add a seed-level power calculation.

   **Work classification:** Re-scope existing work; more seeds require additional runs only if the power calculation indicates it.

2. **The ablations do not yet isolate "causal supervision" or establish the claimed causal chain.**

   A2 compares raw co-occurrence utility against an ACA model with representations and usage features. That does not isolate interventional labels from model capacity. Also, component ablations alter the future bank and retrieval distribution; observing CCC → SR/CTI → AVG is mechanism-consistent evidence, not mediation proof.

   **Minimum fix:** Replace or supplement A2 with the identical attributor architecture trained on matched observational/outcome labels under the same update and compute budget. Evaluate both signals on a shared, fixed audit set, and rename "causal chain" to "mechanism-consistent sequence" unless formal mediation is added.

   **Work classification:** Requires new ablation runs, using existing datasets and checkpoints.

3. **"Superstitious" currently collapses three distinct cases.**

   LOO \(\le0\) includes harmful memories, practically null memories, and redundant-but-useful memories. The redundancy caveat is relegated to exploratory H5, but it can contaminate the headline C1 statistic.

   **Minimum fix:** Report harmful \((\phi<-\delta)\), practically null \((|\phi|\le\delta)\), and interaction/redundancy cases separately. Define "superstitious" operationally as high observational credit plus confidently null/harmful marginal contribution in a stated context.

   **Work classification:** Mostly reanalysis; identifying redundancy requires the already planned group-intervention/A7 data on an audit subset.

4. **Algorithm 1 is not yet self-contained.**

   The "only eight objects" statement omits the label pool, trajectory, counts, prototypes, quarantine status, and calibration state. Initialization/warm-up is missing; the UCB exploration bonus is said not to affect ranking; merge semantics are unspecified despite write-time quality being declared out of scope; and the log-likelihood feature may be unavailable for the closed backbone.

   **Minimum fix:** Add a state/initialization paragraph; define forced exploration separately from ranking; state that merge content is inherited and fixed from the baseline while only its trigger changes; and specify a feature mask/fallback for APIs without token log-probabilities. Report complexity as \(O(kd)\) per query or \(O(d)\) per retrieved-memory event, not unqualified \(O(1)\).

   **Work classification:** Specification fix with no new experiment; feature portability can use the planned A5 and closed-model rows.

5. **The general claim is broader than the planned diagnostic population.**

   Two systems on two streams can demonstrate existence in evaluated conditions, but not that "current systems" generally breed increasingly superstitious memories. Likewise, an outcome reward used under randomized RL exploration is not necessarily "correlational" in the same sense as passive co-occurrence counting.

   **Minimum fix:** Scope C1 to the evaluated memory-update families and streams, and distinguish observational credit from action-value learning with exploration/counterfactual baselines. If broad prevalence remains central, repeat the baseline audit across the already planned main streams.

   **Work classification:** No new experiments if narrowed; broader prevalence requires re-scoping the planned main runs to include additional audits.

### MINOR

- C4 is an evaluation plan, not yet a scientific contribution. Move it from "Contributions" to "Evaluation overview," or replace it with the eventual validated empirical finding.
- The draft repeats defensive meta-language—"strictly linear," "no second method," "not a separate method," "source gate," "source default," "verified linear chain." This reads process-generated and consumes scarce space.
- "Semantic retrieval naturally induces" the required covariance is asserted without evidence and is not generally true; change to "can induce, under conditions tested in the pilot."
- "RIT continuously produces causal labels at low budget" and "verified linear chain" prematurely assert validity/affordability. Use "interventional outcome-difference labels" and "architecturally linear."
- Table and figure counters are manually reset, producing Table 5 before Tables 1–4 and Figure 5 before Figure 4. This is confusing and fragile.

## 5. Positioning / missing related-work families

The family-level organization is good, but the eventual positioning should cover:

- Sequential causal inference, online experimentation, causal/contextual bandits, adaptive treatment assignment, and doubly robust/off-policy evaluation.
- Retrieval valuation in information retrieval and RAG: value of information, retrieval ablation, learned reranking, and context selection.
- RL credit assignment: counterfactual baselines, difference rewards, advantage estimation, and delayed credit.
- Continual/lifelong learning: concept drift, catastrophic interference, dynamic memory consolidation, and online calibration.
- Cooperative-game interaction attribution: group Shapley, interaction indices, redundant/complementary features, and structured removal.
- LLM context attribution beyond static data valuation: input erasure, causal context ablation, and attribution stability.
- Memory poisoning and adaptive-data security, given the draft's own "credit laundering" concern.

The key positioning risk is not missing a citation name; it is equating all outcome-reward learning with passive correlational bookkeeping.

## 6. Visual review of the compiled PDF

I inspected all eight rendered pages of the current compiled PDF (build/main.pdf).

- **Overall rendering:** Crisp and legible, with no clipping, overlap, broken glyphs, unresolved cross-references, or overfull boxes in the final log. Only several underfull-line warnings remain.
- **Figures:** All placeholder text is readable. However, the "hero" appears only on page 3, too late for a skim reviewer. Figures 1 and 3 are data-free schematics and should be drawn now; the empirical plot placeholders can reasonably wait.
- **Float order:** Table 5 appears on page 3 before Table 1 on page 7; Figure 5 appears before Figure 4. Remove all manual counter resets and use source order.
- **Page flow:** Figure 1 plus Table 5 interrupts the problem formulation between pages 2–3. Page 7 is visually dense, while page 8 has a large blank lower/right region because references are disabled.
- **Tables:** Table 1 is readable with short "TBD" cells, but nine real mean±SD columns are unlikely to fit. Plan to split it by benchmark family, shorten rows, or move secondary streams to the appendix. Tables 3, 4, and 6 are structurally clear.
- **Captions:** Informative and honest, but "skeleton," "planned," and "source unspecified" should disappear from the submission version.
- **Algorithm 1:** Generally legible. The retrieval comment and paired-LOO line wrap awkwardly, the input block is dense, and the warm-start/state omissions are visible at skim speed.
- **Page budget:** The body already occupies eight pages without references. Check the final AAAI 2027 content-page rule before real plots and bibliography increase the footprint.

## 7. Planned-versus-observed language audit

The evidence policy is largely obeyed: there is no invented measured gain or ranking. The main slips are Proposition 1's theorem-style assertion, "semantic retrieval naturally induces," "produces causal labels at low budget," "verified linear chain," and the categorical characterization of learned managers' rewards as correlational. These should be softened or formally justified; the rest of the planned/hypothesis language is careful.

## 8. Verdict

**Almost.** If favorable numbers are inserted into the current protocol unchanged, I would still hesitate because the result would be difficult to interpret causally.

The three highest-leverage changes are:

1. Define the time/state-conditioned estimand and separate \(\phi\), \(\widetilde\phi\), \(\widehat\phi\), and \(\bar\phi\); narrow the claim to immediate retrieval contribution.
2. Redesign the RIT audit before execution: uncertainty-aware labels, audit-only split, common support, neutral-pad validation, and an explicit token-cost formula.
3. Replace Table 4 with atomic C1–C4 gates and lock all streams, CTI/AVG definitions, statistical units, and failure actions before running experiments.

</details>

## Fixes implemented this round

**None.** Paused at the Round-1 human checkpoint per user constraint. No paper source, table, figure, bibliography, or ledger file was modified. Awaiting user + Codex decision on which findings to act on.

---

# Round 2 — Fix Implementation (2026-07-19)

> **Mode:** Round 2 fix/recompile ONLY. Round 2 review (`ROUND2_REVIEW.md`) and the
> detect-only kill-argument (`KILL_ARGUMENT.md`) were already complete and were **not
> re-run**. Only the changes approved in `reviews/ROUND2_REVISION_PLAN.md` were
> implemented. No experiments, no network, no citations added, no real results/
> thresholds back-filled. No `USER_APPROVAL_REQUIRED` value was resolved. No new
> ledger ID was created; `PILOT_NOPAD_REMOVAL_DELTA` was **not** created and no no-pad
> arm was added. Individual-Shapley claims and C1 causal claims were removed. Reward-
> swap and H3--H5 were kept in the main paper, labelled secondary; no appendix created.

## Score Progression (cumulative)

| Round | Score | Verdict | Notes |
|-------|-------|---------|-------|
| Round 0 (original) | 4/10 | Almost | Baseline draft. |
| Round 1 fixes (R1--R6) | — | — | Applied + human-approved in a prior turn (estimand/notation, uncertainty/neutral-pad/audit split, A2 control, float numbering). |
| Round 2 review | 5/10 | Almost | Fresh zero-context `gpt-5.6-sol` xhigh; sharpened notation exposed C1/C2 formal issues. Projected 7/10 with the fixes below. |
| Round 2 fixes (this turn) | — | — | Implemented the approved RC1--RC5, RM1--RM7, MINOR. Not re-scored (no re-review this turn). |

## Fixes implemented (mapped to ROUND2_REVISION_PLAN.md)

**CRITICAL**
- **RC4 (scope & causal wording).** Target renamed to *immediate conditional retrieval
  contribution* in abstract/intro/related/conclusion; removed "full-lifecycle credit";
  qualified "missing primitive" to the credit-assignment step in the immediate-
  contribution setting; replaced causal verbs ("breeds"/"causes"/"produces") with
  "accumulates under / is associated with"; stated governance & scope are *empirically
  tested consumers*, not causal estimators of retention value; **Conjecture split** —
  the decomposition is now **Observation 1** (identity), "biased estimator" replaced by
  "composite signal that can be misaligned with immediate contribution", and only the
  feedback **superstition equilibrium** remains a Conjecture.
- **RC2 (removal vs pad-replacement).** Def. 1 note states the literal-removal target,
  the neutral-pad equivalence precondition (`PILOT_NEUTRAL_PAD_VALIDATION`), and the
  automatic downgrade to "pad-replacement contribution"; mirrored in §4/§5. No no-pad
  arm; no new placeholder.
- **RC3 (audit distribution/estimator).** §3/§4 now give the audit distribution
  (retrieval-conditioned, frozen snapshot, common support), uniform event weighting,
  the design-based finite estimator for $\widetilde\Phi_i$, and the common-audit-
  population statement for $\widehat U_i,\bar\varphi_i,\widetilde\Phi_i$. Values remain
  `USER_APPROVAL_REQUIRED`.
- **RC1 (interaction/Shapley/case study).** Individual-Shapley and LOO-as-Shapley-
  approximation framing deleted; AS3 rewritten as a no-guarantee interaction caveat;
  group interaction is exploratory A7 only; case study + Fig. 6 + Table 3 A7 row
  relabelled **redundant/substitutable**.
- **RC5 (CTI + reproducibility).** Added the mathematical CTI definition
  ($\mathrm{Acc}_B(\text{B-only})-\mathrm{Acc}_B(\text{A}\cup\text{B})$) and a
  reproducibility-protocol block enumerating every lock (S2--S4, A/B pairs, thresholds,
  splits, ordering, judge) as `USER_APPROVAL_REQUIRED`; no values invented.

**MAJOR**
- **RM1 gates.** G-C2 made conjunctive (event- + memory-level CCC, ACA$-$baseline CCC
  gain, ECE, cost); G-C4 joined with token-overhead; exact one-sided/CI rules replace
  "with a CI rule"; G-C1 uses the interval; **G-H3 row added**; Table 4 simplified in place.
- **RM2 inference.** Inferential unit = seed/deployment run; hierarchical/block
  resampling; predefined Holm FWER family (FDR for exploratory); note that task-
  clustered BCa alone misses run-level variation; seed count from independent pilot.
- **RM3 governance.** Eviction/merge now use a conservative confidence bound plus
  repeated evidence, not a point estimate; confidence level & repetition count are
  `USER_APPROVAL_REQUIRED`.
- **RM4 Algorithm 1.** Added write/update, a forced-exploration step distinct from the
  quarantine bonus, shadow (non-mutating) RIT, fit/calibration/development/sealed-audit
  pool routing, warm-start; line-9 crowding fixed.
- **RM5 data roles.** Four disjoint roles (fit/calibration/development/sealed final
  audit); final audit blind to model/threshold/calibration/stopping.
- **RM6 vocabulary.** C1--C4 kept as the only claim vocabulary; reward portability and
  H3/H4/H5 labelled *secondary analyses*, kept in the main paper; RL positioned as
  complementary.
- **RM7 baseline fidelity.** Added a fidelity checklist; distinguished source-faithful
  reproductions from standardized credit-variant wrappers.

**MINOR (Rm2--Rm7)**
- Figs 2/5 relabelled to finite RIT outputs ($\widetilde\Phi$, $\widetilde\varphi$).
- "Two readouts of the same $\bar\varphi$" corrected (prototypes from event-level
  $\widehat\varphi$; retrieval score uses $\bar\varphi$).
- $R(q)\rightarrow R_t(q;\mathcal M_t,\bar\varphi,S)$.
- $O(1)$ qualified to "constant in bank size, at fixed $d$ and top-$k$".
- Table 1 S1--S5 / W-A / LME / LCM key added; Table 4 simplified in place; `\clearpage`
  before Limitations so no float appears after the conclusion begins.

## Files modified

`main.tex` (Observation env), `math_commands.tex` (unchanged this turn),
`sections/00_abstract.tex`, `01_introduction.tex`, `02_related_work.tex`,
`03_problem_formulation.tex`, `04_pilot_diagnostic.tex`, `05_method.tex`,
`06_experiments_analysis.tex`, `07_limitations_conclusion.tex`,
`tables/table1_main_results.tex`, `tables/table3_ablation.tex`,
`tables/table4_hypotheses_map.tex`,
`figures/placeholders/fig2_diagnostic_baseline.tex`,
`figures/placeholders/fig5_mechanism_recovery.tex`,
`figures/placeholders/fig6_case_study.tex`.

## Compile & audit

- **Compile:** two `latexmk` passes, exit 0. **11 pages.** 0 undefined refs/citations,
  **0 Overfull hbox, 0 Underfull hbox**, 0 LaTeX warnings, 0 unresolved `??`.
- **Placeholders:** 239 unique IDs used, **all ledger-registered, 0 unregistered, 0 new
  IDs** (2 registered IDs unused: `AAAI2027_TRACK_PAGE_LIMIT`, `FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION`).
- **Numbering:** Def 1, Def 2, Observation 1, Conjecture 1; Figs 1--6 and Tables 1--6
  monotonic.
- **Floats:** all floats on pages $\le 10$; conclusion (p. 11) is float-free; Fig. 6
  sits with the case study.
- **Evidence wording:** no asserted results, no fabricated numbers/thresholds (all
  decimals are pre-existing source-defaults); every unresolved lock marked
  `USER_APPROVAL_REQUIRED`.
- **Page budget:** 11 pages vs unresolved `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]` — flagged;
  compression deferred until the venue limit is user-provided (and references are added).

## Output PDF

`reviews/main_round2.pdf` (= `build/main.pdf`, 11 pages).

## Unresolved `USER_APPROVAL_REQUIRED` (carried; none resolved this turn)

Neutral-pad content/band/decision rule; governance confidence level, repetition count,
dead-zone; four-role split fractions; hierarchical/block resampling details,
multiplicity membership, max-baseline statistic, Holm $\alpha$/FDR $q$, target power,
target CI half-width; S2--S4 identities & heterogeneity bins; CTI A/B pairs; all gate
thresholds; $\delta$, MEI; RIT budget $\varepsilon$; warm-up $W$; Pareto-knee $\tau$;
formal $K$/$n^{\text{audit}}$/seed count (computed post-pilot).

**Stopped after Round 2 fix + recompile + audit. Did NOT enter citation, figure-
drawing, or experiment phases.**
