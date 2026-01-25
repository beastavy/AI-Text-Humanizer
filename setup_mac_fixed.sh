#!/bin/bash

echo ""
echo "========================================"
echo "  AI Text Humanizer Pro - MAC FIXED SETUP"
echo "========================================"
echo ""
echo "This will fix the spacy installation issue on Mac"
echo "Please wait..."
echo ""

# Get the directory where this script is located
cd "$(dirname "$0")"

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ Python 3 is not installed or not in PATH"
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

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ Python 3.8+ is required. Current version: $PYTHON_VERSION"
    echo "Please upgrade Python and try again."
    read -p "Press Enter to continue..."
    exit 1
fi

echo "✅ Python version is compatible"
echo ""

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

echo "Creating fresh virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    echo "Trying with --clear flag..."
    python3 -m venv venv --clear
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "Please check your Python installation"
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

echo "✅ Virtual environment created"
echo ""

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel --quiet

echo "Installing core dependencies first..."
echo "This may take 5-10 minutes..."

# Install core packages one by one with error handling
echo "Installing streamlit..."
pip install streamlit --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install streamlit"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Installing numpy (required for spacy)..."
pip install numpy --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install numpy"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Installing spacy..."
pip install spacy --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install spacy"
    echo "Trying alternative installation method..."
    pip install spacy --no-cache-dir --quiet
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install spacy with alternative method"
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

echo "Installing nltk..."
pip install nltk --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install nltk"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Installing sentence-transformers..."
pip install sentence-transformers --quiet
if [ $? -ne 0 ]; then
    echo "⚠️ sentence-transformers failed, but continuing..."
fi

echo ""
echo "✅ Core packages installed"
echo ""

echo "Installing remaining packages from requirements.txt..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "⚠️ Some packages may have failed, but continuing..."
fi

echo ""
echo "Downloading spaCy language model..."
echo "This is the critical step that was failing before..."

# Try multiple methods to download the spacy model
echo "Method 1: Direct download..."
python -m spacy download en_core_web_sm --quiet
if [ $? -ne 0 ]; then
    echo "Method 1 failed. Trying Method 2..."
    
    # Method 2: Install via pip
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl --quiet
    if [ $? -ne 0 ]; then
        echo "Method 2 failed. Trying Method 3..."
        
        # Method 3: Manual download and install
        echo "Downloading model manually..."
        curl -L https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl -o en_core_web_sm.whl
        if [ $? -eq 0 ]; then
            pip install en_core_web_sm.whl --quiet
            rm en_core_web_sm.whl
        else
            echo "❌ All methods failed to download spacy model"
            echo "Please check your internet connection and try again"
            read -p "Press Enter to continue..."
            exit 1
        fi
    fi
fi

echo "✅ spaCy model downloaded successfully"
echo ""

# Download NLTK resources
echo "Downloading NLTK resources..."
python -c "
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = ssl._create_unverified_https_context

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
echo "Testing installation..."
python -c "
try:
    import spacy
    import nltk
    import streamlit
    print('✅ All core packages imported successfully')
    
    # Test spacy model
    nlp = spacy.load('en_core_web_sm')
    doc = nlp('This is a test.')
    print('✅ spaCy model working correctly')
    
    # Test nltk
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize('This is a test.')
    print('✅ NLTK working correctly')
    
    print('✅ All tests passed!')
    
except Exception as e:
    print(f'❌ Test failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Installation test failed"
    echo "Please check the error messages above"
    read -p "Press Enter to continue..."
    exit 1
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Your AI Text Humanizer Pro is ready to use!"
echo ""
echo "Features available:"
echo "✅ Contraction expansion"
echo "✅ Academic transitions"
echo "✅ Synonym replacement"
echo "✅ Passive voice conversion"
echo "✅ Structure preservation"
echo ""
echo "To start the app, run: ./start_mac_fixed.sh"
echo ""
echo "The app will open in your browser automatically."
echo ""
read -p "Press Enter to continue..."

