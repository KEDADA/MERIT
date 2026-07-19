# data/

- **用途**：保存数据 manifest、sample-index 摘要、隔离证明与小型 synthetic fixture。
- **输入/输出**：输入为外部只读数据路径；输出为 partition 记录及零重叠检查。
- **命名规则**：`<phase>-<role>-<revision>.manifest.json`；partition ID 全局唯一。
- **Run ID 对应**：每个 run manifest 引用一个冻结 data manifest；pilot 与
  confirmatory 禁止引用同一 partition。
- **可提交**：README、manifest、schema、小型 synthetic fixture；真实数据不提交。
- **大文件**：raw/interim/processed 数据仅登记路径别名、字节数、SHA-256、
  sample-index SHA-256 和 manifest。

## 当前真实 toy split

- `real-toy-split.20260719.manifest.json` 登记 ALFWorld 官方 trajectory/TextWorld
  archives 和既有 HotpotQA-100 replay trace 的版本、许可、大小与 SHA-256；不含
  私有绝对路径。
- `indexes/real-toy-*.index.json` 只含不可逆 query ID、stream 和相对 source
  locator，不含问题、答案、observation、reward 或 trajectory payload。
- 每流先从可重放 common-support universe 按 seed `20260719` 的 SHA-256 顺序固定
  10 个 task，再按锁定规则做 7 TRAIN / 3 AUDIT；总计 14/6，重叠为 0。
- ALFWorld 真实 archives 保存在 repo 外数据区；HotpotQA 复用已有只读 trace。
  `validate_real_toy_data.py` 需要调用者显式提供本地源路径，manifest 永不记录它们。
- 当前只开放 data engineering；原子 run manifest、模型 revision 绑定和正式
  R001/R002 仍为 BLOCKED。
