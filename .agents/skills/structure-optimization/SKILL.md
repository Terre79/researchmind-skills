---
name: structure-optimization
description: 对给定 CIF 用 MatterSim 计算单点能和原子力，或执行固定晶胞与可变晶胞的几何弛豫。
---

# 结构能量与弛豫

## 适合用它做什么

- 校验输入 CIF，计算给定构型的总能量、每原子能量和原子力。
- 用 MatterSim 做几何弛豫并导出优化后的结构。可按要求固定晶胞或同步调整晶胞。

## 典型请求

- “计算这个硅结构的单点能，把每个原子的力列出来。”
- “固定晶胞弛豫这份 CIF，最大受力阈值设为 0.03 eV/Å。”
- “让晶胞也参与弛豫，给我收敛记录和优化后的 CIF。”

## 你需要提供

使用 [Windows x64 CPU 完整 ZIP](https://github.com/Terre79/researchmind-skills/releases/tag/skills-win-cpu-v1)。完整包中的脚本使用同目录下的 `python/python.exe`，可从任意工作目录用绝对路径调用。源码目录部署方法见本节的依赖清单。

- 提供输入 CIF 和输出目录。完整包内置 MatterSim 权重。可补充 `--device`、`--fmax`、`--max-steps`，需要调整晶胞时用 `--relax-cell`。
- 从源码安装按 [依赖清单](requirements.txt) 安装并查看 [模型准备与平台要求](references/model.md)。只校验 CIF 时用 [validate_cif.py](scripts/validate_cif.py)，无需加载权重。

## 产出

- [calculate_energy.py](scripts/calculate_energy.py) 生成 `energy.json`，包括总能量 eV、每原子能量 eV/atom 和原子力 eV/Å。
- [relax_structure.py](scripts/relax_structure.py) 输出 `relaxed.cif`、`relaxation.json` 和日志。核对 `converged`、步数、晶胞设置和弛豫前后最大原子受力。

在本 Skill 目录执行：

```powershell
.\python\python.exe .\scripts\calculate_energy.py --input ./si.cif --out-dir ./energy
.\python\python.exe .\scripts\relax_structure.py --input ./si.cif --fmax 0.03 --out-dir ./relaxed
```

## 边界

- 结构比较应记录相同的势模型与能量归一方式。达到步数上限仍未满足条件时，标记为未收敛。
- 热力学稳定性判断依赖参考相和统一能量基准。单点能和弛豫结果仅反映相应势模型及所给构型。
