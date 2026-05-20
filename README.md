# Ultimate_Game_Insights

**基于大规模 Steam 游戏数据的市场结构、玩家反馈与平台生态变化分析**

本仓库是“大数据处理技术”课程的个人项目。项目使用 Kaggle 上的 **Steam Games Dataset 2025**，围绕 Steam 游戏市场结构、玩家反馈、热度指标和平台生态变化进行分析。

项目并不是一个完整软件系统，而是一个以 Jupyter Notebook 为主线的数据分析项目。整体流程参考 Kaggle 数据分析 Notebook 的形式：先说明问题，再运行代码，展示表格或图表，最后给出解释和阶段性结论。

更完整的项目背景、Notebook 设计原则、后续 Agent 协作注意事项见：

[reports/project_brief.md](reports/project_brief.md)

## 研究问题

本项目主要回答两个问题：

1. 在 Steam 平台上，什么样的游戏更容易获得玩家关注？
2. 从 2024 年 5 月到 2025 年 3 月，Steam 游戏市场在数量、类型、玩家反馈和平台生态方面发生了哪些变化？

项目同时展示大规模表格数据处理能力，包括大 CSV 文件读取、字段理解、数据清洗、特征工程、Parquet 转换、工具性能对比和可视化分析。

## 数据集

数据来源：

- Kaggle: [Steam Games Dataset 2025](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)

数据下载后应放在本地目录：

```text
data/raw/archive/
```

解压后的预期文件结构如下：

```text
data/raw/archive/
├── games_march2025_cleaned.csv
├── games_march2025_full.csv
├── games_may2024_cleaned.csv
└── games_may2024_full.csv
```

原始 CSV 文件总大小约 1.7GB，不适合直接提交到 GitHub。仓库中保留下载说明和分析代码，原始数据需要在本地重新下载。

Notebook 01 中包含 KaggleHub 和 Kaggle CLI 的下载示例代码。为避免每次运行都重复下载，相关代码默认保持注释状态。

## 项目结构

```text
Ultimate_Game_Insights/
├── data/
│   ├── raw/                 # 原始数据，本地保存，不提交大文件
│   └── processed/           # 小型汇总结果和可再生中间数据
├── figures/                 # Notebook 生成的图表
├── notebooks/               # 主要数据分析流程
├── reports/
│   ├── latex/               # 中文课程报告 LaTeX 源文件
│   ├── latex_build/         # LaTeX 编译输出
│   ├── references/          # 参考论文
│   └── project_brief.md     # 项目上下文和协作说明
├── requirements.txt
├── README.md
└── .gitignore
```

## 环境配置

建议在 macOS 或 Linux 下使用 Python 虚拟环境。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果后续新增或删除 Python 依赖，请重新生成依赖文件：

```bash
pip freeze > requirements.txt
```

主要依赖包括：

- `pandas`, `numpy`: 基础表格处理与数值计算
- `matplotlib`, `seaborn`: 可视化
- `duckdb`, `polars`, `pyarrow`: 大表读取、查询和 Parquet 支持
- `psutil`: 性能和内存测量
- `jupyter`, `notebook`, `ipykernel`: Notebook 运行环境
- `scikit-learn`: 后续特征缩放、聚类或相似度实验的基础依赖
- `kagglehub`: 可选的数据下载辅助工具

## Notebook 流程

按顺序运行以下 Notebook：

```text
notebooks/01_steam_dataset_overview.ipynb
notebooks/02_large_table_processing_strategy.ipynb
notebooks/03_steam_data_cleaning_and_features.ipynb
notebooks/04_steam_market_structure_analysis.ipynb
notebooks/05_steam_reviews_popularity_analysis.ipynb
notebooks/06_steam_tag_genre_positioning_analysis.ipynb
notebooks/07_report_synthesis.ipynb
```

各 Notebook 的作用如下：

| Notebook | 内容 |
| --- | --- |
| 01 | 数据集介绍、文件规模、字段结构、缺失情况和主分析文件选择 |
| 02 | `pandas`、`duckdb`、`polars` 的大表处理策略对比，并将常用字段转为 Parquet |
| 03 | 数据清洗、字段统一、异常值检查、多标签处理和基础特征工程 |
| 04 | Steam 市场结构分析，包括发行趋势、价格、平台、类型、标签和开发商/发行商长尾 |
| 05 | 玩家反馈与热度分析，包括评论数、好评率、推荐数、峰值在线、价格和平台关系 |
| 06 | 标签、类型和市场定位分析，包括标签竞争、共现关系和高反馈细分方向 |
| 07 | 报告综合整理，汇总方法、发现、局限性和后续方向 |

启动 Jupyter：

```bash
jupyter notebook
```

## 当前输出

项目已生成：

- 7 个主线 Notebook；
- 38 张分析图表，保存在 `figures/`；
- 多个小型 summary CSV，保存在 `data/processed/`；
- 报告汇总文件 `reports/final_report_summary.md`；
- 中文 LaTeX 报告模板 `reports/latex/main.tex`；
- 编译后的 PDF 报告草稿 `reports/latex_build/main.pdf`。

较大的 Parquet 中间文件不会提交到 GitHub，可通过重新运行 Notebook 02 和 Notebook 03 生成。

## LaTeX 报告

课程报告使用中文 LaTeX 编写，主文件为：

```text
reports/latex/main.tex
```

本地使用 `tectonic` 编译：

```bash
tectonic --synctex --keep-logs --keep-intermediates --outdir reports/latex_build reports/latex/main.tex
```

VS Code 中已配置 LaTeX Workshop 使用 `tectonic` 保存自动编译。报告模板包含封面、摘要、目录、章节大纲、图表示例、参考资料和附录。

## 数据与 GitHub 提交说明

以下内容不应提交到 GitHub：

- `data/raw/archive/` 下的原始 Kaggle CSV；
- 下载得到的压缩包；
- `data/processed/` 下的 Parquet 文件；
- LaTeX 编译中间文件。

以下内容可以提交：

- Notebook；
- README 和项目说明文档；
- 小型 summary CSV；
- 生成的 PNG 图表；
- LaTeX 源文件；
- 最终需要提交的 PDF 报告。

这样可以保持仓库体积较小，同时保证项目流程可复现。

## 后续方向

当前主线分析已经完成。后续可以在报告之外继续扩展一个简单的 Steam 游戏相似推荐功能，例如基于标签、类型、类别和简介文本计算相似度，输入一个游戏名称后返回相似游戏。该扩展不属于当前 Notebook 主线分析的一部分。
