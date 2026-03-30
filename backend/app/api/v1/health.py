from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", summary="Service health check")
async def health_check() -> dict:
    """Return a simple uptime health check response."""
    return {"status": "ok"}
