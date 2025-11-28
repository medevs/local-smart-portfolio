# 📋 Commands Cheat Sheet

Copy-paste ready commands for Windows!

---

## 🔐 Generate API Key

```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Copy the output!**

---

## 📝 Setup Environment

```cmd
copy .env.example .env
notepad .env
```

**In Notepad:**
1. Find: `ADMIN_API_KEY=your-secure-api-key-here...`
2. Replace with your key from above
3. Save (Ctrl+S)
4. Close

---

## 🐳 Docker Commands

### First Time Setup

```cmd
REM Build images (5-10 minutes)
docker compose build

REM Start services
docker compose up -d

REM Download AI model (5-15 minutes)
docker compose exec ollama ollama pull llama3.2:3b
```

### Daily Use

```cmd
REM Start everything
docker compose up -d

REM Stop everything
docker compose down

REM View logs
docker compose logs -f

REM Check status
docker compose ps

REM Restart a service
docker compose restart backend
```

### Troubleshooting

```cmd
REM View all logs
docker compose logs -f

REM View backend logs only
docker compose logs -f backend

REM Restart everything
docker compose down
docker compose up -d

REM Full reset (WARNING: deletes data)
docker compose down -v
docker compose up -d
```

---

## 🌐 Access URLs

```
Frontend:     http://localhost:3000
Admin:        http://localhost:3000/admin
Backend API:  http://localhost:8000
Health Check: http://localhost:8000/health
API Docs:     http://localhost:8000/docs
```

---

## ✅ Quick Test Commands

```cmd
REM Test backend
curl http://localhost:8000/health

REM Check Ollama models
docker compose exec ollama ollama list

REM Check service status
docker compose ps
```

---

## 🎯 Complete Setup (One Go)

```cmd
REM 1. Generate key
python -c "import secrets; print(secrets.token_urlsafe(32))"

REM 2. Create .env (then edit it with the key above)
copy .env.example .env
notepad .env

REM 3. Build and start
docker compose build
docker compose up -d

REM 4. Download model
docker compose exec ollama ollama pull llama3.2:3b

REM 5. Open browser
start http://localhost:3000
```

---

## 📱 Admin Dashboard Login

1. Go to: http://localhost:3000/admin
2. Enter your API key (from Step 1)
3. Click "Access Dashboard"

---

**That's all you need! 🎉**

