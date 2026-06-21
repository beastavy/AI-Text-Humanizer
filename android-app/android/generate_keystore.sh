#!/bin/bash
set -e

echo "============================================="
echo "🔑 AI Text Humanizer Pro - Keystore Generator"
echo "============================================="
echo ""
echo "This script will generate a secure production keystore for the Google Play Store"
echo "and automatically configure your local keystore.properties file."
echo ""

# Find a valid keytool command
KEYTOOL_CMD="keytool"
if [ -d "/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home" ]; then
    KEYTOOL_CMD="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home/bin/keytool"
elif [ -d "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home" ]; then
    KEYTOOL_CMD="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home/bin/keytool"
fi

# Prompt for passwords
read -s -p "Enter Keystore Password (minimum 6 characters): " PASSWORD
echo ""
read -s -p "Confirm Keystore Password: " PASSWORD_CONFIRM
echo ""

if [ "$PASSWORD" != "$PASSWORD_CONFIRM" ]; then
    echo "❌ Error: Passwords do not match!"
    exit 1
fi

if [ ${#PASSWORD} -lt 6 ]; then
    echo "❌ Error: Password must be at least 6 characters!"
    exit 1
fi

ALIAS="humanizer-key"
KEYSTORE_PATH="app/release.keystore"
PROPERTIES_PATH="../keystore.properties"

# Generate Keystore
echo ""
echo "Generating keystore..."
"$KEYTOOL_CMD" -genkeypair \
  -v \
  -keystore "$KEYSTORE_PATH" \
  -alias "$ALIAS" \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "$PASSWORD" \
  -keypass "$PASSWORD" \
  -dname "CN=Obsidian AI Labs, OU=Mobile Development, O=Obsidian AI Labs, L=San Francisco, S=California, C=US"

# Write to keystore.properties
echo "Writing configuration to keystore.properties..."
cat << EOF > "$PROPERTIES_PATH"
storePassword=$PASSWORD
keyPassword=$PASSWORD
keyAlias=$ALIAS
storeFile=release.keystore
EOF

echo ""
echo "✅ Success! Keystore generated and configured."
echo "🔒 Note: 'release.keystore' and 'keystore.properties' are ignored by Git and will remain secure on your machine."
