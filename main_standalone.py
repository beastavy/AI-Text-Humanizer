#!/usr/bin/env python3
"""
Standalone AI Text Humanizer - Simple version that works as executable
"""

import streamlit as st
import re
import random
import time
import os
import sys

# Simple text transformation functions
def expand_contractions(text):
    """Expand contractions in text"""
    contractions = {
        "don't": "do not", "doesn't": "does not", "didn't": "did not",
        "won't": "will not", "can't": "cannot", "couldn't": "could not",
        "wouldn't": "would not", "shouldn't": "should not", "mustn't": "must not",
        "isn't": "is not", "aren't": "are not", "wasn't": "was not",
        "weren't": "were not", "hasn't": "has not", "haven't": "have not",
        "hadn't": "had not",
        "I'm": "I am", "you're": "you are", "he's": "he is", "she's": "she is",
        "we're": "we are", "they're": "they are", "I'll": "I will",
        "you'll": "you will", "he'll": "he will", "she'll": "she will",
        "we'll": "we will", "they'll": "they will", "I've": "I have",
        "you've": "you have", "we've": "we have", "they've": "they have",
        "I'd": "I would", "you'd": "you would", "he'd": "he would",
        "she'd": "she would", "we'd": "we would", "they'd": "they would",
        "it's": "it is", "that's": "that is", "there's": "there is",
        "here's": "here is", "what's": "what is", "who's": "who is",
        "where's": "where is", "when's": "when is", "why's": "why is",
        "how's": "how is"
    }
    
    result = text
    for contraction, expansion in contractions.items():
        pattern = r'\b' + re.escape(contraction) + r'\b'
        result = re.sub(pattern, expansion, result, flags=re.IGNORECASE)
    
    return result

def add_academic_transitions(text):
    """Add academic transitions to text"""
    transitions = [
        "Moreover,", "Additionally,", "Furthermore,", "Hence,", 
        "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,"
    ]
    
    sentences = text.split('. ')
    if len(sentences) > 1:
        # Add transition to some sentences
        for i in range(1, len(sentences)):
            if random.random() < 0.3:  # 30% chance
                transition = random.choice(transitions)
                sentences[i] = f"{transition} {sentences[i]}"
    
    return '. '.join(sentences)

def convert_to_passive(text):
    """Convert some sentences to passive voice"""
    sentences = text.split('. ')
    passive_sentences = []
    
    for sentence in sentences:
        if random.random() < 0.2:  # 20% chance
            # Simple passive conversion examples
            sentence = sentence.replace("I do", "It is done by me")
            sentence = sentence.replace("we can", "it can be done by us")
            sentence = sentence.replace("you should", "it should be done by you")
            sentence = sentence.replace("they will", "it will be done by them")
        
        passive_sentences.append(sentence)
    
    return '. '.join(passive_sentences)

def replace_with_synonyms(text):
    """Replace common words with more formal synonyms"""
    synonyms = {
        "good": "excellent", "bad": "poor", "big": "significant", "small": "minimal",
        "important": "crucial", "easy": "straightforward", "hard": "challenging",
        "help": "assist", "use": "utilize", "get": "obtain", "make": "create",
        "show": "demonstrate", "tell": "inform", "ask": "inquire", "try": "attempt",
        "start": "commence", "end": "conclude", "find": "discover", "know": "understand"
    }
    
    result = text
    for word, synonym in synonyms.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        if random.random() < 0.3:  # 30% chance
            result = re.sub(pattern, synonym, result, flags=re.IGNORECASE)
    
    return result

def humanize_text(text, use_passive=False, use_synonyms=False, preserve_structure=False):
    """Main text humanization function"""
    if not text.strip():
        return text
    
    # Step 1: Expand contractions
    result = expand_contractions(text)
    
    # Step 2: Add academic transitions
    result = add_academic_transitions(result)
    
    # Step 3: Convert to passive voice (if enabled)
    if use_passive:
        result = convert_to_passive(result)
    
    # Step 4: Replace with synonyms (if enabled)
    if use_synonyms:
        result = replace_with_synonyms(result)
    
    return result

def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="AI Text Humanizer Pro",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Professional CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-color: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary-color: #64748b;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
    }
    
    .main {
        padding: 0;
        background: var(--background-color);
        font-family: 'Inter', sans-serif;
    }
    
    .header-container {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        padding: 3rem 0;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0 0 1rem 0;
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .card {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 1rem 0;
    }
    
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
    }
    
    .stTextArea > div > div > textarea {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .stats-container {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: var(--background-color);
        border-radius: var(--radius-md);
        margin: 0.5rem 0;
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0.25rem 0 0 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">✨ AI Text Humanizer Pro</h1>
        <p class="header-subtitle">Transform your text into professional, academic writing with AI-powered enhancement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2 class="card-title">📝 Enter Your Text</h2>
        </div>
        """, unsafe_allow_html=True)
        
        user_text = st.text_area(
            "Paste your text here:",
            height=200,
            placeholder="Enter the text you want to humanize...",
            help="Paste any text that needs to be transformed into formal, academic writing"
        )
        
        # Transform button
        if st.button("🚀 Transform to Academic Style", use_container_width=True):
            if user_text.strip():
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Processing steps
                status_text.text("📊 Analyzing text...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                status_text.text("🔄 Transforming text...")
                progress_bar.progress(50)
                time.sleep(0.5)
                
                # Get options from sidebar
                use_passive = st.session_state.get('use_passive', False)
                use_synonyms = st.session_state.get('use_synonyms', False)
                preserve_structure = st.session_state.get('preserve_structure', False)
                
                # Transform text
                transformed = humanize_text(
                    user_text,
                    use_passive=use_passive,
                    use_synonyms=use_synonyms,
                    preserve_structure=preserve_structure
                )
                
                progress_bar.progress(75)
                status_text.text("✨ Finalizing output...")
                time.sleep(0.5)
                
                progress_bar.progress(100)
                status_text.text("✅ Transformation complete!")
                
                # Clear progress
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                # Output section
                st.markdown("""
                <div class="card">
                    <h2 class="card-title">✨ Transformed Text</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Display transformed text
                st.text_area(
                    "Humanized Text:",
                    value=transformed,
                    height=300,
                    key="transformed_output",
                    help="Your transformed text is ready!"
                )
                
                # Copy button
                if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_btn"):
                    st.success("✅ Text ready to copy! Use Ctrl+A to select all text, then Ctrl+C to copy.")
                
                # Statistics
                input_words = len(user_text.split())
                output_words = len(transformed.split())
                input_sentences = len([s for s in user_text.split('.') if s.strip()])
                output_sentences = len([s for s in transformed.split('.') if s.strip()])
                
                st.markdown(f"""
                <div class="stats-container">
                    <h3 style="font-family: 'Inter', sans-serif; font-size: 1.125rem; font-weight: 600; color: var(--text-primary); margin: 0 0 1rem 0; text-align: center;">📊 Transformation Statistics</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div class="stat-item">
                            <div class="stat-number">{input_words}</div>
                            <div class="stat-label">Input Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{input_sentences}</div>
                            <div class="stat-label">Input Sentences</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{output_words}</div>
                            <div class="stat-label">Output Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{output_sentences}</div>
                            <div class="stat-label">Output Sentences</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.warning("⚠️ Please enter some text to transform.")
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 class="card-title">⚙️ Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        use_passive = st.checkbox(
            "🔄 Passive Voice Conversion",
            value=False,
            help="Convert active voice sentences to passive voice"
        )
        st.session_state.use_passive = use_passive
        
        use_synonyms = st.checkbox(
            "📚 Synonym Replacement",
            value=False,
            help="Replace common words with sophisticated alternatives"
        )
        st.session_state.use_synonyms = use_synonyms
        
        preserve_structure = st.checkbox(
            "📋 Preserve Structure",
            value=False,
            help="Maintain original formatting"
        )
        st.session_state.preserve_structure = preserve_structure
        
        st.markdown("---")
        
        st.markdown("""
        <div class="card">
            <h3 class="card-title">ℹ️ About</h3>
            <p style="font-family: 'Inter', sans-serif; color: var(--text-secondary); line-height: 1.6;">
                This AI-powered tool transforms your text into professional, academic writing by:
            </p>
            <ul style="font-family: 'Inter', sans-serif; color: var(--text-secondary); line-height: 1.6;">
                <li>Expanding contractions (don't → do not)</li>
                <li>Adding academic transitions</li>
                <li>Converting to passive voice (optional)</li>
                <li>Replacing with synonyms (optional)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: var(--text-secondary); font-family: 'Inter', sans-serif; padding: 2rem; margin-top: 3rem;">
        <p>✨ <strong>AI Text Humanizer Pro</strong> - Professional text transformation</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
