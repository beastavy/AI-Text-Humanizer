import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import time
import random

def main():
    """
    Ultra Modern AI Text Humanizer with stunning animations and UX
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
    
    # Ultra Modern CSS with Animations
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 0rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Animated Background */
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating Particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Header Styles */
    .header-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem 2rem;
        border-radius: 30px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: slideInDown 1s ease-out;
    }
    
    @keyframes slideInDown {
        from {
            transform: translateY(-100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .header-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 4px 8px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.3); }
        to { text-shadow: 0 4px 8px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.6); }
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        margin: 1rem 0 0 0;
        font-weight: 300;
        animation: fadeInUp 1s ease-out 0.5s both;
    }
    
    @keyframes fadeInUp {
        from {
            transform: translateY(30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Feature Cards with Hover Effects */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: slideInUp 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .feature-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.8rem;
    }
    
    .feature-desc {
        font-family: 'Inter', sans-serif;
        color: rgba(255,255,255,0.8);
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Input/Output Sections */
    .input-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        animation: slideInLeft 1s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .output-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        animation: slideInRight 1s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Buttons with Advanced Animations */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Copy Button Special Styling */
    .copy-button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3) !important;
    }
    
    .copy-button:hover {
        box-shadow: 0 15px 35px rgba(76, 175, 80, 0.4) !important;
    }
    
    /* Stats Container with Glass Effect */
    .stats-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: slideInUp 1s ease-out;
    }
    
    .stats-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    .stat-item:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.2);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stat-number {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Checkboxes with Custom Styling */
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: white;
        font-size: 1rem;
    }
    
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Text Areas with Glass Effect */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Progress Bar with Animation */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        animation: progressGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes progressGlow {
        from { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        to { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    
    /* Success Messages with Animation */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 15px;
        animation: slideInDown 0.5s ease-out;
    }
    
    /* Info Messages with Animation */
    .stInfo {
        background: rgba(33, 150, 243, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(33, 150, 243, 0.3);
        border-radius: 15px;
        animation: slideInDown 0.5s ease-out;
    }
    
    /* Warning Messages with Animation */
    .stWarning {
        background: rgba(255, 152, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 152, 0, 0.3);
        border-radius: 15px;
        animation: slideInDown 0.5s ease-out;
    }
    
    /* Section Titles */
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.7);
        font-family: 'Inter', sans-serif;
        padding: 3rem 2rem;
        margin-top: 3rem;
        animation: fadeInUp 1s ease-out 1s both;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr 1fr;
        }
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
    </style>
    """, unsafe_allow_html=True)
    
    # Add animated background and particles
    st.markdown("""
    <div class="animated-bg"></div>
    <div class="particles" id="particles"></div>
    <script>
    // Create floating particles
    function createParticles() {
        const particlesContainer = document.getElementById('particles');
        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.width = Math.random() * 4 + 2 + 'px';
            particle.style.height = particle.style.width;
            particle.style.animationDelay = Math.random() * 20 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
            particlesContainer.appendChild(particle);
        }
    }
    
    // Initialize particles when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createParticles);
    } else {
        createParticles();
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Ultra Modern Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">✨ AI Text Humanizer Pro</h1>
        <p class="header-subtitle">Transform your text into professional, academic writing with AI-powered enhancement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards with Staggered Animation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.1s;">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Smart Contraction Expansion</div>
            <div class="feature-desc">Automatically converts contractions like "don't" to "do not" for formal writing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.2s;">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Academic Transitions</div>
            <div class="feature-desc">Adds professional transitions like "Moreover," "Therefore," for better flow</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.3s;">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Advanced Transformations</div>
            <div class="feature-desc">Passive voice conversion and intelligent synonym replacement</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content
    st.markdown("---")
    
    # Sidebar for options with enhanced styling
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
        <h2 class="section-title">📝 Enter Your Text</h2>
    </div>
    """, unsafe_allow_html=True)
    
    user_text = st.text_area(
        "Paste your text here:",
        height=200,
        placeholder="Enter the text you want to humanize...",
        help="Paste any text that needs to be transformed into formal, academic writing"
    )
    
    # Transform Button with Enhanced Animation
    if st.button("🚀 Transform to Academic Style", use_container_width=True):
        if user_text.strip():
            # Show animated progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Input stats with animation
            status_text.markdown('<div class="loading"></div> 📊 Analyzing input text...')
            progress_bar.progress(25)
            time.sleep(0.5)
            
            input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
            doc_input = NLP_GLOBAL(user_text)
            input_sentence_count = len(list(doc_input.sents))
            
            # Transform with animation
            status_text.markdown('<div class="loading"></div> 🔄 Transforming text...')
            progress_bar.progress(50)
            time.sleep(0.5)
            
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
            status_text.markdown('<div class="loading"></div> ✨ Finalizing output...')
            time.sleep(0.5)
            
            # Output stats
            output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
            doc_output = NLP_GLOBAL(transformed)
            output_sentence_count = len(list(doc_output.sents))
            
            progress_bar.progress(100)
            status_text.markdown('✅ Transformation complete!')
            
            # Clear progress with delay
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            # Output Section
            st.markdown("""
            <div class="output-section">
                <h2 class="section-title">✨ Transformed Text</h2>
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
            
            # Copy Button with Enhanced Animation
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_btn"):
                    st.success("✅ **Text ready to copy!** Use Ctrl+A to select all text in the box above, then Ctrl+C to copy.")
            
            # Statistics with Glass Effect
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
            
            # Debug info with animation
            st.info(f"🔧 **Debug Info:** Passive={use_passive}, Synonyms={use_synonyms}, Structure={preserve_structure}")
            
        else:
            st.warning("⚠️ Please enter some text to transform!")
    
    # Ultra Modern Footer
    st.markdown("""
    <div class="footer">
        <p>✨ <strong>AI Text Humanizer Pro</strong> - Transform your writing with AI-powered enhancement</p>
        <p>Built with ❤️ using Streamlit and advanced NLP techniques</p>
        <p>Experience the future of text transformation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
