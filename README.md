# SteamScope: Large-scale Steam Game Market and Popularity Analysis

This repository is a personal final project for a Big Data Processing and Analysis course. The project uses Steam Games Dataset 2025 as a large tabular data case study.

The project goal is to transform large-scale Steam game tables into decision-oriented insights about market structure, player feedback, popularity, and platform ecosystem changes.

Recommended Chinese title:

**基于大规模 Steam 游戏数据的市场结构、玩家反馈与平台生态变化分析**

The repository name remains `Ultimate_Game_Insights` for continuity, but the report and notebook storyline should use the SteamScope title.

For the full project memory, research framing, reference-paper takeaways, notebook storyline, and implementation rules, read:

[`reports/project_brief.md`](reports/project_brief.md)

## Project Vision

The project should show that a medium-to-large real-world tabular dataset can be processed step by step with a clear and verifiable workflow.

The Steam dataset is suitable for the course because it contains multiple CSV files totaling about 1.7GB, long text columns, mixed data types, multi-label fields, time fields, review metrics, popularity indicators, and platform information.

Core research questions:

1. What kinds of Steam games are more likely to gain player attention?
2. How did the Steam game market change between the May 2024 and March 2025 dataset snapshots?

Course alignment:

- Chapter 2: use AI agents and vibe coding responsibly, while keeping code runnable and results verifiable.
- Chapter 3: follow a complete data analysis framework and explicitly recognize data types.
- Chapter 4: focus on large-scale tabular data processing tools, including reading, filtering, aggregation, memory use, and performance comparison.
- Chapter 5: analyze time-related fields such as `release_date` and version snapshots from 2024 and 2025.

Important rule for future assistants: this is primarily a notebook-based data analysis project, not a full software system. Keep notebooks focused, reproducible, and report-ready. Do not over-engineer the project.

## Dataset

Dataset source: Steam Games Dataset 2025

Kaggle link: <https://www.kaggle.com/datasets/artermiloff/steam-games-dataset>

The dataset is too large to upload to GitHub. The raw files should be downloaded locally and stored under:

```text
data/raw/archive/
```

After downloading and extracting the Kaggle archive, the expected structure is:

```text
data/raw/archive/
├── games_march2025_cleaned.csv
├── games_march2025_full.csv
├── games_may2024_cleaned.csv
└── games_may2024_full.csv
```

Current local file sizes:

- `games_march2025_cleaned.csv`: about 447MB
- `games_march2025_full.csv`: about 450MB
- `games_may2024_cleaned.csv`: about 403MB
- `games_may2024_full.csv`: about 405MB

Approximate row counts:

- `games_march2025_cleaned.csv`: 89,619 rows
- `games_march2025_full.csv`: 94,949 rows
- `games_may2024_cleaned.csv`: 83,647 rows
- `games_may2024_full.csv`: 87,807 rows

Key columns include:

- Basic game fields: `appid`, `name`, `release_date`
- Platform fields: `windows`, `mac`, `linux`
- Price and package fields: `price`, `discount`, `dlc_count`, `packages`
- Review and rating fields: `positive`, `negative`, `user_score`, `metacritic_score`, `pct_pos_total`, `num_reviews_total`, `pct_pos_recent`, `num_reviews_recent`
- Popularity fields: `recommendations`, `peak_ccu`
- Playtime fields: `average_playtime_forever`, `average_playtime_2weeks`, `median_playtime_forever`, `median_playtime_2weeks`
- Multi-label fields: `genres`, `categories`, `tags`, `developers`, `publishers`, `supported_languages`, `full_audio_languages`
- Text fields: `detailed_description`, `about_the_game`, `short_description`, `reviews`

## Download Instructions

The first notebook should include the download code as a commented reference cell. Do not run it every time, because the data is large.

Recommended KaggleHub reference code:

```python
# Optional one-time download. Keep this commented unless the dataset is missing.
# import kagglehub
# from pathlib import Path
# import shutil
#
# dataset_path = kagglehub.dataset_download("artermiloff/steam-games-dataset")
# target_dir = Path("data/raw/archive")
# target_dir.mkdir(parents=True, exist_ok=True)
#
# # Copy downloaded CSV files into the project data folder.
# for csv_file in Path(dataset_path).glob("*.csv"):
#     shutil.copy2(csv_file, target_dir / csv_file.name)
#
# print("Dataset copied to:", target_dir.resolve())
```

Alternative Kaggle CLI workflow:

```bash
# Optional one-time download. Run from the project root only if data is missing.
# mkdir -p data/raw
# kaggle datasets download -d artermiloff/steam-games-dataset -p data/raw
# unzip data/raw/steam-games-dataset.zip -d data/raw/archive
```

Raw data files should not be committed to GitHub. Keep the Kaggle link and download instructions instead.

## Notebook Plan

The project follows a clean Steam dataset notebook storyline.

Main notebook sequence:

1. `notebooks/01_steam_dataset_overview.ipynb`
   - Introduce the Steam dataset.
   - Verify expected files under `data/raw/archive/`.
   - Show file sizes, row counts, columns, sample rows, and data types.
   - Explain why large CSV files require careful reading strategies.
   - Include commented download instructions.

2. `notebooks/02_large_table_processing_strategy.ipynb`
   - Compare practical large-table processing strategies.
   - Focus on `pandas`, `duckdb`, and `polars`.
   - Use `pyarrow` for Parquet conversion where useful.
   - Compare selected-column loading, filtering, groupby aggregation, memory use, and CSV vs Parquet strategy.
   - Keep tool comparison useful but not larger than the Steam market analysis itself.

3. `notebooks/03_steam_data_cleaning_and_features.ipynb`
   - Standardize column names such as `AppID` vs `appid`.
   - Check missing values, duplicates, abnormal values, and date parsing.
   - Clean numeric fields such as price, reviews, playtime, and peak CCU.
   - Create features such as game age, free/paid flag, platform count, review count, positive-rate features, text length, genre count, tag count, and language count.
   - Process multi-label fields such as `genres`, `categories`, `tags`, `developers`, and `publishers`.
   - Save feature data to `data/processed/`.

4. `notebooks/04_steam_market_structure_analysis.ipynb`
   - Analyze Steam game market structure.
   - Study price distribution, free vs paid games, platform support, genres, tags, developers, publishers, and review volume.

5. `notebooks/05_steam_reviews_popularity_analysis.ipynb`
   - Analyze review metrics, positive rates, recommendations, peak CCU, playtime, and release-year trends.
   - Compare May 2024 and March 2025 snapshots where useful.

6. `notebooks/06_steam_tag_genre_positioning_analysis.ipynb`
   - Analyze Steam tags and genres as market-positioning signals.
   - Study tag frequency, tag co-occurrence, competition, and high-feedback tag groups.
   - Connect tag/genre structure to future similarity recommendation ideas.

7. `notebooks/07_report_synthesis.ipynb`
   - Summarize methodology, processing strategy, cleaning workflow, feature engineering, major findings, limitations, and future work.
   - This notebook should be Markdown-heavy and suitable for course report writing.

Optional final extension outside the main notebook storyline:

- Build a simple Steam game similarity recommender using tags, genres, categories, and descriptions.
- This should be implemented later as a script or small app, not as part of the core big-data analysis notebooks.

## Notebook Style Guidelines

- All notebook Markdown explanations, analysis comments, and conclusions should be written in Chinese.
- Figure titles and axis labels may stay in English to avoid Chinese font rendering issues in Matplotlib.
- Each major step should follow the Kaggle-style pattern: Chinese Markdown explanation, Python code, visible table/figure output, and Chinese interpretation.
- Keep notebooks focused and incremental. Do not put all analysis into one huge notebook.
- Save generated figures to `figures/`.
- Save reusable processed datasets to `data/processed/`.
- Do not run large downloads automatically inside notebooks; keep download code commented.
- Do not commit raw CSV files or downloaded Kaggle archives.
- Do not build the final recommendation system until the analysis notebooks are complete.

## Project Structure

```text
Ultimate_Game_Insights/
├── data/
│   ├── raw/
│   │   └── archive/
│   └── processed/
├── notebooks/
├── figures/
├── scripts/
├── reports/
├── README.md
├── requirements.txt
└── .gitignore
```

## Environment Setup

Create and activate a virtual environment on macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

If you install or remove Python packages later, update the dependency file:

```bash
pip freeze > requirements.txt
```

## Core Dependencies

The Steam version of this project uses:

- `pandas`, `numpy`: baseline data analysis
- `matplotlib`, `seaborn`: visualization
- `scikit-learn`: later feature scaling, PCA, clustering, and possible similarity experiments
- `jupyter`, `notebook`, `ipykernel`: notebook workflow
- `polars`: high-performance DataFrame processing
- `duckdb`: SQL-based analytics over large CSV/Parquet files
- `dask[dataframe]`: chunked/distributed-style DataFrame processing
- `pyarrow`: columnar data and Parquet support
- `psutil`: memory and CPU measurement for benchmarks
- `kagglehub`: optional Kaggle dataset download helper

## Run Notebooks

Start Jupyter Notebook from the project root:

```bash
jupyter notebook
```

Then follow the new Steam notebook sequence:

```text
notebooks/01_steam_dataset_overview.ipynb
notebooks/02_large_table_processing_strategy.ipynb
notebooks/03_steam_data_cleaning_and_features.ipynb
notebooks/04_steam_market_structure_analysis.ipynb
notebooks/05_steam_reviews_popularity_analysis.ipynb
notebooks/06_steam_tag_genre_positioning_analysis.ipynb
notebooks/07_report_synthesis.ipynb
```
