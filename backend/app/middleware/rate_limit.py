"""
Rate limiting middleware using slowapi.
Protects endpoints from abuse and ensures fair usage.
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from app.config import get_settings


def get_rate_limit_key(request: Request) -> str:
    """
    Get the rate limit key for a request.
    Uses X-Forwarded-For header if behind a proxy, otherwise client IP.
    """
    # Check for forwarded header (when behind nginx/proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Get the first IP in the chain (original client)
        return forwarded.split(",")[0].strip()

    # Fall back to direct client IP
    return get_remote_address(request)


# Create limiter instance
limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=["100/minute"],  # Default limit for all endpoints
    storage_uri="memory://",  # Use in-memory storage (use Redis for production clusters)
    strategy="fixed-window",  # Count requests in fixed time windows
)


# Rate limit configurations based on environment
class RateLimitConfig:
    """Rate limit configurations for different environments."""

    # Development limits (more permissive)
    DEV = {
        "chat": "60/minute",
        "chat_stream": "30/minute",
        "ingest": "20/minute",
        "admin": "100/minute",
        "metrics": "120/minute",
        "health": "300/minute",
    }

    # Production limits (more restrictive)
    PROD = {
        "chat": "20/minute",
        "chat_stream": "10/minute",
        "ingest": "5/minute",
        "admin": "30/minute",
        "metrics": "60/minute",
        "health": "120/minute",
    }

    @classmethod
    def get_limits(cls) -> dict:
        """Get rate limits based on debug setting."""
        settings = get_settings()
        return cls.DEV if settings.debug else cls.PROD


def get_chat_limit() -> str:
    """Get rate limit for chat endpoint."""
    return RateLimitConfig.get_limits()["chat"]


def get_chat_stream_limit() -> str:
    """Get rate limit for streaming chat endpoint."""
    return RateLimitConfig.get_limits()["chat_stream"]


def get_ingest_limit() -> str:
    """Get rate limit for document ingestion."""
    return RateLimitConfig.get_limits()["ingest"]


def get_admin_limit() -> str:
    """Get rate limit for admin endpoints."""
    return RateLimitConfig.get_limits()["admin"]


def get_metrics_limit() -> str:
    """Get rate limit for metrics endpoints."""
    return RateLimitConfig.get_limits()["metrics"]


def get_health_limit() -> str:
    """Get rate limit for health endpoints."""
    return RateLimitConfig.get_limits()["health"]
