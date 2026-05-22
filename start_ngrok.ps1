Write-Host "Starting Ngrok tunnel to dashboard..." -ForegroundColor Cyan
# Download ngrok if not present
if (-not (Test-Path "ngrok.exe")) {
    Invoke-WebRequest -Uri "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip" -OutFile "ngrok.zip"
    Expand-Archive ngrok.zip -DestinationPath . -Force
    Remove-Item ngrok.zip
}
Start-Process -NoNewWindow -FilePath ".\ngrok.exe" -ArgumentList "http 8080"
Write-Host "Ngrok tunnel started. Check https://dashboard.ngrok.com/status for public URL" -ForegroundColor Green
