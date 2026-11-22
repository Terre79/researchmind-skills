---
name: materials-search
description: 按化学组成查询 COD、OQMD、AFLOW 或 Materials Project，导出带来源的记录及可用 CIF，或按数据库内的指标排序。
---

# 材料数据库查询

## 适合用它做什么

- 从 COD 查实验晶体记录，或从 OQMD、AFLOW 和 Materials Project 查计算结构及已有材料性质。
- 导出可用于后续计算的 CIF，或按各来源已有的数值字段整理候选。

## 典型请求

- “从 COD 和 OQMD 各找两个硅结构，把能拿到的 CIF 下载给我。”
- “查 OQMD 的 NaCl 候选结构，在同一数据库内按形成能排序。”

## 你需要提供

使用 [Windows x64 CPU 完整 ZIP](https://github.com/Terre79/researchmind-skills/releases/tag/skills-win-cpu-v1)。完整包中的脚本使用同目录下的 `python/python.exe`，可从任意工作目录用绝对路径调用。源码目录部署方法见本节的依赖清单。

- 提供化学式，可选数据源及每个源的记录上限，然后指定输出目录。查询 Materials Project 需 `MP_API_KEY`。
- 从源码部署时安装 [依赖](requirements.txt)。公开数据库的实时查询需要联网。排名或解释数据库字段时查看 [来源与排序指标](references/sources.md)。

## 产出

- [search_materials.py](scripts/search_materials.py) 生成 `materials.json`，[recommend_materials.py](scripts/recommend_materials.py) 生成 `recommendations.json`。记录含 `source`、`source_id` 和可用元数据。
- 结构下载成功时，记录中的 `cif` 指向输出目录下的实际文件。按来源交付结果，并汇报 `failures` 和 `warnings`。

在本 Skill 目录执行：

```powershell
.\python\python.exe .\scripts\search_materials.py --formula Si --sources cod oqmd aflow --limit 2 --out-dir ./silicon
.\python\python.exe .\scripts\recommend_materials.py --formula NaCl --sources oqmd --limit 5 --out-dir ./ranked
```

## 边界

- 数据库结果可能只有记录和属性。缺 CIF 时说明原因，并保留仍有用的记录。单一来源失败时可使用其他成功来源。
- 排序在同一来源内解释。形成能和凸包距离应分别报告，查询结果覆盖范围以所选来源实际返回为准。
