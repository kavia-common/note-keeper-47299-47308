#!/usr/bin/env bash
set -euo pipefail

# Defaults
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-3000}"
LOG_LEVEL="${LOG_LEVEL:-info}"
RELOAD_FLAG="${RELOAD_FLAG:-}"

# Move to repo root if invoked from nested directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Ensure Python path includes current container root for src.* imports
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"

# Validate uvicorn is installed
if ! command -v uvicorn >/dev/null 2>&1; then
  echo "ERROR: uvicorn not found. Please install dependencies: pip install -r requirements.txt" >&2
  exit 1
fi

# Start uvicorn with correct module path
# Example:
# HOST=0.0.0.0 PORT=3000 LOG_LEVEL=info RELOAD_FLAG=--reload bash .init/start.sh
echo "Starting notes_backend via uvicorn: src.api.main:app at ${HOST}:${PORT} (log-level=${LOG_LEVEL}) ${RELOAD_FLAG}"
exec uvicorn "src.api.main:app" --host "${HOST}" --port "${PORT}" --log-level "${LOG_LEVEL}" ${RELOAD_FLAG}
