---
name: materials-search
description: 按化学组成查询 COD、OQMD、AFLOW 或 Materials Project，导出带来源的材料记录和 CIF。适用于查找实验或计算结构，以及按同来源指标排序。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

## 查询材料

- 查实验 CIF 时先选 COD。查计算条目时用 OQMD、AFLOW 或 Materials Project。Materials Project 需要 `MP_API_KEY`。
- 根据用户输入的化学组成调用查询。需要按已有性质选候选时运行 `recommend_materials.py`，检查各来源采用的指标及缺失项。

```bash
python scripts/search_materials.py --formula Si --sources cod oqmd aflow --limit 2 --out-dir ./silicon
python scripts/recommend_materials.py --formula Si --sources oqmd --limit 5 --out-dir ./ranked
```

检查 `materials.json` 或 `recommendations.json` 的记录数量、数据库 ID、`failures` 和 `warnings`。使用 `structures/` 内实际输出的 CIF。数据源语义见 [来源说明](references/sources.md)。
