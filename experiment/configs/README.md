# configs/

- **用途**：保存协议参数接口、不可执行模板、schema 和未来冻结配置。
- **输入/输出**：输入为用户批准的协议决策；输出为带 SHA-256 的配置快照。
- **命名规则**：`protocol.pending.json` 只含待批准接口；冻结配置使用
  `<run-family>-<revision>.json`，schema 位于 `schemas/`。
- **Run ID 对应**：一个 `R###` family 可有多个原子 run，但每个原子 run 固定引用
  一个不可变配置快照。
- **可提交**：配置、schema、模板和小型枚举表；不得提交 secret 或私有 endpoint。
- **大文件**：外部 prompt corpus/配置包仅登记路径别名、SHA-256 与 manifest。

## 当前协议文件

- `protocol.pending.json`：保留全部后续开放接口的 pending 模板；Stage 2C 不覆盖
  或删除其中字段。
- `pilot-protocol.locked.20260719.json`：用户于 2026-07-19 批准的 Stage-1 pilot
  锁定快照，同时包含 G-C1 与 confirmatory token-affordability ceiling。
- `pilot-protocol.locked.20260719.manifest.json`：锁定快照及对应
  `PRE_RUN_PROTOCOL.md` 的 SHA-256 追溯记录。
- `schemas/pilot-protocol-lock.schema.json`：锁定快照的字段和关键常量约束。
- `baseline-fidelity.pending.json`：ReasoningBank-style / MemRL-style 的来源、
  revision、实现模式、adapter 与偏差登记接口；未核验时禁止 exact-name claim。
- `pilot-implementation.pending.json`：Stage 2C 尚未无歧义定义的六项工程规则，
  逐项列出原始待批准字段和阻塞路径；作为历史模板保留。
- `pilot-implementation.locked.20260719.json`：用户委托采用推荐方案后形成的六项
  工程规则锁，包括固定 AUDIT split、TRAIN priority、neutral-pad、原子预算、
  G-C1 bootstrap/Holm 和 shared-control reuse。
- `pilot-implementation.locked.20260719.manifest.json`：Stage 2D 锁与同步后的
  `PRE_RUN_PROTOCOL.md` 的 SHA-256 追溯记录。
- `sanity-baseline.locked.20260719.json`：只覆盖 R001/R002 工程 sanity 的内部
  standardized wrapper；禁止据此宣称 exact upstream fidelity。
- `sanity-engineering.locked.20260719.manifest.json`：批准快照与核心实现文件的
  SHA-256 追溯清单，并记录正式 run/GPU/model/install 均为 0。
- `model-adapter.contract.20260719.json`：只锁定 token-ID 模型 adapter 的工程
  接口、环境锁引用和执行边界。具体 model/tokenizer revision 必须由后续原子
  run manifest 显式绑定；该合同不开放模型推理或正式 R001/R002。
- `schemas/runtime-designation.schema.json`、`schemas/baseline-fidelity.schema.json`、
  `schemas/pilot-implementation.schema.json`：上述 pending 接口的结构约束。
- `schemas/*-lock.schema.json`：本轮批准的 runtime、baseline 与 pilot 实现锁约束。
- `schemas/dependency-inventory.schema.json`、
  `schemas/runtime-environment-lock.schema.json` 和
  `schemas/runtime-preflight-result.schema.json`：attempt-002 实测依赖清单、环境锁
  与 metadata-only PASS 快照的结构、脱敏和 readiness 边界。
- `schemas/model-adapter-contract.schema.json`：模型 adapter 工程 READY 与其余门禁
  继续 BLOCKED 的结构约束。
- `schemas/real-toy-data-manifest.schema.json`：真实双流 toy source provenance、
  content-free indexes、固定 7:3 split 和后续门禁仍 BLOCKED 的结构约束。
- `atomic-r001-sanity.planned.20260719.json` 与
  `atomic-r002-sanity.planned.20260719.json`：不可执行 planning snapshots；已绑定
  环境/数据/协议，未猜填 seed、模型 revision、decoding 或 R001 output。
- `schemas/atomic-*.schema.json` 与 `schemas/dirty-worktree-inventory.schema.json`：
  blocked atomic envelope、输入引用和 dirty 内容证明的结构约束。

锁定快照只覆盖其中明确列出的 scope。formal K、`n^audit`、formal seed count、
governance dead-zone、Huber δ 和其他 pre-confirmatory 参数仍以
`USER_APPROVAL_REQUIRED` 表示。

所有 `*.pending.json` 都是不可执行接口。获批值必须写入新的、带日期或 revision
的锁定快照，并由 run manifest 引用其路径别名和 SHA-256；不得覆盖 pending
模板，也不得把 formal K、`n^audit` 或 formal seed count 当作 pre-pilot 用户
常数填写。
