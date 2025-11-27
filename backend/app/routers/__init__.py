"""API routers for the application."""

from .health import router as health_router
from .chat import router as chat_router
from .ingest import router as ingest_router
from .admin import router as admin_router
from .documents import router as documents_router

__all__ = [
    "health_router",
    "chat_router",
    "ingest_router",
    "admin_router",
    "documents_router",
]

