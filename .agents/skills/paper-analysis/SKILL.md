---
name: paper-analysis
description: 下载和读取论文，提取正文、按字符分段或查找关键词，并围绕方法、结果和局限分析论文。适用于精读、批量证据提取和论文对比。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

## 获取证据

给了 URL 时用 `scripts/download_paper.py --url … --output paper.pdf`。给了本地文件时，用 `extract_text.py --input …`。给了文献清单时，用 `--papers …` 加 `--paper-id` 选择论文。要求完整正文时加 `--require-fulltext`，并检查 `evidence` 字段。

```bash
python scripts/extract_text.py --input ./paper.pdf --out-dir ./evidence
python scripts/read_segment.py --input ./evidence/paper.txt --start 0 --length 1200
python scripts/find_in_text.py --input ./evidence/paper.txt --term "limitations" --limit 5
```

## 跑分析

配置 `OPENAI_API_KEY` 和 `MODEL_USE`。本地兼容服务使用 `OPENAI_BASE_URL`。

```bash
python scripts/analyze_paper.py --papers ./evidence/papers.json --instruction "说明方法、主要发现与局限" --out-dir ./analysis
```

检查 `analysis.md`、`analysis.csv` 和 `analysis.json` 中的论文 ID、证据级别和截断字段。正文证据不足时，说明哪些判断只用到了摘要或节选。
