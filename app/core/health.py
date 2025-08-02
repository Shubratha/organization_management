import time
from typing import Dict

import psutil
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.session import get_session

router = APIRouter(tags=["Health"])


async def check_database(session: AsyncSession) -> bool:
    """Check database connectivity."""
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)) -> Dict:
    """Basic health check endpoint."""
    return {"status": "healthy", "version": settings.VERSION, "database": await check_database(session)}


@router.get("/health/detailed")
async def detailed_health_check(session: AsyncSession = Depends(get_session)) -> Dict:
    """Detailed health check with system metrics."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": time.time(),
        "database": await check_database(session),
        "system": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
        },
    }
