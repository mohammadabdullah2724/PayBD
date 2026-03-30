from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="PayBD API")
app.include_router(api_router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["Health"])
async def health_check() -> dict:
    """Return API health status."""
    return {"status": "ok"}
