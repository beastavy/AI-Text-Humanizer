#!/usr/bin/env python3
"""
Test script to verify humanization is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, download_nltk_resources

def test_humanization():
    """Test that humanization is working"""
    
    # Download required resources
    download_nltk_resources()
    
    # Test text
    test_text = "I don't think this will work. It's not good enough. We can't do it."
    
    print("🧪 Testing Humanization")
    print("=" * 50)
    print(f"Original: {test_text}")
    
    # Initialize humanizer
    humanizer = AcademicTextHumanizer(
        p_passive=0.3,
        p_synonym_replacement=0.3,
        p_academic_transition=0.4
    )
    
    # Test different modes
    print("\n1. Basic mode (no options):")
    result1 = humanizer.humanize_text(test_text, use_passive=False, use_synonyms=False, preserve_structure=False)
    print(f"Result: {result1}")
    
    print("\n2. With passive voice:")
    result2 = humanizer.humanize_text(test_text, use_passive=True, use_synonyms=False, preserve_structure=False)
    print(f"Result: {result2}")
    
    print("\n3. With synonyms:")
    result3 = humanizer.humanize_text(test_text, use_passive=False, use_synonyms=True, preserve_structure=False)
    print(f"Result: {result3}")
    
    print("\n4. With both:")
    result4 = humanizer.humanize_text(test_text, use_passive=True, use_synonyms=True, preserve_structure=False)
    print(f"Result: {result4}")
    
    # Check if any changes were made
    if result1 != test_text:
        print("\n✅ Humanization is working!")
    else:
        print("\n❌ Humanization is NOT working - text unchanged")

if __name__ == "__main__":
    test_humanization()
