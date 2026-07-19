# Experiment Tracker — MERIT

> 紧凑执行表。所有 `Status` 初始为 `TODO`；`Metrics` 列为已登记 `[[TBD:...]]` 占位符 ID（账本 241 个，未新增）。
> 本表登记的是 **35 个 run families**，使用按 milestone 分段的稀疏 ID（R000–R081），不是 82 个原子进程。待协议参数锁定和 pilot sizing 完成后，每个 family 再展开为 backbone×stream×seed×variant 的原子运行 ID。
> 未运行任何实验；`Priority`：MUST / NICE。latest revision UTC `20260719_045459`；原始版本 `20260719T043340Z` 保留。

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics（占位符 ID） | Priority | Status | Notes |
|--------|-----------|---------|------------------|-------|----------------------|----------|--------|-------|
| R000 | M-1 | 8×H20 环境盘点 | NVIDIA H20 节点（USER-CONFIRMED） | — | —（只读系统信息） | MUST | TODO | 记录每卡显存、驱动/CUDA/PyTorch、CPU/RAM/磁盘、GPU 拓扑与最小通信/分配自检；不得推测 |
| R001 | M0 | sanity：配对重跑可复现 | ReasoningBank-style 复现 + RIT 脚本 | ALFWorld+HotpotQA toy split，单快照 | —（逐位复现自检） | MUST | TODO | 门控全下游；锁 Fig2/Fig5 同坐标同统计 |
| R002 | M0 | sanity：指标脚本正确 | CCC/SR@k/CTI 计算脚本 | toy split | —（口径自检） | MUST | TODO | δ、dead-zone±0.02、Huber δ=0.1 三者不混用 |
| R003 | M0.5 | judge 一致性验证 | GPT-5.1 judge vs 人工 200 例 | 抽检子集 | JUDGE_HUMAN_AGREEMENT_KAPPA | MUST-for-judge | TODO | 只阻塞依赖 LLM judge 的最终评测，不阻塞非 judge baseline/pilot；κ 口径待定（USER_APPROVAL） |
| R010 | M1 | 复现 baseline（启发式） | ReasoningBank | 主基准 4 类 | MAIN_RBANK_S1..S5/WAL/LME/LCM/AVG | MUST | TODO | RM7 fidelity checklist |
| R011 | M1 | 复现 baseline（MC 学习） | MemRL | 主基准 4 类 | MAIN_MEMRL_S1..S5/WAL/LME/LCM/AVG | MUST | TODO | source-faithful vs wrapper 分列 |
| R012 | M3 | 复现其余 baseline 行 | NoMem/FullHist/Mem0/A-MEM/AWM/SkeMex/MemR1/Mem-α/Reflexion/RBANK+MaTTS | 主基准 4 类 | MAIN_{NOMEM,FULLHIST,MEM0,AMEM,AWM,SKEMEX,MEMR1,MEMALPHA,REFLEXION,RBANKMATTS}_* | MUST | TODO | 仅在 M2 pilot 通过后展开；14 行主表除 MERIT/RITFULL |
| R020 | M2 | C1 诊断：CCC/SR vs t | ReasoningBank + MemRL RIT 审计 | replayable 流，snapshot {100..500}，task-level split | PILOT_CCC_REASONINGBANK_T500, PILOT_CCC_MEMRL_T500, PILOT_SR20_T100, PILOT_SR20_T500 | MUST | TODO | **Gate-C1** falsifier；Fig2 |
| R021 | M2 | SR 三分（harmful/null/positive） | RIT 审计 | AUDIT probability sample | PILOT_SR20_HARMFUL_T100/T500, PILOT_SR20_NULL_T100/T500 | MUST | TODO | MAJOR-3 三分 |
| R022 | M2 | 控制1：测量可靠性 | split-half 重测 | audit 事件 | PILOT_SPLITHALF_PHI_RELIABILITY | MUST | TODO | 排除「噪声假象」 |
| R023 | M2 | 控制2：记忆整体有用 | φ>0-subset removal | audit 事件 | PILOT_UTILITY_SUBSET_REMOVAL_DROP | MUST | TODO | 坏在记功不在记忆 |
| R024 | M2 | neutral-pad 等价验证 | pad vs literal removal | validation 子集 | PILOT_NEUTRAL_PAD_VALIDATION | MUST | TODO | 未过→pad-replacement 降级（ROUND2 Part C） |
| R025 | M2 | 审计覆盖 + pilot 成本 | RIT 采样 | audit pool | PILOT_AUDIT_SUPPORT_COVERAGE, PILOT_TOTAL_ROLLOUT_BUDGET, PILOT_TOTAL_TOKEN_COST, RIT_ROLLOUT_EQUIV_PER_EVENT | MUST | TODO | 成本走 §3.7 公式；数值待测 |
| R030 | M2.5 | 冻结 K/n^audit/seeds | 由 Stage-1 方差计算 | — | —（计算，非运行） | MUST | TODO | pilot 数据不进 confirmatory gate（硬独立） |
| R040 | M3 | MERIT 主结果 | MERIT (ours) | 主基准 4 类，冻结 seeds | MAIN_MERIT_S1..S5/WAL/LME/LCM/AVG, MAIN_AVG_GAIN_OVER_BEST_BASELINE | MUST | TODO | **Gate-C4** 合取（max-baseline Holm + 低开销） |
| R041 | M3 | RIT-Full 参照行 | RIT-Full | 主基准 4 类 | MAIN_RITFULL_*, MERIT_FRACTION_OF_RITFULL_GAIN | MUST | TODO | intervention reference，非无条件上界 |
| R042 | M3 | 异质性趋势 | MERIT vs baselines | S1(单域)→S5(混流) | MAIN_GAIN_SINGLE_DOMAIN, MAIN_GAIN_MIXED_STREAM | MUST | TODO | 增益随异质性放大 |
| R043 | M3 | 主实验算力 | 所有主表 runs | — | MAIN_GPU_HOURS_PER_RUN | MUST | TODO | 待测；无虚构 |
| R050 | M4 | C2 保真 + 校准 | ACA vs correlational baseline | sealed held-out AUDIT | ACA_HELDOUT_CCC_T500, ECE_ACA_HELDOUT | MUST | TODO | **Gate-C2** 合取；Fig5a；final audit 盲 |
| R051 | M4 | A1 recalibration 消融 | Full vs A1（no recalib） | held-out | ABL_A1_AVG/DELTA/SR20/CCC/CTI | MUST | TODO | C2 组件 |
| R052 | M4 | A2 signal-localization | Full vs A2（swap→co-occurrence） | 主基准子集 | ABL_A2_AVG/DELTA/SR20/CCC/CTI | MUST | TODO | **A2 gate**：增益应消失（capacity-matched） |
| R053 | M4 | A3 no-scope（CTI） | Full vs A3 | A/B 混流审计 | ABL_A3_*, （CTI） | MUST | TODO | **G-C3b** CTI 降低 |
| R054 | M4 | A4 no-governance（SR 斜率） | Full vs A4 | mechanism 检查点 | ABL_A4_*, SR_MERIT_T500, SR_REDUCTION_MERIT_T500_PERCENT | MUST | TODO | **G-C3a** SR 斜率差；Fig5b |
| R055 | M5 | reward-swap 移植 | MemR1/Mem-α × {orig, φ̂} | GRPO 不变 | PLUGIN_MEMR1_ORIG_AVG, PLUGIN_MEMR1_PHI_AVG, PLUGIN_MEMALPHA_ORIG_AVG, PLUGIN_MEMALPHA_PHI_AVG, REWARD_SWAP_MEMORY_R1_GAIN, REWARD_SWAP_MEMALPHA_GAIN | NICE | TODO | 非阻塞 **G-C3c**；Table 2；RL 定位互补 |
| R056 | M4 | A5 usage-feature 必要性 | ACA vs 仅 (q,m) 语义特征 | held-out | ABL_A5_AVG/DELTA/SR20/CCC/CTI | NICE | TODO | frontier necessity（B6） |
| R057 | M4 | A-judge 对照 | ACA vs LLM self-judge | held-out | ABL_AJUDGE_AVG/DELTA/SR20/CCC/CTI | NICE | TODO | 自我确认陷阱对照（B6） |
| R058 | M4 | Full 参照行 | Full MERIT | 消融基准 | ABL_FULL_AVG/SR20/CCC/CTI | MUST | TODO | Table 3 参照 |
| R060 | M3/M4 | 核心成本 sweep + 次要 Pareto | baseline/MERIT/A1/RIT-Full | budget sweep p∈{1,2,5,10}% | EFF_BASELINE_AVG, EFF_MERIT_AVG, EFF_A1_AVG, EFF_RITFULL_AVG, MERIT_RELATIVE_TOKEN_COST, A1_RELATIVE_TOKEN_COST, RITFULL_RELATIVE_TOKEN_COST, FULL_RIT_COST_MULTIPLIER | MUST | TODO | C4 成本上限为阻塞 gate；**G-H4** knee（τ_knee 待定）为 NICE、非阻塞；Table 6 |
| R061 | M3/M4 | 开销 profiling | MERIT 常驻归因器 | 主基准 | ACA_SCORING_LATENCY_MS, ACA_VRAM_OVERHEAD_GB, RIT_TOKEN_OVERHEAD_PERCENT, TOKEN_OVERHEAD_PERCENT, ACA_TRAINABLE_PARAMS | MUST | TODO | 低开销 gate 支撑 C4 |
| R062 | M3 | 流式曲线 | MERIT vs baselines vs RIT-Full | 主流 | FIG4_LATE_STREAM_GAIN_SHARE, MAIN_AVG_GAIN_OVER_BEST_BASELINE | MUST | TODO | Fig4 |
| R070 | M5 | backbone scaling | MERIT 32B→235B | 主基准 | SCALING_GAIN_32B, SCALING_GAIN_235B | NICE | TODO | 迷信机制不变 |
| R071 | M5 | zero-shot transfer（H3） | ACA 训练于 ALFWorld+HotpotQA | WebArena zero-shot | ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA | NICE | TODO | **G-H3** |
| R072 | M5 | H5 边界三轴 | MERIT | bank-size / heterogeneity / redundancy | H5_GAIN_SMALL_BANK_LT100, H5_GAIN_SINGLE_DOMAIN | NICE | TODO | **G-H5**；redundancy 轴 = EVIDENCE GAP（无 ID） |
| R080 | M5 | 案例研究 | 成功 vs superstitious vs redundant/substitutable | case logs | CASE_SUPERSTITION_EVICTION_TASK_INDEX, FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION | NICE | TODO | Fig6/Fig1；A7 group fallback 无数值保证 |
| R081 | M5 | 残余失败分析 | MERIT 失败样本分类 | 失败子集 | RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION | NICE | TODO | 与「写什么」方向互补 |

**说明**
- Run ID 段位：R000=environment(M-1)，R00x=sanity/judge，R01x=baseline family，R02x/R03x=pilot/freeze(M2/M2.5)，R04x=main(M3)，R05x=ablation/secondary，R06x=efficiency，R07x/R08x=boundary/case(M5)。ID 为 family 段位，不要求连续。
- M1 只运行 R010–R011；R012 完整 baseline family 在 pilot 通过后进入 M3。R003 只门控 judge-dependent 原子 runs。R055 与 R060 的 H4 解释均为 secondary/non-blocking。
- 所有 `USER_APPROVAL_REQUIRED`（δ、MEI/power、CI half-width、split、subset、pad 内容/带、ε、S2–S4、A/B 对、max-baseline 统计量、Holm α/FDR q、W、τ_knee、各 gate 阈值、四角色 split、governance bound）在 `EXPERIMENT_PLAN.md` 末节列出，**均未锁定**。
- formal K / n^audit / seed count 由 R030（M2.5）从独立 pilot 方差**计算**并冻结，非预设。

**Status：未运行任何实验；未联网；论文源/协议/账本/reviews 未改；未新增占位符 ID；未调用 `/run-experiment`。停止。**
