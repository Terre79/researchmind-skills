# 独立 Skill 验收记录

验收于 2026-11-22 在 Windows、Python 3.12 和 RTX 3070 Ti Laptop 上执行。测试运行环境中未安装原 ResearchMind 运行包。仓库测试复制各 Skill，清空 `PYTHONPATH`，从外部工作目录执行入口帮助和本地功能。实测另行加载 Python 科学依赖、官方权重和本地模型服务。

| Skill | 实际执行与产物 |
| --- | --- |
| literature-search | arXiv 主题查询返回 4 条、作者查询返回 2 条。检索计划用真实 Qwen 推理生成。独立测试覆盖本地文献导入、选集、读回与清空、CSV 导出和清理。 |
| paper-analysis | 从 arXiv 下载 296,279 字节的 PDF。两篇真实论文提取出正文，校验了字符分段，并用真实 Qwen 生成 Markdown 和 CSV 分析。 |
| research-report | 从单独复制的 Skill 用 Qwen 生成英文单篇研究报告，结果标出完整 arXiv ID `cond-mat/0211520v2`、链接、证据级别和证据截断状态。验收覆盖来源可追踪和文件生成。 |
| literature-knowledge | Chroma 和 BGE Small EN v1.5 为两篇全文写入 168 段。另起进程查询层状氧化物电荷有序，前两条均来自 `cond-mat/0211520v2`，含正文和偏移量。 |
| materials-search | COD、OQMD、AFLOW 分别返回 2 条硅记录，共导出 6 个可解析 CIF。另一轮从独立拷贝验证 OQMD 排序，以及两家暂时不可达时 AFLOW 部分成功。 |
| crystal-generation | 官方 CrystaLLM v1 Small 使用 NaCl 和种子 1337 分别在 CPU 和 CUDA 上生成 2 个候选。两次运行的 CIF 均可解析，且组成均为 NaCl。归档离线安装和哈希校验通过。 |
| structure-optimization | MatterSim 1M 对 2 原子硅单胞的单点能约 −10.825 eV。弛豫 2 步后收敛，最大原子受力由 1.398 降到 0.013 eV/Å，输出 `relaxed.cif`。 |
| phonon-analysis | MatterSim 和 Phonopy 对硅的 2×2×2 超胞运行有限位移，独立脚本产出色散 PNG 与 1296 条频率数据。分别测试直接计算和先弛豫再计算。 |
| thermal-conductivity | 用 AI4Kappa 的两个原始检查点和原元素特征表实际计算硅结构的两种 300 K 热导率，并导出 CSV。另验证非 300 K 输入会被拒绝。 |

Materials Project 与 Tavily 的成功路径需要相应凭据。验收环境缺少这些凭据，已检查缺项提示。Semantic Scholar 公共请求返回 HTTP 429，确认脚本报告限流。Google 嵌入服务已保留，真实索引实测使用 OpenAI 兼容的本地服务。文献分析和报告结果按模型生成文本交付，引用和证据级别仍需要按用途审阅。

MatterSim 原版权重已从公开 Release 经安装脚本下载并校验。MatterSim 在该 Windows 环境使用官方 1.2.2 源码编译三体索引扩展后测试。平台首次安装依赖可用的 C 编译工具。测试展示单例真实运行和产物检查，模型预测值需要面向目标材料、物性和基准数据另行验证。

在仓库根目录运行 `python -m unittest discover -s tests`。仓库测试另外检查所有跟踪文本文件的 500 物理行上限。
