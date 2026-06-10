Write-Host ""
Write-Host "========================"
Write-Host " SLH CONTROL TOWER"
Write-Host "========================"
Write-Host ""

docker compose ps

Write-Host ""
Write-Host "API:"
try {
    Invoke-RestMethod http://localhost:8080/health
}
catch {
    Write-Host "OFFLINE"
}

Write-Host ""
Write-Host "STATE:"
Get-Content .\SLH_STATE.json

Write-Host ""
Write-Host "KNOWN BUGS:"
Get-Content .\docs\KNOWN_BUGS.md
