# slh-status.ps1 - RUN THIS OFTEN
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SLH TRADING BOT - LIVE STATUS 05/23/2026 18:29:38" -ForegroundColor Green
Write-Host "========================================="

docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Invoke-WebRequest http://localhost:8080/health -UseBasicParsing -ErrorAction SilentlyContinue | Select-Object Content

Write-Host "
Supervisor Status:" -ForegroundColor Yellow
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {.CommandLine -like "*supervisor*"}

Write-Host "
Next Milestone: Phase 10 - VPS" -ForegroundColor Magenta
