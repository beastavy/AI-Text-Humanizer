#!/bin/bash
set -euo pipefail

# AI Text Humanizer Pro - Native macOS DMG Builder
# This script creates a proper native macOS app using PyInstaller

APP_NAME="AI Text Humanizer Pro"
BUNDLE_ID="com.example.ai-text-humanizer-pro"
VERSION="1.0.0"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build/macos-native-dmg"
DIST_DIR="$PROJECT_ROOT/dist"
ENTRYPOINT="gui/qt_app.py"
ICON_ICNS="$PROJECT_ROOT/icon.icns"
NLTK_DIR="$PROJECT_ROOT/nltk_data"

echo "🚀 Starting Native DMG Build for $APP_NAME"
echo "=============================================="

# Clean previous builds
echo "[1/8] Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR" "$NLTK_DIR"

# Validate entrypoint
if [ ! -f "$PROJECT_ROOT/$ENTRYPOINT" ]; then
  echo "❌ Entrypoint $ENTRYPOINT not found."
  exit 1
fi

# Check for icon
if [ ! -f "$ICON_ICNS" ]; then
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

# Prefetch NLP resources
echo "[5/8] Preparing NLP resources..."
"$PYBIN" - <<'PY'
import os, nltk, spacy
from pathlib import Path

# NLTK resources required by app
RES = ['punkt', 'averaged_perceptron_tagger', 'punkt_tab', 'wordnet', 'averaged_perceptron_tagger_eng']
nl_dir = Path('nltk_data')
nl_dir.mkdir(exist_ok=True)
for r in RES:
    try:
        nltk.download(r, download_dir=str(nl_dir), quiet=True)
        print(f"✓ Downloaded NLTK: {r}")
    except Exception as e:
        print(f"⚠ Failed NLTK {r}: {e}")

# Ensure spaCy model is available
try:
    nlp = spacy.load('en_core_web_sm')
    print('✓ spaCy en_core_web_sm is available')
except Exception as e:
    print(f'⚠ spaCy model issue: {e}')
PY

# Install PyInstaller
echo "[6/8] Installing PyInstaller..."
"$PIPBIN" install pyinstaller

# Build native app with PyInstaller
echo "[7/8] Building native app..."

# PyInstaller configuration for Qt apps
HIDDEN_IMPORTS=(
  nltk
  spacy
  spacy.lang.en
  srsly
  thinc
  cymem
  preshed
  blis
  murmurhash
  transformers
  tokenizers
  sentence_transformers
  torch
  sklearn
  scipy
  pandas
  numpy
  PyQt6
  PyQt6.QtCore
  PyQt6.QtGui
  PyQt6.QtWidgets
)

COLLECT_ARGS=(
  --collect-all spacy
  --collect-all en_core_web_sm
  --collect-all sentence_transformers
  --collect-all transformers
  --collect-all tokenizers
  --collect-all torch
  --collect-all sklearn
  --collect-all scipy
  --collect-all pandas
  --collect-all numpy
  --collect-all PyQt6
)

# Build arguments
BUILD_ARGS=(
  --noconfirm
  --clean
  --windowed
  --name "$APP_NAME"
  --noconsole
  --osx-bundle-identifier "$BUNDLE_ID"
  --version "$VERSION"
)

# Add icon if available
if [ -f "$ICON_ICNS" ]; then
  BUILD_ARGS+=(--icon "$ICON_ICNS")
fi

# Add hidden imports
for mod in "${HIDDEN_IMPORTS[@]}"; do
  BUILD_ARGS+=(--hidden-import "$mod")
done

# Add data files and collections
BUILD_ARGS+=(
  --add-data "transformer:transformer"
  --add-data "templates:templates"
  --add-data "static:static"
  --add-data "nltk_data:nltk_data"
  --add-data "icon.icns:icon.icns"
)

# Add collect arguments
for arg in "${COLLECT_ARGS[@]}"; do
  BUILD_ARGS+=("$arg")
done

# Run PyInstaller
echo "Building with PyInstaller..."
"$PYBIN" -m PyInstaller "${BUILD_ARGS[@]}" "$ENTRYPOINT"

# Verify app was created
APP_PATH="$DIST_DIR/${APP_NAME}.app"
if [ ! -d "$APP_PATH" ]; then
  echo "❌ PyInstaller build failed; .app not found at $APP_PATH"
  exit 1
fi

echo "✓ Native app created successfully at $APP_PATH"

# Ensure icon is embedded in the app bundle
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
  echo "🎉 SUCCESS! Native DMG created successfully!"
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
