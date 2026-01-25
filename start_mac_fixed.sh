#!/bin/bash

echo ""
echo "========================================"
echo "  AI Text Humanizer Pro - START"
echo "========================================"
echo ""

# Get the directory where this script is located
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup_mac_fixed.sh first"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Test if all dependencies are available
echo "Checking dependencies..."
python -c "
try:
    import spacy
    import nltk
    import streamlit
    nlp = spacy.load('en_core_web_sm')
    print('✅ All dependencies available')
except Exception as e:
    print(f'❌ Missing dependencies: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Dependencies not properly installed"
    echo "Please run ./setup_mac_fixed.sh again"
    read -p "Press Enter to continue..."
    exit 1
fi

echo ""
echo "🚀 Starting AI Text Humanizer Pro..."
echo "========================================"
echo ""
echo "The app will open in your web browser automatically."
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
echo "Press Ctrl+C to stop the server when you're done."
echo ""

# Start the application
python -m streamlit run main.py --server.headless true --server.port $PORT
]
