#!/bin/bash

echo "========================================"
echo "   AI Text Humanizer Pro - Launcher"
echo "========================================"
echo ""

# Get the directory where this script is located
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ Python 3 is not installed or not in PATH"
    echo ""
    echo "Please install Python first:"
    echo "1. Go to: https://www.python.org/downloads/"
    echo "2. Install Python 3.10+"
    echo "3. Make sure Python is in your PATH"
    echo "4. Restart Terminal"
    echo "5. Run ./setup.sh first, then ./start.sh"
    echo ""
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first to set up the environment."
    echo ""
    read -p "Press Enter to continue..."
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "✅ Checking dependencies..."
python -c "import streamlit, spacy, nltk; print('✅ All dependencies available')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies!"
    echo "Please run ./setup.sh first to install required packages."
    echo ""
    read -p "Press Enter to continue..."
    exit 1
fi

echo ""
echo "🚀 Starting AI Text Humanizer Pro..."
echo "========================================"
echo ""
echo "The app will open in your web browser automatically."
echo "You can also visit: http://localhost:\$PORT"
echo ""
echo "Press Ctrl+C in this window to stop the server."
echo ""

# Find an available port
PORT=8501
MAX_PORT=8520

while [ $PORT -le $MAX_PORT ]; do
    if ! lsof -i :$PORT >/dev/null 2>&1; then
        break
    fi
    PORT=$((PORT + 1))
done

if [ $PORT -gt $MAX_PORT ]; then
    echo "❌ No available ports found between 8501-8520"
    echo "Please close some applications and try again"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "✅ Using port $PORT"
echo ""

# Start the application
python -m streamlit run main.py --server.headless true --server.port $PORT

read -p "Press Enter to continue..."

