"""
Health check endpoint.
Used to verify the API and dependent services are running.
"""

from fastapi import APIRouter
from datetime import datetime
from app.config import get_settings
from app.models.response import HealthResponse
from app.services.ollama_client import get_ollama_client
from app.services.chroma_client import get_chroma_service
from app.utils.logger import logger

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check the health status of the API and dependent services.
    
    Returns:
        HealthResponse with status of all services
    """
    settings = get_settings()
    
    # Check Ollama
    ollama = get_ollama_client()
    ollama_connected = await ollama.check_connection()
    
    # Check ChromaDB
    chroma = get_chroma_service()
    chroma_connected = chroma.check_connection()
    
    # Determine overall status
    all_healthy = ollama_connected and chroma_connected
    status = "healthy" if all_healthy else "degraded"
    
    services = {
        "ollama": "connected" if ollama_connected else "disconnected",
        "chromadb": "connected" if chroma_connected else "disconnected",
    }
    
    if not all_healthy:
        logger.warning(f"Health check - Status: {status}, Services: {services}")
    
    return HealthResponse(
        status=status,
        version=settings.app_version,
        timestamp=datetime.now(),
        services=services,
    )


@router.get("/ready")
async def readiness_check():
    """
    Simple readiness check for load balancers.
    
    Returns:
        Simple OK response
    """
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """
    Simple liveness check for container orchestration.
    
    Returns:
        Simple OK response
    """
    return {"status": "alive"}

