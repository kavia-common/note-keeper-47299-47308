# Notes Backend

FastAPI backend service for the Notes application.

## Run locally

Ensure dependencies are installed in the provided virtual environment or your system Python.

Recommended:
- Activate the venv: `source venv/bin/activate`
- Start the server (correct app import path):
  - `uvicorn src.api.main:app --host 0.0.0.0 --port 3000 --log-level info`

Alternatively, use the helper script:
- `bash .init/start.sh`
  - Supports env vars: HOST (default 0.0.0.0), PORT (default 3000), LOG_LEVEL (default info), RELOAD_FLAG (set to --reload for dev mode)

Preview/CI boot command:
- Preferred:
  - `bash note-keeper-47299-47308/notes_backend/.init/start.sh`
  - This binds to 0.0.0.0:3000 and serves src.api.main:app
- Compatibility:
  - This repo also provides a top-level `main.py` which re-exports `app` from `src.api.main`.
  - Runners that invoke `uvicorn main:app --host 0.0.0.0 --port 3000` will now work.

Health check:
- GET http://localhost:3000/ returns: `{"message":"Healthy"}`
