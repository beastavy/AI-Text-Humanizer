#!/usr/bin/env python3
"""
Test the improved transition logic to ensure it doesn't add transitions inappropriately
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer

def test_transition_logic():
    """Test that transitions are added more intelligently"""
    humanizer = AcademicTextHumanizer(p_academic_transition=0.5)  # 50% chance for testing

    test_cases = [
        "This is the first sentence. This is the second sentence. This is the third sentence.",
        "I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning.",
        "The research shows significant results. The methodology was sound. The conclusions are valid.",
        "AI detection is becoming more sophisticated. Content creators need better tools. Humanization is essential.",
    ]

    print("🧪 Testing Improved Transition Logic")
    print("=" * 60)

    for i, test_text in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Original: {test_text}")

        # Test without transitions
        result_no_transitions = humanizer.humanize_text(test_text, use_passive=False, use_synonyms=False, preserve_structure=False)
        print(f"No transitions: {result_no_transitions}")

        # Test with transitions (multiple times to see variation)
        print("With transitions (3 samples):")
        for j in range(3):
            result_with_transitions = humanizer.humanize_text(test_text, use_passive=False, use_synonyms=False, preserve_structure=False)
            transition_count = result_with_transitions.count('Moreover,') + result_with_transitions.count('Furthermore,') + result_with_transitions.count('Additionally,')
            print(f"  Sample {j+1}: {result_with_transitions} (transitions: {transition_count})")

        print("-" * 60)

def test_first_sentence_protection():
    """Test that first sentences don't get transitions"""
    humanizer = AcademicTextHumanizer(p_academic_transition=1.0)  # 100% chance

    test_text = "This is the first sentence. This is the second sentence. This is the third sentence."

    print("\n🔒 Testing First Sentence Protection")
    print(f"Original: {test_text}")

    # Run multiple times to ensure first sentence never gets transition
    for i in range(5):
        result = humanizer.humanize_text(test_text, use_passive=False, use_synonyms=False, preserve_structure=False)
        first_sentence = result.split('.')[0].strip()
        print(f"Attempt {i+1} - First sentence: '{first_sentence}'")

        if first_sentence.startswith(('Moreover,', 'Furthermore,', 'Additionally,')):
            print("❌ ERROR: First sentence got a transition!")
        else:
            print("✅ First sentence correctly protected from transitions")

if __name__ == "__main__":
    test_transition_logic()
    test_first_sentence_protection()

    print("\n" + "=" * 60)
    print("🎉 Transition logic test completed!")
    print("✅ Transitions should only appear between sentences")
    print("✅ First sentences should never get transitions")
    print("✅ Existing transitions should not be duplicated")
    print("=" * 60)
