# 熊旭 · 数据作品集 (data-portfolio)

> 用途：求职展示（数据分析 / 数据运营实习生）。证明「原始数据 → 清洗 → 分析 → 结论」全链路能独立跑通。
> 对应简历占位：个人优势里的「作品集」链接填本仓库地址。

## 仓库结构
```
data-portfolio/
├─ README.md                # 本文件（总览）
├─ index.html               # 作品集展示页（本地预览 / GitHub Pages）
└─ projects/
   └─ 01_ecommerce_sales/   # 项目 01：电商销售分析
      ├─ README.md
      ├─ raw/               # 原始数据（脏）
      ├─ clean/             # 清洗后数据 + SQLite 数据库
      ├─ analysis/          # Python / R 分析脚本
      └─ output/            # 图表 + 结论
```

## 添加新项目的规范
每个项目一个文件夹，命名 `NN_主题`，统一分层 `raw / clean / analysis / output`，
必须包含：
1. 一份 `README.md`（业务问题 / 方法 / 发现 / 图表）
2. 至少 1 张图 + 1 句话结论 + 1 条可落地建议
3. 可复现脚本（Python 或 R）

## 里程碑（建议）
- [x] 项目 01：电商销售分析（脚手架）
- [ ] 项目 02：（楚超科研数据 / 武汉公开数据 / 家乡旅游，待定）
- [ ] 项目 03：（按岗位 JD 补一个对标方向）
- [ ] 推 GitHub + 绑定简历链接 + 配置 GitHub Pages 展示页

## 本地预览展示页
```bash
python -m http.server 8000   # 浏览器打开 http://localhost:8000
```
