while ($true) {
    Write-Host "Starting Telegram bot..." -ForegroundColor Cyan
    $proc = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main_telegram.py" -PassThru -NoNewWindow
    $proc.WaitForExit()
    Write-Host "Bot stopped (exit code $($proc.ExitCode)). Restarting in 3 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}
