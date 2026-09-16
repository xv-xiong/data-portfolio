# 项目 01 · 电商销售数据分析

> 状态：脚手架已完成，可运行 ✅ ｜ 数据：示例脏数据（待替换为真实 Kaggle 数据集）

## 业务问题
基于一份电商订单数据，识别销售趋势、品类与区域表现，定位可优化的运营方向。

## 数据链路
`raw/orders_raw.csv`（脏） → `clean/orders_clean.csv`（净） → `analysis/`（Python + R） → `output/`（图表 + 结论） → `clean/portfolio.db`（SQLite）

## 清洗规则（已在脚本实现）
- 去重、统一 region 大小写与空格
- 丢弃缺失关键字段、quantity≤0、非法日期、退款订单
- 计算 amount = quantity × unit_price

## 产出
- 月度销售额趋势图（`output/sales_trend.png`）
- 结论与建议（`output/findings.md`）
- SQLite 数据库 `clean/portfolio.db`（表 `orders_clean`）

## 怎么跑
```bash
python analysis/clean_and_analyze.py     # 生成所有产出
# R 版（需本地 R + tidyverse）：Rscript analysis/clean_and_analyze.R
```

## 换成真实数据
把 `raw/orders_raw.csv` 换成你的 Kaggle 数据集（如 Online Retail / 某电商订单），
按实际字段调整脚本顶部的列名即可。推荐用 Kaggle CLI 拉取：
```bash
kaggle datasets download -d <owner/dataset> -p raw --unzip
```
