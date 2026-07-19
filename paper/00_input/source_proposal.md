# 论文整体框架:MERIT — Retrieval Is Not Contribution

> ### Idea :反事实记忆归因——治疗"迷信记忆"\(Retrieval Is Not Contribution\)
>
> **一句话故事:** 现在所有系统给记忆记功的方式是**相关性**:任务成功 \+ 该记忆被检索 → utility\+1\(SkeMex 的效用估计、MemRL 的 Monte Carlo 更新都是这样\)。但检索≠被使用≠有用。这和 Skinner 鸽子实验里迷信行为的形成机制完全同构——**碰巧与成功共现的无关记忆被持续强化,系统里会长出一批"迷信记忆"\(cargo\-cult memories\)**。
>
> **诊断性发现:** 对跑了几百个任务后的 ReasoningBank/MemRL 记忆库做干预实验:随机摘除单条被检索的记忆重跑任务,估计其真实因果贡献,和系统记录的 utility 分数对比。预期结论:相关性很低,且高 utility 记忆中有相当比例是零贡献甚至负贡献,该比例随运行时长**上升**\(迷信在积累\)。这是全文的钩子。
>
> **具体机制:**
>
> - 反事实标签太贵,不能每条都重跑,所以做**摊销归因**:\(a\) 离线阶段用随机 leave\-one\-out rollout 收集小规模因果标签;\(b\) 用这些标签训练一个轻量 attribution model,输入是 query、记忆内容、生成轨迹中对该记忆的引用特征,输出贡献分;\(c\) 在线用 \(b\) 打分,周期性用 \(a\) 重新校准。推理时 O\(1\)。
>
> - 因果贡献分做两件事:一是替换 Memory\-R1 / MemRL 里的 outcome\-level 奖励,作为**去混淆的 per\-memory 奖励**训练写入/合并/淘汰策略;二是给每条记忆积累"帮过的 query"和"害过的 query"正负样本,学出**每条记忆自己的适用域表征**,检索时做 gate——这一步顺手解决了 Evo\-Memory 和 EEVEE 都观察到的跨任务干扰问题:药方没错,错在用给了不对的病人。
>
> **实验设计:** LoCoMo / LongMemEval\(对话侧\)\+ Evo\-Memory streaming \+ WebArena\(agentic 侧\)。核心指标除了终局性能,还有:迷信记忆占比随时间的曲线\(我们的方法应当压平它\)、归因分与 ground\-truth 因果分的相关性、跨任务干扰量。Baseline 直接对标 MemRL、Memory\-R1、Mem\-α、SkeMex。
>
> **为什么能中 / 风险:** "从相关到因果"是审稿人一听就懂的升维,金句现成\("retrieval is not contribution"\)。ICML/NeurIPS 气质最重。风险是归因估计的噪声,需要一节认真的校准分析——但这恰好让论文显得扎实而非取巧。

# 论文整体框架:MERIT — Retrieval Is Not Contribution

> **用法说明**:本框架按《论文框架模板 v3》从 §\-1 填至 §13 与附录,可直接交给 Claude Code / LLM 执行正文写作、实验代码与 LaTeX 生成。 **数字约定**:所有带 ◇ 标记的数字为**预期目标值\(占位\)**,须由真实实验回填;回填后若与 Headline 冲突,按 §13 迭代环先回改 Idea Card。 **目标会议**:主目标 NeurIPS 2027 / ICML 2027\(9 页,机制分析权重高\);备选 AAAI\-28\(按附 A 压缩方案裁剪\)。
> 
> 

---

## §\-1 叙事原型与贡献类型\(选型\)

**\(1\) 贡献类型:主 T1\(新方法\)\+ 辅 T2\(新洞察\)**

- 主 T1:提出 MERIT——用随机干预试验 \+ 摊销反事实归因,替换自进化记忆系统中的相关性记功信号。

- 辅 T2:揭示并量化"迷信记忆"\(superstitious memories\)现象——相关性记功导致零/负贡献记忆被系统性强化,且随运行时长累积。

- **为什么不选 T2 为主**:现象本身\(相关≠因果\)在因果推断领域是常识,单独作为发现体量不足;本文的分量在于给出了一套让反事实信号在在线、非平稳、闭环的记忆系统中**可负担、可消费**的完整机制,并证明换掉信号即可修复现象。方法是主菜,现象是最锋利的开胃菜。

**\(2\) 叙事原型:A 修复型\(唯一原型,全文贯穿\)**

- 故事骨架:自进化记忆系统随运行时长退化\(X 在 Y 场景下失败\)→ 根因是记功信号是相关性的,检索≠使用≠有贡献\(根因 Z\)→ 我们把记功从"观察性研究"升级为"随机对照试验",并将试验信号摊销到 O\(1\) 在线估计器\(针对 Z 设计\)。

- **为什么不选 E 现象型**:现象\(§4\)只占约 1\.5 页;资源重心在方法\(§6\)与消融/机制回收\(§8\.4/8\.5\),符合 A 型篇幅分配。全文不讲第二个故事——所有"跨任务干扰""RL 奖励替换"等内容一律作为"因果记功信号的两个消费者"叙述,不另起炉灶。

**原型对资源分配的约束\(执行者必须遵守\)**:方法 §6 与消融 §8\.4 是主战场\(合计约占正文 45%\);Pilot §4 控制在 1\~1\.5 页;理论\(Proposition 1\)只保留一条、证明进附录。

---

## §0 Idea Card\(单一事实源,全文与此对齐\)

**减法测试记录**:候选模块"用 φ̂ 训练 GRPO 记忆管理策略"被降级——删掉它、只用阈值规则消费 φ̂,Insight 依然成立且更锋利\("信号对了,简单规则就够"\);RL 版本降级为 §8\.3 的插件实验\(reward swap\)。候选模块"记忆间交互的完整 Shapley 采样"降级为 §8\.5 的 H5 边界讨论 \+ 附录变体。

---

## §1 Title\(标题\)

**主选\(模式 A\+B 复合,方法名\+冒号\+断言\)**:

> **MERIT: Retrieval Is Not Contribution — Counterfactual Credit Assignment for Self\-Evolving Agent Memory**
> 
> 

- 钩子词:断言 "Retrieval Is Not Contribution"\(可口头传播、可被引用为观点\);方法名 MERIT 可发音、与机制语义关联\(merit=功绩,对应记功;缩写展开 Randomized Interventional Trials 呼应 RCT 类比\)。

- 备选 1\(纯断言式,若审稿风向偏分析\):*Superstitious Memories: How Correlational Credit Corrupts Self\-Evolving Agents, and How to Fix It*

- 备选 2\(保守方法式\):*Counterfactual Memory Attribution for Self\-Evolving LLM Agents*

- 查重要求:执行者投稿前搜索 "MERIT \+ LLM/memory/agent" 确认不撞名;撞名则换 "CREDO / VERITY" 备用名并全局替换。

---

## §2 Abstract\(六句法,150–250 词,英文\)

> \(1背景\) Self\-evolving agents improve over time by distilling experience into a persistent memory bank, and the quality of this loop hinges on how credit is assigned to individual memories\. \(2Gap\) We show that the prevailing credit signal—co\-occurrence between retrieval and task success—systematically breeds *superstitious memories*: in ReasoningBank\- and MemRL\-style systems run over 500\-task streams, ◇38% of top\-utility memories have zero or negative causal effect on outcomes, and this fraction grows with deployment time\. \(3Insight\) **Our key observation is that retrieval is not contribution**: a memory's value is only defined counterfactually—by how much outcomes degrade when it is removed—yet no existing system measures this, because per\-memory interventions appear unaffordable\. \(4方法\) We introduce MERIT, which makes counterfactual credit affordable: randomized interventional trials \(paired leave\-one\-out rollouts\) on a small replayable budget provide causal labels; an amortized attributor trained on these labels scores every retrieval event at O\(1\) cost; and the resulting credit drives both memory governance \(evict/merge/quarantine\) and scope\-gated retrieval that learns *where* each memory applies\. \(5结果\) ◇Across five Evo\-Memory task streams, WebArena\-Lite, LongMemEval, and LoCoMo, MERIT outperforms the strongest baseline by \+5\.5 average points at \+2\.8% token overhead, flattens superstition accumulation \(38%→9%\), and, plugged into Memory\-R1 as a reward, lifts it by \+3\.1\. \(6意义\) Causal credit, not better heuristics, is the missing primitive of self\-evolution; we release the RIT auditing protocol as a community tool for diagnosing deployed memory banks\.
> 
> 

**兑现标注**\(写完正文后逐句核对\):句2→§4/Fig\.2;句3→§5 Prop\.1;句4→§6\.1–6\.3;句5→§8\.3/8\.5/8\.7;句6→§10\+开源声明。数字与正文逐位一致。

---

## §3 Introduction\(段落剧本\)

- **P1 背景\(2–3 句\)**:LLM agent 正从无状态走向经验驱动的自进化:ReasoningBank、Mem0、A\-MEM、SkeMex 等把交互轨迹蒸馏为持久记忆,MemRL、Memory\-R1、Mem\-α 进一步用学习信号管理记忆生命周期。整个范式的隐含前提:系统知道**哪条记忆值得记功**。

- **P2 失败模式\(命名化\)**:指出两个可引用的失败模式:\(i\) **Superstitious Memory\(迷信记忆\)**——与成功仅共现、无因果贡献的记忆被持续强化并占据检索位;\(ii\) **Cross\-Task Interference\(跨任务干扰\)**——在任务族 A 上真正有用的记忆被无差别检索到任务族 B 并造成伤害\(引 Evo\-Memory 与 EEVEE 的干扰观察\)。后果:记忆库越大、跑得越久,信噪比越低,长流末端性能不升反降\(预告 Fig\.2\)。

- **P3 归因与洞察\(★ 全文最关键段,建议逐句打磨\)**:前人为什么没解决?因为所有现有记功信号——ReasoningBank 的成功轨迹蒸馏、SkeMex 的环境反馈效用、MemRL 的 Monte Carlo 更新——本质都是**共现计数**,这是一项观察性研究:检索概率与 query 难度相关\(易题搭车\),高效用又反过来抬高检索概率\(马太效应\),形成 Skinner 鸽子式的迷信强化回路;我们在 Proposition 1 中证明该估计量即使样本无穷也不收敛到真实贡献。**Key Insight:retrieval is not contribution——记忆的价值只能由干预定义**;而干预看似不可负担,实则可摊销:少量随机对照试验足以训练一个 O\(1\) 的归因器。"Section 4 用一个干预式 pilot study 把这一归因变成证据。"

- **P4 方法概述**:MERIT 三个组件各一句:RIT 审计\(采因果标签\)→ ACA 摊销归因\(在线 O\(1\) 记功\)→ 双消费者\(信用治理 \+ 适用域门控\)。与 Figure 1 右侧一一对应;强调治理规则**刻意保持极简**,以证明增益来自信号而非管道。

- **P5 结果预告**:◇三个数字:\+5\.5 平均成功率\(Evo\-Memory 5 流\);SR@20% 38%→9%\(迷信被压平,Fig\.5 与 Fig\.2 同坐标\);Memory\-R1 奖励替换 \+3\.1\(信号可移植\)。

- **P6 贡献列表\(四向对齐锚点\)**: 

    - **C1\(揭示,T2\)**:We reveal and quantify *superstitious memories*:提出 RIT 审计协议与两个命名统计量\(CCC、SR@k\),首次以干预证据证明相关性记功在主流系统中随时间积累零/负贡献记忆\(§4, Fig\.2, Prop\.1\)。

    - **C2\(方法核心,T1\)**:We propose amortized counterfactual attribution\(ACA\):以轨迹使用行为特征为输入、RIT 标签为监督的 O\(1\) 归因器,配周期性再校准,使因果记功在闭环非平稳系统中可负担\(§6\.2, 消融 A1/A5, Fig\.5 校准图\)。

    - **C3\(方法,T1\)**:We show causal credit is directly consumable:极简阈值治理 \+ 每记忆适用域门控两个消费者,分别压平迷信积累与消除跨任务干扰;并可作为奖励插件泛化到 RL 式管理器\(§6\.3, 消融 A2/A3/A4, 表 2 插件行\)。

    - **C4\(实证\)**:◇跨 4 类基准、3 骨干、3 种子的系统评估:\+5\.5 平均提升、\+2\.8% 开销、机制统计量闭环回收\(§8\)。

---

## §3\.5 Figure Storyboard\(全文图表分镜\)

**Caption 要点\(写结论,不写描述;以下为成稿 caption 初稿\)**:

- Fig\.1: "Correlational credit turns memory banks into Skinner boxes: ◇38% of top\-utility memories have no causal effect \(left\)\. MERIT replaces co\-occurrence bookkeeping with randomized\-trial evidence and flattens superstition accumulation \(right\)\."

- Fig\.2: "System\-assigned utility barely tracks true counterfactual contribution \(Spearman ρ=◇0\.11, a\), and the superstition rate *grows* with deployment length \(◇12%→38%, b\): correlational credit does not self\-correct\."

- Fig\.4: "MERIT's advantage widens over the stream: most of the \+◇5\.5 average gain comes from the last 200 tasks, where baselines' banks are most polluted\."

- Fig\.5: "Amortized attribution recovers causal credit at O\(1\) cost \(ρ=◇0\.72 vs 0\.11 in Fig\.2a\) and eliminates the superstition growth observed in Fig\.2b \(−◇76% at t=500\)\."

**翻图测试**:Fig\.1\(问题\+方案\)→ Fig\.2\(证据\)→ Fig\.3\(方法\)→ Fig\.4\(有效\)→ Fig\.5\(为何有效\)→ Fig\.6\(直觉\),链条完整。配色语义:MERIT 恒用同一主色\(建议深青\),基线用灰阶;Fig\.2 与 Fig\.5 坐标轴范围强制一致。

---

## §4 Key Observation / Pilot Study — "Why Does Memory Credit Go Wrong?"

1. **Setup\(最小化干预实验\)**

- 系统:基于 EvolveLab 统一代码库复现 ReasoningBank 与 MemRL 两个代表\(一个启发式记功、一个 MC 学习记功\),骨干 Qwen3\-32B\(temperature 0\.7 采样执行、贪心评测\)。

- 环境:Evo\-Memory 协议下两条**可重放**任务流——ALFWorld\(具身文本\)与 HotpotQA\(多跳检索\),各 500 任务,3 种子。选可重放环境是因为干预需要在完全相同的初始状态下配对重跑。

- 干预协议\(即 C1 的 RIT,在此首次登场\):在 t∈\{100,200,300,400,500\} 冻结记忆库快照;对随后 50 个任务中的每个检索事件,抽样 300 个 \(query, 被检索记忆集\) 对;对其中每条记忆 m\_i 做**配对 leave\-one\-out**:完整上下文 vs 移除 m\_i,各 K=5 次固定种子 rollout;φ̂\_i\(q\) = 成功率之差。

- 预算说明\(防"pilot 造假"质疑\):共 ◇约 300×4×5×2 = 1\.2 万次 rollout/快照点,文本环境单次 rollout 约 2K token,总开销可控\(附 B 给成本表\)。

2. **Phenomenon\(命名统计量 ×2,配 Fig\.2\)**

- **CCC\(Credit–Contribution Correlation\)**:系统记功分与 RIT 真实贡献 φ 的 Spearman 相关。◇预期 ReasoningBank ρ=0\.11±0\.04,MemRL ρ=0\.19±0\.05——学习式记功也没好多少。

- **SR@k\(Superstition Rate\)**:效用分前 k% 的记忆中,φ≤0 的比例。◇预期 SR@20% 从 t=100 的 12% 升至 t=500 的 38%,单调上升——**迷信在积累,系统不会自我纠正**。

3. **Attribution\(锁定根因 \+ 排除两个替代解释\)**

- 根因机制:\(i\) **易题搭车**——检索由语义相关性决定,而语义相关的 query 往往本就更易\(记忆多来自同域成功任务\),成功被记到记忆头上;\(ii\) **马太效应**——效用分参与检索排序,高分→更常被检索→更多共现→分更高,正反馈把初始噪声放大成稳定迷信。两者合并为 Proposition 1\(共现效用估计量在检索\-难度相关条件下渐近有偏,且迷信均衡在效用贪心检索下稳定;证明附录 C\)。

- 排除替代解释 1\("φ 测量本身太噪"\):对同一批检索事件做 split\-half 重测,φ̂ 的分半相关 ◇ρ=0\.81——测量可靠,低 CCC 不是噪声假象。

- 排除替代解释 2\("记忆整体无用,归因无意义"\):整体移除 φ\>0 子集使成功率下降 ◇−9\.3 点——记忆确实有价值,坏的是**记功**而不是**记忆**。

4. **Design Implication\(桥接到方法\)**

- 记功必须是干预式的 → 但全量干预开销 ◇20–50×,不可在线负担 → **摊销**:RIT 只做小预算抽检\(C1\),训练 O\(1\) 归因器\(C2\);

- 因果分必须被消费才有意义 → 治理\(压平 SR\)\+ 适用域门控\(消除干扰\)\(C3\);

- 现象边界随手记录\(喂 H5/§10\):SR 上升幅度随任务流**异质性**与**库规模**增大;单域短流\(\<100 任务\)下 SR@20% 仅 ◇5% 且不增长——方法增益预期在该条件下消失。

---

## §5 Problem Formulation\(问题定义\)

**符号\(共 8 个,全部在 §6 使用\)**:任务流 \{\(q\_t, r\_t\)\},q\_t 为 query/任务,r\_t∈\[0,1\] 为结果信号;记忆库 M\_t=\{m\_i\};检索算子 R\(q\_t\)⊆M\_t\(top\-k\);agent 策略 π\(y\|q, R\(q\)\);归因器 g\_θ;每记忆运行信用 φ̄\_i;适用域表征 S\_i。

**Definition 1\(反事实贡献\)**:φ\_i\(q\) ≜ E\[r \| q, R\(q\)\] − E\[r \| q, R\(q\)∖\{m\_i\}\],期望对策略与环境随机性取。推广:φ 可视为对被检索集的单点干预效应;记忆间交互下的完整值为 Shapley 值,单点 LOO 为其一阶近似\(近似质量在 §8\.5 H5 实验刻画\)。

**Definition 2\(共现效用,基线信号\)**:Û\(m\_i\) = Σ\_t 1\[m\_i∈R\(q\_t\)\]·r\_t / Σ\_t 1\[m\_i∈R\(q\_t\)\]。

**Proposition 1\(非正式陈述,正式版与证明见附录 C\)**:若检索事件与 query 基线可解性相关\(Cov≠0\),则 Û 是 φ 的渐近有偏估计;且在效用参与检索排序的正反馈下,存在稳定的迷信均衡\(Û 高而 φ=0\)。现实对应:语义检索天然满足该相关条件\(§4 归因 i\)。

**Assumptions\(单独编号,rebuttal 用\)**:

- **A1\(结果可观测\)**:每任务有可用的 r\_t\(环境成功信号或经一致性抽检的 LLM\-judge 分\)。

- **A2\(局部可重放\)**:存在任务子集可固定初始状态重放\(docker 快照/文本环境天然满足\);**仅 RIT 标签采集需要 A2**,ACA 在线打分不需要。

- **A3\(低阶交互\)**:被检索集内记忆交互效应有界,LOO 近似 Shapley 的误差可控;A3 被违反的情形\(冗余记忆对\)在 §8\.5/Fig\.6 主动展示并给出组消融兜底。

**优化对象**:学习 g\_θ 最小化 RIT 标签上的回归损失 E\[\(g\_θ\(x\_i\(q\)\) − φ̂\_i\(q\)\)²\];系统目标为最大化流式累计成功 Σr\_t,受 token 预算约束\(检索 \+ RIT 抽检 ≤ 基线的 1\+ε,ε=◇3%\)。

---

## §6 Proposed Approach:MERIT

**6\.0 Overview\(配 Fig\.3\)** 一段话:MERIT 在标准"检索–执行–写入"记忆回路上加三件事:\(C1\) 低预算 RIT 抽检持续产出因果标签;\(C2\) ACA 归因器把标签摊销为每次检索事件的 O\(1\) 贡献分,并周期性用新标签再校准以适应闭环分布漂移;\(C3\) 贡献分被两个极简消费者使用——阈值治理更新记忆去留,适用域门控修正检索排序。模块间是严格的上下游依赖\(C1 产标签 → C2 产信号 → C3 消费信号\),无并列 trick。

**6\.1 RIT:Randomized Interventional Trials\(→C1\)**

- **Why**:共现效用有偏\(Prop\.1\);naive 替代"让 LLM 自评这条记忆有没有用"复现自我确认陷阱\(EDV, 2026\),作为消融变体 A\-judge 在 §8\.4 对照。

- **How**:以概率 p=◇5% 抽取任务进入试验组;对其检索集内每条记忆做配对 LOO\(K=5 固定种子 rollout\);为控制位置混淆,移除记忆后**保持其余上下文顺序与填充占位**;输出 \(q, m\_i, 轨迹, φ̂\_i\) 四元组入标签池。抽检只在满足 A2 的任务上执行。

- **Link**:对应 C1;审计协议独立可用\(社区工具,呼应 Who cares\)。

**6\.2 ACA:Amortized Counterfactual Attribution\(→C2,the core of our approach\)**

- **Why**:全量 RIT 开销 ◇20–50×;摊销把因果记功压到 O\(1\)。Intuitively, ACA 学的是"什么样的记忆在什么样的 query 上、以什么样的**被使用方式**产生真实贡献"——第三类特征是关键:它让模型区分"被检索但被无视"与"被实际执行"。

- **How**:输入特征 x\_i\(q\) 三组——query 表征、记忆表征\(Qwen3\-Embedding\-4B\)、**使用行为特征**\(记忆内容与输出的 n\-gram/编辑重合度、模型显式引用标记、上下文位置与检索排名、记忆 token 上的对数似然增益\);头部为 2 层 MLP 回归 φ̂∈\[−1,1\]。训练:标签池上 Huber 损失;**周期再校准**:每 100 任务用最新标签微调 \+ 保序回归校准\(闭环下检索分布被 C3 改变,防归因器漂移\)。在线推理:每次检索事件对 top\-k 条各打一分,更新运行信用 φ̄\_i\(指数滑动平均\)与正负 query 样本集。

- **Link**:对应 C2/H2;校准质量在 Fig\.5a 与 §8\.5 可靠性图回收。

**6\.3 双消费者:信用治理 \+ 适用域门控\(→C3\)**

- **Why**:信号不被消费就只是审计;治理压平迷信积累\(SR\),门控解决"药方没错、病人不对"的跨任务干扰\(CTI\)。刻意用**阈值规则而非 RL**,证明增益来自信号\(消融 A2:同规则换回共现效用,增益应消失\)。

- **How\(治理,3 条规则\)**:淘汰——φ̄\_i\<−0\.02 且样本数 n\_i≥8;合并——嵌入相似度\>0\.9 且双方 φ̄\>0 时由 LLM 摘要合并\(信用取加权\);隔离——新记忆进入 quarantine,前 n\_min=3 次检索带探索加成\(UCB 式,防"新记忆永远没机会积累信用"的冷启动死亡\)且不参与排序加成。

- **How\(门控\)**:每条记忆维护正负 query 原型\(φ̂\>τ⁺ 的 query 嵌入均值 / φ̂\<τ⁻ 的均值\);检索分 = α·语义相关 \+ β·\(sim\(q,proto⁺\)−sim\(q,proto⁻\)\) \+ γ·φ̄\_i,默认 α,β,γ=1\.0,0\.5,0\.3\(敏感性见 §8\.5\)。

- **Link**:对应 C3/H1/H3;插件性\(把 φ̂ 作为 per\-operation 奖励替换 Memory\-R1 的 outcome 奖励,GRPO 训练设置不变\)在表 2 单列。

**6\.4 减法与开销**

- 模块依赖检查:C1→C2→C3 线性依赖链,已通过;被减掉的模块见 §0 减法测试记录。

- 开销声明\(正文一句话,附录全表\):ACA 打分 ◇\<1ms/事件\(4B 编码器批处理\);RIT 抽检摊到全流为 ◇\+2\.6% token;门控与治理零额外 LLM 调用;合计 ◇\+2\.8% token、\+0\.4 GB 显存\(归因器常驻\)。

- 设计选择表\(附录 D,行示例\):`LOO 而非全 Shapley | 采样 Shapley | 开销 5× vs 1×,A3 下误差<0.05 | 消融 A7`;`使用行为特征 | 仅 (q,m) 语义特征 | 区分"检索而未用" | 消融 A5`;`保序回归再校准 | 不校准 | 闭环分布漂移 | 敏感性 S3`。任何一行两列全空 → 删设计。

**Algorithm 1\(主循环伪代码,进正文\)**:

```Plain Text
Input: stream {q_t}, bank M, retriever R, policy π, attributor g_θ, budget p
for t = 1,2,...:
    C ← R(q_t)  # scope-gated: α·rel + β·scope + γ·credit, quarantine 探索加成
    y_t, traj ← π(q_t, C);  r_t ← env/judge(y_t)
    for m_i in C:  φ̂_i ← g_θ(x_i(q_t, traj));  update φ̄_i, proto±_i
    if replayable(q_t) and rand() < p:            # RIT 抽检
        for m_i in C: label ← paired_LOO(q_t, C, m_i, K=5); pool.add(label)
    governance(M): evict / merge / quarantine by rules(φ̄, n)
    if t % 100 == 0: recalibrate g_θ on pool (Huber + isotonic)
```

---

## §7 Hypotheses → Experiments Mapping\(对齐表\)

CTI 定义\(正文给出\):CTI = Acc\_B\(仅 B 域记忆库\) − Acc\_B\(A∪B 混合库\),≥0 表示存在干扰;沿 Evo\-Memory 的混流协议构造 A/B 域对。

---

## §8 Experiments

### 8\.1 Setup

**Benchmarks\(4 类,各配选择理由\)**:

**Implementation**:代码基 EvolveLab\(统一记忆系统实现,保证基线公平\);骨干 **Qwen3\-32B**\(主\)、**Qwen3\-235B\-A22B**\(规模趋势点\)、**GPT\-5\.1**\(闭源泛化点,仅主表附加行\);ACA = Qwen3\-Embedding\-4B 冻结编码 \+ 2 层 MLP\(可训练参数 ◇2\.1M\)。硬件 8×A100\-80G;单主实验\(1 骨干×1 基准×3 种子\)◇约 180 GPU·h \+ API 成本表进附录。

**公平性声明**:所有方法同骨干、同检索器\(bge\-m3 或 Qwen3\-Embedding,统一\)、同 top\-k=4、同 token 预算\(基线不做 RIT,则给其等额预算用于其自身机制或空烧,两种记法都报\);种子 \{13,42,2026\},报 mean±std;主对比做配对 bootstrap 显著性\(10⁴ 重采样,报 p 值\),流式曲线报逐点置信带。

**评测者偏差**:HotpotQA/LoCoMo 部分子任务用 LLM\-as\-judge\(GPT\-5\.1,与被测骨干 Qwen3 **不同源**\);judge prompt 进附录;抽 200 例人工核对一致性\(报 Cohen's κ,目标 ≥0\.8\)。

### 8\.2 Baselines\(谱系制,标年份\+核心思路\+复现方式\)

1. **Vanilla**:No\-Memory ReAct\(2023,下界\);Full\-History Stuffing\(全历史塞上下文,证明"记忆结构"本身必要\);Mem0\(2025,启发式增删改\);A\-MEM\(2025,Zettelkasten 链接演化\)。

2. **同方向结构化记功**:AWM\(2024,workflow 蒸馏\);ReasoningBank\(2025,成功/失败策略蒸馏\+启发式效用\);SkeMex\(2026,环境反馈效用\+价值感知治理\)——证明"更好的启发式效用"不够。

3. **当前 SOTA\(学习式记功\)**:Memory\-R1\(2025,GRPO 训练增删改策略、outcome 奖励\);Mem\-α\(2025,RL 记忆构建\);MemRL\(2026,MC 值更新检索\)。

4. **正交方向**:Reflexion\(2023,无持久库的测试时反思\);ReasoningBank\+MaTTS\(2025,记忆感知测试时扩展\)——证明优势不来自测试时计算。

5. **上界参考**:RIT\-Full\(全量干预记功,不摊销\)——报告其成绩与 ◇20–50× 开销,MERIT 目标达到其 ≥90% 增益。 复现声明:1/2/4 类基于 EvolveLab 统一复现\(对齐检索器与预算\);3 类优先用官方代码,主表脚注标注"复现/引用"。

### 8\.3 Main Results

**表 1\(主表\)结构**:行 = 方法\(按谱系 1→5 排序,MERIT 倒数第二,RIT\-Full 上界最后一行灰色\);列 = 5 条 Evo\-Memory 流\(按异质性递增排序:单域 ALFWorld → 混流\)→ WebArena\-Lite → LongMemEval → LoCoMo → **AVG**;单元格 mean±std,最优加粗、次优下划线。列按难度递增排,让"混流上差距最大"的叙事直接可见。 示例行\(◇占位\): `MemRL (2026) | 61.3±1.2 | ... | 42.0±1.8 | 31.2±2.1 | 62.4±0.9 | 58.1±1.1 | 48.7MERIT (ours) | 62.1±1.0 | ... | 49.5±1.4 | 35.0±1.7 | 66.1±0.8 | 61.9±1.0 | 54.2` 表后 3 句结论\(初稿\):"\(i\) 增益随流异质性单调放大\(单域 \+0\.8 → 混流 \+7\.5\),与干扰机制预测一致;\(ii\) 学习式记功基线\(3 类\)并不稳定优于启发式\(2 类\)——学错了信号,学习本身不解决问题;\(iii\) MERIT 达到 RIT\-Full 上界 ◇93% 的增益,开销仅其 1/18。"

**表 2\(插件实验\)**:Memory\-R1 / Mem\-α 原奖励 vs 换 φ̂ 奖励,各 \+◇3\.1 / \+◇2\.4——证明修的是信号,不是管道\(直接回应 Delta 行\)。

**Fig\.4**:流式累计成功率曲线\(见 §3\.5\)。

### 8\.4 Ablation Study\(逐贡献移除 \+ 替代方案对照\)

### 8\.5 Analysis\(机制闭环,oral 主战场\)

- **机制回收\(H2\)**:Fig\.5 与 Fig\.2 同统计量同坐标:\(a\) CCC 从 0\.11 → ACA 的 ◇0\.72;\(b\) SR@20% 曲线基线上扬至 38%、MERIT 压平至 ◇9%\(−76%\)。一句话结论进 caption。

- **校准分析\(回应最大风险"归因噪声"\)**:held\-out RIT 上可靠性图 \+ ECE\(◇≤0\.06\);分域校准;φ̂ 的分半重测一致性;失败模式:φ 接近 0 的记忆上符号判断最不稳\(承认并连接治理阈值设计——阈值刻意留死区 ±0\.02\)。

- **敏感性**:K∈\{1,3,5,10\}、RIT 预算 p∈\{1,2,5,10\}%、\(α,β,γ\) 网格、top\-k∈\{2,4,8\}——展示 p=5% 即饱和\(H4 弹药\)。

- **Scaling/迁移趋势**:骨干 32B→235B 增益保持\(◇\+5\.5→\+4\.8,基线变强但迷信机制不变\);ACA 在 ALFWorld\+HotpotQA 训练、WebArena 零样本迁移 ρ=◇0\.58\(H3\)。

- **边界刻画\(H5\)**:三条趋势线——增益 vs 库规模\(\<100 条时 ≤1 点\)、vs 流异质性\(单域≈0\)、vs 人工注入冗余记忆比例\(LOO 低估随冗余上升,A7 变体缓解\);解释均与机理预测一致。

- **错误分析**:MERIT 仍失败的样本分类\(◇约 40% 为记忆库根本没有相关经验——记功再准也无米下锅;喂 §10\)。

### 8\.6 Case Study\(成功例\+失败例,配 Fig\.6\)

成功例:HotpotQA 流中一条"先搜实体别名再搜关系"的记忆 vs 一条迷信记忆"检索结果为空时重复原查询一次"——展示后者效用分虚高的积累过程、RIT 判零、第 ◇217 个任务被淘汰,前者信用与适用域\(仅多跳类 query\)被正确刻画。失败例:两条各含一半流程的互补记忆,单独 LOO 均≈0,治理几乎双杀;组消融兜底规则\(相似度聚类后整组干预\)挽回——诚实展示 A3 边界。

### 8\.7 Efficiency\(H4\)

Pareto 图:x=相对 token 开销\(对数轴\),y=AVG 成功率;点:共现基线\(1×\)、MERIT\(◇1\.028×\)、A1\(1\.026×\)、RIT\-Full\(◇18×\)。结论:MERIT 位于 Pareto 前沿拐点。附标签预算\-性能曲线\(p 扫描\)。

---

## §9 Related Work\(三子域,对应三条贡献\)

1. **自进化记忆与经验蒸馏**\(对应 C1\):Mem0 / A\-MEM / AWM / ReasoningBank / SkeMex / MemEvolve——记功一律为启发式或共现效用;"但没有工作以干预证据审计过这些信号的因果有效性,这正是 C1。"

2. **学习式记忆管理**\(对应 C3\):Memory\-R1 / Mem\-α / MemRL / MemSkill——学习的是策略,信号仍是 outcome 级或 MC 共现;EDV\(2026\)用多智能体共识修**写入时判断**,与本文修**全生命周期信用**正交且可叠加。"前人优化了消费信号的方式,没有修信号本身。"

3. **数据估值与上下文归因**\(对应 C2\):Data Shapley\(2019\)/ Influence Functions / TracIn\(2020\)面向**训练数据、静态、离线**;ContextCite\(2024\)与 RAG 归因面向**单次生成的解释**;"没有工作处理在线、非平稳、且归因结果反过来改变数据分布的闭环设定——这要求摊销\+再校准\(C2\)。"

- **对比表\(加分项\)**:行=代表方法,列=\[因果信号 \| O\(1\) 在线 \| 闭环再校准 \| 适用域 \| 审计协议\],MERIT 全勾。

- **范围声明**:"We focus on credit assignment for extant memories and leave what\-to\-write policies \(write\-time quality\) out of scope; MERIT composes with them\."

- **并发工作**:投稿前 2 周扫 arXiv;预留句式:"Concurrent work \[X\] explores \.\.\., differing from ours in that their signal remains observational / their attribution is not closed\-loop\."

---

## §10 Limitations, Broader Impact \& Conclusion

**Limitations\(三条,各配 forward\-looking\)**:

1. RIT 依赖局部可重放\(A2\):完全不可重放的物理/单次环境无法采标签;未来方向——用世界模型模拟重放或离轨估计\(off\-policy evaluation\)替代真实干预。

2. LOO 在高冗余记忆库下低估信用\(A3,§8\.5/Fig\.6 已量化\):组干预兜底有额外开销;未来——结构感知的交互归因。

3. 增益边界\(引 H5\):单域短流、小库场景收益趋零——MERIT 是长期部署的药,不是短会话的药;错误分析显示 ◇40% 剩余失败源于经验缺失而非记功错误,与"写什么"方向\(ReasoningBank 一族\)互补。 **Broader Impact**:因果审计提升自进化系统可解释性与可治理性;风险——归因分若被外部内容操纵可成为新攻击面\(记忆投毒的信用洗白\),提示与安全方向组合。 **Conclusion**:3 句复述 Idea Card\(Problem→Insight→Headline\),不引入新信息。

---

## §11 For Rebuttal\(反驳预案\)

**攻击点预案**:

1. **"RIT/干预开销不现实"** → Defense:设计层面——干预只在 ◇5% 可重放任务抽检,摊销后 \+2\.8% token\(§6\.4\);实验层面——§8\.7 Pareto 与预算扫描显示 p=5% 已饱和、达到全量干预 93% 增益。

2. **"归因有噪,φ̂ 不可信"** → Defense:设计——治理阈值留死区、门控用相对分;实验——§8\.5 校准小节\(ECE≤0\.06、分半重测 0\.81、Fig\.5a ρ=0\.72\),且 §4 已排除"噪声假象"替代解释。

3. **"这不就是 Data Shapley/ContextCite 搬到记忆上"** → Defense:机制差异三点\(在线非平稳、闭环反馈改变分布故需再校准、使用行为特征针对'检索≠使用'\)见 §9 子域 3 与消融 A5;数字之外的差异见表 2 插件实验。

4. **"与 MemRL/Memory\-R1 相比增量不足"** → Defense:核心消融 A2——同管道换信号增益消失,证明贡献在信号层;表 2——我们的信号让他们的管道也涨 \+3\.1,这是互补而非增量。

5. **"只在文本可重放环境成立"** → Defense:Assumption A2 已声明边界且 H5 主动刻画;WebArena\-Lite\(真实网页\)与 ACA 跨环境零样本迁移\(ρ=0\.58\)证明归因器可脱离标签环境使用。 **Rebuttal 专用实验\(预跑或三天内可跑\)**:\(i\) 第 6 条 Evo\-Memory 流\(留一条不进正文\);\(ii\) Llama\-4\-Maverick 第三骨干点;\(iii\) judge 换 Claude Sonnet 4\.6 的一致性复核。

---

## §12 Self\-Check Checklist\(终检,当前状态\)

* [x] 原型一致性:全文只讲 A 修复型;干扰/插件均纳入"信号的消费者"主线,未换故事

* [x] 一句话测试:"Retrieval is not contribution;记忆的价值只能由干预定义,而干预可以摊销到 O\(1\)"

* [x] 减法测试:RL 管理器、全量 Shapley 已降级\(§0 记录\);正文无删掉不伤 Insight 的模块

* [x] 四向对齐:C1→§6\.1→\(§4 即其应用\)→Fig\.2;C2→§6\.2→A1/A5→Fig\.5a;C3→§6\.3→A2/A3/A4→表1/CTI;C4→§8

* [x] 假设闭环:H1–H5 各有指标/实验/贡献\(§7 表\);无孤儿实验

* [x] 统计量回收:CCC 与 SR@k 在 §4 定义、§8\.5 同坐标回收

* [x] 翻图测试:Fig\.1–6 链条完整,caption 均为结论式

* [x] 边界刻画:H5 三条趋势线,§10 引用之

* [ ] 摘要兑现:待真实数字回填后逐句核对\(执行者任务\)

* [ ] 公平性:多种子/显著性/预算对齐已设计,待执行

* [ ] 复现性:Algorithm 1 已有;超参表/开销表/prompt 见附 B,待随代码发布

* [x] 符号体检:8 个符号全部在 §6 使用

* [ ] 并发工作扫描:投稿前 2 周执行\(§9 已留句式\)

* [x] Reviewer 2 测试:5 个攻击点均有设计\+实验双层防御

---

## §13 写作顺序与迭代流程\(建议 10 周生产线\)

1. **W1**:填卡完成\(本框架即卡\)→ 搭 EvolveLab 环境,复现 ReasoningBank/MemRL 于 2 条流。

2. **W2–3**:跑通 §4 Pilot\(RIT 协议 \+ CCC/SR 统计\)。**Gate:若 CCC\>0\.5 或 SR 不随时间上升,归因被证伪 → 回改 Idea Card\(候选转向:迷信只在异质流出现 → 收窄 claim\),不硬写。**

3. **W3**:画空主表\(表 1/2\)与 §7 对齐表,锁定要填的格子;画 Fig\.1/3 草图。

4. **W4–6**:实现 ACA \+ 治理/门控;先在 2 条流上打通 H2\(Fig\.5a 的 ρ≥0\.6 是第二道 Gate\),再铺全部基准与基线。

5. **W6–8**:消融 A1–A7、敏感性、H5 边界、插件表 2;边跑边填 §8。

6. **W8–9**:写 Method/Experiments 正文 → Intro → Abstract → Title;图表精修\(Fig\.2/5 同坐标\)。

7. **W9–10**:Rebuttal 专用实验预跑;终检清单;并发工作扫描;内部红队评审\(找一人扮演 Reviewer 2 攻击 §11 五点\)。 迭代环提醒:任何数字撑不起 Headline\(如 AVG 增益 \<3 点\)→ 先改卡\(降 Headline、强化机制故事把重心移向 C1/C2\),再改文。

---

## 附 A 会议差异与投稿选择

## 附 B 可执行资产清单\(交给 Claude Code 的任务分解\)

1. **代码资产**:fork EvolveLab;新增 `merit/{rit.py, aca.py, governance.py, gate.py}`;RIT 需要环境快照接口\(ALFWorld/ScienceWorld 原生支持,WebArena 用 docker commit\)。

2. **超参与运行设置示例\(附录表初稿\)**:骨干 Qwen3\-32B\(执行 temp=0\.7, top\-p=0\.95;评测 greedy\);检索 top\-k=4;RIT p=5%, K=5;ACA lr=1e\-4, batch=256, Huber δ=0\.1, 每 100 任务再校准;治理阈值 −0\.02/n≥8;quarantine n\_min=3, UCB c=0\.5;\(α,β,γ\)=\(1\.0,0\.5,0\.3\);种子 \{13,42,2026\}。

3. **成本估算表**:Pilot ◇1\.2 万 rollout×4 快照×2 系统 ≈ 2×10⁸ token;主实验 ◇180 GPU·h/骨干/基准;总预算表按 8×A100 折算。

4. **Prompt 资产**:记忆蒸馏 prompt\(沿基线原文\)、LLM\-judge prompt、合并摘要 prompt——全部进附录并随代码发布。

5. **补充材料计划**:附录 C\(Prop\.1 证明\)、附录 D\(设计选择表\)、附录 E\(全部超参/开销/judge 一致性\)、代码与 RIT 审计工具开源\(Apache\-2\.0\)。

6. **图表生产**:Fig\.2/5 用同一绘图脚本参数化\(锁坐标\);主色 \#0F766E;字号 ≥ 正文。

