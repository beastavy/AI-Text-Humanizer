import streamlit as st
import re
import random
import time
from datetime import datetime

def expand_contractions(text):
    """Expand common contractions"""
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
    """Add academic transitions between sentences"""
    transitions = [
        "Moreover,", "Additionally,", "Furthermore,", "Hence,", 
        "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,",
        "In addition,", "Furthermore,", "Moreover,", "Additionally,",
        "As a result,", "For this reason,", "In contrast,", "On the other hand,"
    ]
    
    sentences = text.split('. ')
    if len(sentences) > 1:
        for i in range(1, len(sentences)):
            if random.random() < 0.3:  # 30% chance to add transition
                transition = random.choice(transitions)
                sentences[i] = f"{transition} {sentences[i]}"
        return '. '.join(sentences)
    
    return text

def improve_sentence_structure(text):
    """Improve sentence structure and flow"""
    # Add variety to sentence beginnings
    sentences = text.split('. ')
    improved_sentences = []
    
    for i, sentence in enumerate(sentences):
        if i > 0 and sentence.strip():
            # Sometimes start with a transition or connector
            if random.random() < 0.2:
                connectors = ["This", "Such", "These", "That", "It"]
                if not sentence.startswith(tuple(connectors)):
                    sentence = f"{random.choice(connectors)} {sentence.lower()}"
        
        improved_sentences.append(sentence)
    
    return '. '.join(improved_sentences)

def humanize_text(text, use_transitions=True, use_structure=True):
    """Enhanced text humanization"""
    result = text
    
    # Expand contractions
    result = expand_contractions(result)
    
    # Add academic transitions
    if use_transitions:
        result = add_academic_transitions(result)
    
    # Improve sentence structure
    if use_structure:
        result = improve_sentence_structure(result)
    
    return result

def main():
    st.set_page_config(
        page_title="AI Text Humanizer Pro",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Modern CSS Styling
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 2rem;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 1rem;
        font-weight: 300;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-family: 'Inter', sans-serif;
        color: #7f8c8d;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Input/Output Areas */
    .input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px dashed #dee2e6;
    }
    
    .output-section {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid #4CAF50;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Statistics */
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #4CAF50;
    }
    
    .stat-item {
        display: inline-block;
        margin-right: 2rem;
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #4CAF50;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Text Areas */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #2c3e50;
    }
    
    /* File Uploader */
    .stFileUploader > div {
        border-radius: 10px;
        border: 2px dashed #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success Messages */
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">✨ AI Text Humanizer Pro</h1>
        <p class="subtitle">Transform AI-generated text into natural, human-like writing with advanced algorithms</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Contraction Expansion</div>
            <div class="feature-desc">Converts contractions like "don't" to "do not" for more formal writing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Academic Transitions</div>
            <div class="feature-desc">Adds professional transitions like "Moreover" and "Furthermore"</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Structure Enhancement</div>
            <div class="feature-desc">Improves sentence flow and readability for better comprehension</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar Options
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        use_transitions = st.checkbox("🔄 Add Academic Transitions", value=True, help="Add professional transitions between sentences")
        use_structure = st.checkbox("🎯 Improve Structure", value=True, help="Enhance sentence flow and readability")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        if 'last_transformation' in st.session_state:
            stats = st.session_state.last_transformation
            st.metric("Input Words", stats['input_words'])
            st.metric("Output Words", stats['output_words'])
            st.metric("Improvement", f"+{stats['output_words'] - stats['input_words']} words")
    
    # Main Content
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📝 Enter Your Text")
    
    # Text input
    user_text = st.text_area(
        "Paste your AI-generated text here:",
        height=200,
        placeholder="Example: I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning.",
        help="Enter the text you want to humanize"
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        "📁 Or upload a .txt file:",
        type=["txt"],
        help="Upload a text file to humanize its content"
    )
    
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text
        st.success("✅ File uploaded successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Transform button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Humanize Text", type="primary", use_container_width=True):
            if not user_text.strip():
                st.warning("⚠️ Please enter some text to humanize.")
            else:
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate processing steps
                status_text.text("🔄 Analyzing text structure...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                status_text.text("📝 Expanding contractions...")
                progress_bar.progress(50)
                time.sleep(0.5)
                
                status_text.text("🔄 Adding transitions...")
                progress_bar.progress(75)
                time.sleep(0.5)
                
                status_text.text("✨ Finalizing humanization...")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Count words
                input_words = len(user_text.split())
                
                # Transform text
                transformed = humanize_text(user_text, use_transitions, use_structure)
                output_words = len(transformed.split())
                
                # Store stats in session state
                st.session_state.last_transformation = {
                    'input_words': input_words,
                    'output_words': output_words
                }
                
                # Display results
                st.markdown('<div class="output-section">', unsafe_allow_html=True)
                st.markdown("### ✨ Humanized Text")
                
                st.text_area(
                    "Your humanized text:",
                    value=transformed,
                    height=300,
                    help="Click in the text area and use Ctrl+A to select all, then Ctrl+C to copy"
                )
                
                # Copy button
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.markdown("""
                    <div class="success-message">
                        ✅ Text ready to copy! Use Ctrl+A to select all text above, then Ctrl+C to copy.
                    </div>
                    """, unsafe_allow_html=True)
                
                # Statistics
                st.markdown("""
                <div class="stats-container">
                    <div class="stat-item">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Input Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Output Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">+{}</div>
                        <div class="stat-label">Words Added</div>
                    </div>
                </div>
                """.format(input_words, output_words, output_words - input_words), unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-family: 'Inter', sans-serif; padding: 2rem;">
        <p>✨ <strong>AI Text Humanizer Pro</strong> - Making AI text more human-like since 2024</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()




