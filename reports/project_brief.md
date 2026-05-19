# Project Brief: SteamScope

This document stores the current project memory and decision rationale. Future work should read this file before creating new notebooks or changing the project direction.

## Working Title

Recommended English title:

**SteamScope: Large-scale Steam Game Market and Popularity Analysis**

Recommended Chinese title:

**基于大规模 Steam 游戏数据的市场结构、玩家反馈与平台生态变化分析**

Alternative English title:

**Ultimate Game Insights: Large-scale Steam Game Market Analysis**

The project repository can remain named `Ultimate_Game_Insights`, but the report and notebook storyline should use the SteamScope title.

## Core Research Questions

The project should not be a loose collection of charts. It should answer two connected questions:

1. **What kinds of Steam games are more likely to gain player attention?**
2. **How did the Steam game market change between the May 2024 and March 2025 dataset snapshots?**

The course-friendly framing is:

> Transform complex large-scale Steam game tables into decision-oriented insights about market structure, player feedback, popularity, and platform ecosystem changes.

## Project Positioning

This is a Big Data Processing and Analysis course project. It is primarily a notebook-based data analysis project, not a full software system.

The dataset is large enough for a course-level big-table processing project because the raw CSV files total about 1.7GB and contain:

- multiple time snapshots,
- tens of thousands of games,
- long text columns,
- mixed numerical, categorical, Boolean, time, and text fields,
- multi-label columns,
- review and popularity indicators,
- platform support information.

The analysis should emphasize both:

- **big-table processing ability**, and
- **Steam market/player insight**.

Tool benchmarking is a highlight, not the main story. The main story is Steam game market structure and player attention.

## Three Narrative Lines

### A. Large-scale Table Processing Capability

Show that the project can handle large CSV files responsibly:

- file size and row count inspection,
- selected-column reading,
- sampling,
- memory-aware processing,
- practical comparison of table tools,
- CSV to Parquet conversion for repeated analysis.

Recommended tools:

- `pandas` as the familiar baseline,
- `duckdb` for SQL-style large CSV queries,
- `polars` for high-performance DataFrame operations,
- `pyarrow` for Parquet conversion and columnar storage,
- `psutil` for memory measurement.

`dask` can be mentioned or lightly tested, but it should not become an environment-heavy distraction unless clearly useful.

### B. Steam Market Structure Analysis

Analyze the supply side of the Steam market:

- release trends,
- price structure,
- free vs paid games,
- platform support (`windows`, `mac`, `linux`),
- genre/category/tag distribution,
- developer and publisher long-tail structure,
- 2024 vs 2025 snapshot changes.

The report should explain how Steam is not just a list of games, but a market ecosystem with head games, long-tail games, platform constraints, genre clusters, and tag-based positioning.

### C. Player Feedback and Popularity Mechanisms

Analyze what relates to player attention and feedback:

- `positive`, `negative`, `pct_pos_total`,
- `num_reviews_total`, `num_reviews_recent`,
- `recommendations`,
- `peak_ccu`,
- `average_playtime_forever`,
- `median_playtime_forever`,
- price, platform count, genre/tag count, release age.

The project should avoid claiming causality. It should describe associations and patterns:

- Which features are associated with more reviews?
- Which types/tags have higher positive rates?
- Are free games more visible but not necessarily better received?
- Are certain platform or genre combinations associated with higher engagement?

## Reference Literature Takeaways

The papers in `reports/references/` should guide framing, not force the project into heavy modeling.

### Predicting the Popularity of Games on Steam

Useful for framing popularity as a measurable target. It suggests that Steam game popularity can be studied through variables such as price, release date, language support, genre/category information, and player activity.

Project implication:

- Use `peak_ccu`, `recommendations`, `num_reviews_total`, and review counts as popularity/attention proxies.
- Analyze related factors descriptively rather than jumping directly into prediction.

### Data-Driven Classifications of Video Game Vocabulary

Useful for understanding Steam tags and genres as player-facing vocabulary rather than ordinary categories.

Project implication:

- Treat `tags`, `genres`, and `categories` as market-positioning signals.
- Analyze tag frequency, tag co-occurrence, and tag/genre positioning.
- Notebook 06 should be more than “Top tags”; it should discuss competition and positioning.

### Enhancing Game Review Sentiment Classification on Steam Platform with Attention-Based BiLSTM

Useful for emphasizing Steam reviews as player feedback.

Project implication:

- This project does not need BiLSTM or deep learning.
- Use available aggregate fields such as `positive`, `negative`, `pct_pos_total`, `pct_pos_recent`, and review counts as lightweight feedback indicators.
- Mention review sentiment modeling as a possible future extension.

### Category-based and Popularity-guided Video Game Recommendation / CPGRec+

Useful for final extension thinking. These papers suggest recommendation should balance category relevance, popularity, personalization, and long-tail discovery.

Project implication:

- Do not build the recommender inside the main analysis notebooks.
- The main notebooks should prepare clean features that could support a future recommender.
- A later recommender can use tags, genres, categories, descriptions, and popularity signals.
- Avoid recommending only the most popular games; diversity and category balance should be considered.

## Notebook Storyline

The notebook plan should be organized by research questions, not just mechanical steps.

### 01_steam_dataset_overview.ipynb

Research question:

**Why is this dataset suitable for a Big Data Processing course project?**

Content:

- dataset source and local structure,
- commented download instructions,
- file sizes and row counts,
- columns and data types,
- sample rows,
- large CSV reading risks,
- selection of main analysis files.

### 02_large_table_processing_strategy.ipynb

Research question:

**How should we process 1.7GB of Steam CSV data efficiently and reproducibly?**

Content:

- practical comparison of `pandas`, `duckdb`, and `polars`,
- selected-column reads,
- filtering,
- groupby aggregation,
- memory/time measurement,
- CSV vs Parquet strategy,
- final decision for the main processing tool.

Avoid:

- an overly heavy five-tool benchmark that distracts from Steam analysis.

### 03_steam_data_cleaning_and_features.ipynb

Research question:

**How can raw Steam CSV tables be transformed into a reliable analytical dataset?**

Content:

- unify `AppID` / `appid`,
- date parsing,
- duplicate checks,
- missing value checks,
- abnormal value checks,
- numeric conversion,
- multi-label cleanup,
- feature engineering,
- output feature Parquet/CSV.

### 04_steam_market_structure_analysis.ipynb

Research question:

**What does the Steam game market structure look like?**

Content:

- release trend,
- price distribution,
- free vs paid games,
- platform support,
- genre/category/tag distribution,
- developer/publisher long tail,
- market concentration.

### 05_steam_reviews_popularity_analysis.ipynb

Research question:

**Which game attributes are associated with player attention and feedback?**

Content:

- positive rate,
- review count,
- recommendations,
- peak CCU,
- playtime,
- relationships with price, platform support, genres, tags, and release age.

### 06_steam_tag_genre_positioning_analysis.ipynb

Research question:

**How do Steam tags and genres describe market positioning and competition?**

Content:

- tag frequency,
- genre/tag co-occurrence,
- high-feedback tag groups,
- low-competition/high-feedback niches,
- independent game positioning insights.

### 07_report_synthesis.ipynb

Research question:

**What are the final course-report findings from processing and analyzing the Steam dataset?**

Content:

- dataset and processing workflow,
- tool strategy,
- cleaning and feature engineering,
- market structure findings,
- player feedback/popularity findings,
- tag and positioning findings,
- limitations,
- future recommender direction.

## Future Recommender Boundary

A Steam game similarity recommender is a good final extension, but it should not be part of the core notebook analysis sequence.

Possible later implementation:

- script or small app under `scripts/`,
- user inputs a game name,
- system recommends similar games,
- features may include `tags`, `genres`, `categories`, `short_description`, `about_the_game`, and popularity/quality filters,
- possible method: TF-IDF + cosine similarity,
- recommendation should consider category relevance and not only popularity.

In the report, this should be described as future work or a post-analysis extension.

## Important Implementation Rules

- Notebook Markdown and explanations should be in Chinese.
- Figure titles and axes can use English to avoid font issues.
- Do not automatically download the large Kaggle dataset in every run.
- Keep Kaggle download code commented in Notebook 01.
- Raw data lives under `data/raw/archive/` and must not be committed.
- Save reusable processed data to `data/processed/`.
- Save figures to `figures/`.
- Prefer practical and explainable processing over overly complex tooling.
- Avoid turning the project into a generic “Steam data EDA” notebook dump.
- Avoid causal claims unless the analysis supports them.
- Make every notebook answer a clear question.

