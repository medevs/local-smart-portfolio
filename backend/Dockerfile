# =============================================================================
# Backend Dockerfile - FastAPI Application
# =============================================================================
# Two-stage build with Docling support (optional via USE_DOCLING env var)
# First build takes ~10-15 minutes, subsequent builds use cache (~2-3 min)
# =============================================================================

FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies (including those needed for Docling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# =============================================================================
# Layer 1: Core dependencies (fast, ~2 min)
# =============================================================================
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --prefer-binary \
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
# Layer 2: Docling dependencies (slow, ~8-10 min, cached after first build)
# =============================================================================
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/huggingface \
    pip install --user --prefer-binary \
    transformers>=4.47.0 \
    docling>=2.14.0 \
    docling-core>=2.4.0

# =============================================================================
# Production stage
# =============================================================================
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install runtime dependencies (Tesseract for Docling OCR, curl for health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

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

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
