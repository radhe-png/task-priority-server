from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from app.core.config import settings

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger(__name__)
        logger.info(f"{request.method} {request.url}")
        try:
            response = await call_next(request)
            logger.info(f"Response status: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response