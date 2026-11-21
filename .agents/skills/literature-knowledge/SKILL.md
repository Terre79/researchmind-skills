---
name: literature-knowledge
description: 对已有论文正文或摘要建立持久化语义索引，并检索带论文 ID、来源和字符位置的片段。适用于已知文献集合中的证据定位。
---

# 文献语义索引与检索

## 1. 判断是否需要建索引

- 已有可用索引且只要求查找证据时，直接运行 [search_knowledge.py](scripts/search_knowledge.py)。
- 新文献集或原文已更新时，用 [index_papers.py](scripts/index_papers.py) 处理所需论文。清单保留 `paper_id` 和可用的 `content_file`、`pdf_url` 或 `abstract`。限定论文时在建索引阶段加 `--paper-id`；查询覆盖所用集合里的内容。
- 在本 Skill 目录运行 `python -m pip install -r requirements.txt`。配置 `GOOGLE_API_KEY`，或者提供 `OPENAI_API_KEY`、`OPENAI_EMBEDDING_MODEL` 和可选 `OPENAI_BASE_URL`。两次执行应使用同一嵌入服务和模型。

## 2. 执行

以下示例用同一索引目录、集合名和分段字符数。模型输入太长时，可使用较小的 `--chunk-size` 重新索引，并在查询命令里使用同一值。

```bash
python scripts/index_papers.py --papers ./evidence/papers.json --index-dir ./index --collection perovskites --chunk-size 512
python scripts/search_knowledge.py --index-dir ./index --collection perovskites --chunk-size 512 --query "二维电荷有序有哪些证据" --top-k 5 --output ./matches.json
```

## 3. 检查和交付

建索引后核对成功的论文 ID、片段数和 `failures`。索引找不到时先检查目录、集合、服务、模型和分段参数。返回命中时保留 `paper_id`、`source`、`evidence` 和字符区间 `start` 至 `end`，按相关性整理片段。引用事实前读回原文上下文。空结果或证据不足时说明实际覆盖范围。
