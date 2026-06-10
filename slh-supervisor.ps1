# SLH SUPERVISOR - AUTO RECOVERY DAEMON

$BOT_PATH = "C:\Users\USER\Desktop\SLH\algo-bot\run_trader.py"
$PYTHON = ".\venv\Scripts\python.exe"

while ($true) {

    Write-Host "[$(Get-Date)] Starting SLH Trader..." -ForegroundColor Green

    try {
        Start-Process -NoNewWindow -FilePath $PYTHON -ArgumentList $BOT_PATH -Wait
    }
    catch {
        Write-Host "Bot crashed! Restarting..." -ForegroundColor Red
    }

    Write-Host "Restarting in 3 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}