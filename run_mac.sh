#!/bin/bash

echo ""
echo "========================================"
echo "  AI Text Humanizer Pro - ONE CLICK"
echo "========================================"
echo ""
echo "This will automatically:"
echo "1. Set up everything (if needed)"
echo "2. Start the app"
echo ""
echo "Please wait..."
echo ""

# Get the directory where this script is located
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ Python 3 is not installed!"
    echo ""
    echo "Please install Python first:"
    echo "1. Go to: https://www.python.org/downloads/"
    echo "2. Download Python 3.10+ for macOS"
    echo "3. Install it and make sure to check 'Add Python to PATH'"
    echo "4. Restart Terminal"
    echo "5. Run this script again"
    echo ""
    read -p "Press Enter to continue..."
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "🔧 Setting up for first time..."
    echo "This may take 5-10 minutes..."
    echo ""
    
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        read -p "Press Enter to continue..."
        exit 1
    fi
    
    echo "✅ Virtual environment created"
    echo ""
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Upgrading pip..."
    pip install --upgrade pip --quiet
    
    echo "Installing packages..."
    echo "This may take several minutes..."
    pip install streamlit --quiet
    pip install spacy --quiet
    pip install nltk --quiet
    pip install sentence-transformers --quiet
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install core packages"
        echo "Please check your internet connection and try again"
        read -p "Press Enter to continue..."
        exit 1
    fi
    
    echo "Installing remaining packages..."
    pip install -r requirements.txt --quiet
    
    echo "Downloading language models..."
    python -m spacy download en_core_web_sm --quiet
    
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
    
    echo ""
    echo "✅ Setup completed!"
    echo ""
else
    echo "✅ Virtual environment found"
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if required packages are installed
echo "✅ Checking dependencies..."
python -c "import streamlit, spacy, nltk; print('✅ All dependencies available')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies! Reinstalling..."
    pip install -r requirements.txt --quiet
    python -m spacy download en_core_web_sm --quiet
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
