# MERIT 实验工程骨架

本目录是 MERIT 的实验工程边界。阶段 3 只建立可追溯、可校验的骨架，不执行
R001/R002、训练、benchmark、GPU 压测或正式实验。论文、协议、账本和 R000
仍由仓库原有目录管理；本目录不复制或回填其结果。

## 目录树

```text
experiment/
├── environments/  已确认环境基线与锁定策略
├── configs/       协议参数、配置模板和 manifest schema
├── src/           纯标准库追溯与校验实现
├── scripts/       只读校验入口；未来运行入口需另行批准
├── tests/         骨架单元测试与小型 synthetic fixture
├── data/          数据 manifest、小型 fixture；不存放真实大数据
├── runs/          原子 run manifest、配置快照和状态记录
├── results/       可提交的小型聚合结果及其来源索引
└── artifacts/     大型产物的路径、SHA-256 和 manifest
```

## 实验生命周期

1. **协议锁定**：`configs/protocol.pending.json` 中所有
   `USER_APPROVAL_REQUIRED` 必须由用户批准后，通过新的、可追溯配置快照锁定。
2. **环境锁定**：以 `environments/baseline.json` 为已确认事实；目标 runtime
   已在 `runtime-target.locked.20260719.json` 中获批，并由 attempt-002 的只读
   metadata preflight、dependency inventory 与环境锁完成实测锁定。不得从该
   metadata 结果推断模型容量、吞吐、adapter 正确性或正式 run 就绪。
3. **数据登记**：真实数据只写入 repo 外路径；`data/` 仅保存 manifest、SHA-256、
   sample-index 摘要和跨角色零重叠证明。
4. **run 展开**：tracker 的 `R###` 是 run family；原子 run 使用
   `R###__<phase>__<slug>__seed-<seed|pending>__aNNN`。每个原子 run 必须记录
   seed、代码提交、dirty-worktree 证明、配置快照及输入 manifest。
5. **执行与状态**：状态只能按 `PLANNED/READY/RUNNING/SUCCEEDED/FAILED/`
   `ABORTED/INVALID/BLOCKED` 记录；失败必须带规范化 failure type。
6. **聚合与发布**：`results/` 只接收由成功 run 派生的小型汇总；大型日志、
   checkpoint 和原始产物进入外部存储，仅在 manifest 中登记路径和 SHA-256。

## 数据流与隔离

```text
外部只读数据 -> data manifest + sample-index SHA-256
             -> pilot:{pilot_train,pilot_audit}
             -> confirmatory:{fit,calibration,development,sealed_final_audit}
             -> run config snapshot -> run manifest -> artifact manifest
             -> 小型聚合结果 + provenance
```

pilot 与 confirmatory 必须使用不同 partition，且每一对跨阶段 partition 都要有
`overlap_count = 0` 的 disjointness check。pilot 数据只能用于方差估计和 sizing，
不得进入 confirmatory gate。`sealed_final_audit` 不得参与模型、阈值、校准或
stopping 选择。

## 结果追溯最低要求

每个可执行 run 必须能够从结果反向定位：run ID、run family、seed、代码提交、
dirty 路径摘要、配置快照及 SHA-256、环境基线、数据 manifest、日志、原始产物、
artifact manifest、状态、失败类型和聚合脚本。任一字段缺失时不得标记为 READY。

## 当前边界

- 当前已实现 R001/R002 的 CPU-only 工程组件与 synthetic sanity 校验，不表示
  正式 R001/R002 已执行或已就绪。目标 runtime 的 metadata preflight 与依赖
  inventory 已通过；模型 adapter 的 token-ID/generation/provenance 工程合同也已
  由注入式假后端通过标准库测试，但未绑定或调用真实模型。只读数据 adapter 与
  ALFWorld/HotpotQA 双流真实 toy split 已完成并通过源文件哈希、可加载性和零重叠
  校验。R001/R002 各自的 blocked atomic manifest、planning config、输入引用、空
  artifact envelope 与 dirty-worktree 内容清单已完成；正式执行门禁尚未评估。
- 所有未批准协议参数均以 `USER_APPROVAL_REQUIRED` 标记。
- `baseline-fidelity.pending.json` 只允许先登记 `ReasoningBank-style` 与
  `MemRL-style` 类别；只有 source-faithful checklist 通过后才能使用 exact
  method name，否则必须标为 standardized credit-variant wrapper。
- 六项 Stage 2C 工程规则已在 `pilot-implementation.locked.20260719.json` 中按
  用户委托批准；原 pending 模板保留为历史接口，未被覆盖。
- R001 当前只批准内部 standardized wrapper，不宣称 exact ReasoningBank/MemRL
  fidelity；R010/R011 与 M2 baseline execution 仍需 source-fidelity 证据。
- 禁止把凭据、Token、`.env`、机器私有配置、真实数据或大型产物提交到 Git。
- 不创建 no-pad 结果占位符或独立主实验臂；redundancy 轴维持 `EVIDENCE GAP`。
