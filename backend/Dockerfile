# =============================================================================
# Backend Dockerfile - FastAPI Application (Two-Image Strategy)
# =============================================================================
# Supports two build modes:
# 1. Full build: FROM python:3.11-slim-bookworm (CI base + local dev)
# 2. Extension build: FROM ghcr.io/.../backend:base (homelab with Docling)
#
# CI builds base image (no Docling) -> pushes to GHCR
# Homelab builds FROM base + adds Docling layer
# =============================================================================

# Base image ARG - allows building FROM a pre-built base image
ARG BASE_IMAGE=python:3.11-slim-bookworm

FROM python:3.11-slim-bookworm AS builder

# Build arg to control Docling installation (default: true for local builds)
# Set USE_DOCLING=false in CI to save disk space
ARG USE_DOCLING=true

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# =============================================================================
# Layer 1: Core dependencies
# No cache mounts - prevents disk space issues on CI runners
# =============================================================================
RUN pip install --user --no-cache-dir --prefer-binary \
    fastapi==0.115.0 \
    uvicorn[standard]==0.32.0 \
    sqlalchemy>=2.0.0 \
    asyncpg>=0.29.0 \
    alembic>=1.13.0 \
    chromadb>=0.5.0 \
    httpx>=0.27.0 \
    pydantic>=2.9.0 \
    pydantic-settings>=2.5.0 \
    loguru>=0.7.0 \
    python-multipart==0.0.12 \
    python-dotenv==1.0.1 \
    celery>=5.3.0 \
    redis>=5.0.0 \
    langchain>=0.3.0 \
    langchain-community>=0.3.0 \
    langchain-text-splitters>=0.3.0 \
    rank-bm25>=0.2.2 \
    pypdf>=5.0.0 \
    python-docx>=1.1.0 \
    markdown>=3.6 \
    aiofiles>=24.0.0 \
    psutil>=5.9.0 \
    slowapi>=0.1.9 \
    langfuse>=2.0.0 \
    psycopg2-binary>=2.9.9

# =============================================================================
# Layer 2: Docling dependencies (optional, ~8-10 min, ~2GB disk)
# Only installed if USE_DOCLING=true
# No cache - HuggingFace models downloaded at runtime, not build time
# =============================================================================
RUN if [ "$USE_DOCLING" = "true" ]; then \
        pip install --user --no-cache-dir --prefer-binary \
        transformers>=4.47.0 \
        docling>=2.14.0 \
        docling-core>=2.4.0 && \
        pip install --user --no-cache-dir --force-reinstall "huggingface-hub>=0.24.0,<1.0" && \
        pip uninstall -y opencv-python 2>/dev/null || true && \
        pip install --user --no-cache-dir opencv-python-headless; \
    else \
        echo "Skipping Docling install (USE_DOCLING=$USE_DOCLING)"; \
    fi

# =============================================================================
# Production stage - uses BASE_IMAGE (python:slim for CI, or ghcr backend:base for homelab)
# =============================================================================
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Re-declare build args for production stage
ARG USE_DOCLING=true

WORKDIR /app

# Install runtime dependencies
# - Skip if building FROM base image (already has curl installed)
# - Add tesseract only if Docling enabled
RUN if [ ! -f /app/.base-marker ]; then \
        apt-get update && apt-get install -y --no-install-recommends curl && \
        rm -rf /var/lib/apt/lists/*; \
    fi && \
    if [ "$USE_DOCLING" = "true" ]; then \
        apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-eng && \
        rm -rf /var/lib/apt/lists/*; \
    fi

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/data/huggingface \
    TRANSFORMERS_CACHE=/app/data/huggingface

# Copy application code
COPY app/ ./app/

# Copy Alembic for database migrations
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Create directories for data persistence
RUN mkdir -p /app/data/chroma_db /app/data/documents /app/logs /app/data/huggingface \
    && chmod -R 755 /app/data /app/logs

# Mark as base image (used to detect if we're extending from base)
RUN touch /app/.base-marker

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
