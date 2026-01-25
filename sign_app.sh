#!/bin/bash
# Simple ad-hoc signing for testing
APP_PATH="dist/AI Text Humanizer Pro"

echo "🔒 Ad-hoc signing the app..."
codesign --force --deep --sign - "$APP_PATH" 2>/dev/null || echo "⚠️  Ad-hoc signing failed (normal for non-developer Macs)"

echo "📦 Creating DMG..."
rm -f build/*.dmg
hdiutil create -volname "AI Text Humanizer Pro" \
    -srcfolder "$APP_PATH" \
    -ov -format UDZO \
    "build/AI-Text-Humanizer-Pro-1.0.0.dmg"

echo "✅ Done! DMG created at build/AI-Text-Humanizer-Pro-1.0.0.dmg"
