---
name: phonon-analysis
description: 以 MatterSim 力模型和 Phonopy 有限位移法计算给定 CIF 的声子色散，输出图和频率表。适用于检查谐近似下的软模和声子谱。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

参阅 [模型准备](references/model.md)。优先使用已收敛结构。只有需要先弛豫时才加 `--relax-first`，或用本目录内的 `relax_structure.py` 单独保存弛豫结构。

```bash
python scripts/calculate_phonon.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --supercell 2 2 2 --amplitude 0.01 --out-dir ./phonon
```

交付 `dispersion.png`、`dispersion.csv` 和 `phonon.json`。记录超胞和位移量，检查频率单位 THz 和负频率。结果对小负频率敏感时，说明超胞、初始结构和位移设置。
