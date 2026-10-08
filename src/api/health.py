from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=200)
def health_check():
    """Health check endpoint returning 200 within 1 second of successful startup (NFR-07)."""
    return {
        "status": "healthy",
        "service": "MarketScope Platform",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
