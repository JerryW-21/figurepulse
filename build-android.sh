#!/bin/bash
# =============================================
# MuskTracker Android Build Script
# 用法: bash build-android.sh
# 需要: Android Studio 或 Android SDK
# =============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANDROID_DIR="$SCRIPT_DIR/android"
WWW_DIR="$ANDROID_DIR/app/src/main/assets/www"

echo "=== MuskTracker APK Builder ==="

# Step 1: Copy latest PWA files to Android assets
echo "[1/4] Syncing PWA files to assets..."
mkdir -p "$WWW_DIR/icons"
cp "$SCRIPT_DIR/index.html" "$WWW_DIR/"
cp "$SCRIPT_DIR/manifest.json" "$WWW_DIR/"
cp "$SCRIPT_DIR/sw.js" "$WWW_DIR/"
cp "$SCRIPT_DIR/icons/"* "$WWW_DIR/icons/" 2>/dev/null || true
echo "  Done."

# Step 2: Check for Android SDK
if [ -z "$ANDROID_HOME" ]; then
    if [ -d "$HOME/Android/Sdk" ]; then
        export ANDROID_HOME="$HOME/Android/Sdk"
    elif [ -d "$HOME/Library/Android/sdk" ]; then
        export ANDROID_HOME="$HOME/Library/Android/sdk"
    fi
fi

if [ ! -d "$ANDROID_HOME" ]; then
    echo ""
    echo "[ERROR] Android SDK not found."
    echo "  Set ANDROID_HOME or install Android Studio."
    echo "  Then create $ANDROID_DIR/local.properties with:"
    echo "  sdk.dir=/path/to/Android/Sdk"
    exit 1
fi

# Step 3: Write local.properties
echo "[2/4] Configuring SDK path..."
echo "sdk.dir=$ANDROID_HOME" > "$ANDROID_DIR/local.properties"
echo "  SDK: $ANDROID_HOME"

# Step 4: Build APK
echo "[3/4] Building debug APK (this may take a few minutes)..."
cd "$ANDROID_DIR"

# Use gradlew if exists, otherwise need Android Studio
if [ -f "./gradlew" ]; then
    ./gradlew assembleDebug
elif command -v gradle &> /dev/null; then
    gradle assembleDebug
else
    echo ""
    echo "[ERROR] Gradle not found. Options:"
    echo "  1. Open $ANDROID_DIR in Android Studio and click Build > Build APK"
    echo "  2. Install Gradle: brew install gradle (macOS) or sdk install gradle (Linux)"
    exit 1
fi

# Step 5: Report result
APK="$ANDROID_DIR/app/build/outputs/apk/debug/app-debug.apk"
if [ -f "$APK" ]; then
    SIZE=$(ls -lh "$APK" | awk '{print $5}')
    echo "[4/4] APK built successfully!"
    echo ""
    echo "  Location: $APK"
    echo "  Size: $SIZE"
    echo ""
    echo "  Install on device: adb install $APK"
else
    echo "[4/4] Build may have failed. Check errors above."
    exit 1
fi
