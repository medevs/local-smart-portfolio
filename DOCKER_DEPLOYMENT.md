# 🐳 Docker Deployment Guide

Complete guide for deploying the AI Portfolio application using Docker and Docker Compose.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Development Mode](#development-mode)
- [Production Deployment](#production-deployment)
- [Data Persistence](#data-persistence)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

---

## Prerequisites

### Required Software

1. **Docker** (version 20.10+)
   ```bash
   # Check Docker version
   docker --version
   ```

2. **Docker Compose** (version 2.0+)
   ```bash
   # Check Docker Compose version
   docker compose version
   ```

3. **Git** (for cloning the repository)

### System Requirements

- **CPU**: 2+ cores recommended
- **RAM**: 8GB minimum (16GB recommended for Ollama)
- **Disk**: 20GB+ free space (for models and data)
- **OS**: Linux, macOS, or Windows with WSL2

---

## Quick Start

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd portfolio
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your ADMIN_API_KEY
# Generate a secure key:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Required in `.env`:**
- `ADMIN_API_KEY` - Must be set (minimum 16 characters)

### 3. Start Services

```bash
# Build and start all services
docker compose up -d

# View logs
docker compose logs -f

# Check service status
docker compose ps
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Ollama**: http://localhost:11434
- **Health Check**: http://localhost:8000/health

### 5. Initialize Ollama Model

```bash
# Pull the LLM model (this may take several minutes)
docker compose exec ollama ollama pull llama3.2:3b

# Verify model is available
docker compose exec ollama ollama list
```

---

## Configuration

### Environment Variables

All configuration is done via environment variables in `.env`:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ADMIN_API_KEY` | Admin API key for protected endpoints | - | ✅ Yes |
| `NEXT_PUBLIC_API_URL` | Backend API URL for frontend | `http://localhost:8000` | No |
| `OLLAMA_MODEL` | Ollama model to use | `llama3.2:3b` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:3001` | No |

### Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Next.js application |
| Backend | 8000 | FastAPI REST API |
| Ollama | 11434 | Local LLM server |

---

## Development Mode

### Start Development Environment

```bash
# Start with auto-reload (if using volume mounts)
docker compose up

# Or run in background
docker compose up -d
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f ollama
```

### Rebuild After Changes

```bash
# Rebuild specific service
docker compose build backend
docker compose up -d backend

# Rebuild all services
docker compose build
docker compose up -d
```

### Execute Commands in Containers

```bash
# Backend shell
docker compose exec backend bash

# Frontend shell
docker compose exec frontend sh

# Ollama commands
docker compose exec ollama ollama list
docker compose exec ollama ollama pull <model>
```

---

## Production Deployment

### 1. Production Configuration

```bash
# Use production compose file
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 2. Set Production Environment Variables

Update `.env` for production:

```env
DEBUG=false
NEXT_PUBLIC_API_URL=https://your-domain.com/api
CORS_ORIGINS=https://your-domain.com
ADMIN_API_KEY=<strong-production-key>
```

### 3. Configure Nginx (Optional)

The production compose file includes Nginx reverse proxy:

1. **Update Nginx configuration**:
   ```bash
   # Edit infra/nginx/conf.d/default.conf
   # Update server_name with your domain
   ```

2. **SSL/TLS Setup** (Recommended):
   ```bash
   # Place SSL certificates in:
   infra/nginx/ssl/fullchain.pem
   infra/nginx/ssl/privkey.pem
   
   # Uncomment HTTPS server block in default.conf
   ```

3. **Start with Nginx**:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

### 4. Resource Limits

Production compose includes resource limits. Adjust in `docker-compose.prod.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

---

## Data Persistence

### Docker Volumes

Data is persisted in Docker volumes:

| Volume | Contains | Location |
|--------|---------|----------|
| `chroma_data` | ChromaDB vector database | `/app/data/chroma_db` |
| `documents_data` | Uploaded documents | `/app/data/documents` |
| `backend_logs` | Application logs | `/app/logs` |
| `ollama_data` | Ollama models | `/root/.ollama` |

### Backup Data

```bash
# Backup ChromaDB
docker run --rm -v portfolio_chroma_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/chroma_backup.tar.gz /data

# Backup documents
docker run --rm -v portfolio_documents_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/documents_backup.tar.gz /data
```

### Restore Data

```bash
# Restore ChromaDB
docker run --rm -v portfolio_chroma_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/chroma_backup.tar.gz -C /

# Restore documents
docker run --rm -v portfolio_documents_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/documents_backup.tar.gz -C /
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check service status
docker compose ps

# View error logs
docker compose logs <service-name>

# Check container health
docker compose ps
```

### Port Already in Use

```bash
# Find process using port
# Linux/Mac:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Change port in docker-compose.yml:
ports:
  - "8001:8000"  # Host:Container
```

### Ollama Model Not Found

```bash
# Pull the model
docker compose exec ollama ollama pull llama3.2:3b

# Verify
docker compose exec ollama ollama list
```

### Backend Can't Connect to Ollama

```bash
# Check Ollama is running
docker compose ps ollama

# Check network connectivity
docker compose exec backend curl http://ollama:11434/api/tags

# Verify OLLAMA_BASE_URL in .env
OLLAMA_BASE_URL=http://ollama:11434
```

### Frontend Can't Connect to Backend

```bash
# Verify NEXT_PUBLIC_API_URL
# In Docker: use service name (http://backend:8000)
# From browser: use host URL (http://localhost:8000)

# Check CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Permission Errors

```bash
# Fix volume permissions
docker compose down
sudo chown -R $USER:$USER <volume-path>
docker compose up -d
```

---

## Security Considerations

### 1. API Key Security

- ✅ **Never commit** `.env` files to version control
- ✅ Use **strong, random** API keys (32+ characters)
- ✅ **Rotate** keys regularly in production
- ✅ Use **different keys** for development and production

### 2. Network Security

- ✅ Use **reverse proxy** (Nginx) in production
- ✅ Enable **HTTPS/TLS** for all external traffic
- ✅ **Restrict** CORS origins to your domain only
- ✅ Use **Docker networks** to isolate services

### 3. Container Security

- ✅ Run containers as **non-root** users (frontend does this)
- ✅ Use **resource limits** to prevent DoS
- ✅ Keep **base images updated**
- ✅ Scan images for vulnerabilities

### 4. Data Security

- ✅ **Backup** volumes regularly
- ✅ **Encrypt** sensitive data at rest
- ✅ Use **secure** volume drivers
- ✅ **Restrict** access to volume mounts

---

## Common Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild and restart
docker compose up -d --build

# Remove everything (including volumes)
docker compose down -v

# Execute command in container
docker compose exec <service> <command>

# Check resource usage
docker stats

# Clean up unused resources
docker system prune -a
```

---

## Next Steps

1. ✅ **Configure SSL/TLS** for production
2. ✅ **Set up monitoring** (Prometheus, Grafana)
3. ✅ **Configure backups** (automated)
4. ✅ **Set up CI/CD** pipeline
5. ✅ **Enable logging** aggregation

---

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review service logs: `docker compose logs`
- Check GitHub Issues
- Review documentation in `docs/`

---

**Last Updated**: November 27, 2025

