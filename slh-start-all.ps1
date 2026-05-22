Write-Host "Starting all SLH services..." -ForegroundColor Cyan
Set-Location "C:\Users\USER\Desktop\SLH\algo-bot"
Remove-Item "logs\*.lock" -Force -ErrorAction SilentlyContinue
docker-compose up -d
Start-Sleep -Seconds 15
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "supervisor_agent.py"
Start-Sleep -Seconds 3
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main_telegram.py"
Start-Sleep -Seconds 3
Set-Location "C:\Users\USER\Desktop\SLH\frontend"
if (-not (Get-Process -Name "node" -ErrorAction SilentlyContinue)) {
    Start-Process cmd -ArgumentList "/c npm run dev" -WindowStyle Minimized
}
Write-Host "? All SLH services started." -ForegroundColor Green
