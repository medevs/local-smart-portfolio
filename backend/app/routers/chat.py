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
from app.services.observability import get_observability_service
from app.utils.logger import logger
from app.middleware.rate_limit import limiter, get_chat_limit, get_chat_stream_limit
from app.config import get_settings

router = APIRouter(prefix="/chat", tags=["Chat"])


from app.agent.core import Agent

@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
@limiter.limit(get_chat_limit)
async def chat(request: Request, chat_request: ChatRequest) -> ChatResponse:
    """
    Send a message and get an AI response using Agentic RAG.
    """
    logger.info(f"Chat request: {chat_request.message[:100]}...")
    settings = get_settings()
    
    try:
        # Convert history to dict format
        history = None
        if chat_request.history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.history
            ]
            
        agent = Agent()
        response = await agent.run(chat_request.message, history=history)
        
        # Parse response to extract sources if possible, or Agent should return them.
        # Currently Agent returns string.
        # rag.txt says "cite sources using metadata".
        # So the sources should be IN the text.
        # But ChatResponse model expects `sources` list.
        # We can extract them or just leave empty for now, as the text contains citations.
        
        return ChatResponse(
            response=response,
            sources=[] # Sources are embedded in the text citation
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
    Send a message and get a streaming AI response using Agentic RAG.
    Note: Currently sends the full response as a single chunk after processing.
    """
    logger.info(f"Streaming chat request: {chat_request.message[:100]}...")
    settings = get_settings()

    async def generate():
        try:
            # Convert history to dict format
            history = None
            if chat_request.history:
                history = [
                    {"role": msg.role, "content": msg.content}
                    for msg in chat_request.history
                ]

            agent = Agent()
            # Agent processing (plan -> execute -> merge -> generate)
            response = await agent.run(chat_request.message, history=history)
            
            # Yield the full response as a single chunk
            # In the future, we could stream tokens from Ollama in the final step of Agent
            chunk_data = {
                "chunk": response,
                "done": False,
                "sources": [] # Sources embedded in text
            }
            yield f"data: {json.dumps(chunk_data)}\n\n"

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
            "X-Accel-Buffering": "no",
        }
    )

