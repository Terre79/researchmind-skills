# ResearchMind Agent Skills

九个独立 Skill 位于 `.agents/skills/`。将所需的完整目录复制到 Agent 宿主的技能目录，即可让 Agent 读取 `SKILL.md` 和对应工作流。宿主需要支持读取 Skill 并执行 Python 命令。

| 任务 | Skill | 入口示例 |
| --- | --- | --- |
| 文献检索与导出 | [literature-search](.agents/skills/literature-search/SKILL.md) | `python scripts/search_papers.py --help` |
| 读取与分析论文 | [paper-analysis](.agents/skills/paper-analysis/SKILL.md) | `python scripts/analyze_paper.py --help` |
| 研究报告 | [research-report](.agents/skills/research-report/SKILL.md) | `python scripts/write_report.py --help` |
| 文献语义检索 | [literature-knowledge](.agents/skills/literature-knowledge/SKILL.md) | `python scripts/search_knowledge.py --help` |
| 材料数据库查询 | [materials-search](.agents/skills/materials-search/SKILL.md) | `python scripts/search_materials.py --help` |
| 晶体生成 | [crystal-generation](.agents/skills/crystal-generation/SKILL.md) | `python scripts/generate_crystals.py --help` |
| 能量与弛豫 | [structure-optimization](.agents/skills/structure-optimization/SKILL.md) | `python scripts/relax_structure.py --help` |
| 声子谱 | [phonon-analysis](.agents/skills/phonon-analysis/SKILL.md) | `python scripts/calculate_phonon.py --help` |
| 热导率 | [thermal-conductivity](.agents/skills/thermal-conductivity/SKILL.md) | `python scripts/predict_conductivity.py --help` |

## 直接运行

在相应 Skill 目录用 Python 3.11 或 3.12 安装 `requirements.txt`，然后按 `SKILL.md` 的命令运行。也可以从任意工作目录用绝对路径调用脚本。业务代码随每个目录一起分发，运行入口是普通 Python 脚本。文献清单、CIF 和结果文件通过显式路径在 Skill 之间传递。

```bash
cd .agents/skills/materials-search
python -m pip install -r requirements.txt
python scripts/search_materials.py --formula Si --sources cod oqmd aflow --limit 2 --out-dir ./silicon
```

执行成功时 stdout 输出一份 JSON 摘要，日志写到 stderr。成功和无记录返回 0，部分成功返回 3，全部失败返回 1，参数语法错误由 argparse 返回 2。使用 `--help` 查看每个入口的参数。对于多次运行，使用不同的输出目录或以本次结果清单引用的文件为准。

模型及校验值见 [模型说明](docs/models.md)。旧工具到新入口的对应关系见 [迁移表](docs/legacy-capabilities.md)。真实测试结果见 [验收记录](docs/verification.md)。开发环境可在仓库根目录运行 `python -m unittest discover -s tests`。
