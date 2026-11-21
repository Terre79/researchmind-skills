---
name: thermal-conductivity
description: 用 AI4Kappa 的体积和剪切模量检查点，通过 Kappa-P 或 Kappa-MTP 预测晶体在 300 K 的晶格热导率。适用于对给定结构进行模型估算。
---

# 晶格热导率预测

## 1. 核对输入和计算方法

准备一个或多个含确定占位的周期 CIF。此预测流程适用于 300 K。用户指定其他温度时，说明可用模型的温度范围。按用户要求选 `kappa_p`、`kappa_mtp` 或 `both`。两种方法的结果保留各自标签。

## 2. 准备权重并执行

在本 Skill 目录按 [依赖清单](requirements.txt) 准备环境。首次准备权重时读 [AI4Kappa 模型说明](references/model.md)，由 [setup_models.py](scripts/setup_models.py) 获取并校验两份检查点和元素特征表。若特征表不在模型目录，给 [predict_conductivity.py](scripts/predict_conductivity.py) 传 `--atom-init`。

```bash
python scripts/setup_models.py --model-dir ./models/kappa
python scripts/predict_conductivity.py --input ./si.cif --model-dir ./models/kappa --method both --temperature 300 --out-dir ./conductivity
```

## 3. 核对并交付

在 `thermal_conductivity.json` 中按输入结构和方法核对结果，检查体积与剪切模量以及热导率为有限正值。报告预测温度 300 K、单位 W/(m·K)、计算方法及实际的失败条目，附上生成的 JSON 和 CSV。若两种方法有明显差异，分别保留结果并注明它们都是模型预测。
