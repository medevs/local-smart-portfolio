#!/bin/bash
# =============================================================================
# Automated Setup Script for AI Portfolio
# =============================================================================

set -e

echo "🚀 AI Portfolio - Automated Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."
echo ""

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo "   Please install Docker from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"
echo ""

# Step 2: Generate API key
echo "🔐 Step 2: Generating secure API key..."
echo ""

if command -v python3 &> /dev/null; then
    API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
elif command -v python &> /dev/null; then
    API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
else
    echo -e "${YELLOW}⚠️  Python not found. Please generate API key manually.${NC}"
    echo "   Run: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    read -p "Enter your API key: " API_KEY
fi

echo -e "${GREEN}✅ Generated API key: ${API_KEY:0:20}...${NC}"
echo ""

# Step 3: Create .env file
echo "📝 Step 3: Creating .env file..."
echo ""

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env from .env.example${NC}"
    else
        echo -e "${RED}❌ .env.example not found!${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    read -p "Do you want to overwrite it? (y/N): " OVERWRITE
    if [[ ! $OVERWRITE =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
        # Still update ADMIN_API_KEY if it's the default
        if grep -q "ADMIN_API_KEY=your-secure-api-key-here" .env; then
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s|ADMIN_API_KEY=your-secure-api-key-here.*|ADMIN_API_KEY=$API_KEY|" .env
            else
                # Linux
                sed -i "s|ADMIN_API_KEY=your-secure-api-key-here.*|ADMIN_API_KEY=$API_KEY|" .env
            fi
            echo -e "${GREEN}✅ Updated ADMIN_API_KEY in existing .env${NC}"
        fi
    else
        cp .env.example .env
        echo -e "${GREEN}✅ Overwritten .env file${NC}"
    fi
fi

# Update ADMIN_API_KEY in .env
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|ADMIN_API_KEY=.*|ADMIN_API_KEY=$API_KEY|" .env
else
    # Linux
    sed -i "s|ADMIN_API_KEY=.*|ADMIN_API_KEY=$API_KEY|" .env
fi

echo -e "${GREEN}✅ Updated ADMIN_API_KEY in .env${NC}"
echo ""

# Step 4: Build Docker images
echo "🔨 Step 4: Building Docker images..."
echo "   This may take 5-10 minutes..."
echo ""

docker compose build

echo ""
echo -e "${GREEN}✅ Docker images built successfully${NC}"
echo ""

# Step 5: Start services
echo "🚀 Step 5: Starting services..."
echo ""

docker compose up -d

echo ""
echo -e "${GREEN}✅ Services started${NC}"
echo ""

# Step 6: Wait for services to be ready
echo "⏳ Step 6: Waiting for services to be ready..."
echo ""

sleep 10

# Check service status
echo "📊 Service Status:"
docker compose ps

echo ""

# Step 7: Initialize Ollama
echo "📥 Step 7: Initializing Ollama model..."
echo "   This will download ~2GB model (5-15 minutes)"
echo ""

read -p "Do you want to download the model now? (Y/n): " DOWNLOAD_MODEL
if [[ ! $DOWNLOAD_MODEL =~ ^[Nn]$ ]]; then
    echo "Downloading llama3.2:3b model..."
    docker compose exec -T ollama ollama pull llama3.2:3b || {
        echo -e "${YELLOW}⚠️  Model download failed. You can run it manually later:${NC}"
        echo "   docker compose exec ollama ollama pull llama3.2:3b"
    }
else
    echo -e "${YELLOW}⚠️  Skipping model download. Run this later:${NC}"
    echo "   docker compose exec ollama ollama pull llama3.2:3b"
fi

echo ""

# Final summary
echo "=================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "🌐 Access your application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Admin:     http://localhost:3000/admin"
echo "   Health:    http://localhost:8000/health"
echo ""
echo "🔑 Your Admin API Key:"
echo "   $API_KEY"
echo "   (Also saved in .env file)"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    docker compose logs -f"
echo "   Stop:         docker compose down"
echo "   Restart:      docker compose restart"
echo "   Status:       docker compose ps"
echo ""
echo -e "${YELLOW}⚠️  Remember: Keep your API key secret!${NC}"
echo ""

