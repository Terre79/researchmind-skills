---
name: crystal-generation
description: 用 CrystaLLM 按化学组成或指定空间群生成候选晶体，并检查候选 CIF 的组成和晶胞。适用于材料结构生成和 CIF 基础校验。
---

在本 Skill 目录使用 Python 3.11 或 3.12 安装依赖。

```bash
python -m pip install -r requirements.txt
```

## 准备模型并生成

首次部署由维护者下载并校验 [CrystaLLM v1 Small 权重](references/model.md)。已有权重时，直接把包含 `ckpt.pt` 的目录传给 `--model-dir`。

```bash
python scripts/setup_models.py --model-dir ./models/crystallm_v1_small
python scripts/generate_crystals.py --formula NaCl --num-samples 2 --seed 1337 --device cpu --model-dir ./models/crystallm_v1_small --out-dir ./nacl
```

检查 `generation.json` 的通过和拒收记录，逐个读取实际生成的 `candidates/*.cif`。用 `validate_cif.py --input …` 单独验证用户给出的 CIF。交付时注明模型、组成和可用候选数量。后续可按需求安排弛豫和稳定性验证。
