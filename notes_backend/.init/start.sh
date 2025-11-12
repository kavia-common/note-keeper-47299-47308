#!/usr/bin/env bash
# Start script for notes_backend using the correct module path.
# Uses local venv if present; otherwise falls back to system python env with uvicorn installed.

set -euo pipefail

APP_MODULE="src.api.main:app"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-3000}"
LOG_LEVEL="${LOG_LEVEL:-info}"
RELOAD_FLAG="${RELOAD_FLAG:-}"

# Activate virtualenv if exists
if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
fi

# PUBLIC_INTERFACE
# start_app: Entry script to run the FastAPI server
# This will start uvicorn with the proper app import path following the repository layout.
# Parameters (via env):
# - HOST: host binding (default 0.0.0.0)
# - PORT: port to listen on (default 3000)
# - LOG_LEVEL: uvicorn log level (default info)
# - RELOAD_FLAG: set to --reload for dev mode (default empty)
# Returns: exits with uvicorn's status code
uvicorn "${APP_MODULE}" --host "${HOST}" --port "${PORT}" --log-level "${LOG_LEVEL}" ${RELOAD_FLAG}
