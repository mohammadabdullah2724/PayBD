from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize local database resources before serving requests."""
    await init_db()
    yield


app = FastAPI(title="PayBD API", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")


@app.get("/api/v1/health", tags=["Health"])
async def health_check() -> dict:
    """Return API health status."""
    return {"status": "ok"}
