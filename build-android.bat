@echo off
REM =============================================
REM MuskTracker Android Build Script (Windows)
REM =============================================
setlocal enabledelayedexpansion

echo === MuskTracker APK Builder ===

REM Step 1: Copy latest PWA files
echo [1/3] Syncing PWA files to assets...
if not exist "android\app\src\main\assets\www" mkdir "android\app\src\main\assets\www"
if not exist "android\app\src\main\assets\www\icons" mkdir "android\app\src\main\assets\www\icons"
copy /Y "index.html" "android\app\src\main\assets\www\" >nul
copy /Y "manifest.json" "android\app\src\main\assets\www\" >nul
copy /Y "sw.js" "android\app\src\main\assets\www\" >nul
copy /Y "icons\*" "android\app\src\main\assets\www\icons\" >nul 2>nul
echo   Done.

REM Step 2: Check for Android Studio Gradle
echo [2/3] Looking for Gradle...
if exist "android\gradlew.bat" (
    echo   Using gradlew.bat
    cd android
    call gradlew.bat assembleDebug
    cd ..
) else (
    echo.
    echo [WARNING] gradlew.bat not found.
    echo   Open android\ folder in Android Studio.
    echo   Click Build ^> Build Bundle(s) / APK ^> Build APK(s^).
    echo.
    pause
    exit /b 0
)

REM Step 3: Done
set APK=android\app\build\outputs\apk\debug\app-debug.apk
if exist "%APK%" (
    echo [3/3] APK built successfully!
    echo   Location: %APK%
    echo   Install: adb install %APK%
) else (
    echo [3/3] Build may have failed. Check errors above.
)
pause
