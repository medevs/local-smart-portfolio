"""
Chat endpoint with RAG-powered responses.
Supports both regular and streaming responses.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
import json
from typing import Optional
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag import get_rag_service
from app.utils.logger import logger
from app.middleware.rate_limit import limiter, get_chat_limit, get_chat_stream_limit

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
@limiter.limit(get_chat_limit)
async def chat(request: Request, chat_request: ChatRequest) -> ChatResponse:
    """
    Send a message and get an AI response.
    Uses RAG to retrieve relevant context from the knowledge base.

    Args:
        request: FastAPI Request object (for rate limiting)
        chat_request: ChatRequest with message and optional history

    Returns:
        ChatResponse with AI response and sources
    """
    logger.info(f"Chat request: {chat_request.message[:100]}...")

    try:
        rag = get_rag_service()

        # Convert history to dict format
        history = None
        if chat_request.history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.history
            ]

        result = await rag.query(
            question=chat_request.message,
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
@limiter.limit(get_chat_stream_limit)
async def chat_stream(request: Request, chat_request: ChatRequest):
    """
    Send a message and get a streaming AI response.
    Uses Server-Sent Events (SSE) for real-time streaming.

    Args:
        request: FastAPI Request object (for rate limiting)
        chat_request: ChatRequest with message and optional history

    Returns:
        StreamingResponse with SSE events
    """
    logger.info(f"Streaming chat request: {chat_request.message[:100]}...")

    async def generate():
        try:
            rag = get_rag_service()

            # Convert history to dict format
            history = None
            if chat_request.history:
                history = [
                    {"role": msg.role, "content": msg.content}
                    for msg in chat_request.history
                ]

            async for chunk_data in rag.query_stream(
                question=chat_request.message,
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

