# Project Brief for Future Agents

This file is the working memory for agents continuing the `Ultimate_Game_Insights` project. The public-facing README is intentionally written in Chinese for repository visitors. This brief is more operational and can be updated whenever the project direction or implementation details change.

## 1. Project Identity

- Repository/project name: `Ultimate_Game_Insights`
- Course: Big Data Processing Technology / Big Data Processing and Analysis
- Report topic in Chinese: `基于大规模 Steam 游戏数据的市场结构、玩家反馈与平台生态变化分析`
- Report storyline title: `SteamScope: Large-scale Steam Game Market and Popularity Analysis`
- The repository name should remain `Ultimate_Game_Insights`; do not rename the project to SteamScope.

The project is a notebook-first data analysis project, not a production software system. The goal is to show a clear, reproducible, report-ready workflow for processing and analyzing a large Steam game dataset.

## 2. Core Research Questions

The project should not become a loose EDA collection. Keep the analysis connected to these two questions:

1. What kinds of Steam games are more likely to gain player attention?
2. How did the Steam game market change between the May 2024 and March 2025 dataset snapshots?

Course-friendly framing:

> Transform complex large-scale Steam game tables into decision-oriented insights about market structure, player feedback, popularity, and platform ecosystem changes.

## 3. Audience and Writing Rules

### README

- Must be in Chinese.
- It is for third-party repository visitors, not for the owner or the agent.
- Tone should be clear and natural, not chatty, and not overly academic.
- Keep operational or agent-specific details in this file instead.

### Notebooks

- Notebook Markdown explanations, analysis comments, and conclusions must be in Chinese.
- Figure titles and axis labels may use English to avoid Chinese font issues in Matplotlib.
- Use a Kaggle-style rhythm: Chinese Markdown explanation, Python code, visible table/figure output, then Chinese interpretation.
- Keep notebooks focused and incremental.
- Save figures to `figures/`.
- Save reusable small outputs to `data/processed/`.
- Do not run large dataset downloads automatically; keep download code commented.

### Final Report

- The final written report is in Chinese and uses LaTeX.
- The student should write the core arguments because the course does not allow AI to replace the student's own core viewpoints.
- Agent assistance should focus on formatting, structure, local wording polish, reproducibility, and technical LaTeX support.

## 4. Dataset

Dataset source:

- Kaggle: `artermiloff/steam-games-dataset`
- Public URL: <https://www.kaggle.com/datasets/artermiloff/steam-games-dataset>

Local raw data path:

```text
data/raw/archive/
```

Expected raw files:

```text
data/raw/archive/
├── games_march2025_cleaned.csv
├── games_march2025_full.csv
├── games_may2024_cleaned.csv
└── games_may2024_full.csv
```

Approximate local file sizes:

- `games_march2025_cleaned.csv`: about 447MB
- `games_march2025_full.csv`: about 450MB
- `games_may2024_cleaned.csv`: about 403MB
- `games_may2024_full.csv`: about 405MB

Approximate row counts:

- `games_march2025_cleaned.csv`: 89,619 rows including header
- `games_march2025_full.csv`: 94,949 rows including header
- `games_may2024_cleaned.csv`: 83,647 rows including header
- `games_may2024_full.csv`: 87,807 rows including header

Main analysis file:

- `data/raw/archive/games_march2025_cleaned.csv`

Snapshot comparison file:

- `data/raw/archive/games_may2024_cleaned.csv`

Important fields include:

- Basic identifiers: `appid`, `name`, `release_date`
- Platforms: `windows`, `mac`, `linux`
- Price/package fields: `price`, `discount`, `dlc_count`, `packages`
- Reviews and ratings: `positive`, `negative`, `user_score`, `metacritic_score`, `pct_pos_total`, `num_reviews_total`, `pct_pos_recent`, `num_reviews_recent`
- Popularity proxies: `recommendations`, `peak_ccu`
- Ownership/sales proxy: `estimated_owners`; this is an estimated owner range, not official Steam sales.
- Playtime: `average_playtime_forever`, `average_playtime_2weeks`, `median_playtime_forever`, `median_playtime_2weeks`
- Multi-label fields: `genres`, `categories`, `tags`, `developers`, `publishers`, `supported_languages`, `full_audio_languages`
- Text fields: `detailed_description`, `about_the_game`, `short_description`, `reviews`

## 5. Data and Git Policy

Do not commit:

- raw Kaggle CSVs under `data/raw/archive/`,
- downloaded dataset archives,
- generated Parquet files under `data/processed/`,
- LaTeX intermediate files such as `.aux`, `.log`, `.out`, `.toc`, `.synctex.gz`.

Commit when useful:

- notebooks,
- README and project documents,
- generated figures,
- small summary CSV files,
- LaTeX source files,
- final PDF files when ready for submission.

Large processed Parquet files are reproducible. If they are missing, rerun the generating notebook instead of trying to track them in Git.

## 6. Environment

Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

When dependencies change:

```bash
pip freeze > requirements.txt
```

Key Python packages currently used:

- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `duckdb`, `polars`, `pyarrow`
- `psutil`
- `jupyter`, `notebook`, `ipykernel`
- `scikit-learn`
- `kagglehub`

## 7. Notebook Status

The main notebook sequence is complete from `01` to `08`.

### 01_steam_dataset_overview.ipynb

Purpose:

- introduce the dataset,
- show download instructions as commented code,
- verify expected files under `data/raw/archive/`,
- inspect file sizes, row counts, column structures, data types, and sample rows,
- explain why large CSV files need careful reading strategies,
- choose March 2025 cleaned data as the main analysis table and May 2024 cleaned data as the comparison snapshot.

### 02_large_table_processing_strategy.ipynb

Purpose:

- compare practical large-table processing with `pandas`, `duckdb`, and `polars`,
- measure selected-column reads, filtering, grouping, time, and memory,
- convert selected fields to Parquet,
- show why columnar files are useful for repeated analysis.

Keep tool comparison as a supporting capability, not the main story.

### 03_steam_data_cleaning_and_features.ipynb

Purpose:

- standardize fields,
- check missing values, duplicate rows, duplicate `appid`, and abnormal ranges,
- parse dates and numeric fields,
- treat Steam percentage sentinel values such as `-1` as missing in percentage columns,
- process multi-label fields,
- engineer analysis features such as release year, game age, free/paid flag, platform count, review count, positive-rate metrics, text lengths, and multi-label counts,
- save reusable feature data and quality reports.

Important output:

- `data/processed/steam_march2025_features.parquet`
- Shape after creation: 89,618 rows and 63 columns
- This file is larger than GitHub's 100MB limit and must stay ignored.

### 04_steam_market_structure_analysis.ipynb

Purpose:

- analyze release trends,
- analyze price and free/paid structure,
- summarize platform support,
- analyze genres, categories, tags,
- examine developer and publisher long-tail concentration,
- compare May 2024 and March 2025 market structure.

Current findings to preserve:

- Main feature dataset contains 89,618 games.
- Valid release-year range used in plots: 1997 to 2025.
- The largest release year is 2024, with 18,282 games.
- Free games account for about 15.80%.
- Multi-platform games account for about 23.05%.
- Top genre: `Indie`.
- Top category: `Single-player`.
- Top tag: `Indie`.
- Developer and publisher distributions are long-tailed.
- Top 100 developers cover about 6.87% of developer-game assignments.
- Top 100 publishers cover about 11.44% of publisher-game assignments.
- May 2024 cleaned snapshot has 83,646 unique AppIDs.
- March 2025 cleaned snapshot has 89,618 unique AppIDs.

Visual refinement note:

- The free-vs-paid comparison should remain a clean donut chart with counts and shares in the legend.
- The final summary cell is robust to kernel restarts and can reload the minimum required data.

### 05_steam_reviews_popularity_analysis.ipynb

Purpose:

- analyze review counts, positive rates, recommendations, peak CCU, and playtime,
- distinguish popularity scale from feedback quality,
- use `log1p` transformations for highly skewed attention metrics,
- use a 30-review threshold for more stable positive-rate interpretation,
- compare price buckets, free/paid status, platform count, genres, release year, and game age against feedback/popularity metrics,
- build a descriptive composite attention score,
- compare May 2024 and March 2025 feedback/popularity snapshots.

Current findings to preserve:

- Total games: 89,618.
- Games with at least one review: 72,563.
- Games with 30 or more reviews: 33,358.
- Review counts are highly long-tailed.
- Median review count is 13.
- Mean review count is about 1,479.70.
- Among games with at least 30 reviews, median positive rate is about 81.08%.
- Recommendations and peak CCU are also highly long-tailed, with median 0 in the full dataset.
- Total review count increased from 124,126,364 in May 2024 to 132,607,623 in March 2025.

Do not make causal claims. This notebook is descriptive.

### 06_steam_tag_genre_positioning_analysis.ipynb

Purpose:

- treat tags, genres, and categories as market-positioning signals,
- analyze tag frequency, tag competition, high-feedback niches, high-attention tags, genre-tag positioning, and tag co-occurrence,
- connect the analysis to the optional future similarity recommender.

Current findings to preserve:

- Parsed 33 genres, 40 categories, and 452 tags.
- Average tags per game: about 11.26.
- Top genre: `Indie`.
- Top category: `Single-player`.
- Top tag: `Indie`.
- `Sokoban` appears as a low-competition/high-feedback tag candidate under the notebook thresholds.
- `Games Workshop` appears as a high descriptive-attention tag candidate.
- One strong top-tag co-occurrence pair is `Indie + Singleplayer`.
- In Indie-positioned games, `Short` is relatively over-represented by lift.

The notebook exports a small positioning feature sample for future recommender design, but it does not implement the recommender.

### 07_report_synthesis.ipynb

Purpose:

- synthesize the full notebook sequence into a report-facing narrative,
- check key report resources,
- generate a notebook workflow figure,
- summarize dataset scale, processing strategy, cleaning, feature engineering, market structure, feedback/popularity, tag positioning, limitations, and future recommender direction.

Important outputs:

- `figures/38_report_notebook_workflow.png`
- `reports/final_report_summary.md`

### 08_sales_proxy_publishing_strategy.ipynb

Purpose:

- parse `estimated_owners` into lower bound, upper bound, and midpoint,
- use the midpoint as a descriptive sales proxy for buyout/paid games,
- keep the caveat that `estimated_owners` is not official sales data,
- compare sales proxy with review count, recommendations, and peak CCU,
- analyze buyout game price buckets and rough gross revenue proxy,
- summarize genre and tag patterns for indie buyout games,
- summarize discussion-oriented metrics for large publishers,
- summarize feedback and engagement signals for free live-service style games,
- export report-friendly strategy tables and figures.

Important outputs:

- `figures/39_estimated_owners_bucket_distribution.png`
- `figures/40_sales_proxy_vs_discussion_metrics.png`
- `figures/41_buyout_price_bucket_sales_proxy.png`
- `figures/42_buyout_genre_sales_proxy.png`
- `figures/43_indie_tag_sales_proxy_candidates.png`
- `figures/44_discussion_score_by_price_bucket.png`
- `figures/45_free_game_tag_feedback_engagement.png`
- `data/processed/steam_sales_proxy_publishing_strategy_summary.csv`

Current notes:

- The notebook is descriptive and should not be framed as sales prediction.
- For buyout games, `estimated_owners` midpoint is treated as a sales proxy.
- For free games, `estimated_owners` should be interpreted as estimated reach/ownership, not sales revenue.
- Strategy displays should not hide adult/mature tags. Treat them as real Steam market signals, but discuss them neutrally as a special segment that may also reflect low-quality supply concentration and tag saturation.

## 8. Generated Outputs

Main generated figures:

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
- `figures/39_estimated_owners_bucket_distribution.png`
- `figures/40_sales_proxy_vs_discussion_metrics.png`
- `figures/41_buyout_price_bucket_sales_proxy.png`
- `figures/42_buyout_genre_sales_proxy.png`
- `figures/43_indie_tag_sales_proxy_candidates.png`
- `figures/44_discussion_score_by_price_bucket.png`
- `figures/45_free_game_tag_feedback_engagement.png`

Small summary outputs under `data/processed/` include:

- `large_table_processing_benchmark.csv`
- `steam_data_quality_report.csv`
- `steam_march2025_features_sample.csv`
- review/popularity summary CSV files,
- tag/genre positioning summary CSV files.
- sales-proxy and publishing-strategy summary CSV files.

Large ignored outputs include:

- `steam_march2025_selected.parquet`
- `steam_march2025_yearly_summary.parquet`
- `steam_march2025_features.parquet`

## 9. Reference Literature Takeaways

Reference papers live in `reports/references/`. They guide framing but should not force the project into heavy modeling.

### Predicting the Popularity of Games on Steam

Useful for framing popularity as measurable through price, release date, language support, category information, player activity, and attention proxies.

Project implication:

- Use `peak_ccu`, `recommendations`, `num_reviews_total`, and review counts as popularity or attention proxies.
- Analyze related factors descriptively before considering prediction.

### Data-Driven Classifications of Video Game Vocabulary

Useful for treating Steam vocabulary as player-facing positioning information.

Project implication:

- Treat `tags`, `genres`, and `categories` as market-positioning signals.
- Analyze tag frequency, co-occurrence, and tag/genre positioning instead of only showing top tags.

### Enhancing Game Review Sentiment Classification on Steam Platform with Attention-Based BiLSTM

Useful for explaining why Steam reviews are player feedback signals.

Project implication:

- Do not add deep learning to the current notebook sequence.
- Use aggregate fields such as `positive`, `negative`, `pct_pos_total`, `pct_pos_recent`, and review counts as lightweight feedback indicators.
- Mention sentiment modeling as future work only.

### Category-based and Popularity-guided Video Game Recommendation / CPGRec+

Useful for a future recommender extension.

Project implication:

- Keep recommender work outside the main notebook storyline.
- A later recommender can use tags, genres, categories, descriptions, and popularity/quality filters.
- Avoid recommending only the most popular games; diversity and category balance should be considered.

## 10. LaTeX Report Environment

Report source:

- `reports/latex/main.tex`

Build output:

- `reports/latex_build/main.pdf`

Engine:

- `tectonic`

VS Code:

- Extension: `James-Yu.latex-workshop`
- Workspace settings: `.vscode/settings.json`
- Build on save is configured with `tectonic`.
- The settings use `%DOC_EXT%` rather than `%DOC%` because `tectonic` requires `main.tex`, not `main`.
- `latex-workshop.latex.build.forceRecipeUsage` is enabled.

Compile command:

```bash
tectonic --synctex --keep-logs --keep-intermediates --outdir reports/latex_build reports/latex/main.tex
```

Current LaTeX notes:

- The document uses `ctexart` with `fontset=fandol` to avoid macOS absolute-font-path warnings in Tectonic.
- `hypertexnames=false` is set to avoid duplicate PDF page object warnings.
- The cover page uses centered title/name/student ID layout.
- Name: `张思拓`
- Student ID: `2025134009`
- Course name on cover: `《大数据处理技术》课程实践报告`
- Topic on cover: `基于大规模 Steam 游戏数据的市场结构、玩家反馈与平台生态变化分析`

## 11. Sales Proxy and Publishing Strategy Notes

Notebook 08 adds a report-supporting analysis layer for publishing strategy.

Key interpretation rules:

- `estimated_owners` is an estimated owner range from the dataset, not official sales.
- It is acceptable in this course project to use the range midpoint as a descriptive sales proxy, as long as the limitation is clearly stated.
- For buyout games, the midpoint can support discussion about rough sales scale.
- For free games, the midpoint should be interpreted as estimated ownership/reach, not revenue.
- A rough gross revenue proxy can be computed as `price * estimated_owner_mid`, but it does not account for discounts, regional pricing, refunds, platform fees, taxes, bundles, DLC, or time of purchase.

Latest Notebook 08 findings to preserve:

- For buyout games, the `$40-79.99` bucket has the highest median estimated-owner midpoint in the current price-bucket summary, but it contains far fewer games than lower-price buckets.
- The `$40-79.99` bucket also has the highest median rough gross revenue proxy among standard buckets in the current summary.
- Buyout genre summaries show many major genres with the same median estimated-owner midpoint because `estimated_owners` is bucketed coarsely; avoid over-interpreting small rank differences.
- Indie buyout tag candidates include tags such as `Kickstarter`, `Touch-Friendly`, `Sequel`, `Moddable`, `Episodic`, and `Villain Protagonist` under the notebook thresholds.
- Free-game strategy summaries currently include tags such as `Idler`, `Moddable`, `Hentai`, `MMORPG`, `Mature`, `Online Co-Op`, `Trading`, and `Co-op`. Adult/mature tags should be analyzed instead of hidden, with clear caveats about platform rules, audience limits, low-quality supply concentration, and tag saturation.

Suggested report framing:

- Independent developers: discuss buyout sales proxy, price bucket, manageable tag competition, and positive-rate stability.
- Large publishers: discuss review count, recommendations, peak CCU, and discussion score rather than sales proxy alone.
- Free live-service games: discuss review volume, positive rate, peak CCU, and recommendations; do not treat estimated owners as sales revenue.

## 12. Optional Future Extension

A Steam game similarity recommender is a reasonable final extension, but it should not be part of the core big-data notebook sequence.

Possible implementation:

- create a script or small app under `scripts/`,
- user inputs a game name,
- system returns similar games,
- features may include `tags`, `genres`, `categories`, `short_description`, `about_the_game`, and popularity/quality filters,
- possible method: TF-IDF plus cosine similarity,
- recommendation should balance category relevance, popularity, and long-tail discovery.

If implemented, describe it as a post-analysis extension rather than the central course project.

## 13. Agent Checklist Before Future Work

Before creating or modifying notebooks:

1. Read `README.md` and this file.
2. Confirm whether the requested work is public-facing documentation, notebook analysis, report formatting, or future recommender work.
3. Preserve Chinese Markdown in notebooks.
4. Avoid adding new dependencies without explaining why.
5. Do not commit or ask to commit raw data or Parquet files.
6. Do not overwrite existing notebooks unless explicitly requested.
7. Keep the analysis descriptive unless a later task explicitly asks for modeling.
8. Keep the project name `Ultimate_Game_Insights`.
