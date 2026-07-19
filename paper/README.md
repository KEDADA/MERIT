# MERIT 论文工作区

本目录集中保存 **MERIT — Retrieval Is Not Contribution** 的 AAAI 2027 初稿撰写、审阅、编译和后续实验回填所产生的全部工作文件。

## 工作规则

1. 论文写作流程不得修改 `.agents/docs/` 中的原始论文方案。
2. `00_input/source_proposal.md` 是原始方案的不可变工作快照，后续整理和写作均以此为事实来源。
3. 缺失的实验数据必须使用明确且唯一的占位符表示，不得猜测、补造或用虚假示例数值替代。
4. `.agents/docs/AAAI-AuthorKit27/` 中的 AAAI 2027 Author Kit 是唯一权威的排版与格式来源。
5. `main.tex`、`math_commands.tex`、`references.bib` 等规范文件放在本目录根部。
6. 每一阶段开始前说明目标与验收标准，完成后核验产物，并经用户确认后再进入下一阶段。

## 目录说明

- `00_input/`：不可变方案快照和结构化写作输入。
- `01_planning/`：论文计划、写作政策和占位符账本。
- `sections/`：各章节的 LaTeX 源文件。
- `tables/`：预先构建的 LaTeX 表格。
- `figures/placeholders/`：尚未正式绘制的可编译图形说明占位内容。
- `figures/specs/`：后续图形的详细绘制要求、数据字段和视觉目标。
- `figures/generated/`：获得真实数据后生成的正式图片。
- `references/`：种子文献、候选文献和已核验的参考文献记录。
- `reviews/`：ARIS、Claude 和 Codex 的审稿报告及修改日志。
- `audits/`：数值声明、引用、证明和研究完整性审计结果。
- `scripts/`：可复现的论文维护、数据处理和绘图脚本。
- `build/`：PDF、编译日志及其他中间构建产物；`build/qa/` 保存逐页视觉检查图。

## 当前阶段

已完成：

1. 论文工作区初始化与源方案快照固化。
2. 英文权威叙事报告 `00_input/NARRATIVE_REPORT.md`。
3. 中文查阅版 `00_input/NARRATIVE_REPORT.zh-CN.md`。
4. 写作约束 `01_planning/DRAFT_POLICY.md` 与占位符账本 `01_planning/PLACEHOLDER_LEDGER.md`。
5. ARIS `/paper-plan` 论文计划 `01_planning/PAPER_PLAN.md`，并确认采用 AS1–AS3 假设命名。
6. AAAI 2027 LaTeX 初稿骨架：8 个章节、6 个数据占位表格和 6 个图形说明占位稿。
7. 骨架已成功编译为 `build/main.pdf`，并完成编译日志与逐页版面检查。
8. ARIS `/paper-write` 已将 8 个章节扩写为英文正文初稿；未获得的数据、引用和观察性结论继续使用受控占位符。
9. 第 6 步排版修订与验收已完成：正文占位符在源码中保留完整 ID、在 PDF 中紧凑显示；最新 PDF 为 8 页，无横向溢出、编译错误或未定义引用，并已完成逐页视觉检查。

第 6 步（依据论文计划逐节撰写正文初稿）已经完成。引用核验、正式绘图、实验执行、真实数据回填、附录迁移和整体交叉评审均尚未启动；实验数值、结论性陈述与参考文献不得在未经核验时补造。进入下一阶段前必须由用户确认。
