#!/usr/bin/env python3
"""
AI Text Humanizer Pro - Flask Backend with Full Python Libraries
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import re

# Add the transformer module to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Download NLTK resources on startup
try:
    download_nltk_resources()
    print("✅ NLTK resources downloaded successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not download NLTK resources: {e}")

# Initialize the humanizer
try:
    humanizer = AcademicTextHumanizer(
        p_passive=0.3,
        p_synonym_replacement=0.3,
        p_academic_transition=0.4
    )
    print("✅ AcademicTextHumanizer initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize humanizer: {e}")
    humanizer = None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/transform', methods=['POST'])
def transform_text():
    """API endpoint for text transformation"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Enforce word limit
        MAX_WORDS = 5000
        word_count = len(text.split())
        if word_count > MAX_WORDS:
            return jsonify({'error': f'Text exceeds the {MAX_WORDS} word limit ({word_count} words). Please shorten your text.'}), 400
        
        # Get options from request
        use_passive = data.get('use_passive', False)
        use_synonyms = data.get('use_synonyms', False)
        preserve_structure = data.get('preserve_structure', False)
        intensity = data.get('intensity', 'medium')
        style = data.get('style', 'academic')
        
        # Transform text using the full Python humanizer
        if humanizer:
            transformed = humanizer.humanize_text(
                text,
                use_passive=use_passive,
                use_synonyms=use_synonyms,
                preserve_structure=preserve_structure,
                intensity=intensity,
                style=style
            )
        else:
            # Fallback to simple transformation if humanizer not available
            transformed = simple_transform(text, use_passive, use_synonyms, intensity, style)
        
        # Calculate statistics with safe fallbacks
        input_word_count = count_words(text)
        input_sentence_count = count_sentences(text)

        output_word_count = count_words(transformed)
        output_sentence_count = count_sentences(transformed)
        
        return jsonify({
            'success': True,
            'transformed_text': transformed,
            'statistics': {
                'input_words': input_word_count,
                'input_sentences': input_sentence_count,
                'output_words': output_word_count,
                'output_sentences': output_sentence_count
            },
            'options_used': {
                'use_passive': use_passive,
                'use_synonyms': use_synonyms,
                'preserve_structure': preserve_structure,
                'intensity': intensity,
                'style': style
            }
        })
        
    except Exception as e:
        print(f"Error in transform_text: {e}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Transformation failed: {str(e)}'
        }), 500

@app.route('/api/sample', methods=['GET'])
def get_sample_text():
    """Get sample text for testing"""
    sample_texts = [
        "I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning. The team needs to understand the requirements better before we proceed.",
        "You're right about the issue. We should fix it as soon as possible. It's important to get this done quickly. Let me know if you need any help with the implementation.",
        "The project is going well. We've made good progress this week. The team is working hard and we're on track to meet our deadlines. I think we can finish everything on time.",
        "This is a great idea! We should definitely try it. It might help us solve the problem we've been having. Let's discuss it in the next meeting and see what everyone thinks.",
        "I'm not sure about this solution. It seems too complicated for what we need. Maybe we should look for a simpler approach. What do you think about trying something different?"
    ]
    
    import random
    return jsonify({
        'sample_text': random.choice(sample_texts)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'humanizer_available': humanizer is not None,
        'nltk_available': True,
        'spacy_available': True
    })

def simple_transform(text, use_passive=False, use_synonyms=False, intensity='medium', style='academic'):
    """Simple fallback transformation if full humanizer is not available"""
    import random

    # Basic contraction expansion
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

    # Add style-aware transitions
    style_transitions = {
        "academic": ["Moreover,", "Additionally,", "Furthermore,", "Hence,", "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,"],
        "professional": ["Additionally,", "As a result,", "In summary,", "Importantly,", "Moving forward,", "With this in mind,"],
        "formal": ["Furthermore,", "Moreover,", "Accordingly,", "Thus,", "In light of the above,", "Notwithstanding,"]
    }
    transitions = style_transitions.get(str(style).lower(), style_transitions["academic"])
    sentence_parts = [s.strip() for s in re.split(r'(?<=[.!?])\s+', result) if s.strip()]
    intensity_level = str(intensity).lower()
    if len(sentence_parts) > 1:
        if intensity_level == 'very_heavy':
            p_transition = 0.8
        elif intensity_level == 'heavy':
            p_transition = 0.5
        elif intensity_level == 'light':
            p_transition = 0.2
        else:
            p_transition = 0.35
        transition_added = False
        for i in range(1, len(sentence_parts)):
            if random.random() < p_transition:
                sentence_parts[i] = f"{random.choice(transitions)} {sentence_parts[i]}"
                transition_added = True
        if not transition_added:
            sentence_parts[1] = f"{random.choice(transitions)} {sentence_parts[1]}"
        result = " ".join(sentence_parts)

    if use_synonyms:
        synonyms = {
            "good": "strong", "bad": "poor", "important": "significant",
            "help": "assist", "show": "demonstrate", "use": "utilize",
            "start": "commence", "end": "conclude", "think": "consider",
            "get": "obtain", "make": "produce"
        }
        synonym_replaced = False
        for word, replacement in synonyms.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            p_synonym = 0.55 if intensity_level == 'very_heavy' else 0.4 if intensity_level == 'heavy' else 0.25 if intensity_level == 'light' else 0.35
            if random.random() < p_synonym:
                new_result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
                if new_result != result:
                    synonym_replaced = True
                result = new_result

        # Ensure at least one visible synonym change when enabled.
        if not synonym_replaced:
            for word, replacement in synonyms.items():
                pattern = r'\b' + re.escape(word) + r'\b'
                new_result, count = re.subn(pattern, replacement, result, count=1, flags=re.IGNORECASE)
                if count > 0:
                    result = new_result
                    break

    if use_passive:
        # Minimal safe passive-like rewrites for common pronoun openings.
        result = re.sub(r"\bwe\s+can\b", "it can be", result, flags=re.IGNORECASE)
        result = re.sub(r"\bwe\s+will\b", "it will be", result, flags=re.IGNORECASE)
        result = re.sub(r"\bthey\s+can\b", "it can be", result, flags=re.IGNORECASE)
        result = re.sub(r"\byou\s+should\b", "it should be", result, flags=re.IGNORECASE)

    return result

def count_words(text):
    try:
        return len(word_tokenize(text, language='english', preserve_line=True))
    except Exception:
        return len(re.findall(r"\b\w+\b", text))

def count_sentences(text):
    try:
        return len(list(NLP_GLOBAL(text).sents))
    except Exception:
        return len([s for s in re.split(r"[.!?]+", text) if s.strip()])

if __name__ == '__main__':
    print("🚀 Starting AI Text Humanizer Pro Flask Server...")
    print("📝 Full Python libraries enabled")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Set to False for production
        threaded=True
    )
