"""
Chat endpoint with RAG-powered responses.
Supports both regular and streaming responses.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
from typing import Optional
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag import get_rag_service
from app.utils.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message and get an AI response.
    Uses RAG to retrieve relevant context from the knowledge base.
    
    Args:
        request: ChatRequest with message and optional history
        
    Returns:
        ChatResponse with AI response and sources
    """
    logger.info(f"Chat request: {request.message[:100]}...")
    
    try:
        rag = get_rag_service()
        
        # Convert history to dict format
        history = None
        if request.history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.history
            ]
        
        result = await rag.query(
            question=request.message,
            history=history
        )
        
        logger.info(f"Chat response generated, sources: {result.get('sources', [])}")
        
        return ChatResponse(
            response=result["response"],
            sources=result.get("sources", [])
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response"
        )


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Send a message and get a streaming AI response.
    Uses Server-Sent Events (SSE) for real-time streaming.
    
    Args:
        request: ChatRequest with message and optional history
        
    Returns:
        StreamingResponse with SSE events
    """
    logger.info(f"Streaming chat request: {request.message[:100]}...")
    
    async def generate():
        try:
            rag = get_rag_service()
            
            # Convert history to dict format
            history = None
            if request.history:
                history = [
                    {"role": msg.role, "content": msg.content}
                    for msg in request.history
                ]
            
            async for chunk_data in rag.query_stream(
                question=request.message,
                history=history
            ):
                # Format as SSE event
                event_data = json.dumps(chunk_data)
                yield f"data: {event_data}\n\n"
            
            # Send done event
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )

