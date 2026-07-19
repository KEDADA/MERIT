# 环境锁定策略

1. `baseline.json` 只记录 R000 已确认事实，不把驱动报告的 CUDA 版本等同于
   任意未验证 toolkit，也不推断模型可运行性。
2. 项目 runtime 目标已锁定为 R000 观察栈，安装策略锁定为本阶段只使用现有环境；
   dependency lock 仍是必须从可解析 runtime 实测捕获的事实。不得安装依赖或生成
   虚假 lockfile。
3. 锁定时同时记录 Python、框架、CUDA runtime、关键库、系统包、容器 digest
   和生成命令；任何变化产生新版本，禁止覆盖历史快照。
4. run manifest 必须引用环境 snapshot 的相对路径和 SHA-256。
5. 模型与数据缓存不进 Git，只在 manifest 中记录路径别名、内容 SHA-256、大小
   和生成/获取方式。路径别名不得包含机器私有绝对路径。
6. `runtime-designation.pending.json` 永久作为待决接口；项目 runtime、依赖锁和
   安装来源获批后，应创建新的 `environment-<date>-<revision>.*` 快照并记录
   pending 文件与 R000 基线的 SHA-256，不得原地把 pending 状态改成 READY。
7. runtime preflight 只验证版本、依赖锁一致性和设备可见性；它不是 benchmark、
   GPU 压测或模型容量证明。preflight 未全部通过前，R001/R002 保持阻塞。
8. 用户批准 runtime 目标不等于批准实测结果。`NOT_CAPTURED` 和 `NOT_RUN` 必须由
   后续只读 preflight 的真实输出写入新的环境快照，禁止在目标锁中手填通过。
9. dependency inventory 只允许记录隔离 runtime 实际可见的规范化 package name
   和 version；不得写入 direct URL、index、安装源、绝对路径、凭据或机器身份。
   inventory 与环境锁必须分别记录文件 SHA-256，并以 exclusive-create 生成新
   revision。metadata PASS 只开放真实 toy adapter 工程，不开放正式 R001/R002。
