---
name: structure-optimization
description: 对指定 CIF 用 MatterSim 计算结构能量和原子受力，或进行几何弛豫并导出 CIF。适用于比较已给结构和获得弛豫后的候选。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

参阅 [模型准备](references/model.md)。给了 CIF 后先用 `validate_cif.py` 确认可解析。单点能用 `calculate_energy.py`，想降低原子受力时用 `relax_structure.py`。默认固定晶胞；用户需要优化晶胞时加 `--relax-cell`。

```bash
python scripts/calculate_energy.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --out-dir ./energy
python scripts/relax_structure.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --fmax 0.03 --out-dir ./relaxed
```

检查能量和力的单位、`converged`、前后最大原子受力及 `relaxed.cif`。总能量是势模型的预测。凸包或热力学稳定性需要额外的统一基准数据和验证。
