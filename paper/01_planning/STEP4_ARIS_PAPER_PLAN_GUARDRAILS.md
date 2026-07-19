# 第 4 步：ARIS `/paper-plan` 执行约束

> 本文件是 `/paper-plan` 的项目级覆盖约束。若 ARIS skill 的默认行为与本文件冲突，以本文件和 `DRAFT_POLICY.md` 为准。

## 1. 任务目标

根据英文权威叙事报告，为 **AAAI 2027 匿名初稿**生成一份可执行、逐章节、证据受约束的论文计划。

本轮只做 paper planning：

- 构建 Claims–Evidence Matrix；
- 确定论文类型与章节结构；
- 为每节规划论证目标、证据、表格、图示、引用槽位和篇幅比例；
- 规划 C1–C4、H1–H5、Table 1–6、Fig. 1–6 的落点；
- 通过 Codex MCP 调用 `gpt-5.6-sol`、`xhigh` 进行独立 outline review；
- 整合 reviewer feedback 后输出最终计划；
- 输出后立即停止。

禁止启动 `/paper-write`、`/paper-writing`、`/paper-figure`、`/paper-compile`、实验执行或文献搜索。

## 2. 必须读取的文件

按以下顺序读取：

1. `E:\Project\MERIT-AAAI\paper\01_planning\DRAFT_POLICY.md`
2. `E:\Project\MERIT-AAAI\paper\00_input\NARRATIVE_REPORT.md`
3. `E:\Project\MERIT-AAAI\paper\01_planning\PLACEHOLDER_LEDGER.md`
4. `E:\Project\MERIT-AAAI\paper\00_input\SOURCE_MANIFEST.md`
5. `E:\Project\MERIT-AAAI\.agents\docs\AAAI-AuthorKit27\CameraReady2027.tex`
6. ARIS `paper-plan` skill 要求的 writing principles 与 venue checklist。

可以按需只读参考：

- `paper/00_input/source_proposal.md`，用于解决英文叙事报告没有覆盖的来源定位；
- `paper/00_input/NARRATIVE_REPORT.zh-CN.md`，仅供语言理解，不得作为权威输入。

## 3. 唯一允许写入的文件

只允许创建：

`E:\Project\MERIT-AAAI\paper\01_planning\PAPER_PLAN.md`

不得在项目根目录写 `PAPER_PLAN.md`，不得创建 `MANIFEST.md`、`CLAUDE.md`、`findings.md`、时间戳副本、review-stage、idea-stage、LaTeX、BibTeX、图片或其他文件。

这是该路径的第一次生成，不需要 timestamped copy。若目标文件意外已存在，停止并报告，不得覆盖。

## 4. 投稿场所与篇幅约束

- Venue：**AAAI 2027**。
- 当前具体 track 和页数限制尚未核验，必须保留为：`[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`。
- 不得采用 ARIS skill 中内置的 “AAAI = 7 pages” 作为已确认事实。
- 不得沿用源方案的 9 页安排。
- 在页数未确认前，使用**正文篇幅比例**规划，例如 Introduction、Method、Experiments 各占正文的百分比；可以同时给出条件式页数公式，但不得给出未经核验的总页数。
- Author Kit 中的格式规则可以采用；具体 event page limit 必须等待官方 call 核验。

## 5. 证据纪律

- C1–C4 的总体状态均保持 `PLANNED-EVIDENCE`。
- Proposition 1 保持 `HYPOTHESIS` / pending formal proof。
- 未运行的 pilot、主实验、消融、效率、扩展和案例分析不得写成已观察结果。
- 不得出现无条件的 “we show”“we demonstrate”“outperforms”“significantly”“proves”。
- 计划中的结果预览必须写成：需要由哪个表/图/指标检验，以及不支持假设时如何修改主张。
- 不得把设计参数、源方案示例数字或门槛当作结果。
- 不得生成任何真实实验数字。

## 6. 占位符规则

- 只允许使用 `PLACEHOLDER_LEDGER.md` 已登记的 234 个 ID。
- 不得创建新 `[[TBD:...]]` ID，不得修改现有 ID。
- 需要表达账本未覆盖的缺口时，使用普通文本 `NOT SPECIFIED IN SOURCE` 或 `EVIDENCE GAP`，不要自行新增占位符。
- 同一指标在 section plan、table plan、figure plan 中必须复用相同 ID。
- 计划必须注明：占位符只有在账本状态达到 `VERIFIED` 后才能替换。

## 7. 方法与故事边界

- 论文类型：primary **T1 method paper** + auxiliary **T2 diagnostic insight**。
- 唯一方法链：`RIT → ACA → consumers`。
- Pilot 是开篇诊断证据，不是第二篇论文。
- Credit Governance 与 Scope-Gated Retrieval 是因果信用的两个消费者，不得变成独立故事。
- RL manager 只作为 reward-swap plugin study。
- Full Shapley 只作为 H5 boundary / appendix variant。
- 不得新增模型、模块、数据集、baseline、指标、理论结果或贡献。
- 保留“Method + Ablation 是主要篇幅战场；Pilot 受控”的源方案减法决策。

## 8. 必须包含的计划结构

最终 `PAPER_PLAN.md` 至少包含：

1. Working Title；
2. One-sentence Contribution；
3. Venue、Paper Type、Evidence State、Conditional Page Budget；
4. Claims–Evidence Matrix：C1–C4；
5. Hypotheses–Evidence Map：H1–H5；
6. Section Architecture：5–8 个正文 section，包含 Abstract、Introduction、Related Work、Problem/Formulation、Method、Experiments/Analysis、Limitations/Conclusion 的合理合并或拆分；
7. 每节的目标、段落级逻辑、依赖的 claim、证据状态、表/图、引用槽位、预计正文比例和可移入附录的内容；
8. Table Plan：Table 1–6 全部列出，不能删减；
9. Figure Plan：Fig. 1–6 全部列出，不能删减；Fig. 2 与 Fig. 5 必须使用相同坐标范围和统计口径；
10. Citation Plan：只使用已有 `[[TBD:CITATION_...]]`，全部标为待核验；
11. Appendix Plan：正式证明、完整成本、额外敏感性、A7/group-Shapley 等；
12. Evidence Gaps and Falsification Gates；
13. Reviewer Feedback：保留 Codex review 的评分、关键问题与最小修复；
14. Review Integration Log：逐条说明采纳、部分采纳或拒绝 reviewer 建议的原因；
15. Acceptance Checklist；
16. Next Step 建议，但不得执行。

## 9. 表格与图示约束

- Table 1–6 必须继承 `NARRATIVE_REPORT.md` 中的行列设计与语义，不得填入真实数字。
- Figure Plan 必须描述 purpose、panels、axes/visual entities、comparisons、future data source、placeholders 和 caption intent。
- 结果图不得规划虚构曲线或预定柱高；只规划数据字段和待检验趋势。
- Fig. 3 是无实验数字的方法示意图，可以标为当前即可绘制。
- Hero figure 的选择必须解释其对快速审稿阅读的价值；不得为了“更吸引人”而引入第二条叙事。

## 10. 引用与联网约束

- 本轮禁止 WebSearch/WebFetch 和任何联网文献补全。
- 不得生成 BibTeX、DOI、作者、年份、venue 或论文结论。
- Citation Plan 只规划已有引用占位符应放在哪一节、支持什么定位，以及后续如何核验。
- Table 5 的所有 ✓ / ✗ / partial / — 均标记为需要逐项文献核验。
- 不得使用未经核验的 first/only/never/no prior work 表述。

## 11. Codex MCP 独立评审

使用 ARIS skill 规定的 Codex MCP reviewer：

- model：`gpt-5.6-sol`
- reasoning effort：`xhigh`
- reviewer 输入：完整 outline、Claims–Evidence Matrix 和本任务的证据约束；
- 不向 reviewer 提供任何外部 style reference；
- 重点评分：逻辑流、claim–evidence 对齐、缺失实验、定位风险、条件式篇幅可行性、front matter、占位符纪律和是否存在第二故事线。

若 Codex MCP 不可用：

- 不得伪造 reviewer feedback；
- 在目标文件中明确写 `CROSS_REVIEW_UNAVAILABLE`；
- 完成未经交叉评审的 draft plan 后停止并报告，等待人工决定。

## 12. 完成前自检

完成前必须检查并在 Claude 对话中报告：

- 实际写入文件是否恰好只有 `paper/01_planning/PAPER_PLAN.md`；
- C1–C4、H1–H5、Table 1–6、Fig. 1–6 是否全部存在；
- 是否错误使用 7 页或 9 页；
- 是否存在账本外占位符；
- 是否把 planned/hypothesis 写成 observed/proven；
- 是否完成 Codex MCP cross-review；
- 是否启动了任何 writing/figure/compile 后续技能（必须为否）；
- `source_proposal.md` SHA-256 是否仍为 `E700D46BDD1B4F83A2D45466EDBDB2112D2FAB3EFDCC912A7AED2F5BDFC496CC`。

输出 `PAPER_PLAN.md` 后立即停止，等待用户和 Codex 当前任务中的独立验收。

