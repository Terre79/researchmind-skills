---
name: phonon-analysis
description: 用 MatterSim 力模型和 Phonopy 有限位移法计算给定 CIF 的声子色散，输出频率表和色散图。
---

# 声子色散分析

## 适合用它做什么

- 对已收敛的周期晶体计算谐近似声子色散。
- 查看频率分支和负频率位置。需要时可先弛豫，再用收敛结构计算。

## 典型请求

- “用 2×2×2 超胞计算这个硅晶体的声子谱，给我图和频率表。”
- “先弛豫这份 CIF，再计算声子色散并列出负频率出现的位置。”

## 你需要提供

- 提供输入 CIF、MatterSim 权重路径和输出目录。可补充超胞、位移幅度和设备，默认超胞为 `2 2 2`，位移为 0.01 Å。
- 正式计算前准备 [依赖](requirements.txt) 和 [MatterSim 权重](references/model.md)。已收敛结构可直接使用。需要预弛豫时用 `--relax-first`，或先用 [relax_structure.py](scripts/relax_structure.py) 保存结果。

## 产出

- [calculate_phonon.py](scripts/calculate_phonon.py) 生成 `dispersion.png`、`dispersion.csv`、`phonon.json`。核对超胞、位移、频率单位 THz 和频率值数量。
- 有负频率时给出频率大小和路径位置，以 CSV 保留原值。

在本 Skill 目录执行：

```bash
python scripts/calculate_phonon.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --supercell 2 2 2 --amplitude 0.01 --out-dir ./phonon
```

## 边界

- 初步弛豫未收敛时，先检查结构和收敛记录。接近零的负频率需要结合收敛、超胞和位移的数值敏感性解读。
- 本流程计算谐近似色散。热导率或有限温度下的动力学性质需另行计算。
