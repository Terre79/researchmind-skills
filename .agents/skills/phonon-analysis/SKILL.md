---
name: phonon-analysis
description: 用 MatterSim 力模型和 Phonopy 有限位移法计算 CIF 对应的声子色散，导出频率表和图。适用于分析谐近似下的软模和频率分支。
---

# 声子色散分析

## 1. 选择输入结构处理方式

已有收敛 CIF 时，直接运行 [calculate_phonon.py](scripts/calculate_phonon.py)。若输入还需弛豫，按用户意图加 `--relax-first`，或先用 [relax_structure.py](scripts/relax_structure.py) 保存并检查结构，然后把收敛的 `relaxed.cif` 用作输入。只需检查 CIF 时运行 [validate_cif.py](scripts/validate_cif.py)。

## 2. 运行有限位移

准备 [依赖](requirements.txt)，首次安装或编译失败时查看 [MatterSim 模型说明](references/model.md)。保留用户指定的超胞和位移参数。默认超胞为 `2 2 2`，位移为 0.01 Å。

```bash
python scripts/calculate_phonon.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --supercell 2 2 2 --amplitude 0.01 --out-dir ./phonon
```

初步弛豫失败时，检查结构和收敛状态，再决定是否调整弛豫参数。计算过程中确保输入是实际使用的构型。

## 3. 检查和交付

读取 `phonon.json` 核对输入、超胞、位移、位移构型数、频率数和 THz 单位。附上 `dispersion.png` 和 `dispersion.csv`。报告负频率出现的路径位置及大小。遇到接近零的小负值时，结合结构收敛、超胞与位移数值敏感性解释，保留原始数据。
