import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import time
import traceback

def main():
    """
    AI Text Humanizer Pro - Full-featured version with advanced Python libraries
    """
    # Download NLTK resources if needed
    try:
        download_nltk_resources()
        nltk_available = True
    except Exception as e:
        st.warning(f"⚠️ NLTK resources not available: {e}")
        nltk_available = False

    # Configure Streamlit page
    st.set_page_config(
        page_title="AI Text Humanizer Pro",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': "https://github.com/DadaNanjesha/AI-Text-Humanizer-App/issues",
            'Report a bug': "https://github.com/DadaNanjesha/AI-Text-Humanizer-App/issues",
            'About': "# AI Text Humanizer Pro - Full Python Libraries"
        }
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
        <p class="subtitle">Transform AI-generated text into natural, human-like writing with advanced Python libraries</p>
    </div>
    """, unsafe_allow_html=True)

    # Features Section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Advanced NLP Processing</div>
            <div class="feature-desc">Uses spaCy, NLTK, and sentence transformers for sophisticated text analysis</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Synonym Replacement</div>
            <div class="feature-desc">AI-powered synonym selection using semantic similarity</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Passive Voice Conversion</div>
            <div class="feature-desc">Automatically converts active voice to passive where appropriate</div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Options
    with st.sidebar:
        st.markdown("### ⚙️ Transformation Settings")

        # Advanced options
        use_passive = st.checkbox("🔄 Enable Passive Voice", value=False,
                                help="Convert active voice to passive voice where appropriate")
        use_synonyms = st.checkbox("🔍 Enable Synonym Replacement", value=True,
                                 help="Replace words with more sophisticated alternatives using AI")
        preserve_structure = st.checkbox("📄 Preserve Structure", value=False,
                                       help="Maintain headings and paragraph formatting")

        # Intensity slider
        intensity = st.select_slider(
            "Transformation Intensity",
            options=["Light", "Medium", "Heavy", "Very Heavy"],
            value="Medium",
            help="Controls the strength of transformations applied"
        )

        st.markdown("---")
        st.markdown("### 📊 System Status")
        if nltk_available:
            st.success("✅ Full Python libraries loaded")
        else:
            st.warning("⚠️ Using basic features only")

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
        help="Enter the text you want to humanize with advanced AI processing"
    )

    # File upload
    uploaded_file = st.file_uploader(
        "📁 Or upload a .txt file:",
        type=["txt"],
        help="Upload a text file to humanize its content with full Python libraries"
    )

    if uploaded_file is not None:
        try:
            file_text = uploaded_file.read().decode("utf-8", errors="ignore")
            user_text = file_text
            st.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")

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
                status_text.text("🔄 Analyzing text with spaCy...")
                progress_bar.progress(25)
                time.sleep(0.5)

                status_text.text("🧠 Processing with AI models...")
                progress_bar.progress(50)
                time.sleep(0.5)

                status_text.text("✨ Applying transformations...")
                progress_bar.progress(75)
                time.sleep(0.5)

                status_text.text("🎯 Finalizing humanization...")
                progress_bar.progress(100)
                time.sleep(0.5)

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                try:
                    # Count words and sentences
                    if nltk_available:
                        input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                        doc_input = NLP_GLOBAL(user_text)
                        input_sentence_count = len(list(doc_input.sents))
                    else:
                        input_word_count = len(user_text.split())
                        input_sentence_count = len(user_text.split('.'))

                    # Transform text with advanced features
                    intensity_key = intensity.lower().replace(" ", "_")
                    humanizer = AcademicTextHumanizer(
                        p_passive=0.45 if intensity == "Very Heavy" else 0.4 if intensity == "Heavy" else 0.3 if intensity == "Medium" else 0.2,
                        p_synonym_replacement=0.5 if intensity == "Very Heavy" else 0.4 if intensity == "Heavy" else 0.3 if intensity == "Medium" else 0.2,
                        p_academic_transition=0.6 if intensity == "Very Heavy" else 0.5 if intensity == "Heavy" else 0.4 if intensity == "Medium" else 0.3
                    )

                    transformed = humanizer.humanize_text(
                        user_text,
                        use_passive=use_passive,
                        use_synonyms=use_synonyms,
                        preserve_structure=preserve_structure,
                        intensity=intensity_key,
                        style="academic"
                    )

                    # Output statistics
                    if nltk_available:
                        output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                        doc_output = NLP_GLOBAL(transformed)
                        output_sentence_count = len(list(doc_output.sents))
                    else:
                        output_word_count = len(transformed.split())
                        output_sentence_count = len(transformed.split('.'))

                    # Store stats in session state
                    st.session_state.last_transformation = {
                        'input_words': input_word_count,
                        'output_words': output_word_count
                    }

                    # Display results
                    st.markdown('<div class="output-section">', unsafe_allow_html=True)
                    st.markdown("### ✨ Humanized Text")

                    st.text_area(
                        "Your humanized text (with advanced AI processing):",
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

                    # Advanced Statistics
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
                        <div class="stat-item">
                            <div class="stat-number">{}</div>
                            <div class="stat-label">Input Sentences</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{}</div>
                            <div class="stat-label">Output Sentences</div>
                        </div>
                    </div>
                    """.format(input_word_count, output_word_count, output_word_count - input_word_count,
                             input_sentence_count, output_sentence_count), unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # Show transformation settings used
                    with st.expander("🔧 Transformation Details"):
                        st.write(f"**Passive Voice:** {'Enabled' if use_passive else 'Disabled'}")
                        st.write(f"**Synonym Replacement:** {'Enabled' if use_synonyms else 'Disabled'}")
                        st.write(f"**Structure Preservation:** {'Enabled' if preserve_structure else 'Disabled'}")
                        st.write(f"**Intensity Level:** {intensity}")

                except Exception as e:
                    st.error(f"❌ Error during transformation: {e}")
                    st.error("Please check that all Python libraries are properly installed.")
                    if st.button("🔧 Try Simple Mode"):
                        st.switch_page("simple_humanizer.py")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-family: 'Inter', sans-serif; padding: 2rem;">
        <p>✨ <strong>AI Text Humanizer Pro</strong> - Advanced AI-powered text transformation</p>
        <p>Powered by spaCy, NLTK, and sentence-transformers</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
