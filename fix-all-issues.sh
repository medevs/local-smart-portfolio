#!/bin/bash
# =============================================================================
# Complete Fix Script - Resolves git conflict and Watchtower issues
# =============================================================================

set -e

echo "🔧 Fixing all issues..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Step 1: Resolve git conflict
echo -e "${YELLOW}📋 Step 1: Resolving git conflict...${NC}"
if [ -f "docker-compose.homelab.yml" ]; then
    echo "Backing up local docker-compose.homelab.yml..."
    mv docker-compose.homelab.yml docker-compose.homelab.yml.backup
    echo -e "${GREEN}✅ Backed up local file${NC}"
fi

# Pull latest code
echo -e "${YELLOW}📥 Pulling latest code...${NC}"
git pull origin main

if [ -f "docker-compose.homelab.yml.backup" ]; then
    echo -e "${YELLOW}⚠️  You had a local docker-compose.homelab.yml file${NC}"
    echo "It's been backed up as docker-compose.homelab.yml.backup"
    echo "If you had custom changes, you can merge them manually."
fi

# Step 2: Check Docker version
echo -e "${YELLOW}📋 Step 2: Checking Docker version...${NC}"
DOCKER_VERSION=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "unknown")
echo "Docker daemon version: $DOCKER_VERSION"

# Step 3: Fix Watchtower
echo -e "${YELLOW}📋 Step 3: Fixing Watchtower...${NC}"

# Stop and remove old Watchtower
if docker ps -a | grep -q watchtower; then
    echo "Stopping old Watchtower..."
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

# Start Watchtower with latest image (which should support newer Docker API)
echo -e "${YELLOW}🚀 Starting Watchtower with latest image...${NC}"
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower:latest \
  --interval 30 \
  --cleanup \
  portfolio-frontend \
  portfolio-backend

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Watchtower started successfully!${NC}"
    echo ""
    echo "📊 Watchtower Status:"
    sleep 2
    docker ps | grep watchtower || echo "Watchtower container not found in ps output"
    echo ""
    echo "📝 Recent logs:"
    docker logs watchtower --tail 10 2>&1 || echo "Could not read logs yet"
    echo ""
    echo -e "${GREEN}✨ Setup complete!${NC}"
else
    echo -e "${RED}❌ Failed to start Watchtower${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check Docker version: docker version"
    echo "2. Try updating Docker: sudo apt update && sudo apt upgrade docker.io"
    echo "3. Check Watchtower logs: docker logs watchtower"
    exit 1
fi

