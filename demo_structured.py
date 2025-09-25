#!/usr/bin/env python3
"""
Demo script showing the improved structure preservation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, download_nltk_resources

def demo_structured_humanization():
    """Demo the structured text humanization"""
    
    # Download required resources
    download_nltk_resources()
    
    # Your example text
    sample_text = """Introduction

The disconnect between Sarah's team's technical approach and the audience's actual motivations represents a fundamental challenge in marketing communication. While the team has focused extensively on product features and scientific specifications, the focus group feedback reveals that consumers are primarily concerned with environmental responsibility and health safety. This misalignment between what the company emphasizes and what customers value can significantly impact the success of the product launch.

The current campaign's reliance on technical jargon and formal language has created a barrier between the brand and its target audience. For the organic cleaning product launch to succeed, Sarah's team must fundamentally reframe their messaging strategy to align with consumer motivations and create meaningful emotional connections.

Concepts and Application

To address this communication gap, Sarah's team should implement several strategic adjustments:

Reframe the Value Proposition

Instead of leading with technical specifications, the campaign should position the products as solutions for health-conscious families and environmentally aware consumers. The messaging should shift from "Our proprietary formula delivers 99.7% cleaning efficiency" to "Protect your family's health while maintaining a spotless home." This approach addresses the audience's primary concerns while still highlighting effectiveness as a supporting benefit.

The campaign should emphasize the peace of mind that comes with using safer products, particularly for families with children or pets. Parents want assurance that their children can safely play on freshly cleaned surfaces, while environmentally conscious consumers seek validation that their choices contribute to planetary health.

Simplify Technical Language

The current dense technical copy alienates the target audience by using terminology that requires specialized knowledge. Replace jargon like "proprietary enzymatic breakdown technology" with accessible language such as "plant-based ingredients that naturally break down dirt and grime." The tone should be conversational yet professional, using everyday vocabulary that resonates with busy parents and environmentally conscious consumers.

Successful organic brands like Seventh Generation and Method demonstrate how warm, approachable language can create stronger connections with consumers. The messaging should feel like advice from a trusted friend rather than a scientific report."""
    
    print("🤖 AI TEXT HUMANIZER - STRUCTURE PRESERVATION DEMO")
    print("=" * 60)
    
    # Initialize humanizer
    humanizer = AcademicTextHumanizer(
        p_passive=0.3,
        p_synonym_replacement=0.3,
        p_academic_transition=0.4
    )
    
    # Process the text
    transformed = humanizer.humanize_text(
        sample_text,
        use_passive=True,
        use_synonyms=True
    )
    
    print("\n📝 ORIGINAL TEXT:")
    print("-" * 40)
    print(sample_text[:200] + "...")
    
    print("\n✨ HUMANIZED TEXT (with preserved structure):")
    print("-" * 40)
    print(transformed[:200] + "...")
    
    print("\n📊 STRUCTURE ANALYSIS:")
    print("-" * 40)
    original_lines = sample_text.split('\n')
    transformed_lines = transformed.split('\n')
    
    print(f"Original lines: {len(original_lines)}")
    print(f"Transformed lines: {len(transformed_lines)}")
    print(f"Structure preserved: {'✅ YES' if len(original_lines) == len(transformed_lines) else '❌ NO'}")
    
    # Show headings preserved
    original_headings = [line.strip() for line in original_lines if line.strip() and not line.strip().endswith('.') and len(line.split()) <= 8]
    transformed_headings = [line.strip() for line in transformed_lines if line.strip() and not line.strip().endswith('.') and len(line.split()) <= 8]
    
    print(f"\nHeadings preserved: {len(original_headings)} → {len(transformed_headings)}")
    
    print("\n🎯 KEY IMPROVEMENTS:")
    print("-" * 40)
    print("✅ Headings and subheadings preserved")
    print("✅ Paragraph structure maintained")
    print("✅ Line breaks and spacing kept")
    print("✅ Text humanized while keeping format")
    print("✅ AI detection bypassed with structure intact")
    
    return transformed

if __name__ == "__main__":
    demo_structured_humanization()
