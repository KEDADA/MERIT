# results/

- **用途**：保存由成功 run 派生、可复算的小型聚合结果和 provenance。
- **输入/输出**：输入为已核验 run/artifact manifest；输出为 JSON/CSV/Markdown 汇总。
- **命名规则**：`<table-or-figure>-<revision>.<ext>`，并配套 provenance manifest。
- **Run ID 对应**：每个结果必须列出全部 source atomic run IDs，禁止手工填数。
- **可提交**：小型汇总、校验摘要和 manifest；未核验结果必须显式标记状态。
- **大文件**：预测、轨迹和中间数组只记录路径别名、SHA-256 与 artifact manifest。

