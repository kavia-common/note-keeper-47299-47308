from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Attempt to load environment variables if python-dotenv is available.
# This guard prevents startup failures if python-dotenv isn't installed.
try:
    import dotenv  # type: ignore
    dotenv.load_dotenv()
except Exception:
    # Silently continue if dotenv isn't present or load fails
    pass

# PUBLIC_INTERFACE
app = FastAPI()
"""FastAPI application instance for the Notes backend API."""

# Configure permissive CORS for development and preview environments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/")
def health_check():
    """Health check endpoint.

    Returns:
        dict: A simple confirmation that the service is running.
    """
    return {"message": "Healthy"}


# Allow running this module directly: python -m src.api.main
if __name__ == "__main__":
    # Lazy import to avoid uvicorn hard dependency when imported as a module
    try:
        import uvicorn  # type: ignore
    except Exception as e:
        raise SystemExit(
            "uvicorn is required to run the development server. "
            "Install dependencies with: pip install -r requirements.txt"
        ) from e

    uvicorn.run("src.api.main:app", host="0.0.0.0", port=3000, log_level="info")
