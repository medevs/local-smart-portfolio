"""
Observability service using Langfuse for LLM tracing and monitoring.
Provides visibility into LLM calls, latencies, token usage, and errors.

Updated for Langfuse SDK v3 API.
"""

import os
import time
from typing import Optional, Dict, Any
from functools import wraps
from datetime import datetime

from app.utils.logger import logger
from app.config import get_settings

# Try to import Langfuse, but make it optional
try:
    from langfuse import Langfuse, observe, get_client
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    observe = None
    get_client = None
    logger.warning("Langfuse not installed. Observability features disabled.")


class ObservabilityService:
    """
    Service for LLM observability and tracing using Langfuse SDK v3.
    Uses Langfuse when available, falls back to local logging otherwise.
    """

    _instance: Optional["ObservabilityService"] = None

    def __init__(self):
        self.enabled = False
        self.langfuse: Optional[Any] = None
        self._initialize()

    def _initialize(self):
        """Initialize Langfuse client if configured."""
        # Check for Langfuse environment variables
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        host = os.getenv("LANGFUSE_HOST", "http://localhost:3001")

        if LANGFUSE_AVAILABLE and public_key and secret_key:
            try:
                self.langfuse = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=host,
                )
                self.enabled = True
                logger.info(f"Langfuse observability enabled (host: {host})")
            except Exception as e:
                logger.warning(f"Failed to initialize Langfuse: {e}")
                self.enabled = False
        else:
            if not LANGFUSE_AVAILABLE:
                logger.info("Langfuse not installed - using local logging")
            else:
                logger.info("Langfuse not configured - using local logging")

    @classmethod
    def get_instance(cls) -> "ObservabilityService":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def trace_llm_call(
        self,
        name: str,
        input_text: str,
        model: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "TraceContext":
        """
        Create a trace context for an LLM call.

        Args:
            name: Name of the operation (e.g., "chat", "rag_query")
            input_text: Input prompt/query
            model: Model name being used
            metadata: Additional metadata

        Returns:
            TraceContext for managing the trace
        """
        return TraceContext(
            service=self,
            name=name,
            input_text=input_text,
            model=model,
            metadata=metadata or {},
        )

    def log_error(
        self,
        trace_id: Optional[str],
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Log an error event."""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        logger.error(f"LLM Error: {error_info}")

    def flush(self):
        """Flush any pending events to Langfuse."""
        if self.enabled and self.langfuse:
            try:
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to flush Langfuse: {e}")


class TraceContext:
    """Context manager for tracing LLM operations using Langfuse SDK v3."""

    def __init__(
        self,
        service: ObservabilityService,
        name: str,
        input_text: str,
        model: str,
        metadata: Dict[str, Any],
    ):
        self.service = service
        self.name = name
        self.input_text = input_text
        self.model = model
        self.metadata = metadata
        self.trace_id: Optional[str] = None
        self.start_time: float = 0
        self.output_text: str = ""
        self.tokens_input: Optional[int] = None
        self.tokens_output: Optional[int] = None
        self._span = None

    def __enter__(self) -> "TraceContext":
        self.start_time = time.time()

        if self.service.enabled and self.service.langfuse:
            try:
                # Use the new SDK v3 context manager API
                self._span = self.service.langfuse.start_as_current_span(
                    name=self.name,
                    input={"message": self.input_text},
                    metadata={
                        "model": self.model,
                        **self.metadata,
                    },
                )
                self._span.__enter__()
                self.trace_id = getattr(self._span, 'trace_id', None)
            except Exception as e:
                logger.warning(f"Failed to create trace: {e}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        latency_ms = (time.time() - self.start_time) * 1000

        if self._span:
            try:
                if exc_type is not None:
                    # Log error
                    self._span.update(
                        level="ERROR",
                        status_message=str(exc_val),
                        metadata={"error_type": type(exc_val).__name__}
                    )
                else:
                    # Log success with output
                    self._span.update(
                        output={"response": self.output_text},
                        metadata={
                            "latency_ms": latency_ms,
                            "tokens_input": self.tokens_input,
                            "tokens_output": self.tokens_output,
                        }
                    )

                self._span.__exit__(exc_type, exc_val, exc_tb)

                # Flush to ensure data is sent
                self.service.flush()
            except Exception as e:
                logger.warning(f"Failed to complete trace: {e}")

        # Always log locally for debugging
        logger.debug(
            f"LLM Call: {self.name} | Model: {self.model} | "
            f"Latency: {latency_ms:.0f}ms"
        )

        return False  # Don't suppress exceptions

    def set_output(self, output: str):
        """Set the output text for logging."""
        self.output_text = output

    def set_tokens(self, input_tokens: int, output_tokens: int):
        """Set token counts for logging."""
        self.tokens_input = input_tokens
        self.tokens_output = output_tokens


# Singleton accessor
def get_observability_service() -> ObservabilityService:
    """Get the observability service singleton."""
    return ObservabilityService.get_instance()
