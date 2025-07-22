echo off
@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Hero Fate server...
python app.py
pause 