@echo off
echo ========================================
echo    AI Text Humanizer Pro - Simple
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Install Python 3.10+
    echo 3. Check "Add Python to PATH" during installation
    echo 4. Restart your computer
    echo 5. Try again
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ℹ️ No virtual environment found, using system Python...
)

REM Find an available port
set PORT=8501
set MAX_PORT=8520

:CHECK_PORT
netstat -an | findstr :%PORT% >nul
if %errorlevel% equ 0 (
    set /a PORT=%PORT%+1
    if %PORT% gtr %MAX_PORT% (
        echo ❌ No available ports found between 8501-8520
        echo Please close some applications and try again
        pause
        exit /b 1
    )
    goto CHECK_PORT
)

echo ✅ Using port %PORT%
echo.

echo 🚀 Starting AI Text Humanizer Pro (Simple Version)...
echo ========================================
echo.
echo The app will open in your web browser automatically.
echo You can also visit: http://localhost:%PORT%
echo.
echo Press Ctrl+C in this window to stop the server.
echo.

REM Start the simple humanizer
python -m streamlit run simple_humanizer.py --server.headless true --server.port %PORT%

pause
