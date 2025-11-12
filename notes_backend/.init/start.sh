#!/usr/bin/env bash
set -euo pipefail

# Simple bootstrap script to run the FastAPI server consistently in preview/CI.
# Variables:
#   HOST        - Bind host (default: 0.0.0.0)
#   PORT        - Bind port (default: 3000)
#   LOG_LEVEL   - Uvicorn log level (default: info)
#   RELOAD_FLAG - Set to '--reload' for dev mode hot reload, otherwise empty

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-3000}"
LOG_LEVEL="${LOG_LEVEL:-info}"
RELOAD_FLAG="${RELOAD_FLAG:-}"

# Prefer canonical module path to avoid import ambiguity
APP_PATH="src.api.main:app"

# Fall back to main:app if needed by some runners, but we will always call the canonical path here
CMD=("uvicorn" "${APP_PATH}" "--host" "${HOST}" "--port" "${PORT}" "--log-level" "${LOG_LEVEL}")

if [[ -n "${RELOAD_FLAG}" ]]; then
  CMD+=("${RELOAD_FLAG}")
fi

echo "[notes_backend] Starting uvicorn with: ${CMD[*]}"
exec "${CMD[@]}"
