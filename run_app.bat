@echo off
echo ========================================
echo Starting AI Text Humanizer App
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Streamlit application...
streamlit run main.py

pause
