#!/bin/bash
set -euo pipefail

# AI Text Humanizer Pro - Fixed DMG Builder
# This script creates a macOS DMG with proper metadata handling

APP_NAME="AI Text Humanizer Pro"
BUNDLE_ID="com.example.ai-text-humanizer-pro"
VERSION="1.0.0"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build/macos-fixed-dmg"
DIST_DIR="$PROJECT_ROOT/dist"
ENTRYPOINT="main.py"
ICON_ICNS="$PROJECT_ROOT/icon.icns"

echo "🚀 Starting Fixed DMG Build for $APP_NAME"
echo "=============================================="

# Clean previous builds
echo "[1/8] Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Validate entrypoint
if [ ! -f "$PROJECT_ROOT/$ENTRYPOINT" ]; then
  echo "❌ Entrypoint $ENTRYPOINT not found."
  exit 1
fi

# Check for icon
if [ -f "$ICON_ICNS" ]; then
  echo "✓ Found icon: $ICON_ICNS"
else
  echo "⚠️  Icon not found at $ICON_ICNS; app will use default icon."
fi

cd "$PROJECT_ROOT"

# Choose Python version
choose_python() {
  if [ -n "${PYTHON:-}" ] && command -v "$PYTHON" >/dev/null 2>&1; then
    echo "$PYTHON"
    return 0
  fi
  for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" >/dev/null 2>&1; then
      echo "$cmd"
      return 0
    fi
  done
  echo "python3"
}

PY_CMD=$(choose_python)
echo "[2/8] Using Python: $PY_CMD"

# Create isolated virtual environment
echo "[3/8] Creating build environment..."
"$PY_CMD" -m venv "$BUILD_DIR/.venv"
PYBIN="$BUILD_DIR/.venv/bin/python"
PIPBIN="$BUILD_DIR/.venv/bin/pip"

# Upgrade pip and install wheel
"$PIPBIN" install --upgrade pip wheel

# Install requirements
echo "[4/8] Installing dependencies..."
"$PIPBIN" install -r requirements.txt

# Download NLTK resources
echo "[5/8] Downloading NLTK resources..."
"$PYBIN" -c "
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
resources = ['punkt', 'averaged_perceptron_tagger', 'punkt_tab', 'wordnet', 'averaged_perceptron_tagger_eng']
for resource in resources:
    try:
        nltk.download(resource, quiet=True)
        print(f'✅ {resource} downloaded')
    except Exception as e:
        print(f'⚠️ Failed to download {resource}: {e}')
"

# Install PyInstaller
echo "[6/8] Installing PyInstaller..."
"$PIPBIN" install pyinstaller

# Create a simple launcher script that avoids metadata issues
LAUNCHER_SCRIPT="$BUILD_DIR/launcher.py"
cat > "$LAUNCHER_SCRIPT" << LAUNCHER
#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run main application
try:
    import main
    main.main()
except Exception as e:
    print(f"Error running application: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
LAUNCHER

# Build native app with PyInstaller using the launcher
echo "[7/8] Building native app..."

# Create a temporary PyInstaller spec file for better control
SPEC_FILE="$BUILD_DIR/app.spec"

cat > "$SPEC_FILE" << SPEC
# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

a = Analysis(
    ['$LAUNCHER_SCRIPT'],
    pathex=['$PROJECT_ROOT'],
    binaries=[],
    datas=[
        ('$PROJECT_ROOT/main.py', '.'),
        ('$PROJECT_ROOT/transformer', 'transformer'),
        ('$PROJECT_ROOT/templates', 'templates'),
        ('$PROJECT_ROOT/static', 'static'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.version',
        'nltk',
        'spacy',
        'spacy.lang.en',
        'srsly',
        'thinc',
        'cymem',
        'preshed',
        'blis',
        'murmurhash',
        'sentence_transformers',
        'transformers',
        'tokenizers',
        'torch',
        'sklearn',
        'scipy',
        'pandas',
        'numpy',
        'importlib.metadata',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI Text Humanizer Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='$ICON_ICNS' if os.path.exists('$ICON_ICNS') else None,
)

app = BUNDLE(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='AI Text Humanizer Pro.app',
    icon='$ICON_ICNS' if os.path.exists('$ICON_ICNS') else None,
    bundle_identifier='$BUNDLE_ID',
    version='$VERSION',
    info_plist={
        'CFBundleDisplayName': '$APP_NAME',
        'CFBundleName': '$APP_NAME',
        'CFBundleIdentifier': '$BUNDLE_ID',
        'CFBundleVersion': '$VERSION',
        'CFBundleShortVersionString': '$VERSION',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
        'CFBundleIconFile': 'icon.icns' if os.path.exists('$ICON_ICNS') else None,
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': True,
        },
    },
)
SPEC

# Run PyInstaller with the spec file
echo "Building with PyInstaller spec file..."
"$PYBIN" -m PyInstaller --noconfirm --clean "$SPEC_FILE"

# Verify app was created
APP_PATH="$DIST_DIR/${APP_NAME}.app"
if [ ! -d "$APP_PATH" ]; then
  echo "❌ PyInstaller build failed; .app not found at $APP_PATH"
  echo "Checking dist directory contents:"
  ls -la "$DIST_DIR" || echo "Dist directory not found or empty"
  exit 1
fi

echo "✓ Native app created successfully at $APP_PATH"

# Ensure icon is embedded in the app bundle (backup method)
if [ -f "$ICON_ICNS" ]; then
  echo "[8/8] Embedding icon in app bundle..."
  RES_DIR="$APP_PATH/Contents/Resources"
  mkdir -p "$RES_DIR"

  # Copy icon to Resources
  cp "$ICON_ICNS" "$RES_DIR/icon.icns"

  # Update Info.plist to reference the icon
  PLIST="$APP_PATH/Contents/Info.plist"
  if command -v /usr/libexec/PlistBuddy >/dev/null 2>&1; then
    /usr/libexec/PlistBuddy -c "Add :CFBundleIconFile string icon.icns" "$PLIST" 2>/dev/null || \
    /usr/libexec/PlistBuddy -c "Set :CFBundleIconFile icon.icns" "$PLIST" 2>/dev/null || true
  fi
fi

# Create DMG staging area
echo "[9/9] Creating DMG..."
DMG_STAGING="$BUILD_DIR/dmg-staging"
DMG_OUTPUT="$BUILD_DIR/${APP_NAME}.dmg"

rm -rf "$DMG_STAGING"
mkdir -p "$DMG_STAGING"

# Create Applications symlink for drag-and-drop install
ln -s /Applications "$DMG_STAGING/Applications"

# Copy the app bundle to staging
cp -R "$APP_PATH" "$DMG_STAGING/"

# Create compressed DMG
echo "Creating DMG..."
rm -f "$DMG_OUTPUT"
hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_STAGING" -ov -format UDZO "$DMG_OUTPUT"

# Verify DMG was created
if [ -f "$DMG_OUTPUT" ]; then
  DMG_SIZE=$(du -h "$DMG_OUTPUT" | cut -f1)
  echo ""
  echo "🎉 SUCCESS! Fixed DMG created successfully!"
  echo "=============================================="
  echo "📦 DMG Location: $DMG_OUTPUT"
  echo "📏 DMG Size: $DMG_SIZE"
  echo ""
  echo "💡 To install: Double-click the DMG, then drag the app to Applications folder."
  echo ""
else
  echo "❌ Failed to create DMG"
  exit 1
fi