# FALCON-Q PowerShell Launcher
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Starting FALCON-Q Server on http://localhost:8000" -ForegroundColor Cyan
if (Test-Path "$ProjectDir\.venv\Scripts\python.exe") {
    & "$ProjectDir\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
} else {
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

