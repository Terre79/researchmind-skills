---
name: literature-search
description: 按主题、作者或 arXiv ID 检索文献，导入本地论文，筛选、选择和导出文献清单。适用于找论文、整理检索结果或生成检索计划。
---

## 选择检索方式

- 用户给主题或 arXiv ID 时运行 `scripts/search_papers.py`。arXiv 适合预印本；如需扩展覆盖，加入 Semantic Scholar。混合来源时保留来源标签，合并前核对 DOI、URL 或论文 ID。
- 用户给作者时运行 `scripts/search_by_author.py`；检查作者和研究方向，避免把同名作者的论文合在一起。
- 给了本地 PDF、DOCX、HTML 或文本时运行 `scripts/import_papers.py`。给了已有清单时直接运行 `scripts/filter_papers.py`，可按主题或论文 ID 筛选。
- 用户明确要新闻或网页时使用 `--mode news` 或 `--mode general`，需要 `TAVILY_API_KEY`。网页摘要应标成网页证据。

## 执行

```bash
python scripts/search_papers.py --query "all:perovskite" --sources arxiv --limit 5 --out-dir ./literature
python scripts/search_by_author.py --author "Shoucheng Zhang" --limit 3 --out-dir ./by-author
python scripts/filter_papers.py --input ./literature/papers.json --topic "all:perovskite" --out-dir ./selected
python scripts/export_csv.py --input ./selected/papers.json --output ./selected/references.csv
```

arXiv 查询、筛选与 CSV 导出可直接用标准库执行。解析已下载的 PDF 或 DOCX 时，安装 `requirements.txt`。要生成检索计划，使用 `scripts/plan_search.py --query … --out-dir …`，配置 `OPENAI_API_KEY`、`MODEL_USE`，可用 `OPENAI_BASE_URL` 指向兼容服务。

## 检查结果

检查 JSON 的 `paper_count`、`failures` 及实际文件。分享论文时至少给标题、链接、来源和可用年份。空结果时先检查查询语法，再调整术语或数据源。选集和批量操作见 [清单操作](references/catalog.md)。
