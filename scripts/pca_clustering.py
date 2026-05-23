#!/usr/bin/env python3
"""PCA + K-Means analysis for report. Generates figures 51-53."""
import warnings, sys, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path("/Users/situozhang/Documents/大数据处理技术/Ultimate_Game_Insights")
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "steam_march2025_features.parquet"
FIGURES_DIR = PROJECT_ROOT / "figures"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 160

# ── Load ──
print("Loading data...", flush=True)
df = pd.read_parquet(DATA_PATH)
print(f"  Shape: {df.shape}", flush=True)

# ── Prepare features ──
df_model = df[[
    "price", "review_count_calc", "positive_rate_calc",
    "recommendations", "peak_ccu",
    "tags_count", "genres_count", "categories_count",
    "platform_count", "is_free", "release_year", "game_age_years",
    "average_playtime_forever",
]].copy()

for col, name in [
    ("recommendations", "recommendations_log1p"),
    ("peak_ccu", "peak_ccu_log1p"),
    ("review_count_calc", "review_count_log1p"),
    ("average_playtime_forever", "playtime_log1p"),
]:
    df_model[name] = np.log1p(df_model[col].fillna(0).clip(lower=0))
df_model["is_free"] = df_model["is_free"].astype(float)

pca_features = [
    "price", "review_count_log1p", "positive_rate_calc",
    "recommendations_log1p", "peak_ccu_log1p",
    "tags_count", "genres_count", "categories_count",
    "platform_count", "is_free", "release_year", "game_age_years",
    "playtime_log1p",
]

pca_data = df_model.dropna(subset=pca_features).copy()
print(f"  After dropna: {pca_data.shape}", flush=True)

# ── PCA ──
print("Running PCA...", flush=True)
t0 = time.time()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(pca_data[pca_features])
del df_model  # free memory

pca = PCA()
X_pca = pca.fit_transform(X_scaled)
var_ratio = pca.explained_variance_ratio_
cumsum_var = np.cumsum(var_ratio)
print(f"  PCA done in {time.time()-t0:.1f}s, PC1={var_ratio[0]:.1%}, PC2={var_ratio[1]:.1%}", flush=True)

# Figure 51: Scree plot + PC1 loadings
print("Generating figure 51...", flush=True)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

axes[0].bar(range(1, len(var_ratio) + 1), var_ratio, color="#4C78A8", alpha=0.8)
axes[0].plot(range(1, len(cumsum_var) + 1), cumsum_var, "o-", color="#F58518", lw=2, ms=5)
axes[0].axhline(y=0.8, color="gray", linestyle="--", lw=1, label="80% threshold")
axes[0].set_xlabel("Principal Component")
axes[0].set_ylabel("Explained Variance Ratio")
axes[0].set_title("PCA Scree Plot")
axes[0].legend()
for i in [1, 2, 4, 6]:
    if i <= len(cumsum_var):
        axes[0].annotate(f"{cumsum_var[i-1]:.0%}", (i, cumsum_var[i-1]),
                         textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center")

loadings = pd.DataFrame(pca.components_.T[:, :2], index=pca_features, columns=["PC1", "PC2"])
loadings_sorted = loadings.reindex(loadings["PC1"].abs().sort_values(ascending=False).index)
labels_clean = [f.replace("_log1p", "(log)").replace("_calc", "").replace("average_playtime_forever", "playtime(log)") for f in loadings_sorted.index]

axes[1].barh(range(len(loadings_sorted)), loadings_sorted["PC1"].values, color="#66c0f4", height=0.6)
axes[1].set_yticks(range(len(loadings_sorted)))
axes[1].set_yticklabels(labels_clean, fontsize=9)
axes[1].set_xlabel("Loading on PC1")
axes[1].set_title("PC1 Feature Loadings")
axes[1].axvline(x=0, color="gray", linestyle="--", lw=0.8)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "51_pca_scree_and_loadings.png", bbox_inches="tight")
plt.close()
print("  Saved 51_pca_scree_and_loadings.png", flush=True)

# Figure 52: PC1 vs PC2 scatter (sample for speed)
print("Generating figure 52...", flush=True)
sample_n = min(15000, len(X_pca))
rng = np.random.default_rng(42)
sample_idx = rng.choice(len(X_pca), size=sample_n, replace=False)
heat_sample = pca_data.iloc[sample_idx]["review_count_log1p"].values

fig2, ax2 = plt.subplots(figsize=(10, 7))
sc = ax2.scatter(X_pca[sample_idx, 0], X_pca[sample_idx, 1],
                 c=heat_sample, cmap="YlOrRd", alpha=0.25, s=8, rasterized=True)
ax2.set_xlabel(f"PC1 ({var_ratio[0]:.1%} variance)")
ax2.set_ylabel(f"PC2 ({var_ratio[1]:.1%} variance)")
ax2.set_title("PCA: PC1 vs PC2 (15K sample, colored by Review Count)")
plt.colorbar(sc, ax=ax2, label="Review Count (log1p)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "52_pca_scatter.png", bbox_inches="tight")
plt.close()
print("  Saved 52_pca_scatter.png", flush=True)

# ── K-Means Clustering ──
print("Running K-Means...", flush=True)
t0 = time.time()
X_pca5 = X_pca[:, :5]
kmeans = MiniBatchKMeans(n_clusters=5, random_state=42, batch_size=2048, n_init=3)
clusters = kmeans.fit_predict(X_pca5)
pca_data["cluster"] = clusters
print(f"  K-Means done in {time.time()-t0:.1f}s", flush=True)

# Profile clusters
cluster_profile = pca_data.groupby("cluster").agg(
    count=("price", "count"),
    price_median=("price", "median"),
    review_count_median=("review_count_calc", "median"),
    positive_rate_median=("positive_rate_calc", "median"),
    recommendations_median=("recommendations", "median"),
    peak_ccu_median=("peak_ccu", "median"),
    tags_count_mean=("tags_count", "mean"),
    platform_count_mean=("platform_count", "mean"),
    is_free_ratio=("is_free", "mean"),
    playtime_median=("average_playtime_forever", "median"),
).reset_index()

# Label clusters
def label_cluster(row):
    if row["is_free_ratio"] > 0.85:
        return "Free-to-Play / Live Service"
    if row["review_count_median"] > 150 and row["positive_rate_median"] > 75:
        return "High-Traction Mainstream"
    if row["review_count_median"] >= 30 and row["positive_rate_median"] >= 78:
        return "High-Rating Niche"
    if row["review_count_median"] < 20:
        return "Low-Visibility Long Tail"
    return "Mid-Tier Standard"

cluster_profile["label"] = cluster_profile.apply(label_cluster, axis=1)
cluster_profile = cluster_profile.sort_values("review_count_median", ascending=False)
cluster_profile.to_csv(PROCESSED_DIR / "cluster_profile_summary.csv", index=False)

print("\n=== Cluster Profiles ===", flush=True)
for _, row in cluster_profile.iterrows():
    print(f"C{int(row['cluster'])} [{row['label']}]: "
          f"{int(row['count']):,} games, "
          f"median reviews={row['review_count_median']:.0f}, "
          f"pos_rate={row['positive_rate_median']:.1f}%, "
          f"free={row['is_free_ratio']:.1%}, "
          f"peak_ccu={row['peak_ccu_median']:.0f}",
          flush=True)

# Figure 53: Clusters on PC1/PC2
print("\nGenerating figure 53...", flush=True)
colors = ["#F58518", "#4C78A8", "#54A24B", "#E45756", "#72B7B2"]
cluster_label_map = dict(zip(cluster_profile["cluster"], cluster_profile["label"]))

fig3, ax3 = plt.subplots(figsize=(11, 7))
for ci in sorted(pca_data["cluster"].unique()):
    mask = pca_data["cluster"] == ci
    n = mask.sum()
    sample_n = min(3000, n)
    if sample_n < n:
        ci_idx = np.where(mask)[0]
        ci_sample = rng.choice(ci_idx, size=sample_n, replace=False)
    else:
        ci_sample = np.where(mask)[0]
    ax3.scatter(X_pca[ci_sample, 0], X_pca[ci_sample, 1],
                color=colors[int(ci)], alpha=0.35, s=7,
                label=f"{cluster_label_map.get(ci, f'C{ci}')} ({n:,} games)",
                rasterized=True)

ax3.set_xlabel(f"PC1 ({var_ratio[0]:.1%} variance)")
ax3.set_ylabel(f"PC2 ({var_ratio[1]:.1%} variance)")
ax3.set_title("K-Means Clusters (k=5) on PC1–PC2")
ax3.legend(markerscale=4, fontsize=9, loc="upper right")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "53_cluster_scatter.png", bbox_inches="tight")
plt.close()
print("  Saved 53_cluster_scatter.png", flush=True)

# ── Summary ──
pca_summary = pd.DataFrame({
    "PC": [f"PC{i+1}" for i in range(len(var_ratio))],
    "Explained_Variance": [round(v, 4) for v in var_ratio],
    "Cumulative_Variance": [round(v, 4) for v in cumsum_var],
})
pca_summary.to_csv(PROCESSED_DIR / "pca_variance_summary.csv", index=False)

print(f"\nDone! PC1+PC2 explain {cumsum_var[1]:.1%}, first 5 PCs explain {cumsum_var[4]:.1%}", flush=True)
