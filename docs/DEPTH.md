# 政务统计小样本抑制与汇总保护检查 深度登记

使用者：政务统计发布审核员。核心规则：小于阈值的单元格主抑制，再为每条行列合计约束补充次抑制，避免单个隐值被减法还原；抑制代价按权重确定且结果可复算。

## 功能模块
| 模块 | 使用者动作 | 入口 | 核心文件 | 测试 |
|---|---|---|---|---|
| M1 底表采信 | 执行底表采信并复核证据 | `GET /intake` `POST /api/intake` | `app/modules/m1_intake/service.py` `app/modules/m1_intake/rules.py` | `tests/test_intake.py` |
| M2 发布契约 | 执行发布契约并复核证据 | `GET /contract` `POST /api/contract` | `app/modules/m2_contract/service.py` `app/modules/m2_contract/rules.py` | `tests/test_contract.py` |
| M3 汇总建模 | 执行汇总建模并复核证据 | `GET /model` `POST /api/model` | `app/modules/m3_model/service.py` `app/modules/m3_model/rules.py` | `tests/test_model.py` |
| M4 抑制求解 | 执行抑制求解并复核证据 | `GET /calculate` `POST /api/calculate` | `app/modules/m4_calculate/service.py` `app/modules/m4_calculate/rules.py` | `tests/test_calculate.py` |
| M5 质量隔离 | 执行质量隔离并复核证据 | `GET /quarantine` `POST /api/quarantine` | `app/modules/m5_quarantine/service.py` `app/modules/m5_quarantine/rules.py` | `tests/test_quarantine.py` |
| M6 泄露复核 | 执行泄露复核并复核证据 | `GET /reconcile` `POST /api/reconcile` | `app/modules/m6_reconcile/service.py` `app/modules/m6_reconcile/rules.py` | `tests/test_reconcile.py` |
| M7 发布归档 | 执行发布归档并复核证据 | `GET /batches` `POST /api/batches` | `app/modules/m7_batches/service.py` `app/modules/m7_batches/rules.py` | `tests/test_batches.py` |

## 陷阱登记
| TRAP | 现象 | 朴素实现 | 处理 | 位置 | 测试 |
|---|---|---|---|---|---|
| TRAP-01 | 历史编码 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m1_intake/rules.py` | `tests/test_intake.py::test_gb18030_sample` |
| TRAP-02 | BOM表头 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m1_intake/rules.py` | `tests/test_intake.py::test_bom_sample` |
| TRAP-06 | 数字归一 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m2_contract/rules.py` | `tests/test_contract.py::test_fullwidth_thousands` |
| TRAP-07 | 缺失哨兵 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m2_contract/rules.py` | `tests/test_contract.py::test_sample_missing_not_zero` |
| TRAP-08 | 编码保形 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m2_contract/rules.py` | `tests/test_contract.py::test_sample_leading_zero` |
| TRAP-14 | 重复异值 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m3_model/rules.py` | `tests/test_model.py::test_sample_conflicts_isolated` |
| TRAP-18 | 空态区分 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m1_intake/rules.py` | `tests/test_intake.py::test_empty_three_states` |
| TRAP-19 | 规则优先级 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m3_model/rules.py` | `tests/test_model.py::test_shuffle_equivalent` |
| TRAP-21 | 双向汇总 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/modules/m3_model/rules.py` | `tests/test_model.py::test_source_total_mismatch` |
| TRAP-26 | 陈旧版本 | 直接转换或覆盖产生误判 | 按数据字典处理并保留来源证据 | `app/store.py` | `tests/test_batches.py::test_sample_stale_review` |

## 对账规则
底表总数=行汇总=列汇总；所有发布等式不能只含一个隐藏单元格

## 已知不覆盖
不覆盖跨发布期差分攻击、外部辅助信息与基于非负界限的区间推断；检查范围为当前二维表公开行列合计下的精确线性还原。

## 证据
每个事件保留CSV逻辑记录结束行号与原值；隔离记录附原因码。运行摘要包含输入SHA256、规则版本、参数和耗时。持久化为单次事务；重复输入复用运行ID。
