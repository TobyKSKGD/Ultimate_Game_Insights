# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a **notebook-first data analysis project** for a university big-data course. It analyzes the Kaggle **Steam Games Dataset 2025** to answer two research questions:

1. What kinds of Steam games are more likely to gain player attention?
2. How did the Steam game market change between May 2024 and March 2025 snapshots?

The project is an analysis workflow, not a production software system. All analysis is descriptive, not causal or predictive.

Read `reports/project_brief.md` for the full operational context — it is the authoritative reference for rules, notebook status, generated outputs, and agent collaboration guidelines.

## Commands

```bash
# Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start Jupyter to run notebooks
jupyter notebook

# Freeze dependencies after adding/removing packages
pip freeze > requirements.txt

# Compile the LaTeX report (requires tectonic)
tectonic --synctex --keep-logs --keep-intermediates --outdir reports/latex_build reports/latex/main.tex
```

There are no tests, linters, or build scripts — this is a pure notebook analysis project.

## Architecture: data flow and notebook pipeline

The 8 notebooks form a linear pipeline. Each depends on the outputs of previous notebooks, so they must be run in order.

```
Raw CSV (data/raw/archive/, ~1.7GB, NOT committed)
    │
    ├─ 01: Dataset overview, field inspection, file selection
    │       Decides: March 2025 = main, May 2024 = comparison snapshot
    │
    ├─ 02: Tool comparison (pandas vs duckdb vs polars)
    │       Output: data/processed/steam_march2025_selected.parquet (ignored, large)
    │
    ├─ 03: Data cleaning, feature engineering, quality report
    │       Output: data/processed/steam_march2025_features.parquet (89,618 rows × 63 cols, ignored)
    │
    ├─ 04: Market structure analysis (release trends, price, platforms, genres, long-tail)
    │
    ├─ 05: Reviews and popularity analysis (review counts, positive rates, attention metrics)
    │
    ├─ 06: Tag/genre positioning analysis (tag competition, co-occurrence, niches)
    │
    ├─ 07: Report synthesis — aggregates all findings into final_report_summary.md
    │
    └─ 08: Sales proxy and publishing strategy (estimated_owners as sales proxy)
```

All notebooks save figures to `figures/` and small summary CSVs to `data/processed/`.

## Key data rules

- **Raw CSVs** (`data/raw/archive/`) and **generated Parquet files** (`data/processed/*.parquet`) are git-ignored. They are reproducible by rerunning notebooks 01–03.
- **Small summary CSVs** in `data/processed/` are committed.
- The main analysis table is `games_march2025_cleaned.csv` (89,619 rows).
- `estimated_owners` is a bucketed owner range from the dataset, NOT official sales data. It can be used as a descriptive proxy with clear caveats.

## Notebook conventions

- Markdown explanations, analysis comments, and conclusions must be in **Chinese**.
- Figure titles and axis labels use **English** (to avoid Matplotlib Chinese font issues).
- Download code for Kaggle data must remain **commented out** to avoid repeated downloads.
- Keep notebooks focused and incremental — Kaggle-style: explanation → code → output → interpretation.
- Do not overwrite existing notebooks unless explicitly requested.

## LaTeX report

- Source: `reports/latex/main.tex` (uses `ctexart` with `fontset=fandol`)
- Build output: `reports/latex_build/main.pdf`
- Engine: `tectonic` (configured in `.vscode/settings.json` for build-on-save)
- LaTeX intermediates (`.aux`, `.log`, `.out`, `.toc`, `.synctex.gz`) are git-ignored
- Name on cover: `张思拓`, Student ID: `2025134009`
