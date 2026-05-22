# SteamScope

基于大规模 Steam 游戏数据的交互式分析与图推荐展示 — 课程项目前端原型。

## 数据来源

本目录中的 JSON 数据来自项目已有的 Notebook 分析和 processed 输出（`data/processed/steam_march2025_features.parquet` 及相关 summary CSV），**不直接读取原始 1.7GB Kaggle CSV**。

所有数据经 Notebook 01–08 的清洗、特征工程和聚合处理后，由本目录的导出脚本进一步转换为轻量 JSON。

## 技术栈

- 纯静态 HTML / CSS / JavaScript
- [ECharts 5.5.0](https://echarts.apache.org/)（CDN 加载，用于数据可视化图表）
- 无需后端、无需数据库、无需构建工具

## 快速开始

### 1. 生成网页 JSON 数据

在项目根目录执行：

```bash
source .venv/bin/activate
python steam-scope/scripts/export_steam_scope_data.py
```

该脚本会从 `data/processed/steam_march2025_features.parquet` 导出 9 个轻量 JSON 文件到 `steam-scope/data/`。

### 2. 本地运行

```bash
# 方式一：直接启动（会自动释放已有端口）
bash steam-scope/start.sh

# 方式二：手动启动
cd steam-scope
python3 -m http.server 8000
```

### 3. 访问

打开浏览器访问：**http://localhost:8000/**

## 页面模块

| 模块 | 说明 |
|------|------|
| Hero / 概览 | 核心统计卡片（游戏总数、评论数、免费比例、类型/标签数等） |
| 市场结构 | 发行年份趋势、价格区间分布、Top 类型/标签 |
| 反馈与定位 | 标签/类型的好评率气泡图、中位评论数对比 |
| 图数据展示 | 异构图统计、Top 40 标签共现网络、共现对表格 |
| 游戏推荐 | 搜索框 + Top 10 相似游戏推荐（基于 Jaccard 图相似度） |

## 生成的数据文件

| 文件 | 说明 | 大小 |
|------|------|------|
| `overview_stats.json` | 核心统计数字 | < 1 KB |
| `chart_release_year.json` | 发行年份趋势 | ~1 KB |
| `chart_price_structure.json` | 价格区间分布 | ~1 KB |
| `chart_top_tags.json` | Top 50 标签数据 | ~6 KB |
| `chart_top_genres.json` | Top 30 类型数据 | ~4 KB |
| `graph_stats.json` | 图数据结构统计 | < 1 KB |
| `tag_cooccurrence_graph.json` | 标签共现网络 | ~21 KB |
| `game_index.json` | 精简游戏索引（5,000 款） | ~5.4 MB |
| `graph_recommendations.json` | 预计算推荐（1,000 款） | ~7.0 MB |

## 部署到博客服务器

将 `steam-scope/` 整个目录上传到博客服务器对应的路径：

```bash
# 假设博客根目录为 /www/wwwroot/tobykskgd.life/
rsync -avz steam-scope/ user@server:/www/wwwroot/tobykskgd.life/steam-scope/
```

部署后通过 **https://tobykskgd.life/steam-scope/** 访问。

## 当前原型限制

- 推荐结果是**预计算**的（不是实时推荐），无法动态更新
- 没有后端数据库，所有数据以静态 JSON 文件提供
- 没有使用完整图数据库（如 Neo4j），相似度计算是基于 Jaccard 的简化实现
- game_index.json 和 graph_recommendations.json 目前各约 5–7 MB，首次加载需一定时间；后续可启用 gzip 压缩或进一步精简
- 仅用于**课程项目展示**，非生产系统
