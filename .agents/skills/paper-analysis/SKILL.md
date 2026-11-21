---
name: paper-analysis
description: 下载、提取和阅读指定论文，定位原文段落，或分析论文的方法、发现与局限。适用于单篇精读和批量论文证据提取。
---

# 论文读取与分析

## 适合用它做什么

- 下载公开论文，提取单篇或多篇文件的可读文本。
- 从已有文本定位关键词或按字符分段阅读。需要解读时，围绕用户问题分析论文。

## 典型请求

- “提取这篇 PDF 的文字，定位作者谈实验局限的位置。”
- “比较这三篇论文的方法，并指出哪些结论有全文证据。”
- “从上次读到的字符位置继续读 1200 字。”

## 你需要提供

- 提供本地文档、公开下载 URL、已提取文本或论文清单。批量处理时可给论文 ID；必须取得全文时说明。
- 分析时提供问题和输出语言。用兼容模型服务配置 `OPENAI_API_KEY`、`MODEL_USE` 及可选的 `OPENAI_BASE_URL`。PDF 和 DOCX 提取需安装 [依赖](requirements.txt)。

## 产出

- [download_paper.py](scripts/download_paper.py) 保存公开文档。[extract_text.py](scripts/extract_text.py) 输出文本和 `papers.json`；批量文本路径以各条记录的 `content_file` 为准。要求全文时用 `--require-fulltext`。
- [read_segment.py](scripts/read_segment.py) 返回文本和 `next_start`；[find_in_text.py](scripts/find_in_text.py) 返回字面匹配和偏移。[analyze_paper.py](scripts/analyze_paper.py) 生成 `analysis.md`、`analysis.csv` 和 `analysis.json`。

在本 Skill 目录执行：

```bash
python scripts/extract_text.py --input ./paper.pdf --out-dir ./evidence
python scripts/read_segment.py --input ./evidence/paper.txt --start 0 --length 1200
python scripts/find_in_text.py --input ./evidence/paper.txt --term "limitations" --limit 5
python scripts/analyze_paper.py --papers ./evidence/papers.json --instruction "说明方法、发现和局限" --out-dir ./analysis
```

## 边界

- 分段偏移按 Unicode 字符计算。已有文本的定位与分段可离线执行。
- 核对 `evidence`、`truncated` 和逐篇失败。只有摘要、节选或截断文本时，结论限于实际取得的内容。引用关键数字前回到原文核对。
