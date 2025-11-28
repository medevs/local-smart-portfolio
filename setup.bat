@echo off
REM =============================================================================
REM Automated Setup Script for AI Portfolio (Windows)
REM =============================================================================

echo 🚀 AI Portfolio - Automated Setup
echo ==================================
echo.

REM Step 1: Check prerequisites
echo 📋 Step 1: Checking prerequisites...
echo.

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed!
    echo    Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
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

REM Step 2: Generate API key
echo 🔐 Step 2: Generating secure API key...
echo.

python -c "import secrets; print(secrets.token_urlsafe(32))" > temp_key.txt 2>nul
if %errorlevel% neq 0 (
    python3 -c "import secrets; print(secrets.token_urlsafe(32))" > temp_key.txt 2>nul
    if %errorlevel% neq 0 (
        echo ⚠️  Python not found. Please generate API key manually.
        echo    Run: python -c "import secrets; print(secrets.token_urlsafe(32))"
        set /p API_KEY="Enter your API key: "
        goto :create_env
    )
)

set /p API_KEY=<temp_key.txt
del temp_key.txt

echo ✅ Generated API key: %API_KEY:~0,20%...
echo.

:create_env
REM Step 3: Create .env file
echo 📝 Step 3: Creating .env file...
echo.

if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ Created .env from .env.example
    ) else (
        echo ❌ .env.example not found!
        pause
        exit /b 1
    )
) else (
    echo ⚠️  .env file already exists
    set /p OVERWRITE="Do you want to overwrite it? (y/N): "
    if /i not "%OVERWRITE%"=="y" (
        echo Keeping existing .env file
        REM Still update ADMIN_API_KEY if it's the default
        findstr /C:"ADMIN_API_KEY=your-secure-api-key-here" .env >nul
        if %errorlevel% == 0 (
            powershell -Command "(Get-Content .env) -replace 'ADMIN_API_KEY=your-secure-api-key-here.*', 'ADMIN_API_KEY=%API_KEY%' | Set-Content .env"
            echo ✅ Updated ADMIN_API_KEY in existing .env
        )
        goto :build
    ) else (
        copy .env.example .env >nul
        echo ✅ Overwritten .env file
    )
)

REM Update ADMIN_API_KEY in .env
powershell -Command "(Get-Content .env) -replace 'ADMIN_API_KEY=.*', 'ADMIN_API_KEY=%API_KEY%' | Set-Content .env"

echo ✅ Updated ADMIN_API_KEY in .env
echo.

:build
REM Step 4: Build Docker images
echo 🔨 Step 4: Building Docker images...
echo    This may take 5-10 minutes...
echo.

docker compose build
if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Docker images built successfully
echo.

REM Step 5: Start services
echo 🚀 Step 5: Starting services...
echo.

docker compose up -d
if %errorlevel% neq 0 (
    echo ❌ Failed to start services!
    pause
    exit /b 1
)

echo.
echo ✅ Services started
echo.

REM Step 6: Wait for services
echo ⏳ Step 6: Waiting for services to be ready...
echo.

timeout /t 10 /nobreak >nul

echo 📊 Service Status:
docker compose ps

echo.

REM Step 7: Initialize Ollama
echo 📥 Step 7: Initializing Ollama model...
echo    This will download ~2GB model (5-15 minutes)
echo.

set /p DOWNLOAD_MODEL="Do you want to download the model now? (Y/n): "
if /i not "%DOWNLOAD_MODEL%"=="n" (
    echo Downloading llama3.2:3b model...
    docker compose exec ollama ollama pull llama3.2:3b
    if %errorlevel% neq 0 (
        echo ⚠️  Model download failed. You can run it manually later:
        echo    docker compose exec ollama ollama pull llama3.2:3b
    )
) else (
    echo ⚠️  Skipping model download. Run this later:
    echo    docker compose exec ollama ollama pull llama3.2:3b
)

echo.

REM Final summary
echo ==================================
echo ✅ Setup Complete!
echo ==================================
echo.
echo 🌐 Access your application:
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    Admin:     http://localhost:3000/admin
echo    Health:    http://localhost:8000/health
echo.
echo 🔑 Your Admin API Key:
echo    %API_KEY%
echo    (Also saved in .env file)
echo.
echo 📋 Useful commands:
echo    View logs:    docker compose logs -f
echo    Stop:         docker compose down
echo    Restart:      docker compose restart
echo    Status:       docker compose ps
echo.
echo ⚠️  Remember: Keep your API key secret!
echo.
pause

