---
name: crystal-generation
description: 用 CrystaLLM 按给定组成和可选空间群生成候选晶体，或验证已有 CIF 的组成、位点和晶胞。
---

# 晶体生成与 CIF 校验

## 适合用它做什么

- 按化学组成和可选空间群生成候选 CIF。
- 检查已有的 CIF 是否可解析，并查看组成、位点数和晶胞体积。

## 典型请求

- “用 CrystaLLM 生成两个 NaCl 候选结构，给我可解析的 CIF。”
- “生成含 4 个 Na 和 4 个 Cl 的晶胞，要求空间群为 Fm-3m。”
- “帮我确认这份 CIF 的组成和晶胞体积。”

## 你需要提供

- 生成时提供化学组成和输出目录，可补充候选数量、目标空间群、随机种子和运行设备。提供含 `ckpt.pt` 的模型目录。初次准备时查看 [模型安装与校验](references/model.md)。
- 仅校验时提供 CIF 文件。环境依赖见 [依赖清单](requirements.txt)。

## 产出

- [generate_crystals.py](scripts/generate_crystals.py) 生成 `generation.json` 和实际通过校验的候选 CIF。汇报通过数量、文件路径和拒收原因。
- [validate_cif.py](scripts/validate_cif.py) 返回约化组成、位点数和晶胞体积。要求固定原子数或空间群时，另行核对生成结构的实际位点和空间群。

在本 Skill 目录执行：

```bash
python scripts/setup_models.py --model-dir ./models/crystallm_v1_small
python scripts/generate_crystals.py --formula NaCl --num-samples 2 --seed 1337 --device cpu --model-dir ./models/crystallm_v1_small --out-dir ./nacl
python scripts/validate_cif.py --input ./nacl/candidates/001.cif
```

## 边界

- 空间群参数是生成条件，实际对称性要以结构解析结果为准。模型筛选使用约化组成，指定单胞原子数时应单独核对。
- 输出是候选结构。稳定性、可合成性和材料性质需要后续计算或实验证据。全拒收时说明本次未得到可用候选。
