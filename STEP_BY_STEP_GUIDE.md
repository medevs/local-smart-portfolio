# 📖 Step-by-Step Deployment Guide

Complete beginner-friendly guide to deploy your AI Portfolio application.

---

## 🎯 Overview

This guide will walk you through:
1. Generating secure API keys
2. Setting up environment variables
3. Starting the application with Docker
4. Testing everything works
5. Accessing the admin dashboard

**Time Required**: 15-20 minutes  
**Difficulty**: Beginner-friendly

---

## 📋 Prerequisites Check

Before starting, make sure you have:

### 1. Docker Installed

**Check if Docker is installed:**
```bash
docker --version
```

**If not installed:**
- **Windows**: Download from [docker.com](https://www.docker.com/products/docker-desktop/)
- **Mac**: Download from [docker.com](https://www.docker.com/products/docker-desktop/)
- **Linux**: 
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### 2. Docker Compose Installed

**Check if Docker Compose is installed:**
```bash
docker compose version
```

**If not installed** (usually comes with Docker Desktop):
- Install Docker Desktop (includes Docker Compose)

### 3. Git (Optional)

To clone the repository if you haven't already.

---

## 🔐 Step 1: Generate Secure API Key

You need a secure API key for the admin dashboard. Here's how to generate one:

### Option A: Using Python (Recommended)

**Windows (Command Prompt or PowerShell):**
```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Mac/Linux:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**What you'll get:**
```
Xk9mP2qR7vN4tY8wZ1aB3cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6
```

**Copy this key** - you'll need it in the next step!

### Option B: Using Online Generator

1. Go to: https://randomkeygen.com/
2. Use "CodeIgniter Encryption Keys" section
3. Copy a 32+ character key

### Option C: Manual (Not Recommended)

Create a random string of at least 32 characters:
```
my-super-secret-api-key-12345-abcdef-67890
```

**⚠️ Important**: The key should be:
- At least 16 characters (32+ recommended)
- Random and unpredictable
- Different for development and production

---

## 📝 Step 2: Create Environment File

### 2.1 Navigate to Project Directory

```bash
# If you're not already there
cd C:\Users\ahmed\OneDrive\Documents\apps\portfolio
```

### 2.2 Create .env File

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

### 2.3 Edit .env File

Open `.env` in a text editor (Notepad, VS Code, etc.)

**Find this line:**
```
ADMIN_API_KEY=your-secure-api-key-here-minimum-16-characters
```

**Replace it with your generated key:**
```
ADMIN_API_KEY=Xk9mP2qR7vN4tY8wZ1aB3cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6
```

**Example of complete .env file:**
```env
# Security Settings (REQUIRED)
ADMIN_API_KEY=Xk9mP2qR7vN4tY8wZ1aB3cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6

# Application Settings
APP_NAME=AI Portfolio Backend
APP_VERSION=1.0.0
DEBUG=false

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Ollama LLM Settings
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b

# ChromaDB Settings
CHROMA_COLLECTION_NAME=portfolio_docs

# Document Processing
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=.pdf,.md,.txt,.docx

# RAG Settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=3

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**✅ Save the file!**

---

## 🐳 Step 3: Start Docker Services

### 3.1 Build Docker Images

This will create the container images for your application:

```bash
docker compose build
```

**What's happening:**
- Building backend image (Python/FastAPI)
- Building frontend image (Next.js)
- This may take 5-10 minutes the first time

**Expected output:**
```
[+] Building 45.2s (15/15) FINISHED
 => [backend builder] ...
 => [frontend deps] ...
 => [frontend builder] ...
```

### 3.2 Start All Services

```bash
docker compose up -d
```

**What's happening:**
- Starting backend container
- Starting frontend container
- Starting Ollama container
- `-d` means "detached" (runs in background)

**Expected output:**
```
[+] Running 4/4
 ✔ Container portfolio-ollama    Started
 ✔ Container portfolio-backend  Started
 ✔ Container portfolio-frontend Started
```

### 3.3 Check Service Status

```bash
docker compose ps
```

**You should see:**
```
NAME                  STATUS          PORTS
portfolio-backend     Up 30 seconds   0.0.0.0:8000->8000/tcp
portfolio-frontend    Up 30 seconds   0.0.0.0:3000->3000/tcp
portfolio-ollama      Up 30 seconds   0.0.0.0:11434->11434/tcp
```

**All should show "Up" status!**

---

## 📥 Step 4: Initialize Ollama Model

Ollama needs to download the AI model. This is a one-time setup:

### 4.1 Pull the Model

```bash
docker compose exec ollama ollama pull llama3.2:3b
```

**What's happening:**
- Downloading the LLM model (llama3.2:3b)
- This is ~2GB download
- Takes 5-15 minutes depending on internet speed

**Expected output:**
```
pulling manifest
pulling 8b8e9f5e2c3a... 100% ▕████████████████▏ 2.0 GB
pulling 5eb2fa8b1a38... 100% ▕████████████████▏ 1.0 KB
pulling 7c23fb36d801... 100% ▕████████████████▏ 4.8 KB
pulling 4915f10e6b5a... 100% ▕████████████████▏  30 B
verifying sha256 digest
writing manifest
success
```

### 4.2 Verify Model is Installed

```bash
docker compose exec ollama ollama list
```

**You should see:**
```
NAME            ID              SIZE    MODIFIED
llama3.2:3b     abc123def456    2.0GB   2 minutes ago
```

**✅ Model is ready!**

---

## ✅ Step 5: Test Everything Works

### 5.1 Test Backend Health

Open in browser or use curl:

**Browser:**
```
http://localhost:8000/health
```

**Command line:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-27T..."
}
```

### 5.2 Test Frontend

**Open in browser:**
```
http://localhost:3000
```

**You should see:**
- Your portfolio homepage
- Navigation menu
- Chat widget button (bottom right)

### 5.3 Test Admin Dashboard

**Open in browser:**
```
http://localhost:3000/admin
```

**You'll see:**
1. **API Key Login Screen**
   - Enter your `ADMIN_API_KEY` from Step 2
   - Click "Access Dashboard"

2. **Admin Dashboard**
   - System Status (Backend, Ollama, ChromaDB should be green)
   - Knowledge Base stats
   - Document upload section

**✅ If you see the dashboard, authentication works!**

### 5.4 Test Chat

1. Click the **"AI Chat"** button (top right or floating button)
2. Type a message: `"Hello"`
3. Press Enter or click Send

**Expected:**
- Message appears in chat
- AI responds (may take 5-10 seconds)
- Response includes information from your documents

**✅ If chat works, everything is configured correctly!**

---

## 🔍 Step 6: View Logs (If Something Goes Wrong)

### View All Logs

```bash
docker compose logs -f
```

**Press `Ctrl+C` to exit**

### View Specific Service Logs

```bash
# Backend logs
docker compose logs -f backend

# Frontend logs
docker compose logs -f frontend

# Ollama logs
docker compose logs -f ollama
```

### Common Issues and Solutions

#### Issue: "Port already in use"

**Solution:**
```bash
# Find what's using the port
# Windows:
netstat -ano | findstr :8000

# Stop the service using that port, or change port in docker-compose.yml
```

#### Issue: "Cannot connect to Ollama"

**Solution:**
```bash
# Check Ollama is running
docker compose ps ollama

# Restart Ollama
docker compose restart ollama

# Verify model is installed
docker compose exec ollama ollama list
```

#### Issue: "Admin dashboard shows error"

**Solution:**
- Make sure `ADMIN_API_KEY` is set in `.env`
- Make sure you're using the same key in the login screen
- Check backend logs: `docker compose logs backend`

---

## 🎉 Step 7: You're Done!

Your application is now running! Here's what you have:

### Access Points:
- **Portfolio**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3000/admin
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Useful Commands:

```bash
# Stop all services
docker compose down

# Start services again
docker compose up -d

# Restart a specific service
docker compose restart backend

# View logs
docker compose logs -f

# Rebuild after code changes
docker compose build
docker compose up -d
```

---

## 📚 Next Steps

### Upload Documents to Knowledge Base

1. Go to http://localhost:3000/admin
2. Login with your API key
3. Click "Choose File" in Upload Document section
4. Select a PDF, Markdown, TXT, or DOCX file
5. Click "Upload"
6. Wait for processing (30-60 seconds)
7. Document appears in the list

### Test RAG (Retrieval-Augmented Generation)

1. Upload a document about yourself (resume, bio, etc.)
2. Open chat widget
3. Ask: "Tell me about Ahmed" (or your name)
4. AI should respond using information from your document!

---

## 🔒 Security Reminders

1. **Never commit `.env` file** to Git
2. **Use different API keys** for development and production
3. **Keep your API key secret** - don't share it
4. **Rotate keys** if you suspect they're compromised

---

## ❓ Need Help?

### Check Logs
```bash
docker compose logs -f
```

### Check Service Status
```bash
docker compose ps
```

### Restart Everything
```bash
docker compose down
docker compose up -d
```

### Full Reset (WARNING: Deletes all data)
```bash
docker compose down -v
docker compose up -d
```

---

## 📝 Quick Reference Card

```bash
# 1. Generate API Key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. Create .env file
copy .env.example .env
# Edit .env and set ADMIN_API_KEY

# 3. Start services
docker compose build
docker compose up -d

# 4. Initialize Ollama
docker compose exec ollama ollama pull llama3.2:3b

# 5. Access application
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# Admin:    http://localhost:3000/admin
```

---

**Congratulations! 🎉 Your AI Portfolio is now running!**

