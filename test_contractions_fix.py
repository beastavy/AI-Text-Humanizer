#!/usr/bin/env python3
"""
Test script to verify the contraction fix works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, download_nltk_resources

def test_contraction_fix():
    """Test that contractions are handled correctly"""
    
    # Download required resources
    download_nltk_resources()
    
    # Test cases
    test_cases = [
        # Names with possessives (should NOT change)
        ("Sarah's team", "Sarah's team"),
        ("John's car", "John's car"),
        ("Mary's book", "Mary's book"),
        ("David's house", "David's house"),
        
        # Grammar contractions (should change)
        ("it's working", "it is working"),
        ("that's good", "that is good"),
        ("don't do it", "do not do it"),
        ("can't help", "cannot help"),
        ("won't work", "will not work"),
        ("isn't it", "is not it"),
        ("I'm here", "I am here"),
        ("you're right", "you are right"),
        ("he's coming", "he is coming"),
        ("she's going", "she is going"),
        ("we're ready", "we are ready"),
        ("they're here", "they are here"),
        
        # Mixed cases
        ("Sarah's team can't help", "Sarah's team cannot help"),
        ("John's car isn't working", "John's car is not working"),
        ("Mary's book that's good", "Mary's book that is good"),
    ]
    
    print("🧪 Testing Contraction Fix")
    print("=" * 60)
    
    # Initialize humanizer
    humanizer = AcademicTextHumanizer(
        p_passive=0.0,  # Disable other transformations
        p_synonym_replacement=0.0,
        p_academic_transition=0.0
    )
    
    all_passed = True
    
    for input_text, expected in test_cases:
        # Test just the contraction expansion
        result = humanizer.expand_contractions(input_text)
        
        # Check if result matches expected
        if result == expected:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False
        
        print(f"{status} | Input: '{input_text}'")
        print(f"      | Expected: '{expected}'")
        print(f"      | Got: '{result}'")
        print("-" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Contraction fix is working correctly!")
    else:
        print("\n⚠️ Some tests failed. Check the logic above.")
    
    return all_passed

if __name__ == "__main__":
    test_contraction_fix()
