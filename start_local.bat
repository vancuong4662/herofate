@echo off
echo ==========================================
echo Starting MongoDB Local Service
echo ==========================================

echo Checking if MongoDB service is running...
sc query MongoDB > nul 2>&1
if %errorlevel% == 0 (
    echo ✅ MongoDB service is already running
) else (
    echo Starting MongoDB service...
    net start MongoDB
    if %errorlevel% == 0 (
        echo ✅ MongoDB service started successfully
    ) else (
        echo ❌ Failed to start MongoDB service
        echo Please make sure MongoDB is installed correctly
        pause
        exit /b 1
    )
)

echo.
echo ==========================================
echo Starting Hero Fate Server
echo ==========================================
python app.py
pause
