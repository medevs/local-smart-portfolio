# 🚀 Local Development Guide - Quick Test

This guide will help you run the portfolio locally to test your changes.

---

## 📋 Prerequisites

Make sure you have installed:
- **Node.js 18+** (check with `node --version`)
- **pnpm** (install with `npm install -g pnpm`)
- **Python 3.11+** (check with `python --version`)
- **Ollama** (download from https://ollama.com)

---

## ⚡ Quick Start (5 minutes)

### Step 1: Start Ollama (Required for Backend)

**Open a terminal and run:**
```bash
ollama serve
```

**In another terminal, pull the model:**
```bash
ollama pull llama3.2:3b
```

Keep Ollama running in the background.

---

### Step 2: Setup Backend

**Open a new terminal:**

```bash
# Navigate to backend folder
cd backend

# Create virtual environment (Windows)
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Create backend/.env file:**

Create a file named `.env` in the `backend` folder with this content:

```env
# Application Settings
APP_NAME=AI Portfolio Backend
APP_VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8000

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# ChromaDB Settings
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION_NAME=portfolio_docs

# Document Settings
UPLOAD_DIR=./data/documents
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=.pdf,.md,.txt,.docx

# RAG Settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=3
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Admin Settings (REQUIRED - generate a secure key)
ADMIN_API_KEY=your-secure-api-key-here-minimum-16-characters
```

**Generate a secure API key:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and replace `your-secure-api-key-here-minimum-16-characters` in the `.env` file.

**Start the backend:**

```bash
# Make sure venv is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!**

---

### Step 3: Setup Frontend

**Open a NEW terminal:**

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies (first time only)
pnpm install

# Start development server
pnpm dev
```

You should see:
```
  ▲ Next.js 15.5.5
  - Local:        http://localhost:3000
```

**Keep this terminal open!**

---

### Step 4: Access Your Application

Open your browser and go to:

- **Portfolio Website**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3000/admin
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

---

## ✅ Verify Everything Works

1. **Check Backend Health:**
   - Go to: http://localhost:8000/health
   - Should show: `{"status": "healthy", ...}`

2. **Check Frontend:**
   - Go to: http://localhost:3000
   - Should see your portfolio with your name "Ahmed Oublihi"
   - Should see your projects (TaB/TheDoc, Docopresso, etc.)

3. **Check Admin Dashboard:**
   - Go to: http://localhost:3000/admin
   - Enter the API key you set in `backend/.env`
   - Should see the admin dashboard

---

## 🎯 Testing Your Changes

After making changes to:
- **Frontend files** → Changes appear automatically (Next.js hot reload)
- **Backend files** → Backend restarts automatically (Uvicorn --reload)

**To see your personal data updates:**
1. Make sure you saved all files
2. Refresh the browser (Ctrl+R or Cmd+R)
3. Check that your name, projects, and timeline appear correctly

---

## 🛑 Stopping the Servers

**To stop:**
- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

**To stop Ollama:**
- Press `Ctrl+C` in the Ollama terminal

---

## 🆘 Troubleshooting

### "Port 8000 already in use"
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :8000
# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### "Port 3000 already in use"
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :3000
# Kill the process
taskkill /PID <PID> /F
```

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if model is downloaded: `ollama list`
- If not, download it: `ollama pull llama3.2:3b`

### "Module not found" errors
```bash
# Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
pnpm install
```

### "Admin API key invalid"
- Make sure you set `ADMIN_API_KEY` in `backend/.env`
- Use the same key when logging into `/admin`
- Restart the backend after changing `.env`

---

## 📝 Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
pnpm dev

# Ollama
ollama serve
ollama pull llama3.2:3b
ollama list
```

---

## 🎉 You're Ready!

Your portfolio should now be running locally with all your personal data!

**Next Steps:**
- Test all pages (Home, About, Projects, Contact)
- Verify your personal information is correct
- Test the admin dashboard
- Make any adjustments needed

