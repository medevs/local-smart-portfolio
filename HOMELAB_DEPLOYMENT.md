## 🏠 Homelab Deployment Guide – Local Smart Portfolio

This document explains **everything we’ve already done** and **every step you need** to deploy and run your `local-smart-portfolio` app on your homelab, using your existing Docker, Nginx Proxy Manager, Dashy, and monitoring stack.

It’s written so you can:
- Reproduce the setup any time.
- See which steps are already done.
- Know exactly what remains.

---

## 1. What You Already Had in Your Homelab

From your `📘 My Complete Homelab Journey` and the current server state, you already have:

- **Base system**
  - Ubuntu Server 22.04 LTS (`medevs`), Wi‑Fi-based, static DHCP lease on `192.168.178.23`.
  - SSH hardened (port `2222`, key-only login, UFW, Fail2ban, unattended upgrades).

- **Core services (running via Docker)**
  - `nginx-proxy-manager` (NPM) on ports `80`/`81`/`443`.
  - `portainer` for container management.
  - `nginx-demo` on port `8080`.
  - `dashy` as a homelab dashboard.
  - `monitoring` stack:
    - `prometheus` on port `9090`.
    - `cadvisor` on port `8082`.
    - `grafana` on port `3000`.

- **Project layout on the server**
  - `~/projects/dashy`
  - `~/projects/monitoring`
  - `~/projects/nginx-demo`
  - `~/projects/nginx-proxy-manager`
  - `~/projects/portainer`

All of that stays as-is. We are **adding** a new app: `local-smart-portfolio`.

---

## 2. What We Cloned and Where

On the server:

```bash
cd ~/projects
git clone <your GitHub repo> local-smart-portfolio
cd local-smart-portfolio
```

Current contents on the server (simplified):

```text
~/projects/local-smart-portfolio
  AUDIT_REPORT.md
  backend/
  frontend/
  infra/
  docker-compose.yml
  docker-compose.prod.yml
  docker-compose.homelab.yml
  DOCKER_DEPLOYMENT.md
  QUICK_START.md
  START_HERE.md
  STEP_BY_STEP_GUIDE.md
  COMMANDS_CHEATSHEET.md
  NEXT_STEPS.md
  setup.sh / setup.bat
```

---

## 3. Environment Files – What We Created

We created **server-side** env files based on your local dev ones, but adjusted for homelab/production.

### 3.1 Backend env – `backend/.env`

On the server (`~/projects/local-smart-portfolio/backend/.env`):

```env
# Production Environment
APP_NAME=AI Portfolio Backend
APP_VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://portfolio.medevs.local,http://portfolio-api.medevs.local,http://localhost:3000,http://127.0.0.1:3000
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION_NAME=portfolio_docs
UPLOAD_DIR=./data/documents
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=.pdf,.md,.txt,.docx
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=3
EMBEDDING_MODEL=all-MiniLM-L6-v2
ADMIN_API_KEY=TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg
```

**Important:**
- This `ADMIN_API_KEY` is your **admin login secret**. Keep it safe.

### 3.2 Frontend env – `frontend/.env.local`

On the server (`~/projects/local-smart-portfolio/frontend/.env.local`):

```env
# Production Environment
NEXT_PUBLIC_API_URL=http://portfolio-api.medevs.local
NEXT_PUBLIC_ADMIN_API_KEY=TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg
```

- `NEXT_PUBLIC_API_URL` is what the browser uses to call the backend.
- `NEXT_PUBLIC_ADMIN_API_KEY` allows the admin page to auto-validate this key.

You can change these values later, but this is the current working setup.

---

## 4. Local DNS / Hosts Setup (What You Did)

On your **Windows machine**, you added entries to:

```text
C:\Windows\System32\drivers\etc\hosts
```

Lines (example):

```text
192.168.178.23  portfolio.medevs.local
192.168.178.23  portfolio-api.medevs.local
```

Result:
- Hitting `http://portfolio.medevs.local` or `http://portfolio-api.medevs.local` from your browser now reaches your server.
- You saw the **Nginx Proxy Manager default page**, which confirms routing but not app wiring yet.

---

## 5. Docker Build – What We Ran

On the server (via SSH):

```bash
ssh -p 2222 -i ~/.ssh/id_ed25519 medevs@192.168.178.23
cd ~/projects/local-smart-portfolio

docker compose -f docker-compose.yml -f docker-compose.prod.yml build
```

This:
- Built `local-smart-portfolio-backend` (FastAPI image).
- Built `local-smart-portfolio-frontend` (Next.js standalone image).
- Reused cached layers after the first time (faster subsequent builds).

We also pulled the `ollama/ollama:latest` image automatically when bringing the stack up.

---

## 6. First Attempt to Start the Stack – What Happened

We ran:

```bash
ADMIN_API_KEY=TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg \
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Result:**

- `ollama`, `backend` started correctly.
- `frontend` failed with:

```text
Bind for 0.0.0.0:3000 failed: port is already allocated
```

Reason:
- Your Grafana container (from the `monitoring` stack) already uses **host port 3000**.
- Our `frontend` service in `docker-compose.yml` also maps `3000:3000`.

We then:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```

to cleanly stop/remove the partially started containers and the network.

---

## 7. Current Compose Configuration (Key Points)

### 7.1 Base compose – `docker-compose.yml`

- `backend`:
  - Exposes `8000:8000` (for dev/local) – **overridden to no ports in prod**.

- `frontend`:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-http://localhost:8000}
  container_name: portfolio-frontend
  restart: unless-stopped
  ports:
    - "3000:3000"   # <— conflicts with Grafana on the homelab
  environment:
    - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-http://backend:8000}
    - NEXT_PUBLIC_ADMIN_API_KEY=${ADMIN_API_KEY}
```

- `ollama`:
  - Exposes `11434:11434`, persists models in `/root/.ollama`.

### 7.2 Production override – `docker-compose.prod.yml`

- Removes port mappings for `backend` and `frontend` and introduces a dedicated **Nginx reverse proxy** on ports 80/443.

### 7.3 Homelab override – `docker-compose.homelab.yml`

We created this **simple override** file:

```yaml
services:
  frontend:
    ports:
      - "3100:3000"
```

Goal: expose the frontend on `3100` instead of `3000` to avoid conflict with Grafana.

However, Docker still complained about port 3000 being allocated. That means:
- The original `3000:3000` mapping from `docker-compose.yml` is still active, and our override must either **replace** or **remove** that mapping more explicitly.

---

## 8. Recommended Clean Strategy from Here

You have **two valid options** for running the portfolio frontend in your homelab:

### Option A – Keep Grafana on 3000, run portfolio on 3100

1. **Edit `docker-compose.yml` on the server** to remove the hard-coded `3000:3000` mapping and rely on the homelab override instead.

   In `~/projects/local-smart-portfolio/docker-compose.yml`:

   - Find:

   ```yaml
   frontend:
     ...
     ports:
       - "3000:3000"
   ```

   - Change it to:

   ```yaml
   frontend:
     ...
     ports: []
   ```

2. **Keep `docker-compose.homelab.yml` as:**

   ```yaml
   services:
     frontend:
       ports:
         - "3100:3000"
   ```

3. **Start the stack using the homelab override:**

   ```bash
   cd ~/projects/local-smart-portfolio

   ADMIN_API_KEY=TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg \
     docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d
   ```

4. **Check containers:**

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.homelab.yml ps
   ```

   You should see:
   - `portfolio-ollama` (up)
   - `portfolio-backend` (healthy)
   - `portfolio-frontend` (up, bound to `3100->3000`)

5. **Pull the model if not already done (only once):**

   ```bash
   docker compose exec ollama ollama pull llama3.2:3b
   ```

6. **Test directly from your PC:**

   - Backend health:

     ```bash
     curl http://192.168.178.23:8000/health
     ```

   - Frontend:

     - In the browser: `http://192.168.178.23:3100`
     - Admin: `http://192.168.178.23:3100/admin`
     - Use admin key: `TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg`

7. **Later: wire Nginx Proxy Manager (NPM)**

   Once you confirm that `http://192.168.178.23:3100` works, you can:

   - In NPM, create a Proxy Host:
     - Domain: `portfolio.medevs.local`
     - Forward IP: `192.168.178.23`
     - Forward Port: `3100`
     - Scheme: `http`
   - Save and test `http://portfolio.medevs.local`.

This option is **easiest right now** and keeps everything LAN-only.

### Option B – Use the Nginx container from `docker-compose.prod.yml`

This is closer to a “real” production stack:

1. Use:

   ```bash
   ADMIN_API_KEY=... \
     docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

2. Let the `portfolio-nginx` container listen on ports `80` and `443`.
3. Configure NPM (or skip NPM) and talk directly to your homelab’s `80/443`.

Because you already have NPM on `80/443`, this requires more careful planning (to avoid conflicts) and is better as a **later** refactor.

---

## 9. Step-by-Step Checklist for You

Here’s a **simple checklist** you can follow now:

1. **SSH into server**

   ```bash
   ssh -p 2222 -i ~/.ssh/id_ed25519 medevs@192.168.178.23
   cd ~/projects/local-smart-portfolio
   ```

2. **Edit frontend ports in base compose** (Option A, recommended now)

   - Open `docker-compose.yml` and change:

   ```yaml
   frontend:
     ...
     ports:
       - "3000:3000"
   ```

   to:

   ```yaml
   frontend:
     ...
     ports: []
   ```

3. **Ensure `docker-compose.homelab.yml` contains:**

   ```yaml
   services:
     frontend:
       ports:
         - "3100:3000"
   ```

4. **Start the stack (homelab profile):**

   ```bash
   ADMIN_API_KEY=TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg \
     docker compose -f docker-compose.yml -f docker-compose.homelab.yml up -d
   ```

5. **Verify containers:**

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.homelab.yml ps
   ```

6. **(If not done) Pull the LLM model:**

   ```bash
   docker compose exec ollama ollama pull llama3.2:3b
   ```

7. **Test from your PC:**

   - `http://192.168.178.23:3100` → portfolio UI.
   - `http://192.168.178.23:3100/admin` → admin login.
   - Key: `TIUcWCcaKrobhWtabzKG2n93Bd4c6IIa1dvPoAgg`.

8. **Later: add a Proxy Host in NPM (optional for now)**

   - Domain: `portfolio.medevs.local`
   - Forward to `192.168.178.23:3100`.

---

## 10. Summary

- Your homelab is already **very well prepared** (SSH hardening, NPM, Portainer, Dashy, Grafana/Prometheus/cAdvisor).
- We:
  - Cloned the `local-smart-portfolio` repo to `~/projects/local-smart-portfolio`.
  - Created production-ish env files for backend and frontend.
  - Built Docker images for backend, frontend, and Ollama.
  - Hit a **port conflict** on 3000 with Grafana.
  - Introduced a homelab override to move the frontend to **3100**.
- The main remaining work is:
  - Adjusting the compose ports as described.
  - Bringing the stack up with the homelab override.
  - Testing and then optionally integrating with NPM / Dashy.

You can refer back to this file any time as the **single source of truth** for how your portfolio app is deployed on the homelab.


