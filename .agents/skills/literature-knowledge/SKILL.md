---
name: literature-knowledge
description: 为已有论文建立持久化语义索引，按问题检索带论文 ID、来源和字符位置的片段。适用于在指定文献集合中定位证据。
---

# 文献语义索引与检索

## 适合用它做什么

- 把已选论文的正文或摘要写入本地持久化索引。
- 用自然语言查询已有索引，找出可以回到原文核对的片段。

## 典型请求

- “把这些论文建成一个可重复查询的知识库。”
- “从现有索引找出关于二维电荷有序的三段证据，并给我原文位置。”

## 你需要提供

- 建索引时提供 `papers.json` 及输出索引目录，条目有 `paper_id` 和可用正文、公开 PDF 链接或摘要。查询时提供问题和已有索引目录。
- 两次运行使用相同的集合名、`--chunk-size`、嵌入服务和模型。安装 [依赖](requirements.txt)，配置 `GOOGLE_API_KEY`，或配置 `OPENAI_API_KEY`、`OPENAI_EMBEDDING_MODEL` 及可选的 `OPENAI_BASE_URL`。

## 产出

- [index_papers.py](scripts/index_papers.py) 写入持久化索引并返回论文 ID、片段数和失败项。
- [search_knowledge.py](scripts/search_knowledge.py) 返回相关片段和 `paper_id`、`source`、`evidence`、字符偏移 `start` 和 `end`。提供 `--output` 可保存 JSON。

在本 Skill 目录执行：

```bash
python scripts/index_papers.py --papers ./evidence/papers.json --index-dir ./index --collection perovskites --chunk-size 512
python scripts/search_knowledge.py --index-dir ./index --collection perovskites --chunk-size 512 --query "二维电荷有序有哪些证据" --top-k 5 --output ./matches.json
```

## 边界

- 查询范围由现有索引决定。若索引不存在，先检查目录、集合名、模型和分段大小。若服务限制输入长度，可用较小分段重新建索引。
- 匹配距离用于排序。引用片段前回到原文核对上下文，并说明摘要、正文和覆盖范围。
