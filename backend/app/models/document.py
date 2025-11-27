"""Document-related Pydantic models."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DocumentMetadata(BaseModel):
    """Metadata for a document in the knowledge base."""
    id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File extension/type")
    file_size: int = Field(..., description="File size in bytes")
    chunk_count: int = Field(default=0, description="Number of chunks created")
    uploaded_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_abc123",
                "filename": "homelab-guide.md",
                "file_type": ".md",
                "file_size": 15360,
                "chunk_count": 12,
                "uploaded_at": "2024-01-15T10:30:00"
            }
        }


class DocumentUploadResponse(BaseModel):
    """Response after uploading and processing a document."""
    success: bool = Field(..., description="Whether upload was successful")
    message: str = Field(..., description="Status message")
    document: Optional[DocumentMetadata] = Field(
        default=None,
        description="Document metadata if successful"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Document uploaded and indexed successfully",
                "document": {
                    "id": "doc_abc123",
                    "filename": "homelab-guide.md",
                    "file_type": ".md",
                    "file_size": 15360,
                    "chunk_count": 12,
                    "uploaded_at": "2024-01-15T10:30:00"
                }
            }
        }


class DocumentListResponse(BaseModel):
    """Response containing list of documents."""
    documents: List[DocumentMetadata] = Field(
        default=[],
        description="List of document metadata"
    )
    total_count: int = Field(default=0, description="Total number of documents")
    total_chunks: int = Field(default=0, description="Total number of chunks across all documents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "documents": [
                    {
                        "id": "doc_abc123",
                        "filename": "homelab-guide.md",
                        "file_type": ".md",
                        "file_size": 15360,
                        "chunk_count": 12,
                        "uploaded_at": "2024-01-15T10:30:00"
                    }
                ],
                "total_count": 1,
                "total_chunks": 12
            }
        }


class DocumentDeleteResponse(BaseModel):
    """Response after deleting a document."""
    success: bool = Field(..., description="Whether deletion was successful")
    message: str = Field(..., description="Status message")
    deleted_id: Optional[str] = Field(
        default=None,
        description="ID of deleted document"
    )

