---
name: paper-analysis
description: 下载、提取、分段阅读和分析指定论文，给出方法、结论及局限。适用于论文精读、批量正文提取和针对原文的证据核对。
---

# 论文读取与分析

## 1. 根据输入选路径

- **现有文本**。直接用 [read_segment.py](scripts/read_segment.py) 分段，或用 [find_in_text.py](scripts/find_in_text.py) 定位字面关键词。已有文本可离线读，字符偏移以 Unicode 字符计。
- **单篇本地文档**。使用 [extract_text.py](scripts/extract_text.py) 的 `--input`。仅收到公开下载 URL 时，先用 [download_paper.py](scripts/download_paper.py) 的 `--url` 和 `--output` 保存，再做本地提取。
- **已有论文清单**。使用 `extract_text.py --papers`，可用 `--paper-id` 指定一个或多个 ID。必须拿到正文时加 `--require-fulltext`。提取结果可能包含正文、摘要或节选，逐篇检查 `evidence`。
- **需要分析**。把提取后的清单交给 [analyze_paper.py](scripts/analyze_paper.py)，按用户问题设置 `--instruction`。只要求下载、提取或定位时，到对应产物为止。

## 2. 执行

提取 PDF 或 DOCX 前，在该 Skill 目录运行 `python -m pip install -r requirements.txt`。模型分析使用配置好的 `OPENAI_API_KEY`、`MODEL_USE` 和可选的 `OPENAI_BASE_URL`。

```bash
python scripts/extract_text.py --input ./paper.pdf --out-dir ./evidence
python scripts/read_segment.py --input ./evidence/paper.txt --start 0 --length 1200
python scripts/find_in_text.py --input ./evidence/paper.txt --term "limitations" --limit 5
python scripts/analyze_paper.py --papers ./evidence/papers.json --instruction "结合原文说明方法、主要发现与局限" --out-dir ./analysis
```

批量提取的文本路径以 `papers.json` 的 `content_file` 为准。连续阅读时按 `next_start` 继续，直到 `has_more` 为假。

## 3. 检查和交付

分析时读取 `analysis.json` 检查论文 ID、证据级别、`truncated` 和逐篇失败，再交付 `analysis.md` 或 `analysis.csv`。需要引用具体方法或数值时，回到相关文本核对。只有摘要、原文截断或部分论文无法获取时，在相关结论旁说明具体证据范围。
