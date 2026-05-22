/**
 * SteamScope — Main Application JavaScript
 * Loads pre-exported JSON and renders ECharts charts.
 */

const DATA_DIR = "data/";

// ── Data loading ─────────────────────────────────────────────────
let overviewData, releaseYearData, priceData, topTags, topGenres;
let graphStats, tagCooccurrence;

// File registry: key, display name, human-readable size
const FILE_REGISTRY = [
  { key: "overview_stats",            file: "overview_stats.json",            label: "项目概览统计",         size: "< 1 KB" },
  { key: "releaseYearData",           file: "chart_release_year.json",        label: "发行年份趋势",         size: "~1 KB"  },
  { key: "priceData",                 file: "chart_price_structure.json",     label: "价格区间分布",         size: "< 1 KB"  },
  { key: "topTags",                   file: "chart_top_tags.json",            label: "热门标签数据",         size: "~6 KB"  },
  { key: "topGenres",                 file: "chart_top_genres.json",          label: "热门类型数据",         size: "~4 KB"  },
  { key: "graphStats",                file: "graph_stats.json",               label: "图结构统计",           size: "< 1 KB"  },
  { key: "tagCooccurrence",           file: "tag_cooccurrence_graph.json",    label: "标签共现网络",         size: "~21 KB" },
];

// Progress UI elements
const progressFill  = document.getElementById("progress-bar-fill");
const progressFile  = document.getElementById("loading-file");
const progressList  = document.getElementById("loading-list");
const loadingOverlay = document.getElementById("loading-overlay");
const loadingStatus = document.getElementById("loading-status");

function buildLoadingList() {
  let html = "";
  for (const entry of FILE_REGISTRY) {
    html += `<div class="file-row" id="row-${entry.key}">
      <span class="file-status pending">○</span>
      <span class="file-name">${entry.label}</span>
      <span class="file-size">${entry.size}</span>
    </div>`;
  }
  progressList.innerHTML = html;
}

function updateProgress(done, total, currentLabel) {
  const pct = Math.round((done / total) * 100);
  progressFill.style.width = pct + "%";
  loadingStatus.textContent = `${done} / ${total} 个文件已完成`;
  if (currentLabel) {
    progressFile.textContent = "正在加载: " + currentLabel;
  }
}

function markFile(key, status) {
  const row = document.getElementById("row-" + key);
  if (!row) return;
  const icon = row.querySelector(".file-status");
  icon.className = "file-status " + status;
  if (status === "done")   icon.textContent = "✓";
  if (status === "error")  icon.textContent = "✗";
}

async function loadJSON(filename) {
  const resp = await fetch(DATA_DIR + filename);
  if (!resp.ok) throw new Error(`Failed to load ${filename}: ${resp.status}`);
  return resp.json();
}

async function loadAllData() {
  buildLoadingList();
  const total = FILE_REGISTRY.length;
  let done = 0;
  let hasError = false;

  for (const entry of FILE_REGISTRY) {
    updateProgress(done, total, entry.label);
    try {
      const data = await loadJSON(entry.file);
      // store into the correct variable
      switch (entry.key) {
        case "overview_stats":     overviewData = data;     break;
        case "releaseYearData":    releaseYearData = data;  break;
        case "priceData":          priceData = data;        break;
        case "topTags":            topTags = data;          break;
        case "topGenres":          topGenres = data;        break;
        case "graphStats":         graphStats = data;       break;
        case "tagCooccurrence":    tagCooccurrence = data;  break;
      }
      markFile(entry.key, "done");
    } catch (err) {
      console.error("Failed to load", entry.file, err);
      markFile(entry.key, "error");
      hasError = true;
      // continue loading other files
    }
    done++;
    updateProgress(done, total, null);
  }

  if (hasError) {
    loadingStatus.textContent = "部分文件加载失败，请刷新重试";
    progressFile.textContent = "请确认已运行 python steam-scope/scripts/export_steam_scope_data.py";
    return;
  }

  console.log("Data loaded:", {
    overview: overviewData,
    releaseYears: releaseYearData.length,
    priceBuckets: priceData.length,
    topTags: topTags.length,
    topGenres: topGenres.length,
    graphStats,
    cooccurNodes: tagCooccurrence.nodes.length,
    cooccurEdges: tagCooccurrence.edges.length,
  });

  // Brief moment showing all-green before fade
  updateProgress(total, total, null);
  loadingStatus.textContent = "加载完成，正在渲染页面...";
  progressFile.textContent = "";

  setTimeout(() => {
    renderAll();
    loadingOverlay.classList.add("fade-out");
  }, 400);
}

// ── Render helpers ───────────────────────────────────────────────
const chartInstances = {};

function getOrCreateChart(domId) {
  if (chartInstances[domId]) return chartInstances[domId];
  const dom = document.getElementById(domId);
  if (!dom) return null;
  const chart = echarts.init(dom, null, { height: dom.clientHeight || 380 });
  chartInstances[domId] = chart;
  return chart;
}

function updateChart(domId, option) {
  const chart = getOrCreateChart(domId);
  if (chart) chart.setOption(option, { notMerge: true });
}

function darkThemeOpt(baseOpt) {
  return Object.assign(
    {
      backgroundColor: "transparent",
      textStyle: { color: "#8f98a0" },
    },
    baseOpt
  );
}

// ── 1. Overview Stats ────────────────────────────────────────────
function renderOverview() {
  if (!overviewData) return;
  document.getElementById("stat-total").textContent =
    (overviewData.total_games / 1000).toFixed(0) + "K";
  document.getElementById("stat-reviewed").textContent =
    (overviewData.reviewed_games / 1000).toFixed(0) + "K";
  document.getElementById("stat-free").textContent =
    overviewData.free_share_pct + "%";
  document.getElementById("stat-genres").textContent =
    overviewData.genre_count;
  document.getElementById("stat-tags").textContent =
    overviewData.tag_count;
  document.getElementById("stat-top-year").textContent =
    overviewData.top_release_year;
}

// ── 2. Release Year Chart ────────────────────────────────────────
function renderReleaseYear() {
  if (!releaseYearData) return;
  const chart = getOrCreateChart("chart-release-year");
  if (!chart) return;
  chart.setOption(
    darkThemeOpt({
      tooltip: { trigger: "axis" },
      grid: { left: 65, right: 30, top: 20, bottom: 40 },
      xAxis: {
        type: "category",
        data: releaseYearData.map((d) => d.year),
        axisLabel: { color: "#8f98a0", rotate: 45 },
        axisLine: { lineStyle: { color: "#2a475e" } },
      },
      yAxis: {
        type: "value",
        name: "游戏数量",
        axisLabel: { color: "#8f98a0" },
        splitLine: { lineStyle: { color: "#2a475e" } },
      },
      series: [
        {
          type: "bar",
          data: releaseYearData.map((d) => d.game_count),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "#66c0f4" },
              { offset: 1, color: "#1b4f72" },
            ]),
            borderRadius: [4, 4, 0, 0],
          },
        },
      ],
    }),
    { notMerge: true }
  );
  window.addEventListener("resize", () => chart.resize());
}

// ── 3. Price Structure ───────────────────────────────────────────
function renderPriceStructure() {
  if (!priceData) return;
  const chart1 = getOrCreateChart("chart-price-structure");
  if (chart1) {
    chart1.setOption(
      darkThemeOpt({
        tooltip: { trigger: "axis" },
        grid: { left: 75, right: 30, top: 30, bottom: 80 },
        xAxis: {
          type: "category",
          data: priceData.map((d) => d.bucket),
          axisLabel: { color: "#8f98a0", rotate: 30, fontSize: 11 },
          axisLine: { lineStyle: { color: "#2a475e" } },
        },
        yAxis: {
          type: "value",
          name: "游戏数量",
          axisLabel: { color: "#8f98a0" },
          splitLine: { lineStyle: { color: "#2a475e" } },
        },
        series: [
          {
            type: "bar",
            data: priceData.map((d) => d.game_count),
            itemStyle: { color: "#66c0f4", borderRadius: [4, 4, 0, 0] },
            label: { show: true, position: "top", color: "#8f98a0", fontSize: 10 },
          },
        ],
      })
    );
    window.addEventListener("resize", () => chart1.resize());
  }

  const chart2 = getOrCreateChart("chart-price-rate");
  if (chart2) {
    const rates = priceData
      .filter((d) => d.median_positive_rate != null)
      .map((d) => ({
        bucket: d.bucket,
        rate: d.median_positive_rate,
      }));
    const rateValues = rates.map((d) => d.rate);
    const yMin = Math.floor(Math.min(...rateValues) / 5) * 5;
    const yMax = Math.ceil(Math.max(...rateValues) / 5) * 5;
    chart2.setOption(
      darkThemeOpt({
        tooltip: { trigger: "axis", valueFormatter: (v) => (v != null ? v.toFixed(1) + "%" : "—") },
        grid: { left: 75, right: 30, top: 25, bottom: 80 },
        xAxis: {
          type: "category",
          data: rates.map((d) => d.bucket),
          axisLabel: { color: "#8f98a0", rotate: 30, fontSize: 10 },
          axisLine: { lineStyle: { color: "#2a475e" } },
        },
        yAxis: {
          type: "value",
          name: "好评率 (%)",
          nameLocation: "middle",
          nameGap: 45,
          min: yMin,
          max: yMax,
          axisLabel: { color: "#8f98a0", formatter: (v) => v + "%" },
          splitLine: { lineStyle: { color: "#2a475e" } },
        },
        series: [
          {
            type: "bar",
            data: rateValues,
            itemStyle: { color: "#a4d007", borderRadius: [4, 4, 0, 0] },
            label: {
              show: true,
              position: "top",
              color: "#8f98a0",
              fontSize: 10,
              formatter: (p) => (p.value != null ? p.value.toFixed(1) + "%" : "—"),
            },
          },
        ],
      })
    );
    window.addEventListener("resize", () => chart2.resize());
  }
}

// ── 4. Top Genres / Tags ─────────────────────────────────────────
function renderHorizontalBar(domId, data, labelField, valueField, color, labelFn) {
  const chart = getOrCreateChart(domId);
  if (!chart) return;
  const items = data.slice(0, 15);
  chart.setOption(
    darkThemeOpt({
      tooltip: { trigger: "axis" },
      grid: { left: 210, right: 40, top: 10, bottom: 20 },
      xAxis: {
        type: "value",
        axisLabel: { color: "#8f98a0" },
        splitLine: { lineStyle: { color: "#2a475e" } },
      },
      yAxis: {
        type: "category",
        data: items.map((d) => (labelFn ? labelFn(d[labelField]) : d[labelField])).reverse(),
        axisLabel: { color: "#8f98a0" },
        axisLine: { lineStyle: { color: "#2a475e" } },
        inverse: true,
      },
      series: [
        {
          type: "bar",
          data: items
            .map((d) => d[valueField])
            .reverse(),
          itemStyle: { color, borderRadius: [0, 4, 4, 0] },
        },
      ],
    }),
    { notMerge: true }
  );
  window.addEventListener("resize", () => chart.resize());
}

function renderTopGenres() {
  if (!topGenres) return;
  renderHorizontalBar("chart-top-genres", topGenres, "genre", "game_count", "#66c0f4", zhGenre);
}

function renderTopTags() {
  if (!topTags) return;
  renderHorizontalBar("chart-top-tags", topTags, "tag", "game_count", "#a4d007", zhTag);
}

// ── 5. Bubble Charts ─────────────────────────────────────────────
function renderBubbleChart(domId, data, labelField, countField, rateField, color, labelFn) {
  const chart = getOrCreateChart(domId);
  if (!chart) return;
  const items = data
    .filter((d) => d[rateField] != null && d.median_review_count > 0)
    .slice(0, 20);
  chart.setOption(
    darkThemeOpt({
      tooltip: {
        trigger: "item",
        formatter: (p) => {
          const d = p.data;
          return `<b>${d.name}</b><br/>游戏数量: ${d.value[0].toLocaleString()}<br/>中位评论数: ${d.value[1].toLocaleString()}<br/>中位好评率: ${d.value[2].toFixed(1)}%`;
        },
      },
      grid: { left: 80, right: 40, top: 30, bottom: 50 },
      xAxis: {
        type: "value",
        name: "游戏数量",
        nameLocation: "middle",
        nameGap: 30,
        axisLabel: { color: "#8f98a0" },
        splitLine: { lineStyle: { color: "#2a475e" } },
      },
      yAxis: {
        type: "value",
        name: "中位评论数",
        nameLocation: "middle",
        nameGap: 55,
        axisLabel: { color: "#8f98a0" },
        splitLine: { lineStyle: { color: "#2a475e" } },
      },
      series: [
        {
          type: "scatter",
          data: items.map((d) => ({
            name: labelFn ? labelFn(d[labelField]) : d[labelField],
            value: [
              d[countField],
              d.median_review_count,
              d[rateField],
            ],
          })),
          symbolSize: (val) => Math.max(8, Math.min(36, Math.sqrt(Math.max(0, val[2] - 50)) * 5)),
          itemStyle: { color, opacity: 0.6 },
          emphasis: { itemStyle: { opacity: 1, borderWidth: 2, borderColor: "#fff" }, scale: 1.3 },
        },
      ],
    }),
    { notMerge: true }
  );
  window.addEventListener("resize", () => chart.resize());
}

function renderTagBubble() {
  if (!topTags) return;
  renderBubbleChart("chart-tag-bubble", topTags, "tag", "game_count", "median_positive_rate", "#a4d007", zhTag);
}

function renderGenreBubble() {
  if (!topGenres) return;
  renderBubbleChart("chart-genre-bubble", topGenres, "genre", "game_count", "median_positive_rate", "#66c0f4", zhGenre);
}

// ── 6. Median Review Count Bar Charts ────────────────────────────
function renderReviewBar(domId, data, labelField, countField, color, labelFn) {
  const chart = getOrCreateChart(domId);
  if (!chart) return;
  const items = data
    .filter((d) => d[countField] > 0)
    .sort((a, b) => b[countField] - a[countField])
    .slice(0, 20);
  chart.setOption(
    darkThemeOpt({
      tooltip: { trigger: "axis" },
      grid: { left: 210, right: 40, top: 10, bottom: 20 },
      xAxis: {
        type: "value",
        name: "中位评论数",
        axisLabel: { color: "#8f98a0" },
        splitLine: { lineStyle: { color: "#2a475e" } },
      },
      yAxis: {
        type: "category",
        data: items.map((d) => (labelFn ? labelFn(d[labelField]) : d[labelField])).reverse(),
        axisLabel: { color: "#8f98a0" },
        axisLine: { lineStyle: { color: "#2a475e" } },
        inverse: true,
      },
      series: [
        {
          type: "bar",
          data: items.map((d) => d[countField]).reverse(),
          itemStyle: { color, borderRadius: [0, 4, 4, 0] },
        },
      ],
    }),
    { notMerge: true }
  );
  window.addEventListener("resize", () => chart.resize());
}

function renderTagReviews() {
  if (!topTags) return;
  renderReviewBar("chart-tag-reviews", topTags, "tag", "median_review_count", "#a4d007", zhTag);
}

function renderGenreReviews() {
  if (!topGenres) return;
  renderReviewBar("chart-genre-reviews", topGenres, "genre", "median_review_count", "#66c0f4", zhGenre);
}

// ── 7. Graph Stats ───────────────────────────────────────────────
function renderGraphStats() {
  if (!graphStats) return;
  document.getElementById("gs-games").textContent =
    (graphStats.game_nodes / 1000).toFixed(1) + "K";
  document.getElementById("gs-tags").textContent = graphStats.tag_nodes;
  document.getElementById("gs-genres").textContent = graphStats.genre_nodes;
  document.getElementById("gs-categories").textContent =
    graphStats.category_nodes;
  document.getElementById("gs-total-nodes").textContent =
    (graphStats.total_nodes / 1000).toFixed(1) + "K";
  document.getElementById("gs-total-edges").textContent =
    (graphStats.total_edges / 1000000).toFixed(2) + "M";
}

// ── 8. Tag Co-occurrence Network ─────────────────────────────────
function renderCooccurrenceGraph() {
  if (!tagCooccurrence) return;
  const chart = getOrCreateChart("chart-cooccurrence");
  if (!chart) return;

  const maxVal = Math.max(...tagCooccurrence.nodes.map((n) => n.value));
  const maxWeight = Math.max(...tagCooccurrence.edges.map((e) => e.weight));

  // Pre-compute zh labels for nodes and edges (use Chinese-only for graph to avoid clutter)
  function zhShort(en) {
    const cn = ZH_TAG[en] || en;
    return cn === en ? en : cn;  // Chinese name only, or English if no mapping
  }

  chart.setOption(
    darkThemeOpt({
      tooltip: {
        formatter: (p) => {
          if (p.dataType === "node") {
            return `<b>${zhTag(p.name)}</b><br/>关联游戏数: ${p.value}`;
          }
          return `<b>${zhTag(p.data.source)} — ${zhTag(p.data.target)}</b><br/>共现次数: ${p.data.value}`;
        },
      },
      series: [
        {
          type: "graph",
          layout: "force",
          roam: true,
          draggable: true,
          force: {
            initLayout: "circular",
            repulsion: 200,
            edgeLength: [100, 240],
            gravity: 0.05,
            friction: 0.1,
            layoutAnimation: true,
          },
          data: tagCooccurrence.nodes.map((n) => ({
            name: zhShort(n.id),
            value: n.value,
            symbolSize: 10 + (n.value / maxVal) * 40,
            itemStyle: {
              color: `rgba(102, 192, 244, ${0.35 + (n.value / maxVal) * 0.65})`,
            },
            label: { show: true, fontSize: 10, color: "#c6d4df" },
          })),
          edges: tagCooccurrence.edges.map((e) => ({
            source: zhShort(e.source),
            target: zhShort(e.target),
            value: e.weight,
            lineStyle: {
              width: 0.5 + (e.weight / maxWeight) * 4,
              color: `rgba(143, 152, 160, ${0.15 + (e.weight / maxWeight) * 0.45})`,
              curveness: 0.1,
            },
          })),
          emphasis: {
            focus: "adjacency",
            lineStyle: { width: 3 },
          },
        },
      ],
    }),
    { notMerge: true }
  );
  window.addEventListener("resize", () => chart.resize());
}

// ── 9. Co-occurrence Table ───────────────────────────────────────
function renderCooccurrenceTable() {
  if (!tagCooccurrence) return;
  const tbody = document.querySelector("#cooccur-table tbody");
  if (!tbody) return;
  const sorted = [...tagCooccurrence.edges].sort(
    (a, b) => b.weight - a.weight
  ).slice(0, 30);
  tbody.innerHTML = sorted
    .map(
      (e) =>
        `<tr><td>${zhTag(e.source)}</td><td>${zhTag(e.target)}</td><td>${e.weight.toLocaleString()}</td></tr>`
    )
    .join("");
}

// ── Sample-size filter ───────────────────────────────────────────
function filterByMinGames(data, countField, minGames) {
  if (!data) return [];
  return data.filter((d) => d[countField] >= minGames);
}

function renderFilterableCharts(minGames) {
  const filteredTags = filterByMinGames(topTags, "game_count", minGames);
  const filteredGenres = filterByMinGames(topGenres, "game_count", minGames);

  // Horizontal bar charts (Top 15)
  renderHorizontalBar("chart-top-genres", filteredGenres, "genre", "game_count", "#66c0f4", zhGenre);
  renderHorizontalBar("chart-top-tags", filteredTags, "tag", "game_count", "#a4d007", zhTag);

  // Bubble charts (Top 30)
  renderBubbleChart("chart-tag-bubble", filteredTags, "tag", "game_count", "median_positive_rate", "#a4d007", zhTag);
  renderBubbleChart("chart-genre-bubble", filteredGenres, "genre", "game_count", "median_positive_rate", "#66c0f4", zhGenre);

  // Review count bar charts (Top 20)
  renderReviewBar("chart-tag-reviews", filteredTags, "tag", "median_review_count", "#a4d007", zhTag);
  renderReviewBar("chart-genre-reviews", filteredGenres, "genre", "median_review_count", "#66c0f4", zhGenre);
}

function initSampleFilter() {
  const slider = document.getElementById("min-sample-slider");
  const display = document.getElementById("min-sample-value");
  if (!slider || !display) return;

  // Set slider max based on data
  const maxGames = Math.max(
    ...(topTags || []).map((d) => d.game_count),
    ...(topGenres || []).map((d) => d.game_count)
  );
  slider.max = Math.min(2000, maxGames);

  slider.addEventListener("input", () => {
    const val = parseInt(slider.value);
    display.textContent = val;
    renderFilterableCharts(val);
  });

  // Trigger initial render at default threshold
  const initialVal = parseInt(slider.value);
  display.textContent = initialVal;
  renderFilterableCharts(initialVal);
}

// ── Main Render ──────────────────────────────────────────────────
function renderAll() {
  renderOverview();
  renderReleaseYear();
  renderPriceStructure();
  renderGraphStats();
  renderCooccurrenceGraph();
  renderCooccurrenceTable();
  initSampleFilter();
}

// ── Bootstrap ────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", loadAllData);
