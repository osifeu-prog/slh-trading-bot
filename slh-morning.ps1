Write-Host ""
Write-Host "================================="
Write-Host " GOOD MORNING - SLH SYSTEM"
Write-Host "================================="
Write-Host ""

docker compose up -d

Start-Sleep 10

docker compose ps

Write-Host ""
Write-Host "API HEALTH:"
try {
    Invoke-RestMethod http://localhost:8080/health
}
catch {
    Write-Host "API OFFLINE"
}

Write-Host ""
Write-Host "Opening Dashboard..."

Start-Process "http://localhost:3000"
Start-Process "http://localhost:8080/docs"

Write-Host ""
Write-Host "Today's Context:"
Get-Content .\docs\CHATGPT_CONTEXT.md
