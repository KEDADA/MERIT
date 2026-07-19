# MERIT 占位符账本（Placeholder Ledger）

> 状态：`ACTIVE`
>
> 权威占位符来源：`paper/00_input/NARRATIVE_REPORT.md`
>
> 建立时统计：234 个唯一 ID。
>
> 2026-07 更新：经用户批准，依据 `PRE_RUN_PROTOCOL.md` 新增 7 个协议派生占位符（见完整登记表），当前唯一 ID 总数 **241**。这 7 个 ID 的权威来源为 `PRE_RUN_PROTOCOL.md`；其余条目仍以 `NARRATIVE_REPORT.md` 为准。
>
> 本账本登记实验结果、成本、实现测量、引用与会议信息。未经验证，不得用真实数值或引用替换任何条目。

## 1. 使用规则

- 状态流转：`UNRESOLVED → DATA_AVAILABLE → VERIFIED → REPLACED`；删除分析时可经人工批准改为 `NOT_APPLICABLE`。
- 从 `UNRESOLVED` 进入 `DATA_AVAILABLE` 时，必须在“权威来源/计算”栏补充具体数据路径和脚本路径。
- 进入 `VERIFIED` 前必须记录：指标定义、聚合口径、随机种子、单位、统计检验、复核者和日期。
- `REPLACED` 后必须全局搜索同一 ID，确保正文、表格、图和附录同步替换。
- 派生指标必须从已核验基础量计算，不得手工录入。
- 引用条目必须核验标题、作者、年份、venue 和稳定 URL/DOI；不得凭模型记忆补全。
- 将任何条目替换为真实值前必须获得用户确认。

## 2. ID 语义约定

- `MAIN_<METHOD>_<DATASET>`：主表中指定方法和数据集的主指标；`AVG` 表示预先定义的聚合平均。
- `ABL_<VARIANT>_<METRIC>`：指定消融变体的 AVG、DELTA、SR20、CCC 或 CTI。
- `PILOT_*`：诊断性 pilot 的 CCC、SR、可靠性、控制实验或预算。
- `PLUGIN_*` / `REWARD_SWAP_*`：奖励替换实验及其派生增益。
- `EFF_*`、`*_TOKEN_*`、`*_LATENCY_*`、`*_VRAM_*`：效率和成本。
- `CITATION_*`：必须通过文献核验获得的引用记录，不是自由文本。

## 3. 数据登记附加字段

条目不再是 `UNRESOLVED` 时，必须补充 `data_path`、`script_path`、`metric_definition`、`aggregation`、`unit`、`verification_record`、`verified_by`、`verified_at` 和 `replacement_commit_or_snapshot`。

## 4. 完整登记表

| 占位符 ID | 类别 | 待填内容 | 权威来源/计算 | 状态 |
|---|---|---|---|---|
| `[[TBD:A1_RELATIVE_TOKEN_COST]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:AAAI2027_TRACK_PAGE_LIMIT]]` | 会议信息 | AAAI 2027 track 与页数限制 | 对应 AAAI 2027 官方 call | `UNRESOLVED` |
| `[[TBD:ABL_A1_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A1_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A1_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A1_DELTA]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A1_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A2_AVG]]` | 消融 | 容量、架构、特征、更新规则和计算预算匹配、仅监督标签替换为观察性/outcome label 的 A2 对照——AVG | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A2_CCC]]` | 消融 | 容量、架构、特征、更新规则和计算预算匹配、仅监督标签替换为观察性/outcome label 的 A2 对照——CCC | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A2_CTI]]` | 消融 | 容量、架构、特征、更新规则和计算预算匹配、仅监督标签替换为观察性/outcome label 的 A2 对照——CTI | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A2_DELTA]]` | 消融 | 容量、架构、特征、更新规则和计算预算匹配、仅监督标签替换为观察性/outcome label 的 A2 对照——ΔAVG | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A2_SR20]]` | 消融 | 容量、架构、特征、更新规则和计算预算匹配、仅监督标签替换为观察性/outcome label 的 A2 对照——SR@20% | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A3_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A3_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A3_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A3_DELTA]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A3_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A4_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A4_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A4_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A4_DELTA]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A4_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A5_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A5_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A5_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A5_DELTA]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A5_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A7_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A7_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A7_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A7_DELTA]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_A7_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_AJUDGE_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_AJUDGE_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_AJUDGE_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_AJUDGE_DELTA]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_AJUDGE_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_FULL_AVG]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_FULL_CCC]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_FULL_CTI]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ABL_FULL_SR20]]` | 消融 | 消融表指标 | 消融实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:ACA_HELDOUT_CCC_T500]]` | ACA/校准 | ACA 实现、准确性或校准指标 | ACA 配置、预测与校准分析 | `UNRESOLVED` |
| `[[TBD:ACA_SCORING_LATENCY_MS]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:ACA_TRAINABLE_PARAMS]]` | ACA/校准 | ACA 实现、准确性或校准指标 | ACA 配置、预测与校准分析 | `UNRESOLVED` |
| `[[TBD:ACA_VRAM_OVERHEAD_GB]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:ACA_ZEROSHOT_TRANSFER_CCC_WEBARENA]]` | ACA/校准 | ACA 实现、准确性或校准指标 | ACA 配置、预测与校准分析 | `UNRESOLVED` |
| `[[TBD:CASE_SUPERSTITION_EVICTION_TASK_INDEX]]` | 案例 | 案例研究事件指标 | 案例事件日志 | `UNRESOLVED` |
| `[[TBD:CITATION_A_MEM]]` | 引用 | A MEM 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_AWM]]` | 引用 | AWM 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_CONTEXTCITE]]` | 引用 | CONTEXTCITE 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_DATA_SHAPLEY]]` | 引用 | DATA SHAPLEY 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_EDV]]` | 引用 | EDV 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_EEVEE]]` | 引用 | EEVEE 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_EVO_MEMORY]]` | 引用 | EVO MEMORY 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_INFLUENCE_FUNCTIONS]]` | 引用 | INFLUENCE FUNCTIONS 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MATTS]]` | 引用 | MATTS 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MEM_ALPHA]]` | 引用 | MEM ALPHA 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MEM0]]` | 引用 | MEM0 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MEMEVOLVE]]` | 引用 | MEMEVOLVE 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MEMORY_R1]]` | 引用 | MEMORY R1 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MEMRL]]` | 引用 | MEMRL 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_MEMSKILL]]` | 引用 | MEMSKILL 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_REASONINGBANK]]` | 引用 | REASONINGBANK 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_REFLEXION]]` | 引用 | REFLEXION 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_SKEMEX]]` | 引用 | SKEMEX 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_SKINNER_SUPERSTITION]]` | 引用 | SKINNER SUPERSTITION 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:CITATION_TRACIN]]` | 引用 | TRACIN 的文献元数据 | 出版方或论文官方页面 | `UNRESOLVED` |
| `[[TBD:ECE_ACA_HELDOUT]]` | ACA/校准 | ACA 实现、准确性或校准指标 | ACA 配置、预测与校准分析 | `UNRESOLVED` |
| `[[TBD:EFF_A1_AVG]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:EFF_BASELINE_AVG]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:EFF_MERIT_AVG]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:EFF_RITFULL_AVG]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:FIG1_TOPUTILITY_ZERO_EFFECT_FRACTION]]` | 图示 | 图示所需派生指标 | 对应实验日志与绘图数据脚本 | `UNRESOLVED` |
| `[[TBD:FIG4_LATE_STREAM_GAIN_SHARE]]` | 图示 | 图示所需派生指标 | 对应实验日志与绘图数据脚本 | `UNRESOLVED` |
| `[[TBD:FULL_RIT_COST_MULTIPLIER]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:H5_GAIN_SINGLE_DOMAIN]]` | 边界 | H5 边界分析指标 | 边界实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:H5_GAIN_SMALL_BANK_LT100]]` | 边界 | H5 边界分析指标 | 边界实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:JUDGE_HUMAN_AGREEMENT_KAPPA]]` | 质量控制 | Judge 与人工一致性指标 | 人工复核数据与分析 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AMEM_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AVG_GAIN_OVER_BEST_BASELINE]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_AWM_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_FULLHIST_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_GAIN_MIXED_STREAM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_GAIN_SINGLE_DOMAIN]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_GPU_HOURS_PER_RUN]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEM0_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMALPHA_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMR1_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MEMRL_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_MERIT_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_NOMEM_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANK_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RBANKMATTS_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_REFLEXION_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_RITFULL_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_AVG]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_LCM]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_LME]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_S1]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_S2]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_S3]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_S4]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_S5]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MAIN_SKEMEX_WAL]]` | 主实验 | 主实验表或其派生指标 | 主实验机器可读聚合与派生脚本 | `UNRESOLVED` |
| `[[TBD:MERIT_FRACTION_OF_RITFULL_GAIN]]` | 主实验 | MERIT 获得的 RIT-Full 增益比例 | 由已核验主表派生 | `UNRESOLVED` |
| `[[TBD:MERIT_RELATIVE_TOKEN_COST]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:PILOT_AUDIT_SUPPORT_COVERAGE]]` | Pilot | 具备充分 common support 的记忆比例（审计覆盖率，PRE_RUN_PROTOCOL §3.1） | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_CCC_MEMRL_T500]]` | Pilot | 诊断实验指标或预算 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_CCC_REASONINGBANK_T500]]` | Pilot | 诊断实验指标或预算 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_NEUTRAL_PAD_VALIDATION]]` | Pilot | 中性 padding 等价性验证结果（pad 与真实移除的等价检验，PRE_RUN_PROTOCOL §3.6） | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SPLITHALF_PHI_RELIABILITY]]` | Pilot | 诊断实验指标或预算 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SR20_HARMFUL_T100]]` | Pilot | SR@20% 中有害子类（φ < −δ）比例，t=100（PRE_RUN_PROTOCOL §3.2） | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SR20_HARMFUL_T500]]` | Pilot | SR@20% 中有害子类（φ < −δ）比例，t=500（PRE_RUN_PROTOCOL §3.2） | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SR20_NULL_T100]]` | Pilot | SR@20% 中实际为零子类（|φ| ≤ δ）比例，t=100（PRE_RUN_PROTOCOL §3.2） | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SR20_NULL_T500]]` | Pilot | SR@20% 中实际为零子类（|φ| ≤ δ）比例，t=500（PRE_RUN_PROTOCOL §3.2） | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SR20_T100]]` | Pilot | SR@20% 点估计及其置信区间，t=100 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_SR20_T500]]` | Pilot | SR@20% 点估计及其置信区间，t=500 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_TOTAL_ROLLOUT_BUDGET]]` | Pilot | 诊断实验指标或预算 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_TOTAL_TOKEN_COST]]` | Pilot | 诊断实验指标或预算 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PILOT_UTILITY_SUBSET_REMOVAL_DROP]]` | Pilot | 诊断实验指标或预算 | Pilot 日志与 RIT 分析脚本 | `UNRESOLVED` |
| `[[TBD:PLUGIN_MEMALPHA_ORIG_AVG]]` | 插件 | Reward-swap 实验指标 | 插件实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:PLUGIN_MEMALPHA_PHI_AVG]]` | 插件 | Reward-swap 实验指标 | 插件实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:PLUGIN_MEMR1_ORIG_AVG]]` | 插件 | Reward-swap 实验指标 | 插件实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:PLUGIN_MEMR1_PHI_AVG]]` | 插件 | Reward-swap 实验指标 | 插件实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:RESIDUAL_FAILURE_NO_RELEVANT_MEMORY_FRACTION]]` | 失效分析 | 残余失败构成比例 | 失败案例分类数据 | `UNRESOLVED` |
| `[[TBD:REWARD_SWAP_MEMALPHA_GAIN]]` | 插件 | Reward-swap 实验指标 | 插件实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:REWARD_SWAP_MEMORY_R1_GAIN]]` | 插件 | Reward-swap 实验指标 | 插件实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:RIT_BUDGET_EPSILON_PERCENT]]` | RIT/预算 | RIT 配置或开销指标 | 最终 RIT 配置与执行日志 | `UNRESOLVED` |
| `[[TBD:RIT_ROLLOUT_EQUIV_PER_EVENT]]` | 效率/成本 | 每部署事件的 RIT 摊销成本（rollout-equivalent/event，PRE_RUN_PROTOCOL §3.7） | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:RIT_SAMPLING_PROB_PERCENT]]` | RIT/预算 | RIT 配置或开销指标 | 最终 RIT 配置与执行日志 | `UNRESOLVED` |
| `[[TBD:RIT_TOKEN_OVERHEAD_PERCENT]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:RITFULL_RELATIVE_TOKEN_COST]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |
| `[[TBD:SCALING_GAIN_235B]]` | 扩展 | Backbone 扩展实验增益 | 扩展实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:SCALING_GAIN_32B]]` | 扩展 | Backbone 扩展实验增益 | 扩展实验机器可读聚合 | `UNRESOLVED` |
| `[[TBD:SR_MERIT_T500]]` | 机制 | 迷信率机制指标 | 机制实验分析 | `UNRESOLVED` |
| `[[TBD:SR_REDUCTION_MERIT_T500_PERCENT]]` | 机制 | 迷信率机制指标 | 机制实验分析 | `UNRESOLVED` |
| `[[TBD:TOKEN_OVERHEAD_PERCENT]]` | 效率/成本 | 实现效率或资源成本指标 | 统一 profiling 与成本统计 | `UNRESOLVED` |

## 5. 替换记录

当前无替换记录。

| 日期 | ID | 旧状态 | 新状态 | 数据/脚本 | 复核者 | 说明 |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## 6. 自动验收条件

1. 英文权威叙事报告 `NARRATIVE_REPORT.md`，以及经用户批准登记的 7 个 `PRE_RUN_PROTOCOL.md` 协议派生 ID，其中每个合法 `[[TBD:...]]` ID 在完整登记表中恰好出现一次；
2. 登记表不得包含上述两个授权来源（`NARRATIVE_REPORT.md` 与经批准的 `PRE_RUN_PROTOCOL.md` 派生 ID）之外的 ID；
3. ID 只能包含 `A–Z`、`0–9` 和下划线；
4. 所有新条目初始状态必须为 `UNRESOLVED`；
5. 已替换条目必须带完整追溯信息；
6. 中文查阅版中的 ID 集合必须与英文权威版保持一致。

