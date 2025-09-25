import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import time

def main():
    """
    Modern AI Text Humanizer with beautiful UI
    """
    # Download NLTK resources if needed
    download_nltk_resources()
    
    # Page config
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
    
    /* Header Styles */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin: 1rem 0 0 0;
        font-weight: 300;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #f0f0f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-family: 'Inter', sans-serif;
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* Input/Output Areas */
    .input-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .output-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Copy Button */
    .copy-button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3) !important;
    }
    
    .copy-button:hover {
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
    }
    
    /* Stats Box */
    .stats-container {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.1);
    }
    
    .stats-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #2e7d32;
        margin-bottom: 1rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2e7d32;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #4CAF50;
        margin-top: 0.5rem;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #2c3e50;
    }
    
    /* Text Areas */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #4CAF50;
        border-radius: 10px;
    }
    
    /* Info Messages */
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 1px solid #17a2b8;
        border-radius: 10px;
    }
    
    /* Custom Copy Button */
    .copy-btn {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        width: 100%;
    }
    
    .copy-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modern Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">✨ AI Text Humanizer Pro</h1>
        <p class="header-subtitle">Transform your text into professional, academic writing with AI-powered enhancement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Smart Contraction Expansion</div>
            <div class="feature-desc">Automatically converts contractions like "don't" to "do not" for formal writing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Academic Transitions</div>
            <div class="feature-desc">Adds professional transitions like "Moreover," "Therefore," for better flow</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Advanced Transformations</div>
            <div class="feature-desc">Passive voice conversion and intelligent synonym replacement</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content
    st.markdown("---")
    
    # Sidebar for options
    with st.sidebar:
        st.markdown("### ⚙️ Transformation Options")
        
        use_passive = st.checkbox(
            "🔄 Enable Passive Voice", 
            value=False,
            help="Convert active voice sentences to passive voice for more formal tone"
        )
        
        use_synonyms = st.checkbox(
            "📚 Enable Synonym Replacement", 
            value=False,
            help="Replace common words with more sophisticated alternatives"
        )
        
        preserve_structure = st.checkbox(
            "📋 Preserve Structure", 
            value=False,
            help="Keep original formatting with headings and paragraphs"
        )
        
        st.markdown("---")
        st.markdown("### 📊 About This App")
        st.markdown("""
        This AI-powered tool transforms your text into professional, academic writing by:
        
        • **Expanding contractions** (don't → do not)
        • **Adding transitions** (Moreover, Therefore, etc.)
        • **Converting to passive voice** (optional)
        • **Replacing with synonyms** (optional)
        • **Preserving structure** (optional)
        """)
    
    # Input Section
    st.markdown("""
    <div class="input-section">
        <h2 style="color: #2c3e50; font-family: 'Inter', sans-serif; margin-bottom: 1rem;">📝 Enter Your Text</h2>
    </div>
    """, unsafe_allow_html=True)
    
    user_text = st.text_area(
        "Paste your text here:",
        height=200,
        placeholder="Enter the text you want to humanize...",
        help="Paste any text that needs to be transformed into formal, academic writing"
    )
    
    # Transform Button
    if st.button("🚀 Transform to Academic Style", use_container_width=True):
        if user_text.strip():
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Input stats
            status_text.text("📊 Analyzing input text...")
            progress_bar.progress(25)
            
            input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
            doc_input = NLP_GLOBAL(user_text)
            input_sentence_count = len(list(doc_input.sents))
            
            # Transform
            status_text.text("🔄 Transforming text...")
            progress_bar.progress(50)
            
            humanizer = AcademicTextHumanizer(
                p_passive=0.3,
                p_synonym_replacement=0.3,
                p_academic_transition=0.4
            )
            
            transformed = humanizer.humanize_text(
                user_text,
                use_passive=use_passive,
                use_synonyms=use_synonyms,
                preserve_structure=preserve_structure
            )
            
            progress_bar.progress(75)
            status_text.text("✨ Finalizing output...")
            
            # Output stats
            output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
            doc_output = NLP_GLOBAL(transformed)
            output_sentence_count = len(list(doc_output.sents))
            
            progress_bar.progress(100)
            status_text.text("✅ Transformation complete!")
            
            # Clear progress
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            # Output Section
            st.markdown("""
            <div class="output-section">
                <h2 style="color: #2c3e50; font-family: 'Inter', sans-serif; margin-bottom: 1rem;">✨ Transformed Text</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Display transformed text
            st.text_area(
                "Humanized Text:",
                value=transformed,
                height=300,
                key="transformed_output",
                help="Your transformed text is ready! Use Ctrl+A to select all, then Ctrl+C to copy."
            )
            
            # Copy Button (Fixed - won't cause text to vanish)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_btn"):
                    st.success("✅ **Text ready to copy!** Use Ctrl+A to select all text in the box above, then Ctrl+C to copy.")
            
            # Statistics
            st.markdown(f"""
            <div class="stats-container">
                <div class="stats-title">📊 Transformation Statistics</div>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">{input_word_count}</div>
                        <div class="stat-label">Input Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{input_sentence_count}</div>
                        <div class="stat-label">Input Sentences</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{output_word_count}</div>
                        <div class="stat-label">Output Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{output_sentence_count}</div>
                        <div class="stat-label">Output Sentences</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Debug info
            st.info(f"🔧 **Debug Info:** Passive={use_passive}, Synonyms={use_synonyms}, Structure={preserve_structure}")
            
        else:
            st.warning("⚠️ Please enter some text to transform!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-family: 'Inter', sans-serif; padding: 2rem;">
        <p>✨ <strong>AI Text Humanizer Pro</strong> - Transform your writing with AI-powered enhancement</p>
        <p>Built with ❤️ using Streamlit and advanced NLP techniques</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
