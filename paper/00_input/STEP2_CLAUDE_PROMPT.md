# 第 2 步 Claude 任务：生成 ARIS Narrative Report

你现在只执行 MERIT 论文工作流的第 2 步。不要启动 `/paper-writing`、`/paper-plan`、`/paper-figure` 或任何后续 ARIS 流水线。

## 唯一目标

基于指定输入，创建且只创建：

`E:\Project\MERIT-AAAI\paper\00_input\NARRATIVE_REPORT.md`

完成该文件后立即停止，不得生成 LaTeX、论文正文、图像、实验脚本、参考文献文件或其他新文件，也不得修改任何现有文件。

## 必须读取的输入

按顺序完整读取：

1. `E:\Project\MERIT-AAAI\paper\README.md`
2. `E:\Project\MERIT-AAAI\paper\00_input\SOURCE_MANIFEST.md`
3. `E:\Project\MERIT-AAAI\paper\00_input\source_proposal.md`
4. `E:\Project\ARIS\templates\NARRATIVE_REPORT_TEMPLATE.md`

`source_proposal.md` 是科学内容的唯一事实来源。ARIS 模板只提供组织形式，不能凌驾于方案内容之上。

## 输出定位

`NARRATIVE_REPORT.md` 是供后续 ARIS `/paper-plan` 使用的结构化英文叙事报告，不是正式论文正文。主体用英文撰写；源章节定位可以保留原方案中的中英文标题。

文件开头必须明确写明：

- Document status: `PRELIMINARY NARRATIVE WITH PLACEHOLDERS`
- Evidence status: experiments have not been executed or verified
- Target format: AAAI 2027 anonymous preliminary draft
- Authoritative source snapshot: `paper/00_input/source_proposal.md`
- Venue override: 当前写作任务使用 AAAI 2027；原方案中 NeurIPS/ICML 2027 主投、AAAI-28 备选的记录仅作为来源背景保留，不得让它覆盖当前任务

## 必须包含的章节

至少包含以下结构；可以在 ARIS 模板基础上扩展，但不得删除这些部分：

1. `Core Story`
2. `Problem and Key Observation`
3. `Contribution Type and Narrative Prototype`
4. `Claims and Evidence Status`
5. `Problem Formulation and Theoretical Commitments`
6. `Proposed Method: MERIT`
   - Randomized Interventional Trials (RIT)
   - Amortized Counterfactual Attribution (ACA)
   - Credit Governance
   - Scope-Gated Retrieval
   - Cost and Complexity Commitments
7. `Hypotheses-to-Experiments Mapping`
8. `Experiments`
   - Setup
   - Pilot / Diagnostic Study
   - Main Results Plan
   - Reward-Swap Plugin Study
   - Ablation Study
   - Mechanism and Calibration Analysis
   - Boundary and Scaling Analysis
   - Case Study
   - Efficiency Study
9. `Planned Tables`
10. `Planned Figures`
11. `Known Weaknesses, Assumptions, and Scope Boundaries`
12. `Related Work Map`
13. `Proposed Title`
14. `Target Venue`
15. `Source Traceability Map`

## Claim 规范

必须保留并编号核心贡献 `C1`–`C4`。每条 claim 至少包含：

- `Statement`
- `Status`: 只能是 `SUPPORTED-BY-DESIGN`, `PLANNED-EVIDENCE`, 或 `HYPOTHESIS`
- `Required evidence`
- `Planned paper location`
- `Source anchor`

不得把设计合理性写成实验证实，不得把预期机制写成已观察事实。对于尚未运行的 pilot、主实验、消融和效率实验，使用将来时或明确的 planned wording。

## 数值与占位符规则

1. `source_proposal.md` 中所有带 `◇` 的数值均为预期目标，不是结果。必须转换为唯一、语义化的占位符。
2. 示例表格中的性能数字，即使没有 `◇`，也不得作为真实结果保留。
3. 尚未测量的准确率、成功率、相关系数、显著性、标准差、开销、GPU 时间、token overhead、校准误差和比例等，全部使用：

   `[[TBD:<UNIQUE_SEMANTIC_ID>]]`

4. 占位符示例：

   - `[[TBD:PILOT_CCC_REASONINGBANK_T500]]`
   - `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]`
   - `[[TBD:PILOT_SR20_T500]]`
   - `[[TBD:ACA_HELDOUT_CCC_T500]]`
   - `[[TBD:TOKEN_OVERHEAD_PERCENT]]`

5. 固定的实验设计参数可以保留，例如任务数、采样概率、`K`、`top-k`、种子、治理阈值和算法超参数，但必须标为 `planned configuration` 或 `provisional hyperparameter`，不能暗示其已经验证为最优。
6. 不允许用 `X.XX`、随机小数、范围中点或“合理猜测”代替占位符。

## 表格要求

Narrative Report 中必须规划并构造 Markdown 表格骨架，至少覆盖：

- Main benchmark comparison
- Reward-swap plugin comparison
- Ablation matrix
- Hypotheses-to-experiments mapping
- Method comparison / related-work positioning
- Efficiency / cost comparison

所有未知实验数据单元格使用唯一 `[[TBD:...]]`。表头、方法行、指标列和 caption intent 必须完整，不能只写“以后做一个表”。

## 图片要求

不要生成任何图片。对 Fig. 1–Fig. 6 分别写出完整的文字规格，至少包括：

- figure purpose
- panel layout
- x/y axes or visual entities
- compared methods or stages
- intended takeaway
- future data source
- placeholders required
- source anchor

Fig. 2 与 Fig. 5 必须注明未来使用相同坐标范围以支持机制闭环比较。

## 理论与方法约束

- 保留反事实贡献、共现效用、Proposition 1、A1–A3 和优化目标的逻辑，但不得扩展出源方案没有的新定理或证明结论。
- 保留 MERIT 的线性依赖链 `RIT → ACA → consumers`，不得将方法改写成无关模块堆叠。
- 保留“RL 管理器和完整 Shapley 已被降级”的减法决策。
- 不得新增模型架构、数据集、baseline、评价指标或贡献点，除非明确标成 `OPEN QUESTION`，且不能进入 claim。

## 引用规则

- 不得编造 BibTeX、DOI、作者列表或论文结论。
- 只保留源方案已经点名的方法或论文族。
- 元数据未经核验时使用 `[[TBD:CITATION_<NAME>]]`，并写明 `requires bibliographic verification`。
- 不得声称某项工作“从未做过”而不加限定；使用适当的待核验措辞。

## 可追溯性要求

文件末尾必须包含 `Source Traceability Map`，把以下对象映射回 `source_proposal.md` 的具体章节：

- C1–C4
- Proposition 1 / A1–A3
- MERIT 各模块
- H1–H5 或源方案中对应的实验假设
- 每张计划表格
- Fig. 1–Fig. 6
- limitations 和 rebuttal-sensitive risks

如果源方案未显式提供某个细节，写 `NOT SPECIFIED IN SOURCE`，不得自行补全。

## 写入前自检

写入前逐项确认：

- 没有把任何 `◇` 数字当成真实结果；
- 没有把计划实验改写为已完成实验；
- 没有虚构引用；
- C1–C4 均存在且可追溯；
- 所有计划表格都已有完整骨架；
- Fig. 1–Fig. 6 均有文字规格；
- 唯一修改目标是 `paper/00_input/NARRATIVE_REPORT.md`。

## 完成后的聊天回复

完成文件后，只报告：

- 输出路径；
- 文件行数；
- claim 数量；
- planned experiment 数量；
- planned table 数量；
- planned figure 数量；
- `[[TBD:...]]` 唯一占位符数量；
- 是否修改了目标文件之外的任何文件。

然后停止，等待人工审查。
