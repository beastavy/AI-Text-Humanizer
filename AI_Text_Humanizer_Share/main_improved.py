import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import time
import random

def main():
    """
    Enhanced AI Text Humanizer with Improved UI/UX
    """
    # Download NLTK resources if needed
    download_nltk_resources()
    
    # Page config
    st.set_page_config(
        page_title="AI Text Humanizer Pro",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced Modern CSS
    st.markdown("""
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');
    
    /* CSS Variables */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #8b5cf6;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border: #e2e8f0;
        --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.1);
        --radius: 0.75rem;
    }
    
    /* Global Styles */
    .main {
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Header */
    .header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--radius);
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
    }
    
    .header h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin: 0;
    }
    
    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--radius);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
    }
    
    /* Input/Output Areas */
    .stTextArea > div > div > textarea {
        border-radius: var(--radius);
        border: 2px solid var(--border);
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 0.75rem 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    /* Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: var(--radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }
    
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0;
    }
    
    .metric-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin: 0;
        margin-top: 0.5rem;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, var(--success), #059669);
        color: white;
        padding: 1rem 2rem;
        border-radius: var(--radius);
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header h1 {
            font-size: 2rem;
        }
        
        .card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🤖 AI Text Humanizer Pro</h1>
        <p>Transform AI-generated text into natural, human-like content with advanced NLP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'transformed_text' not in st.session_state:
        st.session_state.transformed_text = ""
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📝 Input Text")
        
        # Text input
        input_text = st.text_area(
            "Enter your text to humanize:",
            height=300,
            placeholder="Paste your AI-generated text here...",
            key="input_text"
        )
        
        # Options
        st.markdown("### ⚙️ Transformation Options")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            enable_passive = st.checkbox("🔄 Passive Voice", value=True, help="Convert active voice to passive voice")
            enable_synonyms = st.checkbox("📚 Synonym Replacement", value=True, help="Replace words with sophisticated synonyms")
        
        with col_opt2:
            preserve_structure = st.checkbox("📋 Preserve Structure", value=False, help="Maintain original formatting (headings, paragraphs)")
        
        # Transform button
        if st.button("🚀 Transform Text", type="primary", use_container_width=True):
            if input_text.strip():
                st.session_state.processing = True
                
                # Show loading
                with st.spinner("🔄 Processing your text..."):
                    try:
                        # Initialize humanizer
                        humanizer = AcademicTextHumanizer()
                        
                        # Transform text
                        transformed = humanizer.humanize_text(
                            input_text,
                            enable_passive_voice=enable_passive,
                            enable_synonym_replacement=enable_synonyms,
                            preserve_structure=preserve_structure
                        )
                        
                        st.session_state.transformed_text = transformed
                        st.session_state.processing = False
                        
                        # Success message
                        st.markdown('<div class="success-message">✅ Text transformed successfully!</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.session_state.processing = False
            else:
                st.warning("⚠️ Please enter some text to transform.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ✨ Transformed Text")
        
        # Output text
        if st.session_state.transformed_text:
            st.text_area(
                "Humanized text:",
                value=st.session_state.transformed_text,
                height=300,
                key="output_text"
            )
            
            # Copy button
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.write("💡 **Tip:** Select all text (Ctrl+A) and copy (Ctrl+C) to copy to clipboard")
        else:
            st.text_area(
                "Humanized text will appear here...",
                value="",
                height=300,
                disabled=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    if st.session_state.transformed_text and input_text:
        st.markdown("### 📊 Transformation Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{}</p>
                <p class="metric-label">Words Transformed</p>
            </div>
            """.format(len(word_tokenize(st.session_state.transformed_text))), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{}</p>
                <p class="metric-label">Original Words</p>
            </div>
            """.format(len(word_tokenize(input_text))), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{:.1f}%</p>
                <p class="metric-label">Transformation Rate</p>
            </div>
            """.format((len(word_tokenize(st.session_state.transformed_text)) / len(word_tokenize(input_text))) * 100), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{}</p>
                <p class="metric-label">Characters</p>
            </div>
            """.format(len(st.session_state.transformed_text)), unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: var(--text-secondary); font-family: 'Poppins', sans-serif;">
        <p>🤖 AI Text Humanizer Pro - Powered by Advanced NLP</p>
        <p>Transform AI text into natural, human-like content</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
