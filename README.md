# Ultimate_Game_Insights

## Project Vision

Ultimate_Game_Insights is a personal final project for a Big Data Processing and Analysis course. The project uses the Kaggle Ultimate Games Dataset to explore game metadata, ratings, platforms, genres, tags, popularity, and engagement indicators.

The main goal is to demonstrate a clear, step-by-step data analysis workflow with AI-assisted development. The project is intentionally organized as a series of Jupyter Notebooks, similar to Kaggle-style data analysis notebooks: each notebook should contain Chinese Markdown explanations, executable Python code, visible outputs, saved figures, and report-ready findings.

Although the dataset is not "big data" in the strict distributed-computing sense, it is still suitable for a course project because it contains 15,000 games, 43 original fields, multi-label columns, mixed data types, missing values, text fields, time fields, and multiple behavioral indicators. The project should present it as a medium-scale, heterogeneous dataset that can be processed with big-data thinking: data cleaning, data type recognition, feature engineering, exploratory analysis, visualization, time-based analysis, and AI-assisted workflow documentation.

Course alignment:

- Chapter 2: use AI agents and vibe coding as part of the development workflow, while keeping code runnable and results verifiable.
- Chapter 3: follow a data analysis framework and explicitly recognize data types.
- Chapter 4: focus on tabular data understanding, cleaning, feature construction, and visualization.
- Chapter 5: add time-oriented analysis using `release_date` and `release_year`.

Important project rule for future assistants: this is primarily a notebook-based data analysis project, not a full software system. Avoid over-engineering, avoid unnecessary dependencies, and do not turn the project into a complex application unless the user explicitly asks for that.

## Dataset

Dataset source: Kaggle Ultimate Games Dataset.

dataset: https://www.kaggle.com/datasets/rudrakumargupta/ultimate-games-dataset-15k-games-43-features/data

Place the raw CSV file at:

```bash
data/raw/Ultimate_Games_Dataset.csv
```

If the raw data file is too large for GitHub, keep only the Kaggle source link in the project documentation and do not upload the original CSV.

## Notebooks

Current progress:

- `notebooks/01_initial_eda.ipynb`: initial data exploration, basic quality checks, light preprocessing, basic feature engineering, and first-round visualizations.
- `notebooks/02_deeper_analysis.ipynb`: deeper analysis of genres, platforms, release years, tags, text-derived features, numeric correlations, and saved feature data.

Recommended next notebooks:

- `notebooks/03_temporal_trend_analysis.ipynb`: a dedicated time-oriented analysis notebook aligned with the course chapter on time series data. It should analyze release year/date trends, rolling release counts, decade cohorts, genre changes over time, rating/popularity/engagement changes over time, and possible abnormal years. This should remain exploratory and should not implement complex forecasting.
- `notebooks/04_segmentation_and_pca.ipynb`: optional later notebook for simple unsupervised analysis. It can use standardized numeric features, PCA for 2D visualization, and basic clustering to describe game groups. This should be framed as exploratory grouping, not as a recommendation system.
- `notebooks/05_report_synthesis.ipynb`: optional final notebook that collects key figures and findings into a report-ready storyline, including limitations and future work.

`notebooks/01_initial_eda.ipynb` includes:

- Python environment and package version checks
- Dataset loading from `data/raw/Ultimate_Games_Dataset.csv`
- Basic data overview, including shape, column types, missing values, and field categories
- Missing value, duplicate, and basic range checks
- Gentle preprocessing for dates, numeric fields, and multi-label columns
- Basic feature engineering for genre count, platform count, tag count, description length, release decade, and recent-game flags
- Initial visualizations saved to `figures/`
- Preliminary findings based on the executed notebook outputs

`notebooks/02_deeper_analysis.ipynb` includes:

- Multi-label processing for genres, platforms, and tags
- Genre-level rating, popularity, and engagement analysis
- Single-platform vs multi-platform comparison
- Release year and release decade trend analysis
- Tag count and description length analysis
- Numeric feature correlation analysis
- Feature dataset export to `data/processed/Ultimate_Games_Dataset_features.csv`

## Notebook Style Guidelines

- All notebook Markdown explanations, analysis comments, and conclusions should be written in Chinese so the student and teacher can read them easily.
- Figure titles and axis labels may stay in English to avoid Chinese font rendering problems in Matplotlib.
- Each major step should follow the Kaggle-style pattern: Chinese Markdown explanation, Python code, visible table/figure output, and Chinese interpretation.
- Keep notebooks focused and incremental. Do not put all analysis into one large notebook.
- Prefer `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `jupyter`, `notebook`, and `ipykernel`. Do not add new dependencies unless there is a clear reason.
- If a new Python package is added, update `requirements.txt` with `pip freeze > requirements.txt`.
- Do not train complex machine learning models, build a recommendation system, or implement prediction tasks unless the user explicitly asks for a later extension.
- Preserve previous notebooks. Create new notebooks for new analysis stages instead of overwriting earlier work.
- Save generated figures to `figures/`.
- Save reusable processed datasets to `data/processed/`.

## Suggested Next Step

The strongest next step is `03_temporal_trend_analysis.ipynb`.

Reason: the first two notebooks already cover the course topics of tabular data understanding, missing values, multi-label fields, basic feature engineering, visualization, and correlation analysis. The course materials also include a chapter on time series data. A dedicated temporal notebook would show that the project applies the lecture content beyond generic EDA.

Suggested contents for Notebook 03:

- Load `data/processed/Ultimate_Games_Dataset_features.csv` first, and fall back to `data/raw/Ultimate_Games_Dataset.csv` if needed.
- Recheck `release_date`, `release_year`, and `release_decade`.
- Analyze yearly release counts and decade-level release counts.
- Add rolling averages for yearly game releases.
- Compare average `user_rating`, `metacritic`, `popularity_score`, and `engagement_score` by year and decade.
- Analyze genre composition changes over time, especially the top genres.
- Analyze platform expansion over time using `platform_count_check` or `platform_count`.
- Identify abnormal years with unusually high or low release counts using simple z-score or IQR logic.
- Save all figures to `figures/` with filenames beginning from `23_`.
- End with Chinese, report-ready findings and limitations.

Avoid in Notebook 03:

- Complex forecasting models.
- Recommendation systems.
- Heavy NLP.
- New dependencies.

## Project Structure

```text
Ultimate_Game_Insights/
├── data/
│   ├── raw/
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

Install the basic dependencies:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter notebook ipykernel
```

After installing dependencies, update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Whenever you add a new Python package later, run this command again:

```bash
pip freeze > requirements.txt
```

## Run the Notebook

Start Jupyter Notebook from the project root:

```bash
jupyter notebook
```

Then open:

```text
notebooks/01_initial_eda.ipynb
notebooks/02_deeper_analysis.ipynb
```
