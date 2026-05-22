/**
 * SteamScope — Game Recommender
 * Loads game_index.json and graph_recommendations.json for search + similarity display.
 */

const DATA_DIR = "data/";

let gameIndex, recommendations;
let gameIndexMap = {};

const REC_FILE_REGISTRY = [
  { key: "gameIndex",       file: "game_index.json",              label: "游戏索引（5,000 款）", size: "~5.4 MB" },
  { key: "recommendations", file: "graph_recommendations.json",   label: "推荐结果（1,000 款）", size: "~7.0 MB" },
];

// ── Loading UI ────────────────────────────────────────────────────
const progressFill  = document.getElementById("progress-bar-fill");
const progressFile  = document.getElementById("loading-file");
const progressList  = document.getElementById("loading-list");
const loadingOverlay = document.getElementById("loading-overlay");
const loadingStatus = document.getElementById("loading-status");

function buildLoadingList() {
  let html = "";
  for (const entry of REC_FILE_REGISTRY) {
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
  if (status === "done")  icon.textContent = "✓";
  if (status === "error") icon.textContent = "✗";
}

async function loadJSON(filename) {
  const resp = await fetch(DATA_DIR + filename);
  if (!resp.ok) throw new Error(`Failed to load ${filename}: ${resp.status}`);
  return resp.json();
}

async function loadRecData() {
  buildLoadingList();
  const total = REC_FILE_REGISTRY.length;
  let done = 0, hasError = false;

  for (const entry of REC_FILE_REGISTRY) {
    updateProgress(done, total, entry.label);
    try {
      const data = await loadJSON(entry.file);
      if (entry.key === "gameIndex") gameIndex = data;
      if (entry.key === "recommendations") recommendations = data;
      markFile(entry.key, "done");
    } catch (err) {
      console.error("Failed to load", entry.file, err);
      markFile(entry.key, "error");
      hasError = true;
    }
    done++;
    updateProgress(done, total, null);
  }

  if (hasError) {
    loadingStatus.textContent = "数据加载失败，请刷新重试";
    return;
  }

  // Build search index on lowercase name
  gameIndexMap = {};
  for (const g of gameIndex) {
    const key = g.name.toLowerCase();
    if (!gameIndexMap[key]) gameIndexMap[key] = [];
    gameIndexMap[key].push(g);
  }

  updateProgress(total, total, null);
  loadingStatus.textContent = "加载完成";
  progressFile.textContent = "";

  setTimeout(() => {
    loadingOverlay.classList.add("fade-out");
    initSearch();
  }, 300);
}

// ── Search ────────────────────────────────────────────────────────
function initSearch() {
  const input = document.getElementById("search-input");
  const suggestions = document.getElementById("search-suggestions");
  const hint = document.getElementById("rec-empty-hint");

  input.focus();

  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    if (query.length < 2) {
      suggestions.classList.remove("active");
      return;
    }
    const matches = [];
    for (const key of Object.keys(gameIndexMap)) {
      if (key.includes(query)) {
        for (const g of gameIndexMap[key]) {
          if (matches.length < 10) matches.push(g);
        }
      }
      if (matches.length >= 10) break;
    }
    if (matches.length === 0) {
      suggestions.innerHTML =
        '<div class="suggestion-item" style="color:#8f98a0;">未找到匹配游戏</div>';
    } else {
      suggestions.innerHTML = matches
        .map(
          (g) =>
            `<div class="suggestion-item" data-appid="${g.appid}">
              ${g.name}
              <span style="color:#8f98a0;font-size:0.78rem;">
                — ${g.review_count_calc.toLocaleString()} 评论 | ${g.positive_rate_calc}% 好评
                ${g.genres.length ? '| ' + g.genres.slice(0,2).map(t => zhGenre(t)).join(' · ') : ''}
              </span>
            </div>`
        )
        .join("");
    }
    suggestions.classList.add("active");
  });

  suggestions.addEventListener("click", (e) => {
    const item = e.target.closest(".suggestion-item");
    if (!item || !item.dataset.appid) return;
    const appid = parseInt(item.dataset.appid);
    const game = gameIndex.find((g) => g.appid === appid);
    input.value = game ? game.name : "";
    suggestions.classList.remove("active");
    if (hint) hint.style.display = "none";
    showRecommendations(appid);
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const query = input.value.trim().toLowerCase();
      const found = gameIndex.find((g) => g.name.toLowerCase() === query);
      if (found) {
        suggestions.classList.remove("active");
        if (hint) hint.style.display = "none";
        showRecommendations(found.appid);
      } else {
        for (const key of Object.keys(gameIndexMap)) {
          if (key.includes(query)) {
            const g = gameIndexMap[key][0];
            suggestions.classList.remove("active");
            if (hint) hint.style.display = "none";
            showRecommendations(g.appid);
            input.value = g.name;
            break;
          }
        }
      }
    }
  });

  document.addEventListener("click", (e) => {
    if (!input.parentElement.contains(e.target)) {
      suggestions.classList.remove("active");
    }
  });
}

// ── Display ───────────────────────────────────────────────────────
function showRecommendations(appid) {
  const container = document.getElementById("rec-results");
  if (!container) return;
  const game = gameIndex.find((g) => g.appid === appid);
  if (!game) {
    container.innerHTML = '<div class="rec-empty">未找到该游戏</div>';
    return;
  }

  const recs = recommendations[String(appid)] || recommendations[appid];
  if (!recs || recs.length === 0) {
    container.innerHTML = '<div class="rec-empty">该游戏暂无推荐结果</div>';
    return;
  }

  // Build target game card
  const targetTags = game.tags.slice(0, 5).map(t => `<span>${zhTag(t)}</span>`).join("");

  // Read display count from select
  const countSelect = document.getElementById("rec-count-select");
  const showCount = countSelect ? parseInt(countSelect.value) : 10;
  const shown = recs.slice(0, showCount);

  container.innerHTML =
    `<div class="rec-target-card" style="background:var(--card);border:1px solid var(--accent);border-radius:var(--radius);padding:18px;margin-bottom:20px;">
      <div style="font-size:1.1rem;font-weight:700;color:var(--accent);">${game.name}</div>
      <div class="rec-meta" style="font-size:0.82rem;color:var(--text2);margin-top:4px;">
        价格: ${game.price === 0 ? "免费" : "$" + game.price.toFixed(2)} |
        评论数: ${game.review_count_calc.toLocaleString()} |
        好评率: ${game.positive_rate_calc}% |
        发行年份: ${game.release_year || "—"}
      </div>
      ${targetTags ? `<div class="rec-tags" style="margin-top:6px;">${targetTags}</div>` : ""}
      <div style="font-size:0.8rem;color:var(--text2);margin-top:6px;">${game.short_description || ""}</div>
    </div>` +
    shown
      .map(
        (r) => `
      <div class="rec-card">
        <div class="rec-name">${r.name}</div>
        <div class="rec-score">相似度: ${(r.score * 100).toFixed(1)}%</div>
        <div class="rec-meta">
          价格: ${r.price === 0 ? "免费" : "$" + r.price.toFixed(2)} |
          评论数: ${r.review_count_calc.toLocaleString()} |
          好评率: ${r.positive_rate_calc}%
        </div>
        <div class="rec-tags">
          ${r.shared_tags.map((t) => `<span>${zhTag(t)}</span>`).join("")}
          ${r.shared_genres.map((g) => `<span>${zhGenre(g)}</span>`).join("")}
          ${r.shared_categories.map((c) => `<span>${zhCategory(c)}</span>`).join("")}
        </div>
        <div class="rec-reason">${r.reason}</div>
      </div>`
      )
      .join("");
}

// ── Bootstrap ────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", loadRecData);
