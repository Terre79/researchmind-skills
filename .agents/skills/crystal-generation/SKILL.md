---
name: crystal-generation
description: 用 CrystaLLM 按化学组成和可选空间群生成候选晶体，或检查已有 CIF 的组成、位点和晶胞。适用于候选结构生成及基础 CIF 校验。
---

# 晶体生成与 CIF 校验

## 1. 确定任务要求

- **已有 CIF，只验证文件**。直接运行 [validate_cif.py](scripts/validate_cif.py)。检查组成、位点数和晶胞体积。这个入口只需要 CIF 解析依赖。
- **需要生成候选**。确认用户给的化学组成、候选数量以及是否约束空间群。若用户给定单胞化学计量，保留其中的原子数。只有任务要求特定空间群时才传 `--spacegroup`。

## 2. 执行对应流程

在本 Skill 目录按 [依赖清单](requirements.txt) 准备环境。生成任务需要包含 `ckpt.pt` 的模型目录；首次准备或校验权重时读 [CrystaLLM 模型说明](references/model.md)，再运行 [setup_models.py](scripts/setup_models.py)。

```bash
python scripts/validate_cif.py --input ./input.cif
python scripts/setup_models.py --model-dir ./models/crystallm_v1_small
python scripts/generate_crystals.py --formula NaCl --num-samples 2 --seed 1337 --device cpu --model-dir ./models/crystallm_v1_small --out-dir ./nacl
```

要复现实验，记录模型版本、随机种子、设备和采样参数。已有模型时直接将其目录传入 [generate_crystals.py](scripts/generate_crystals.py)。

## 3. 检查候选并交付

1. 查看 `generation.json` 的 `structures` 和 `rejected`，逐个确认实际生成的 CIF 可读且约化组成符合要求。报告通过数量、拒收原因和文件路径。全拒收时说明该次采样未取得可用结构。
2. 如果用户要求固定原子数或空间群，用结构解析器分别核对位点数和实际空间群。`requested_spacegroup` 记录生成条件。
3. 按模型生成的候选结构交付。稳定性、合成可行性或力学性质需要相应计算和证据。
