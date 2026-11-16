# 政务统计小样本抑制与汇总保护检查

供政务统计发布审核员核对缺失计数与零混淆、同编码异名、合计矛盾、单隐值泄露等数据问题。小于阈值的单元格主抑制，再为每条行列合计约束补充次抑制，避免单个隐值被减法还原；抑制代价按权重确定且结果可复算。

## 启动

```sh
docker compose up --build -d
```

访问 [工作台](http://localhost:18207/)，无需准备文件即可运行。

## 演示

1. 进入采信模块，选脏样例并运行。
2. 逐模块核对来源行、业务结果与隔离原因。
3. 切换干净样例比较差异；重复运行相同输入复用批次。
4. 对账通过后进入归档模块复核，可下载抑制后的发布CSV。

## 模块与入口

- 底表采信：`/intake`，`GET/POST /api/intake`。
- 发布契约：`/contract`，`GET/POST /api/contract`。
- 汇总建模：`/model`，`GET/POST /api/model`。
- 抑制求解：`/calculate`，`GET/POST /api/calculate`。
- 质量隔离：`/quarantine`，`GET/POST /api/quarantine`。
- 泄露复核：`/reconcile`，`GET/POST /api/reconcile`。
- 发布归档：`/batches`，`GET/POST /api/batches`。

[接口文档](http://localhost:18207/docs)。

## 验证

```sh
docker compose config --quiet
docker compose exec -T app pytest -q
```

## 数据与定义

输入为完整地区×类别矩阵，count为非负人数，0是有效计数，缺失不等于0。0<count<阈值为主抑制；在完整二分图上按最小边际权重寻找替代路径，使每条隐藏边进入环，并以桥边检测核对线性可还原风险。选择过程确定性，使用贪心补环，不宣称全局最优。行列源合计必须与复算一致。发布CSV只包含抑制后的值，结构或保护检查失败时禁止导出。

定义见 `docs/DATA-DICTIONARY.md`，模块和测试映射见 `docs/DEPTH.md`。样例位于 `sample_data/`。SQLite存放于命名卷，重启保留批次。确认不再需要历史记录时，可用 `docker compose down -v` 重建数据。

## 已知范围

不覆盖跨发布期差分攻击、外部辅助信息与基于非负界限的区间推断；检查范围为当前二维表公开行列合计下的精确线性还原。

计数与代价上限为1000000000000，极值返回字段错误；同一cell_id不得指向不同地区与类别。
