# scripts/

- **用途**：提供人工可审计的薄入口；当前仅包含骨架静态校验。
- **输入/输出**：输入为 repo 内配置和 manifest；输出为终端校验摘要。
- **命名规则**：`validate_*.py` 为只读检查；未来执行脚本须显式带 `R###`。
- **Run ID 对应**：当前脚本不执行任何 run；未来脚本必须接收而非生成 run ID。
- **可提交**：短小入口脚本和说明；临时日志、锁文件、PID 不提交。
- **大文件**：日志与原始输出只写外部存储，并登记 SHA-256/manifest。

`validate_skeleton.py` 仅使用 Python 标准库：解析全部 JSON，检查 pending 接口、
证据 SHA-256、pilot/confirmatory 隔离、私有路径、疑似凭据和文件大小。它不会
导入 PyTorch、访问 GPU、安装依赖或启动 run。

该校验还验证模型 adapter 合同对 attempt-002 环境锁的 SHA-256 引用，并强制其
只开放 engineering readiness；该历史合同中的后续 gate 不被原地改写。当前数据
readiness 由更新的 real-toy manifest 单独声明，正式 run 仍保持阻塞。

`prepare_real_toy_split.py` 从调用者显式提供的 ALFWorld archives 和 HotpotQA
trace 生成 content-free sample indexes，使用 exclusive-create 防止覆盖。
`validate_real_toy_data.py` 重算 source SHA-256、common-support selection 与 7:3
split，并实际解析全部 20 个入选 task 的 replay 结构；它不运行任务或调用模型。

`capture_dirty_worktree.py` 以 exclusive-create 生成未暂存工作树的内容清单，不做
git add/commit；`validate_atomic_run_inputs.py` 重算 dirty 清单及 R001/R002 的全部
repo 内输入引用，强制两个 run 保持 BLOCKED 且无输出。

`validate_sanity_components.py` 对 CCC/SR/CTI、split、neutral-pad 和 paired replay
做 deterministic CPU-only smoke check。其成功输出明确记录正式 run、GPU 和模型
调用均为 0，不能替代 R001/R002 run manifest。

`preflight_runtime.py` 从已脱敏的 R000 profile、显式临时引用和现有离线 runtime
registry 中解析已批准 runtime，只输出安全的版本/设备计数或规范化阻塞原因，
绝不回显 executable 私有路径。候选必须与锁定的 Python/PyTorch/CUDA runtime
metadata 精确匹配。`--capture` 仅以 exclusive-create 方式生成固定 attempt-002
的 dependency inventory、环境锁和 preflight 快照；目标文件存在时拒绝覆盖。
它不安装或下载资源，也不做训练、模型推理、benchmark、GPU 压测或 collective。
