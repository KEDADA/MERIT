# Round 2 Review — MERIT (AAAI 2027)

> **Mode:** Round 2 independent review ONLY. `HUMAN_CHECKPOINT = true`.
> **Status:** `PAUSED — awaiting user authorization of Round 2 fixes; none implemented.`
> **Constraints honored:** fresh `gpt-5.6-sol` / `xhigh` thread; no reuse of the
> Round 1 threadId; the reviewer was told nothing about prior rounds, prior scores,
> the revision plan, or any fix summary. Detect-only kill-argument run (see
> `KILL_ARGUMENT.md`). No paper/table/figure/ledger/protocol modified. All artifacts
> under `paper/reviews/`.
> **Reviewer threadId (recovery bookkeeping only):** `019f772e-f482-7293-b8b5-56a7f6379367`
> **Artifact reviewed:** `reviews/main_round1.pdf` (9 pages, post-R1→R6) + current LaTeX source.

## Score & verdict

| | Current draft | If planned evidence lands | With formal/statistical repairs |
|---|---|---|---|
| **Round 2** | **5/10** (borderline reject) | 6/10 (weak accept, as scoped) | 7/10 |
| Verdict | **Almost** — not ready merely by replacing TBDs; repair the formal target and protocol before running experiments. | | |

## Graded issues (Round 2)

**CRITICAL**
- **C1 — AS3 & interaction example formally wrong.** LOO is the defined estimand, so interactions are not estimation "error" unless the normative target is Shapley; and two *complementary* memories (each a necessary half) should each have *large* LOO — near-zero individual LOO with positive group value is the *redundant/substitutable* case. The draft alternates among removal effect / Shapley / group credit without defining their relationship or how group credit affects governance. *(Re-scope A7/group work; individual Shapley claims would need coalition interventions.)*
- **C2 — Implemented RIT ≠ stated estimand.** Def. 1 removes $m_i$; RIT replaces it with a neutral pad → estimates a pad-replacement effect unless exact neutrality is shown. $\Phi_i=\mathbb{E}[\varphi_{i,t}]$ lacks an explicit audit distribution, conditioning/window, and finite estimator, so $\bar\varphi_i$, $\widehat U_i$, $\widetilde\Phi_i$ may summarize different endogenous context distributions. *(No new experiment if renamed to pad-replacement; a true removal claim needs no-pad equivalence data.)*
- **C3 — C1 causal wording exceeds evidence.** Rising SR + low CCC show accumulation *under* correlational credit, not that it *breeds/causes* it; the pilot has no randomized removal of the utility-feedback mechanism. *(No new experiment if reworded to "accumulates under / associated with"; causal claim needs a feedback control.)*
- **C4 — Protocol not yet executable/reproducible.** S2–S4 unspecified; backbones/benchmarks generic; stream construction, ordering, bank schedule, split policy, baseline adapters absent; CTI (a primary C3 estimand) never defined. *(Prerequisite lock for existing runs — these are the open `USER_APPROVAL_REQUIRED` protocol items.)*

**MAJOR**
- **M1** Several gates don't test the full claim (G-C2 lacks superiority-over-baseline / memory-level / cost; "with a CI rule" is not a rule; G-C4 omits low-overhead; G-C1 treats point 0.5 as sufficient; H3 has no gate).
- **M2** Dependence/multiplicity/inferential unit underspecified (serial dependence, recurring memories, nested top-sets, runs across seeds/streams/categories/backbones); task-clustered BCa may not address run-level variation.
- **M3** Governance not uncertainty-aware (eviction/merge use point $\bar\varphi$ + count, inconsistent with the CI-based audit policy).
- **M4** Algorithm 1 omits the write/update op and a real forced-exploration step; shadow-RIT, pool assignment, warm-start, group fallback unspecified.
- **M5** Fit/calibration/development/audit roles not separated (isotonic calibration appears to reuse the training pool; final audit must stay blind to selection/threshold/stopping).
- **M6** Secondary branches diffuse the story (reward substitution as a 3rd gate; H3/H4/H5 read as a second claim system over C1–C4).
- **M7** Baseline fidelity protocol needed (shared retriever may strip a defining part of some baselines; "in the style of" implementations should not be reported under exact method names).

**MINOR** — Conjecture mixes an algebraic identity with a genuine equilibrium conjecture (split them); Figs 2/5 label finite RIT outputs as $\phi$ not $\widetilde\phi$; "two readouts of the same $\bar\varphi$" is inaccurate (prototypes come from event-level $\widehat\varphi$); $R(q)$ should be time/state-indexed; qualify $O(1)$ as "fixed $d,k$, per retrieved-memory event"; residual policy-sensitive wording ("breeds…", "diagnoses the failure", "unchanged superstition mechanism").

## Kill-argument (detect-only) — conclusion

Full record in `KILL_ARGUMENT.md`. Attack thesis: **estimand overclaim** (immediate
LOO sold as the causal primitive of self-evolution). Independent defense: headline
**partially_answered / critical** (formal def scopes it, but abstract/intro/related/
conclusion re-expand to "full-lifecycle credit" / "missing primitive"); obj 2
still_unresolved/major; objs 1,3,5,AS3 partially_answered/major; obj 4 answered.
**Single still-unresolved critical:** estimand/positioning mismatch — fixable by
re-scoping wording, no new experiments. Merged critical/major items are listed in
`KILL_ARGUMENT.md`; the case-study complementary-vs-redundant error was surfaced
independently by both the review (C1) and the defense.

## Objective Round 1 → Round 2 comparison (executor, computed AFTER the review)

> This comparison was NOT shown to the reviewer; the Round 2 thread was fresh and
> context-naive.

- **Score:** Round 1 **4/10** → Round 2 **5/10** (+1) on the current draft; both
  project 6/10 if evidence lands and 7/10 with fixes; verdict unchanged (**Almost**).
- **What the R1→R6 fixes bought (acknowledged in Round 2):** the reviewer calls the
  six-symbol ontology "the right ontology," praises the capacity-matched
  observational-label control **A2**, the no-governance/no-scope ablations,
  split-half reliability, neutral-pad validation, RIT-Full reference, positive-subset
  removal, and explicit boundary analysis; notes honest immediate-vs-long-horizon
  scope, clean compile with **no overfull boxes or broken refs**, and correct
  monotonic float numbering. These are precisely the R1(estimand), R3(uncertainty/
  neutral-pad/audit split), R5(A2), R6(numbering) targets — so the applied fixes
  registered.
- **Why the score rose only +1:** sharpening the notation *exposed* deeper formal
  issues that a looser draft hid — the removal-vs-pad-replacement-vs-Shapley/group
  distinction (C1/C2) and the complementary-vs-redundant case-study error. These are
  new CRITICALs, not regressions.
- **Round 1 items now resolved/eased:** the Round 1 CRITICAL "one symbol $\hat\phi$
  for both label and prediction" is fixed (now $\widetilde\varphi$ vs $\widehat\varphi$);
  Proposition→Conjecture done; Table 4 atomic gates exist (Round 1 said C1 had no
  gate — now G-C1 exists, though Round 2 M1 says gates are under-strict); float order
  fixed (Round 1 flagged Table 5 before Table 1 / Fig 5 before Fig 4 — now monotonic).
- **Round 1 items still open (consistent across rounds):** S2–S4 / CTI / statistical
  unit lock (Round 1 MAJOR-1 → Round 2 C4/M2), and the causal-wording caution
  (Round 1 MAJOR-5 → Round 2 C3 + kill headline). These remain because they are
  `USER_APPROVAL_REQUIRED` protocol items, deliberately not decided.
- **New in Round 2 (not seen in Round 1):** pad-replacement-vs-removal estimand
  mismatch (C2); complementary/redundant case-study error (C1); Algorithm 1 missing
  write/update op (M4); calibration/audit role separation (M5); "two readouts of the
  same $\bar\varphi$" inaccuracy (MINOR); Table 4 now flagged *too dense*; end-of-paper
  float placement damages the conclusion (float interruption + stranded fragment,
  page 9 whitespace).

## Fixes implemented this round

**None.** Paused at the Round 2 human checkpoint. No paper source, table, figure,
ledger, or protocol modified.

---

<details>
<summary>Full raw GPT-5.6-Sol xhigh Round 2 review (verbatim)</summary>

## 1. Overall Score

- **Current preliminary draft: 5/10 — borderline reject.**
- **Projected if the planned evidence lands as hypothesized: 6/10 — weak accept as currently scoped.** With the formal and statistical repairs below, this could plausibly reach **7/10**.

I do not penalize the paper for the registered TBDs or disabled bibliography.

## 2. Summary

The paper has a strong, singular core contribution: sparse randomized leave-one-out trials train an amortized credit predictor whose signal governs memory retention and retrieval scope. The evidence architecture is unusually disciplined, but the current formalization has a serious interaction-credit error, an intervention/estimand mismatch, and several gates that do not fully test their associated claims. Experiments alone will not make the paper ready; these issues should be resolved before running them.

## 3. Strengths, ranked

1. **Excellent central framing.** "Retrieval is not contribution" is memorable, consequential, and consistently motivates RIT → ACA → consumers.
2. **Strong evidence discipline.** The paper cleanly distinguishes hypotheses, planned readings, failure actions, and unresolved results. I found no fabricated quantitative conclusion.
3. **Good intended separation of statistical objects.** The macros distinguish true event effect $\varphi$, finite RIT label $\widetilde\varphi$, ACA prediction $\widehat\varphi$, running aggregate $\bar\varphi$, true memory aggregate $\Phi$, and finite audit estimate $\widetilde\Phi$. This is the right ontology, even though several usages still violate it.
4. **Thoughtful controls.** Particularly strong are the capacity-matched observational-label control A2, no-governance/no-scope ablations, split-half reliability, neutral-pad validation, RIT-Full reference, positive-memory subset removal, and explicit boundary analysis.
5. **Honest scope.** Immediate rather than long-horizon value, replayability, closed-loop drift, redundancy, write-time quality, and poisoning risk are all acknowledged.
6. **Generally clear presentation.** The paper compiles cleanly with no overfull boxes or unresolved references. Figures and captions clearly label themselves as planned artifacts.

## 4. Weaknesses, ranked

### CRITICAL

**C1. AS3 and the interaction example are formally wrong.** Leave-one-out is the defined estimand, so interactions do not create estimation "error" unless the intended normative target is instead Shapley value. More concretely, two complementary memories containing different necessary halves of a procedure should each have a large leave-one-out effect: removing either causes failure. Near-zero individual leave-one-out with positive group value is the **redundant/substitutable** case, not the complementary case. The paper alternates among removal effect, Shapley value, and group credit without defining their relationship or how group credit affects governance.

**C2. The implemented RIT intervention does not exactly estimate the stated estimand.** Definition 1 removes $m_i$, whereas RIT replaces it with a length-matched neutral pad. Unless exact neutrality is established, this estimates a pad-replacement effect. In addition, $\Phi_i=\mathbb E[\varphi_{i,t}]$ lacks an explicit audit distribution, conditioning/window, and finite estimator. Consequently, $\bar\varphi_i$, $\widehat U_i$, and $\widetilde\Phi_i$ may summarize different endogenous context distributions.

**C3. C1's causal wording exceeds its evidence.** A rising SR and low CCC under existing systems show accumulation under correlational credit, not that correlational credit **breeds** or causes the phenomenon. The pilot has no randomized removal of the utility-feedback mechanism. The planned evidence supports "co-occurs with," "fails to prevent," or "accumulates under," unless an explicit feedback control is added.

**C4. The experimental protocol is not yet executable or reproducible.** S2–S4 are explicitly unspecified; backbones and most benchmarks are generic categories; stream construction, task ordering, bank-size schedule, split policy, and exact baseline adapters are absent. CTI, a primary C3 estimand, is never defined. This prevents a reviewer from determining whether evidence landing "as hypothesized" would be comparable or reproducible.

### MAJOR

**M1. Several claim gates do not test the full claim.**
- G-C2 requires only an event-level correlation threshold; it does not require superiority over the correlational comparator, does not gate memory-level CCC, and does not gate low cost.
- "With a CI rule" is not a decision rule.
- G-C4 gates accuracy but not C4's "low token overhead."
- G-C1 uses an uncertain correlation estimate as if the point threshold $0.5$ were sufficient.
- H3 has no gate, while H1/H2 are invoked without being defined.

**M2. Dependence, multiplicity, and the inferential unit are insufficiently specified.** Tasks are sequential, memories recur, top sets are nested over time, and methods are repeated across seeds, streams, categories, and backbones. "Task-clustered paired BCa intervals" do not obviously address run-level variation or serial dependence. C1 also entails several systems, streams, subsets, checkpoints, and correlations without a clear multiplicity family.

**M3. Governance is not uncertainty-aware.** Eviction and merging use point-valued $\bar\varphi_i$ and a count threshold. A dead zone plus $n_i\ge8$ is not uncertainty quantification, especially under drift and prediction error. This is inconsistent with the otherwise careful CI-based audit policy.

**M4. Algorithm 1 is not yet a self-contained retrieve–execute–write loop.** It omits the write/update operation entirely. It also says quarantine provides "forced exploration" while the bonus does not enter ranking and no separate forced-inclusion step exists. Warm-start data, audit assignment, shadow/non-mutating RIT execution, and the group fallback are not specified.

**M5. Fit, calibration, development, and audit roles are not separated.** The paper has training and audit pools, but isotonic calibration appears to use the same training pool as model fitting, and provisional hyperparameters have no stated development split. The final audit must remain blind to model selection, threshold selection, calibration, and stopping decisions.

**M6. The story develops secondary branches.** The claimed method has "two consumers," but C3 also includes reward substitution as a third gate. Zero-shot transfer H3, Pareto-knee H4, boundary H5, and whether learned managers beat heuristic managers further diffuse the central mechanism. The core story remains recoverable, but this material currently reads like a second claim system layered over C1–C4.

**M7. Baseline fairness needs a fidelity protocol.** Giving every method the same retriever may control one variable while removing a defining part of some baselines. "In the style of ReasoningBank/MemRL" should not be reported under exact method names unless the implementations are source-faithful. Native versus standardized-wrapper comparisons need to be distinguished.

### MINOR

- The Conjecture combines an immediate algebraic identity with a genuinely conjectural equilibrium claim. The former should be an observation/proposition; only the feedback equilibrium is conjectural.
- Figures 2 and 5 label finite RIT outputs as $\phi$, not $\widetilde\phi$.
- "Governance and scope gating are two readouts of the same $\bar\varphi$" is inaccurate: prototypes are learned from event-level $\widehat\varphi$, while the retrieval score also uses $\bar\varphi$.
- $R(q)$ should be $R_t(q;\mathcal M_t,\bar\varphi,S)$ or equivalent because retrieval changes over time.
- The $O(1)$ language should say "fixed $d,k$, per retrieved-memory event"; usage features and log-likelihood gain still have nontrivial computation.
- Policy-sensitive wording remains in "credit breeds…whose fraction rises," "diagnoses the failure," and "an unchanged superstition mechanism." These should be changed to explicit test/hypothesis language.

## 5. Minimum fixes and experiment impact

| ID | Minimum fix | Existing plan or new evidence? |
|---|---|---|
| C1 | Keep removal effect as the primary target; rename the failure case "redundant/substitutable memories"; define $\varphi_{G,t}$, its trigger, and how group credit changes governance. Remove Shapley claims unless an allocation estimator is specified. | **Re-scope existing A7/group work.** Retaining individual Shapley claims requires coalition interventions. |
| C2 | Define the pad-replacement estimand or add a no-pad arm; write explicit formulas for $\widetilde\varphi$ and weighted $\widetilde\Phi$; lock audit population, time window, support, inclusion weights, and aggregation for all compared signals. | **No new experiment if renamed to pad-replacement.** A genuine removal-effect claim requires no-pad equivalence data if not already part of pad validation. |
| C3 | Replace "breeds/causes" with "accumulates under/is associated with" throughout C1. | **No new experiment.** Retaining causal language requires a randomized feedback/no-feedback control. |
| C4 | Register exact datasets, versions, backbones, splits, stream ordering, task counts, bank schedules, judge protocol, and a mathematical CTI definition before running. | **No new experiment; prerequisite for existing runs.** |
| M1 | Make G-C2 conjunctive: lower CI for ACA–baseline improvement, event and memory fidelity, calibration, and cost ceiling. Join C4 success and overhead gates. Replace vague CI language with exact one-sided/equivalence rules. | **Existing planned measurements suffice.** |
| M2 | Use seed/deployment run as the top-level unit, with hierarchical or block resampling for streams; predefine multiplicity families and power the number of independent runs. | May require **additional seeds/runs**, but this is already compatible with the promised power analysis. |
| M3 | Base eviction/merge on calibrated bounds or conservative repeated evidence, not only $\bar\varphi$ and count. | **No additional experimental arm** if incorporated before the planned runs. |
| M4 | Add baseline write/update, a dedicated exploration slot or randomized forced inclusion, shadow-RIT semantics, fixed pool assignment, and warm-start details to Algorithm 1. | **No new experiment.** |
| M5 | Split labels into fit/calibration/development/final-audit roles, or use nested cross-fitting; keep final audit sealed. | Usually **no new data**, though label budget may need expansion after power analysis. |
| M6 | Keep C1–C4 as the only claim vocabulary; move reward portability, transfer, Pareto knee, and broad boundary trends to secondary or appendix analyses. | **Pure re-scoping; no new experiment.** |
| M7 | State a baseline-fidelity checklist and distinguish exact reproductions from standardized credit variants. | Within the **existing planned baseline work** if fixed before running. |

## 6. Positioning / missing related-work families

The eventual related-work review should cover these families, without necessarily expanding the main narrative:

1. **Difference rewards and counterfactual credit assignment**, including multi-agent and reinforcement-learning settings.
2. **Causal/contextual bandits and adaptive experimentation**, especially inference under changing policies.
3. **Causal recommendation and exposure/slate debiasing**, closely related to retrieval-induced selection bias.
4. **Cooperative-game attribution and interaction indices**, including redundancy, complementarity, group Shapley, and coalition sampling.
5. **Sequential inference under non-stationarity**, including anytime-valid inference, drift detection, and recalibration.
6. **Continual-learning interference and memory management**, beyond agent-memory systems specifically.
7. **RAG context attribution, context pruning, retrieval utility, and counterfactual context evaluation.**
8. **Uncertainty-aware selective prediction and safe policy updates**, relevant to eviction and merging.

The paper should avoid claiming that reward-driven managers are merely correlational until each method's exploration, counterfactual baselines, and reward construction have been checked.

## 7. Visual review from the PDF

- The PDF is nine pages, anonymous, and cleanly compiled. I found **no overfull boxes or broken references**; the log contains only underfull-box warnings.
- Placeholder figures are readable and honest. Captions clearly distinguish planned from measured content.
- Figure and table numbering is correct and monotonic.
- Table 1 is structurally readable, but S1–S5 and W-A/LME/LCM need an explicit key. Fourteen nearly identical TBD rows make it visually heavy.
- Table 4 is too dense: narrow paragraph columns cause excessive wrapping and make the decision rules difficult to scan. It should be simplified or moved to an appendix.
- Algorithm 1 is legible, but line 9 has poor spacing/wrapping, and the long state/input lines are crowded. More importantly, the visible algorithm exposes the missing write and exploration operations.
- Float placement deteriorates badly at the end:
  - The case-study sentence from page 7 is completed by the isolated words "can repair." only after Tables 3–4 on page 8.
  - Limitations and Conclusion begin on page 8 before Tables 5–6 and Figure 6 appear on page 9.
  - The final conclusion word is split across that float interruption, with the concluding fragment stranded below Figure 6.
  - Page 9 has substantial unused whitespace.

Move Tables 4–6 to the appendix or force them before Limitations; keep Figure 6 with the case-study subsection. The final paper should not allow floats to appear after the conclusion begins.

## 8. Verdict

**Almost.** The paper is not ready merely after replacing TBDs; the formal target and protocol should be repaired before experiments run.

The three highest-leverage changes are:

1. **Resolve removal vs pad-replacement vs Shapley/group credit, and correct the redundancy/complementarity error.**
2. **Lock the audit population, aggregation, CTI, inference unit, data partitions, and exact claim gates.**
3. **Restore one claim vocabulary—C1–C4—and make Algorithm 1 a complete, uncertainty-aware retrieve–execute–write loop.**

</details>
