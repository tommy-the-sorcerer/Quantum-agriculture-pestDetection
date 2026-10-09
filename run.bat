@echo off
title FALCON-Q Server
cd /d "%~dp0"
echo ===================================================
echo Starting FALCON-Q Server on http://localhost:8000
echo ===================================================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
)
pause

