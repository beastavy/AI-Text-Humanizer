import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import time



def main():
    """
    The `main` function sets up a Streamlit page for transforming user-provided text into a more formal
    academic style by expanding contractions, adding academic transitions, and optionally converting
    sentences to passive voice or replacing words with synonyms.
    """
    # Download NLTK resources if needed
    download_nltk_resources()

    # Configure Streamlit page
    st.set_page_config(
        page_title="Humanize AI Generated text",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': "https://github.com/DadaNanjesha/AI-Text-Humanizer-App/issues",
            'Report a bug': "https://github.com/DadaNanjesha/AI-Text-Humanizer-App/issues",
            'About': "# This app is used to Humanize AI generated text"
        }
    )

    # --- Custom CSS for Title Centering and Additional Styling ---
    st.markdown(
        """
        <style>
        /* Center the main title */
        .title {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            margin-top: 0.5em;
        }
        /* Center the subtitle / introduction block */
        .intro {
            text-align: left;
            line-height: 1.6;
            margin-bottom: 1.2em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Title / Intro ---
    st.markdown("<div class='title'>🧔🏻‍♂️Humanize AI🤖 Generated text</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='intro'>
        <p><b>This app transforms your text into a more formal academic style by:<b><br>
        • Expanding contractions<br>
        • Adding academic transitions<br>
        • <em>Optionally</em> converting some sentences to passive voice<br>
        • <em>Optionally</em> replacing words with synonyms for a more formal tone.</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Checkboxes
    use_passive = st.checkbox("Enable Passive Voice Transformation", value=False)
    use_synonyms = st.checkbox("Enable Synonym Replacement", value=False)
    preserve_structure = st.checkbox("Preserve Structure (Headings/Paragraphs)", value=False, 
                                   help="Keep original formatting with headings and paragraphs")

    # Text input
    user_text = st.text_area("Enter your text here:")

    # File upload
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # Button
    if st.button("Transform to Academic Style"):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Transforming text..."):
                # Input stats
                input_word_count = len(word_tokenize(user_text,language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # Transform
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
                
                # Debug info
                st.info(f"🔧 Debug: Passive={use_passive}, Synonyms={use_synonyms}, Structure={preserve_structure}")

                # Output
                st.subheader("✨ Transformed Text:")
                
                # Display transformed text in a text area for easy copying
                st.text_area(
                    "Humanized Text:",
                    value=transformed,
                    height=300,
                    key="transformed_output",
                    help="Click in the text area and use Ctrl+A to select all, then Ctrl+C to copy"
                )
                
                # Copy button that doesn't cause text to vanish
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("📋 Copy to Clipboard", help="Click to copy the transformed text", use_container_width=True):
                        # Use JavaScript to copy to clipboard
                        st.markdown("""
                        <script>
                        function copyToClipboard() {
                            const textArea = document.querySelector('textarea[aria-label*="Humanized Text"]');
                            if (textArea) {
                                textArea.select();
                                document.execCommand('copy');
                                alert('Text copied to clipboard!');
                            }
                        }
                        </script>
                        """, unsafe_allow_html=True)
                        st.success("✅ Text copied! Use Ctrl+A to select all text in the box above, then Ctrl+C to copy.")

                # Output stats with green styling
                output_word_count = len(word_tokenize(transformed,language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                st.markdown(
                    f"""
                    <div style="
                        background-color: #e8f5e8;
                        padding: 10px;
                        border-radius: 5px;
                        border: 1px solid #4CAF50;
                        margin: 10px 0;
                    ">
                        <strong style="color: #2e7d32;">📊 Statistics:</strong><br>
                        <span style="color: #2e7d32;">Input Word Count:</span> {input_word_count} | 
                        <span style="color: #2e7d32;">Sentence Count:</span> {input_sentence_count}<br>
                        <span style="color: #2e7d32;">Output Word Count:</span> {output_word_count} | 
                        <span style="color: #2e7d32;">Sentence Count:</span> {output_sentence_count}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")


if __name__ == "__main__":
    main()