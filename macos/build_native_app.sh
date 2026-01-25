#!/bin/bash
set -euo pipefail

APP_NAME="AI Text Humanizer Pro"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build/macos-native"
DMG_STAGING="$BUILD_DIR/dmg-staging"
DMG_OUTPUT="$BUILD_DIR/${APP_NAME}.dmg"
ENTRYPOINT="gui/qt_app.py"
ICON_ICNS="$PROJECT_ROOT/icon.icns"
NLTK_DIR="$PROJECT_ROOT/nltk_data"

echo "[1/8] Preparing build directories"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR" "$DMG_STAGING" "$NLTK_DIR"

if [ ! -f "$PROJECT_ROOT/$ENTRYPOINT" ]; then
  echo "❌ Entrypoint $ENTRYPOINT not found."
  exit 1
fi

# Ensure icon exists
if [ ! -f "$ICON_ICNS" ]; then
  echo "⚠️ icon.icns not found at project root; the app will use default icon."
fi

cd "$PROJECT_ROOT"

# Choose the best available Python for the build (prefers >=3.10)
choose_python() {
  if [ -n "${PYTHON:-}" ] && command -v "$PYTHON" >/dev/null 2>&1; then
    echo "$PYTHON"; return 0
  fi
  for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" >/dev/null 2>&1; then
      echo "$cmd"; return 0
    fi
  done
  echo "python3"
}

PY_CMD=$(choose_python)
echo "[2/8] Using interpreter: $PY_CMD"

# Create isolated build venv to avoid polluting user env
echo "[2/8] Creating isolated build virtualenv"
"$PY_CMD" -m venv "$BUILD_DIR/.build-venv"
PYBIN="$BUILD_DIR/.build-venv/bin/python"
PIPBIN="$BUILD_DIR/.build-venv/bin/pip"

PYVER=$("$PYBIN" - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)
echo "[3/8] Detected Python $PYVER in build venv"

case "$PYVER" in
  3.10|3.11|3.12) ;; # ok
  *)
    echo "❌ Python $PYVER is not supported for this build. Please install Python 3.10+ and rerun."
    echo "   You can set PYTHON to the desired interpreter, e.g.:"
    echo "   PYTHON=/opt/homebrew/bin/python3.11 ./macos/build_native_app.sh"
    exit 1
    ;;
esac

echo "[3/8] Installing project requirements (this can take a while)"
"$PIPBIN" install --upgrade pip wheel >/dev/null

"$PIPBIN" install -r requirements.txt >/dev/null

# Prefetch NLP resources into project-local folders
echo "[4/8] Prefetching NLP resources (NLTK + spaCy model)"
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
        print(f"nltk: downloaded {r}")
    except Exception as e:
        print(f"nltk: failed {r}: {e}")

# Ensure spaCy model is importable (installed by requirements)
try:
    nlp = spacy.load('en_core_web_sm')
    print('spacy: en_core_web_sm is available')
except Exception as e:
    print('spacy: en_core_web_sm missing or failed to load:', e)
PY

# Ensure PyInstaller
echo "[5/8] Installing PyInstaller"
"$PIPBIN" install --upgrade pyinstaller >/dev/null

echo "[6/8] Bundling native app with PyInstaller"

COMMON_HIDDEN_IMPORTS=(
  nltk
  spacy
  spacy.lang.en
  srsly
  thinc
  cymem
  preshed
  blis
  murmurhash
)

HIDDEN_IMPORT_ARGS=()
for mod in "${COMMON_HIDDEN_IMPORTS[@]}"; do
  HIDDEN_IMPORT_ARGS+=(--hidden-import "$mod")
done

ICON_ARG=()
if [ -f "$ICON_ICNS" ]; then
  ICON_ARG=(--icon "$ICON_ICNS")
fi

# Use --collect-all to ensure spaCy model and data files are included
COLLECT_ARGS=(
  --collect-all spacy
  --collect-all en_core_web_sm
  --collect-all sentence_transformers
  --collect-all transformers
  --collect-all tokenizers
  --collect-all torch
)

"$PYBIN" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  "${ICON_ARG[@]}" \
  "${HIDDEN_IMPORT_ARGS[@]}" \
  "${COLLECT_ARGS[@]}" \
  --add-data "transformer:transformer" \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --add-data "nltk_data:nltk_data" \
  "$ENTRYPOINT"

APP_PATH="$PROJECT_ROOT/dist/${APP_NAME}.app"
if [ ! -d "$APP_PATH" ]; then
  echo "❌ PyInstaller build failed; .app not found at $APP_PATH"
  exit 1
fi

# Optional: ensure app has icon embedded inside Resources
if [ -f "$ICON_ICNS" ]; then
  echo "[7/8] Embedding icon into app bundle"
  RES_DIR="$APP_PATH/Contents/Resources"
  mkdir -p "$RES_DIR"
  cp "$ICON_ICNS" "$RES_DIR/icon.icns"
  PLIST="$APP_PATH/Contents/Info.plist"
  /usr/libexec/PlistBuddy -c "Add :CFBundleIconFile string icon.icns" "$PLIST" 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Set :CFBundleIconFile icon.icns" "$PLIST" 2>/dev/null || true
fi

# Create DMG staging
echo "[8/8] Creating DMG"
rm -rf "$DMG_STAGING"
mkdir -p "$DMG_STAGING"
ln -s /Applications "$DMG_STAGING/Applications"
cp -R "$APP_PATH" "$DMG_STAGING/"
rm -f "$DMG_OUTPUT"
hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_STAGING" -ov -format UDZO "$DMG_OUTPUT"

echo "\n✅ Native DMG created at: $DMG_OUTPUT"
