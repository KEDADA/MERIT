# KILL_ARGUMENT — MERIT (AAAI 2027), Round 2 adversarial exercise

> Detect-only. **No paper edits were made as a result of this exercise.**
> Two fresh, independent `gpt-5.6-sol` / `xhigh` threads (Reviewer Independence
> Protocol): an attack thread built the strongest rejection memo, a separate fresh
> thread adjudicated it against the actual source. Neither thread was told about
> prior review rounds, scores, the revision plan, or fix summaries.
> Artifact reviewed: `reviews/main_round1.pdf` (post-R1→R6, 9 pages) + current LaTeX.
> Attack threadId: `019f7736-479f-7150-ae02-4cd09b5bfce8` · Defense threadId: `019f773b-5dec-7ed3-8092-a7d08c5fa858` (recovery bookkeeping only).

## Attack — strongest rejection memo (verbatim)

> The most likely rejection, even under perfect results, is **estimand overclaim**: MERIT measures a conditional, immediate prompt-deletion effect but sells it as the causal-credit primitive governing persistent memory and self-evolution.
>
> 1. The leave-one-out estimand conditions on an endogenous retrieved set and frozen history, excluding future retrieval, writing, redundancy, complementarity, and policy adaptation — the effects actually relevant to retaining a memory.
> 2. The "bias" conjecture is a category error: co-occurrence utility is an outcome predictor, not necessarily an estimator of the proposed marginal effect, and the decomposition subtracts baseline solvability without establishing harmful ranking or a superstition equilibrium.
> 3. Rising SR@20% cannot identify correlational credit as the cause because every snapshot changes bank membership, exposure, and survivor composition, while null leave-one-out effects also arise from saturation and substitutes rather than superstition.
> 4. Even perfect held-out CCC and reward-swap gains validate only replayable, retrieved, common-support events under MERIT's own distribution, not unseen retrieval actions, non-replayable tasks, or the distribution induced by governance.
> 5. The novelty reduces to randomized ablation labels, a learned surrogate, and heuristic consumers, while the positioning incorrectly dismisses exploratory outcome-reward learning even though it targets policy value more relevant than itemwise deletion.
>
> The rebuttal's most vulnerable step is AS3 plus the unstated leap that bounded interaction converts immediate conditional leave-one-out credit into actionable long-horizon memory value.

## Defense — adjudication summary

| Charge | Classification | Severity if unresolved |
|---|---|---|
| Headline estimand overclaim | partially_answered | **critical** |
| 1. Conditional LOO omits retention effects | partially_answered | major |
| 2. "Bias" / superstition-equilibrium category error | **still_unresolved** | major |
| 3. SR trend does not identify the cause | partially_answered | major |
| 4. Replay / common-support / external-validity limits | **answered_by_current_text** | — |
| 5. Incremental novelty & RL positioning | partially_answered | major |
| AS3 / long-horizon leap | partially_answered | major |

**Defense's key adjudication.** The *formal* paper does not conceal the estimand —
Def. 1 conditions on the realized set and history and §3 states "the single-event
effect, *not* a long-horizon memory value; long-horizon value is out of scope." So
the memo is wrong that the leap is *wholly unstated*. But the abstract, intro,
related work, and conclusion still re-expand the target into "a memory's value,"
"full-lifecycle credit," and "the missing primitive of self-evolution," which
invites exactly the over-general reading and could be rejection-level even with
perfect numbers. Objection 4 is already handled by the paper's own scope
disclaimers. The defense also independently surfaced the **complementary-vs-redundant
case-study error** (two complementary memories holding necessary halves should have
*large* individual LOO, not near-zero; near-zero individual LOO with positive group
value is the *redundant/substitutable* case).

### STILL-UNRESOLVED CRITICAL ISSUE (from the defense)

- **Estimand/positioning mismatch:** the formal target is *immediate conditional
  retrieval contribution*, while the abstract, introduction, related work, and
  conclusion still sell it as general memory value, full-lifecycle credit, and the
  causal primitive of self-evolution. **Fixable by consistent re-scoping without new
  experiments.**

## Merge decision (auto-loop responsibility; detect-only, not applied)

Per the merge rule, still-unresolved / partially-answered points at critical
severity are carried into the Round 2 fix list (deduped against the Round 2
weaknesses), for the human to authorize later:

- **[MERGE — critical]** Estimand/positioning mismatch (kill headline + defense
  still-unresolved). Overlaps Round 2 C3 (causal wording) and M6 (one claim
  vocabulary) but is sharper: it names "full-lifecycle credit"/"missing primitive"
  over-generalization in abstract/intro/related/conclusion. Fix = re-scope wording
  to "immediate conditional retrieval contribution" everywhere; no new experiments.
- **[MERGE — major]** "Bias" category error (kill obj 2, still_unresolved). Overlaps
  Round 2 MINOR (Conjecture mixes identity + equilibrium) but the defense rates it
  major: "biased estimator" wording presumes Û is meant as an estimator of the
  contribution estimand. Fix = "composite signal that can be misaligned with
  immediate contribution"; treat equilibrium as a possible mechanism.
- **[MERGE — major]** Complementary-vs-redundant case-study error (defense, AS3
  section) — also independently raised as Round 2 CRITICAL C1. Fix = relabel the
  failure case "redundant/substitutable."
- Objections 1, 3, 5 (major, partially_answered) are recorded but not force-merged
  (not critical); they align with Round 2 M6/M7 and the causal-wording fix.

**No fixes implemented.** All items await user authorization at the checkpoint.
