#!/bin/bash
set -euo pipefail

APP_NAME="AI Text Humanizer Pro"
BUNDLE_ID="com.aitexthumanizer.pro"
VERSION="1.0.0"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build/macos"
DIST_DIR="$PROJECT_ROOT/dist"
APP_PATH="$DIST_DIR/AI Text Humanizer Pro.app"
DMG_STAGING="$BUILD_DIR/dmg-staging"
DMG_OUTPUT="$BUILD_DIR/$APP_NAME.dmg"

echo "[1/8] Checking dependencies"
# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Check for PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Install PyQt6 if not present
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo "Installing PyQt6..."
    pip3 install PyQt6
fi

echo "[2/8] Cleaning previous build"
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DMG_STAGING"

echo "[3/8] Generating PyInstaller spec file"
cd "$PROJECT_ROOT"
python3 pyinstaller_config.py

echo "[4/8] Building native macOS app with PyInstaller"
cd "$PROJECT_ROOT"
pyinstaller --clean --noconfirm "build_macos_app.spec"

echo "[5/8] Verifying app bundle"
if [ ! -d "$APP_PATH" ]; then
    echo "❌ App bundle not created. Build may have failed."
    exit 1
fi

# Sign the app for Gatekeeper (if developer certificate is available)
if security find-identity -p codesigning -v | grep -q "Developer ID Application"; then
    echo "[6/8] Code signing app..."
    codesign --deep --force --verify --verbose --sign "Developer ID Application" "$APP_PATH"
else
    echo "[6/8] Skipping code signing (no Developer ID found)"
    # Remove quarantine attribute to prevent Gatekeeper issues
    xattr -cr "$APP_PATH" 2>/dev/null || true
fi

echo "[7/8] Preparing DMG staging"
# Copy app to staging directory
cp -R "$APP_PATH" "$DMG_STAGING/"

# Create Applications symlink for drag-and-drop install
ln -s /Applications "$DMG_STAGING/Applications"

# Create a beautiful background image for DMG (optional)
cat > "$DMG_STAGING/.background/background.md" << 'BG'
Drag the AI Text Humanizer Pro app to the Applications folder to install.
BG

echo "[8/8] Creating DMG installer"
# Remove existing DMG
rm -f "$DMG_OUTPUT"

# Create DMG with compression
hdiutil create -volname "$APP_NAME" \
    -srcfolder "$DMG_STAGING" \
    -ov -format UDZO \
    "$DMG_OUTPUT"

# Verify DMG
if [ -f "$DMG_OUTPUT" ]; then
    echo ""
    echo "========================================"
    echo "✅ SUCCESS! DMG created successfully"
    echo "========================================"
    echo "📦 DMG Location: $DMG_OUTPUT"
    echo "📏 Size: $(du -h \"$DMG_OUTPUT\" | cut -f1)"
    echo ""
    echo "📱 To install:"
    echo "  1. Double-click the DMG file"
    echo "  2. Drag 'AI Text Humanizer Pro' to Applications"
    echo "  3. Launch from Applications folder"
    echo ""
    echo "🚀 You can now share this DMG with any Mac user!"
    echo "========================================"
else
    echo "❌ Failed to create DMG"
    exit 1
fi
