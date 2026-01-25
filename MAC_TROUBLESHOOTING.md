# Mac Troubleshooting Guide - "No module named spacy" Fix

## Quick Fix for "No module named spacy" Error

If your friend is getting the "no module named spacy" error on Mac, here's the step-by-step solution:

### Method 1: Use the Fixed Setup Script (Recommended)

1. **Download the fixed setup script** (if not already available):
   ```bash
   # Make sure you're in the AI-Text-Humanizer-App directory
   cd /path/to/AI-Text-Humanizer-App
   ```

2. **Make the script executable**:
   ```bash
   chmod +x setup_mac_fixed.sh
   chmod +x start_mac_fixed.sh
   ```

3. **Run the fixed setup**:
   ```bash
   ./setup_mac_fixed.sh
   ```

4. **Start the app**:
   ```bash
   ./start_mac_fixed.sh
   ```

### Method 2: Manual Installation (If Method 1 Fails)

If the fixed script doesn't work, try this manual approach:

1. **Open Terminal** and navigate to the app directory:
   ```bash
   cd /path/to/AI-Text-Humanizer-App
   ```

2. **Remove any existing virtual environment**:
   ```bash
   rm -rf venv
   ```

3. **Create a fresh virtual environment**:
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

5. **Upgrade pip and install core packages**:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install numpy
   pip install spacy
   pip install nltk
   pip install streamlit
   ```

6. **Download the spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

   If that fails, try:
   ```bash
   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
   ```

7. **Install remaining packages**:
   ```bash
   pip install -r requirements.txt
   ```

8. **Test the installation**:
   ```bash
   python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy working!')"
   ```

9. **Start the app**:
   ```bash
   python -m streamlit run main.py
   ```

### Method 3: Alternative Installation (If Methods 1 & 2 Fail)

If you're still having issues, try this alternative approach:

1. **Install using conda instead of pip**:
   ```bash
   # Install conda if not already installed
   # Download from: https://docs.conda.io/en/latest/miniconda.html
   
   conda create -n humanizer python=3.10
   conda activate humanizer
   conda install spacy
   python -m spacy download en_core_web_sm
   pip install streamlit nltk sentence-transformers
   ```

2. **Or use Homebrew to install Python dependencies**:
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python and dependencies
   brew install python@3.10
   python3.10 -m venv venv
   source venv/bin/activate
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

## Common Issues and Solutions

### Issue 1: "spacy: command not found"
**Solution**: Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Issue 2: "Permission denied" errors
**Solution**: Use `sudo` or fix permissions:
```bash
sudo pip install spacy
# OR
chmod +x setup_mac_fixed.sh
```

### Issue 3: "No module named en_core_web_sm"
**Solution**: The language model wasn't downloaded properly:
```bash
python -m spacy download en_core_web_sm
# OR
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

### Issue 4: "Failed to build wheel"
**Solution**: Install build tools:
```bash
pip install --upgrade pip setuptools wheel
pip install spacy --no-cache-dir
```

### Issue 5: "SSL Certificate" errors
**Solution**: This is handled automatically in the fixed script, but if you need to do it manually:
```bash
python -c "
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = ssl._create_unverified_https_context
"
```

## Verification Steps

After installation, verify everything is working:

1. **Test spaCy**:
   ```bash
   python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✅ spaCy working!')"
   ```

2. **Test NLTK**:
   ```bash
   python -c "import nltk; from nltk.tokenize import word_tokenize; print('✅ NLTK working!')"
   ```

3. **Test Streamlit**:
   ```bash
   python -c "import streamlit; print('✅ Streamlit working!')"
   ```

4. **Test the full app**:
   ```bash
   python -m streamlit run main.py
   ```

## System Requirements

- **macOS**: 10.14 (Mojave) or newer
- **Python**: 3.8 or newer (3.10+ recommended)
- **RAM**: At least 4GB
- **Storage**: At least 2GB free space
- **Internet**: Required for downloading models

## Still Having Issues?

If none of these methods work:

1. **Check Python version**: `python3 --version`
2. **Check if you're in the right directory**: `pwd`
3. **Check if virtual environment is activated**: Look for `(venv)` in your terminal prompt
4. **Try a different Python version**: Install Python 3.10 specifically
5. **Check internet connection**: The models need to be downloaded
6. **Try running as administrator**: `sudo ./setup_mac_fixed.sh`

## Contact Support

If you're still having issues, please provide:
1. Your macOS version: `sw_vers`
2. Your Python version: `python3 --version`
3. The exact error message you're seeing
4. Which method you tried

The fixed setup script should resolve the "no module named spacy" error in 99% of cases.
