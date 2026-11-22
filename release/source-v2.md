# 源码版验收

在 Windows x64 CPU 上，将每个技能单独复制到临时目录，通过技能自己的 PowerShell 入口连续执行两次。科学测试使用 Python 3.12、固定依赖锁和用户缓存。八份上游原始资产（含 Windows 推理引擎）下载后逐项校验 SHA-256，再通过 `RM_ASSET_DIR` 供首次安装使用。多个操作复用相同的依赖环境和模型。

| 技能 | 已核对的产物 |
| --- | --- |
| literature-search | PDF 导入和 CSV、本地模型生成的检索计划。另在线按 arXiv ID 查回 1706.03762v7 并导出 CSV。 |
| paper-analysis | 从 PDF 读到已知的 diamond 段落，本地模型根据所选证据写出分析。 |
| research-report | 从含两条记录的目录选择 Si1 生成报告，引用列表与正文均包含 Si1。 |
| literature-knowledge | 持久化两条记录，用新的查询进程命中 Si1，并核对字符偏移。 |
| materials-search | 在线查询 OQMD 的硅结构，核对来源 ID 和导出 CIF。 |
| crystal-generation | 固定种子生成 NaCl，使用校验入口重新读取 CIF、核对化学式。 |
| structure-optimization | 对 8 原子硅结构求有限能量和力，对扰动结构弛豫，核对收敛和最大受力下降。 |
| phonon-analysis | 硅的 2×2×2 超胞，位移 0.01 Å。读取频散 CSV 中全部 1,296 个有限 THz 值，核对 PNG。 |
| thermal-conductivity | 对硅分别用 Kappa-P 和 Kappa-MTP 计算 300 K 热导率，两种结果均为有限正值。 |

另在测试进程中从 PATH 移除 Python、uv，使用空的运行时缓存。论文提取入口先报告缺项，随后下载 uv、校验并准备 Python 3.12；一次调用生成正文和 papers.json，再次诊断返回 ready。

日常回归覆盖中文空格路径、单目录安装、只读诊断、缺少密钥、模型损坏及中断恢复。GitHub Actions 在 Windows、Linux、macOS 上运行入口测试。此处记录的九项科研实算平台为 Windows x64 CPU。GPU、Claude Code 和其他宿主的自然语言调用，以及需要私有凭据的在线服务，仍需在对应环境验收。

完整命令见 [仓库说明](../README.md)。旧版上传附件的名称、大小及摘要见 [迁移清单](legacy-assets.json)。
