# ResearchMind Skills

ResearchMind 的九个 Agent Skills 集中存放在 `.agents/skills/`。每个目录包含 `SKILL.md`、参考资料、执行脚本和 ResearchMind 运行包版本清单。

| 领域 | Skills |
| --- | --- |
| 文献 | `literature-search`、`paper-analysis`、`research-report`、`literature-knowledge` |
| 材料数据库 | `materials-search` |
| 仿真 | `crystal-generation`、`structure-optimization`、`phonon-analysis`、`thermal-conductivity` |

## 使用

1. 克隆本仓库并从该目录打开支持 `.agents/skills/` 的 Agent，或把所需的完整 Skill 目录复制到 Agent 宿主的技能目录。
2. 若走脚本或 CLI 路径，在 Agent 实际执行命令的 Python 3.11+ 环境中安装配套运行包。下面的命令需要 Git，并固定到与这些 Skill 匹配的源码提交。

   ```sh
   python -m pip install "researchmind-skills @ git+https://github.com/crjia111/ResearchMind2.0.git@e667d3f5d6ca1c775290bc9326c2a49f20208f4b#subdirectory=packages/researchmind-skills"
   ```

3. 在仓库根目录运行检查。根据目标能力配置 Python 可选依赖、第三方凭据或本地模型。按需将安装命令中的包名改为 `researchmind-skills[paper]`、`researchmind-skills[vector]`、`researchmind-skills[database]` 或 `researchmind-skills[simulation]`。

   ```sh
   python -m researchmind_skills doctor --skill literature-search --target .agents/skills
   ```

支持原生函数工具的宿主可由维护者绑定同一运行包的 Python API。已经绑定相应工具的 Agent 可以通过宿主调用，环境检查也由宿主或维护者完成。首次提供的框架适配为 AgentScope。

Skill 快照来自 [ResearchMind2.0 的迁移提交](https://github.com/crjia111/ResearchMind2.0/commit/e667d3f5d6ca1c775290bc9326c2a49f20208f4b)，对应运行包 `0.1.0`。更新 Skill 时，请同步核对脚本和清单中的运行包版本。有关可选依赖和模型配置，请参阅[运行包文档](https://github.com/crjia111/ResearchMind2.0/blob/e667d3f5d6ca1c775290bc9326c2a49f20208f4b/docs/portable-skills.md)。
