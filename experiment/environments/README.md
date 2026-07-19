# environments/

- **用途**：记录已确认硬件/软件事实、项目 runtime 指定和依赖锁定策略。
- **输入/输出**：输入为只读环境盘点；输出为基线 JSON、锁文件及变更说明。
- **命名规则**：`baseline.json` 保存证据基线；未来锁文件使用
  `environment-<date>-<revision>.*`。
- **Run ID 对应**：环境基线主要对应 R000，并由所有 R001+ run manifest 引用。
- **可提交**：小型 JSON、依赖锁文件、容器 recipe 和中文说明；不得写凭据。
- **大文件**：镜像、wheel cache 和环境包只登记外部路径、SHA-256 与 manifest。

## 当前文件

- `baseline.json`：R000 已确认的 H20/Python/PyTorch/CUDA 观察事实，不是项目
  runtime 锁。
- `runtime-designation.pending.json`：候选 runtime 的只读证据引用、待批准指定项
  和尚未执行的 preflight 清单；固定为 `BLOCKED`，不得作为 run 环境快照。
- `runtime-target.locked.20260719.json`：已批准以 R000 观察栈作为项目目标；其
  `PENDING_PREFLIGHT` 状态是硬边界，未捕获 dependency lock 前不得用于正式 run。
- `runtime-preflight.20260719.json`：首次只读 preflight 的脱敏结果。当前会话无法
  解析 R000 登记的隔离 runtime 引用，因此版本/CUDA 检查均未启动，正式
  R001/R002 继续阻塞；文件不记录实际绝对路径或服务器身份。
- `dependency-inventory.20260719.attempt-002.json`：从成功解析的既有 runtime
  实测捕获的 193 项 Python distribution 名称/版本清单；排除 URL、安装来源、
  路径、凭据和机器身份，文件 SHA-256 由环境锁引用。
- `environment-lock.20260719.attempt-002.json`：attempt-002 的不可覆盖 runtime
  环境锁，记录 Python/PyTorch/PyTorch CUDA runtime、CUDA 可用性、GPU 数量与
  型号、cuDNN/NCCL，以及 dependency inventory 的相对路径和 SHA-256。该锁只
  证明 toy adapter 工程所需的环境 metadata 条件，不证明模型或数据 adapter。
- `runtime-preflight.20260719.attempt-002.json`：第二次只读 preflight 的不可覆盖
  PASS 快照，保留首次阻塞快照，不记录 executable 路径、URL、机器身份或 GPU
  UUID，也未执行训练、推理、benchmark、压测或 collective。
- `LOCKING_POLICY.md`：获批后另建不可变环境快照的规则。依赖版本未确认时不得
  写入虚构 lockfile。
