#!/bin/bash
# Quick diagnostic script for Watchtower issues

echo "=========================================="
echo "🔍 Watchtower Diagnostic Report"
echo "=========================================="
echo ""

echo "1️⃣  Checking if Watchtower is running..."
if docker ps | grep -q watchtower; then
    echo "   ✅ Watchtower is RUNNING"
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep watchtower
else
    echo "   ❌ Watchtower is NOT running"
    echo "   Fix: Run deployment/fix-watchtower.sh"
fi

echo ""
echo "2️⃣  Checking Docker GHCR authentication..."
if [ -f ~/.docker/config.json ]; then
    if grep -q "ghcr.io" ~/.docker/config.json; then
        echo "   ✅ Docker is logged into GHCR"
    else
        echo "   ❌ Docker is NOT logged into GHCR"
        echo "   Fix: echo 'TOKEN' | docker login ghcr.io -u USERNAME --password-stdin"
    fi
else
    echo "   ❌ Docker config file not found"
    echo "   Fix: docker login ghcr.io"
fi

echo ""
echo "3️⃣  Checking portfolio containers..."
CONTAINERS=$(docker ps --format "{{.Names}}" | grep -E "portfolio-frontend|portfolio-backend" || echo "")
if [ -z "$CONTAINERS" ]; then
    echo "   ❌ No portfolio containers found"
    echo "   Fix: cd ~/projects/local-smart-portfolio && docker compose up -d"
else
    echo "   ✅ Found containers:"
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep -E "portfolio|NAMES"
fi

echo ""
echo "4️⃣  Checking if containers use :latest tag..."
docker ps --format "{{.Names}}\t{{.Image}}" | grep portfolio | while read name image; do
    if [[ "$image" == *":latest"* ]]; then
        echo "   ✅ $name uses :latest tag"
    else
        echo "   ⚠️  $name does NOT use :latest tag: $image"
        echo "      Watchtower only monitors :latest by default"
    fi
done

echo ""
echo "5️⃣  Checking Watchtower logs (last 30 lines)..."
if docker ps | grep -q watchtower; then
    echo "   Recent activity:"
    docker logs watchtower --tail 30 2>&1 | tail -10
    echo ""
    echo "   Look for:"
    echo "   - 'Found new image' = ✅ Working"
    echo "   - 'No new images' = ⚠️  No updates available or auth issue"
    echo "   - 'unauthorized' = ❌ GHCR authentication problem"
else
    echo "   ⚠️  Cannot check logs (Watchtower not running)"
fi

echo ""
echo "6️⃣  Testing manual image pull..."
echo "   Testing frontend..."
if docker pull ghcr.io/medevs/portfolio-frontend:latest > /dev/null 2>&1; then
    echo "   ✅ Can pull frontend image (authentication OK)"
else
    echo "   ❌ Cannot pull frontend image (authentication FAILED)"
    echo "   Fix: docker login ghcr.io"
fi

echo ""
echo "=========================================="
echo "📋 Summary & Next Steps"
echo "=========================================="
echo ""
echo "If Watchtower is not working, most likely causes:"
echo "  1. Watchtower not running → Run: deployment/fix-watchtower.sh"
echo "  2. Not logged into GHCR → Run: docker login ghcr.io"
echo "  3. Containers not using :latest → Update docker-compose.homelab.yml"
echo "  4. Watchtower not monitoring containers → Specify container names"
echo ""
echo "For detailed fixes, see: deployment/WATCHTOWER_DEBUG.md"

