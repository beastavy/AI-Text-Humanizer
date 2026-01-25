#!/usr/bin/env python3
"""
PyInstaller configuration for AI Text Humanizer Pro macOS app
"""

import os
import sys
from pathlib import Path

# Get the project root
PROJECT_ROOT = Path(__file__).parent
MACOS_DIR = PROJECT_ROOT / "macos"
ICON_PATH = PROJECT_ROOT / "icon.icns"

# PyInstaller spec configuration
spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

# Analysis configuration
a = Analysis(
    ['{PROJECT_ROOT / "macos_app.py"}'],
    pathex=['{PROJECT_ROOT}'],
    binaries=[],
    datas=[
        ('{ICON_PATH}', '.') if ICON_PATH.exists() else ('', ''),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'torch',
        'transformers',
        'spacy',
        'nltk',
        'streamlit',
        'altair',
        'notebook',
        'jupyterlab',
        'ipython',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ configuration
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

# EXE configuration
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
    argv_emulation=True,
    target_arch='universal2',  # For Apple Silicon and Intel Macs
    codesign_identity=None,
    entitlements_file=None,
    icon='{ICON_PATH}' if ICON_PATH.exists() else None,
)

# COLLECT configuration
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI Text Humanizer Pro',
)

# macOS App Bundle configuration
app = BUNDLE(
    coll,
    name='AI Text Humanizer Pro.app',
    icon='{ICON_PATH}' if ICON_PATH.exists() else None,
    bundle_identifier='com.aitexthumanizer.pro',
    version='1.0.0',
    info_plist={{
        'CFBundleDisplayName': 'AI Text Humanizer Pro',
        'CFBundleName': 'AI Text Humanizer Pro',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1',
        'CFBundleExecutable': 'AI Text Humanizer Pro',
        'CFBundleIdentifier': 'com.aitexthumanizer.pro',
        'CFBundleIconFile': 'icon.icns',
        'LSMinimumSystemVersion': '10.13',
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'NSHighResolutionCapable': True,
        'NSSupportsAutomaticGraphicsSwitching': True,
        'NSHumanReadableCopyright': '© 2024 AI Text Humanizer Pro. All rights reserved.',
    }},
)
"""

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_path = PROJECT_ROOT / "build_macos_app.spec"
    with open(spec_path, "w") as f:
        f.write(spec_content)
    print(f"Created spec file: {spec_path}")
    return spec_path

if __name__ == "__main__":
    create_spec_file()
