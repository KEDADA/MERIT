# MERIT AAAI 2027 初稿写作政策（Draft Policy）

> 状态：`ACTIVE`
>
> 适用范围：`paper/` 下的论文规划、LaTeX 初稿、表格、图示规格、审阅和审计文件。
>
> 目的：允许在实验尚未完成时建立一份完整、可编译、可审阅的 AAAI 初稿，同时禁止把计划、假设或示例数字伪装成真实证据。

## 1. 权威来源与优先级

发生冲突时，按以下顺序处理：

1. 用户在当前任务中的明确指令；
2. AAAI 2027 官方模板：`.agents/docs/AAAI-AuthorKit27/`；
3. 本文件 `paper/01_planning/DRAFT_POLICY.md`；
4. 英文权威叙事报告 `paper/00_input/NARRATIVE_REPORT.md`；
5. 源方案快照 `paper/00_input/source_proposal.md`；
6. ARIS 或 Claude 生成的规划、草稿和评审建议。

`paper/00_input/NARRATIVE_REPORT.zh-CN.md` 仅供中文查阅。如中英文叙事报告存在差异，以英文版为准。

不得直接修改 `source_proposal.md`。其 SHA-256 必须保持为：

`E700D46BDD1B4F83A2D45466EDBDB2112D2FAB3EFDCC912A7AED2F5BDFC496CC`

## 2. 工作区边界

- 所有论文撰写产物必须位于 `paper/` 内。
- 不得覆盖 `.agents/docs/AAAI-AuthorKit27/` 中的官方模板。
- 需要使用模板文件时，应复制到后续确定的 `paper/` 子目录，并保留原始许可与样式文件。
- `paper/build/` 仅存放编译生成物；源文件不得只存在于 `build/`。
- 未经用户确认，不得启动下一阶段、批量运行实验、联网补引文、提交 Git、发送消息或发布文件。
- 每个阶段只修改该阶段授权的文件。发现范围外问题时记录到审计文件，不顺手扩展任务。

## 3. 三类证据状态

论文规划和初稿中的非平凡主张必须能归入以下一种状态：

| 状态 | 含义 | 允许的措辞 | 禁止的措辞 |
|---|---|---|---|
| `SUPPORTED-BY-DESIGN` | 可由已给出的架构、定义或算法直接检查，但不代表经验有效 | “the design performs one ACA scoring pass per retrieval event” | “the method is efficient in practice” |
| `PLANNED-EVIDENCE` | 需要尚未完成的实验、统计或实现测量 | “we will test whether…”, “planned evaluation” | “we show”, “results demonstrate”, “outperforms” |
| `HYPOTHESIS` | 理论或经验假设，尚未证明/证实 | “we hypothesize”, “pending formal proof” | “we prove”, “the theorem establishes” |

特殊约束：

- C1–C4 的总体状态均为 `PLANNED-EVIDENCE`。
- Proposition 1 当前为 `HYPOTHESIS`，直到正式陈述、证明和人工核验均完成。
- O(1) online scoring 是设计属性；ACA 的实际延迟、成本和归因准确率仍是 `PLANNED-EVIDENCE`。
- 设计参数不是实验结果，但必须标记为 `planned configuration`、`provisional hyperparameter`、`planned gate` 或 `target criterion`。

## 4. 占位符规范

### 4.1 唯一合法格式

未知数据使用：

```text
[[TBD:<UPPERCASE_SEMANTIC_ID>]]
```

ID 只能包含大写英文字母、数字和下划线。禁止使用 `X.XX`、问号、随机数字、范围中点、空白单元格或“合理猜测”。

### 4.2 何时必须使用

以下尚未测量或核验的内容必须使用占位符：

- accuracy、success rate、AVG、gain、drop、correlation、CCC、SR@k；
- mean、standard deviation、confidence interval、p-value、effect size；
- latency、GPU hours、token/API cost、VRAM、overhead、parameter count；
- calibration error、agreement、比例、任务索引等经验量；
- 未核验的引用元数据；
- AAAI 2027 具体 track/page limit 等尚未确认的会议信息。

### 4.3 生命周期

占位符状态只允许：

1. `UNRESOLVED`：尚无可信数据；
2. `DATA_AVAILABLE`：已有原始输出，但尚未完成核验；
3. `VERIFIED`：数据来源、计算脚本、统计口径和复核均完成；
4. `REPLACED`：已在论文源文件中替换，并通过全局一致性检查；
5. `NOT_APPLICABLE`：经人工决定删除对应分析，而不是填入数字。

未经进入 `VERIFIED`，不得将占位符替换为真实数值。任何替换都必须同步更新 `PLACEHOLDER_LEDGER.md`，并记录数据文件、计算脚本、统计口径、复核者和日期。

### 4.4 一致性规则

- 同一语义量在正文、表格、图示规格和附录中必须复用同一 ID。
- 不同方法、数据集、种子聚合口径或时间点必须使用不同 ID。
- 派生量必须记录计算公式，不得手工复制数字。
- 正负号和单位属于指标定义的一部分；替换前必须确认“越大越好/越小越好”。
- 英文权威文件中的占位符是账本基准；中文查阅版不得改变 ID。

## 5. 未完成实验时的正文写法

允许先完成：

- 完整的研究动机、问题定义、方法、算法、实验协议和限制；
- 带完整行列结构的表格；
- 带 caption 草稿、坐标、panel 和数据来源说明的图示占位；
- 以条件或计划语气表述的结果段落骨架。

实验完成前，结果段落必须使用类似结构：

```text
Table X will test whether MERIT improves ... .
The measured gain is [[TBD:...]], pending verification.
If the effect is not supported, this interpretation must be revised or removed.
```

禁止：

- 使用 “we show/demonstrate/find/observe” 描述未运行实验；
- 使用 “significantly” 而没有已核验检验与 p-value；
- 先写结论再寻找数字配合；
- 隐藏不支持假设的结果；
- 把源方案中的示例数值、目标数值或 `◇` 数值当成结果。

## 6. 表格政策

- 表格必须在没有真实数字时也保持完整：caption、方法行、指标列、单位、方向和必要脚注不可省略。
- 未知结果单元格必须使用账本中的 `[[TBD:...]]`。
- 固定参照值（例如基线相对成本 `1×` 或 reference delta `0`）只有在定义上成立时才可直接写出，并应在 caption/脚注说明。
- 加粗、下划线、排名和显著性标记只能在数据进入 `VERIFIED` 后生成。
- 不得预先把 MERIT 行加粗为最佳结果；方法名本身可加粗以标识 ours，但不得暗示排名。
- 每张最终表格必须能追溯到生成它的机器可读数据和脚本。

## 7. 图示政策

- 数据图未生成前，在 LaTeX 对应位置放置带边框的文字占位框；文字必须说明 future figure 的目的、panel、坐标轴、比较方法、数据来源和占位符。
- 不得绘制带虚构曲线、柱高、误差带或散点位置的“示意结果图”。
- 纯方法示意图（如 Fig. 3）可在无实验数据时绘制，但不得加入经验性能数字。
- Fig. 2 与 Fig. 5 必须采用相同的坐标范围和统计口径；任何变更必须同步进行。
- 图生成后必须检查轴标签、单位、图例、颜色可辨性、黑白打印可读性及 caption 与正文一致性。

## 8. 引用与相关工作政策

- 不得编造 BibTeX、DOI、作者、年份、页码、结论或比较结果。
- 引用未核验时使用 `[[TBD:CITATION_<NAME>]]` 或账本中对应的合法 ID。
- “first”“only”“never”“no prior work”“all existing methods”等优先性表述，必须在完成系统文献检索和逐项核验后才能使用。
- 核验前使用限定措辞，例如：
  - “the source proposal characterizes…”
  - “among the methods currently reviewed…”
  - “pending bibliographic verification…”
- Table 5 的每个 ✓ / ✗ / partial / — 都必须有可追溯证据；不能依据记忆或方法名称猜测。

## 9. 方法与理论政策

- 保持唯一方法主线：`RIT → ACA → consumers`。
- Credit Governance 与 Scope-Gated Retrieval 是因果信用的消费者，不得改写成独立故事。
- RL manager 只保留为 reward-swap plugin；不得重新升级为主方法。
- Full Shapley 只保留为边界/附录变体；不得无授权扩展为第二套核心方法。
- 不得新增源方案未授权的模型架构、数据集、baseline、指标、贡献点或定理。
- 修改符号、假设或算法前，必须同步检查 C1–C4、H1–H5、表格、图示和 Source Traceability Map。

## 10. AAAI 2027 格式政策

- 必须以 `.agents/docs/AAAI-AuthorKit27/` 为模板来源。
- 不得修改 `aaai2027.sty`，不得通过缩小页边距、调整章节间距或其他压缩技巧规避页数限制。
- 当前具体 track 和页数限制仍为 `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]`；必须从对应 AAAI 2027 call 核验，不能沿用源方案的 9 页假设。
- 初稿使用匿名作者信息；在明确进入 camera-ready 阶段前不得泄露作者身份或致谢信息。
- 附录是否计入页数、参考文献规则和 reproducibility checklist 均以对应 event 的正式要求为准。
- 每个阶段结束时至少执行一次 LaTeX 编译；不得把“源文件存在”视为“模板合规”。

## 11. ARIS 使用与人工审批门

- `NARRATIVE_REPORT.md` 是 `/paper-plan` 的权威输入。
- ARIS 输出是建议性产物，不得覆盖本政策或源方案。
- 禁止从 `/paper-plan` 自动继续到 `/paper-writing`；必须先由用户审阅并确认计划。
- 每次 ARIS/Claude 任务必须明确允许读取和写入的文件列表。
- 自动任务结束后必须检查越界文件、源方案哈希、占位符变化和证据措辞。
- 用户未确认前，不得从计划阶段进入 LaTeX 骨架或章节写作阶段。

## 12. 变更控制

以下变更必须先停下并请求用户确认：

- 修改 C1–C4、H1–H5 或 Proposition 1 的范围/状态；
- 新增或删除数据集、baseline、指标、表格、主图或方法模块；
- 改变投稿 track、页数目标或匿名策略；
- 将任何占位符替换为真实数值；
- 删除负结果、证伪门槛或限制；
- 启动 `/paper-writing`、实验执行或联网文献核验。

## 13. 阶段验收清单

每一阶段结束时至少检查：

- [ ] 只修改了授权范围内的文件；
- [ ] `source_proposal.md` 哈希保持一致；
- [ ] C1–C4、H1–H5、Table 1–6、Fig. 1–6 未意外丢失；
- [ ] 没有 `◇`、`X.XX`、随机结果数字或未登记占位符；
- [ ] 没有把 planned/hypothesis 写成 observed/proven；
- [ ] 没有未经核验的优先性或文献结论；
- [ ] 表格结构完整，图示位置有明确规格；
- [ ] LaTeX 阶段能够从干净环境编译；
- [ ] 下一阶段尚未在用户确认前启动。
