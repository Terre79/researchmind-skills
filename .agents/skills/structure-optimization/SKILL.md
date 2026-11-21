---
name: structure-optimization
description: 对给定 CIF 检查结构，用 MatterSim 计算单点能和原子力，或实施固定晶胞及可变晶胞的几何弛豫。
---

# 结构能量与弛豫

## 1. 按任务选入口

| 用户要做什么 | 执行入口 |
| --- | --- |
| 检查输入 CIF | [validate_cif.py](scripts/validate_cif.py)，只需要结构解析依赖。 |
| 计算给定构型的能量和原子力 | [calculate_energy.py](scripts/calculate_energy.py)。 |
| 降低原子受力，保存弛豫构型 | [relax_structure.py](scripts/relax_structure.py)。默认固定晶胞，用户要求调整晶胞时用 `--relax-cell`。 |

## 2. 执行计算

在本 Skill 目录按 [依赖清单](requirements.txt) 准备环境。计算任务需要 MatterSim 检查点，首次安装或遇到编译问题时读 [模型准备与平台要求](references/model.md)。提供实际输入和输出目录；需要时记录 `--device`、`--fmax` 和 `--max-steps`。

```bash
python scripts/validate_cif.py --input ./si.cif
python scripts/calculate_energy.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --out-dir ./energy
python scripts/relax_structure.py --input ./si.cif --model-path ./models/mattersim-v1.0.0-1M.pth --fmax 0.03 --out-dir ./relaxed
```

## 3. 核对并交付

- 单点结果见 `energy.json`。区分总能量、每原子能量和原子力，单位分别为 eV、eV/atom 和 eV/Å。比较结构时记录模型和能量归一方式。
- 弛豫结果见 `relaxation.json` 与 `relaxed.cif`。报告 `converged`、步数、是否放开晶胞及前后最大原子受力，并重新解析输出 CIF。达到步数上限时标明未收敛。
- 解释稳定性时注明这是势模型计算。热力学稳定性需要相应组成空间的参考相及统一能量基准。
