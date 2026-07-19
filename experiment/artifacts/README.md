# artifacts/

- **用途**：登记模型、checkpoint、日志包、图表源数据等产物，不承载大型内容。
- **输入/输出**：输入为 run 产物；输出为 artifact manifest 和完整性元数据。
- **命名规则**：`<atomic-run-id>.artifact-manifest.json`，artifact ID 在 run 内唯一。
- **Run ID 对应**：每条 artifact 必须指向唯一 atomic run ID 和生成步骤。
- **可提交**：manifest、校验报告和小型文本摘要；大型 blob 不提交。
- **大文件**：仅记录非私有路径别名、SHA-256、大小、MIME、创建时间和保留策略。

当前两个 atomic sanity envelope 各含一个 `NOT_STARTED` 空 artifact manifest；
它们证明输出命名与追溯接口已存在，但不表示任何日志、结果或模型产物已生成。
