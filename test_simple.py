#!/usr/bin/env python3
"""
Test the simple humanizer functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_humanizer import expand_contractions, add_academic_transitions, improve_sentence_structure, humanize_text

def test_humanizer():
    """Test the humanizer with sample text"""
    test_text = "I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning. The team needs to understand the requirements better before we proceed."

    print("Original text:")
    print(test_text)
    print("\n" + "="*50 + "\n")

    # Test contraction expansion
    expanded = expand_contractions(test_text)
    print("After contraction expansion:")
    print(expanded)
    print("\n" + "="*50 + "\n")

    # Test transition addition
    with_transitions = add_academic_transitions(expanded)
    print("After adding transitions:")
    print(with_transitions)
    print("\n" + "="*50 + "\n")

    # Test structure improvement
    structured = improve_sentence_structure(with_transitions)
    print("After structure improvement:")
    print(structured)
    print("\n" + "="*50 + "\n")

    # Test full humanization
    full_result = humanize_text(test_text, use_transitions=True, use_structure=True)
    print("Full humanization result:")
    print(full_result)
    print("\n" + "="*50 + "\n")

    # Count words
    original_words = len(test_text.split())
    result_words = len(full_result.split())
    print(f"Word count: {original_words} → {result_words} (+{result_words - original_words})")

    return True

if __name__ == "__main__":
    print("🧪 Testing Simple Humanizer")
    print("=" * 50)
    test_humanizer()



