---
name: research-report
description: 根据用户选定的论文或提取后的证据生成带来源的研究报告，核对引用 ID 和证据范围。适用于已有文献集的综述与证据汇总。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

准备一个包含 `papers` 数组的 JSON 文件。每条记录有 `paper_id` 和标题，证据来自相对该清单的 `content_file`、公开 `pdf_url` 或 `abstract`。选定关键论文，核对每条来源和证据级别。让用户配置 `OPENAI_API_KEY`、`MODEL_USE` 及可选 `OPENAI_BASE_URL`。

```bash
python scripts/write_report.py --papers ./evidence/papers.json --topic "钙钛矿电荷有序" --out-dir ./report
```

用 `--paper-id` 指定子集，`--max-characters` 控制总证据字符数。交付 `report.md` 和 `report.json`。查看后者的引用、证据标签和截断状态，并对照原文核查关键事实。单篇报告在页首标明原论文来源。多篇报告需要至少一个可追溯的正文引用。遇到未知引用 ID 时，脚本报错。
