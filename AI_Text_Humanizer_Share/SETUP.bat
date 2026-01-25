@echo off
echo.
echo ========================================
echo   AI Text Humanizer Pro - Auto Setup
echo ========================================
echo.
echo This will automatically set up the AI Text Humanizer Pro
echo for your friend. Please wait...
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
echo This may take 5-10 minutes on first run...
echo.

pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed successfully!
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Your AI Text Humanizer Pro is ready to use!
echo.
echo To start the app, double-click: START_AI_HUMANIZER.bat
echo.
echo The app will open in your browser automatically.
echo.
pause
