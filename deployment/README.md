# Deployment Configurations

This directory contains optional deployment configurations for specific use cases.

## Files

### `docker-compose.homelab.yml`

**Purpose**: For homelab deployments using CI/CD with GHCR (GitHub Container Registry) images.

**When to use**: 
- You have CI/CD set up that builds and pushes images to GHCR
- You want automatic updates from your container registry
- You're deploying to a homelab server

**Usage**:
```bash
docker compose -f docker-compose.yml -f deployment/docker-compose.homelab.yml up -d
```

**Note**: Update the image names (`ghcr.io/medevs/portfolio-*`) to match your own registry if using this template.

---

## For Regular Users

If you're just using this as a portfolio template, you don't need any files in this directory. Simply use:

```bash
docker compose up -d
```

This will build the images locally from the Dockerfiles.

