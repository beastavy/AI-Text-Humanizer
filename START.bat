@echo off
echo ========================================
echo    AI Text Humanizer Pro - Launcher
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
    echo 5. Run SETUP.bat first, then START.bat
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run SETUP.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if required packages are installed
echo ✅ Checking dependencies...
python -c "import streamlit, spacy, nltk; print('✅ All dependencies available')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Missing dependencies!
    echo Please run SETUP.bat first to install required packages.
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting AI Text Humanizer Pro...
echo ========================================
echo.
echo The app will open in your web browser automatically.
echo You can also visit: http://localhost:%PORT%
echo.
echo Press Ctrl+C in this window to stop the server.
echo.

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

REM Start the application
python -m streamlit run main.py --server.headless true --server.port %PORT%

pause
