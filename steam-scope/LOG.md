# SteamScope — 项目日志

## Step 1 — 创建 steam-scope 项目目录

- **Time:** 2026-05-22 18:35
- **Goal:** 在项目根目录中新建 `steam-scope/` 目录并创建完整子目录结构
- **Input files:** 无
- **Output files:** 创建了如下目录结构：
  ```
  steam-scope/
  ├── assets/css/
  ├── js/
  ├── data/
  └── scripts/
  ```
- **Method:** `mkdir -p` 命令
- **Key decisions:** 目录结构按照需求文档中的要求创建，与已有 notebooks/、reports/、figures/ 平行
- **Result:** 成功

---

## Step 2 — 检查可用 processed 数据

- **Time:** 2026-05-22 18:36
- **Goal:** 确认 data/processed/ 中有哪些数据文件可用于导出 JSON
- **Input files:** 无（探索性读取）
- **Output files:** 无
- **Method:**
  1. `ls data/processed/` 列出所有文件
  2. 使用 pandas 读取 `steam_march2025_features.parquet` 查看 schema（89,618 行 × 63 列）
  3. 检查了多个 summary CSV 的内容
- **Key decisions:**
  - 主数据表确认：`steam_march2025_features.parquet`（107MB）包含所有需要的字段
  - tags_list、genres_list、categories_list 的分隔符是 `|`（竖线）而非 `;`（分号）
  - 有 review_count_calc、positive_rate_calc、is_free、price、release_year 等核心字段
  - 已有 summary CSV 可以直接使用或交叉验证
- **Data size / record count:** 89,618 行 × 63 列
- **Result:** 数据结构清晰，可以直接用于导出所有需要的 JSON
- **Problems / Notes:** 标签分隔符是 `|`，后续解析需要注意

---

## Step 3 — 导出 overview 和 chart JSON 文件

- **Time:** 2026-05-22 18:37
- **Goal:** 从 Parquet 导出 overview_stats.json、chart_release_year.json、chart_price_structure.json、chart_top_tags.json、chart_top_genres.json
- **Input files:** `data/processed/steam_march2025_features.parquet`
- **Output files:**
  - `steam-scope/data/overview_stats.json`（370 B）
  - `steam-scope/data/chart_release_year.json`（1.3 KB）
  - `steam-scope/data/chart_price_structure.json`（911 B）
  - `steam-scope/data/chart_top_tags.json`（6.1 KB）
  - `steam-scope/data/chart_top_genres.json`（3.7 KB）
- **Method:**
  - 直接从 Parquet 读取完整表
  - overview_stats.json：统计总数、评论数、免费比例、类型/标签/分类唯一值数量
  - chart_release_year.json：按 release_year 分组统计游戏数量
  - chart_price_structure.json：按 7 个价格区间（Free、$0.01-4.99、$5-9.99、$10-19.99、$20-29.99、$30-59.99、$60+）统计
  - chart_top_tags.json：统计 Top 50 标签的游戏数、中位好评率、中位评论数
  - chart_top_genres.json：统计 Top 30 类型的上述指标
- **Key decisions:**
  - 价格区间的划分参考了 Steam 常见定价档位
  - 中位好评率只在 review_count_calc >= 30 的可靠子集中计算（避免小样本偏差）
  - 标签/类型匹配使用 str.contains 进行近似匹配（对统计分析足够精确）
- **Data size / record count:** 见各文件
- **Result:** 5 个 chart JSON 全部成功导出，数据量很小
- **Problems / Notes:** 初始版本使用 `|` 分隔符解析失败，修复了 parse_list_column 函数

---

## Step 4 — 构建图数据统计

- **Time:** 2026-05-22 18:37
- **Goal:** 构建 graph_stats.json 和 tag_cooccurrence_graph.json
- **Input files:** `data/processed/steam_march2025_features.parquet`
- **Output files:**
  - `steam-scope/data/graph_stats.json`（334 B）
  - `steam-scope/data/tag_cooccurrence_graph.json`（21 KB）
- **Method:**
  - 遍历所有游戏，解析 tags_list、genres_list、categories_list
  - 统计节点数（game 节点、tag 节点、genre 节点、category 节点）和边数
  - 对于标签共现网络：
    - 提取 Top 40 标签
    - 统计两两共现次数
    - 构建 nodes 数组（含游戏数量作为 value 用于节点大小）
    - 构建 edges 数组（保留权重最高的 200 条边，过滤掉权重 < 3 的边）
- **Key decisions:**
  - 共现网络仅保留 Top 40 标签，避免网络过于复杂
  - 边数限制为 200 条以保持可视化可读性
  - 边权重过滤阈值设为 3（即两个标签必须至少在 3 款游戏中同时出现）
- **Data size / record count:**
  - 图总节点数：90,143（89,618 Game + 452 Tag + 33 Genre + 40 Category）
  - 图总边数：1,643,164（1,008,987 tag 边 + 258,024 genre 边 + 376,153 category 边）
  - 标签共现网络：40 nodes, 200 edges
- **Result:** 成功
- **Problems / Notes:** 第一次运行时标签分隔符识别错误导致 0 条边，修复后正常

---

## Step 5 — 构建精简游戏索引

- **Time:** 2026-05-22 18:37
- **Goal:** 构建 game_index.json 用于网页搜索和推荐展示
- **Input files:** `data/processed/steam_march2025_features.parquet`
- **Output files:** `steam-scope/data/game_index.json`（5,434 KB，5,000 条游戏记录）
- **Method:**
  1. 筛选条件：
     - name 非空
     - review_count_calc >= 30（有足够评论的游戏）
     - positive_rate_calc 有效（非空、非负）
     - 至少有 tags、genres、categories 中的一类
  2. 筛选后剩余 33,358 行
  3. 按 review_count_calc 降序排列，取 Top 5,000
  4. 只保留精简字段：appid、name、price、is_free、genres、categories、tags、review_count_calc、positive_rate_calc、recommendations、peak_ccu、short_description（截断至 200 字符）、release_year
- **Key decisions:**
  - 限制为 5,000 个游戏以控制 JSON 文件大小
  - short_description 截断至 200 字符减少文件体积
  - 所有列表字段（tags、genres、categories）已解析为数组
- **Data size / record count:**
  - 筛选前：89,618 行
  - 筛选后（条件过滤）：33,358 行
  - 最终输出：5,000 行
  - JSON 文件大小：5,434 KB（约 5.3 MB）
- **Result:** 成功
- **Problems / Notes:** 5.3MB 对于网页仍有优化空间，后续如果部署需要可以进一步减少或启用 gzip 压缩

---

## Step 6 — 构建图推荐 JSON

- **Time:** 2026-05-22 18:38
- **Goal:** 基于图数据思想生成相似游戏推荐结果（graph_recommendations.json）
- **Input files:**
  - `data/processed/steam_march2025_features.parquet`（通过 game_index）
- **Output files:** `steam-scope/data/graph_recommendations.json`（6,972 KB，1,000 个游戏 × Top 10 推荐）
- **Method:**
  1. 从 game_index 中选择 review_count_calc 最高的 1,000 个游戏作为候选
  2. 将每款游戏的 tags、genres、categories 转为 frozenset
  3. 对每对游戏计算：
     - `tag_jaccard = |tags_A ∩ tags_B| / |tags_A ∪ tags_B|`
     - `genre_jaccard = |genres_A ∩ genres_B| / |genres_A ∪ genres_B|`
     - `category_jaccard = |categories_A ∩ categories_B| / |categories_A ∪ categories_B|`
     - `weighted_score = 0.60 × tag_jaccard + 0.25 × genre_jaccard + 0.15 × category_jaccard`
  4. 对每个游戏保留 Top 10 相似游戏
  5. 每个推荐包含：appid、name、score、shared_tags/genres/categories（最多 5 个）、price、review_count_calc、positive_rate_calc、reason
- **Key decisions:**
  - 权重分配：Tag 权重最高（0.60），因为标签粒度最细、最能区分游戏风格；Genre（0.25）和 Category（0.15）作为辅助
  - 候选游戏限制为 1,000 个以控制计算时间（O(n²)）和输出文件大小
  - shared_tags/genres/categories 各截断至 5 个以减少 JSON 冗余
  - 计算耗时约 4.6 秒
- **Data size / record count:**
  - 候选游戏：1,000 个
  - 推荐输出：1,000 个游戏 × 各 Top 10
  - JSON 文件大小：6,972 KB（约 6.8 MB）
- **Result:** 成功
- **Problems / Notes:**
  - 这是预计算推荐，不是实时推荐；如果在生产环境应使用向量数据库
  - 6.8MB 的 JSON 对于网页加载较大，后续部署时可考虑进一步减少候选数至 500 或启用 gzip

---

## Step 7 — 构建本地静态网页

- **Time:** 2026-05-22 18:40
- **Goal:** 创建 index.html、style.css、app.js 实现交互式展示页面
- **Input files:** steam-scope/data/ 中的所有 JSON
- **Output files:**
  - `steam-scope/index.html` — 主页面
  - `steam-scope/assets/css/style.css` — 样式
  - `steam-scope/js/app.js` — 交互逻辑
- **Method:**
  - 使用原生 HTML/CSS/JS，无构建工具
  - 图表使用 ECharts CDN（v5.5.0）
  - 深色主题设计，响应式布局
  - 页面包含 5 个核心模块：
    1. Hero / 概览（统计卡片）
    2. 市场结构（发行年份趋势、价格结构、Top 类型/标签）
    3. 反馈与定位（气泡图、中位评论数图）
    4. 图数据展示（统计卡片、共现网络图、共现对表格）
    5. 游戏推荐（搜索框 + 推荐卡片）
- **Key decisions:**
  - 使用 ECharts CDN 而非打包，简化部署
  - 所有文字使用中文
  - 数据通过 fetch 异步加载 JSON
  - 搜索框实现了模糊匹配和下拉建议
  - 网络图使用力导向布局
- **Result:** 成功
- **Problems / Notes:** 页面需要在本地 HTTP 服务器下运行（不能直接用 file:// 协议打开，因为 fetch 需要 HTTP）

---

## Step 8 — 本地演示检查

- **Time:** 2026-05-22 18:45
- **Goal:** 本地启动 HTTP 服务器验证页面功能
- **Method:**
  ```bash
  cd steam-scope
  python3 -m http.server 8000
  # 访问 http://localhost:8000/
  ```
- **Result:** 验证通过，所有功能正常：
  1. ✅ 14 个 HTTP 请求全部成功（唯 favicon.ico 404 无影响）
  2. ✅ 6 个统计卡片正确显示（90K 游戏、73K 评论、15.8% 免费等）
  3. ✅ 10 个 ECharts 图表实例全部正确创建并渲染
  4. ✅ 图数据统计正确（89.6K Game 节点、1.64M 总边数）
  5. ✅ 标签共现表格显示 Top 30 共现对（Indie+Singleplayer: 26,699 最高）
  6. ✅ 标签共现网络图正常渲染
  7. ✅ 搜索输入"C​ounter-Strike"正确返回 3 个建议
  8. ✅ 点击选择后正确展示 Top 10 推荐卡片（包含相似度分数、共享属性、推荐理由）
  9. ✅ 推荐结果合理：Counter-Strike 2 → Rainbow Six Siege (61.3%)、Team Fortress 2 (56.2%)
- **Problems / Notes:**
  - game_index.json (5.4MB) 和 graph_recommendations.json (7.0MB) 在首次加载时需要几秒
  - 后续部署到博客时可启用 nginx gzip 压缩以减少传输时间
  - 共现网络图在 40 节点下力导向布局较为密集，用户可拖拽和缩放

---

## Step 9 — 添加加载进度条

- **Time:** 2026-05-22 19:00
- **Goal:** 为用户提供明确的数据加载进度反馈，避免打开页面后"莫名等待"
- **Input files:** index.html、style.css、app.js
- **Output files:** 同上（修改）
- **Method:**
  1. 在 `<body>` 最顶部添加全屏加载遮罩层 `#loading-overlay`
  2. 遮罩包含：标题、进度条（`#progress-bar-fill`）、状态文字、9 个文件的加载列表
  3. 将 JavaScript 数据加载从 `Promise.all`（并行）改为逐个顺序加载，每完成一个文件立即更新进度条和文件状态图标
  4. 文件列表预注册在 `FILE_REGISTRY` 数组中，包含 key、文件名、中文标签、预估体积
  5. 加载完成后 `setTimeout` 400ms 后执行 `renderAll()`，遮罩层添加 `fade-out` class 做淡出动画
- **Key decisions:**
  - 从并行加载改为顺序加载会在本地有微小性能损失，但换来了可感知的进度反馈——对于外网用户（尤其是大文件加载时）体验更好
  - 文件注册表硬编码了预估大小（如 ~5.4 MB、~7.0 MB），方便用户理解哪些文件耗时较长
  - 淡出动画 0.4s + opacity transition，视觉上平滑无突兀
- **Result:**
  - 验证通过：9 个文件全部 ✓，进度条从 0% → 100%，遮罩淡出后页面正常显示
  - 加载过程中每个文件的状态实时更新（○ → ✓ / ✗）
- **Problems / Notes:**
  - 本地 localhost 测试时大文件加载也很快（< 1 秒），进度条一闪而过；外网部署后效果更明显
