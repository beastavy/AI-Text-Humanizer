import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import time
import random

def main():
    """
    Professional Enterprise-Grade AI Text Humanizer
    """
    # Download NLTK resources if needed
    download_nltk_resources()
    
    # Page config
    st.set_page_config(
        page_title="TextHumanizer Pro",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Professional Enterprise CSS
    st.markdown("""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* CSS Variables for Professional Theme */
    :root {
        --primary-color: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary-color: #64748b;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
    }
    
    /* Global Reset and Base Styles */
    .main {
        padding: 0;
        background: var(--background-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional Header */
    .header-container {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        padding: 3rem 0;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
        text-align: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0 0 1rem 0;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0 0 2rem 0;
        font-weight: 400;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .header-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-lg);
        padding: 0.5rem 1rem;
        color: white;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Professional Navigation */
    .nav-container {
        background: var(--surface-color);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 0;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-sm);
    }
    
    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .nav-brand {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        text-decoration: none;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    .nav-link:hover {
        color: var(--primary-color);
    }
    
    /* Professional Cards */
    .card {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        overflow: hidden;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--primary-color);
    }
    
    .card-header {
        padding: 1.5rem 1.5rem 0 1.5rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .card-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0;
        line-height: 1.5;
    }
    
    .card-body {
        padding: 0 1.5rem 1.5rem 1.5rem;
    }
    
    /* Feature Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .feature-icon {
        width: 4rem;
        height: 4rem;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        border-radius: var(--radius-lg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem auto;
        font-size: 1.5rem;
        color: white;
    }
    
    .feature-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.75rem 0;
    }
    
    .feature-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Professional Buttons */
    .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: var(--radius-md);
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        text-decoration: none;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .btn-primary {
        background: var(--primary-color);
        color: white;
        box-shadow: var(--shadow-sm);
    }
    
    .btn-primary:hover {
        background: var(--primary-dark);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .btn-secondary {
        background: var(--surface-color);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    .btn-secondary:hover {
        background: var(--background-color);
        border-color: var(--primary-color);
    }
    
    .btn-success {
        background: var(--success-color);
        color: white;
    }
    
    .btn-success:hover {
        background: #059669;
        transform: translateY(-1px);
    }
    
    /* Professional Form Elements */
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .form-control {
        width: 100%;
        padding: 0.75rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        background: var(--surface-color);
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    
    .form-control:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .form-control::placeholder {
        color: var(--text-secondary);
    }
    
    /* Professional Text Areas */
    .stTextArea > div > div > textarea {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        background: var(--surface-color);
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-primary);
        transition: all 0.2s ease;
        padding: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-secondary);
    }
    
    /* Professional Checkboxes */
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
        font-size: 0.875rem;
    }
    
    /* Professional Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        border-radius: var(--radius-sm);
    }
    
    /* Professional Alerts */
    .alert {
        padding: 1rem 1.5rem;
        border-radius: var(--radius-md);
        border: 1px solid;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        margin: 1rem 0;
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border-color: var(--success-color);
        color: #065f46;
    }
    
    .alert-info {
        background: rgba(6, 182, 212, 0.1);
        border-color: var(--accent-color);
        color: #155e75;
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border-color: var(--warning-color);
        color: #92400e;
    }
    
    /* Professional Stats */
    .stats-container {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1.5rem;
        background: var(--background-color);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0 0 0.5rem 0;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        margin: 0;
    }
    
    /* Professional Sidebar */
    .sidebar .sidebar-content {
        background: var(--surface-color);
        border-right: 1px solid var(--border-color);
    }
    
    /* Professional Footer */
    .footer {
        background: var(--text-primary);
        color: white;
        padding: 3rem 0;
        margin-top: 4rem;
        text-align: center;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .footer-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
    }
    
    .footer-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.7);
        margin: 0 0 2rem 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-link {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    .footer-link:hover {
        color: white;
    }
    
    .footer-copyright {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        margin: 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .nav-content {
            flex-direction: column;
            gap: 1rem;
        }
        
        .nav-links {
            gap: 1rem;
        }
    }
    
    /* Professional Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Professional Loading States */
    .loading-spinner {
        display: inline-block;
        width: 1rem;
        height: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional Header
    st.markdown("""
    <div class="header-container">
        <div class="header-content">
            <div class="header-badge">
                🎯 Enterprise-Grade AI Solution
            </div>
            <h1 class="header-title">TextHumanizer Pro</h1>
            <p class="header-subtitle">Transform your content into professional, academic writing with advanced AI-powered text enhancement technology</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Navigation
    st.markdown("""
    <div class="nav-container">
        <div class="nav-content">
            <div class="nav-brand">TextHumanizer Pro</div>
            <div class="nav-links">
                <a href="#" class="nav-link">Features</a>
                <a href="#" class="nav-link">Documentation</a>
                <a href="#" class="nav-link">Support</a>
                <a href="#" class="nav-link">Enterprise</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content Container
    main_container = st.container()
    
    with main_container:
        # Feature Cards
        st.markdown("""
        <div class="features-grid">
            <div class="feature-card animate-fade-in-up">
                <div class="feature-icon">📝</div>
                <h3 class="feature-title">Smart Contraction Expansion</h3>
                <p class="feature-description">Intelligently converts informal contractions to formal academic language while preserving proper nouns and context.</p>
            </div>
            <div class="feature-card animate-fade-in-up">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title">Academic Transitions</h3>
                <p class="feature-description">Enhances text flow with professional transitional phrases and academic connectors for improved readability.</p>
            </div>
            <div class="feature-card animate-fade-in-up">
                <div class="feature-icon">🔄</div>
                <h3 class="feature-title">Advanced Transformations</h3>
                <p class="feature-description">Sophisticated passive voice conversion and intelligent synonym replacement for professional tone.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Content Grid
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Input Section
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Text Input</h2>
                    <p class="card-description">Enter your text below to begin the professional transformation process</p>
                </div>
                <div class="card-body">
            """, unsafe_allow_html=True)
            
            user_text = st.text_area(
                "Enter your text:",
                height=200,
                placeholder="Paste your text here for professional enhancement...",
                help="Input any text that requires formal, academic transformation"
            )
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Transform Button
            if st.button("🚀 Transform Text", use_container_width=True):
                if user_text.strip():
                    # Professional progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Processing steps
                    steps = [
                        "📊 Analyzing text structure...",
                        "🔄 Applying transformations...",
                        "✨ Optimizing output...",
                        "✅ Finalizing results..."
                    ]
                    
                    for i, step in enumerate(steps):
                        status_text.markdown(f'<div class="loading-spinner"></div> {step}')
                        progress_bar.progress((i + 1) * 25)
                        time.sleep(0.3)
                    
                    # Calculate stats
                    input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                    doc_input = NLP_GLOBAL(user_text)
                    input_sentence_count = len(list(doc_input.sents))
                    
                    # Transform text
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
                    
                    # Calculate output stats
                    output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                    doc_output = NLP_GLOBAL(transformed)
                    output_sentence_count = len(list(doc_output.sents))
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Output Section
                    st.markdown("""
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title">Transformed Output</h2>
                            <p class="card-description">Your professionally enhanced text is ready</p>
                        </div>
                        <div class="card-body">
                    """, unsafe_allow_html=True)
                    
                    # Display transformed text
                    st.text_area(
                        "Enhanced Text:",
                        value=transformed,
                        height=300,
                        key="transformed_output",
                        help="Your professionally transformed text"
                    )
                    
                    # Copy Button
                    if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_btn"):
                        st.success("✅ Text copied! Use Ctrl+A to select all text, then Ctrl+C to copy.")
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
                    
                    # Statistics
                    st.markdown(f"""
                    <div class="stats-container">
                        <h3 style="font-family: 'Inter', sans-serif; font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin: 0 0 1.5rem 0; text-align: center;">Transformation Statistics</h3>
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
                    st.info(f"🔧 **Configuration:** Passive Voice: {use_passive} | Synonym Replacement: {use_synonyms} | Structure Preservation: {preserve_structure}")
                    
                else:
                    st.warning("⚠️ Please enter some text to transform.")
        
        with col2:
            # Configuration Panel
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Configuration</h3>
                    <p class="card-description">Customize your transformation settings</p>
                </div>
                <div class="card-body">
            """, unsafe_allow_html=True)
            
            use_passive = st.checkbox(
                "🔄 Passive Voice Conversion",
                value=False,
                help="Convert active voice sentences to passive voice for formal tone"
            )
            
            use_synonyms = st.checkbox(
                "📚 Synonym Replacement",
                value=False,
                help="Replace common words with sophisticated alternatives"
            )
            
            preserve_structure = st.checkbox(
                "📋 Preserve Structure",
                value=False,
                help="Maintain original formatting and paragraph structure"
            )
            
            st.markdown("---")
            
            # Additional Options
            st.markdown("""
            <h4 style="font-family: 'Inter', sans-serif; font-size: 1rem; font-weight: 600; color: var(--text-primary); margin: 0 0 1rem 0;">Advanced Options</h4>
            """, unsafe_allow_html=True)
            
            st.selectbox(
                "Transformation Intensity:",
                ["Light", "Medium", "Heavy"],
                index=1,
                help="Control the level of text transformation"
            )
            
            st.selectbox(
                "Output Style:",
                ["Academic", "Professional", "Formal"],
                index=0,
                help="Choose the desired output writing style"
            )
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Quick Actions
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Quick Actions</h3>
                </div>
                <div class="card-body">
            """, unsafe_allow_html=True)
            
            if st.button("📄 Load Sample Text", use_container_width=True):
                sample_text = """
                I don't think this approach will work. It's not good enough for our needs. 
                We can't implement it without proper planning. The team needs to understand 
                the requirements better before we proceed.
                """
                st.session_state.sample_text = sample_text
                st.rerun()
            
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.clear_all = True
                st.rerun()
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Professional Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <h3 class="footer-title">TextHumanizer Pro</h3>
            <p class="footer-description">Enterprise-grade AI text enhancement platform for professional content transformation</p>
            <div class="footer-links">
                <a href="#" class="footer-link">Documentation</a>
                <a href="#" class="footer-link">API Reference</a>
                <a href="#" class="footer-link">Support</a>
                <a href="#" class="footer-link">Enterprise</a>
            </div>
            <p class="footer-copyright">© 2024 TextHumanizer Pro. All rights reserved.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
