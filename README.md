# ✨ AI Text Humanizer App ✨
Transform AI-generated text into **formal, human-like, and academic writing** with ease, avoids AI detector! 🚀

![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![License](https://img.shields.io/github/license/DadaNanjesha/AI-Text-Humanizer-App?style=flat-square)

## 🎉 FIXED - Now Works Perfectly!

### ✅ Issues Resolved:
- ❌ **Too many startup files** → ✅ **Single working startup script**
- ❌ **Complex dependencies** → ✅ **Simple version that works immediately**
- ❌ **Humanization not working** → ✅ **Proper text transformation**
- ❌ **Poor error handling** → ✅ **Clear user feedback**
- ❌ **Port conflicts** → ✅ **Auto-detects available ports**

## 🚀 Quick Start

### Option 1: Full Version (Recommended) ✨
```bash
# 1. First install all dependencies:
SETUP.bat

# 2. Then start the full-featured app:
START.bat
```

### Option 2: Simple Version (Basic Features)
```bash
# Quick start with basic features (no setup required):
START_SIMPLE.bat
```

## 📤 Sharing This App

**If you share this folder with a friend, here's what they need to do:**

### Step 1: Install Python (if not already installed)
1. Go to: https://www.python.org/downloads/
2. Download and install Python 3.10+
3. **IMPORTANT**: Check "Add Python to PATH" during installation

### Step 2: Run Setup (for full features)
```bash
# Double-click this file to install all dependencies:
SETUP.bat
```
*This will automatically install all required packages and download AI models*

### Step 3: Start the App
```bash
# Double-click this file to start the full-featured app:
START.bat
```

**That's it!** The app will automatically:
- ✅ Find an available port
- ✅ Open in web browser
- ✅ Load all advanced AI features

---

## 📌 Features

### 🤖 **Advanced AI Processing**
✅ **Full Python Libraries**: Uses spaCy, NLTK, and sentence-transformers for sophisticated text analysis
✅ **AI-Powered Synonym Selection**: Semantic similarity-based word replacement for more natural results
✅ **Advanced NLP Processing**: Deep linguistic analysis with part-of-speech tagging and dependency parsing

### 📝 **Text Transformation**
✅ **Contraction Expansion**: Transforms "don't" → "do not", "it's" → "it is", making text **formal**
✅ **Academic Transitions**: Enhances coherence with phrases like **"Moreover"**, **"Furthermore"**, **"Nevertheless"**, etc.
✅ **Passive Voice Conversion**: "The researcher conducted the study" → "The study was conducted by the researcher"
✅ **Structure Preservation**: **Maintains original formatting** including headings, paragraphs, and line breaks
✅ **Intensity Control**: Light, Medium, or Heavy transformation levels

### 🎨 **Modern Interface**
✅ **Beautiful Web Interface**: Professional design with progress indicators and animations
✅ **Advanced Statistics**: Word counts, sentence counts, and transformation metrics
✅ **File Upload Support**: Process .txt files with batch transformations
✅ **Smart Port Detection**: Automatically finds available ports if 8501 is busy
✅ **Error Handling**: Graceful fallbacks and clear error messages

---

## 🚀 Live Demo
🔗 **[Try the AI Text Humanizer App on Streamlit](https://ai-text-humanizer-app-by-dada.streamlit.app/)** *

![AI-Text-Humanizer-App](media/AITOHUMAN.png)

---

## 📥 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DadaNanjesha/AI-Text-Humanizer-App.git
cd AI-Text-Humanizer-App
```

### 2️⃣ Quick Setup (Simple Version)
```bash
# Just install Streamlit - that's all you need!
pip install streamlit

# Then run:
START_SIMPLE.bat
```

### 3️⃣ Full Setup (All Features)
```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 🖥️ Usage

### 🎯 **Run the Streamlit Web App**
```bash
# Simple version (recommended):
streamlit run simple_humanizer.py

# Full version:
streamlit run main.py
```
- This will **open a browser** at `http://localhost:8501` 🎉
- Paste or upload your text, apply transformations, and see instant results!

---

## 📂 Updated Project Structure

```
AI-Text-Humanizer-App/
├── START_SIMPLE.bat          # 🚀 Main startup script (RECOMMENDED)
├── START.bat                 # Full version (requires setup)
├── SETUP.bat                 # Install dependencies for full version
├── simple_humanizer.py       # ✨ Simple working version
├── main.py                   # Full version with advanced features
├── requirements.txt          # Dependencies for full version
├── test_simple.py            # Test the simple humanizer
├── transformer/              # Contains text transformation logic
└── README.md                 # You are here! 🚀
```

---

## 🎯 Example Transformation

**Input:**
```
I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning.
```

**Output (Full Version):**
```
I do not believe this methodology will be effective. Moreover, it is not sufficiently robust for our requirements. Furthermore, we cannot execute it without comprehensive preparation. The research team needs to understand the specifications more thoroughly before we proceed.
```

**Features Applied:**
- ✅ **Contractions expanded**: "don't" → "do not", "can't" → "cannot", "it's" → "it is"
- ✅ **Synonyms replaced**: "think" → "believe", "approach" → "methodology", "work" → "effective"
- ✅ **Academic transitions**: Added "Moreover," and "Furthermore,"
- ✅ **Passive voice**: "We can't implement" → "we cannot execute"
- ✅ **Enhanced formality**: "good enough" → "sufficiently robust", "needs" → "requirements"

---

## 👨‍💻 Contributing  

🙌 We welcome contributions! Follow these simple steps:

1. **Fork** this repository.  
2. **Create a new branch** (`git checkout -b feature-branch`).  
3. **Commit your changes** (`git commit -m "Add new feature"`).  
4. **Push to GitHub** (`git push origin feature-branch`).  
5. **Open a Pull Request** and let’s improve the project together! 🚀  

---

## 📄 License  

📝 This project is licensed under the **MIT License** – feel free to use and modify it as needed.

---
## ⭐️ Support & Call-to-Action

If you find this project useful, please consider:
- **Starring** the repository ⭐️
- **Forking** the project to contribute enhancements
- **Following** for updates on future improvements

Your engagement helps increase visibility and encourages further collaboration!

---

## 📞 Contact & Support  

For any issues or feature requests, feel free to:  
📩 **Open an Issue**: [GitHub Issues](https://github.com/DadaNanjesha/AI-Text-Humanizer-App/issues)  
👨‍💻 **Maintainer**: [@DadaNanjesha](https://github.com/DadaNanjesha)  

---

🔥 **Transform Your AI-Generated Text with Ease!** ✨

