Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "     SLH - SECURE TOKEN ROTATION TOOL v1.1" -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Cyan

$journalFile = "SLH_JOURNAL.md"
$backupDir = "config/backups/tokens_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

function Log-Rotation { param($msg); $entry = "`n## $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n**Task:** Token Rotation`n**Action:** $msg`n**Status:** Completed`n"; Add-Content -Path $journalFile -Value $entry; Write-Host $msg -ForegroundColor Green }

# Backup
Copy-Item ".env" "$backupDir/.env.backup" -Force
Log-Rotation "✅ .env backed up to $backupDir"

Write-Host "`n=== Telegram Supervisor Token ===" -ForegroundColor Cyan
$newSup = Read-Host "Enter NEW Supervisor Bot Token (or Enter to skip)"
if ($newSup) {
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace 'SUPERVISOR_BOT_TOKEN=.*', "SUPERVISOR_BOT_TOKEN=$newSup"
    $envContent | Set-Content ".env"
    Log-Rotation "✅ Supervisor Token rotated"
}

Write-Host "`n=== Binance API Keys ===" -ForegroundColor Cyan
$newKey = Read-Host "Enter NEW Binance API Key (or Enter to skip)"
$newSecret = Read-Host "Enter NEW Binance Secret Key (or Enter to skip)"

if ($newKey -and $newSecret) {
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace 'BINANCE_API_KEY=.*', "BINANCE_API_KEY=$newKey"
    $envContent = $envContent -replace 'BINANCE_SECRET_KEY=.*', "BINANCE_SECRET_KEY=$newSecret"
    $envContent | Set-Content ".env"
    Log-Rotation "✅ Binance Keys rotated"
}

Write-Host "`n✅ Token Rotation Completed!" -ForegroundColor Green
Write-Host "Backup: $backupDir" -ForegroundColor Cyan
Write-Host "Restart Docker + Supervisor to apply." -ForegroundColor Yellow

$restart = Read-Host "Restart now? (y/n)"
if ($restart -eq 'y') {
    Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
    docker-compose restart
    Start-Sleep -Seconds 8
    Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "supervisor_agent.py"
    Write-Host "✅ System restarted with new tokens" -ForegroundColor Green
}
