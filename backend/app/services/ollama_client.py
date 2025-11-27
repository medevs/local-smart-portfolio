"""
Ollama LLM client for generating responses.
Supports both streaming and non-streaming responses.
"""

import httpx
import json
from typing import AsyncGenerator, Optional
from app.config import get_settings
from app.utils.logger import logger


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        settings = get_settings()
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.timeout = httpx.Timeout(120.0, connect=10.0)
        
    async def check_connection(self) -> bool:
        """Check if Ollama is available."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    async def list_models(self) -> list:
        """List available models."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
                return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def _build_prompt(self, query: str, context: str, history: list = None) -> str:
        """Build the prompt with context and history."""
        system_prompt = """You are an AI assistant for a developer's portfolio website. 
You help visitors learn about the developer's skills, projects, homelab setup, and experience.
Use the provided context to answer questions accurately and helpfully.
If the context doesn't contain relevant information, say so honestly but try to be helpful.
Keep responses concise but informative."""

        prompt_parts = [f"System: {system_prompt}\n"]
        
        if context:
            prompt_parts.append(f"Context from knowledge base:\n{context}\n")
        
        if history:
            prompt_parts.append("Previous conversation:")
            for msg in history[-6:]:  # Keep last 6 messages for context
                role = "User" if msg.get("role") == "user" else "Assistant"
                prompt_parts.append(f"{role}: {msg.get('content', '')}")
            prompt_parts.append("")
        
        prompt_parts.append(f"User: {query}")
        prompt_parts.append("Assistant:")
        
        return "\n".join(prompt_parts)
    
    async def generate(
        self,
        query: str,
        context: str = "",
        history: list = None,
        model: Optional[str] = None
    ) -> str:
        """
        Generate a response (non-streaming).
        
        Args:
            query: User's question
            context: Retrieved context from RAG
            history: Previous conversation history
            model: Override default model
            
        Returns:
            Generated response text
        """
        prompt = self._build_prompt(query, context, history)
        
        payload = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 1024,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                else:
                    logger.error(f"Ollama error: {response.status_code} - {response.text}")
                    return "I'm sorry, I encountered an error generating a response."
                    
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return "I'm sorry, the request timed out. Please try again."
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return "I'm sorry, I encountered an error. Please try again."
    
    async def generate_stream(
        self,
        query: str,
        context: str = "",
        history: list = None,
        model: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response.
        
        Args:
            query: User's question
            context: Retrieved context from RAG
            history: Previous conversation history
            model: Override default model
            
        Yields:
            Text chunks as they are generated
        """
        prompt = self._build_prompt(query, context, history)
        
        payload = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 1024,
            }
        }
        
        try:
            logger.info(f"Calling Ollama with model: {model or self.model}")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status_code != 200:
                        logger.error(f"Ollama error: status {response.status_code}")
                        yield "I'm sorry, I encountered an error generating a response."
                        return
                    
                    logger.info("Ollama stream started successfully")
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                chunk = data.get("response", "")
                                if chunk:
                                    yield chunk
                                if data.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.TimeoutException:
            logger.error("Ollama streaming request timed out")
            yield "I'm sorry, the request timed out."
        except Exception as e:
            import traceback
            logger.error(f"Ollama streaming error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            yield "I'm sorry, I encountered an error."


# Singleton instance
_ollama_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get or create the Ollama client singleton."""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client

