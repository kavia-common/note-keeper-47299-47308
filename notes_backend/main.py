"""
Entrypoint module to support preview systems that run `uvicorn main:app`.

This module imports the FastAPI `app` from the canonical location `src.api.main`.
"""

# PUBLIC_INTERFACE
from src.api.main import app  # noqa: F401
"""FastAPI application instance imported from src.api.main."""
