Write-Host "SLH Watchdog – checking agents..." -ForegroundColor Cyan

# Supervisor
$supLock = Test-Path "logs\supervisor.lock"
$supProc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*supervisor*" }
if (-not $supProc -and $supLock) {
    Write-Host "Supervisor down, restarting..." -ForegroundColor Yellow
    Remove-Item "logs\supervisor.lock" -Force -ErrorAction SilentlyContinue
    Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "supervisor_agent.py"
}

# Main Telegram Listener
$mainLock = Test-Path "logs\main_telegram.lock"
$mainProc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*main_telegram*" }
if (-not $mainProc -and $mainLock) {
    Write-Host "Main Telegram listener down, restarting..." -ForegroundColor Yellow
    Remove-Item "logs\main_telegram.lock" -Force -ErrorAction SilentlyContinue
    Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main_telegram.py"
}

# Docker container
$container = docker ps --filter "name=slh_bot" --format "{{.Names}}"
if ($container -ne "slh_bot") {
    Write-Host "Docker container down, starting..." -ForegroundColor Yellow
    docker-compose up -d
}

Write-Host "Watchdog check complete." -ForegroundColor Green
