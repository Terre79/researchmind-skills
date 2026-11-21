---
name: thermal-conductivity
description: 用 AI4Kappa 的两份已训练模量模型和 Kappa-P 或 Kappa-MTP 方法预测晶体在 300 K 的晶格热导率。适用于比较候选晶体的模型预测值。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

从 [AI4Kappa 配置说明](references/model.md)准备两个模量检查点和元素特征表。输入 CIF 应有确定的占位和周期晶胞。

```bash
python scripts/setup_models.py --model-dir ./models/kappa
python scripts/predict_conductivity.py --input ./si.cif --model-dir ./models/kappa --method both --temperature 300 --out-dir ./conductivity
```

`--method` 可选 `kappa_p`、`kappa_mtp` 或 `both`。交付 `thermal_conductivity.csv` 及同名 JSON，注明方法、300 K 和单位 W/(m·K)。检查模量和热导率是否为有限正值。
