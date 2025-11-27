"""Chat-related Pydantic models."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Tell me about your homelab setup",
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=4000, description="User's message")
    history: Optional[List[ChatMessage]] = Field(
        default=[],
        description="Previous messages for context"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What technologies do you use in your homelab?",
                "history": []
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Assistant's response")
    sources: Optional[List[str]] = Field(
        default=[],
        description="Source documents used for the response"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "My homelab uses Docker, Proxmox, and various self-hosted services...",
                "sources": ["homelab-docs.md", "infrastructure.pdf"]
            }
        }


class StreamingChatResponse(BaseModel):
    """Model for streaming chat response chunks."""
    chunk: str = Field(..., description="Text chunk from the stream")
    done: bool = Field(default=False, description="Whether streaming is complete")
    sources: Optional[List[str]] = Field(
        default=None,
        description="Source documents (only included in final chunk)"
    )

