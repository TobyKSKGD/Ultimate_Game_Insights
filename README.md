# Ultimate_Game_Insights

## Project Overview

Ultimate_Game_Insights is an initial data analysis project for a Big Data Processing course. The project uses the Kaggle Ultimate Games Dataset to explore game metadata, ratings, platforms, genres, tags, popularity, and engagement indicators.

This repository is currently organized as a Jupyter Notebook based analysis project, similar to a Kaggle EDA notebook. The first version focuses on environment setup, dataset loading, basic data understanding, quality checks, simple preprocessing, basic feature engineering, and initial visualizations.

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
