echo off
@echo off
echo ==========================================
echo Hero Fate - Web Game Online
echo ==========================================
echo.
echo Note: This will use the database configured in .env file
echo - For Local MongoDB: Use start_local.bat (recommended for development)
echo - To switch database: Use switch_db.bat
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Hero Fate server...
python app.py
pause 