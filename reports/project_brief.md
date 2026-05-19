# Project Brief: Ultimate_Game_Insights / SteamScope

This document stores the current project memory and decision rationale. Future work should read this file before creating new notebooks or changing the project direction.

## Working Title

Project name:

**Ultimate_Game_Insights**

The project name should remain `Ultimate_Game_Insights`.

Recommended English title:

**SteamScope: Large-scale Steam Game Market and Popularity Analysis**

Recommended Chinese title:

**基于大规模 Steam 游戏数据的市场结构、玩家反馈与平台生态变化分析**

Alternative English title:

**Ultimate Game Insights: Large-scale Steam Game Market Analysis**

SteamScope is the report theme and notebook storyline title. It should not replace the project/repository name.

## Current Progress

Completed notebooks:

- `notebooks/01_steam_dataset_overview.ipynb`
  - verified the expected Steam CSV files under `data/raw/archive/`,
  - recorded file sizes, row counts, column structures, and sample rows,
  - grouped fields by analytical meaning,
  - confirmed the main analysis file as `games_march2025_cleaned.csv`,
  - identified `games_may2024_cleaned.csv` as the snapshot comparison file.
- `notebooks/02_large_table_processing_strategy.ipynb`
  - compared practical large-table processing with `pandas`, `duckdb`, and `polars`,
  - created benchmark results,
  - converted selected core fields to Parquet,
  - saved a yearly summary table for later time analysis.
- `notebooks/03_steam_data_cleaning_and_features.ipynb`
  - transformed the March 2025 Steam CSV into a reusable feature dataset,
  - standardized field names and checked structure, missing values, duplicate rows, and duplicate `appid`,
  - converted date and numeric fields,
  - treated Steam percentage sentinel values such as `-1` as missing for positive-rate percentage columns,
  - parsed multi-label columns such as `genres`, `categories`, `tags`, `developers`, `publishers`, and language fields,
  - engineered analysis features such as release year, game age, free/paid flag, platform count, review count, positive-rate metrics, text lengths, and multi-label counts,
  - saved feature data and a data quality report for later notebooks.
- `notebooks/04_steam_market_structure_analysis.ipynb`
  - analyzed Steam market structure using the feature Parquet from Notebook 03,
  - studied release-year and release-decade trends,
  - analyzed free vs paid games and paid-game price distribution,
  - summarized Windows/Mac/Linux support and platform combinations,
  - parsed pipe-delimited and list-like multi-label fields for genres, categories, tags, developers, and publishers,
  - analyzed top genres, categories, and tags by game count,
  - measured developer and publisher long-tail concentration,
  - compared May 2024 and March 2025 cleaned snapshots at a light market-structure level,
  - refined the free-vs-paid comparison into a cleaner donut chart,
  - made the final summary cell robust enough to recover required data after a kernel restart.
- `notebooks/05_steam_reviews_popularity_analysis.ipynb`
  - analyzed player feedback and popularity using the feature Parquet from Notebook 03,
  - treated review count, positive rate, recommendations, peak CCU, and playtime as separate but related feedback/popularity proxies,
  - used `log1p` transformations for long-tailed attention metrics,
  - used a 30-review threshold for more stable positive-rate interpretation,
  - compared price buckets, free vs paid games, platform count, genres, release year, and game age against feedback/popularity metrics,
  - built a descriptive composite attention score from standardized log review count, recommendations, and peak CCU,
  - saved summary tables for metric, price, platform, genre, correlation, snapshot, and top-attention-game analysis,
  - compared May 2024 and March 2025 cleaned snapshots at a light feedback/popularity level.
- `notebooks/06_steam_tag_genre_positioning_analysis.ipynb`
  - analyzed Steam tags, genres, and categories as market-positioning signals,
  - treated tag game count as a descriptive competition proxy,
  - compared tag competition with median positive rate, median review count, and descriptive attention score,
  - identified low-competition/high-feedback tag candidates and high-attention tags,
  - built a genre-tag positioning matrix,
  - built top-tag co-occurrence count, Jaccard, and pair tables,
  - analyzed Indie-positioned games with tag lift,
  - exported a small positioning feature sample for future similarity recommendation design.
- `notebooks/07_report_synthesis.ipynb`
  - synthesized the full notebook sequence into a course-report narrative,
  - checked key report resources and generated a notebook workflow figure,
  - summarized dataset scale, processing strategy, data cleaning, feature engineering, market structure, feedback/popularity, and tag positioning,
  - mapped the project work to course topics,
  - documented limitations and future recommender direction,
  - exported a concise final report summary to `reports/final_report_summary.md`.

Generated intermediate files:

- `data/processed/large_table_processing_benchmark.csv`
- `data/processed/steam_march2025_selected.parquet`
- `data/processed/steam_march2025_yearly_summary.parquet`
- `data/processed/steam_march2025_features.parquet`
- `data/processed/steam_march2025_features_sample.csv`
- `data/processed/steam_data_quality_report.csv`
- `data/processed/steam_reviews_popularity_metric_summary.csv`
- `data/processed/steam_reviews_popularity_price_summary.csv`
- `data/processed/steam_reviews_popularity_platform_summary.csv`
- `data/processed/steam_reviews_popularity_genre_summary.csv`
- `data/processed/steam_reviews_popularity_correlation.csv`
- `data/processed/steam_reviews_popularity_snapshot_summary.csv`
- `data/processed/steam_reviews_popularity_top_attention_games.csv`
- `data/processed/steam_tag_positioning_summary.csv`
- `data/processed/steam_tag_niche_high_feedback_candidates.csv`
- `data/processed/steam_tag_high_attention_summary.csv`
- `data/processed/steam_genre_tag_matrix_top.csv`
- `data/processed/steam_tag_cooccurrence_counts_top.csv`
- `data/processed/steam_tag_cooccurrence_jaccard_top.csv`
- `data/processed/steam_tag_cooccurrence_pairs_top.csv`
- `data/processed/steam_indie_tag_lift_summary.csv`
- `data/processed/steam_positioning_features_sample.csv`
- `reports/final_report_summary.md`

Generated figures:

- `figures/01_steam_dataset_file_size_and_rows.png`
- `figures/02_core_columns_missing_ratio.png`
- `figures/03_csv_vs_selected_parquet_size.png`
- `figures/04_processing_time_by_tool_and_task.png`
- `figures/05_memory_delta_by_tool_and_task.png`
- `figures/06_key_feature_missing_ratio.png`
- `figures/07_market_release_trend_by_year.png`
- `figures/08_market_release_distribution_by_decade.png`
- `figures/09_price_distribution_paid_games.png`
- `figures/10_free_vs_paid_market_share.png`
- `figures/11_platform_support_counts.png`
- `figures/12_platform_combination_distribution.png`
- `figures/13_top_genres_by_game_count.png`
- `figures/14_top_categories_by_game_count.png`
- `figures/15_top_tags_by_game_count.png`
- `figures/16_top_developers_publishers_by_game_count.png`
- `figures/17_developer_publisher_long_tail_cumulative_share.png`
- `figures/18_snapshot_market_structure_comparison.png`
- `figures/19_attention_metrics_log_distributions.png`
- `figures/20_positive_rate_distribution_reliable_reviews.png`
- `figures/21_review_count_vs_positive_rate.png`
- `figures/22_popularity_proxy_relationships.png`
- `figures/23_price_bucket_feedback_popularity.png`
- `figures/24_free_paid_attention_metrics.png`
- `figures/25_platform_count_feedback_popularity.png`
- `figures/26_genre_feedback_popularity_comparison.png`
- `figures/27_release_year_feedback_trends.png`
- `figures/28_game_age_vs_review_count.png`
- `figures/29_feedback_popularity_correlation_heatmap.png`
- `figures/30_snapshot_feedback_popularity_comparison.png`
- `figures/31_tag_genre_category_frequency.png`
- `figures/32_tag_competition_vs_positive_feedback.png`
- `figures/33_niche_high_feedback_tags.png`
- `figures/34_genre_tag_positioning_heatmap.png`
- `figures/35_tag_cooccurrence_jaccard_heatmap.png`
- `figures/36_indie_tag_lift.png`
- `figures/37_tag_count_positioning_complexity.png`
- `figures/38_report_notebook_workflow.png`

Main notebook sequence status:

- Completed from `notebooks/01_steam_dataset_overview.ipynb` through `notebooks/07_report_synthesis.ipynb`.
- Optional future extension: a simple Steam similarity recommender outside the main notebook storyline.

Latest feature dataset status:

- Main reusable dataset: `data/processed/steam_march2025_features.parquet`
- Shape after Notebook 03: 89,618 rows and 63 columns
- Sample export: `data/processed/steam_march2025_features_sample.csv`
- Quality report: `data/processed/steam_data_quality_report.csv`
- Important cleaning note: percentage fields such as `pct_pos_total` and `pct_pos_recent` used `-1` as an unavailable-value marker in the source data. Notebook 03 converts these invalid percentages to missing values before range checks and downstream analysis.
- GitHub note: `steam_march2025_features.parquet` is larger than 100MB and should not be committed. It is ignored because it can be regenerated by running Notebook 03.

Repository data policy:

- Do not commit raw Kaggle data under `data/raw/archive/`.
- Do not commit downloaded dataset archives.
- Do not commit generated Parquet files under `data/processed/`.
- Commit notebooks, README/project documents, generated figures, and small summary CSV files when useful for grading.
- If a future notebook requires a missing processed Parquet file, rerun the earlier notebook that generates it.

Latest market structure findings from Notebook 04:

- Main analysis dataset: 89,618 Steam games from `steam_march2025_features.parquet`.
- Valid release-year range used in market plots: 1997 to 2025.
- The largest release year in the dataset is 2024, with 18,282 games.
- Free games account for about 15.80% of games.
- Multi-platform games account for about 23.05% of games.
- Top genre by game count: `Indie`.
- Top category by game count: `Single-player`.
- Top tag by game count: `Indie`.
- Developer and publisher distributions are long-tailed. The top 100 developers cover about 6.87% of developer-game assignments, while the top 100 publishers cover about 11.44% of publisher-game assignments.
- Snapshot comparison: May 2024 cleaned snapshot has 83,646 unique AppIDs; March 2025 cleaned snapshot has 89,618 unique AppIDs.

Latest feedback and popularity findings from Notebook 05:

- Total games: 89,618.
- Games with at least one review: 72,563.
- Games with 30 or more reviews: 33,358.
- Review counts are highly long-tailed: median review count is 13, while mean review count is about 1,479.70.
- Among games with 30 or more reviews, median positive rate is about 81.08%.
- Recommendations and peak CCU are also highly long-tailed: both have median 0 in the full dataset.
- Among genre groups with enough games, `Massively Multiplayer` has the highest median review count, while `Casual` has the highest median positive rate under the 30-review threshold.
- Snapshot comparison: total review count increased from 124,126,364 in May 2024 to 132,607,623 in March 2025.
- Notebook 05 remains descriptive; it does not train a prediction model or make causal claims.

Latest tag/genre positioning findings from Notebook 06:

- Parsed 33 genres, 40 categories, and 452 tags.
- Average tags per game: about 11.26.
- Top genre by coverage: `Indie`.
- Top category by coverage: `Single-player`.
- Top tag by coverage: `Indie`.
- `Sokoban` appears as a low-competition/high-feedback tag candidate under the notebook's thresholds.
- `Games Workshop` appears as a high descriptive-attention tag candidate under the notebook's thresholds.
- One of the strongest top-tag co-occurrence pairs is `Indie + Singleplayer`.
- In Indie-positioned games, `Short` is relatively over-represented by lift.
- Notebook 06 exports a small positioning feature sample for future recommender design, but it does not implement the recommender.

Latest synthesis output from Notebook 07:

- Notebook 07 completed the course-report narrative across all previous notebooks.
- Generated `figures/38_report_notebook_workflow.png`.
- Generated `reports/final_report_summary.md`.
- The project's main data-analysis notebook storyline is now complete.

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

Current status:

- Completed and executed.
- Output dataset: `data/processed/steam_march2025_features.parquet`.
- Later notebooks should read this Parquet file first instead of repeatedly reading the large raw CSV.

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

Current status:

- Completed, refined, and executed.
- Generated figures `07` through `18` under `figures/`.
- The free-vs-paid chart is now a donut chart with the total game count in the center and counts/shares in the legend.
- The final summary cell can reload the feature Parquet and rebuild the minimum required summary variables if the user accidentally runs it after restarting the kernel.
- This notebook is descriptive. It should not make causal claims about why games become popular.
- Later notebooks should use the market structure findings as background for player feedback and popularity analysis.

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

Current status:

- Completed and executed.
- Generated figures `19` through `30` under `figures/`.
- Generated reusable summary CSV files under `data/processed/`.
- This notebook separates popularity scale from feedback quality: high review/recommendation volume does not automatically mean higher positive rate.
- Later Notebook 06 should use these feedback/popularity findings as context for tag and genre positioning.

### 06_steam_tag_genre_positioning_analysis.ipynb

Research question:

**How do Steam tags and genres describe market positioning and competition?**

Content:

- tag frequency,
- genre/tag co-occurrence,
- high-feedback tag groups,
- low-competition/high-feedback niches,
- independent game positioning insights.

Current status:

- Completed and executed.
- Generated figures `31` through `37` under `figures/`.
- Generated reusable tag/genre positioning summary CSV files under `data/processed/`.
- This notebook connects the analysis sequence to the optional future recommender by showing which tag, genre, category, and feedback fields could support game similarity.

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

Current status:

- Completed and executed.
- Generated `figures/38_report_notebook_workflow.png`.
- Generated `reports/final_report_summary.md`.
- This notebook is the report-facing synthesis of the project and should be used as the main reference when writing the final course submission.

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
