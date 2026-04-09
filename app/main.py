"""FastAPI application entrypoint for ContractClear AI.

The application exposes a health endpoint and a contract analysis endpoint that
accepts a document plus user context, extracts text, builds the risk-analysis
prompt, and returns a structured assessment.
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import router as analysis_router

STATIC_DIR = Path(__file__).resolve().parent / "static"


def _file_response(name: str) -> FileResponse:
    """Return a static HTML page by filename."""

    return FileResponse(STATIC_DIR / name)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="ContractClear AI",
        version="0.1.0",
        description="Backend for contract risk analysis using Cloudflare AI.",
    )
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    async def landing_page() -> FileResponse:
        """Serve landing page."""

        return _file_response("index.html")

    @app.get("/upload")
    async def upload_page() -> FileResponse:
        """Serve upload page."""

        return _file_response("upload.html")

    @app.get("/context")
    async def context_page() -> FileResponse:
        """Serve context page."""

        return _file_response("context.html")

    @app.get("/result")
    async def result_page() -> FileResponse:
        """Serve result page."""

        return _file_response("result.html")

    app.include_router(analysis_router)
    return app


app = create_app()
