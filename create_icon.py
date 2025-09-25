#!/usr/bin/env python3
"""
Create a simple icon for the executable
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the app"""
    # Create a 256x256 image with a blue background
    size = 256
    img = Image.new('RGBA', (size, size), (37, 99, 235, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle in the center
    margin = 40
    draw.ellipse([margin, margin, size-margin, size-margin], fill=(255, 255, 255, 255))
    
    # Draw text "AI" in the center
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "AI"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    draw.text((x, y), text, fill=(37, 99, 235, 255), font=font)
    
    # Draw "T" for Text below
    text2 = "T"
    bbox2 = draw.textbbox((0, 0), text2, font=font)
    text2_width = bbox2[2] - bbox2[0]
    text2_height = bbox2[3] - bbox2[1]
    
    x2 = (size - text2_width) // 2
    y2 = y + text_height + 5
    
    draw.text((x2, y2), text2, fill=(37, 99, 235, 255), font=font)
    
    # Save as ICO file
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("✅ Icon created: icon.ico")

if __name__ == "__main__":
    create_icon()
