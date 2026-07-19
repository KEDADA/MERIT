# Experiment Plan — MERIT（claim-driven 实验路线图）

**Problem**：自进化 agent 记忆系统随部署时长退化，根因是记功信号为 correlational（co-occurrence），
使零/负贡献的 *superstitious memories* 被系统性强化并占据检索位。
**Method Thesis**：把记功从「观察性研究」升级为「随机对照试验」——`RIT` 采因果标签 → `ACA` 摊销为 O(1)-per-event attributor →
两个极简 consumers（credit governance + scope-gated retrieval）消费同一信号，使因果记功在**在线、非平稳、闭环**记忆系统中可负担、可消费。
**Date**：2026-07-19（latest revision UTC `20260719_045459`；原始版本 `20260719T043340Z` 保留）

> **证据纪律（DRAFT_POLICY 约束，本文件逐条遵守）**：C1–C4 全为 `PLANNED-EVIDENCE`，
> Observation 1 为 identity、Conjecture 1 为 `HYPOTHESIS`；实验**尚未执行**；
> 本文件只规划证据、不声称证据；所有量指向已登记 `[[TBD:...]]` 占位符（账本 241 个 ID，未新增）；
> 成本只写公式或「待测项」，不虚构 GPU-hours / 运行时间 / 样本量 / 预算；
> 所有 `USER_APPROVAL_REQUIRED` 保持未决，仅给 recommendation + rationale + alternative；
> 措辞一律 "we will test whether…"，C1 用非因果动词（accumulates under / is associated with）。
> 本文件**不修改**论文源 / 协议 / 账本 / reviews；不联网；不运行实验；不调用 `/run-experiment`。

## Confirmed Execution Resource

- **USER-CONFIRMED**：实际可用资源为 **8×NVIDIA H20**；该事实仅覆盖执行计划中源方案暂定的 `8×A100-80G`，不修改冻结的 `source_proposal.md`。
- 每卡显存、驱动/CUDA/PyTorch、CPU、RAM、磁盘和 GPU 互联仍待只读系统盘点；不得从型号名推测。
- 在完成环境盘点前，不承诺可运行的模型并行方案、吞吐量、GPU-hours 或最大模型配置。

---

## Claim Map

| Claim | 为何重要（Why It Matters） | Minimum Convincing Evidence | 目标 table/figure | Gate（Table 4 `tab:hypotheses-map`） | Failure Action | Linked Blocks |
|---|---|---|---|---|---|---|
| **C1**（T2，揭示） | 若 correlational credit 不会自我纠正、且 superstition 随 t 积累，则「换信号」这一动机成立——全文钩子 | 在 ReasoningBank-/MemRL-style banks 上做 RIT 审计：`CCC` 低 **且** `SR@k` 随部署时长上升；并排除两替代解释（测量噪声 split-half、记忆整体无用 φ>0-subset removal drop） | `fig:diagnostic-baseline`(Fig 2)；Observation 1 / Conjecture 1 | **G-C1**：SR 斜率 CI 排除 0（上升）**且** memory-level `CCC(Û,Φ̃)` 低于界 | 收窄 C1 至 heterogeneous streams（不硬写） | B2（主）, B1 |
| **C2**（T1，核心） | 若 ACA 能在 O(1) 下逼近 RIT 标签并优于 correlational baseline，则「可负担的即时条件检索贡献估计」这一主贡献成立 | held-out event-level `CCC(φ̂,φ̃)` 优于 baseline；memory-level `CCC(φ̄,Φ̃)`；calibration（reliability + `ECE_ACA_HELDOUT`）；split-half 可靠；成本落在上限内 | `fig:mechanism-recovery`(Fig 5a)；`tab:ablation`(Table 3) | **G-C2**（ROUND2：**合取**）：ACA-over-baseline 下界改善 ∧ event-level CCC ∧ memory-level CCC ∧ calibration ∧ cost 上限；`ρ≥0.6` 为 `SOURCE-DEFAULT` gate | C2 unsupported / revise scope | B3（主）, B6（次要） |
| **C3**（T1） | 若同一信号被极简规则消费即可压平 SR、降低 CTI，则「一个信号、直接可消费」成立，且增益可定位到信号而非管道 | A2（swap interventional→co-occurrence，增益应消失）、A3（no scope，CTI 应回升）、A4（no governance，SR 斜率应回升）；`CTI` 度量 | `tab:ablation`(Table 3)；`fig:mechanism-recovery`(Fig 5b) | **G-C3a**（Full-vs-A4 SR 斜率差 CI 排除 0）/ **G-C3b**（CTI 降低 CI 排除 0）；Holm 校正。**G-C3c reward portability 为非阻塞次要检查** | 丢弃对应核心子 claim；reward null 仅报告不具可移植性 | B4（主）, B5（次要） |
| **C4**（实证） | 若跨 4 类基准 / 3 backbones / 3 seeds MERIT 在**低 token 开销**下优于最强 baseline 且闭环统计量回收，则端到端有效性成立 | Table 1 主表 AVG gain over **simultaneous max-baseline**（Holm）；效率 Pareto；机制统计量 `SR`/`CCC` 闭环回收 | `tab:main-results`(Table 1)；`tab:efficiency`(Table 6)；`fig:streaming-efficiency`(Fig 4)；`fig:mechanism-recovery`(Fig 5) | **G-C4**（ROUND2：**合取**）：AVG gain over simultaneous max-baseline，Holm 校正，CI 排除 0 ∧ 低 token 开销 gate | report parity / revise scope | B1（主）, B7 |

**附加理论承诺（非编号 claim）**：**Observation 1** = leave-one-out 分解 identity（非 conjecture，无需实验）；
**Conjecture 1** = feedback superstition-equilibrium（`HYPOTHESIS`，形式化 + 人工核验，无实验回填）。

**MAX_PRIMARY_CLAIMS 说明**：主贡献是 C2（可负担的因果记功，T1 core）；C1 为最锋利的支撑 claim（T2 现象）。
C3、C4 是 C2 的直接下游（消费者有效性 + 端到端）。四者不可分割地构成 A 修复型单一叙事，故保留 C1–C4 全集，
但**主战场**是 C2/C3 的 novelty-isolation（B3/B4）与 C4 主表（B1）。

---

## Paper Storyline

- **Main paper must prove（MUST-RUN 覆盖）**：
  - C1 诊断（B2 → Fig 2）：correlational credit 不自我纠正、superstition 随 t 积累。
  - C2 保真（B3 → Fig 5a / Table 3）：ACA 在 O(1) 下回收因果信用，优于 baseline。
  - C3 核心消费者（B4 → Table 3 / Fig 5b）。
  - C4 主结果（B1 → Table 1）+ 效率（B7 → Table 6 / Fig 4）。
- **Appendix can support（NICE-TO-HAVE）**：
  - frontier necessity（B6：usage-feature A5、A-judge）——回答「现代归因器是否必要」。
  - signal portability（B5 → Table 2）——reward-swap 是非阻塞次要检查。
  - boundary & scaling（B8：32B→235B、zero-shot transfer、H5 三轴趋势）。
  - failure / case study（B9：Fig 6 + 残余失败构成）。
- **Experiments intentionally cut（CUT，不进 paper 主线）**：
  - full/exact Shapley 采样 → 仅作附录 A7 边界变体（ROUND2：放弃 individual-Shapley claim）。
  - RL manager 升级为主方法 → 降级为 B5 reward-swap 插件（§0 减法测试已记录）。
  - cross-modality transfer（`NOT SPECIFIED IN SOURCE`）→ 明确排除于 C1–C4。
  - no-pad 实验臂 → ROUND2 已批准**不新增**，且不创建 `PILOT_NOPAD_REMOVAL_DELTA`。

---

## Experiment Blocks

> 每个 block 的 metrics/成本均指向已登记占位符；数值一律待实验回填。
> 复用 PRE_RUN_PROTOCOL 的 two-stage 时间线；`USER_APPROVAL_REQUIRED` 项在下方「仍需用户决定」集中列出，此处仅标注依赖。

### Block B0：Sanity / 管道与指标正确性
- **Claim tested**：无（门控全部下游 blocks）。
- **Why this block exists**：指标口径错误会污染 C1–C4 全部证据；先证明 replayable 配对重跑与统计脚本正确。
- **Dataset / split / task**：ALFWorld + HotpotQA 各一条 replayable 短流的 toy split（少量任务）；一个冻结快照。
- **Compared systems**：仅 pipeline 自检（ReasoningBank-style 复现 + RIT 脚本），无正式对比。
- **Metrics（口径自检，非结果）**：`CCC(s,φ)` = Spearman(signal, RIT φ)；`SR@k(s)` = top-k%-by-s 中 φ≤0 比例；`CTI = Acc_B(B-only) − Acc_B(A∪B)`；judge 一致性口径 `[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]`（抽检流程自检）。
- **Setup details**：backbone `Qwen3-32B`；固定种子配对重跑（同初始状态 removal vs full）；paired-LOO `K=5`（Stage-1 值）；neutral-pad 占位机制在位。
- **Success criterion**：同初始状态配对重跑逐位可复现；三个指标脚本在 toy split 上给出可解释、方向正确的输出；一次 overfit/toy 检查通过。
- **Failure interpretation**：任一指标脚本不可复现或方向反 → 停在 M0 修管道，不进入 M1。
- **Table / figure target**：无（内部 sanity），但为 Fig 2 / Fig 5 的坐标与统计口径锁定基础。
- **Priority**：MUST-RUN。

### Block B1：Main anchor result（主表，C4）
- **Claim tested**：C4（端到端优于最强 baseline，低开销）。
- **Why this block exists**：Table 1 是全文 anchor；先设计主表再加消融。
- **Dataset / split / task**：4 类基准 **categories** — Evo-Memory streams S1–S5、WebArena-Lite、LongMemEval、LoCoMo。**S1 = 单域 ALFWorld、S5 = 混流**（`SOURCE-DEFAULT`）；**S2–S4 身份 `NOT SPECIFIED IN SOURCE`（USER_APPROVAL_REQUIRED）**。
- **Compared systems（`tab:main-results` 14 行，含 `MAIN_RBANKMATTS_*`）**：No-Memory ReAct、Full-History、Mem0、A-MEM、AWM、ReasoningBank、SkeMex、Memory-R1、Mem-α、MemRL、Reflexion、ReasoningBank+MaTTS、**MERIT (ours)**、RIT-Full（intervention reference）。`MAX_BASELINE_FAMILIES` 精神：以少数强 baseline 为主，忠实复现（RM7 baseline-fidelity checklist）。
- **Metrics**：决定性 — AVG（two-stage macro-average，§4.3）over **simultaneous max-baseline**（§4.5，Holm §4.6）。次要 — 各 category 分数、per-cell。
- **Setup details**：backbones `Qwen3-32B`(主)/`Qwen3-235B-A22B`(scale)/`GPT-5.1`(closed-source 附加行)；ACA=`Qwen3-Embedding-4B`+2-layer MLP（`[[TBD:ACA_TRAINABLE_PARAMS]]`）；统一 codebase；同 retriever、top-k=4、同预算；seeds `{13,42,2026}`（`SOURCE-DEFAULT`，正式 seed 数**由 pilot power 计算**）；cold-start + warm-up `W`（USER_APPROVAL_REQUIRED）；推断单位 = **seed/deployment run**（ROUND2）。
- **占位符**：126 个 `[[TBD:MAIN_<METHOD>_<S1..S5|WAL|LME|LCM|AVG>]]`；headline `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`；`[[TBD:MAIN_GAIN_SINGLE_DOMAIN]]`→`[[TBD:MAIN_GAIN_MIXED_STREAM]]`；`[[TBD:MERIT_FRACTION_OF_RITFULL_GAIN]]`；`[[TBD:MAIN_GPU_HOURS_PER_RUN]]`。
- **Success criterion（G-C4 合取）**：MERIT AVG > simultaneous max-baseline（Holm，CI 排除 0）**且**满足低 token 开销 gate。
- **Failure interpretation**：无显著 AVG gain → report parity / 收窄 scope（不删负结果）。
- **Table / figure target**：`tab:main-results`(Table 1)。
- **Priority**：MUST-RUN。

### Block B2：Pilot / Diagnostic（C1，RIT 审计）
- **Claim tested**：C1（superstition 随 t 积累，correlational credit 不自我纠正）。
- **Why this block exists**：提供全文钩子的干预证据；同时产出 Stage-1 方差用于冻结正式 sizing。
- **Dataset / split / task**：两条 **replayable** 流 ALFWorld + HotpotQA，各 500 任务；snapshot grid `t∈{100,200,300,400,500}`（`SOURCE-DEFAULT`）；train/audit 按 **task-level** split，AUDIT 为 probability sample（§3.1）；四类数据角色 fit/calibration/development/sealed-final-audit（ROUND2）。
- **Compared systems**：ReasoningBank-style（启发式记功）+ MemRL-style（MC 学习记功），忠实复现（RM7）。
- **Metrics**：memory-level `CCC(Û,Φ̃)`；`SR@20%` 随 t（三分：harmful/null/positive）；控制1 split-half 可靠性；控制2 φ>0-subset removal drop。
- **Setup details**：`Qwen3-32B`；paired-LOO `K=5`（Stage-1）；per-trial memory subset（§3.4，USER_APPROVAL_REQUIRED）；neutral-pad 位置混淆控制；**neutral-pad 等价验证** `[[TBD:PILOT_NEUTRAL_PAD_VALIDATION]]`（决定 removal vs pad-replacement 措辞，ROUND2 Part C）。
- **占位符**：`[[TBD:PILOT_CCC_REASONINGBANK_T500]]`、`[[TBD:PILOT_CCC_MEMRL_T500]]`、`[[TBD:PILOT_SR20_T100]]`、`[[TBD:PILOT_SR20_T500]]`、`[[TBD:PILOT_SR20_HARMFUL_T100/T500]]`、`[[TBD:PILOT_SR20_NULL_T100/T500]]`、`[[TBD:PILOT_SPLITHALF_PHI_RELIABILITY]]`、`[[TBD:PILOT_UTILITY_SUBSET_REMOVAL_DROP]]`、`[[TBD:PILOT_AUDIT_SUPPORT_COVERAGE]]`、`[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]`、`[[TBD:PILOT_TOTAL_TOKEN_COST]]`、`[[TBD:RIT_ROLLOUT_EQUIV_PER_EVENT]]`。
- **Success criterion（G-C1）**：`SR@20%` 斜率 CI 排除 0（上升）**且** memory-level CCC 低于界（source 记 `CCC>0.5` 为 falsifier）。
- **Failure interpretation**：`CCC>0.5` 或 `SR@k` 不随 t 上升 → C1 证伪 → 收窄至 heterogeneous streams（不硬写）。neutral-pad 等价未过 → 全局措辞降级为 "pad-replacement contribution"。
- **Table / figure target**：`fig:diagnostic-baseline`(Fig 2)；喂 Observation 1 / Conjecture 1。
- **Priority**：MUST-RUN。

### Block B3：ACA fidelity & calibration（C2，核心）
- **Claim tested**：C2（O(1) 摊销归因回收因果信用）。
- **Why this block exists**：C2 是主贡献；held-out 保真 + 校准是「可负担的因果记功」证据核心。
- **Dataset / split / task**：sealed held-out AUDIT pool（ACA 从未训练的标签，§3.1）；四角色 split，final audit 对 model/threshold/calibration/stopping 选择**盲**（RM5）。
- **Compared systems**：ACA(MERIT) vs correlational baseline；消融 A1（no recalibration）、A5（no usage-behavior features）。
- **Metrics**：决定性 — event-level `CCC(φ̂,φ̃)`、memory-level `CCC(φ̄,Φ̃)`；calibration reliability diagram + `[[TBD:ECE_ACA_HELDOUT]]`。次要 — split-half、per-domain calibration、φ≈0 符号稳定性。
- **Setup details**：ACA 特征三组（query rep、memory rep `Qwen3-Embedding-4B` frozen、usage-behavior features）；2-layer MLP 回归 φ̂∈[−1,1]；Huber loss（`δ=0.1` provisional，注意与 SR 的 δ、governance dead-zone ±0.02 三者**不得混用**）；每 100 任务 recalibration + isotonic。
- **占位符**：`[[TBD:ACA_HELDOUT_CCC_T500]]`、`[[TBD:ECE_ACA_HELDOUT]]`、`[[TBD:ABL_A1_*]]`、`[[TBD:ABL_A5_*]]`。
- **Success criterion（G-C2 合取）**：held-out ACA-over-baseline 下界改善 ∧ event-level CCC（`ρ≥0.6` SOURCE-DEFAULT）∧ memory-level CCC ∧ calibration ∧ cost 上限，全部满足。
- **Failure interpretation**：held-out `ρ<0.6` 或任一合取项不过 → C2 undercut，revise。
- **Table / figure target**：`fig:mechanism-recovery`(Fig 5a)；`tab:ablation`(Table 3) 的 CCC 列。
- **Priority**：MUST-RUN。

### Block B4：Consumers / Novelty isolation（C3）
- **Claim tested**：C3（信号直接可消费；增益来自信号而非管道）。
- **Why this block exists**：**A2 是 signal-localization 关键**——同管道换回共现信号，增益应消失。
- **Dataset / split / task**：主基准子集 + CTI 的 A/B 混流审计（A/B 域对 USER_APPROVAL_REQUIRED）。
- **Compared systems（`tab:ablation` 行）**：Full、A2（swap causal→co-occurrence，capacity-matched control，复用 `ABL_A2_*`）、A3（no scope）、A4（no governance）。
- **Metrics**：AVG、ΔAVG、`SR@20%`(t=500)、CCC(held-out)、`CTI`。governance 用**保守 calibrated bound + 重复证据**（RM3），非点估计。
- **Setup details**：governance 三规则（evict/merge/quarantine，阈值 provisional，dead-zone ±0.02）；scope-gated retrieval `score = α·rel + β·(sim(q,proto⁺)−sim(q,proto⁻)) + γ·φ̄`（(α,β,γ)=(1.0,0.5,0.3) provisional）；Algorithm 1 完整 retrieve–execute–**write** loop（RM4）。
- **占位符**：`[[TBD:ABL_A2_*]]`、`[[TBD:ABL_A3_*]]`、`[[TBD:ABL_A4_*]]`、`[[TBD:ABL_FULL_*]]`、`[[TBD:SR_MERIT_T500]]`、`[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]`。
- **Success criterion**：G-C3a（Full-vs-A4 SR 斜率差 CI 排除 0，Full 更平）；G-C3b（CTI 降低 CI 排除 0）；**A2 gate**：换共现信号后增益消失。
- **Failure interpretation**：A2 增益仍在 → 贡献未定位到信号；G-C3a/b 不过 → 丢弃对应子 claim。
- **Table / figure target**：`tab:ablation`(Table 3)；`fig:mechanism-recovery`(Fig 5b)。
- **Priority**：MUST-RUN。

### Block B5：Simplicity check / signal portability（C3，减法）
- **Claim tested**：C3（「信号对了，简单阈值规则就够」；同一信号可移植到 RL 管理器）。
- **Why this block exists**：defend simplicity——对照刻意拒绝的更复杂变体（RL manager）。
- **Dataset / split / task**：reward-swap 运行（GRPO 设置不变，仅替换奖励）。
- **Compared systems**：Memory-R1 / Mem-α × {orig reward, φ̂ reward}。
- **Metrics**：AVG、Δ（lift）。
- **Setup details**：把 φ̂ 作为 per-operation 去混淆奖励替换 outcome-level 奖励；GRPO 超参不变；RL 定位为**互补**（ROUND2 RM6），仅在证据支持处声称优势。
- **占位符**：`[[TBD:PLUGIN_MEMR1_ORIG_AVG]]`、`[[TBD:PLUGIN_MEMR1_PHI_AVG]]`、`[[TBD:PLUGIN_MEMALPHA_ORIG_AVG]]`、`[[TBD:PLUGIN_MEMALPHA_PHI_AVG]]`、`[[TBD:REWARD_SWAP_MEMORY_R1_GAIN]]`、`[[TBD:REWARD_SWAP_MEMALPHA_GAIN]]`。
- **Success criterion（G-C3c）**：reward-swap lift CI 排除 0（Holm 校正）。
- **Failure interpretation**：lift 不显著 → report null portability（不夸大）。
- **Table / figure target**：`tab:reward-swap`(Table 2，body 摘要 + 附录全表)。
- **Priority**：NICE-TO-HAVE（ROUND2 已批准为次要分析；G-C3c 不阻塞 C3/C4）。

### Block B6：Frontier necessity check（C2，NICE-TO-HAVE）
- **Claim tested**：C2 辅证（现代归因器组件是否必要，而非装饰）。
- **Why this block exists**：frontier 必要性——对照最强的更简单/更老替代。
- **Dataset / split / task**：held-out AUDIT pool。
- **Compared systems**：ACA（usage-behavior features + MLP）vs A5（仅 (q,m) 语义特征）vs A-judge（LLM self-judge 替代 RIT 标签，复现自我确认陷阱）。
- **Metrics**：CCC、AVG、ΔAVG、calibration。
- **Setup details**：与 B3 共享 ACA 训练管道；A-judge 为消融变体。
- **占位符**：`[[TBD:ABL_A5_*]]`、`[[TBD:ABL_AJUDGE_*]]`。
- **Success criterion**：ACA 显著优于 A5 与 A-judge（说明 usage-behavior 特征 + RIT 标签必要）。
- **Failure interpretation**：A5/A-judge 追平 ACA → 现代组件非必要，需在正文诚实弱化 C2 的组件必要性论述。
- **Table / figure target**：`tab:ablation`(Table 3)。
- **Priority**：NICE-TO-HAVE（附录优先；不阻塞主线）。

### Block B7：Efficiency / Pareto（C4，H4）
- **Claim tested**：C4/H4（低开销 Pareto 前沿；RIT budget 小 p 即饱和）。
- **Why this block exists**：低 token 开销 gate 是 G-C4 合取的一半；把「affordable」变成公式 + 实测点。
- **Dataset / split / task**：主基准；budget sweep `p∈{1,2,5,10}%`。
- **Compared systems（`tab:efficiency`）**：baseline(1×)、MERIT、A1、RIT-Full。
- **Metrics**：relative token cost（log 轴）、AVG、ACA latency/event、extra VRAM、RIT overhead；Pareto knee（marginal AVG gain per doubling token cost < `τ_knee`，USER_APPROVAL_REQUIRED）。
- **Setup details**：成本用 PRE_RUN_PROTOCOL §3.7 公式预算（见下节 Compute Budget），实测回填占位符。
- **占位符**：`[[TBD:EFF_BASELINE_AVG]]`、`[[TBD:EFF_MERIT_AVG]]`、`[[TBD:EFF_A1_AVG]]`、`[[TBD:EFF_RITFULL_AVG]]`、`[[TBD:MERIT_RELATIVE_TOKEN_COST]]`、`[[TBD:A1_RELATIVE_TOKEN_COST]]`、`[[TBD:RITFULL_RELATIVE_TOKEN_COST]]`、`[[TBD:ACA_SCORING_LATENCY_MS]]`、`[[TBD:ACA_VRAM_OVERHEAD_GB]]`、`[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]`、`[[TBD:TOKEN_OVERHEAD_PERCENT]]`、`[[TBD:FULL_RIT_COST_MULTIPLIER]]`、`[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]`。
- **Success criterion**：核心 C4 成本上限通过；次要 G-H4 仅在 Pareto knee 按 `τ_knee` 规则存在且 MERIT 位于前沿拐点时报告。
- **Failure interpretation**：成本上限失败 → C4 低开销子主张失败；仅无 knee / MERIT 非 Pareto 最优 → 丢弃次要 Pareto claim，不阻塞其他 C4 证据。
- **Table / figure target**：`tab:efficiency`(Table 6)；`fig:streaming-efficiency`(Fig 4)。
- **Priority**：成本/开销 profiling 为 MUST-RUN（支撑 C4）；Pareto-knee/H4 解释为 NICE-TO-HAVE、非阻塞。

### Block B8：Boundary & Scaling（H3/H5，NICE-TO-HAVE）
- **Claim tested**：H3（scope 迁移）、H5（增益边界）。
- **Why this block exists**：诚实刻画增益边界，rebuttal 弹药；非阻塞主 claim。
- **Dataset / split / task**：32B→235B scaling；ACA 在 ALFWorld+HotpotQA 训练、WebArena zero-shot transfer；bank-size / heterogeneity / redundancy 三轴。
- **Compared systems**：MERIT 跨 backbone / 跨环境。
- **Metrics**：`SCALING_GAIN_32B`→`SCALING_GAIN_235B`；transfer `CCC`；H5 三轴趋势（**redundancy 轴保持 `EVIDENCE GAP`，无 ID**）。
- **占位符**：`[[TBD:SCALING_GAIN_32B]]`、`[[TBD:SCALING_GAIN_235B]]`、`[[TBD:ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA]]`、`[[TBD:H5_GAIN_SMALL_BANK_LT100]]`、`[[TBD:H5_GAIN_SINGLE_DOMAIN]]`。
- **Success criterion（G-H3 / G-H5）**：每轴预测 sign 成立（CI）。
- **Failure interpretation**：scope H5 至通过的轴；transfer 不成立 → 弱化 H3。
- **Table / figure target**：正文趋势线 + 附录 per-slice。
- **Priority**：NICE-TO-HAVE。

### Block B9：Failure analysis / Case study（NICE-TO-HAVE）
- **Claim tested**：无新 claim；诚实展示残余失败与 AS3 边界。
- **Why this block exists**：qualitative diagnosis——方法仍缺什么。
- **Dataset / split / task**：case-study logs（成功例 vs superstitious 例；redundant/substitutable 例，ROUND2 relabel）。
- **Compared systems**：correlational accumulation vs RIT vs governance。
- **Metrics**：`[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]`；`[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]`；`[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]`(Fig 1 派生)。
- **Setup details**：group-intervention fallback 对 redundant/substitutable 记忆（A7 exploratory，无数值保证）。
- **Success criterion**：案例清晰展示 superstition eviction 时点与残余失败构成。
- **Failure interpretation**：不构成证据风险，仅叙事。
- **Table / figure target**：`fig:case-study`(Fig 6)；`fig:problem-solution`(Fig 1)。
- **Priority**：NICE-TO-HAVE。

---

## Run Order and Milestones

| Milestone | Goal | Runs（Blocks） | Decision Gate（stop/go） | Cost | Risk / Mitigation |
|---|---|---|---|---|---|
| **M-1 Environment** | 盘点 8×H20 执行环境 | R000 | 记录显存、软件栈、主机资源与拓扑，完成最小通信/分配自检 → GO；否则先修环境 | 待测 | 型号信息不足以决定并行策略 / 只采用实测盘点 |
| **M0 Sanity** | 管道 + 指标正确 | R001–R002 / B0 | 配对重跑逐位可复现 ∧ CCC/SR@k/CTI 脚本过 toy → GO；否则修管道，不进 M1。R003 不阻塞非 judge 路径 | 待测（无虚构） | 指标口径错污染全下游 / 先锁 Fig2-Fig5 同坐标同统计 |
| **M1 Baseline** | 仅复现 pilot 所需代表 baseline | R010–R011 | ReasoningBank/MemRL 复现落在 fidelity checklist（RM7）内 → GO | `[[TBD:MAIN_GPU_HOURS_PER_RUN]]`（待测） | baseline 不忠实 → C1 可比性 / 用 source-faithful vs standardized-wrapper 分列 |
| **M2 Pilot** | C1 诊断 + Stage-1 方差 | B2 | **Gate-C1**：`CCC>0.5` 或 `SR@k` 不升 → 证伪 → 收窄 C1（不硬写）；否则 GO。neutral-pad 未过 → pad-replacement 降级 | §3.7 公式 + `[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]`/`[[TBD:PILOT_TOTAL_TOKEN_COST]]`（待测） | pilot 方差过大 → Stage-2 sizing 变贵 / 分层分配 |
| **M2.5 Freeze** | 冻结 K/n^audit/seeds | 由 Stage-1 方差**计算** | 冻结值使 CI half-width < pre-pilot δ 且 power≥target → 锁定；**pilot 数据不得进 confirmatory gate** | —（计算，非运行） | 违反 independence → CI 失效 / 硬独立规则 |
| **M3 Main** | 完整 baseline 矩阵 + C4 主结果 + 核心效率 | R012 + B1 full + B7 core | **Gate-C4**（合取）：max-baseline Holm CI 排除 0 ∧ 低开销 gate；否则 report parity / revise | `[[TBD:MAIN_GPU_HOURS_PER_RUN]]`（待测） | pilot 通过后才展开完整 baseline，避免提前消耗算力 |
| **M4 Decision** | 核心 novelty 消融 | B3, B4, (B6) | **Gate-C2**（合取，`ρ≥0.6`+…）∧ **A2 gate**（换信号增益消失）∧ **G-C3a/b**；G-C3c 不阻塞 | 待测 | ACA 噪声 → C2；A2 不消失 → 信号未定位 / §8.5 校准小节 |
| **M5 Polish** | 次要 portability/边界/机制/案例 | B5, B8, B9 + B7/H4 | judge-dependent runs 前须先通过 R003；各次要预测仅在成立时报告；redundancy 保持 `EVIDENCE GAP` | 待测 | 次要分析不得延迟或改写核心结论 |

**执行顺序总述**：`environment(M-1) → sanity(M0) → representative baselines(M1) → pilot(M2) → freeze(M2.5) → full baselines+main(M3) → core ablation/decision(M4) → secondary analysis/polish(M5)`。
与 PRE_RUN_PROTOCOL 的 two-stage fixed design 对齐：pre-pilot 锁阈值（δ/MEI/pilot K=5/split/subset/pad）→ Stage-1 独立 pilot 估方差（M2）→ Stage-2 冻结 K/n/seeds（M2.5）→ confirmatory（M3+，数据与 pilot 不相交）。

---

## Compute and Data Budget

> **纪律：只写公式或待测占位符，不虚构任何数值。**

- **Confirmed hardware**：8×NVIDIA H20（USER-CONFIRMED）。在 M-1 盘点前，不假定显存、互联、并行方案或可承载模型规模；所有性能与成本均以该机器实测。

- **RIT 摊销成本公式（PRE_RUN_PROTOCOL §3.7）**：
  `cost_per_event ≈ p_task · (m·K + K_ctrl − r_reuse) / E_task`
  其中 `m`=每 trial 采样记忆数（§3.4，待定）、`K`=**冻结的 formal** rollouts per LOO（§3.5，two-stage 计算）、
  `K_ctrl`=shared control rollouts、`r_reuse`=复用的 deployment rollouts、`E_task`=每任务检索事件数、
  `p_task`=trial 采样率（`SOURCE-DEFAULT` 5%，占位 `[[TBD:RIT_SAMPLING_PROB_PERCENT]]`）。
  实测回填 → `[[TBD:RIT_ROLLOUT_EQUIV_PER_EVENT]]`；预算上限 ε = `[[TBD:RIT_BUDGET_EPSILON_PERCENT]]`（USER_APPROVAL_REQUIRED）。
- **Total estimated GPU-hours**：**待测** → `[[TBD:MAIN_GPU_HOURS_PER_RUN]]` ×（backbones × categories × 冻结 seed 数）。seed 数由 pilot power **计算**，不预设。
- **Pilot budget**：**待测** → `[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]`、`[[TBD:PILOT_TOTAL_TOKEN_COST]]`（结构：snapshot 数 × 每快照 (query,retrieved-set) 对数 × subset × K × 系统数，各因子 USER_APPROVAL_REQUIRED / 待测）。
- **效率占位符**：`[[TBD:MERIT_RELATIVE_TOKEN_COST]]`、`[[TBD:RITFULL_RELATIVE_TOKEN_COST]]`、`[[TBD:FULL_RIT_COST_MULTIPLIER]]`、`[[TBD:ACA_SCORING_LATENCY_MS]]`、`[[TBD:ACA_VRAM_OVERHEAD_GB]]`、`[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]`、`[[TBD:TOKEN_OVERHEAD_PERCENT]]`。
- **Data preparation needs**：replayable 快照接口（ALFWorld 原生、WebArena 用 docker commit）；4 类基准 category 构造；S2–S4 身份 + heterogeneity bins（USER_APPROVAL_REQUIRED）；A/B 域对（USER_APPROVAL_REQUIRED）；四角色数据 split（fit/calibration/development/sealed-final-audit）。
- **Human evaluation needs**：judge–human 一致性抽检 200 例 → `[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]`（口径待定）。
- **Biggest bottleneck**：RIT 标签采集（paired-LOO rollouts）在 replayable 任务上的 rollout 预算；由 pilot 方差决定的冻结 K/n 是主成本驱动。

---

## Risks and Mitigations

- **[R1 归因噪声]** ACA φ̂ 在 φ≈0 附近符号不稳 → 治理阈值留 dead-zone ±0.02 + 保守 bound + 重复证据（RM3）；§8.5 校准小节（reliability + ECE + split-half）。
- **[R2 pilot optional-stopping 偏差]** → two-stage fixed design，Stage-2 冻结后单次 BCa，pilot 数据不进 confirmatory gate（硬独立规则）。
- **[R3 baseline 不忠实]** → RM7 fidelity checklist；source-faithful 与 standardized-wrapper 分列，主表脚注标注「复现/引用」。
- **[R4 winner's curse]** → 不后选最强 baseline；simultaneous max-baseline 对比 + Holm。
- **[R5 removal vs pad-replacement 语义]** → neutral-pad 等价验证；未过则全局降级为 pad-replacement 措辞（ROUND2 Part C）。
- **[R6 增益不足撑 headline]** → §13 迭代环：先回改 Idea Card（降 headline、把重心移向 C1/C2 机制故事），再改文；不删负结果。
- **[R7 依赖 replayability（AS2）]** → 明确边界；WebArena zero-shot transfer 证明 ACA 可脱离标签环境使用。

---

## Final Checklist

- [x] Main paper tables 覆盖：Table 1(B1)、Table 2(B5)、Table 3(B3/B4/B6)、Table 6(B7)；Fig 2(B2)、Fig 5(B3/B4)、Fig 4(B7)。
- [x] Novelty 隔离：A2（swap causal→co-occurrence）为 signal-localization key（B4）。
- [x] Signal portability：B5 reward-swap 为 NICE-TO-HAVE 非阻塞检查；full Shapley/RL 升级已 CUT。
- [x] Frontier 贡献辩护或明确不主张：B6（usage-feature A5、A-judge）作 NICE-TO-HAVE 附录。
- [x] Nice-to-have（B5/B6/B8/B9 与 B7-H4）和 must-run（B0–B4、B7 核心成本部分）分离。
- [x] 每个实验都为某 claim/ gate 服务；无孤儿实验。
- [x] 成本仅公式或待测占位符；无虚构数值。
- [x] 所有 `USER_APPROVAL_REQUIRED` 未锁定（见下）。

---

## 仍需用户决定（`USER_APPROVAL_REQUIRED`，全部保持未决；rec + rationale + alternative）

> 复用 PRE_RUN_PROTOCOL / ROUND2 的开放项；本文件**不锁定**任何一项。

**Pre-pilot（数据前，data-free）**
1. **δ**（memory-level 最小实际意义贡献）— *Rec*：substantive 判断，pilot 前固定；*Rationale*：等价带须先于看数据；*Alt*：从可容忍 SR 误分类率反推。
2. **MEI on AVG + target power** — *Rec*：pre-register 最小可关注效应，power≥0.8；*Rationale*：防数据驱动效应目标；*Alt*：更保守 power 0.9。
3. **Stage-2 CI half-width** — *Rec*：设为 < δ；*Rationale*：sizing 目标；*Alt*：分层不同 half-width。
4. **train/audit split 比例或 fold k + AUDIT 分层设计** — *Rec*：task-level split，AUDIT probability sample；*Rationale*：防泄漏 + design-based 无偏；*Alt*：cross-fitting k-fold / temporal split。
5. **per-trial memory subset 大小 + TRAIN-pool priority 规则参数** — *Rec*：subset 1–2 + shared control 复用；*Rationale*：降 rollout 开销约一半；*Alt*：all-k（高成本 RIT-Full 参照）。
6. **neutral-pad 内容 + 等价带** — *Rec*：中性 token block + 预注册等价检验；*Rationale*：把假设变检验；*Alt*：literal empty-slot（改变估计目标）。
7. **RIT budget ε / pilot budget** — *Rec*：以 §3.7 公式 + 预算上限约束；*Rationale*：使 affordability 可证伪；*Alt*：固定 token ceiling。

**Pre-confirmatory（与 pilot 无关的设计注册）**
8. **S2–S4 stream 身份 + heterogeneity bins**（`NOT SPECIFIED IN SOURCE`）— *Rec*：S1↔S5 之间的中间混合，按 Shannon entropy 排序；*Rationale*：需可复现的异质性轴；*Alt*：其他域组合。**不猜测。**
9. **CTI A/B 域对** — *Rec*：沿 Evo-Memory 混流协议构造；*Rationale*：定义可复现；*Alt*：其他 A/B 域。
10. **max-baseline 对比统计量** — *Rec*：step-down max-T / min-p；*Rationale*：修正最大化 winner's curse；*Alt*：单一预注册 comparator。
11. **Holm α（FWER）+ BH-FDR q** — *Rec*：confirmatory 用 Holm、exploratory 用 FDR；*Rationale*：confirmatory 严格族错误控制；*Alt*：全用 Holm。
12. **warm-up W** — *Rec*：cold-start + 共享排除前缀 W；*Rationale*：防冷启动混淆；*Alt*：共享预置 bank。
13. **Pareto-knee τ_knee** — *Rec*：marginal-gain 规则；*Rationale*：使 knee 可审计；*Alt*：Kneedle 最大曲率。
14. **各 gate 的 CI/threshold 规则**（G-C1 界、G-C2 CI 规则、G-C3c 阈值等）— *Rec*：用区间而非点估计；*Rationale*：与 CI 审计政策一致；*Alt*：单侧/等价规则。

**Post-pilot（计算，非选择——仅列出以示透明）**
15. **formal K / n^audit / seed count** — 由独立 Stage-1 pilot 方差**计算**并冻结；仅 sizing 准则（2–3）需批准，这些值不猜。

**ROUND2 仍开放细项**
16. governance 置信界 + 重复规则 + dead-zone（若变）；四角色 split 比例与 label 预算；层级/块重采样细节 + 多重性族成员。
17. 占位符注册相关：SR 不确定性作单格（point±CI）还是分离 ID（§6.1 候选，未创建）。

---

## Status

**实验计划已生成；未运行任何实验；未联网；未修改论文源 / 协议 / 账本 / reviews / `source_proposal.md`；
未新增占位符 ID；未安装或调用 `/run-experiment`。所有 `USER_APPROVAL_REQUIRED` 保持未决。停止。**
