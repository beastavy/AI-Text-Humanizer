#!/usr/bin/env python3
"""
Simple AI Text Humanizer - No external dependencies
"""

import streamlit as st
import re
import random
import time

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
        for i in range(1, len(sentences)):
            if random.random() < 0.3:
                transition = random.choice(transitions)
                sentences[i] = f"{transition} {sentences[i]}"
    
    return '. '.join(sentences)

def convert_to_passive(text):
    """Convert some sentences to passive voice"""
    sentences = text.split('. ')
    passive_sentences = []
    
    for sentence in sentences:
        if random.random() < 0.2:
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
        if random.random() < 0.3:
            result = re.sub(pattern, synonym, result, flags=re.IGNORECASE)
    
    return result

def humanize_text(text, use_passive=False, use_synonyms=False):
    """Main text humanization function"""
    if not text.strip():
        return text
    
    result = expand_contractions(text)
    result = add_academic_transitions(result)
    
    if use_passive:
        result = convert_to_passive(result)
    
    if use_synonyms:
        result = replace_with_synonyms(result)
    
    return result

def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="AI Text Humanizer",
        page_icon="✨",
        layout="wide"
    )
    
    # Simple CSS
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        font-size: 3rem;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>✨ AI Text Humanizer</h1>
        <p>Transform your text into professional, academic writing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📝 Enter Your Text")
        
        user_text = st.text_area(
            "Paste your text here:",
            height=200,
            placeholder="Enter the text you want to humanize...",
            help="Paste any text that needs to be transformed into formal, academic writing"
        )
        
        if st.button("🚀 Transform Text", use_container_width=True):
            if user_text.strip():
                with st.spinner("Transforming your text..."):
                    time.sleep(1)
                    
                    use_passive = st.session_state.get('use_passive', False)
                    use_synonyms = st.session_state.get('use_synonyms', False)
                    
                    transformed = humanize_text(
                        user_text,
                        use_passive=use_passive,
                        use_synonyms=use_synonyms
                    )
                    
                    st.markdown("### ✨ Transformed Text")
                    st.text_area(
                        "Humanized Text:",
                        value=transformed,
                        height=300,
                        key="transformed_output"
                    )
                    
                    if st.button("📋 Copy Text", use_container_width=True):
                        st.success("✅ Text ready to copy! Use Ctrl+A to select all, then Ctrl+C to copy.")
                    
                    # Simple stats
                    input_words = len(user_text.split())
                    output_words = len(transformed.split())
                    
                    st.markdown(f"""
                    **📊 Statistics:**
                    - Input Words: {input_words}
                    - Output Words: {output_words}
                    """)
            else:
                st.warning("⚠️ Please enter some text to transform.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Options")
        
        use_passive = st.checkbox("🔄 Passive Voice", value=False)
        st.session_state.use_passive = use_passive
        
        use_synonyms = st.checkbox("📚 Synonyms", value=False)
        st.session_state.use_synonyms = use_synonyms
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This tool transforms your text by:
        - Expanding contractions
        - Adding academic transitions
        - Converting to passive voice (optional)
        - Replacing with synonyms (optional)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: white; margin-top: 3rem;">
        <p>✨ AI Text Humanizer - Professional text transformation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
