# tests/

- **用途**：验证骨架 schema、追溯字段、配置快照和跨阶段角色隔离。
- **输入/输出**：输入为 synthetic fixture；输出为测试通过/失败，不产出实验结果。
- **命名规则**：`test_*.py`；fixture 使用 `synthetic_*`，不得冒充真实数据。
- **Run ID 对应**：测试不属于 R001/R002；测试 ID 不得登记为正式 run。
- **可提交**：单元测试和小型 synthetic fixture；真实样本与 benchmark 输出不提交。
- **大文件**：测试需要的大对象仅登记生成器、路径别名、SHA-256 和 manifest。

负向测试必须覆盖：未批准 runtime 值被擅自填写、baseline exact-name 条件被
弱化、六项实现规则缺失、pilot/confirmatory 重叠，以及出现禁用的 no-pad
占位符。测试通过只代表骨架约束有效，不代表实验结果或运行环境有效。

`test_sanity_components.py` 还覆盖 tie-aware CCC、CI-decided SR@20%、CTI 方向、
OLS/Holm、clustered BCa、固定 split、priority sampling、neutral-pad 短目标失败、
整 bundle 预算拒绝、精确 provenance reuse 和 standardized wrapper。fixture 仍是
synthetic，不得登记为论文结果。

runtime 负向测试还要求 dependency inventory 只能包含规范化 package name 与
version；出现 URL、路径或额外安装来源字段必须拒绝。静态校验会重算 inventory、
环境锁、preflight、R000 profile 和 probe 脚本之间的 SHA-256 引用。

`test_model_adapter.py` 使用纯标准库 recording fake 验证：构造零模型调用、禁止
special tokens、neutral-pad token IDs 不经 decode/re-encode、seed 和 decoding
SHA-256 追溯，以及 unresolved revision/越界 continuation 的 fail-closed 行为。

`test_data_adapter.py` 用临时小型、同格式 ZIP/JSONL 验证 ALFWorld JSON-game
common support、HotpotQA replay trace、稳定双流 7:3 split、缺失 replay pair 拒绝，
以及 data manifest 不能提前打开正式 run gate。真实 payload 仅由独立只读校验器
从 repo 外源文件加载，不进入测试 fixture 或 Git。

`test_provenance.py` 验证 dirty inventory 只含相对内容寻址路径，并对两个 atomic
manifest 做负向 gate 测试：把状态改成 READY 必须被拒绝。
