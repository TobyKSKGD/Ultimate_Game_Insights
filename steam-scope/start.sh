#!/bin/bash
# SteamScope local dev server launcher
# Usage: bash steam-scope/start.sh [port]

PORT=${1:-8000}
DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Kill existing process on the same port ────────────────────────
PID=$(lsof -ti tcp:$PORT 2>/dev/null)
if [ -n "$PID" ]; then
  echo "[steam-scope] Port $PORT is in use by PID $PID — killing it..."
  kill -9 $PID 2>/dev/null
  sleep 0.3
fi

# ── Start server ──────────────────────────────────────────────────
echo "[steam-scope] Starting server at http://localhost:$PORT/"
cd "$DIR" && python3 -m http.server $PORT
