# 叙事报告：MERIT — 检索不等于贡献

- **文件用途：** 本文件是供作者查阅的中文翻译版；后续 ARIS 规划的权威输入是英文版 `paper/00_input/NARRATIVE_REPORT.md`。如中英文存在差异，以英文版为准。
- **文档状态：** `PRELIMINARY NARRATIVE WITH PLACEHOLDERS`
- **证据状态：** 实验尚未执行或核验。本文所有定量结果均为计划/预期量，并以唯一的 `[[TBD:...]]` 占位符表示，不是实测数据。
- **目标格式：** AAAI 2027 匿名初稿。
- **权威源方案快照：** `paper/00_input/source_proposal.md`（SHA-256：`E700D46BDD1B4F83A2D45466EDBDB2112D2FAB3EFDCC912A7AED2F5BDFC496CC`，完整性：`MATCH`）。
- **投稿场所覆盖说明：** 当前写作任务面向 **AAAI 2027**。源方案记录的投稿策略（首选 NeurIPS 2027 / ICML 2027，备选 AAAI-28）仅作为来源背景保留，不得覆盖当前 AAAI 2027 目标。

> 范围说明：这是一份结构化中文叙事报告，便于作者查阅；下游 ARIS `/paper-plan` 使用对应的英文版。它不是正式论文正文。章节定位标题可以保留源方案中的双语形式。此处不生成 LaTeX、图片、参考文献或实验代码。

---

## 核心故事

自进化 LLM 智能体通过把交互轨迹提炼到持久记忆库中而持续改进，这一自我改进循环的质量在很大程度上取决于系统如何将信用分配给每条记忆。源方案将 ReasoningBank、SkeMex 和 MemRL 等系统的信用信号描述为相关性的，此描述仍需文献核验：当任务成功且某条记忆曾被检索时，相关信号会提高该记忆的效用。本报告提出，**检索不等于贡献**——检索 ≠ 使用 ≠ 真正的因果帮助；并提出假设：这类信用可能类似斯金纳鸽子实验中的强化机制，使仅仅与成功共同出现的记忆也不断得到强化，最终产生因果作用为零或负值的**迷信记忆**（cargo-cult memories）。

我们提出 **MERIT**：在保持在线、非平稳、闭环环境下成本可接受的同时，用反事实信用替代相关性记账。MERIT 在标准的“检索—执行—写入”循环上增加三个紧密耦合的组成部分：(1) **随机干预试验（Randomized Interventional Trials, RIT）**，以小预算进行配对留一法（LOO）干预并产生因果标签；(2) **摊销反事实归因（Amortized Counterfactual Attribution, ACA）**，利用这些标签训练每事件 O(1) 的归因器，并定期重新校准以跟踪闭环分布漂移；(3) 两类刻意保持简单的信用**消费者**——基于阈值的**信用治理**（淘汰/合并/隔离）以及学习每条记忆适用范围的**作用域门控检索**。其依赖链严格为：`RIT → ACA → consumers`。

预期贡献是：**因果信用，而不是更复杂的启发式规则，才是自进化系统缺失的基础要素**。叙事以一个诊断现象开篇（迷信记忆随部署时间累积），论文主体则放在使反事实信号变得可负担且可直接消费的机制，以及仅替换信号是否能够修复该现象的检验上。下文所有核心数字均未测量，并以占位符表示，等待真实实验填充。

---

## 问题与关键观察

- **研究设定。** LLM 智能体正从无状态模式转向由经验驱动的自进化：系统把轨迹提炼为持久记忆，并利用学习或启发式信号管理记忆的写入、合并、淘汰和检索。整个范式隐含的前提是，系统知道哪条记忆应该获得信用。
- **两个具名失效模式。**
  1. **迷信记忆（Superstitious Memory）**——只与成功共同出现、没有因果贡献，却不断得到强化并占据检索位置的记忆。
  2. **跨任务干扰（Cross-Task Interference, CTI）**——一条在任务族 A 上确实有用的记忆被不加区分地检索到任务族 B 中并造成伤害，即“药方是对的，但病人错了”。
- **关键观察（叙事钩子）。** *检索不等于贡献。* 一条记忆的价值只能通过反事实来定义，即移除它之后结果下降多少。依据源方案且等待文献核验，本报告涉及的系统没有直接测量这一量，因为逐记忆干预看起来成本过高。计划检验的假设是：相关性信用不会自我纠正，迷信比例会随部署长度**增长**（见“实验”中的 pilot 计划）。
- **为什么源方案认为既有工作尚未解决它。** 源方案将 ReasoningBank 的成功轨迹提炼、SkeMex 的环境反馈效用和 MemRL 的蒙特卡洛更新描述为以共现为基础的观测性信用信号，此定位仍需文献核验。源方案假设检索概率与问题的基础难度相关（“简单问题搭便车”），高效用又会反馈为更高检索概率（马太效应），从而形成斯金纳箱式强化循环。尚未证明的非正式命题 1 对此给出形式化承诺。

---

## 贡献类型与叙事原型

- **贡献类型：** 主要为 **T1（新方法）**，辅助为 **T2（新洞见）**。
  - 主要 T1：MERIT 用随机干预试验和摊销反事实归因，替换自进化记忆中的相关性信用信号。
  - 辅助 T2：揭示并量化“迷信记忆”现象。
  - T2 不作为主贡献的原因：“相关不等于因果”在因果推断中是常识；论文实质是使反事实信号在闭环系统中可负担、可消费的完整机制，以及信号替换是否修复现象的实证检验。
- **叙事原型：** 全文统一采用 **Type A（修复型）**。骨架为：自进化记忆在部署中退化 → 根因是信用信号只有相关性（检索 ≠ 使用 ≠ 贡献）→ 把信用从“观察性研究”升级为“随机对照试验”，并将在线估计摊销到 O(1)。
- **源方案的篇幅约束（执行者必须遵守）：** 方法与消融是主要战场，合计约占正文 45%；Pilot 控制在约 1–1.5 页；只保留一个理论结果（命题 1），证明放入附录。不得引入第二条故事线：跨任务干扰和 RL 奖励替换只能作为因果信用信号的两个消费者来叙述，而非独立贡献。
- **保留源方案中的减法决策（不得逆转）：**
  - 使用 φ̂ 训练 GRPO/RL 记忆管理策略已被**降级**；主方法只使用阈值规则消费 φ̂。RL 变体仅保留为奖励替换插件实验。
  - 对记忆间交互执行完整 Shapley 采样已被**降级**为 H5 边界讨论和附录变体。

---

## 贡献主张与证据状态

保留并编号四项核心贡献 `C1`–`C4`。`Status` 只能是 `SUPPORTED-BY-DESIGN`、`PLANNED-EVIDENCE` 或 `HYPOTHESIS` 之一。设计合理性不得写成实验证实，预期机制不得写成已观察事实。

### C1 — 揭示并量化迷信记忆（T2）
- **Statement：** 相关性信用（检索与成功之间的共现）会系统性地产生迷信记忆，即最高效用集合中因果贡献为零或为负的记忆，其比例随部署时间增加；RIT 审计协议及 CCC、SR@k 两个指标能够用干预证据测量这一现象。
- **Status：** `PLANNED-EVIDENCE`（必须通过尚未运行的 pilot 证明该现象）。
- **Required evidence：** 在可回放任务流上审计 ReasoningBank 风格和 MemRL 风格的记忆库；绘制 CCC、SR@k 随部署长度的曲线；执行两个替代解释控制（φ̂ 的分半重测信度；移除 φ>0 子集）。
- **Planned paper location：** Pilot / Diagnostic Study；Fig. 2；Proposition 1。
- **Source anchor：** `source_proposal.md` §3 P6 (C1)、§4 (Pilot)、§3.5 (Fig.2)、§5 (Prop.1)。

### C2 — 摊销反事实归因（ACA），方法核心（T1）
- **Statement：** ACA 将 RIT 标签摊销到一个每次检索事件 O(1) 的归因器，并周期性重新校准，从而使反事实信用可负担；计划检验该归因器是否比相关性基线更准确地恢复因果信用。
- **Status：** `PLANNED-EVIDENCE`。
- **设计说明：** O(1) 在线评分和摊销是由设计支持的架构属性；归因准确性和实际成本仍需要计划中的证据。
- **Required evidence：** ACA 相对基线的留出集 CCC；校准结果（可靠性图、ECE）；分半重测；重新校准消融 A1 和使用行为特征消融 A5。
- **Planned paper location：** Method §6.2；Mechanism and Calibration Analysis；Fig. 5a。
- **Source anchor：** `source_proposal.md` §3 P6 (C2)、§6.2、§8.5、§3.5 (Fig.5)。

### C3 — 因果信用可以被直接消费（T1）
- **Statement：** 两个最小消费者——阈值治理和逐记忆作用域门控检索——计划分别检验能否压平迷信积累和消除跨任务干扰；还将检验同一个因果信号作为逐操作奖励时，能否改善 RL 风格管理器（Memory-R1 / Mem-α）。
- **Status：** `PLANNED-EVIDENCE`。
- **Required evidence：** 治理相关的 A2 消融（将因果信用换回共现效用，检验增益是否消失）、作用域门控消融 A3、治理消融 A4、CTI 测量和奖励替换插件表格。
- **Planned paper location：** Method §6.3；Ablation Study；Reward-Swap Plugin Study；主表/CTI 分析。
- **Source anchor：** `source_proposal.md` §3 P6 (C3)、§6.3、§8.4、§8.3 (Table 2)。

### C4 — 系统性实证评估（empirical）
- **Statement：** 计划在四类基准、三个 backbone 和三个随机种子上检验：MERIT 是否能以较低 token 开销超过最强基线的平均性能，以及 CCC、SR@k 等机制指标能否在闭环中恢复。
- **Status：** `PLANNED-EVIDENCE`。
- **Required evidence：** 完整主结果表、消融实验、效率 Pareto 研究、扩展与迁移研究，均尚待执行。
- **Planned paper location：** 整个 Experiments 部分。
- **Source anchor：** `source_proposal.md` §3 P6 (C4)、§8。

> 额外理论承诺（不属于编号贡献）：**Proposition 1** 当前是 `HYPOTHESIS`，即等待附录给出正式陈述和证明的分析性承诺。它严格保留源方案的范围，不引入新定理或证明结论；正式证明完成并核验前不得称其已经得到证明。

---

## 问题形式化与理论承诺

**符号（8 个，均在方法中使用）。** 任务流 `{(q_t, r_t)}`，其中查询/任务为 `q_t`、结果信号为 `r_t ∈ [0,1]`；记忆库 `M_t = {m_i}`；检索算子 `R(q_t) ⊆ M_t`（top-k）；智能体策略 `π(y | q, R(q))`；归因器 `g_θ`；逐记忆运行信用 `φ̄_i`；作用域表示 `S_i`。

**定义 1（反事实贡献）。** `φ_i(q) ≜ E[r | q, R(q)] − E[r | q, R(q)∖{m_i}]`，期望取自策略与环境随机性。推广说明：`φ` 是检索集合上的单点干预效应；完整的记忆间价值是 Shapley value，而单点 LOO 是其一阶近似（近似质量在 H5 边界研究中刻画）。

**定义 2（共现效用，基线信号）。** `Û(m_i) = Σ_t 1[m_i ∈ R(q_t)]·r_t / Σ_t 1[m_i ∈ R(q_t)]`。

**命题 1（非正式；正式陈述与证明置于附录）。** 若检索事件与查询的基础可解性相关（`Cov ≠ 0`），则 `Û` 是 `φ` 的渐近有偏估计；在效用参与检索排序的正反馈下，存在稳定的“迷信均衡”（`Û` 高而 `φ = 0`）。现实对应：语义检索自然可能满足相关条件。**此处不扩展源方案中的结论；正式证明完成前，该命题仍是待证明的分析性承诺。**

**假设（编号以便 rebuttal）。**
- **A1（结果可观测）：** 每项任务都有可用的 `r_t`（环境成功信号或经过一致性检查的 LLM judge 分数）。
- **A2（局部可回放）：** 一部分任务可从固定初始状态重新执行（docker 快照/文本环境天然满足）；**只有 RIT 标签收集需要 A2**，ACA 在线评分不需要。
- **A3（低阶交互）：** 检索集合内的交互效应有界，因此 LOO 相对 Shapley 的误差可控；H5 边界研究将主动展示违反 A3 的情形（冗余记忆对），并使用分组干预作为后备方案。

**优化对象。** 在 RIT 标签上学习 `g_θ`，最小化回归损失 `E[(g_θ(x_i(q)) − φ̂_i(q))²]`；系统目标是在 token 预算约束下最大化流式累计成功 `Σ r_t`（检索 + RIT 采样 ≤ baseline × (1 + ε)，其中 `ε = [[TBD:RIT_BUDGET_EPSILON_PERCENT]]`，为 `provisional hyperparameter`）。

---

## 提出的方法：MERIT

**概览（Fig. 3）。** MERIT 在标准“检索—执行—写入”循环中增加三个部分：(C1) 小预算 RIT 持续产生因果标签；(C2) ACA 把标签摊销为每事件 O(1) 的贡献分数，并定期重新校准以适应闭环分布漂移；(C3) 两个最小消费者使用该分数——阈值治理更新记忆保留状态，作用域门控检索修正排序。模块构成严格的上游→下游依赖 `RIT → ACA → consumers`，**没有并行技巧，也没有无关模块堆叠**。

### 随机干预试验（RIT）→ C1
- **Why：** Proposition 1 假设共现效用有偏；源方案还假设朴素替代方案“让 LLM 自评记忆是否有帮助”可能重现自我确认陷阱，因此将其作为消融变体 `A-judge` 保留。
- **How（planned configuration）：** 以概率 `p = [[TBD:RIT_SAMPLING_PROB_PERCENT]]` 将任务采入试验组（`provisional hyperparameter`，源方案计划值为 5%）；对检索集合中的每条记忆执行配对 LOO，每次使用 `K = 5` 个固定种子 rollout（`planned configuration`）；为控制位置混杂，保持其余上下文顺序，并在删除记忆的位置插入填充占位；把 `(q, m_i, trajectory, φ̂_i)` 四元组写入标签池。采样只在满足 A2 的任务上进行。
- **Link：** C1；该审计协议可以独立作为诊断已部署记忆库的社区工具。

### 摊销反事实归因（ACA）→ C2（方法核心）
- **Why：** 完整 RIT 成本尚未测量，为 `[[TBD:FULL_RIT_COST_MULTIPLIER]]`；摊销把因果信用压缩到 O(1)。ACA 学习“什么样的记忆，在什么样的查询上，以什么方式被使用时，会产生真实贡献”。其中**使用行为特征**是关键：它区分“被检索但被忽略”和“被实际执行”。
- **How（planned configuration）：** 输入特征 `x_i(q)` 分三组——查询表示、记忆表示（`Qwen3-Embedding-4B`，冻结）和**使用行为特征**（记忆内容与输出之间的 n-gram/编辑重叠、模型显式引用标记、上下文位置与检索排名、记忆 token 的 log-likelihood gain）；头部是回归 `φ̂ ∈ [−1, 1]` 的两层 MLP。训练：标签池上的 Huber loss（`δ = 0.1`，`provisional hyperparameter`）；每 100 个任务执行一次**周期性重新校准**（`planned configuration`），在最新标签上微调并进行 isotonic-regression calibration。由于 C3 改变闭环检索分布，重新校准用于防止归因器漂移。在线推理：为每次检索的 top-k 记忆评分，更新运行信用 `φ̄_i`（EMA）及正/负查询样本集。
- **Link：** C2 / H2；校准质量将在 Fig. 5a 和可靠性分析中检验。

### 信用治理 → C3
- **Why：** 不被消费的信号只能用于审计；治理计划用于压平迷信积累（SR）。主方法刻意使用阈值**规则而非 RL**，以检验收益是否来自信号本身（消融 A2：规则不变，只把信用换成共现效用，检验增益是否消失）。
- **How（三条规则；planned configuration / provisional thresholds）：**
  - **Evict：** `φ̄_i < −0.02` 且样本数 `n_i ≥ 8`。
  - **Merge：** embedding similarity `> 0.9` 且两者 `φ̄ > 0` → LLM-summary merge（按权重合并信用）。
  - **Quarantine：** 新记忆进入隔离区；最初 `n_min = 3` 次检索带有 UCB 风格探索奖励（`c = 0.5`）以避免冷启动死亡，且不贡献排序加成。
  - 所有阈值都是 `provisional hyperparameter`；±0.02 死区是与校准分析相连的设计选择（在 φ ≈ 0 附近，符号判断最不稳定）。

### 作用域门控检索 → C3
- **Why：** 通过学习每条记忆的适用范围，解决“药方正确、病人错误”的跨任务干扰。
- **How（planned configuration）：** 每条记忆维护正/负查询原型（`φ̂ > τ⁺` / `φ̂ < τ⁻` 的查询 embedding 均值）；检索分数 `= α·(semantic relevance) + β·(sim(q, proto⁺) − sim(q, proto⁻)) + γ·φ̄_i`，默认 `(α, β, γ) = (1.0, 0.5, 0.3)`，均为 `provisional hyperparameter`（在边界/扩展分析中进行敏感性检验）。
- **Link：** C3 / H1 / H3；插件行为（将 φ̂ 作为逐操作奖励替换 Memory-R1 的结果奖励，GRPO 设置不变）在奖励替换研究中单独报告。

### 成本与复杂度承诺
- **依赖检查：** `RIT → ACA → consumers` 是已经核对的线性链；被删减的模块已记录在前述减法决策中。
- **开销（正文一句话，完整表格放附录；所有数值均为计划/未测量）：** ACA 每事件评分 `[[TBD:ACA_SCORING_LATENCY_MS]]`（4B encoder 批处理）；RIT 流式摊销开销 `[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]` token；门控和治理不增加 LLM 调用；总 token 开销 `[[TBD:TOKEN_OVERHEAD_PERCENT]]`，归因器常驻显存 `[[TBD:ACA_VRAM_OVERHEAD_GB]]`。
- **设计选择表（附录 D，示例行）：** `LOO not full Shapley | sampled Shapley | cost lower vs 1×, error bounded under A3 | ablation A7`；`usage-behavior features | (q,m) semantic features only | distinguish "retrieved-not-used" | ablation A5`；`isotonic recalibration | no calibration | closed-loop drift | sensitivity S3`。若某行有两列为空，则删除该设计。

**Algorithm 1（主循环，结构按源方案保留）：**
```

---

## 假设—实验映射

> 说明：源方案在 §7 映射表中列出 “H1–H5”，但只在 §6.3、§8.5 和图注中零散阐述。下表根据这些锚点重建；若源方案未显式写出某个假设标签，则予以标记。**CTI 定义（来自源方案 §7）：** `CTI = Acc_B(B-only bank) − Acc_B(A∪B mixed bank)`，`≥ 0` 表示存在干扰；A/B 领域对按照 Evo-Memory 混合流协议构建。

| Hyp. | 陈述（重建） | 主要指标 | 实验位置 | 相关主张 | 状态 |
|------|--------------|----------|----------|----------|------|
| H1 | 阈值治理使迷信比例随任务流累积的曲线趋于平坦 | SR@20% 曲线斜率 | Ablation A4 / Mechanism analysis | C3 | `HYPOTHESIS`（标签为推断；源锚点 §6.3/§8.5） |
| H2 | ACA 以 O(1) 成本恢复因果信用 | 留出集 CCC（Spearman） | Mechanism & Calibration, Fig. 5a | C2 | `HYPOTHESIS`（源方案门槛：CCC ρ ≥ 0.6） |
| H3 | 作用域门控消除跨任务干扰并实现零样本迁移 | CTI；迁移 CCC | Ablation A3 / Scaling & transfer | C3 | `HYPOTHESIS` |
| H4 | RIT 预算在较小 p 处饱和；MERIT 具有 Pareto 效率 | AVG vs. token cost；p-sweep | Efficiency Study | C4 | `HYPOTHESIS`（源方案假设：p=5% 饱和） |
| H5 | 增益存在边界：小记忆库、单领域短任务流和高冗余情况下减弱或消失 | gain vs. bank size / heterogeneity / redundancy | Boundary & Scaling；Case Study | C4（及范围说明） | `HYPOTHESIS` |

---

## 实验

> 所有数值结果单元格都是未测量占位符。Pilot、主实验、消融和效率实验均采用将来时或计划性措辞。

### 实验设置
- **Backbones（planned configuration）：** `Qwen3-32B`（主要）；`Qwen3-235B-A22B`（规模趋势点）；`GPT-5.1`（闭源泛化点，仅在主表中增加一行）。
- **ACA 模型：** `Qwen3-Embedding-4B` 冻结 encoder + 两层 MLP，可训练参数量 `[[TBD:ACA_TRAINABLE_PARAMS]]`（未测量，待实现后核验）。
- **代码库：** 使用 `EvolveLab` 统一实现记忆系统，以保证基线公平。
- **基准（4 类）：** Evo-Memory 流式任务流（对话 + agentic）、`WebArena-Lite`、`LongMemEval`、`LoCoMo`。Pilot 使用可回放的 `ALFWorld`（具身文本）和 `HotpotQA`（多跳检索）。
- **公平性（planned）：** 相同 backbone、相同 retriever（`bge-m3` 或 `Qwen3-Embedding`，统一）、相同 `top-k = 4`、相同 token 预算（给基线同等预算用于自身机制或空耗，并报告两种记账方式）；种子 `{13, 42, 2026}`，报告 mean±std；配对 bootstrap 显著性检验（10⁴ 次重采样并报告 p-value）；流式曲线为各点报告置信带。
- **Judge 偏差控制：** 部分 HotpotQA/LoCoMo 子任务使用 LLM-as-judge（`GPT-5.1`，与 Qwen3 backbone 不同来源）；人工检查 200 个样本，目标 Cohen's κ 为 `[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]`（源方案目标标准 ≥ 0.8）。
- **硬件（planned）：** 8×A100-80G；单次主实验（1 backbone × 1 benchmark × 3 seeds）的 GPU 时间为 `[[TBD:MAIN_GPU_HOURS_PER_RUN]]`；API 成本表置于附录。

### Pilot / 诊断研究——“记忆信用为何出错？”
- **系统：** 在统一代码库上复现 ReasoningBank（启发式信用）和 MemRL（MC 学习信用）；backbone 为 Qwen3-32B（执行温度 0.7，评估使用 greedy）。
- **任务流：** 两个可回放任务流（ALFWorld、HotpotQA），每个 500 个任务、3 个种子。必须使用可回放环境，因为干预需要从完全相同的初始状态重新执行配对 rollout。
- **干预协议（RIT 首次出现）：** 在 `t ∈ {100, 200, 300, 400, 500}` 冻结记忆库快照；对随后 50 个任务中的每次检索事件，抽取 300 个 `(query, retrieved-set)` 对；对每条记忆执行 full context 与 removed 的配对 LOO，每种使用 `K = 5` 个固定种子 rollout；`φ̂_i(q) = success-rate difference`。（300、K=5 和各快照点均为 `planned configuration`。）
- **预算说明（防止“伪造 pilot”）：** 每个快照点共 `[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]` 次 rollout，总 token 成本 `[[TBD:PILOT_TOTAL_TOKEN_COST]]`；两者均未测量，将在附录成本表中报告。
- **两个具名统计量：**
  - **CCC（Credit–Contribution Correlation）：** 系统信用与 RIT 真实 φ 的 Spearman 相关。计划/预期值：ReasoningBank `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`，MemRL `[[TBD:PILOT_CCC_MEMRL_T500]]`。
  - **SR@k（Superstition Rate）：** top-k% 效用记忆中 `φ ≤ 0` 的比例。计划检验 SR@20% 是否从 t=100 时的 `[[TBD:PILOT_SR20_T100]]` 上升至 t=500 时的 `[[TBD:PILOT_SR20_T500]]`，即迷信是否单调累积且系统是否无法自我纠正。
- **替代解释控制：**
  - Control 1（“φ 测量噪声太大”）：φ̂ 分半重测信度为 `[[TBD:PILOT_SPLITHALF_PHI_RELIABILITY]]`；用于检验低 CCC 是否只是测量噪声的伪影。
  - Control 2（“记忆整体无用，因此归因没有意义”）：移除整个 `φ > 0` 子集后成功率变化 `[[TBD:PILOT_UTILITY_SUBSET_REMOVAL_DROP]]`；用于区分“记忆无价值”和“信用错误”。
- **门槛（来自源方案，诚实保留）：** 若 CCC > 0.5 或 SR 不随时间上升，则归因假设被证伪 → 修改 idea card（把主张收窄到异质任务流），不得强行写作。

### 主结果计划
- 结构：行按方法谱系排列（Vanilla → 结构化启发式信用 → 学习信用 → 正交方法 → 上界），MERIT 位于倒数第二行，RIT-Full 上界位于最后一行（灰色）；列为按异质性递增的 5 个 Evo-Memory 任务流（单领域 ALFWorld → mixed）→ WebArena-Lite → LongMemEval → LoCoMo → AVG。
- 计划叙事（必须由真实数据验证）：(i) 增益是否随任务流异质性单调增加（single-domain `[[TBD:MAIN_GAIN_SINGLE_DOMAIN]]` → mixed `[[TBD:MAIN_GAIN_MIXED_STREAM]]`）；(ii) 学习信用基线是否并不稳定地优于启发式方法；(iii) MERIT 是否以较小成本获得 RIT-Full 上界增益的 `[[TBD:MERIT_FRACTION_OF_RITFULL_GAIN]]`。
- 完整骨架见“计划表格”中的 Table 1。

### 奖励替换插件研究
- 用 φ̂ 替换 Memory-R1 / Mem-α 的原始奖励，GRPO 设置保持不变；预期提升分别为 `[[TBD:REWARD_SWAP_MEMORY_R1_GAIN]]` 和 `[[TBD:REWARD_SWAP_MEMALPHA_GAIN]]`。该实验用于检验 MERIT 修复的是**信号**还是 pipeline，并回应“相对 MemRL/Memory-R1 增量太小”的质疑。骨架见 Table 2。

### 消融研究
- 逐贡献移除 + 替代信号控制：A1（不重新校准/静态归因器）、A2（因果信用 → 共现效用）、A3（无作用域门控）、A4（无治理）、A5（无使用行为特征）、A-judge（使用 LLM 自评而非 RIT）、A7（LOO → 分组/采样 Shapley 干预）。骨架见 Table 3。

### 机制与校准分析（闭环恢复）
- **机制恢复（H2）：** Fig. 5 复用 Fig. 2 的统计量和坐标范围——(a) CCC 从 `[[TBD:PILOT_CCC_REASONINGBANK_T500]]` 到 ACA 的 `[[TBD:ACA_HELDOUT_CCC_T500]]`；(b) baseline SR@20% 上升至 `[[TBD:PILOT_SR20_T500]]`，MERIT 是否压平至 `[[TBD:SR_MERIT_T500]]`（下降 `[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]`）。
- **校准（回应最高风险“归因噪声”）：** 留出 RIT 的可靠性图 + ECE `[[TBD:ECE_ACA_HELDOUT]]`；逐领域校准；分半重测；预期失效模式是 φ ≈ 0 附近符号最不稳定，并与 ±0.02 治理死区相连。
- **敏感性：** `K ∈ {1,3,5,10}`、RIT 预算 `p ∈ {1,2,5,10}%`、`(α,β,γ)` 网格、`top-k ∈ {2,4,8}`；计划检验 p=5% 饱和假设（H4）。

### 边界与扩展分析
- **扩展/迁移：** backbone 从 32B → 235B，检验增益是否保持（`[[TBD:SCALING_GAIN_32B]]` → `[[TBD:SCALING_GAIN_235B]]`；即使基线变强，迷信机制是否仍存在）；ACA 在 ALFWorld+HotpotQA 上训练，零样本迁移到 WebArena 的 CCC 为 `[[TBD:ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA]]`（H3）。
- **边界刻画（H5）：** 三条计划趋势线——增益 vs. 记忆库规模（`< 100` 条目的分析区间，其未测增益为 `[[TBD:H5_GAIN_SMALL_BANK_LT100]]`）、增益 vs. 任务流异质性（单领域增益 `[[TBD:H5_GAIN_SINGLE_DOMAIN]]`）、增益 vs. 注入冗余比例。假设是：冗余越高，LOO 低估越严重，而 A7 变体可以缓解；解释必须与实测趋势对照评估。

### 案例研究
- 成功示例：比较一条 HotpotQA 记忆（“先搜索实体别名，再搜索关系”）和一条迷信记忆（“检索为空时再执行一次相同查询”）；计划检验后者虚高的效用是否会被 RIT 判为接近零，并在任务 `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]` 时被淘汰，同时前者的信用和作用域（仅多跳查询）能否被正确刻画。
- 失败示例：两条互补记忆各自包含程序的一半——两者的单独 LOO 均约为 0，治理几乎会同时误杀；分组干预后备方案（按相似性聚类后整体干预）计划用于恢复其信用，诚实展示 A3 边界（Fig. 6）。
- 残余失效分析：MERIT 剩余失败中，预计有 `[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]` 来自记忆库本身缺少相关经验（没有材料时，信用机制也无能为力）。

### 效率研究
- Pareto 图：x = relative token cost（log 轴），y = AVG success；点包括 co-occurrence baseline（`1×`）、MERIT（`[[TBD:MERIT_RELATIVE_TOKEN_COST]]`）、A1（`[[TBD:A1_RELATIVE_TOKEN_COST]]`）、RIT-Full（`[[TBD:RITFULL_RELATIVE_TOKEN_COST]]`）。计划检验 MERIT 是否位于 Pareto 前沿的拐点；另附 label budget vs. performance 的 p-sweep 曲线。骨架见 Table 6。

---

## 计划表格

所有未知实验单元格均使用唯一 `[[TBD:...]]` 占位符。表头、方法行、指标列和 caption intent 均完整。

### Table 1 — 主基准比较
Caption intent（以最终证据为条件）：检验 MERIT 的平均性能是否超过最强基线、增益是否随任务流异质性扩大，以及学习信用基线是否稳定优于启发式方法。S1→S5 的异质性递增（S1 = 单领域 ALFWorld，S5 = mixed）；**S2–S4 的领域身份为 `NOT SPECIFIED IN SOURCE`。**

| 方法（谱系） | S1 (ALFWorld) | S2 | S3 | S4 | S5 (mixed) | WebArena-Lite | LongMemEval | LoCoMo | AVG |
|---|---|---|---|---|---|---|---|---|---|
| No-Memory ReAct | [[TBD:MAIN_NOMEM_S1]] | [[TBD:MAIN_NOMEM_S2]] | [[TBD:MAIN_NOMEM_S3]] | [[TBD:MAIN_NOMEM_S4]] | [[TBD:MAIN_NOMEM_S5]] | [[TBD:MAIN_NOMEM_WAL]] | [[TBD:MAIN_NOMEM_LME]] | [[TBD:MAIN_NOMEM_LCM]] | [[TBD:MAIN_NOMEM_AVG]] |
| Full-History Stuffing | [[TBD:MAIN_FULLHIST_S1]] | [[TBD:MAIN_FULLHIST_S2]] | [[TBD:MAIN_FULLHIST_S3]] | [[TBD:MAIN_FULLHIST_S4]] | [[TBD:MAIN_FULLHIST_S5]] | [[TBD:MAIN_FULLHIST_WAL]] | [[TBD:MAIN_FULLHIST_LME]] | [[TBD:MAIN_FULLHIST_LCM]] | [[TBD:MAIN_FULLHIST_AVG]] |
| Mem0 | [[TBD:MAIN_MEM0_S1]] | [[TBD:MAIN_MEM0_S2]] | [[TBD:MAIN_MEM0_S3]] | [[TBD:MAIN_MEM0_S4]] | [[TBD:MAIN_MEM0_S5]] | [[TBD:MAIN_MEM0_WAL]] | [[TBD:MAIN_MEM0_LME]] | [[TBD:MAIN_MEM0_LCM]] | [[TBD:MAIN_MEM0_AVG]] |
| A-MEM | [[TBD:MAIN_AMEM_S1]] | [[TBD:MAIN_AMEM_S2]] | [[TBD:MAIN_AMEM_S3]] | [[TBD:MAIN_AMEM_S4]] | [[TBD:MAIN_AMEM_S5]] | [[TBD:MAIN_AMEM_WAL]] | [[TBD:MAIN_AMEM_LME]] | [[TBD:MAIN_AMEM_LCM]] | [[TBD:MAIN_AMEM_AVG]] |
| AWM | [[TBD:MAIN_AWM_S1]] | [[TBD:MAIN_AWM_S2]] | [[TBD:MAIN_AWM_S3]] | [[TBD:MAIN_AWM_S4]] | [[TBD:MAIN_AWM_S5]] | [[TBD:MAIN_AWM_WAL]] | [[TBD:MAIN_AWM_LME]] | [[TBD:MAIN_AWM_LCM]] | [[TBD:MAIN_AWM_AVG]] |
| ReasoningBank | [[TBD:MAIN_RBANK_S1]] | [[TBD:MAIN_RBANK_S2]] | [[TBD:MAIN_RBANK_S3]] | [[TBD:MAIN_RBANK_S4]] | [[TBD:MAIN_RBANK_S5]] | [[TBD:MAIN_RBANK_WAL]] | [[TBD:MAIN_RBANK_LME]] | [[TBD:MAIN_RBANK_LCM]] | [[TBD:MAIN_RBANK_AVG]] |
| SkeMex | [[TBD:MAIN_SKEMEX_S1]] | [[TBD:MAIN_SKEMEX_S2]] | [[TBD:MAIN_SKEMEX_S3]] | [[TBD:MAIN_SKEMEX_S4]] | [[TBD:MAIN_SKEMEX_S5]] | [[TBD:MAIN_SKEMEX_WAL]] | [[TBD:MAIN_SKEMEX_LME]] | [[TBD:MAIN_SKEMEX_LCM]] | [[TBD:MAIN_SKEMEX_AVG]] |
| Memory-R1 | [[TBD:MAIN_MEMR1_S1]] | [[TBD:MAIN_MEMR1_S2]] | [[TBD:MAIN_MEMR1_S3]] | [[TBD:MAIN_MEMR1_S4]] | [[TBD:MAIN_MEMR1_S5]] | [[TBD:MAIN_MEMR1_WAL]] | [[TBD:MAIN_MEMR1_LME]] | [[TBD:MAIN_MEMR1_LCM]] | [[TBD:MAIN_MEMR1_AVG]] |
| Mem-α | [[TBD:MAIN_MEMALPHA_S1]] | [[TBD:MAIN_MEMALPHA_S2]] | [[TBD:MAIN_MEMALPHA_S3]] | [[TBD:MAIN_MEMALPHA_S4]] | [[TBD:MAIN_MEMALPHA_S5]] | [[TBD:MAIN_MEMALPHA_WAL]] | [[TBD:MAIN_MEMALPHA_LME]] | [[TBD:MAIN_MEMALPHA_LCM]] | [[TBD:MAIN_MEMALPHA_AVG]] |
| MemRL | [[TBD:MAIN_MEMRL_S1]] | [[TBD:MAIN_MEMRL_S2]] | [[TBD:MAIN_MEMRL_S3]] | [[TBD:MAIN_MEMRL_S4]] | [[TBD:MAIN_MEMRL_S5]] | [[TBD:MAIN_MEMRL_WAL]] | [[TBD:MAIN_MEMRL_LME]] | [[TBD:MAIN_MEMRL_LCM]] | [[TBD:MAIN_MEMRL_AVG]] |
| Reflexion | [[TBD:MAIN_REFLEXION_S1]] | [[TBD:MAIN_REFLEXION_S2]] | [[TBD:MAIN_REFLEXION_S3]] | [[TBD:MAIN_REFLEXION_S4]] | [[TBD:MAIN_REFLEXION_S5]] | [[TBD:MAIN_REFLEXION_WAL]] | [[TBD:MAIN_REFLEXION_LME]] | [[TBD:MAIN_REFLEXION_LCM]] | [[TBD:MAIN_REFLEXION_AVG]] |
| ReasoningBank+MaTTS | [[TBD:MAIN_RBANKMATTS_S1]] | [[TBD:MAIN_RBANKMATTS_S2]] | [[TBD:MAIN_RBANKMATTS_S3]] | [[TBD:MAIN_RBANKMATTS_S4]] | [[TBD:MAIN_RBANKMATTS_S5]] | [[TBD:MAIN_RBANKMATTS_WAL]] | [[TBD:MAIN_RBANKMATTS_LME]] | [[TBD:MAIN_RBANKMATTS_LCM]] | [[TBD:MAIN_RBANKMATTS_AVG]] |
| **MERIT (ours)** | [[TBD:MAIN_MERIT_S1]] | [[TBD:MAIN_MERIT_S2]] | [[TBD:MAIN_MERIT_S3]] | [[TBD:MAIN_MERIT_S4]] | [[TBD:MAIN_MERIT_S5]] | [[TBD:MAIN_MERIT_WAL]] | [[TBD:MAIN_MERIT_LME]] | [[TBD:MAIN_MERIT_LCM]] | [[TBD:MAIN_MERIT_AVG]] |
| RIT-Full (upper bound) | [[TBD:MAIN_RITFULL_S1]] | [[TBD:MAIN_RITFULL_S2]] | [[TBD:MAIN_RITFULL_S3]] | [[TBD:MAIN_RITFULL_S4]] | [[TBD:MAIN_RITFULL_S5]] | [[TBD:MAIN_RITFULL_WAL]] | [[TBD:MAIN_RITFULL_LME]] | [[TBD:MAIN_RITFULL_LCM]] | [[TBD:MAIN_RITFULL_AVG]] |

推导出的核心结果：相对最佳基线的平均增益 `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`。

### Table 2 — 奖励替换插件比较
Caption intent（以最终证据为条件）：检验因果信号是否具有可移植性，以及将其作为逐操作奖励时是否能改善 RL 风格管理器；若得到支持，这将为“改进来自信号层”提供证据，但不能单独构成证明。

| Manager | Reward signal | AVG | Δ vs. original |
|---|---|---|---|
| Memory-R1 | original outcome reward | [[TBD:PLUGIN_MEMR1_ORIG_AVG]] | — (reference) |
| Memory-R1 | φ̂ (MERIT) reward | [[TBD:PLUGIN_MEMR1_PHI_AVG]] | [[TBD:REWARD_SWAP_MEMORY_R1_GAIN]] |
| Mem-α | original RL reward | [[TBD:PLUGIN_MEMALPHA_ORIG_AVG]] | — (reference) |
| Mem-α | φ̂ (MERIT) reward | [[TBD:PLUGIN_MEMALPHA_PHI_AVG]] | [[TBD:REWARD_SWAP_MEMALPHA_GAIN]] |

### Table 3 — 消融矩阵
Caption intent（以最终证据为条件）：检验 MERIT 各组件的必要性；特别检验将因果信用换回共现效用（A2）是否会移除增益，从而把贡献定位到信号。

| Variant | AVG | ΔAVG vs. full | SR@20% (t=500) | CCC (held-out) | CTI |
|---|---|---|---|---|---|
| Full MERIT | [[TBD:ABL_FULL_AVG]] | 0 (reference) | [[TBD:ABL_FULL_SR20]] | [[TBD:ABL_FULL_CCC]] | [[TBD:ABL_FULL_CTI]] |
| A1: no recalibration (static attributor) | [[TBD:ABL_A1_AVG]] | [[TBD:ABL_A1_DELTA]] | [[TBD:ABL_A1_SR20]] | [[TBD:ABL_A1_CCC]] | [[TBD:ABL_A1_CTI]] |
| A2: causal credit → co-occurrence utility | [[TBD:ABL_A2_AVG]] | [[TBD:ABL_A2_DELTA]] | [[TBD:ABL_A2_SR20]] | [[TBD:ABL_A2_CCC]] | [[TBD:ABL_A2_CTI]] |
| A3: no scope gating | [[TBD:ABL_A3_AVG]] | [[TBD:ABL_A3_DELTA]] | [[TBD:ABL_A3_SR20]] | [[TBD:ABL_A3_CCC]] | [[TBD:ABL_A3_CTI]] |
| A4: no governance | [[TBD:ABL_A4_AVG]] | [[TBD:ABL_A4_DELTA]] | [[TBD:ABL_A4_SR20]] | [[TBD:ABL_A4_CCC]] | [[TBD:ABL_A4_CTI]] |
| A5: no usage-behavior features | [[TBD:ABL_A5_AVG]] | [[TBD:ABL_A5_DELTA]] | [[TBD:ABL_A5_SR20]] | [[TBD:ABL_A5_CCC]] | [[TBD:ABL_A5_CTI]] |
| A-judge: LLM self-judge instead of RIT | [[TBD:ABL_AJUDGE_AVG]] | [[TBD:ABL_AJUDGE_DELTA]] | [[TBD:ABL_AJUDGE_SR20]] | [[TBD:ABL_AJUDGE_CCC]] | [[TBD:ABL_AJUDGE_CTI]] |
| A7: LOO → group/sampled-Shapley | [[TBD:ABL_A7_AVG]] | [[TBD:ABL_A7_DELTA]] | [[TBD:ABL_A7_SR20]] | [[TBD:ABL_A7_CCC]] | [[TBD:ABL_A7_CTI]] |

### Table 4 — 假设—实验映射
（见前文“假设—实验映射”；这里是其计划表格形式。没有实验数据单元格，所有单元格均为设计元数据或假设标签；状态列为 `HYPOTHESIS`。）

| Hyp. | Metric | Experiment | Claim | Status |
|---|---|---|---|---|
| H1 | SR@20% slope | Ablation A4 / Mechanism | C3 | HYPOTHESIS |
| H2 | held-out CCC | Fig. 5a / Calibration | C2 | HYPOTHESIS |
| H3 | CTI; transfer CCC | Ablation A3 / Transfer | C3 | HYPOTHESIS |
| H4 | AVG vs. token cost | Efficiency Study | C4 | HYPOTHESIS |
| H5 | gain vs. bank/heterogeneity/redundancy | Boundary & Case Study | C4 | HYPOTHESIS |

### Table 5 — 方法比较/相关工作定位
Caption intent：在本报告当前列出的方法中，计划将 MERIT 定位为同时结合 causal signal、O(1) online scoring、closed-loop recalibration、per-memory scope 和 standalone audit protocol 的方法。该定位及每个 ✓ / ✗ / — 单元格在写入论文前都必须完成文献核验。

| Method | Causal signal | O(1) online | Closed-loop recalibration | Scope representation | Audit protocol |
|---|---|---|---|---|---|
| Data Shapley `[[TBD:CITATION_DATA_SHAPLEY]]` | ✓ | ✗ | ✗ | ✗ | ✗ |
| Influence Functions `[[TBD:CITATION_INFLUENCE_FUNCTIONS]]` | ✓ | ✗ | ✗ | ✗ | ✗ |
| TracIn `[[TBD:CITATION_TRACIN]]` | ✓ | ✗ | ✗ | ✗ | ✗ |
| ContextCite `[[TBD:CITATION_CONTEXTCITE]]` | partial | ✗ | ✗ | ✗ | ✗ |
| ReasoningBank `[[TBD:CITATION_REASONINGBANK]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| SkeMex `[[TBD:CITATION_SKEMEX]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| Memory-R1 `[[TBD:CITATION_MEMORY_R1]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| MemRL `[[TBD:CITATION_MEMRL]]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| **MERIT (ours)** | ✓ | ✓ | ✓ | ✓ | ✓ |

### Table 6 — 效率/成本比较
Caption intent：检验 MERIT 是否能以接近基线的 token 成本恢复 full-intervention 的大部分增益，并位于 Pareto 前沿拐点。

| Config | Relative token cost | AVG success | ACA latency/event | Extra VRAM | RIT sampling overhead |
|---|---|---|---|---|---|
| Co-occurrence baseline | 1× | [[TBD:EFF_BASELINE_AVG]] | — | — | 0 |
| MERIT | [[TBD:MERIT_RELATIVE_TOKEN_COST]] | [[TBD:EFF_MERIT_AVG]] | [[TBD:ACA_SCORING_LATENCY_MS]] | [[TBD:ACA_VRAM_OVERHEAD_GB]] | [[TBD:RIT_TOKEN_OVERHEAD_PERCENT]] |
| A1 (static attributor) | [[TBD:A1_RELATIVE_TOKEN_COST]] | [[TBD:EFF_A1_AVG]] | [[TBD:ACA_SCORING_LATENCY_MS]] | [[TBD:ACA_VRAM_OVERHEAD_GB]] | [[TBD:RIT_TOKEN_OVERHEAD_PERCENT]] |
| RIT-Full (upper bound) | [[TBD:RITFULL_RELATIVE_TOKEN_COST]] | [[TBD:EFF_RITFULL_AVG]] | — | — | [[TBD:FULL_RIT_COST_MULTIPLIER]] |

---

## 计划图示

此处不生成图片。每张图均给出完整文字规格。**Fig. 2 和 Fig. 5 必须使用完全相同的坐标范围**，以支持机制闭环比较。

### Fig. 1 — 问题 + 解决方案示意图
- **Purpose：** 说明论文动机——相关性信用把记忆库变成斯金纳箱；MERIT 用随机试验的证据替换共现记账。
- **Panel layout：** 两个 panel（左：问题/基线；右：MERIT）。
- **Visual entities：** 左侧为最高效用记忆，并高亮其中没有因果作用的比例；右侧为 RIT→ACA→consumers pipeline，使迷信积累曲线变平。
- **Compared stages：** correlational credit vs. counterfactual credit。
- **Intended takeaway：** 计划测量最高效用记忆中无因果作用者所占 `[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]`；检验 MERIT 是否压平迷信积累。
- **Future data source：** pilot SR@k 和主实验机制分析。
- **Placeholders required：** `[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]`。
- **Source anchor：** §3.5 Fig.1。

### Fig. 2 — 诊断证据（baseline）
- **Purpose：** 检验系统分配的 utility 是否很少追踪真实反事实贡献，以及迷信是否随部署增长。
- **Panel layout：** (a) utility 与 φ 的散点/相关图；(b) SR@20% vs. 部署长度。
- **Axes：** (a) x = system utility，y = counterfactual φ；(b) x = task index t（100→500），y = SR@20%（%）。**坐标范围锁定为与 Fig. 5 相同。**
- **Compared methods：** ReasoningBank、MemRL。
- **Intended takeaway：** (a) CCC `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`；(b) 检验 SR 是否从 `[[TBD:PILOT_SR20_T100]]` 增至 `[[TBD:PILOT_SR20_T500]]`，以及相关性信用是否无法自我纠正。
- **Future data source：** pilot/diagnostic study。
- **Placeholders required：** `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`、`[[TBD:PILOT_SR20_T100]]`、`[[TBD:PILOT_SR20_T500]]`。
- **Source anchor：** §3.5 Fig.2、§4。

### Fig. 3 — MERIT 架构/方法
- **Purpose：** 展示“检索—执行—写入”循环上的 `RIT → ACA → consumers` pipeline。
- **Panel layout：** 单个从左到右的 pipeline 图，包含基础循环和三个新增模块。
- **Visual entities：** RIT sampling（paired LOO）、ACA attributor（features → φ̂）、两个 consumers（governance、scope-gated retrieval）及 recalibration feedback edge。
- **Compared stages：** standard loop vs. MERIT-augmented loop。
- **Intended takeaway：** 改动最小且依赖严格线性；消融将检验增益是否来自信号而非 pipeline 复杂度。
- **Future data source：** 无（schematic）。
- **Placeholders required：** 无（无数据）。
- **Source anchor：** §6.0 Fig.3。

### Fig. 4 — 流式累计成功曲线
- **Purpose：** 检验 MERIT 的优势是否随任务流扩大，且是否集中在后期、污染最严重的部分。
- **Panel layout：** 单幅折线图，cumulative success vs. task index；MERIT 与 baselines 对比。
- **Axes：** x = task index（1→500+），y = cumulative success rate。
- **Compared methods：** MERIT、最强 baselines、RIT-Full。
- **Intended takeaway：** 检验平均增益 `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]` 中有多少来自任务流后段，即 `[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]`。
- **Future data source：** 主实验流式日志。
- **Placeholders required：** `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`、`[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]`。
- **Source anchor：** §3.5 Fig.4、§8.3。

### Fig. 5 — 机制恢复（MERIT）
- **Purpose：** 检验摊销归因是否能以 O(1) 成本恢复因果信用，以及是否能消除 Fig. 2 中的迷信增长。
- **Panel layout：** (a) φ̂ vs. φ 的可靠性/相关性；(b) SR@20% vs. 部署长度，MERIT 与 baseline 对比。
- **Axes：** 与 Fig. 2 使用完全相同的范围（强制要求）。(a) x = φ̂，y = φ；(b) x = t（100→500），y = SR@20%（%）。
- **Compared methods：** ACA（MERIT）vs. correlational baseline。
- **Intended takeaway：** (a) CCC `[[TBD:ACA_HELDOUT_CCC_T500]]` 与 Fig. 2a 的 `[[TBD:PILOT_CCC_REASONINGBANK_T500]]` 对比；(b) 检验 SR 是否压平至 `[[TBD:SR_MERIT_T500]]`（t=500 时降低 `[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]`）。
- **Future data source：** mechanism & calibration analysis。
- **Placeholders required：** `[[TBD:ACA_HELDOUT_CCC_T500]]`、`[[TBD:PILOT_CCC_REASONINGBANK_T500]]`、`[[TBD:SR_MERIT_T500]]`、`[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]`。
- **Source anchor：** §3.5 Fig.5、§8.5。

### Fig. 6 — 直觉/案例研究（A3 边界）
- **Purpose：** 通过一条成功记忆与一条迷信记忆传达直觉，并展示暴露 A3 边界的互补记忆失效。
- **Panel layout：** 两个 mini-timeline（成功示例；包含分组干预后备方案的失败示例）。
- **Visual entities：** utility trajectory vs. RIT φ over tasks；eviction event；scope characterization。
- **Compared stages：** correlational accumulation vs. RIT judgment vs. governance action。
- **Intended takeaway：** 检验虚高效用的迷信记忆是否会在任务 `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]` 被发现并淘汰；互补记忆是否需要分组后备方案（诚实展示 A3 限制）。
- **Future data source：** case study logs。
- **Placeholders required：** `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]`。
- **Source anchor：** §8.6 Fig.6、§5 (A3)。

---

## 已知弱点、假设与范围边界

- **A2 依赖（局部可回放）：** 完全不可回放的物理/单次环境无法产生 RIT 标签。前瞻方向：用世界模型模拟回放或 off-policy evaluation 替代真实干预。
- **A3 依赖（高冗余时 LOO 低估信用）：** 分组干预后备方案会增加成本。前瞻方向：结构感知的交互归因。
- **增益边界（H5）：** 计划检验单领域短任务流和小记忆库是否只产生很小收益——MERIT 面向长期部署，而非短会话。预计剩余失败中有 `[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]` 来自缺少经验而不是信用错误，这与“写入什么”的研究方向互补。
- **范围声明（保留自源方案）：** “我们关注已有记忆的信用分配，不研究写入什么的策略（写入时质量）；MERIT 可以与这类方法组合。”
- **更广泛影响/rebuttal 敏感风险：** 因果审计计划改善可解释性和可治理性；风险在于，若外部内容可以操纵归因分数，就会形成新的攻击面，即 memory-poisoning 的 “credit laundering”。
- **显式跟踪的 rebuttal 风险（源方案 §11）：** (1) 干预成本是否现实；(2) 归因噪声/φ̂ 是否可信；(3) 是否只是把 Data Shapley/ContextCite 用于记忆；(4) 相对 MemRL/Memory-R1 的增量；(5) 是否只适用于文本可回放环境。每项均计划提供设计与实验两层防御。
- **OPEN QUESTION（不是 claim）：** ACA 是否能迁移到测试文本/agentic 环境之外的根本不同模态，为 `NOT SPECIFIED IN SOURCE`；将其标为开放问题，不纳入 C1–C4。

---

## 相关工作图谱

只保留源方案点名的方法或论文族；所有引用元数据均 `requires bibliographic verification`，并使用 `[[TBD:CITATION_<NAME>]]`。不得编造 BibTeX、DOI、作者列表或论文结论。不得在没有限定语的情况下声称某项工作“从未做过”。

- **自进化记忆与经验提炼（→ C1）：** Mem0 `[[TBD:CITATION_MEM0]]`、A-MEM `[[TBD:CITATION_A_MEM]]`、AWM `[[TBD:CITATION_AWM]]`、ReasoningBank `[[TBD:CITATION_REASONINGBANK]]`、SkeMex `[[TBD:CITATION_SKEMEX]]`、MemEvolve `[[TBD:CITATION_MEMEVOLVE]]`。源方案将这些方法的信用信号描述为启发式或基于共现；此描述需要文献核验。计划定位（同样需要核验）：本报告尚未识别出使用干预证据审计这些信号因果有效性的既有工作；这是 C1 针对的空缺。
- **学习式记忆管理（→ C3）：** Memory-R1 `[[TBD:CITATION_MEMORY_R1]]`、Mem-α `[[TBD:CITATION_MEM_ALPHA]]`、MemRL `[[TBD:CITATION_MEMRL]]`、MemSkill `[[TBD:CITATION_MEMSKILL]]`——源方案认为这些方法学习的是策略，而信号仍处于结果层或 MC 共现层，此定位需要核验。EDV `[[TBD:CITATION_EDV]]` 使用多智能体共识修复写入时判断，与修复全生命周期信用正交且可组合；该描述也需核验。
- **数据估值与上下文归因（→ C2）：** Data Shapley `[[TBD:CITATION_DATA_SHAPLEY]]`、Influence Functions `[[TBD:CITATION_INFLUENCE_FUNCTIONS]]`、TracIn `[[TBD:CITATION_TRACIN]]` 面向训练数据（静态、离线）；ContextCite `[[TBD:CITATION_CONTEXTCITE]]` 和 RAG attribution 面向单次生成解释。计划定位（需要核验）：在线、非平稳、归因会改变数据分布的闭环环境需要摊销 + 重新校准，这是 C2 针对的空缺。
- **源方案点名的相关观察：** Evo-Memory `[[TBD:CITATION_EVO_MEMORY]]` 和 EEVEE `[[TBD:CITATION_EEVEE]]`（跨任务干扰）；Reflexion `[[TBD:CITATION_REFLEXION]]` 和 MaTTS `[[TBD:CITATION_MATTS]]`（测试时推理，作为正交方向基线）；Skinner superstition analogy `[[TBD:CITATION_SKINNER_SUPERSTITION]]`。
- **并发工作条款（保留）：** 计划在投稿前两周进行 arXiv 扫描；预留措辞：“Concurrent work [X] explores ..., differing from ours in that their signal remains observational / their attribution is not closed-loop.”

---

## 拟定标题

- **主标题：** *MERIT: Retrieval Is Not Contribution — Counterfactual Credit Assignment for Self-Evolving Agent Memory*
- **备选 1（偏分析）：** *Superstitious Memories: How Correlational Credit Corrupts Self-Evolving Agents, and How to Fix It*
- **备选 2（保守方法型）：** *Counterfactual Memory Attribution for Self-Evolving LLM Agents*
- **命名检查（投稿前执行任务）：** 搜索 “MERIT + LLM/memory/agent” 以确认没有名称冲突；若冲突，改用保留名称 “CREDO / VERITY” 并全局替换。

---

## 目标投稿场所

- **AAAI 2027** 匿名初稿。适用 track 与页数限制为 `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`，必须根据对应的 AAAI 2027 call 确认；Author Kit 说明页数限制由具体 event 决定。
- 仅作来源背景（**不得**覆盖当前任务）：源方案首选 NeurIPS 2027 / ICML 2027，备选 AAAI-28。

---

## 来源可追溯映射

以下每个对象都映射回 `paper/00_input/source_proposal.md` 的具体章节。源方案未明确提供的细节标为 `NOT SPECIFIED IN SOURCE`。

- **C1** → §3 P6 (C1)、§4 Pilot、§3.5 Fig.2、§5 Prop.1。
- **C2** → §3 P6 (C2)、§6.2、§8.5、§3.5 Fig.5。
- **C3** → §3 P6 (C3)、§6.3、§8.4、§8.3 Table 2。
- **C4** → §3 P6 (C4)、§8。
- **Proposition 1** → §5（非正式陈述）、appendix C（引用的正式证明）。
- **A1（observable outcome）** → §5 Assumptions A1。
- **A2（local replayability）** → §5 Assumptions A2；§4（可回放任务流）；§6.1（只在 A2 任务上采样）。
- **A3（low-order interaction）** → §5 Assumptions A3；§8.5/§8.6（边界）、Fig.6。
- **RIT module** → §6.1；首次出现于 §4（干预协议）。
- **ACA module** → §6.2；§8.5（校准）。
- **Credit Governance** → §6.3（三条规则）；§0（RL manager 被降级）。
- **Scope-Gated Retrieval** → §6.3（gating）；§7（CTI 定义）。
- **Cost/Complexity** → §6.4；§8.1（硬件）；appendix B/E（成本表）。
- **H1** → 标签为推断；源锚点 §6.3（治理）/ §8.5（SR 恢复）、§7 映射表（未明确写出）。
- **H2** → §8.5（CCC 恢复，ρ≥0.6 门槛）、§6.2、§3.5 Fig.5a。
- **H3** → §8.5（迁移、CTI）、§6.3、§7（CTI 定义）。
- **H4** → §8.7（效率）、§8.5（p-sweep 饱和）。
- **H5** → §4（边界说明）、§8.5（三条趋势线）、§10（局限）。
- **Table 1（main）** → §8.3（Table 1 结构）。S2–S4 身份为 `NOT SPECIFIED IN SOURCE`。
- **Table 2（plugin）** → §8.3 (Table 2)、§6.3。
- **Table 3（ablation）** → §8.4（A1–A7、A-judge）、§6.4（设计选择行）。
- **Table 4（hypotheses）** → §7、§12（假设闭合检查表）。
- **Table 5（positioning）** → §9（比较表列）。
- **Table 6（efficiency）** → §8.7（Pareto 图）。
- **Fig. 1** → §3.5 Fig.1。
- **Fig. 2** → §3.5 Fig.2、§4。
- **Fig. 3** → §6.0。
- **Fig. 4** → §3.5 Fig.4、§8.3。
- **Fig. 5** → §3.5 Fig.5、§8.5。
- **Fig. 6** → §8.6、§5 (A3)。
- **Limitations** → §10（三项局限）、§11（rebuttal 风险）。
- **Rebuttal-sensitive risks** → §11（五个攻击点）、§8.5（校准防御）。
- **Subtraction decisions（RL manager、full Shapley 被降级）** → §0。
- **Venue** → §-1 header / 用法说明（源方案首选 NeurIPS/ICML 2027、备选 AAAI-28）；当前任务覆盖为 AAAI 2027，是任务级指令，`NOT SPECIFIED IN SOURCE`。
Input: stream {q_t}, bank M, retriever R, policy π, attributor g_θ, budget p
for t = 1,2,...:
    C ← R(q_t)   # scope-gated: α·rel + β·scope + γ·credit, quarantine exploration bonus
    y_t, traj ← π(q_t, C);  r_t ← env/judge(y_t)
    for m_i in C:  φ̂_i ← g_θ(x_i(q_t, traj));  update φ̄_i, proto±_i
    if replayable(q_t) and rand() < p:            # RIT sampling
        for m_i in C: label ← paired_LOO(q_t, C, m_i, K=5); pool.add(label)
    governance(M): evict / merge / quarantine by rules(φ̄, n)
    if t % 100 == 0: recalibrate g_θ on pool (Huber + isotonic)
```
