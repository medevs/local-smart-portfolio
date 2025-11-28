#!/bin/bash
# =============================================================================
# Docker Quick Start Script
# =============================================================================

set -e

echo "🐳 AI Portfolio - Docker Quick Start"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "🔐 IMPORTANT: Edit .env and set ADMIN_API_KEY!"
    echo "   Generate a secure key:"
    echo "   python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    echo ""
    read -p "Press Enter after setting ADMIN_API_KEY in .env..."
fi

# Check if ADMIN_API_KEY is set
if grep -q "ADMIN_API_KEY=your-secure-api-key-here" .env || grep -q "ADMIN_API_KEY=$" .env; then
    echo "❌ ERROR: ADMIN_API_KEY is not set in .env!"
    echo "   Please set a secure API key before continuing."
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Build and start services
echo "🔨 Building Docker images..."
docker compose build

echo ""
echo "🚀 Starting services..."
docker compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo ""
echo "📊 Service Status:"
docker compose ps

echo ""
echo "📝 Initializing Ollama model (this may take a few minutes)..."
echo "   Model: llama3.2:3b"
docker compose exec -T ollama ollama pull llama3.2:3b || echo "⚠️  Ollama pull failed, you may need to pull manually"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Health:    http://localhost:8000/health"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    docker compose logs -f"
echo "   Stop:         docker compose down"
echo "   Restart:      docker compose restart"
echo ""

