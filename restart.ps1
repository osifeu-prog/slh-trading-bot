# =============================================
# SLH Trading Bot – Complete Restart Guide
# =============================================
# Run this script from any PowerShell to restart the bot.

$base = "C:\Users\USER\Desktop\SLH\algo-bot"
Set-Location $base

# 1. Activate venv
Write-Host "Activating Python venv..." -ForegroundColor Cyan
$venvPython = ".\venv\Scripts\python.exe"

# 2. Install dependencies if missing
Write-Host "Checking dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install -r requirements.txt --quiet 2>$null
& $venvPython -m pip install scikit-learn joblib fastapi uvicorn pycoingecko --quiet 2>$null

# 3. Ensure .env exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file missing. Create it with your API keys." -ForegroundColor Red
    exit
}

# 4. Start the bot
Write-Host "Starting SLH Trading Bot..." -ForegroundColor Green
& $venvPython main_live.py
