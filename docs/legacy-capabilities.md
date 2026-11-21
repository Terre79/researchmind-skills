# 旧能力与独立脚本映射

下表以旧版的 [42 个工具注册](https://github.com/crjia111/ResearchMind2.0/blob/e667d3f5d6ca1c775290bc9326c2a49f20208f4b/packages/researchmind-skills/src/researchmind_skills/schemas/legacy-tools.json)为基准。脚本路径从对应 Skill 的根目录开始解析。

| 旧能力或别名 | Skill | 当前入口 |
| --- | --- | --- |
| `list_papers_from_csv`、`get_paper_topics`、`filter_papers_by_topic` | literature-search | `scripts/filter_papers.py --input papers.json`，可选 `--topic` |
| `select_papers`、`get_selected_papers`、`clear_paper_selection` | literature-search | `scripts/select_papers.py --selection selection.json`，用 `--paper-id` 选集或 `--clear` 清空 |
| `generate_research_plan` | literature-search | `scripts/plan_search.py --query …` |
| `search_papers`、`search_arxiv_papers`、`tavily_academic_search` | literature-search | `scripts/search_papers.py --query … --sources arxiv semantic_scholar tavily`，按目标选源 |
| `ingest_uploaded_papers` | literature-search | `scripts/import_papers.py --input …` |
| `search_papers_by_author` | literature-search | `scripts/search_by_author.py --author …` |
| `get_paper_info` | literature-search | 本地用 `scripts/filter_papers.py --paper-id …`，远程 arXiv 用 `scripts/search_papers.py --query id:…` |
| `tavily_search`、`tavily_news_search` | literature-search | `scripts/search_papers.py --mode general` 或 `--mode news` |
| `download_paper` | paper-analysis | `scripts/download_paper.py --url … --output …` |
| `get_paper_content`、`fetch_papers_content` | paper-analysis | `scripts/extract_text.py --input …` 或 `--papers … --paper-id …`，可传多个 ID |
| `load_saved_paper_content`、`load_paper_content_segment` | paper-analysis | `scripts/read_segment.py --input …`，可选 `--start` 和 `--length` |
| `search_in_saved_content` | paper-analysis | `scripts/find_in_text.py --input … --term …` |
| `batch_paper_analysis` | paper-analysis | `scripts/analyze_paper.py --papers …` |
| `save_papers_to_csv`、`clean_csv_data` | literature-search | `scripts/export_csv.py`、`scripts/clean_csv.py` |
| `generate_research_report` | research-report | `scripts/write_report.py --papers … --topic …` |
| `ingest_papers_to_vector_store`、`semantic_search_papers` | literature-knowledge | `scripts/index_papers.py`、`scripts/search_knowledge.py`，指定持久化索引路径 |
| `materials_project_query_tool`、`get_oqmd_phases`、`search_cod_by_formula`、`get_aflow_data`、`batch_database_search` | materials-search | `scripts/search_materials.py --formula … --sources mp oqmd cod aflow`，按目标选源 |
| `get_structure_recommendations` | materials-search | `scripts/recommend_materials.py`，按对应数据库各自的计算指标排序 |
| `materials.health_check` | materials-search | 使用目标来源的小查询检查环境、网络和认证，读取逐来源失败信息 |
| `calculate_phonon` | phonon-analysis | `scripts/calculate_phonon.py`，可选 `--relax-first` |
| `calculate_energy`、`relax_structure` | structure-optimization | `scripts/calculate_energy.py`、`scripts/relax_structure.py` |
| `simulation.health_check` | 仿真技能 | 运行对应 `setup_models.py` 验证检查点，使用小结构检查实际推理 |
| `extract_and_validate_cif` | crystal-generation、structure-optimization、phonon-analysis | `scripts/validate_cif.py --input …` |
| `calculate_kappa` | thermal-conductivity | `scripts/predict_conductivity.py --method kappa_p`、`kappa_mtp` 或 `both` |
| `generate_crystal_structure` | crystal-generation | `scripts/generate_crystals.py --formula …` |
| `clear_structure_cache` | 输出目录管理 | 用户通过 `--out-dir` 控制产物生命周期，模型目录与结果目录独立 |

旧会话 ID 和作业 ID 由显式文件路径、输出目录和宿主进程状态替代。旧版未验证的形成能或凸包稳定性未加入新的能量入口。
