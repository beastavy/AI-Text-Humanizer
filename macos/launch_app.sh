#!/bin/bash

# AI Text Humanizer Pro Launcher
# This script launches the app directly using Python

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Launching AI Text Humanizer Pro..."
echo "====================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.10 or newer from https://www.python.org/downloads/"
    exit 1
fi

# Check if required files exist
if [ ! -f "$PROJECT_ROOT/main.py" ]; then
    echo "❌ main.py not found in project root"
    exit 1
fi

# Create a temporary virtual environment
echo "🔧 Setting up temporary environment..."
cd "$PROJECT_ROOT"
python3 -m venv temp_venv
source temp_venv/bin/activate

# Install required packages
echo "📥 Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK resources
echo "📚 Downloading NLTK resources..."
python3 -c "
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

# Download spaCy model if not present
echo "🧠 Setting up spaCy model..."
python3 -c "
try:
    import spacy
    try:
        nlp = spacy.load('en_core_web_sm')
        print('✅ spaCy en_core_web_sm model is already installed')
    except OSError:
        print('📥 Downloading spaCy en_core_web_sm model...')
        spacy.cli.download('en_core_web_sm')
        print('✅ spaCy en_core_web_sm model downloaded')
except Exception as e:
    print(f'⚠️ Error with spaCy: {e}')
"

echo "🎉 Starting AI Text Humanizer Pro..."
echo "The app will open in your browser shortly..."
echo ""
echo "To stop the app, press Ctrl+C"

# Launch the app
streamlit run main.py --server.port 8501 --server.address localhost

# Cleanup
deactivate