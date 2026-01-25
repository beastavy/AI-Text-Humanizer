@echo off
echo Installing AI Text Humanizer...
echo.

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install basic packages first
pip install --upgrade pip
pip install streamlit flask flask-cors nltk spacy

REM Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

REM Install spaCy model
python -m spacy download en_core_web_sm

echo.
echo Setup complete! Now run START_SIMPLE.bat
pause




