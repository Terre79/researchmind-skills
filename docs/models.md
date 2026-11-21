# 模型与许可证

- CrystaLLM v1 Small 的官方归档采用 CC BY 4.0，保留原样并镜像在本仓库的 `models-v1` Release。[Zenodo 模型记录](https://doi.org/10.5281/zenodo.10642388) · [论文](https://doi.org/10.1038/s41467-024-54639-7) · [许可证](https://creativecommons.org/licenses/by/4.0/)
- MatterSim v1.0.0 1M 的微软原版权重采用 MIT 许可证，同一 Release 同时提供许可证。[模型卡](https://github.com/microsoft/mattersim/blob/e59b088ee621cafe0df1b399a27299f3e9092ede/MODEL_CARD.md) · [权重 Release](https://github.com/Terre79/researchmind-skills/releases/tag/models-v1)
- AI4Kappa 的两个检查点和元素特征表从固定的上游提交直接下载。上游目录未发现再分发许可证，仓库分发的是安装脚本与独立计算代码。[上游](https://github.com/Jack-Liu0227/AI4Kappa/tree/de1608c9cae3c934d43324cd01904ffd7e546142)

各仿真技能的 `scripts/setup_models.py` 验证 SHA-256 并安装模型。已有原始下载文件时可以使用 `--asset-dir` 离线安装。检查点保存在用户指定的模型目录。
