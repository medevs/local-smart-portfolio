# ⚡ Quick Start Guide - 5 Minutes

The fastest way to get your AI Portfolio running!

---

## 🎯 Two Options

### Option 1: Automated Setup (Easiest) ⭐

**Just run one command:**

**Windows:**
```cmd
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**That's it!** The script will:
- ✅ Generate a secure API key
- ✅ Create .env file
- ✅ Build Docker images
- ✅ Start all services
- ✅ Show you how to access everything

**Skip to "Step 4: Access" below!**

---

### Option 2: Manual Setup (Step-by-Step)

Follow these exact steps:

---

## 📝 Step 1: Generate API Key (30 seconds)

**Open Command Prompt or PowerShell:**

```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**You'll get something like:**
```
Xk9mP2qR7vN4tY8wZ1aB3cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6
```

**📋 Copy this key!** You'll need it in a moment.

---

## 📝 Step 2: Create .env File (1 minute)

### 2.1 Create the file

**In Command Prompt (in your project folder):**
```cmd
copy .env.example .env
```

### 2.2 Edit the file

**Open `.env` in Notepad or any text editor**

**Find this line:**
```
ADMIN_API_KEY=your-secure-api-key-here-minimum-16-characters
```

**Replace it with your key from Step 1:**
```
ADMIN_API_KEY=Xk9mP2qR7vN4tY8wZ1aB3cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6
```

**💾 Save the file!**

---

## 🐳 Step 3: Start Docker (3-5 minutes)

### 3.1 Build images (first time only)

```cmd
docker compose build
```

**Wait for it to finish** (5-10 minutes first time)

### 3.2 Start services

```cmd
docker compose up -d
```

**You should see:**
```
[+] Running 3/3
 ✔ Container portfolio-ollama    Started
 ✔ Container portfolio-backend  Started
 ✔ Container portfolio-frontend Started
```

### 3.3 Download AI model (one time)

```cmd
docker compose exec ollama ollama pull llama3.2:3b
```

**This downloads ~2GB** (5-15 minutes depending on internet)

---

## 🌐 Step 4: Access Your Application

### Open in Browser:

1. **Portfolio Website:**
   ```
   http://localhost:3000
   ```

2. **Admin Dashboard:**
   ```
   http://localhost:3000/admin
   ```
   - Enter your API key (from Step 1)
   - Click "Access Dashboard"

3. **Backend Health Check:**
   ```
   http://localhost:8000/health
   ```

---

## ✅ Verify Everything Works

### Test 1: Backend Health
- Go to: http://localhost:8000/health
- Should show: `{"status": "healthy", ...}`

### Test 2: Frontend
- Go to: http://localhost:3000
- Should see: Your portfolio homepage

### Test 3: Admin Dashboard
- Go to: http://localhost:3000/admin
- Enter your API key
- Should see: Dashboard with system status

### Test 4: Chat
- Click "AI Chat" button
- Type: "Hello"
- Should get: AI response

---

## 🎉 Success!

If all tests pass, you're done! Your application is running.

---

## 🆘 Troubleshooting

### "Port already in use"
```cmd
docker compose down
docker compose up -d
```

### "Cannot connect to Ollama"
```cmd
docker compose restart ollama
docker compose exec ollama ollama list
```

### "Admin dashboard shows error"
- Make sure `ADMIN_API_KEY` is set in `.env`
- Use the same key in the login screen
- Check: `docker compose logs backend`

### View logs
```cmd
docker compose logs -f
```

---

## 📋 Common Commands

```cmd
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Restart a service
docker compose restart backend

# Check status
docker compose ps
```

---

## 📚 Need More Details?

- **Full Step-by-Step Guide**: See [STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md)
- **Docker Details**: See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)
- **Next Steps**: See [NEXT_STEPS.md](./NEXT_STEPS.md)

---

**That's it! You're ready to go! 🚀**

