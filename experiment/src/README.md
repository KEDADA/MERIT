# src/

- **用途**：实现 manifest、配置快照、状态、失败分类和角色隔离的最小公共机制。
- **输入/输出**：读取 JSON 配置/manifest，输出校验结果或不可变快照。
- **命名规则**：Python 包为 `merit_experiment`，模块和函数使用 snake_case。
- **Run ID 对应**：公共代码服务所有 `R###`，不得硬编码某个正式 run 的参数。
- **可提交**：源码、类型定义和小型模板；运行缓存与生成代码不得提交。
- **大文件**：源码不承载模型/数据；大型依赖只记录 lockfile 和 digest。

当前 `validation.py` 还校验 runtime 候选、baseline fidelity 和六项 pilot 实现
接口。校验器只检查结构、证据引用与阻塞不变量，不下载依赖，也不宣称任何实现
已具备运行能力。

R001/R002 工程组件均只依赖 Python 标准库：

- `baselines.py`：明确标为非 exact-fidelity 的 standardized credit wrapper；
- `replay.py` / `budget.py` / `neutral_pad.py`：配对 seed、严格 provenance reuse、
  原子预算准入和 token-ID 长度匹配；
- `sampling.py`：固定 70:30 split 与 TRAIN-only priority 基础函数；
- `metrics.py` / `bootstrap.py`：CCC、CI-decided SR@k、CTI、OLS、Holm 和
  task-clustered BCa。
- `model_adapter.py`：显式 model/tokenizer/decoding/seed provenance 的 token-ID
  adapter，以及只接收已加载组件的惰性 Transformers backend。模块导入和对象
  构造不加载、下载或调用模型；当前测试只使用注入式标准库假后端。
- `data_adapter.py`：只读索引 ALFWorld trajectory/game archive 交集与 HotpotQA
  replay JSONL；选择前不加载 outcome/reward payload，固定 real-toy universe 后
  复用锁定的 task-level 70:30 split。源 locator 与 query hash 全程 fail-closed。
- `provenance.py`：通过 Git porcelain 只读枚举 dirty paths，对普通文件内容和
  symlink 相对 target 分别计算 SHA-256；显式排除自引用 atomic envelopes，并拒绝
  rename/copy 等未定义状态。
