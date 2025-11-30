#!/bin/bash
# Fix Watchtower Setup for Automatic CI/CD Updates
# Based on your Day 11 homelab setup

set -e

echo "🔍 Checking Watchtower status..."
if docker ps | grep -q watchtower; then
    echo "✅ Watchtower is running"
    docker ps | grep watchtower
else
    echo "❌ Watchtower is NOT running"
fi

echo ""
echo "📋 Checking Docker GHCR authentication..."
if [ -f ~/.docker/config.json ] && grep -q "ghcr.io" ~/.docker/config.json; then
    echo "✅ Docker is logged into GHCR"
else
    echo "⚠️  WARNING: Docker is NOT logged into GHCR"
    echo "   Watchtower needs this to pull private images"
    echo "   Run: echo 'YOUR_TOKEN' | docker login ghcr.io -u YOUR_USERNAME --password-stdin"
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "📊 Checking portfolio containers..."
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep -E "portfolio|NAMES" || echo "No portfolio containers found"

echo ""
echo "🛑 Stopping and removing old Watchtower..."
docker stop watchtower 2>/dev/null || true
docker rm watchtower 2>/dev/null || true

echo ""
echo "🚀 Creating new Watchtower with proper configuration..."
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.docker/config.json:/config.json:ro \
  containrrr/watchtower:latest \
  --interval 30 \
  --cleanup \
  portfolio-frontend portfolio-backend

echo ""
echo "⏳ Waiting for Watchtower to start..."
sleep 3

echo ""
echo "📋 Watchtower status:"
docker ps | grep watchtower || echo "❌ Watchtower failed to start"

echo ""
echo "📜 Recent Watchtower logs:"
docker logs watchtower --tail 20

echo ""
echo "✅ Watchtower setup complete!"
echo ""
echo "📝 What happens next:"
echo "   1. Watchtower checks for new images every 30 seconds"
echo "   2. When GitHub Actions pushes new images to GHCR"
echo "   3. Watchtower will detect them and restart containers"
echo ""
echo "🔍 To monitor Watchtower:"
echo "   docker logs -f watchtower"
echo ""
echo "🧪 To test immediately:"
echo "   docker exec watchtower watchtower --run-once portfolio-frontend portfolio-backend"

