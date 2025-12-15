# =============================================================================
# Backend Dockerfile - FastAPI Application (Two-Image Strategy)
# =============================================================================
# Build modes:
# 1. CI (base):     USE_DOCLING=false -> backend:base with core deps
# 2. Homelab:       FROM backend:base + USE_DOCLING=true -> installs Docling
# 3. Local dev:     USE_DOCLING=true -> full build with everything
# =============================================================================

ARG BASE_IMAGE=python:3.11-slim-bookworm

# =============================================================================
# Builder stage - compiles Python packages (only for fresh builds)
# =============================================================================
FROM python:3.11-slim-bookworm AS builder

ARG USE_DOCLING=true

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Core dependencies
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

# Docling deps (only if USE_DOCLING=true)
RUN if [ "$USE_DOCLING" = "true" ]; then \
        pip install --user --no-cache-dir --prefer-binary \
        transformers>=4.47.0 \
        docling>=2.14.0 \
        docling-core>=2.4.0 && \
        pip install --user --no-cache-dir --force-reinstall "huggingface-hub>=0.24.0,<1.0" && \
        pip uninstall -y opencv-python 2>/dev/null || true && \
        pip install --user --no-cache-dir opencv-python-headless; \
    fi

# =============================================================================
# Production stage
# =============================================================================
ARG BASE_IMAGE
FROM ${BASE_IMAGE} AS production

ARG USE_DOCLING=true

WORKDIR /app

# Runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Tesseract for Docling OCR
RUN if [ "$USE_DOCLING" = "true" ]; then \
        apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr tesseract-ocr-eng \
        && rm -rf /var/lib/apt/lists/*; \
    fi

# Copy packages from builder (for fresh builds from python:3.11-slim)
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# If extending from base image AND Docling requested, install Docling deps
# The base image already has core deps in /root/.local, we just add Docling
RUN if [ "$USE_DOCLING" = "true" ]; then \
        echo "Installing Docling packages..." && \
        pip install --no-cache-dir --prefer-binary \
        transformers>=4.47.0 \
        docling>=2.14.0 \
        docling-core>=2.4.0 && \
        pip install --no-cache-dir --force-reinstall "huggingface-hub>=0.24.0,<1.0" && \
        pip uninstall -y opencv-python 2>/dev/null || true && \
        pip install --no-cache-dir opencv-python-headless && \
        echo "Docling installed successfully"; \
    fi

# Clean up build tools to reduce image size
RUN apt-get purge -y build-essential gcc g++ \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/data/huggingface \
    TRANSFORMERS_CACHE=/app/data/huggingface

COPY app/ ./app/
COPY alembic.ini ./
COPY alembic/ ./alembic/

RUN mkdir -p /app/data/chroma_db /app/data/documents /app/logs /app/data/huggingface \
    && chmod -R 755 /app/data /app/logs

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
