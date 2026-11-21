---
name: materials-search
description: 按化学组成查询 COD、OQMD、AFLOW 或 Materials Project，导出带来源的材料记录及可用 CIF。适用于寻找已有晶体结构和按数据库指标排序。
---

# 材料数据库查询

## 1. 确定来源与目标

- 要实验晶体记录，选 COD。要计算结构或能量字段，选 OQMD、AFLOW 或 Materials Project。用户指定来源时按其要求执行。启用 Materials Project 前确认已配置 `MP_API_KEY`。
- 要下载现有结构，用 [search_materials.py](scripts/search_materials.py)。要按已有性质筛选候选，用 [recommend_materials.py](scripts/recommend_materials.py) 并按来源解读排序。
- 需要解释形成能、凸包距离、缺失值或 AFLOW 查询限制时，再读 [数据源与排序指标](references/sources.md)。

## 2. 执行

在本 Skill 目录运行 `python -m pip install -r requirements.txt`。传入用户指定的化学式，`--limit` 对每个数据源分别生效。以下以硅为例。

```bash
python scripts/search_materials.py --formula Si --sources cod oqmd aflow --limit 2 --out-dir ./silicon
python scripts/recommend_materials.py --formula Si --sources oqmd --limit 5 --out-dir ./ranked
```

## 3. 检查和交付

1. 读 `materials.json` 或 `recommendations.json`，核对 `formula`、实际记录数量及每条的 `source`、`source_id`。
2. 逐条对照 `cif` 字段与实际文件。只有记录却缺 CIF 时，保留记录并说明导出失败原因。跨数据库的能量指标分别解读。
3. 报告 `failures` 和 `warnings`。来源不可用时交付其他来源的结果；所有源均无命中时，说明已查询的组成与来源。
