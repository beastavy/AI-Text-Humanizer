# AI Text Humanizer App - Setup Guide

## Prerequisites

Before running this application, you need to have Python installed on your system. If you don't have Python installed or are experiencing issues, follow these steps:

### 1. Install Python

**Option A: Download from Python.org**
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. During installation, make sure to check "Add Python to PATH"

**Option B: Use Microsoft Store**
1. Open Microsoft Store
2. Search for "Python 3.13" or "Python 3.12"
3. Install the official Python package

### 2. Verify Python Installation

Open PowerShell or Command Prompt and run:
```bash
python --version
```
or
```bash
python3 --version
```

## Setup Instructions

### 1. Navigate to the Project Directory
```bash
cd "D:\AI HUMNIZER\AI-Text-Humanizer-App"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**For Windows PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

**For Windows Command Prompt:**
```bash
venv\Scripts\activate.bat
```

### 4. Upgrade pip
```bash
python -m pip install --upgrade pip
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Download Required NLP Models

**Download spaCy model:**
```bash
python -m spacy download en_core_web_sm
```

**Download NLTK resources:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger');"
```

## Running the Application

### Start the Streamlit App
```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## Features

- **AI-Powered Text Refinement**: Converts AI-generated or informal text into academic format
- **Expand Contractions**: Transforms "don't" → "do not", "it's" → "it is"
- **Add Academic Transitions**: Enhances coherence with phrases like "Moreover", "Therefore"
- **Passive Voice Conversion**: Optional conversion to passive voice
- **Synonym Replacement**: Optional replacement with more sophisticated alternatives
- **Word & Sentence Statistics**: View counts before and after transformation

## Troubleshooting

### If Python is not recognized:
1. Restart your terminal/PowerShell after installing Python
2. Try using `py` instead of `python`
3. Check if Python is added to your system PATH

### If you get permission errors:
1. Run PowerShell as Administrator
2. Set execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### If models fail to download:
1. Check your internet connection
2. Try running the download commands individually
3. Some models are large and may take time to download

## Alternative: Use the Setup Script

The repository includes a `setup.sh` script that can help with the setup process. On Windows, you can run it using Git Bash or WSL.
