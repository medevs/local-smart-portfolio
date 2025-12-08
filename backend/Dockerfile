# =============================================================================
# Backend Dockerfile - FastAPI Application (Optimized - No ML dependencies)
# =============================================================================
# Multi-stage build for minimal production image
# Embeddings are now handled by Ollama, reducing image size significantly
# =============================================================================

FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --user \
    --prefer-binary \
    -r requirements.txt

# =============================================================================
# Production stage - Minimal image
# =============================================================================
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Set Python environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1

# Copy application code
COPY app/ ./app/

# Create directories for data persistence
RUN mkdir -p /app/data/chroma_db /app/data/documents /app/logs \
    && chmod -R 755 /app/data /app/logs

# Expose port
EXPOSE 8000

# Health check - reduced start period since no ML model loading
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
