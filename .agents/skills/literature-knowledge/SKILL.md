---
name: literature-knowledge
description: 为已有论文正文或摘要建立持久化语义索引，按问题检索能追溯到论文 ID 和字符位置的片段。适用于在特定文献集合中定位证据。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

准备论文清单，确保 `paper_id` 与保存文本或论文链接一致。配置 `GOOGLE_API_KEY`，或者同时设置 `OPENAI_API_KEY`、`OPENAI_EMBEDDING_MODEL` 及可选的 `OPENAI_BASE_URL`。索引和查询使用相同的服务、模型、目录、集合名和分段大小。若嵌入服务限制输入长度，在索引和查询两边使用相同的 `--chunk-size`。

```bash
python scripts/index_papers.py --papers ./evidence/papers.json --index-dir ./index --collection perovskites
python scripts/search_knowledge.py --index-dir ./index --collection perovskites --query "二维电荷有序有哪些证据" --top-k 5 --output ./matches.json
```

核对命中项的 `paper_id`、`evidence`、`source` 和字符范围。用返回片段定位原文。距离用于检索排序；报告中的结论需要查阅相关文本。
