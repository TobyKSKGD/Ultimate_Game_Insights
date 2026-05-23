#!/usr/bin/env python3
"""
SteamScope Data Export Script

Exports lightweight JSON files for the static web showcase from
processed Parquet/CSV data produced by notebooks 01-08.

Run from project root:
    source .venv/bin/activate
    python steam-scope/scripts/export_steam_scope_data.py
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# ── config ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "steam-scope" / "data"

# increasing this reduces # of games in index but also shrinks JSON size
MIN_REVIEWS_FOR_INDEX = 30
MAX_INDEX_ROWS = 5000
TOP_TAGS_N = 50
TOP_GENRES_N = 30
COOCCUR_TOP_N = 40  # tags in co-occurrence graph
MAX_REC_CANDIDATES = 1000  # candidate games for recommendations (top by reviews)
TOP_K_REC = 11  # recommendations per game
MAX_SHARED_ATTRS = 5  # max shared tags/genres/categories in recommendation display


def load_main_table() -> pd.DataFrame:
    parquet_path = PROCESSED_DIR / "steam_march2025_features.parquet"
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)

    sample_path = PROCESSED_DIR / "steam_march2025_features_sample.csv"
    if sample_path.exists():
        print("WARNING: parquet not found, falling back to sample CSV")
        return pd.read_csv(sample_path)

    print("ERROR: no main table found")
    sys.exit(1)


def parse_list_column(series: pd.Series):
    """Convert pipe-delimited or semicolon-delimited string to list of strings."""
    def _parse(val):
        if pd.isna(val) or not val:
            return []
        s = str(val)
        sep = "|" if "|" in s else ";"
        return [t.strip() for t in s.split(sep) if t.strip()]
    return series.apply(_parse)


def safe_float(val, default=0.0):
    try:
        v = float(val)
        return v if np.isfinite(v) else default
    except (ValueError, TypeError):
        return default


def safe_int(val, default=0):
    try:
        v = int(val)
        return v
    except (ValueError, TypeError):
        return default


# ══════════════════════════════════════════════════════════════════════════
# 1. overview_stats.json
# ══════════════════════════════════════════════════════════════════════════

def export_overview_stats(df: pd.DataFrame):
    print("Exporting overview_stats.json ...")
    t0 = time.time()

    total = len(df)

    has_review = int((df["review_count_calc"] > 0).sum())
    has_reliable = int((df["review_count_calc"] >= 30).sum())
    free = int(df["is_free"].sum())
    paid = total - free
    free_share = round(free / total * 100, 2)

    all_tags = set()
    all_genres = set()
    all_categories = set()
    for lst in parse_list_column(df["tags_list"]):
        all_tags.update(lst)
    for lst in parse_list_column(df["genres_list"]):
        all_genres.update(lst)
    for lst in parse_list_column(df["categories_list"]):
        all_categories.update(lst)

    year_counts = df["release_year"].value_counts()
    top_year = int(year_counts.idxmax()) if len(year_counts) > 0 else 0
    top_year_count = int(year_counts.max()) if len(year_counts) > 0 else 0

    reliable = df[df["review_count_calc"] >= 30]
    median_pos_rate = (
        round(float(reliable["positive_rate_calc"].median()), 2)
        if len(reliable) > 0
        else 0
    )
    median_reviews = (
        round(float(reliable["review_count_calc"].median()), 1)
        if len(reliable) > 0
        else 0
    )

    stats = {
        "total_games": total,
        "reviewed_games": has_review,
        "reliable_review_games": has_reliable,
        "free_games": free,
        "paid_games": paid,
        "free_share_pct": free_share,
        "genre_count": len(all_genres),
        "category_count": len(all_categories),
        "tag_count": len(all_tags),
        "top_release_year": top_year,
        "top_release_year_games": top_year_count,
        "median_positive_rate_reliable": median_pos_rate,
        "median_review_count_reliable": median_reviews,
    }

    with open(OUTPUT_DIR / "overview_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"  → overview_stats.json ({time.time() - t0:.1f}s)")
    return stats


# ══════════════════════════════════════════════════════════════════════════
# 2. chart_release_year.json
# ══════════════════════════════════════════════════════════════════════════

def export_release_year(df: pd.DataFrame):
    print("Exporting chart_release_year.json ...")
    t0 = time.time()

    year_counts = df["release_year"].value_counts().sort_index()
    year_counts = year_counts[year_counts.index > 0]  # drop invalid years
    data = [
        {"year": int(y), "game_count": int(c)}
        for y, c in year_counts.items()
    ]

    with open(OUTPUT_DIR / "chart_release_year.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  → chart_release_year.json: {len(data)} years ({time.time() - t0:.1f}s)")


# ══════════════════════════════════════════════════════════════════════════
# 3. chart_price_structure.json
# ══════════════════════════════════════════════════════════════════════════

PRICE_BUCKETS = [
    ("Free", lambda p, f: f),
    ("$0.01–$4.99", lambda p, f: ~f & (p <= 4.99)),
    ("$5.00–$9.99", lambda p, f: ~f & (p >= 5.00) & (p <= 9.99)),
    ("$10.00–$19.99", lambda p, f: ~f & (p >= 10.00) & (p <= 19.99)),
    ("$20.00–$29.99", lambda p, f: ~f & (p >= 20.00) & (p <= 29.99)),
    ("$30.00–$59.99", lambda p, f: ~f & (p >= 30.00) & (p <= 59.99)),
    ("$60.00+", lambda p, f: ~f & (p >= 60.00)),
]


def export_price_structure(df: pd.DataFrame):
    print("Exporting chart_price_structure.json ...")
    t0 = time.time()

    data = []
    for label, fn in PRICE_BUCKETS:
        mask = fn(df["price"], df["is_free"])
        subset = df[mask]
        reliable = subset[subset["review_count_calc"] >= 30]
        data.append(
            {
                "bucket": label,
                "game_count": int(len(subset)),
                "median_review_count": round(float(subset["review_count_calc"].median()), 1),
                "median_positive_rate": (
                    round(float(reliable["positive_rate_calc"].median()), 2)
                    if len(reliable) > 0
                    else None
                ),
            }
        )

    with open(OUTPUT_DIR / "chart_price_structure.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  → chart_price_structure.json ({time.time() - t0:.1f}s)")


# ══════════════════════════════════════════════════════════════════════════
# 4. chart_top_tags.json
# ══════════════════════════════════════════════════════════════════════════

def export_top_tags(df: pd.DataFrame):
    print("Exporting chart_top_tags.json ...")
    t0 = time.time()

    tags_list = parse_list_column(df["tags_list"])
    tag_counter = Counter()
    for lst in tags_list:
        tag_counter.update(lst)

    top_tags = [t for t, _ in tag_counter.most_common(TOP_TAGS_N)]

    tag_stats = []
    for tag in top_tags:
        mask = df["tags_list"].str.contains(tag, na=False, regex=False)
        subset = df[mask]
        reliable = subset[subset["review_count_calc"] >= 30]
        tag_stats.append(
            {
                "tag": tag,
                "game_count": int(len(subset)),
                "median_positive_rate": (
                    round(float(reliable["positive_rate_calc"].median()), 2)
                    if len(reliable) > 0
                    else None
                ),
                "median_review_count": round(float(subset["review_count_calc"].median()), 1),
            }
        )

    with open(OUTPUT_DIR / "chart_top_tags.json", "w", encoding="utf-8") as f:
        json.dump(tag_stats, f, indent=2, ensure_ascii=False)

    print(f"  → chart_top_tags.json: {len(tag_stats)} tags ({time.time() - t0:.1f}s)")


# ══════════════════════════════════════════════════════════════════════════
# 5. chart_top_genres.json
# ══════════════════════════════════════════════════════════════════════════

def export_top_genres(df: pd.DataFrame):
    print("Exporting chart_top_genres.json ...")
    t0 = time.time()

    genres_list = parse_list_column(df["genres_list"])
    genre_counter = Counter()
    for lst in genres_list:
        genre_counter.update(lst)

    top_genres = [g for g, _ in genre_counter.most_common(TOP_GENRES_N)]

    genre_stats = []
    for genre in top_genres:
        mask = df["genres_list"].str.contains(genre, na=False, regex=False)
        subset = df[mask]
        reliable = subset[subset["review_count_calc"] >= 30]
        genre_stats.append(
            {
                "genre": genre,
                "game_count": int(len(subset)),
                "median_positive_rate": (
                    round(float(reliable["positive_rate_calc"].median()), 2)
                    if len(reliable) > 0
                    else None
                ),
                "median_review_count": round(float(subset["review_count_calc"].median()), 1),
            }
        )

    with open(OUTPUT_DIR / "chart_top_genres.json", "w", encoding="utf-8") as f:
        json.dump(genre_stats, f, indent=2, ensure_ascii=False)

    print(f"  → chart_top_genres.json: {len(genre_stats)} genres ({time.time() - t0:.1f}s)")


# ══════════════════════════════════════════════════════════════════════════
# 6. graph_stats.json
# ══════════════════════════════════════════════════════════════════════════

def export_graph_stats(df: pd.DataFrame):
    print("Exporting graph_stats.json ...")
    t0 = time.time()

    tags_list = parse_list_column(df["tags_list"])
    genres_list = parse_list_column(df["genres_list"])
    categories_list = parse_list_column(df["categories_list"])

    all_tags = set()
    all_genres = set()
    all_categories = set()
    game_tag_edges = 0
    game_genre_edges = 0
    game_category_edges = 0

    for i in range(len(df)):
        tags = tags_list.iloc[i]
        genres = genres_list.iloc[i]
        cats = categories_list.iloc[i]
        all_tags.update(tags)
        all_genres.update(genres)
        all_categories.update(cats)
        game_tag_edges += len(tags)
        game_genre_edges += len(genres)
        game_category_edges += len(cats)

    game_nodes = len(df)
    tag_nodes = len(all_tags)
    genre_nodes = len(all_genres)
    category_nodes = len(all_categories)
    total_nodes = game_nodes + tag_nodes + genre_nodes + category_nodes
    total_edges = game_tag_edges + game_genre_edges + game_category_edges

    stats = {
        "graph_description": "Game--has_tag-->Tag, Game--has_genre-->Genre, Game--has_category-->Category",
        "game_nodes": game_nodes,
        "tag_nodes": tag_nodes,
        "genre_nodes": genre_nodes,
        "category_nodes": category_nodes,
        "game_tag_edges": game_tag_edges,
        "game_genre_edges": game_genre_edges,
        "game_category_edges": game_category_edges,
        "total_nodes": total_nodes,
        "total_edges": total_edges,
    }

    with open(OUTPUT_DIR / "graph_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"  → graph_stats.json ({time.time() - t0:.1f}s)")
    return stats


# ══════════════════════════════════════════════════════════════════════════
# 7. tag_cooccurrence_graph.json
# ══════════════════════════════════════════════════════════════════════════

def export_tag_cooccurrence(df: pd.DataFrame):
    print("Exporting tag_cooccurrence_graph.json ...")
    t0 = time.time()

    tags_list = parse_list_column(df["tags_list"])

    tag_counter = Counter()
    for lst in tags_list:
        tag_counter.update(lst)

    top_tags = [t for t, _ in tag_counter.most_common(COOCCUR_TOP_N)]
    top_tag_set = set(top_tags)

    cooccur_matrix = Counter()
    game_counts = Counter()
    for lst in tags_list:
        filtered = [t for t in lst if t in top_tag_set]
        for t in filtered:
            game_counts[t] += 1
        for i in range(len(filtered)):
            for j in range(i + 1, len(filtered)):
                a, b = sorted([filtered[i], filtered[j]])
                cooccur_matrix[(a, b)] += 1

    # Build nodes
    nodes = [
        {"id": tag, "label": tag, "value": game_counts[tag]}
        for tag in top_tags
    ]

    # Build edges (top 200 edges by weight for readability)
    edges = []
    for (src, tgt), weight in cooccur_matrix.most_common(200):
        if weight >= 3:
            edges.append({"source": src, "target": tgt, "weight": weight})

    graph = {"nodes": nodes, "edges": edges}

    with open(OUTPUT_DIR / "tag_cooccurrence_graph.json", "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    print(f"  → tag_cooccurrence_graph.json: {len(nodes)} nodes, {len(edges)} edges ({time.time() - t0:.1f}s)")
    return graph


# ══════════════════════════════════════════════════════════════════════════
# 8. game_index.json
# ══════════════════════════════════════════════════════════════════════════

def export_game_index(df: pd.DataFrame):
    print("Exporting game_index.json ...")
    t0 = time.time()

    # Filter: name not empty, has at least 30 reviews, has valid positive_rate
    mask = (
        df["name"].notna()
        & (df["name"] != "")
        & (df["review_count_calc"] >= MIN_REVIEWS_FOR_INDEX)
        & df["positive_rate_calc"].notna()
        & (df["positive_rate_calc"] >= 0)
    )
    filtered = df[mask].copy()

    before = len(filtered)

    # Keep only games with at least one of tags/genres/categories
    has_attrs = (
        filtered["tags_list"].notna()
        & (filtered["tags_list"] != "")
        | filtered["genres_list"].notna()
        & (filtered["genres_list"] != "")
        | filtered["categories_list"].notna()
        & (filtered["categories_list"] != "")
    )
    filtered = filtered[has_attrs]
    after_attrs = len(filtered)
    print(f"    After attr filter: {before} → {after_attrs}")

    # If still too many, keep top by review_count_calc
    if len(filtered) > MAX_INDEX_ROWS:
        filtered = filtered.nlargest(MAX_INDEX_ROWS, "review_count_calc")
        print(f"    Capped to {MAX_INDEX_ROWS} games by review_count")

    tags_parsed = parse_list_column(filtered["tags_list"])
    genres_parsed = parse_list_column(filtered["genres_list"])
    categories_parsed = parse_list_column(filtered["categories_list"])

    records = []
    for i, (_, row) in enumerate(filtered.iterrows()):
        records.append(
            {
                "appid": int(row["appid"]),
                "name": str(row["name"]),
                "price": round(float(row["price"]), 2),
                "is_free": bool(row["is_free"]),
                "genres": genres_parsed.iloc[i],
                "categories": categories_parsed.iloc[i],
                "tags": tags_parsed.iloc[i],
                "review_count_calc": int(row["review_count_calc"]),
                "positive_rate_calc": round(float(row["positive_rate_calc"]), 2),
                "recommendations": int(row["recommendations"]) if pd.notna(row["recommendations"]) else 0,
                "peak_ccu": int(row["peak_ccu"]) if pd.notna(row["peak_ccu"]) else 0,
                "short_description": (
                    str(row["short_description"])[:200] if pd.notna(row["short_description"]) else ""
                ),
                "release_year": int(row["release_year"]) if pd.notna(row["release_year"]) else 0,
            }
        )

    with open(OUTPUT_DIR / "game_index.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(OUTPUT_DIR / "game_index.json")
    print(f"  → game_index.json: {len(records)} games, {file_size / 1024:.0f} KB ({time.time() - t0:.1f}s)")
    return records


# ══════════════════════════════════════════════════════════════════════════
# 9. graph_recommendations.json
# ══════════════════════════════════════════════════════════════════════════

def build_attr_sets(game_index: list):
    """Build tag/genre/category sets for each game (as frozensets)."""
    tag_sets = {}
    genre_sets = {}
    cat_sets = {}
    for g in game_index:
        aid = g["appid"]
        tag_sets[aid] = frozenset(g["tags"])
        genre_sets[aid] = frozenset(g["genres"])
        cat_sets[aid] = frozenset(g["categories"])
    return tag_sets, genre_sets, cat_sets


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a and not b:
        return 0.0
    union = len(a | b)
    if union == 0:
        return 0.0
    return len(a & b) / union


def export_recommendations(df: pd.DataFrame, game_index: list):
    print("Exporting graph_recommendations.json ...")
    t0 = time.time()

    # Limit candidates for reasonable computation time
    if len(game_index) > MAX_REC_CANDIDATES:
        candidates = sorted(game_index, key=lambda g: g["review_count_calc"], reverse=True)[
            :MAX_REC_CANDIDATES
        ]
        print(f"    Limiting recommendation candidates to {MAX_REC_CANDIDATES}")
    else:
        candidates = game_index

    tag_sets, genre_sets, cat_sets = build_attr_sets(candidates)
    appids = [g["appid"] for g in candidates]
    n = len(appids)

    recs = {}
    for i in range(n):
        aid_a = appids[i]
        tags_a = tag_sets[aid_a]
        genres_a = genre_sets[aid_a]
        cats_a = cat_sets[aid_a]

        if not tags_a and not genres_a and not cats_a:
            recs[aid_a] = []
            continue

        scored = []
        for j in range(n):
            if i == j:
                continue
            aid_b = appids[j]
            tags_b = tag_sets[aid_b]
            genres_b = genre_sets[aid_b]
            cats_b = cat_sets[aid_b]

            t_jac = jaccard(tags_a, tags_b)
            g_jac = jaccard(genres_a, genres_b)
            c_jac = jaccard(cats_a, cats_b)
            score = 0.60 * t_jac + 0.25 * g_jac + 0.15 * c_jac

            if score > 0:
                shared_tags = sorted(tags_a & tags_b)
                shared_genres = sorted(genres_a & genres_b)
                shared_cats = sorted(cats_a & cats_b)
                scored.append((aid_b, score, shared_tags, shared_genres, shared_cats))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_k = scored[:TOP_K_REC]

        # Build lookup for candidate metadata
        cand_lookup = {g["appid"]: g for g in candidates}

        recs[aid_a] = []
        for aid_b, score, s_tags, s_genres, s_cats in top_k:
            gb = cand_lookup.get(aid_b, {})
            n_tags = len(s_tags)
            n_genres = len(s_genres)
            n_cats = len(s_cats)
            reason_parts = []
            if n_tags:
                reason_parts.append(f"共享 {n_tags} 个标签")
            if n_genres:
                reason_parts.append(f"共享 {n_genres} 个类型")
            if n_cats:
                reason_parts.append(f"共享 {n_cats} 个分类")
            reason = "该游戏与目标游戏" + "、".join(reason_parts) + "，因此在游戏—属性图中具有较高相似度。"

            recs[aid_a].append(
                {
                    "appid": aid_b,
                    "name": gb.get("name", ""),
                    "score": round(score, 4),
                    "shared_tags": s_tags[:MAX_SHARED_ATTRS],
                    "shared_genres": s_genres[:MAX_SHARED_ATTRS],
                    "shared_categories": s_cats[:MAX_SHARED_ATTRS],
                    "price": gb.get("price", 0),
                    "review_count_calc": gb.get("review_count_calc", 0),
                    "positive_rate_calc": gb.get("positive_rate_calc", 0),
                    "reason": reason,
                }
            )

        if (i + 1) % 500 == 0:
            print(f"    Processed {i + 1}/{n} games ...")

    with open(OUTPUT_DIR / "graph_recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recs, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(OUTPUT_DIR / "graph_recommendations.json")
    print(f"  → graph_recommendations.json: {len(recs)} games, {file_size / 1024:.0f} KB ({time.time() - t0:.1f}s)")


# ══════════════════════════════════════════════════════════════════════════
# 10. chart_text_tfidf_keywords.json
# ══════════════════════════════════════════════════════════════════════════

def export_chart_text_tfidf_keywords():
    print("Exporting chart_text_tfidf_keywords.json ...")
    t0 = time.time()

    csv_path = PROCESSED_DIR / "steam_text_tfidf_keywords.csv"
    if not csv_path.exists():
        print("  WARNING: steam_text_tfidf_keywords.csv not found, skipping")
        return None

    tfidf_df = pd.read_csv(csv_path)
    # Keep top 25 high-review words and top 25 low-review words
    high_words = tfidf_df.nlargest(25, "diff_high_minus_low")[
        ["word", "high_tfidf", "low_tfidf", "diff_high_minus_low"]
    ].to_dict(orient="records")
    low_words = tfidf_df.nsmallest(25, "diff_high_minus_low")[
        ["word", "high_tfidf", "low_tfidf", "diff_high_minus_low"]
    ].to_dict(orient="records")

    data = {
        "high_group": high_words,
        "low_group": low_words,
    }

    with open(OUTPUT_DIR / "chart_text_tfidf_keywords.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(OUTPUT_DIR / "chart_text_tfidf_keywords.json")
    print(f"  → chart_text_tfidf_keywords.json: {len(high_words)} high + {len(low_words)} low words, {file_size} B ({time.time() - t0:.1f}s)")
    return data


# ══════════════════════════════════════════════════════════════════════════
# 11. chart_text_tag_richness.json
# ══════════════════════════════════════════════════════════════════════════

def export_chart_text_tag_richness():
    print("Exporting chart_text_tag_richness.json ...")
    t0 = time.time()

    csv_path = PROCESSED_DIR / "steam_text_tag_richness_vs_popularity.csv"
    if not csv_path.exists():
        print("  WARNING: steam_text_tag_richness_vs_popularity.csv not found, skipping")
        return None

    richness_df = pd.read_csv(csv_path)
    data = []
    for _, row in richness_df.iterrows():
        data.append({
            "tag_count_bin": str(row["tag_count_bin"]),
            "game_count": int(row["game_count"]),
            "median_review_count": round(float(row["median_review_count"]), 1),
            "median_positive_rate": round(float(row["median_positive_rate"]), 2),
        })

    with open(OUTPUT_DIR / "chart_text_tag_richness.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(OUTPUT_DIR / "chart_text_tag_richness.json")
    print(f"  → chart_text_tag_richness.json: {len(data)} bins, {file_size} B ({time.time() - t0:.1f}s)")
    return data


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SteamScope Data Export")
    print("=" * 60)

    print("\nLoading main table ...")
    df = load_main_table()
    print(f"  Shape: {df.shape}")

    # 1
    export_overview_stats(df)

    # 2
    export_release_year(df)

    # 3
    export_price_structure(df)

    # 4
    export_top_tags(df)

    # 5
    export_top_genres(df)

    # 6
    export_graph_stats(df)

    # 7
    export_tag_cooccurrence(df)

    # 8
    game_index = export_game_index(df)

    # 9 — needs game_index
    export_recommendations(df, game_index)

    # 10 — text analysis: TF-IDF keywords
    export_chart_text_tfidf_keywords()

    # 11 — text analysis: tag richness vs popularity
    export_chart_text_tag_richness()

    # Summary
    print("\n" + "=" * 60)
    print("Export complete!")
    print("=" * 60)
    total_size = sum(
        os.path.getsize(OUTPUT_DIR / f)
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".json")
    )
    print(f"Total JSON size: {total_size / 1024:.0f} KB")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
