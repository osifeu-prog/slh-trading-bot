Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     SLH FULL SYSTEM REPORT" -ForegroundColor Yellow
Write-Host "     Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`n--- SYSTEM DOCTOR ---" -ForegroundColor Green
& ".\slh-doctor.ps1"

Write-Host "`n--- TASKS ---" -ForegroundColor Green
Get-Content "TASKS.md"

Write-Host "`n--- JOURNAL (last 10) ---" -ForegroundColor Green
Get-Content "C:\Users\USER\Desktop\SLH\SLH_JOURNAL.md" -Tail 10

Write-Host "`n--- TELEGRAM CHECK ---" -ForegroundColor Green
Write-Host "Send /start to @SLH_Test_bot and @SLH_Supervisor_bot"
Write-Host "Supervisor commands: /health, /menu, /tasks, /restart, /logs, /wake, /task"
Write-Host "Main bot commands: /status, /pnl, /positions, /help"

Write-Host "`n--- DOCKER CONTAINERS ---" -ForegroundColor Green
docker ps

Write-Host "`n--- PYTHON PROCESSES ---" -ForegroundColor Green
Get-Process -Name "python" -ErrorAction SilentlyContinue | Select Id, CommandLine | Format-Table -AutoSize

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " Copy the above output to share with agents." -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
