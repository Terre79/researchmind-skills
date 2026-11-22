# 构建和验收 Windows x64 CPU Skill

用户在 GitHub Release 下载对应的 `*-win-x64-cpu-v1.zip`，解压包含 `SKILL.md` 的完整目录。脚本在 `python/python.exe` 下运行，权重、解释器和依赖均在技能目录内。具有本地执行权限的宿主可把该目录注册为 Skill。GitHub 自动生成的 Source code 是源码快照。

## 构建机输入

在 Windows x64 CPython 3.12 的开发环境准备 `packaging`。从可信 PyPI 或 PyTorch 官方源安装各 Skill 的依赖到隔离的 `pip --target` 目录。PyTorch 使用官方 CPU 版，构建器读取 wheel RECORD 和依赖元数据，拒绝缺依赖、版本冲突和 CUDA wheel。可从同一技能发布包中的 `bundle-manifest.json` 读取实际构建用的依赖版本和文件指纹。

- 构建器校验资产文件 SHA-256。固定文件名和指纹见 [bundle_assets.py](../tools/bundle_assets.py)。
- 解释器使用 [Python 3.12.10 Windows x64 嵌入版](https://www.python.org/downloads/release/python-31210/)。
- CrystaLLM 和 MatterSim 权重源自 [原模型 Release](https://github.com/Terre79/researchmind-skills/releases/tag/models-v1)。从 CrystaLLM 原档案解出 `ckpt.pt`。CrystaLLM 使用 CC BY 4.0，MatterSim 权重和源代码使用 MIT。
- 本地文字模型采用 Qwen2.5-0.5B 指令模型，固定 [Qwen 官方 GGUF 修订版](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/tree/9217f5db79a29953eb74d5343926648285ec7e67)。知识库采用 Qwen3-Embedding-0.6B Q8，固定 [官方嵌入模型修订版](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF/tree/370f27d7550e0def9b39c1f16d3fbaa13aa67728)。两者均为 Apache-2.0。
- `llama-cpu.zip` 取自 [llama.cpp b5916 Windows x64 CPU 正式附件](https://github.com/ggml-org/llama.cpp/releases/tag/b5916)。将该版本的 MIT 文本放到 `llama.cpp-LICENSE`，并准备 `Apache-2.0.txt` 随包分发。
- 从 [MatterSim 1.2.2 官方源包](https://pypi.org/project/mattersim/1.2.2/#files) 构建 CPython 3.12 Windows x64 扩展 `threebody_indices.pyd`。把扩展放至源目录下 `src/mattersim/datasets/utils/`，通过 `--mattersim-source` 指向该源码目录。构建过程使用开发机 C 编译器。用户端从 ZIP 直接使用编译产物。
- AI4Kappa 权重和元素特征表纳入公开 ZIP 前需要再分发许可。热导率打包分支检查 `--kappa-permission` 提供的分发许可文件。该选项只接受来自权利人的真实许可。

## 构建和验证

示例中的依赖目录由构建机准备。对 MatterSim 相关包补充 `--mattersim-source`。

```powershell
python tools/build_bundle.py --skill crystal-generation --assets .\assets --wheels .\cpu-wheels .\science-wheels --output .\dist
python tools/verify_bundle.py --archive .\dist\crystal-generation-win-x64-cpu-v1.zip --fixtures .\fixtures
```

将 `clean-si.cif`、`perturbed-si.cif`、公开 arXiv 正文 `acceptance-paper.pdf` 和第二篇论文的已提取文本 `standalone-evidence/text/0002.txt` 放至验证输入目录。使用标准硅金刚石晶胞及单原子 0.11 Å 位移构造弛豫用例。文献使用 arXiv `cond-mat/0211520v2` 和 `2601.11793v1`；验证脚本提供清单和断言。验收输入保留在发布测试侧。

验收脚本校验 ZIP 内容和哈希，以最小进程环境从含中文和空格的目录启动包内 Python，清除 PYTHONPATH、系统 Python 和模型路径。离线检查将 HTTP(S) 代理指向不可用地址，嵌入推理只通过临时本机端点。材料库验收须加 `--online`。在目标 Agent 和干净虚拟机上复验后，才能承诺适用该宿主的无外部依赖安装。

## 已知外部条件

材料数据库和远程文献检索需要网络及服务可用，账户型 API 仍需自己的凭据。包内本地模型不发送文本到远程服务。需主动改用远程时，设 `RM_CHAT_BACKEND=remote` 或 `RM_EMBED_BACKEND=remote` 并配置服务。CPU 版需要 x64 硬件，具体支持范围以发布验收环境为准。
