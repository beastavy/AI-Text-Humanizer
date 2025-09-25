#!/usr/bin/env python3
"""
Test script to verify that the AI Text Humanizer preserves structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, download_nltk_resources

def test_structure_preservation():
    """Test that the humanizer preserves text structure"""
    
    # Download required resources
    download_nltk_resources()
    
    # Sample structured text
    test_text = """Introduction

The disconnect between Sarah's team's technical approach and the audience's actual motivations represents a fundamental challenge in marketing communication. While the team has focused extensively on product features and scientific specifications, the focus group feedback reveals that consumers are primarily concerned with environmental responsibility and health safety.

Concepts and Application

To address this communication gap, Sarah's team should implement several strategic adjustments:

Reframe the Value Proposition

Instead of leading with technical specifications, the campaign should position the products as solutions for health-conscious families and environmentally aware consumers. The messaging should shift from "Our proprietary formula delivers 99.7% cleaning efficiency" to "Protect your family's health while maintaining a spotless home."

Simplify Technical Language

The current dense technical copy alienates the target audience by using terminology that requires specialized knowledge. Replace jargon like "proprietary enzymatic breakdown technology" with accessible language such as "plant-based ingredients that naturally break down dirt and grime." """
    
    print("Original Text Structure:")
    print("=" * 50)
    print(test_text)
    print("\n" + "=" * 50)
    
    # Initialize humanizer
    humanizer = AcademicTextHumanizer(
        p_passive=0.3,
        p_synonym_replacement=0.3,
        p_academic_transition=0.4
    )
    
    # Process the text
    transformed = humanizer.humanize_text(
        test_text,
        use_passive=True,
        use_synonyms=True
    )
    
    print("\nTransformed Text Structure:")
    print("=" * 50)
    print(transformed)
    print("\n" + "=" * 50)
    
    # Check if structure is preserved
    original_lines = test_text.split('\n')
    transformed_lines = transformed.split('\n')
    
    print(f"\nStructure Analysis:")
    print(f"Original lines: {len(original_lines)}")
    print(f"Transformed lines: {len(transformed_lines)}")
    
    # Check for headings
    original_headings = [line for line in original_lines if line.strip() and not line.strip().endswith('.') and len(line.split()) <= 8]
    transformed_headings = [line for line in transformed_lines if line.strip() and not line.strip().endswith('.') and len(line.split()) <= 8]
    
    print(f"Original headings: {len(original_headings)}")
    print(f"Transformed headings: {len(transformed_headings)}")
    
    if len(original_lines) == len(transformed_lines):
        print("✅ Structure preserved successfully!")
    else:
        print("❌ Structure not preserved properly")
    
    return transformed

if __name__ == "__main__":
    test_structure_preservation()
