#!/bin/bash
# Proper code signing for distribution (requires Apple Developer ID)

APP_PATH="dist/AI Text Humanizer Pro"

echo "🔒 Code signing with Developer ID..."
# Replace 'Developer ID Application: YOUR NAME (TEAM_ID)' with your actual certificate name
codesign --force --deep --sign "Developer ID Application: YOUR NAME (TEAM_ID)" "$APP_PATH"

echo "📦 Creating DMG..."
rm -f build/*.dmg
hdiutil create -volname "AI Text Humanizer Pro" \
    -srcfolder "$APP_PATH" \
    -ov -format UDZO \
    "build/AI-Text-Humanizer-Pro-1.0.0.dmg"

echo "✅ Done! DMG created and signed at build/AI-Text-Humanizer-Pro-1.0.0.dmg"
