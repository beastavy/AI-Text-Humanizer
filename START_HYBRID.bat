@echo off
echo.
echo ========================================
echo   AI Text Humanizer Pro - Hybrid Mode
echo ========================================
echo.
echo Starting Flask server with full Python libraries...
echo.
echo Frontend: http://localhost:5000
echo API: http://localhost:5000/api/
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
call .\venv\Scripts\activate.bat
python app.py

pause
