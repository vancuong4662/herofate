@echo off
echo ==========================================
echo MongoDB Configuration Switcher
echo ==========================================
echo.
echo Current configuration:
findstr "^MONGODB_URI=" .env | findstr /v "^#"
echo.
echo 1. Switch to Local MongoDB (Development)
echo 2. Switch to MongoDB Atlas (Production)
echo 3. Cancel
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Switching to Local MongoDB...
    powershell -Command "(Get-Content .env) -replace '^MONGODB_URI=mongodb\+srv://.*', '# MONGODB_URI=mongodb+srv://adminGumCode:ZF@ck3rzC@cluster0.kpjzv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' -replace '^# MONGODB_URI=mongodb://localhost:27017/', 'MONGODB_URI=mongodb://localhost:27017/' -replace '^ENVIRONMENT=.*', 'ENVIRONMENT=development' | Set-Content .env"
    echo ✅ Switched to Local MongoDB
    echo 🏠 Environment: Development
) else if "%choice%"=="2" (
    echo Switching to MongoDB Atlas...
    powershell -Command "(Get-Content .env) -replace '^MONGODB_URI=mongodb://localhost:27017/', '# MONGODB_URI=mongodb://localhost:27017/' -replace '^# MONGODB_URI=mongodb\+srv://.*', 'MONGODB_URI=mongodb+srv://adminGumCode:ZF@ck3rzC@cluster0.kpjzv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' -replace '^ENVIRONMENT=.*', 'ENVIRONMENT=production' | Set-Content .env"
    echo ✅ Switched to MongoDB Atlas
    echo ☁️ Environment: Production
) else (
    echo Operation cancelled
)

echo.
echo New configuration:
findstr "^MONGODB_URI=" .env | findstr /v "^#"
echo.
pause
