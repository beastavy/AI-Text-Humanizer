@echo off
echo ========================================
echo Starting AI Text Humanizer App
echo ========================================
echo.

cd /d "D:\AI HUMNIZER\AI-Text-Humanizer-App"
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Streamlit application...
echo.
echo The app will open in your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.

streamlit run main.py

pause
