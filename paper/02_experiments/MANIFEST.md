# MANIFEST — paper/02_experiments/

> ARIS `/experiment-plan` 输出清单（Output Manifest Protocol）。
> 输出目录覆盖 skill 默认 `refine-logs/`，全部落在 `paper/02_experiments/`。

- **Skill**：`/experiment-plan`（MERIT claim-driven 实验路线图）
- **初始生成时间（UTC）**：2026-07-19T04:33:40Z（版本戳 `20260719T043340Z`）
- **最新修订时间（UTC）**：2026-07-19T04:54:59Z（版本戳 `20260719_045459`）
- **项目日期**：2026-07-19
- **语言**：中文说明，保留英文指标 / 变量 / Run ID / 方法名
- **状态**：已生成计划；**未运行任何实验**；未联网；未修改论文源 / 协议 / 账本 / reviews / `source_proposal.md`；未新增占位符 ID；未安装或调用 `/run-experiment`

## 本次输出文件

| 文件 | 说明 | 类型 | SHA-256 |
|---|---|---|---|
| `EXPERIMENT_PLAN.md` | 实验计划（固定名，latest） | fixed | `318bbcf17962556ae42d005eb5fb84721427d624533d569d3576334d1d51c493` |
| `EXPERIMENT_PLAN_20260719T043340Z.md` | 实验计划（初始不可变版本） | versioned | `355aa0e78924d5bb0de1ec51a0c3af68d67d3f8ec24db4dba9c69b65dcf1cf6a` |
| `EXPERIMENT_PLAN_20260719_045459.md` | 实验计划（最新修订版本，内容同固定名） | versioned | `318bbcf17962556ae42d005eb5fb84721427d624533d569d3576334d1d51c493` |
| `EXPERIMENT_TRACKER.md` | 执行追踪表（固定名，latest） | fixed | `10e6f7646394bf5e9fde8f540f9bb8aefd2a30f723a6673b6086ccf7254fce04` |
| `EXPERIMENT_TRACKER_20260719T043340Z.md` | 执行追踪表（初始不可变版本） | versioned | `de4c1f4fa10d62ca48391f26a2e830f49825cabfe8b3bf9a70c8a3088fcb818a` |
| `EXPERIMENT_TRACKER_20260719_045459.md` | 执行追踪表（最新修订版本，内容同固定名） | versioned | `10e6f7646394bf5e9fde8f540f9bb8aefd2a30f723a6673b6086ccf7254fce04` |
| `MANIFEST.md` | 本清单 | manifest | （自身，不自引 SHA） |

## 输入依据（只读，未修改）

- `paper/01_planning/DRAFT_POLICY.md` — 证据纪律与占位符规范
- `paper/01_planning/PRE_RUN_PROTOCOL.md` — two-stage fixed design、gates、sizing、`USER_APPROVAL_REQUIRED`
- `paper/01_planning/PAPER_PLAN.md` — C1–C4 / H1–H5、Table/Figure Plan
- `paper/reviews/ROUND2_REVISION_PLAN.md` — 已批准 scope 决策（removal-vs-pad、放弃 individual-Shapley、非因果措辞、四角色、seed/run 单位、G-C2/G-C4 合取、G-H3 gate）
- `paper/01_planning/PLACEHOLDER_LEDGER.md` — 241 个已登记 `[[TBD:...]]` ID（未新增）
- `paper/00_input/source_proposal.md` — 源方案快照（SHA-256 `E700D46…96CC`，未修改）
- `paper/main.tex`、`paper/sections/*`、`paper/tables/*`、`paper/figures/placeholders/*` — 论文源结构（只读勘察）

## 复用的占位符类别（全部来自账本，未新增）

`MAIN_*`（126 主表 cell + headline / gain / GPU-hours）、`PILOT_*`、`SR_*`、`ACA_*`、`ECE_ACA_HELDOUT`、
`ABL_*`（Full/A1/A2/A3/A4/A5/A-judge/A7 × AVG/DELTA/SR20/CCC/CTI）、`PLUGIN_*` / `REWARD_SWAP_*`、
`EFF_*` / `*_TOKEN_*` / `*_LATENCY_*` / `*_VRAM_*` / `FULL_RIT_COST_MULTIPLIER`、`SCALING_*`、`H5_*`、
`ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA`、`CASE_*` / `FIG*` / `RESIDUAL_*`、`RIT_*` / `RIT_BUDGET_EPSILON_PERCENT`、
`JUDGE_HUMAN_AGREEMENT_KAPPA`、`AAAI2027_TRACK_PAGE_LIMIT`。

## 自检

- [x] 仅写入 `paper/02_experiments/`（7 个文件；保留 2 个初始快照）
- [x] 固定名与最新时间戳版本 SHA-256 逐一一致；初始时间戳版本未改
- [x] 无新增占位符 ID；引用的 ID 均在账本 241 内
- [x] 成本仅公式或「待测（占位 ID）」，无虚构 GPU-hours / 时间 / 样本量 / 预算
- [x] 全部 `USER_APPROVAL_REQUIRED` 未锁定，均带 recommendation + rationale + alternative
- [x] 未运行实验、未联网、未调用 `/run-experiment`、未修改论文/协议/账本/reviews

## 2026-07-19 审计修订

- 用户确认实际实验资源为 **8×NVIDIA H20**；覆盖执行计划中的 provisional
  A100 资源，但不修改冻结源方案。显存、软件栈、主机资源与互联待 R000
  只读盘点，不推测性能。
- Tracker 明确为 **35 个 run families**（稀疏 milestone ID），待协议锁定后才
  展开原子 runs。
- R001/R002 才是全局 sanity gate；R003 仅阻塞 judge-dependent 评测。
- M1 只复现 ReasoningBank/MemRL；完整 baseline family R012 延后至 pilot
  通过后的 M3。
- B5/G-C3c 与 B7 的 H4/Pareto 解释改为 secondary/non-blocking；B7 核心成本
  gate 仍为 MUST-RUN。
