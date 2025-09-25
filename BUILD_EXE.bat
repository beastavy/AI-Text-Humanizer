@echo off
echo Building AI Text Humanizer Pro Executable...
echo.

cd /d "D:\AI HUMNIZER\AI-Text-Humanizer-App"

echo Activating virtual environment...
call .\venv\Scripts\Activate.ps1

echo.
echo Installing required packages...
pip install pyinstaller

echo.
echo Creating icon...
python create_icon.py

echo.
echo Building executable with PyInstaller...
echo This may take several minutes...
echo.

pyinstaller --onefile --windowed --name "AI_Text_Humanizer_Pro" --icon=icon.ico --add-data "transformer;transformer" --hidden-import streamlit --hidden-import nltk --hidden-import spacy --hidden-import sentence_transformers main_professional.py

echo.
echo Build complete!
echo.
echo The executable can be found in the 'dist' folder:
echo dist\AI_Text_Humanizer_Pro.exe
echo.
echo You can now distribute this .exe file to run the app without Python!
echo.
pause
