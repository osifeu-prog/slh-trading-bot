$envFile = ".env"
$backup = "config/backups/env_$(Get-Date -Format 'yyyyMMdd_HHmmss').bak"
Copy-Item $envFile $backup -Force

$newTokens = @{
    "SUPERVISOR_BOT_TOKEN" = "8929094112:AAFvkCT4DQCG-c2g3N2h0_dVcayms0bdkas"
    "BINANCE_API_KEY" = "InV737ztDrr13x8YaShhIpyTqIZd2c01G3tmVHn3109rZDl1d7CY3S1tw39DgnVh"
    "BINANCE_SECRET_KEY" = "XTL71c2Ve1MdwbsSwvLfRsxrSUUL2KBQwZxgCqKDdFuE42FMy4hkEP5SxVAHcuYl"
    "TELEGRAM_TOKEN" = "7591051736:AAHxhszZOoUcpO17ImDf26pxSPe0w9lVrIg"
    "TELEGRAM_CHAT_ID" = "-5294800328"
    "JWT_SECRET_KEY" = "a4fd3233-a996-4f3a-8a42-64f01ec347f15596e38b-c8f9-4b80-afaa-0d217aec000c"
}

$content = Get-Content $envFile -Raw
foreach ($key in $newTokens.Keys) {
    $content = $content -replace "$key=.*", "$key=$($newTokens[$key])"
}
$content | Set-Content $envFile -Encoding utf8

Write-Host "✅ Tokens rotated. Backup: $backup" -ForegroundColor Green
docker compose restart
