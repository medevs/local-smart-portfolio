"""
Embedding service using Ollama API.
Generates vector embeddings for text chunks via Ollama's /api/embed endpoint.
"""

from typing import List, Optional
import httpx
from app.config import get_settings
from app.utils.logger import logger


class EmbeddingService:
    """Service for generating text embeddings via Ollama."""

    # Recommended Ollama embedding models
    MODELS = {
        "nomic": "nomic-embed-text",           # 274MB, 768 dims, good balance
        "mxbai": "mxbai-embed-large",          # 670MB, 1024 dims, high quality
        "snowflake": "snowflake-arctic-embed", # 670MB, 1024 dims
        "all-minilm": "all-minilm",            # 46MB, 384 dims, lightweight
    }

    def __init__(self, model_name: Optional[str] = None):
        settings = get_settings()
        self.base_url = settings.ollama_base_url
        self.model_name = model_name or settings.embedding_model
        self._dimension: Optional[int] = None
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.Client:
        """Lazy load the sync HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                timeout=httpx.Timeout(60.0, connect=10.0),
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )
        return self._client

    def _get_async_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                timeout=httpx.Timeout(60.0, connect=10.0),
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )
        return self._async_client

    def _embed_via_ollama(self, texts: List[str]) -> List[List[float]]:
        """
        Call Ollama's embedding API (sync).

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.post(
                f"{self.base_url}/api/embed",
                json={
                    "model": self.model_name,
                    "input": texts
                }
            )
            response.raise_for_status()
            data = response.json()

            # Ollama returns {"embeddings": [[...], [...]]}
            embeddings = data.get("embeddings", [])

            # Cache dimension from first successful call
            if embeddings and self._dimension is None:
                self._dimension = len(embeddings[0])
                logger.info(f"Ollama embedding model: {self.model_name}, dimension: {self._dimension}")

            return embeddings

        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to Ollama at {self.base_url}: {e}")
            raise ConnectionError(f"Ollama not reachable at {self.base_url}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling Ollama embeddings: {e}")
            raise

    async def _aembed_via_ollama(self, texts: List[str]) -> List[List[float]]:
        """
        Call Ollama's embedding API (async).

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        client = self._get_async_client()
        try:
            response = await client.post(
                f"{self.base_url}/api/embed",
                json={
                    "model": self.model_name,
                    "input": texts
                }
            )
            response.raise_for_status()
            data = response.json()

            embeddings = data.get("embeddings", [])

            if embeddings and self._dimension is None:
                self._dimension = len(embeddings[0])
                logger.info(f"Ollama embedding model: {self.model_name}, dimension: {self._dimension}")

            return embeddings

        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to Ollama at {self.base_url}: {e}")
            raise ConnectionError(f"Ollama not reachable at {self.base_url}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling Ollama embeddings: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return []

        try:
            embeddings = self._embed_via_ollama([text])
            return embeddings[0] if embeddings else []
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batched).

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings
        """
        if not texts:
            return []

        # Filter out empty texts but track original indices
        valid_texts = [t for t in texts if t and t.strip()]

        if not valid_texts:
            logger.warning("No valid texts provided for embedding")
            return []

        try:
            logger.debug(f"Generating embeddings for {len(valid_texts)} texts via Ollama")
            return self._embed_via_ollama(valid_texts)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        if self._dimension is None:
            # Generate a test embedding to determine dimension
            try:
                test_embedding = self.embed_text("test")
                self._dimension = len(test_embedding) if test_embedding else 768
            except Exception:
                # Default fallback for nomic-embed-text
                self._dimension = 768
        return self._dimension

    async def aembed_text(self, text: str) -> List[float]:
        """Async version of embed_text."""
        if not text or not text.strip():
            return []

        try:
            embeddings = await self._aembed_via_ollama([text])
            return embeddings[0] if embeddings else []
        except Exception as e:
            logger.error(f"Async embedding error: {e}")
            return []

    async def aembed_texts(self, texts: List[str]) -> List[List[float]]:
        """Async version of embed_texts."""
        valid_texts = [t for t in texts if t and t.strip()]
        if not valid_texts:
            return []

        try:
            return await self._aembed_via_ollama(valid_texts)
        except Exception as e:
            logger.error(f"Async embeddings error: {e}")
            return []

    def check_model_available(self) -> bool:
        """Check if the embedding model is available in Ollama."""
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            model_names = [m.get("name", "").split(":")[0] for m in models]
            return self.model_name.split(":")[0] in model_names
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False

    def __del__(self):
        """Cleanup HTTP clients on destruction."""
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create the embedding service singleton."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
