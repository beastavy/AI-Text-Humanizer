# AI Text Humanizer Pro - Mac Setup Guide

## Quick Start for Mac Users

### Prerequisites
- macOS (any recent version)
- Python 3.10 or newer
- Terminal app

### Installation Steps

1. **Download Python** (if not already installed):
   - Go to https://www.python.org/downloads/
   - Download Python 3.10+ for macOS
   - Run the installer and make sure to check "Add Python to PATH"

2. **Open Terminal**:
   - Press `Cmd + Space` and type "Terminal"
   - Press Enter to open Terminal

3. **Navigate to the app folder**:
   ```bash
   cd /path/to/AI-Text-Humanizer-App
   ```

4. **Make scripts executable**:
   ```bash
   chmod +x setup.sh start.sh
   ```

5. **Run the setup**:
   ```bash
   ./setup.sh
   ```
   This will:
   - Create a virtual environment
   - Install all required Python packages
   - Download language models
   - Set up everything automatically

6. **Start the app**:
   ```bash
   ./start.sh
   ```

### What the App Does

The AI Text Humanizer Pro helps you make AI-generated text sound more human by:

- ✅ **Contraction expansion** - Converts "don't" to "do not"
- ✅ **Academic transitions** - Adds professional connecting phrases
- ✅ **Synonym replacement** - Uses varied vocabulary
- ✅ **Passive voice conversion** - Makes writing more active
- ✅ **Structure preservation** - Maintains original meaning

### Troubleshooting

**If you get "command not found" errors:**
- Make sure Python is installed: `python3 --version`
- Make sure you're in the right directory
- Try running: `python3 setup.sh` instead of `./setup.sh`

**If setup fails:**
- Check your internet connection
- Make sure you have enough disk space (at least 2GB free)
- Try running the setup again

**If the app won't start:**
- Make sure you ran `./setup.sh` first
- Check that all dependencies are installed
- Try running: `python3 -m streamlit run main.py`

### File Structure

```
AI-Text-Humanizer-App/
├── setup.sh          # Mac setup script
├── start.sh           # Mac start script
├── main.py            # Main application
├── requirements.txt   # Python dependencies
└── README_MAC.md      # This file
```

### Support

If you encounter any issues:
1. Make sure Python 3.10+ is installed
2. Check that you have internet connection
3. Ensure you have at least 2GB free disk space
4. Try running the setup script again

The app will automatically open in your default web browser once started.

