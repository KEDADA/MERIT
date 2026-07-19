# runs/

- **用途**：保存原子 run 的配置快照、run manifest、状态和失败记录。
- **输入/输出**：输入为冻结配置/环境/数据 manifest；输出为追溯记录和产物引用。
- **命名规则**：`R###__<phase>__<slug>__seed-<seed|pending>__aNNN/`；`R###`
  对应 tracker run family，`aNNN` 是原子展开序号。
- **Run ID 对应**：一目录一原子 run；run ID、family ID 和 seed 必须同时记录。
- **可提交**：manifest、配置快照、小型 status/summary；日志和 raw 输出不提交。
- **大文件**：日志、checkpoint、trajectory 只登记路径别名、SHA-256 与 artifact
  manifest。

## 当前 blocked atomic manifests

- `R001__sanity__paired-replay-real-toy__seed-pending__a001/` 与
  `R002__sanity__metrics-real-toy__seed-pending__a001/` 是字段完整、内容寻址但不可
  执行的原子 envelope；状态固定 `BLOCKED`，`execution_authorized=false`。
- 每个目录包含 run manifest、input manifest 和空 artifact manifest。输入引用均
  使用 repo 相对路径与 SHA-256，输出/日志均为空。
- `provenance/dirty-worktree.20260719.json` 记录所有非 envelope dirty 文件的状态、
  类型、大小和内容 SHA-256。三个生成 envelope 路径显式排除以避免自引用哈希环；
  校验器会重算其余完整 dirty worktree 并拒绝漂移。
- exact model/tokenizer revision、decoding、整数 seed 与 R002 upstream output 仍为
  formal gate binding，不得通过原地修改这些 blocked manifests 打开执行。
