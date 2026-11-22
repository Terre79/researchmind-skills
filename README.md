# ResearchMind Skills

九个可单独安装的材料科学与文献研究技能。将下表中一个**完整目录**复制到宿主支持的技能位置，或让具备本地命令执行能力的 Agent 显式读取其中的 `SKILL.md`。每个目录自带操作清单、源代码和适用的 Python 依赖锁。Release 使用 GitHub 的 Source code ZIP / tar.gz。

| 技能 | 示例操作 |
| --- | --- |
| [晶体生成](.agents/skills/crystal-generation/SKILL.md) | `generate-crystals`、`validate-cif` |
| [材料查询](.agents/skills/materials-search/SKILL.md) | `search-materials`、`recommend-materials` |
| [结构优化](.agents/skills/structure-optimization/SKILL.md) | `calculate-energy`、`relax-structure` |
| [声子分析](.agents/skills/phonon-analysis/SKILL.md) | `calculate-phonon` |
| [热导率](.agents/skills/thermal-conductivity/SKILL.md) | `predict-conductivity` |
| [文献检索](.agents/skills/literature-search/SKILL.md) | `search-papers`、`import-papers` |
| [论文分析](.agents/skills/paper-analysis/SKILL.md) | `extract-text`、`analyze-paper` |
| [文献知识库](.agents/skills/literature-knowledge/SKILL.md) | `index-papers`、`search-knowledge` |
| [研究报告](.agents/skills/research-report/SKILL.md) | `write-report` |

## 从源码运行

在 `paper-analysis` 目录执行下面任意一条，得到正文和 `papers.json`。输入和输出路径按调用者的工作目录解析。

```powershell
.\scripts\run.ps1 run extract-text --input "paper.pdf" --out-dir "evidence"
```

```sh
sh ./scripts/run.sh run extract-text --input "paper.pdf" --out-dir "evidence"
```

`doctor extract-text --json --input paper.pdf` 仅检查。正常任务直接用 `run`，启动器按操作与文件格式选择依赖，复用缓存或安装缺项，复查后把原参数交给科研脚本。已有 Python 3.11+ 可直接启动；需要第三方包时通过 uv 安装独立的 Python 3.12 环境。需联网安装时，使用宿主自身的授权界面。缓存位置可用 `RM_CACHE_DIR` 指定。完整任务示例、离线方式和模型来源见各技能的说明及 `references/runtime.json`。

依赖锁覆盖 Windows x64、Linux x86_64 和 macOS arm64 的 CPU 组合。Windows x64 首次使用 MatterSim 时，启动器自动安装锁定的 Zig 和 Cython，从校验过的上游源码构建原生扩展；CUDA 用户可提供已验证的 `RM_SCIENCE_PYTHON`。Materials Project、Tavily 或显式选择的远程模型由使用者配置凭据。默认本地模型从固定上游取得并校验。

## 维护与验收

[源码版九项实算及验证范围](release/source-v2.md)

在仓库根目录运行：

```sh
python tools/sync-runtime.py --check
python -m unittest discover -s tests -v
python tests/science_smoke.py --repeat 2 crystal-generation phonon-analysis
```

最后一条从独立技能副本运行实际算例，按技能下载依赖和权重。材料数据库实测需要 OQMD 可用。锁文件与启动器的维护源位于 `tools/profiles`、`tools/runtime-template`；修改后执行 `python tools/sync-runtime.py`。公开原始模型仍受对应上游许可约束。历史 Windows 预览包的实测见 [历史记录](release/verification.md)。
