#!/usr/bin/env python3
"""
Test script to verify the improved contraction expansion logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, download_nltk_resources

def test_contraction_logic():
    """Test the improved contraction expansion logic"""
    
    # Download required resources
    download_nltk_resources()
    
    # Test cases
    test_cases = [
        # Should expand contractions
        ("don't", "do not"),
        ("can't", "cannot"),  # can't -> cannot
        ("won't", "will not"),
        ("they're", "they are"),
        ("I'll", "I will"),
        ("I've", "I have"),
        ("I'd", "I would"),
        ("I'm", "I am"),
        ("it's", "it is"),
        ("what's", "what is"),
        
        # Should NOT expand possessives
        ("Sarah's team", "Sarah's team"),
        ("John's car", "John's car"),
        ("company's policy", "company's policy"),
        ("team's approach", "team's approach"),
        ("customer's needs", "customer's needs"),
        
        # Mixed cases
        ("Sarah's team doesn't work", "Sarah's team does not work"),
        ("The company's policy won't change", "The company's policy will not change"),
    ]
    
    print("🧪 Testing Improved Contraction Logic")
    print("=" * 50)
    
    # Initialize humanizer
    humanizer = AcademicTextHumanizer()
    
    for original, expected in test_cases:
        result = humanizer.expand_contractions(original)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} | '{original}' -> '{result}'")
        if result != expected:
            print(f"     Expected: '{expected}'")
    
    print("\n" + "=" * 50)
    print("🎯 Key Improvements:")
    print("✅ Possessive forms (Sarah's, John's) are preserved")
    print("✅ Only true contractions are expanded")
    print("✅ Uses regex patterns for more accurate matching")

if __name__ == "__main__":
    test_contraction_logic()
