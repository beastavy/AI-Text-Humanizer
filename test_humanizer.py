#!/usr/bin/env python3
"""
Test script to check if the humanizer is working correctly
"""

import sys
import os

# Add the transformer module to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test if all basic imports work"""
    try:
        import spacy
        import nltk
        from nltk.tokenize import word_tokenize
        print("✅ Basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_spacy_model():
    """Test if spaCy model loads correctly"""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("This is a test sentence.")
        print(f"✅ spaCy model loaded successfully. Processed: {len(list(doc.sents))} sentences")
        return True
    except Exception as e:
        print(f"❌ spaCy model error: {e}")
        return False

def test_nltk_resources():
    """Test if NLTK resources are available"""
    try:
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import wordnet

        # Test word tokenization
        text = "This is a test sentence with contractions like don't and won't."
        tokens = word_tokenize(text)
        print(f"✅ NLTK tokenization works: {len(tokens)} tokens")

        # Test WordNet
        synonyms = []
        for syn in wordnet.synsets("good"):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        print(f"✅ WordNet works: found {len(synonyms)} synonyms for 'good'")
        return True
    except Exception as e:
        print(f"❌ NLTK error: {e}")
        return False

def test_sentence_transformers():
    """Test if sentence-transformers is available"""
    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        print("✅ Sentence transformers available")
        return True
    except ImportError:
        print("⚠️ Sentence transformers not available (optional)")
        return False
    except Exception as e:
        print(f"❌ Sentence transformers error: {e}")
        return False

def test_humanizer():
    """Test the actual humanizer functionality"""
    try:
        from transformer.app import AcademicTextHumanizer

        # Create humanizer
        humanizer = AcademicTextHumanizer(p_passive=0.3, p_synonym_replacement=0.3, p_academic_transition=0.4)

        # Test text
        test_text = "I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning. The team needs to understand the requirements better before we proceed."

        print(f"Original text: {test_text}")
        print()

        # Test humanization
        transformed = humanizer.humanize_text(test_text, use_passive=False, use_synonyms=False, preserve_structure=False)

        print(f"Transformed text: {transformed}")
        print()

        # Test with options
        transformed_with_options = humanizer.humanize_text(
            test_text,
            use_passive=True,
            use_synonyms=True,
            preserve_structure=False
        )

        print(f"Transformed with options: {transformed_with_options}")
        print()

        return True
    except Exception as e:
        print(f"❌ Humanizer error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Testing AI Text Humanizer Components")
    print("=" * 50)

    tests = [
        ("Basic Imports", test_basic_imports),
        ("spaCy Model", test_spacy_model),
        ("NLTK Resources", test_nltk_resources),
        ("Sentence Transformers", test_sentence_transformers),
        ("Humanizer Functionality", test_humanizer)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The humanizer should work correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    print("=" * 50)

    return all_passed

if __name__ == "__main__":
    main()



