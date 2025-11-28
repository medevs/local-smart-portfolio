# 👋 START HERE - Complete Setup Guide

Welcome! This guide will help you deploy your AI Portfolio application step by step.

---

## 🎯 What You Need

1. **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop/))
2. **Python** (to generate API key - usually already installed)
3. **15-20 minutes** of your time

---

## 📚 Choose Your Guide

### 🚀 **Option 1: Super Quick (5 minutes)**
**For experienced users or if you just want to get running fast:**
- Read: **[QUICK_START.md](./QUICK_START.md)**
- Or run: `setup.bat` (Windows) or `./setup.sh` (Mac/Linux)

### 📖 **Option 2: Detailed Step-by-Step (15 minutes)**
**For beginners or if you want to understand everything:**
- Read: **[STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md)**
- Includes explanations, troubleshooting, and screenshots

### 📋 **Option 3: Just Commands**
**If you just want copy-paste commands:**
- Read: **[COMMANDS_CHEATSHEET.md](./COMMANDS_CHEATSHEET.md)**

---

## 🎬 What You'll Do (Overview)

1. **Generate a secure API key** (30 seconds)
   ```cmd
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Create .env file** (1 minute)
   - Copy `.env.example` to `.env`
   - Paste your API key

3. **Start Docker** (5-10 minutes)
   ```cmd
   docker compose build
   docker compose up -d
   ```

4. **Download AI model** (5-15 minutes, one time)
   ```cmd
   docker compose exec ollama ollama pull llama3.2:3b
   ```

5. **Access your app!**
   - Frontend: http://localhost:3000
   - Admin: http://localhost:3000/admin

---

## 🆘 Need Help?

### Common Issues

**"Docker not found"**
- Install Docker Desktop from docker.com

**"Port already in use"**
- Stop other services using ports 3000 or 8000
- Or change ports in `docker-compose.yml`

**"Admin dashboard error"**
- Make sure `ADMIN_API_KEY` is set in `.env`
- Use the same key in the login screen

### Get More Help

- **Troubleshooting**: See [STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md) - Step 6
- **Docker Details**: See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)
- **View Logs**: `docker compose logs -f`

---

## 📁 Documentation Files

| File | Purpose |
|------|---------|
| **[QUICK_START.md](./QUICK_START.md)** | 5-minute quick setup |
| **[STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md)** | Detailed beginner guide |
| **[COMMANDS_CHEATSHEET.md](./COMMANDS_CHEATSHEET.md)** | Copy-paste commands |
| **[DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)** | Advanced Docker info |
| **[NEXT_STEPS.md](./NEXT_STEPS.md)** | What to do after setup |

---

## ✅ Quick Checklist

Before you start:
- [ ] Docker Desktop installed and running
- [ ] You're in the project folder
- [ ] You have 15-20 minutes

After setup:
- [ ] Can access http://localhost:3000
- [ ] Can login to admin dashboard
- [ ] Chat widget works
- [ ] Can upload documents

---

## 🎉 Ready to Start?

**Choose your path:**

1. **Fast Track**: Open [QUICK_START.md](./QUICK_START.md)
2. **Learn Everything**: Open [STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md)
3. **Just Commands**: Open [COMMANDS_CHEATSHEET.md](./COMMANDS_CHEATSHEET.md)

**Or run the automated setup:**

**Windows:**
```cmd
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

---

**Good luck! You've got this! 🚀**

