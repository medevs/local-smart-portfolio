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
        self.timeout = httpx.Timeout(180.0, connect=30.0)
        
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
    
    def _build_messages(self, query: str, context: str, history: list = None) -> list:
        """Build chat messages for Ollama chat API with optimized prompts."""
        
        # Extract key info from context (first 600 chars max)
        context_brief = ""
        if context:
            clean_context = context.replace("[Source:", "").replace("]", "")
            context_brief = clean_context[:600].strip()
        
        # Ultra-concise system prompt
        system_content = f"""You are Ahmed's portfolio assistant. Use this info:
{context_brief}

RULES: Answer in 1-2 SHORT sentences. Be direct. No lists."""
        
        messages = [{"role": "system", "content": system_content}]
        
        if history:
            for msg in history[-2:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        messages.append({"role": "user", "content": query})
        return messages
    
    def _build_prompt(self, query: str, context: str, history: list = None) -> str:
        """Legacy prompt builder - kept for compatibility."""
        system = "You are Ahmed's portfolio assistant. Answer in 1-2 sentences max. Be direct."
        
        prompt = f"{system}\n\n"
        if context:
            prompt += f"Info: {context[:1500]}\n\n"
        prompt += f"Q: {query}\nA:"
        
        return prompt
    
    async def generate(
        self,
        query: str,
        context: str = "",
        history: list = None,
        model: Optional[str] = None
    ) -> str:
        """
        Generate a response using Ollama chat API (non-streaming).
        """
        messages = self._build_messages(query, context, history)
        
        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 60,
                "repeat_penalty": 1.2,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("message", {}).get("content", "")
                else:
                    logger.error(f"Ollama error: {response.status_code}")
                    return "Sorry, I encountered an error."
                    
        except httpx.TimeoutException:
            return "Request timed out. Please try again."
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "Sorry, something went wrong."
    
    async def generate_stream(
        self,
        query: str,
        context: str = "",
        history: list = None,
        model: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response using Ollama chat API.
        """
        messages = self._build_messages(query, context, history)
        
        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.3,
                "num_predict": 60,  # ~40-50 words max
                "repeat_penalty": 1.2,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload
                ) as response:
                    if response.status_code != 200:
                        yield "Sorry, I encountered an error."
                        return
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                chunk = data.get("message", {}).get("content", "")
                                if chunk:
                                    yield chunk
                                if data.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.TimeoutException:
            yield "Request timed out."
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            yield "Sorry, something went wrong."


# Singleton instance
_ollama_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get or create the Ollama client singleton."""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client

