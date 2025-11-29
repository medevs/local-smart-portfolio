# 🏠 Homelab Deployment Guide - CI/CD Fix

## 🔍 Problem Identified

Your GitHub Actions workflow is successfully building and pushing images to GHCR, but your homelab server is still building images locally instead of pulling from GHCR. This means:

- ❌ Watchtower cannot detect new images (it only monitors registry images)
- ❌ Changes pushed to GitHub won't appear on your server
- ❌ You're not using the CI/CD pipeline you set up

## ✅ Solution

You need to update your homelab server to use the `docker-compose.homelab.yml` override file that pulls images from GHCR instead of building locally.

---

## 📋 Step-by-Step Fix

### Step 1: SSH into Your Homelab Server

```bash
ssh -p 2222 -i ~/.ssh/id_ed25519 medevs@192.168.178.23
```

### Step 2: Navigate to Your Project Directory

```bash
cd ~/projects/local-smart-portfolio
# OR wherever your portfolio project is located
```

### Step 3: Pull the Latest Code (Including the New Override File)

```bash
git pull origin main
```

This will pull the new `docker-compose.homelab.yml` file.

### Step 4: Verify GHCR Authentication

Make sure your server is authenticated to pull from GHCR:

```bash
# Check if you're logged in
cat ~/.docker/config.json | grep ghcr.io

# If not logged in, authenticate:
echo "YOUR_GHCR_TOKEN" | docker login ghcr.io -u medevs --password-stdin
```

Replace `YOUR_GHCR_TOKEN` with your actual GitHub Personal Access Token (the same one used in GitHub Actions secrets).

### Step 5: Stop Current Containers

```bash
docker compose down
# OR if you're using the override:
docker compose -f docker-compose.yml -f docker-compose.homelab.yml down
```

### Step 6: Pull Latest Images from GHCR

```bash
docker compose -f docker-compose.yml -f docker-compose.homelab.yml pull
```

This will pull the latest images from GHCR.

### Step 7: Start Containers with Homelab Override

```bash
docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d
```

### Step 8: Verify Containers Are Using GHCR Images

```bash
# Check which images are being used
docker compose -f docker-compose.yml -f docker-compose.homelab.yml ps

# Inspect a container to see its image
docker inspect portfolio-frontend | grep Image
docker inspect portfolio-backend | grep Image
```

You should see `ghcr.io/medevs/portfolio-frontend:latest` and `ghcr.io/medevs/portfolio-backend:latest`.

### Step 9: Verify Watchtower Is Running

```bash
# Check if Watchtower is running
docker ps | grep watchtower

# Check Watchtower logs
docker logs watchtower --tail 50
```

Watchtower should be monitoring your containers. If it's not running, start it:

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 30 \
  portfolio-frontend \
  portfolio-backend
```

The container names at the end tell Watchtower which containers to monitor.

---

## 🔄 Testing the CI/CD Pipeline

After completing the above steps:

1. **Make a small change** to your code (e.g., update a text in `frontend/data/personal.ts`)
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Test CI/CD deployment"
   git push origin main
   ```
3. **Wait for GitHub Actions** to complete (check Actions tab in GitHub)
4. **Wait 30 seconds** for Watchtower to detect the new image
5. **Check Watchtower logs**:
   ```bash
   docker logs watchtower --tail 20
   ```
6. **Verify the change** appears on your deployed site

---

## 🐛 Troubleshooting

### Issue: "Error response from daemon: pull access denied"

**Solution**: Your server is not authenticated to GHCR. Run Step 4 again.

### Issue: Watchtower not updating containers

**Solution**: 
1. Make sure Watchtower is monitoring the correct container names
2. Check that containers are using images from GHCR (not locally built)
3. Verify Watchtower logs: `docker logs watchtower`

### Issue: Containers still using old images

**Solution**:
```bash
# Force pull and recreate
docker compose -f docker-compose.yml -f docker-compose.homelab.yml pull
docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d --force-recreate
```

### Issue: Changes not appearing after update

**Solution**:
1. Clear browser cache
2. Check container logs: `docker logs portfolio-frontend --tail 50`
3. Verify the new image was pulled: `docker images | grep portfolio`

---

## 📝 Quick Reference Commands

```bash
# Start with homelab override
docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d

# Pull latest images
docker compose -f docker-compose.yml -f docker-compose.homelab.yml pull

# View running containers
docker compose -f docker-compose.yml -f docker-compose.homelab.yml ps

# View logs
docker compose -f docker-compose.yml -f docker-compose.homelab.yml logs -f

# Restart services
docker compose -f docker-compose.yml -f docker-compose.homelab.yml restart
```

---

## ✅ Verification Checklist

- [ ] `docker-compose.homelab.yml` file exists in project directory
- [ ] Server is authenticated to GHCR (`docker login ghcr.io`)
- [ ] Containers are using GHCR images (check with `docker inspect`)
- [ ] Watchtower is running and monitoring containers
- [ ] GitHub Actions workflow completes successfully
- [ ] Changes appear on deployed site after push

---

## 🎯 Expected Behavior After Fix

Once everything is configured correctly:

1. You push code to GitHub → GitHub Actions builds images → Images pushed to GHCR
2. Watchtower detects new `:latest` image in GHCR (within 30 seconds)
3. Watchtower pulls the new image and restarts the container
4. Your changes appear on the deployed site automatically

No manual intervention needed! 🚀

