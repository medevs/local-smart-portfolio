"""Generic response models."""

from pydantic import BaseModel, Field
from typing import Any, Optional, List
from datetime import datetime


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now)
    services: dict = Field(
        default={},
        description="Status of dependent services"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00",
                "services": {
                    "ollama": "connected",
                    "chromadb": "connected"
                }
            }
        }


class APIResponse(BaseModel):
    """Generic API response wrapper."""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(default=None, description="Response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {}
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(default=False)
    error: str = Field(..., description="Error type/code")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "Invalid request data",
                "detail": "Field 'message' is required"
            }
        }


class DatabaseStats(BaseModel):
    """Statistics about the vector database."""
    total_documents: int = Field(default=0)
    total_chunks: int = Field(default=0)
    collection_name: str = Field(...)
    embedding_model: str = Field(...)


class SystemMetricsResponse(BaseModel):
    """System metrics response."""
    cpu_usage: float = Field(..., description="CPU usage percentage")
    ram_usage_gb: float = Field(..., description="RAM usage in GB")
    ram_usage_percent: float = Field(..., description="RAM usage percentage")
    ram_total_gb: float = Field(..., description="Total RAM in GB")
    uptime_days: int = Field(..., description="System uptime in days")
    uptime_hours: int = Field(..., description="System uptime in hours")
    uptime_percent: float = Field(..., description="Uptime percentage")
    disk_usage_percent: float = Field(..., description="Disk usage percentage")
    disk_free_gb: float = Field(..., description="Free disk space in GB")
    model_latency_ms: float = Field(..., description="Ollama model latency in milliseconds")
    timestamp: str = Field(..., description="Timestamp of metrics collection")
    error: Optional[str] = Field(default=None, description="Error message if any")


class BenchmarkResult(BaseModel):
    """Single benchmark result for a model."""
    model: str = Field(..., description="Model name")
    speed_tokens_per_sec: float = Field(..., description="Tokens per second")
    speed_display: str = Field(..., description="Formatted speed string")
    memory_gb: float = Field(..., description="Memory usage in GB")
    memory_display: str = Field(..., description="Formatted memory string")
    latency_ms: float = Field(..., description="Latency in milliseconds")
    quality_score: int = Field(..., description="Quality score (0-100)")
    last_benchmarked: str = Field(..., description="Last benchmark timestamp")


class BenchmarksResponse(BaseModel):
    """Benchmarks response."""
    benchmarks: List[BenchmarkResult] = Field(..., description="List of benchmark results")
    timestamp: str = Field(..., description="Timestamp of benchmarks collection")