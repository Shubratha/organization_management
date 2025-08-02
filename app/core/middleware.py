import time
import traceback
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging import get_logger

logger = get_logger(__name__)


async def error_handler_middleware(request: Request, call_next: Callable) -> Response:
    """Global error handling middleware."""
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log request details
        logger.info(
            "request_processed",
            extra={
                "path": request.url.path,
                "method": request.method,
                "process_time": process_time,
                "status_code": response.status_code,
            },
        )

        return response

    except SQLAlchemyError as e:
        logger.error("database_error", extra={"error": str(e), "path": request.url.path, "method": request.method})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Database error occurred"}
        )

    except Exception as e:
        logger.error(
            "unhandled_error",
            extra={
                "error": str(e),
                "path": request.url.path,
                "method": request.method,
                "traceback": traceback.format_exc(),
            },
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal server error"}
        )
