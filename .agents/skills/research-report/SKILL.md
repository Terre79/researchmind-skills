---
name: research-report
description: 根据选定论文生成带出处的简明研究报告，检查引用 ID、证据级别和覆盖范围。适用于已有文献集的综述、证据汇总和研究简报。
---

# 基于文献生成研究报告

## 1. 确定报告范围

使用用户指定的主题、语言和论文范围。已有论文清单时直接复用。清单包含 `papers` 数组，保留原始 `paper_id`、标题和可用链接。证据可来自 `content_file`、公开 `pdf_url` 或 `abstract`，相对 `content_file` 路径从清单所在目录解析。只分析选定论文时用 `--paper-id` 指定，省略该参数会使用清单里的全部论文。

## 2. 生成草稿

在本 Skill 目录运行 `python -m pip install -r requirements.txt`。用已配置的 `OPENAI_API_KEY`、`MODEL_USE` 和可选 `OPENAI_BASE_URL` 运行 [write_report.py](scripts/write_report.py)。

```bash
python scripts/write_report.py --papers ./evidence/papers.json --topic "层状钙钛矿的电荷有序证据" --language Chinese --out-dir ./report
```

脚本生成简报。主题过宽时，按用户关注的问题缩小论文范围。`--max-characters` 是所有论文合计的证据字符预算。设置前结合论文数量和模型上下文，查看结果里哪些论文被截断。

## 3. 核对引用并交付

1. 查看 `report.json` 中的 `citations`、`evidence`、`failures` 和 `warnings`。单篇报告在正文前标明来源，多篇报告的正文包含可追溯论文 ID。
2. 把关键结论对照实际引用的段落。脚本校验引用 ID，证据是否支持具体结论需要对照原文。资料只含摘要或节选时保留证据限制。
3. 交付 `report.md`；需要复核来源或模型输出状态时附 `report.json`。引用无效时，根据报错核对选集、原始 ID 和模型输出。
