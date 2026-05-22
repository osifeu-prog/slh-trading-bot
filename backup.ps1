$date = Get-Date -Format "yyyyMMdd_HHmm"
$backupDir = "C:\Users\USER\Desktop\SLH\Backups\algo-bot_$date"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Copy-Item -Path "C:\Users\USER\Desktop\SLH\algo-bot\*" -Destination $backupDir -Recurse -Exclude @("venv","__pycache__","*.pyc",".git","ngrok.exe","ngrok.zip") -Force
Compress-Archive -Path $backupDir -DestinationPath "$backupDir.zip" -Force
Remove-Item $backupDir -Recurse -Force
Write-Host "Backup created: $backupDir.zip" -ForegroundColor Green
