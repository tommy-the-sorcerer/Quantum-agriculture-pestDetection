@echo off
title Push FALCON-Q Updates to GitHub
cd /d "%~dp0"
echo ===================================================
echo Pushing latest FALCON-Q commits to GitHub main...
echo ===================================================
git push origin main --force
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Successfully pushed all latest updates to GitHub!
) else (
    echo [ERROR] Push failed. Please verify your GitHub credentials.
)
pause
