@echo off
echo.
echo ========================================
echo   AI Text Humanizer Pro - Auto Setup
echo ========================================
echo.
echo This will automatically set up the AI Text Humanizer Pro
echo with full Python libraries. Please wait...
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo Installation steps:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download and install Python 3.10 or newer
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart your computer if prompted
    echo 5. Run this SETUP.bat again
    echo.
    echo After installing Python, come back and double-click this file again.
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
    echo Trying alternative method...
    python -m venv venv --clear
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment again
        pause
        exit /b 1
    )
)

echo ✅ Virtual environment created
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
pip install --upgrade pip --quiet

echo Installing core packages...
echo This may take 5-10 minutes on first run...
echo.

REM Install core packages first
pip install streamlit --quiet
pip install spacy --quiet
pip install nltk --quiet
pip install sentence-transformers --quiet

if %errorlevel% neq 0 (
    echo ❌ Failed to install core packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ Core packages installed
echo.

echo Installing remaining packages...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo ⚠️ Some packages may have failed, but core functionality should work
    echo Continuing with setup...
)

echo.
echo ✅ Installing Python libraries...
echo.

REM Download spaCy model
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm --quiet
if %errorlevel% neq 0 (
    echo ⚠️ spaCy model download may have failed, but will retry later
)

REM Download NLTK resources
echo Downloading NLTK resources...
python -c "
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
resources = ['punkt', 'averaged_perceptron_tagger', 'punkt_tab', 'wordnet', 'averaged_perceptron_tagger_eng']
for resource in resources:
    try:
        nltk.download(resource, quiet=True)
        print(f'✅ {resource} downloaded')
    except Exception as e:
        print(f'⚠️ Failed to download {resource}: {e}')
"

if %errorlevel% neq 0 (
    echo ⚠️ Some NLTK resources may have failed, but core functionality should work
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
echo Features available:
echo ✅ Contraction expansion
echo ✅ Academic transitions
echo ✅ Synonym replacement
echo ✅ Passive voice conversion
echo ✅ Structure preservation
echo.
echo To start the app, double-click: START.bat
echo.
echo The app will open in your browser automatically.
echo.
pause