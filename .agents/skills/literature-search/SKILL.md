---
name: literature-search
description: 按主题、作者或 arXiv ID 查找论文，导入本地文献，管理选集并导出 CSV。适用于文献检索、已有文献清单整理和检索计划。
---

# 文献检索与清单管理

## 1. 选入口

| 用户给出的输入或目标 | 执行入口 |
| --- | --- |
| 研究主题、关键词或 arXiv ID | [search_papers.py](scripts/search_papers.py)。主题用 `--query`，已知 arXiv ID 用 `--query id:<ID>`。 |
| 作者名 | [search_by_author.py](scripts/search_by_author.py)。结合题目和合作者排除同名作者。 |
| 本地 PDF、DOCX、HTML 或文本 | [import_papers.py](scripts/import_papers.py)。解析 PDF 或 DOCX 前按 [依赖清单](requirements.txt) 安装库。 |
| 已有 `papers.json`，只需筛选、保存选集或导出 | 直接读 [清单操作](references/catalog.md)，使用本地文件。 |
| 用户只要检索策略 | [plan_search.py](scripts/plan_search.py)。已有兼容模型服务时，按服务配置 `OPENAI_API_KEY`、`MODEL_USE` 和可选的 `OPENAI_BASE_URL`。输出是检索计划。 |

## 2. 执行检索

1. 保留用户的主题、年份范围和来源要求。学术检索可从 arXiv 的预印本开始，需要更广覆盖时显式加入 `semantic_scholar`。其公共接口限流时，记录受影响的来源。
2. 用户要网页或新闻时，分别使用 `--mode general` 或 `--mode news`。这两种模式走 Tavily，需要 `TAVILY_API_KEY`。保留网页证据标签。
3. 有结果时复核主题相关性和重复记录，保留来源、标题、链接及完整 ID。只有读到结果后才按要求导出或保存选集。

示例在本 Skill 目录运行。将查询和输出目录替换为用户本次的输入。

```bash
python scripts/search_papers.py --query "all:perovskite" --sources arxiv --limit 5 --out-dir ./literature
python scripts/search_by_author.py --author "Shoucheng Zhang" --limit 3 --out-dir ./by-author
python scripts/export_csv.py --input ./literature/papers.json --output ./references.csv
```

## 3. 检查和交付

读取本次生成的 `papers.json` 和 `papers.csv`，报告实际命中数、所用来源和 `failures`。区分来源查询成功但无命中、部分来源失败和全部失败。无命中时检查检索语法，再按需扩大术语或换来源。
