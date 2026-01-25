#!/bin/bash

# Simple DMG Creator for AI Text Humanizer Pro
# This creates a DMG with the app files and launcher script

APP_NAME="AI Text Humanizer Pro"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build/simple-dmg"
DMG_DIR="$BUILD_DIR/dmg"
DMG_OUTPUT="$BUILD_DIR/AI Text Humanizer Pro.dmg"

echo "📦 Creating Simple DMG for $APP_NAME"
echo "==================================="

# Clean previous builds
echo "[1/4] Cleaning previous builds..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR" "$DMG_DIR"

# Copy app files to DMG directory
echo "[2/4] Copying app files..."
cp -R "$PROJECT_ROOT" "$DMG_DIR/$APP_NAME"
rm -rf "$DMG_DIR/$APP_NAME/.git"
rm -rf "$DMG_DIR/$APP_NAME/build"
rm -rf "$DMG_DIR/$APP_NAME/dist"
rm -rf "$DMG_DIR/$APP_NAME/temp_venv"
rm -rf "$DMG_DIR/$APP_NAME/__pycache__"
rm -rf "$DMG_DIR/$APP_NAME/*/__pycache__"

# Make launcher script executable in the DMG
chmod +x "$DMG_DIR/$APP_NAME/macos/launch_app.sh"

# Create Applications symlink for drag-and-drop install
ln -s /Applications "$DMG_DIR/Applications"

# Create compressed DMG
echo "[3/4] Creating DMG..."
rm -f "$DMG_OUTPUT"
hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_DIR" -ov -format UDZO "$DMG_OUTPUT"

# Verify DMG was created
if [ -f "$DMG_OUTPUT" ]; then
  DMG_SIZE=$(du -h "$DMG_OUTPUT" | cut -f1)
  echo ""
  echo "🎉 SUCCESS! Simple DMG created successfully!"
  echo "============================================"
  echo "📦 DMG Location: $DMG_OUTPUT"
  echo "📏 DMG Size: $DMG_SIZE"
  echo ""
  echo "💡 To install:"
  echo "   1. Double-click the DMG file"
  echo "   2. Drag the app folder to Applications"
  echo "   3. Navigate to the app folder in Applications"
  echo "   4. Double-click 'launch_app.sh' to start the app"
  echo ""
  echo "📝 Note: This version includes all source files and will"
  echo "   set up a temporary environment when launched."
  echo ""
else
  echo "❌ Failed to create DMG"
  exit 1
fi

echo "[4/4] Done!"