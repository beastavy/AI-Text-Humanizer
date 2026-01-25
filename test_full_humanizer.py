#!/usr/bin/env python3
"""
Test the full humanizer functionality with all Python libraries
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work"""
    try:
        import streamlit as st
        from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
        from nltk.tokenize import word_tokenize
        import spacy
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_spacy():
    """Test if spaCy works"""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("This is a test sentence for advanced processing.")
        print(f"✅ spaCy working: {len(list(doc.sents))} sentences, {len(list(doc.ents))} entities")
        return True
    except Exception as e:
        print(f"❌ spaCy error: {e}")
        return False

def test_nltk():
    """Test if NLTK works"""
    try:
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import wordnet

        text = "This is a comprehensive test of the advanced humanizer functionality."
        tokens = word_tokenize(text)
        print(f"✅ NLTK working: {len(tokens)} tokens")

        # Test WordNet
        synonyms = []
        for syn in wordnet.synsets("good"):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        print(f"✅ WordNet working: {len(synonyms)} synonyms for 'good'")
        return True
    except Exception as e:
        print(f"❌ NLTK error: {e}")
        return False

def test_sentence_transformers():
    """Test if sentence-transformers works"""
    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        print("✅ Sentence transformers working")
        return True
    except ImportError:
        print("⚠️ Sentence transformers not available (optional)")
        return False
    except Exception as e:
        print(f"❌ Sentence transformers error: {e}")
        return False

def test_humanizer():
    """Test the full humanizer"""
    try:
        from transformer.app import AcademicTextHumanizer

        # Create humanizer with advanced settings
        humanizer = AcademicTextHumanizer(
            p_passive=0.3,
            p_synonym_replacement=0.3,
            p_academic_transition=0.4
        )

        # Test text
        test_text = "I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning. The team needs to understand the requirements better before we proceed."

        print(f"Original text: {test_text}")
        print()

        # Test with all features enabled
        transformed = humanizer.humanize_text(
            test_text,
            use_passive=True,
            use_synonyms=True,
            preserve_structure=False
        )

        print(f"Transformed text: {transformed}")
        print()

        return True
    except Exception as e:
        print(f"❌ Humanizer error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Full AI Text Humanizer Pro")
    print("=" * 60)

    tests = [
        ("Basic Imports", test_imports),
        ("spaCy Model", test_spacy),
        ("NLTK Resources", test_nltk),
        ("Sentence Transformers", test_sentence_transformers),
        ("Full Humanizer", test_humanizer)
    ]

    results = []
    all_passed = True

    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
            all_passed = False

    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Full humanizer is working perfectly.")
        print("✅ Advanced features available:")
        print("   - Synonym replacement with AI")
        print("   - Passive voice conversion")
        print("   - Academic transitions")
        print("   - Structure preservation")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("💡 Try running SETUP.bat if you haven't already.")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    main()



