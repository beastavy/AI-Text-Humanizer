# AI Text Humanizer App - PowerShell Run Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting AI Text Humanizer App" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "Starting Streamlit application..." -ForegroundColor Yellow
streamlit run main.py
