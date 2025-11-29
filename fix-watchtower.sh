#!/bin/bash
# =============================================================================
# Watchtower Fix Script - Safe to run on homelab server
# =============================================================================
# This script safely restarts Watchtower to monitor portfolio containers
# =============================================================================

set -e  # Exit on error

echo "🔧 Fixing Watchtower configuration..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Watchtower container exists
if docker ps -a | grep -q watchtower; then
    echo -e "${YELLOW}📋 Checking Watchtower logs...${NC}"
    docker logs watchtower --tail 20 || true
    
    echo -e "${YELLOW}🛑 Stopping and removing old Watchtower container...${NC}"
    docker stop watchtower 2>/dev/null || true
    docker rm watchtower 2>/dev/null || true
fi

# Verify portfolio containers exist
if ! docker ps | grep -q portfolio-frontend; then
    echo -e "${RED}❌ Error: portfolio-frontend container not found${NC}"
    echo "Please start your portfolio containers first:"
    echo "  docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d"
    exit 1
fi

if ! docker ps | grep -q portfolio-backend; then
    echo -e "${RED}❌ Error: portfolio-backend container not found${NC}"
    echo "Please start your portfolio containers first:"
    echo "  docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d"
    exit 1
fi

# Start Watchtower with correct configuration
echo -e "${YELLOW}🚀 Starting Watchtower with correct configuration...${NC}"
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 30 \
  --cleanup \
  portfolio-frontend \
  portfolio-backend

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Watchtower started successfully!${NC}"
    echo ""
    echo "📊 Watchtower Status:"
    docker ps | grep watchtower
    echo ""
    echo "📝 Recent logs:"
    sleep 2
    docker logs watchtower --tail 10
    echo ""
    echo -e "${GREEN}✨ Watchtower is now monitoring:${NC}"
    echo "  - portfolio-frontend"
    echo "  - portfolio-backend"
    echo ""
    echo "Watchtower will check for updates every 30 seconds."
else
    echo -e "${RED}❌ Failed to start Watchtower${NC}"
    exit 1
fi

