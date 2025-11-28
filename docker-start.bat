@echo off
REM =============================================================================
REM Docker Quick Start Script (Windows)
REM =============================================================================

echo 🐳 AI Portfolio - Docker Quick Start
echo ====================================
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo 📝 Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo 🔐 IMPORTANT: Edit .env and set ADMIN_API_KEY!
    echo    Generate a secure key:
    echo    python -c "import secrets; print(secrets.token_urlsafe(32))"
    echo.
    pause
)

REM Check if ADMIN_API_KEY is set (basic check)
findstr /C:"ADMIN_API_KEY=your-secure-api-key-here" .env >nul
if %errorlevel% == 0 (
    echo ❌ ERROR: ADMIN_API_KEY is not set in .env!
    echo    Please set a secure API key before continuing.
    pause
    exit /b 1
)

echo ✅ Environment configured
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed!
    pause
    exit /b 1
)

docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed!
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose found
echo.

REM Build and start services
echo 🔨 Building Docker images...
docker compose build

echo.
echo 🚀 Starting services...
docker compose up -d

echo.
echo ⏳ Waiting for services to be healthy...
timeout /t 10 /nobreak >nul

REM Check service health
echo.
echo 📊 Service Status:
docker compose ps

echo.
echo 📝 Initializing Ollama model (this may take a few minutes)...
echo    Model: llama3.2:3b
docker compose exec ollama ollama pull llama3.2:3b

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Access the application:
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    Health:    http://localhost:8000/health
echo.
echo 📋 Useful commands:
echo    View logs:    docker compose logs -f
echo    Stop:         docker compose down
echo    Restart:      docker compose restart
echo.
pause

