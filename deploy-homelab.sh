#!/bin/bash
# =============================================================================
# Homelab Deployment Script
# =============================================================================
# This script updates the portfolio containers using GHCR images
# Run this on your homelab server after pushing changes to GitHub
# =============================================================================

set -e  # Exit on error

echo "🚀 Starting Homelab Deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml not found${NC}"
    echo "Please run this script from your project root directory"
    exit 1
fi

# Check if homelab override exists
if [ ! -f "docker-compose.homelab.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.homelab.yml not found${NC}"
    echo "Please ensure the homelab override file exists"
    exit 1
fi

# Check GHCR authentication
echo -e "${YELLOW}📋 Checking GHCR authentication...${NC}"
if ! docker info | grep -q "ghcr.io"; then
    echo -e "${YELLOW}⚠️  Warning: GHCR authentication may not be set up${NC}"
    echo "If you get authentication errors, run:"
    echo "  echo 'YOUR_TOKEN' | docker login ghcr.io -u medevs --password-stdin"
fi

# Pull latest code (optional, uncomment if needed)
# echo -e "${YELLOW}📥 Pulling latest code from Git...${NC}"
# git pull origin main || echo "⚠️  Git pull failed, continuing anyway..."

# Pull latest images from GHCR
echo -e "${YELLOW}📦 Pulling latest images from GHCR...${NC}"
docker compose -f docker-compose.yml -f docker-compose.homelab.yml pull

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to pull images. Check GHCR authentication.${NC}"
    exit 1
fi

# Stop existing containers
echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker compose -f docker-compose.yml -f docker-compose.homelab.yml down

# Start containers with new images
echo -e "${YELLOW}🚀 Starting containers with new images...${NC}"
docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start containers${NC}"
    exit 1
fi

# Wait a moment for containers to start
sleep 5

# Show container status
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📊 Container Status:"
docker compose -f docker-compose.yml -f docker-compose.homelab.yml ps

echo ""
echo "📝 Recent logs (last 20 lines):"
docker compose -f docker-compose.yml -f docker-compose.homelab.yml logs --tail=20

echo ""
echo -e "${GREEN}✨ Your portfolio should now be updated!${NC}"
echo "Access it at: https://portfolio.medevs.local"

