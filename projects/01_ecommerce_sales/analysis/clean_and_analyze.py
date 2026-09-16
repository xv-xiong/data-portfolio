# -*- coding: utf-8 -*-
"""
01_ecommerce_sales —— 数据分析脚手架（Python 版）
链路：原始脏数据 -> 清洗 -> 多维分析 -> 图表 + 结论 + SQLite 数据库

运行：
    python analysis/clean_and_analyze.py
依赖：
    pandas, matplotlib

说明：
    - 首次运行会在 raw/ 自动生成一份「带脏数据」的示例订单表，方便你直接看到清洗效果。
    - 想换成真实 Kaggle 数据集时，把 raw/orders_raw.csv 替换成你的文件，
      并相应调整下面 CLEAN_RULES 里的字段名即可。
"""
import os
import random
from datetime import date, timedelta

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 无界面环境出图
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "raw", "orders_raw.csv")
CLEAN = os.path.join(BASE, "clean", "orders_clean.csv")
DB = os.path.join(BASE, "clean", "portfolio.db")
OUT = os.path.join(BASE, "output")
FIG = os.path.join(OUT, "sales_trend.png")
FIND = os.path.join(OUT, "findings.md")

os.makedirs(os.path.dirname(RAW), exist_ok=True)
os.makedirs(os.path.dirname(CLEAN), exist_ok=True)
os.makedirs(OUT, exist_ok=True)

random.seed(42)

# ---------------------------------------------------------------------------
# 1) 生成示例脏数据（仅当 raw 不存在时）
# ---------------------------------------------------------------------------
def make_raw():
    regions = ["north", "North", "NORTH", "south ", "South", "east", "East", "west"]
    cats = ["数码", "家居", "服饰", "美妆", "食品"]
    prods = {
        "数码": ["无线耳机", "机械键盘", "移动电源"],
        "家居": ["收纳盒", "台灯", "抱枕"],
        "服饰": ["T恤", "卫衣", "牛仔裤"],
        "美妆": ["面膜", "口红", "精华"],
        "食品": ["坚果", "咖啡", "巧克力"],
    }
    start = date(2025, 1, 1)
    rows = []
    oid = 1000
    for i in range(600):
        d = start + timedelta(days=random.randint(0, 240))
        cat = random.choice(cats)
        prod = random.choice(prods[cat])
        region = random.choice(regions)
        qty = random.randint(1, 8)
        price = round(random.uniform(20, 600), 2)
        status = "paid" if random.random() > 0.1 else "refunded"
        rows.append([oid, d.isoformat(), f"C{random.randint(1,80):03d}",
                     region, cat, prod, qty, price, status])
        oid += 1
    df = pd.DataFrame(rows, columns=[
        "order_id", "order_date", "customer_id", "region",
        "category", "product", "quantity", "unit_price", "status"])
    # 注入脏数据
    df.loc[10:14, "unit_price"] = None            # 缺失单价
    df.loc[20:25, "quantity"] = 0                 # 无效数量
    df.loc[30:33, "region"] = " east "            # 多余空格
    df = pd.concat([df, df.iloc[40:45]], ignore_index=True)  # 重复行
    df.loc[50, "order_date"] = "2025/13/40"       # 非法日期
    df.to_csv(RAW, index=False, encoding="utf-8-sig")
    print(f"[生成] 原始脏数据 -> {RAW}  ({len(df)} 行)")

if not os.path.exists(RAW):
    make_raw()

# ---------------------------------------------------------------------------
# 2) 清洗
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
n0 = len(df)

df["region"] = df["region"].str.strip().str.title()          # 去空格 + 统一大小写
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# 清洗规则：去重、去缺失关键字段、去无效数量、去非法日期、只保留已支付
df = df.drop_duplicates()
df = df.dropna(subset=["order_id", "order_date", "quantity", "unit_price"])
df = df[df["quantity"] > 0]
df = df[df["status"].str.strip().str.lower() == "paid"]

df["amount"] = (df["quantity"] * df["unit_price"]).round(2)
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
df = df.sort_values("order_date")

df.to_csv(CLEAN, index=False, encoding="utf-8-sig")
print(f"[清洗] {n0} -> {len(df)} 行  (去重/缺失/无效/非法日期/退款)")

# ---------------------------------------------------------------------------
# 3) 分析
# ---------------------------------------------------------------------------
monthly = df.groupby("order_month")["amount"].sum().round(2)
by_cat = df.groupby("category")["amount"].sum().sort_values(ascending=False).round(2)
by_region = df.groupby("region")["amount"].sum().sort_values(ascending=False).round(2)
top_prod = df.groupby("product")["amount"].sum().sort_values(ascending=False).head(5).round(2)

peak_month = monthly.idxmax()
peak_val = monthly.max()
top_cat = by_cat.index[0]

findings = f"""# 分析结论（自动生成模板，请按需改写）

## 一句话结论
{peak_month} 销售额最高（¥{peak_val:,.0f}），「{top_cat}」品类贡献最大，是后续重点运营方向。

## 关键发现
- 月度销售额峰值出现在 **{peak_month}**，整体呈波动上升趋势。
- 品类销售额排名：{', '.join(f'{c} ¥{v:,.0f}' for c, v in by_cat.items())}。
- 区域销售额排名：{', '.join(f'{r} ¥{v:,.0f}' for r, v in by_region.items())}。
- Top5 商品：{', '.join(f'{p} ¥{v:,.0f}' for p, v in top_prod.items())}。

## 可落地建议
- 在峰值月前 2 周对「{top_cat}」品类加大投放与备货，承接需求高峰。
- 对低贡献区域做定向召回活动，缩小区域间销售差距。
"""
with open(FIND, "w", encoding="utf-8") as f:
    f.write(findings)
print(f"[产出] 结论 -> {FIND}")

# ---------------------------------------------------------------------------
# 4) 图表
# ---------------------------------------------------------------------------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly.index, monthly.values, marker="o", color="#1f4e79", linewidth=2)
ax.set_title("月度销售额趋势", fontsize=13, color="#1f4e79")
ax.set_ylabel("销售额 (¥)")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIG, dpi=120)
plt.close(fig)
print(f"[产出] 图表 -> {FIG}")

# ---------------------------------------------------------------------------
# 5) 导出 SQLite（你真正"拥有"的数据库）
# ---------------------------------------------------------------------------
try:
    import sqlite3
    con = sqlite3.connect(DB)
    df.drop(columns=["order_month"]).to_sql(
        "orders_clean", con, if_exists="replace", index=False)
    con.close()
    print(f"[产出] 数据库 -> {DB}  (表 orders_clean, {len(df)} 行)")
except Exception as e:
    print(f"[跳过] SQLite 导出失败: {e}")

print("\n完成。下一步：用 R 模板 analysis/clean_and_analyze.R 复刻，或把 raw 换成真实 Kaggle 数据。")
