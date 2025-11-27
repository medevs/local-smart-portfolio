"""Generic response models."""

from pydantic import BaseModel, Field
from typing import Any, Optional
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

