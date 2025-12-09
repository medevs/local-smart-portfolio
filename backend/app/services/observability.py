"""
Observability service using Langfuse for LLM tracing and monitoring.
Provides visibility into LLM calls, latencies, token usage, and errors.
"""

import os
import time
from typing import Optional, Dict, Any, Generator, AsyncGenerator
from functools import wraps
from contextlib import contextmanager
from datetime import datetime

from app.utils.logger import logger
from app.config import get_settings

# Try to import Langfuse, but make it optional
try:
    from langfuse import Langfuse
    from langfuse.decorators import observe, langfuse_context
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    logger.warning("Langfuse not installed. Observability features disabled.")


class ObservabilityService:
    """
    Service for LLM observability and tracing.
    Uses Langfuse when available, falls back to local logging otherwise.
    """

    _instance: Optional["ObservabilityService"] = None

    def __init__(self):
        self.enabled = False
        self.langfuse: Optional[Any] = None
        self._initialize()

    def _initialize(self):
        """Initialize Langfuse client if configured."""
        settings = get_settings()

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

    def log_generation(
        self,
        trace_id: Optional[str],
        name: str,
        input_text: str,
        output_text: str,
        model: str,
        latency_ms: float,
        tokens_input: Optional[int] = None,
        tokens_output: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Log a completed LLM generation."""
        if self.enabled and self.langfuse:
            try:
                generation = self.langfuse.generation(
                    trace_id=trace_id,
                    name=name,
                    model=model,
                    input=input_text,
                    output=output_text,
                    usage={
                        "input": tokens_input,
                        "output": tokens_output,
                    } if tokens_input or tokens_output else None,
                    metadata=metadata,
                )
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to log generation to Langfuse: {e}")

        # Always log locally for debugging
        logger.debug(
            f"LLM Generation: {name} | Model: {model} | "
            f"Latency: {latency_ms:.0f}ms | "
            f"Tokens: {tokens_input or '?'}/{tokens_output or '?'}"
        )

    def log_retrieval(
        self,
        trace_id: Optional[str],
        query: str,
        documents: list,
        latency_ms: float,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Log a RAG retrieval operation."""
        if self.enabled and self.langfuse:
            try:
                self.langfuse.span(
                    trace_id=trace_id,
                    name="retrieval",
                    input={"query": query},
                    output={"documents": documents, "count": len(documents)},
                    metadata=metadata,
                )
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to log retrieval to Langfuse: {e}")

        logger.debug(
            f"RAG Retrieval: {len(documents)} docs | Latency: {latency_ms:.0f}ms"
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

        if self.enabled and self.langfuse:
            try:
                self.langfuse.event(
                    trace_id=trace_id,
                    name="error",
                    metadata=error_info,
                )
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to log error to Langfuse: {e}")

        logger.error(f"LLM Error: {error_info}")

    def log_user_feedback(
        self,
        trace_id: str,
        score: float,
        comment: Optional[str] = None,
    ):
        """Log user feedback for a response."""
        if self.enabled and self.langfuse:
            try:
                self.langfuse.score(
                    trace_id=trace_id,
                    name="user_feedback",
                    value=score,
                    comment=comment,
                )
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to log feedback to Langfuse: {e}")

        logger.info(f"User Feedback: trace={trace_id}, score={score}")

    def flush(self):
        """Flush any pending events to Langfuse."""
        if self.enabled and self.langfuse:
            try:
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to flush Langfuse: {e}")


class TraceContext:
    """Context manager for tracing LLM operations."""

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

    def __enter__(self) -> "TraceContext":
        self.start_time = time.time()

        if self.service.enabled and self.service.langfuse:
            try:
                trace = self.service.langfuse.trace(
                    name=self.name,
                    input=self.input_text,
                    metadata={
                        "model": self.model,
                        **self.metadata,
                    },
                )
                self.trace_id = trace.id
            except Exception as e:
                logger.warning(f"Failed to create trace: {e}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        latency_ms = (time.time() - self.start_time) * 1000

        if exc_type is not None:
            self.service.log_error(
                trace_id=self.trace_id,
                error=exc_val,
                context={"name": self.name, "model": self.model},
            )
        else:
            self.service.log_generation(
                trace_id=self.trace_id,
                name=self.name,
                input_text=self.input_text,
                output_text=self.output_text,
                model=self.model,
                latency_ms=latency_ms,
                tokens_input=self.tokens_input,
                tokens_output=self.tokens_output,
                metadata=self.metadata,
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


# Decorator for tracing functions
def trace_llm(name: str, model: Optional[str] = None):
    """
    Decorator to trace LLM operations.

    Usage:
        @trace_llm("chat_completion")
        async def generate_response(query: str) -> str:
            ...
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            obs = get_observability_service()
            settings = get_settings()

            # Extract input from args/kwargs
            input_text = str(kwargs.get("query") or kwargs.get("question") or args[0] if args else "")
            model_name = model or settings.ollama_model

            with obs.trace_llm_call(
                name=name,
                input_text=input_text,
                model=model_name,
            ) as ctx:
                result = await func(*args, **kwargs)
                if isinstance(result, str):
                    ctx.set_output(result)
                elif isinstance(result, dict):
                    ctx.set_output(str(result.get("response", result)))
                return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            obs = get_observability_service()
            settings = get_settings()

            input_text = str(kwargs.get("query") or kwargs.get("question") or args[0] if args else "")
            model_name = model or settings.ollama_model

            with obs.trace_llm_call(
                name=name,
                input_text=input_text,
                model=model_name,
            ) as ctx:
                result = func(*args, **kwargs)
                if isinstance(result, str):
                    ctx.set_output(result)
                elif isinstance(result, dict):
                    ctx.set_output(str(result.get("response", result)))
                return result

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
