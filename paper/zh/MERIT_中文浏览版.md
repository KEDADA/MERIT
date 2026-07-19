# MERIT：检索不等于贡献——面向自演化智能体记忆的反事实信用分配

> **用途说明**：本文档仅用于中文快速浏览，不是 AAAI 投稿源文件，也不取代英文稿。
> 英文 LaTeX 与 `paper/build/main.pdf` 是唯一权威版本。本中文版同步自 2026-07-19
> 完成 Round 2 修订后的工作初稿。所有 `[[TBD:...]]` 均为已登记但尚未回填的占位符；
> 文中实验结论均为计划验证的假设，不代表已经观察到的结果。

## 摘要

自演化语言模型智能体会把交互轨迹提炼成持久记忆库，再在后续任务中检索和复用。
这一闭环能否真正实现自我改进，取决于系统能否把信用正确分配给单条记忆。本文认为，
现有系统常用的信用信号本质上是相关性的：只要某条记忆与成功同时出现，它就会被强化，
于是系统把“被检索”误当成了“作出贡献”。

我们假设，在这种信用机制下会形成“迷信记忆”：它们对当前任务的即时因果效果为零或为负，
却持续积累效用并占据检索位置，而且其比例可能随部署时间增长。真正需要估计的是记忆的
**即时条件检索贡献**：在当前查询、检索集合和部署历史给定的情况下，从检索集合中移除该
记忆会使即时任务结果下降多少。这个量只能通过反事实干预定义，而逐条在线干预看似成本过高。

为此，本文提出 MERIT，其流程严格为：

1. **RIT（随机化干预试验）**：以小预算执行成对的 leave-one-out 干预，收集干预标签；
2. **ACA（摊销反事实归因）**：将 RIT 标签摊销为逐事件贡献预测；在特征维度 $d$ 和
   top-$k$ 固定时，其单次评分成本不随记忆库大小增长；
3. **两个消费者**：信用治理和范围门控检索共同使用 ACA 信号。

计划实验将检验 ACA 能否以较低成本恢复即时贡献、两个消费者能否抑制迷信记忆并减少跨任务
干扰，以及 MERIT 能否超过最强基线。计划中的主要平均增益为
`[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`，尚待实验验证。

## 1. 引言

智能体正从无状态应答器转向经验驱动系统：它们通过“检索—执行—写入”循环，把自己的轨迹写入
记忆库并不断复用。这个范式隐含了一个关键前提：系统知道哪条记忆值得获得信用，因为写入、合并、
淘汰和检索都依赖逐记忆效用信号。然而常见系统在任务成功后直接提高所有已检索记忆的效用，混淆了
“被检索”“被模型使用”和“真正产生因果帮助”三个不同事件。

### 1.1 核心问题：检索不等于贡献

本文只研究**即时条件检索贡献**，不把它宣称为记忆的长期保留价值。相关性信用无法直接测量这个
反事实量。我们假设，高效用又会提高未来检索概率，从而形成正反馈：没有贡献的记忆也可能持续进入
top-utility 集合。另一个相关问题是跨任务干扰：对任务族 A 有用的记忆被无差别用于任务族 B，反而
损害 B 的表现。

### 1.2 为什么已有信号不足

- 经验蒸馏、环境反馈效用和结果级强化学习通常学习“采取什么记忆管理动作”，其底层奖励仍可能是
  结果级或共现信号。本文不把所有探索式强化学习都简单归为相关性方法，而只对实际评测的系统和
  任务流作出诊断。
- Data Shapley、Influence Functions、TracIn 等主要处理静态离线训练数据；ContextCite 等解释单次
  生成。MERIT 面向在线、非平稳、闭环环境，其中归因本身会改变未来检索分布。

### 1.3 方法概览

MERIT 在标准闭环中加入 `RIT → ACA → consumers`：RIT 产生小预算干预标签，ACA 学习逐事件
贡献并周期性重新校准，信用治理与范围门控检索消费该信号。这里的消费者是接受经验检验的设计，
不是长期保留价值的因果估计器。

### 1.4 贡献

- **C1：迷信记忆诊断。** 在受评系统和任务流中，用 CCC（信用—贡献相关性）和 SR@$k$
  （迷信率）检验零/负贡献记忆是否在高效用集合中累积。
- **C2：摊销反事实归因。** 用 ACA 将 RIT 干预标签摊销为逐事件分数，并检验其准确性、校准性和成本。
- **C3：可直接消费的信用信号。** 检验信用治理是否压平迷信率增长、范围门控是否降低跨任务干扰。
  把该信号替换管理器原奖励只作为次要的信号可迁移性分析。
- **C4：系统评测。** 计划在四类基准、三个主干模型和多个独立部署运行上，与最强基线比较平均成功率
  和 token 开销。正式 seed 数由独立 pilot 的功效分析确定。

所有实证陈述都是计划检验，不是已经测得的结论。若某项证伪门失败，相应主张必须收窄，而不能隐藏
失败结果。

## 2. 相关工作

本文按“使用何种信用信号”组织相关工作，而不是逐篇罗列；所有引用元数据仍需联网核验。

1. **自演化记忆与经验蒸馏。** 包括 Mem0、A-MEM、AWM、ReasoningBank、SkeMex、MemEvolve 等。
   按当前待核验的描述，这些系统常把检索记忆与任务结果共同出现当作信用。MERIT 的差异是用干预
   证据审计该信用，而不是增加另一套启发式。
2. **学习式记忆管理。** 包括 Memory-R1、Mem-$\alpha$、MemRL、MemSkill 等。MERIT 与探索式
   结果奖励学习是互补关系：前者针对信用信号，后者针对管理策略。只有在实现和奖励机制逐项核验后，
   才能准确描述各基线。
3. **数据估值与上下文归因。** 这些方法与 MERIT 都采用反事实视角，但通常处在静态、离线或单次生成
   场景。MERIT 必须处理归因—检索—新标签相互影响的闭环漂移。
4. **干扰及正交方向。** 混合任务流中的跨任务干扰是直接相关问题；Reflexion、MaTTS 等测试时推理
   方法属于正交且可组合的基线。

## 3. 问题定义与迷信记忆假设

### 3.1 设置与符号

智能体处理任务流 $\{(q_t,r_t)\}$，其中 $q_t$ 是查询或任务，$r_t\in[0,1]$ 是环境成功信号或经
一致性检查的评分。时刻 $t$ 的记忆库为 $\mathcal M_t=\{m_i\}$，检索器为

$$R_t(q_t;\mathcal M_t,\bar\varphi,S)=C_t\subseteq\mathcal M_t,$$

返回 top-$k$ 记忆集合。MERIT 额外维护归因器 $A$、逐记忆运行信用 $\bar\varphi_i$ 和范围表示 $S_i$。

### 3.2 定义 1：即时检索贡献

对查询 $q$、实际检索集合 $C$ 和历史 $H_t$，记忆 $m_i$ 的即时贡献定义为

$$
\varphi_{i,t}(q,C)=\mathbb E_\xi\left[r_t(C;\xi)-r_t(C\setminus\{m_i\};\xi)\mid H_t\right].
$$

这是单次检索事件的**字面移除效应**，不是长期记忆价值。RIT 实际使用等长 neutral pad 替换被移除
记忆，因此只有当 `[[TBD:PILOT_NEUTRAL_PAD_VALIDATION]]` 对应的预注册等价性检验通过时，RIT
标签才可解释为移除效应；否则必须降级称为 **pad-replacement contribution**，字面移除仍属未验证
的未来工作。本稿不增加 no-pad 实验臂。

必须区分六个量：

- $\varphi$：真实逐事件即时贡献；
- $\widetilde\varphi$：有限次 RIT rollout 得到的逐事件估计；
- $\widehat\varphi$：ACA 的逐事件预测；
- $\bar\varphi_i$：$\widehat\varphi$ 的在线运行聚合；
- $\Phi_i=\mathbb E[\varphi_{i,t}]$：审计分布下的真实记忆级聚合目标；
- $\widetilde\Phi_i$：有限 RIT 审计估计，不称为 ground truth。

审计总体是冻结记忆库快照、common-support 区域内、以被检索事件为条件的概率抽样分布；事件均权。
$\widehat U_i$、$\bar\varphi_i$ 与 $\widetilde\Phi_i$ 必须在同一审计总体上比较。窗口、最低样本量和
纳入设计仍为 `USER_APPROVAL_REQUIRED`。

### 3.3 定义 2：共现效用

$$
\widehat U(m_i)=
\frac{\sum_t \mathbf 1[m_i\in R(q_t)]r_t}
     {\sum_t \mathbf 1[m_i\in R(q_t)]}.
$$

它是“检索了该记忆的任务”的平均结果，属于关联性信号。

### 3.4 Observation 1：分解恒等式

$$
\mathbb E[r(C)\mid i\text{ 被检索}]
=\mathbb E[r(C\setminus\{m_i\})\mid i\text{ 被检索}]
+\mathbb E[\varphi_i\mid i\text{ 被检索}].
$$

因此 $\widehat U_i$ 混合了 leave-one-out 基线成功率与平均贡献，是一个可能与即时贡献错位的复合
信号。该等式由定义直接成立，不需要额外假设。

### 3.5 Conjecture 1：迷信均衡（未证明）

若检索与任务本身的可解性统计相关，且效用又参与未来检索排序，这种错位可能被放大，形成
$\widehat U_i$ 很高但 $\varphi_i=0$ 的稳定迷信均衡。这只是待 pilot 检验的闭环机制假设，不是定理。

### 3.6 假设边界

- **AS1：结果可观测。** 每个任务有可用的环境结果或经一致性检查的评分。
- **AS2：局部可回放。** 至少有一部分任务可从固定初始状态重放；只有 RIT 收集标签依赖此条件。
- **AS3：交互限制。** LOO 本身就是目标，不是 Shapley 的近似误差。它不能捕获高阶交互；冗余/可替代
  记忆可能各自 LOO 近零但联合价值为正。群体干预只作为 A7 探索性分析，没有数值保证，也不提出
  个体 Shapley 主张。

## 4. 诊断性 Pilot

Pilot 的目标不是引入第二种方法，而是先检验问题是否真实存在，并为正式实验冻结采样规模。

### 4.1 诊断指标

- **事件级 CCC**：$\mathrm{CCC}(\widehat\varphi_{i,t},\widetilde\varphi_{i,t})$，衡量 ACA 对 RIT
  标签的拟合忠实度。
- **记忆级 CCC**：$\mathrm{CCC}(\widehat U_i\text{ 或 }\bar\varphi_i,\widetilde\Phi_i)$，衡量运行
  信用与审计贡献的一致性。
- **SR@$k$**：top-$k$ 高信用记忆中，其 $\widetilde\Phi_i$ 置信区间落在负贡献区或实际零区的比例。
  harmful 与 practically-null 两类分别报告。

### 4.2 两阶段固定设计

1. 在 pilot 前按“最小具有实际意义的贡献”预注册等价带 $\delta$、MEI、功效和目标 CI 半宽；
2. Stage-1 使用固定 $K=5$ 的独立 pilot 估计方差；
3. 根据 pilot 方差计算并冻结正式 $K$、$n^{audit}$ 和 seed 数；
4. Stage-1 数据不得进入 confirmatory gate，不使用自适应停止；
5. 正式审计采用已知纳入概率的随机或分层随机 AUDIT 抽样，优先抽样只用于 TRAIN。

RIT 还需验证 common support、neutral pad 等价性，并用 rollout-equivalent/event 与 token 成本显式报告
开销。所有尚未锁定的数值继续保持 `USER_APPROVAL_REQUIRED`。

## 5. MERIT 方法

### 5.1 RIT：收集干预标签

对被概率抽样选中的已检索记忆执行成对 shadow replay：保持查询、初始状态和其余上下文一致，对比完整
集合与移除/neutral-pad 替换集合的结果。shadow RIT 不修改在线记忆库。标签被固定路由到四个互不重叠
的数据角色：**fit、calibration、development、sealed final-audit**。

### 5.2 ACA：摊销反事实归因

ACA 用两层预测头从查询—记忆相关性、轨迹使用特征、结果一致性等特征预测 $\widehat\varphi$，并周期性
重新校准。fit 用于拟合，calibration 用于等距校准，development 用于超参数和阈值，sealed final-audit
只用于最终评估，不能参与模型选择或停止决策。闭源模型若不暴露 token log-probability，则屏蔽该特征。

### 5.3 两个信号消费者

**信用治理。** 淘汰与合并不能只看 $\bar\varphi_i$ 点估计，而要使用保守校准界和跨多次更新的重复证据。
合并还要求高嵌入相似度；新记忆进入 quarantine，并通过独立的随机强制纳入获得冷启动探索机会。治理
dead-zone、置信水平和重复次数仍需预注册。

**范围门控检索。** 每条记忆维护正、负查询原型，检索分数为

$$
\mathrm{score}=\alpha\,\mathrm{rel}
+\beta\,[\mathrm{sim}(q,\mathrm{proto}^+)-\mathrm{sim}(q,\mathrm{proto}^-)]
+\gamma\bar\varphi_i.
$$

暂定 $(\alpha,\beta,\gamma)=(1.0,0.5,0.3)$，属于 provisional 配置，不是实验结果。

### 5.4 成本与主循环

ACA 每个查询处理 top-$k$ 记忆的复杂度为 $O(kd)$，即每个被检索记忆事件为 $O(d)$；当 $d,k$ 固定
时，它不随记忆库大小增长。RIT 和周期校准成本单独核算。主循环依次执行：检索、独立强制探索、任务执行、
ACA 评分与状态更新、baseline writer 写入、概率触发 shadow RIT、四池路由、基于不确定性的治理、周期校准。

## 6. 实验与分析计划

### 6.1 设置

计划使用三个 backbone、四类基准：流式任务、Web Agent、长期记忆、对话记忆；pilot 使用两个可回放
环境。所有方法共享 backbone、retriever 和 top-$k=4$，并获得相同 token 预算。宏平均先将 S1–S5
合成为 Evo-Memory 类别分，再与 WebArena、LongMemEval、LoCoMo 四类等权平均。

推断单位固定为 **seed/deployment run**，流内采用层级/block resampling；确证性 C1–C4 与
max-baseline 对比使用 Holm FWER，探索性扫描才使用 FDR。正式 seed 数由独立 pilot 功效分析计算。
基线必须标记为 source-faithful reproduction 或 standardized credit-variant wrapper，只有前者才能直接
使用原方法名称。

### 6.2 跨任务干扰 CTI

$$
\mathrm{CTI}=\mathrm{Acc}_B(\text{仅 B 记忆库})-
\mathrm{Acc}_B(\text{A+B 混合记忆库}).
$$

$\mathrm{CTI}\ge0$ 表示加入 A 域记忆后 B 域准确率下降。具体 A/B 配对尚未确定。

### 6.3 尚待锁定的复现信息

S2–S4 流身份与异质性分箱、数据集版本、三个 backbone、流构造与顺序、记忆库规模计划、warm-up、
四池比例、judge 协议、基线适配器、CTI 配对、max-baseline 统计量、Holm $\alpha$、FDR $q$ 及各门槛
均为 `USER_APPROVAL_REQUIRED`，本稿不猜测。

### 6.4 分析模块

- **主结果**：比较 14 种方法，检验异质性越高时 MERIT 增益是否更大，以及 MERIT 能否以较低成本
  接近 RIT-Full 干预参考。
- **奖励替换（次要分析）**：把 $\widehat\varphi$ 替换为两个管理器的结果奖励，检验信号可迁移性。
- **消融**：A1 无重校准；A2 容量匹配的观察标签对照；A3 无范围门控；A4 无治理；A5 无使用特征；
  A-judge 使用 LLM 自评；A7 为探索性群体干预。
- **机制与校准**：比较事件/记忆级 CCC、SR 轨迹、ECE、域内校准和 split-half 稳定性。
- **边界与扩展（次要分析）**：更大 backbone、zero-shot transfer、记忆库规模、流异质性和冗余。
- **效率**：累计成功率、RIT 预算扫描、token、延迟、显存和摊销 RIT 成本。
- **案例**：有用记忆与迷信记忆的治理时间线，以及冗余/可替代记忆暴露 AS3 边界的案例。

## 7. 局限与结论

MERIT 有三项主要边界：完全不可回放的单次环境无法直接产生 RIT 标签；LOO 无法覆盖高阶交互，A7
群体分析成本更高且没有数值保证；单域短流和小记忆库可能几乎没有收益。本文只研究既有记忆的即时
信用分配，不解决写入内容质量，也不把治理与范围门控宣称为长期保留价值的因果估计器。外部内容还可能
通过操纵归因分数造成“credit laundering”攻击面。

核心结论仍是待验证的研究主张：自演化记忆系统的问题可能不只是缺少更好的启发式，而是缺少可靠、
可负担的即时反事实信用。MERIT 用 RIT 产生少量干预标签、ACA 摊销这些标签，并把同一信号提供给
治理和范围门控。最终是否成立，取决于所有预注册证伪门及真实实验数据。

---

## 附录 A：六张计划表格

### 表 1：主结果

列说明：S1–S5 为异质性递增的流式任务；W-A 为 Web Agent；LME 为长期记忆；LCM 为对话记忆；
AVG 为两阶段宏平均。

| 方法 | S1 | S2 | S3 | S4 | S5 | W-A | LME | LCM | AVG |
|---|---|---|---|---|---|---|---|---|---|
| No-Memory ReAct | `MAIN_NOMEM_S1` | `MAIN_NOMEM_S2` | `MAIN_NOMEM_S3` | `MAIN_NOMEM_S4` | `MAIN_NOMEM_S5` | `MAIN_NOMEM_WAL` | `MAIN_NOMEM_LME` | `MAIN_NOMEM_LCM` | `MAIN_NOMEM_AVG` |
| Full-History Stuffing | `MAIN_FULLHIST_S1` | `MAIN_FULLHIST_S2` | `MAIN_FULLHIST_S3` | `MAIN_FULLHIST_S4` | `MAIN_FULLHIST_S5` | `MAIN_FULLHIST_WAL` | `MAIN_FULLHIST_LME` | `MAIN_FULLHIST_LCM` | `MAIN_FULLHIST_AVG` |
| Mem0 | `MAIN_MEM0_S1` | `MAIN_MEM0_S2` | `MAIN_MEM0_S3` | `MAIN_MEM0_S4` | `MAIN_MEM0_S5` | `MAIN_MEM0_WAL` | `MAIN_MEM0_LME` | `MAIN_MEM0_LCM` | `MAIN_MEM0_AVG` |
| A-MEM | `MAIN_AMEM_S1` | `MAIN_AMEM_S2` | `MAIN_AMEM_S3` | `MAIN_AMEM_S4` | `MAIN_AMEM_S5` | `MAIN_AMEM_WAL` | `MAIN_AMEM_LME` | `MAIN_AMEM_LCM` | `MAIN_AMEM_AVG` |
| AWM | `MAIN_AWM_S1` | `MAIN_AWM_S2` | `MAIN_AWM_S3` | `MAIN_AWM_S4` | `MAIN_AWM_S5` | `MAIN_AWM_WAL` | `MAIN_AWM_LME` | `MAIN_AWM_LCM` | `MAIN_AWM_AVG` |
| ReasoningBank | `MAIN_RBANK_S1` | `MAIN_RBANK_S2` | `MAIN_RBANK_S3` | `MAIN_RBANK_S4` | `MAIN_RBANK_S5` | `MAIN_RBANK_WAL` | `MAIN_RBANK_LME` | `MAIN_RBANK_LCM` | `MAIN_RBANK_AVG` |
| SkeMex | `MAIN_SKEMEX_S1` | `MAIN_SKEMEX_S2` | `MAIN_SKEMEX_S3` | `MAIN_SKEMEX_S4` | `MAIN_SKEMEX_S5` | `MAIN_SKEMEX_WAL` | `MAIN_SKEMEX_LME` | `MAIN_SKEMEX_LCM` | `MAIN_SKEMEX_AVG` |
| Memory-R1 | `MAIN_MEMR1_S1` | `MAIN_MEMR1_S2` | `MAIN_MEMR1_S3` | `MAIN_MEMR1_S4` | `MAIN_MEMR1_S5` | `MAIN_MEMR1_WAL` | `MAIN_MEMR1_LME` | `MAIN_MEMR1_LCM` | `MAIN_MEMR1_AVG` |
| Mem-$\alpha$ | `MAIN_MEMALPHA_S1` | `MAIN_MEMALPHA_S2` | `MAIN_MEMALPHA_S3` | `MAIN_MEMALPHA_S4` | `MAIN_MEMALPHA_S5` | `MAIN_MEMALPHA_WAL` | `MAIN_MEMALPHA_LME` | `MAIN_MEMALPHA_LCM` | `MAIN_MEMALPHA_AVG` |
| MemRL | `MAIN_MEMRL_S1` | `MAIN_MEMRL_S2` | `MAIN_MEMRL_S3` | `MAIN_MEMRL_S4` | `MAIN_MEMRL_S5` | `MAIN_MEMRL_WAL` | `MAIN_MEMRL_LME` | `MAIN_MEMRL_LCM` | `MAIN_MEMRL_AVG` |
| Reflexion | `MAIN_REFLEXION_S1` | `MAIN_REFLEXION_S2` | `MAIN_REFLEXION_S3` | `MAIN_REFLEXION_S4` | `MAIN_REFLEXION_S5` | `MAIN_REFLEXION_WAL` | `MAIN_REFLEXION_LME` | `MAIN_REFLEXION_LCM` | `MAIN_REFLEXION_AVG` |
| ReasoningBank+MaTTS | `MAIN_RBANKMATTS_S1` | `MAIN_RBANKMATTS_S2` | `MAIN_RBANKMATTS_S3` | `MAIN_RBANKMATTS_S4` | `MAIN_RBANKMATTS_S5` | `MAIN_RBANKMATTS_WAL` | `MAIN_RBANKMATTS_LME` | `MAIN_RBANKMATTS_LCM` | `MAIN_RBANKMATTS_AVG` |
| **MERIT** | `MAIN_MERIT_S1` | `MAIN_MERIT_S2` | `MAIN_MERIT_S3` | `MAIN_MERIT_S4` | `MAIN_MERIT_S5` | `MAIN_MERIT_WAL` | `MAIN_MERIT_LME` | `MAIN_MERIT_LCM` | `MAIN_MERIT_AVG` |
| RIT-Full reference | `MAIN_RITFULL_S1` | `MAIN_RITFULL_S2` | `MAIN_RITFULL_S3` | `MAIN_RITFULL_S4` | `MAIN_RITFULL_S5` | `MAIN_RITFULL_WAL` | `MAIN_RITFULL_LME` | `MAIN_RITFULL_LCM` | `MAIN_RITFULL_AVG` |

### 表 2：奖励替换

| 管理器/奖励 | AVG | 相对原奖励变化 |
|---|---|---|
| Memory-R1 / original | `PLUGIN_MEMR1_ORIG_AVG` | — |
| Memory-R1 / $\widehat\phi$ | `PLUGIN_MEMR1_PHI_AVG` | `REWARD_SWAP_MEMORY_R1_GAIN` |
| Mem-$\alpha$ / original | `PLUGIN_MEMALPHA_ORIG_AVG` | — |
| Mem-$\alpha$ / $\widehat\phi$ | `PLUGIN_MEMALPHA_PHI_AVG` | `REWARD_SWAP_MEMALPHA_GAIN` |

### 表 3：消融

| 变体 | AVG | ΔAVG | SR@20% ($t=500$) | CCC | CTI |
|---|---|---|---|---|---|
| Full MERIT | `ABL_FULL_AVG` | 0 | `ABL_FULL_SR20` | `ABL_FULL_CCC` | `ABL_FULL_CTI` |
| A1：无重校准 | `ABL_A1_AVG` | `ABL_A1_DELTA` | `ABL_A1_SR20` | `ABL_A1_CCC` | `ABL_A1_CTI` |
| A2：匹配观察标签对照 | `ABL_A2_AVG` | `ABL_A2_DELTA` | `ABL_A2_SR20` | `ABL_A2_CCC` | `ABL_A2_CTI` |
| A3：无范围门控 | `ABL_A3_AVG` | `ABL_A3_DELTA` | `ABL_A3_SR20` | `ABL_A3_CCC` | `ABL_A3_CTI` |
| A4：无治理 | `ABL_A4_AVG` | `ABL_A4_DELTA` | `ABL_A4_SR20` | `ABL_A4_CCC` | `ABL_A4_CTI` |
| A5：无使用特征 | `ABL_A5_AVG` | `ABL_A5_DELTA` | `ABL_A5_SR20` | `ABL_A5_CCC` | `ABL_A5_CTI` |
| A-judge：LLM 自评 | `ABL_AJUDGE_AVG` | `ABL_AJUDGE_DELTA` | `ABL_AJUDGE_SR20` | `ABL_AJUDGE_CCC` | `ABL_AJUDGE_CTI` |
| A7：群体干预（探索） | `ABL_A7_AVG` | `ABL_A7_DELTA` | `ABL_A7_SR20` | `ABL_A7_CCC` | `ABL_A7_CTI` |

### 表 4：原子证伪门

| 门 | 估计量 | 比较对象 | 审计总体 | 判定规则（运行前锁定） | 失败动作 |
|---|---|---|---|---|---|
| G-C1 | SR@20% 随时间斜率；记忆级 CCC | 基线记忆库 | pilot audit | 斜率 CI 排除 0 且向上；CCC 上界低于 pilot bound | C1 收窄到异质任务流 |
| G-C2 | 事件/记忆 CCC、ACA-baseline 增益、ECE、成本 | 相关性基线 | sealed audit | 各项合取成立，具体阈值运行前锁定 | C2 不获支持 |
| G-C3a | Full 与 A4 的 SR 斜率差 | A4 无治理 | mechanism audit | Full 更平，差值 CI 排除 0（Holm） | 删除压平主张 |
| G-C3b | 有/无范围门控的 CTI | A3 无范围 | A/B mixed stream | CTI 降幅 CI 排除 0（Holm） | 删除干扰主张 |
| G-C3c | $\widehat\phi$ 奖励替换的 AVG 增益 | 原奖励 | reward-swap runs | 增益 lower-CI > 0（Holm） | 报告不可迁移 |
| G-C4 | 超过最强基线的 AVG 且低 token 开销 | max baseline | main runs | 两个条件合取成立 | 报告持平 |
| G-H3 | zero-shot transfer CCC（次要） | 域内 ACA | transfer runs | lower-CI 超过预注册门槛（FDR） | 报告不迁移 |
| G-H4 | budget–AVG 曲线 Pareto knee（次要） | budget sweep | efficiency runs | 满足边际增益规则 | 删除 Pareto 主张 |
| G-H5 | 增益随规模/异质性/冗余方向（次要） | 轴内比较 | boundary runs | 方向与 CI 规则通过；冗余仍为 Evidence Gap | H5 仅保留通过的轴 |

### 表 5：方法定位

| 方法 | 因果信号 | $O(1)$ 在线 | 重校准 | 范围 | 审计 |
|---|---|---|---|---|---|
| Data Shapley | `CITATION_DATA_SHAPLEY` | `CITATION_DATA_SHAPLEY` | `CITATION_DATA_SHAPLEY` | `CITATION_DATA_SHAPLEY` | `CITATION_DATA_SHAPLEY` |
| Influence Functions | `CITATION_INFLUENCE_FUNCTIONS` | `CITATION_INFLUENCE_FUNCTIONS` | `CITATION_INFLUENCE_FUNCTIONS` | `CITATION_INFLUENCE_FUNCTIONS` | `CITATION_INFLUENCE_FUNCTIONS` |
| TracIn | `CITATION_TRACIN` | `CITATION_TRACIN` | `CITATION_TRACIN` | `CITATION_TRACIN` | `CITATION_TRACIN` |
| ContextCite | `CITATION_CONTEXTCITE` | `CITATION_CONTEXTCITE` | `CITATION_CONTEXTCITE` | `CITATION_CONTEXTCITE` | `CITATION_CONTEXTCITE` |
| ReasoningBank | `CITATION_REASONINGBANK` | `CITATION_REASONINGBANK` | `CITATION_REASONINGBANK` | `CITATION_REASONINGBANK` | `CITATION_REASONINGBANK` |
| SkeMex | `CITATION_SKEMEX` | `CITATION_SKEMEX` | `CITATION_SKEMEX` | `CITATION_SKEMEX` | `CITATION_SKEMEX` |
| Memory-R1 | `CITATION_MEMORY_R1` | `CITATION_MEMORY_R1` | `CITATION_MEMORY_R1` | `CITATION_MEMORY_R1` | `CITATION_MEMORY_R1` |
| MemRL | `CITATION_MEMRL` | `CITATION_MEMRL` | `CITATION_MEMRL` | `CITATION_MEMRL` | `CITATION_MEMRL` |
| **MERIT** | 是 | 是 | 是 | 是 | 是 |

竞争方法单元格只有在逐项核验文献后才能填写；TBD 不能被解释为“不具备该能力”。

### 表 6：效率

| 配置 | 相对 token | AVG | ACA ms/event | 额外 VRAM | RIT 开销 |
|---|---|---|---|---|---|
| 共现基线 | $1\times$ | `EFF_BASELINE_AVG` | — | — | 0 |
| MERIT | `MERIT_RELATIVE_TOKEN_COST` | `EFF_MERIT_AVG` | `ACA_SCORING_LATENCY_MS` | `ACA_VRAM_OVERHEAD_GB` | `RIT_TOKEN_OVERHEAD_PERCENT` |
| A1（静态归因器） | `A1_RELATIVE_TOKEN_COST` | `EFF_A1_AVG` | `ACA_SCORING_LATENCY_MS` | `ACA_VRAM_OVERHEAD_GB` | `RIT_TOKEN_OVERHEAD_PERCENT` |
| RIT-Full reference | `RITFULL_RELATIVE_TOKEN_COST` | `EFF_RITFULL_AVG` | — | — | `FULL_RIT_COST_MULTIPLIER` |

---

## 附录 B：六幅计划图

1. **图 1：问题—方案总览。** 左侧展示相关性信用和含非正贡献记忆的 top-utility 集合；右侧展示
   `RIT → ACA → consumers`。数据验证前不画结果几何。
2. **图 2：基线诊断。** (a) 横轴为共现效用 $\widehat U$，纵轴为记忆级 RIT 审计估计
   $\widetilde\Phi$；(b) 横轴为任务索引，纵轴为 SR@20%。ReasoningBank 与 MemRL 对比。
3. **图 3：MERIT 架构。** 检索—执行—写入闭环，加上 RIT 标签、带重校准的 ACA、信用治理与范围门控。
   这是无数据示意图，可在实验完成前绘制。
4. **图 4：流式表现与效率。** 主图为任务索引—累计成功率；比较 MERIT、最强已核验基线和 RIT-Full。
   可选 inset 为 RIT 预算 $p$ 扫描，只能在数据核验后绘制。
5. **图 5：机制恢复。** (a) $\widehat\varphi$ 对 $\widetilde\varphi$；(b) SR@20% 随任务增长；
   与图 2 使用完全相同的统计定义和坐标轴。
6. **图 6：案例与 AS3 边界。** 时间线 A 对比有用记忆与迷信记忆的信用、范围和治理事件；时间线 B
   展示冗余/可替代记忆及探索性群体干预。数据来自未来核验后的事件日志。

## 当前状态速览

- 英文工作初稿已完成两轮独立评审与获批修订，可编译。
- 实验数据、真实图形和文献引用尚未回填。
- 仍需锁定的协议参数保留为 `USER_APPROVAL_REQUIRED`。
- 当前英文稿 11 页；AAAI-27 要求 7 页正文、总长最多 9 页且后两页只能是参考文献。按用户决定，
  暂不压缩，待实验、图表和引用完成后统一处理终稿篇幅。

