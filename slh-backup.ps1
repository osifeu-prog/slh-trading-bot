$date = Get-Date -Format yyyyMMdd_HHmmss
$target = "backups\daily\backup_$date"

New-Item -ItemType Directory -Force $target | Out-Null

Copy-Item docker-compose.yml $target -Force -ErrorAction SilentlyContinue
Copy-Item TASKS.md $target -Force -ErrorAction SilentlyContinue
Copy-Item .gitignore $target -Force -ErrorAction SilentlyContinue
Copy-Item main.py $target -Force -ErrorAction SilentlyContinue

if(Test-Path docs){ Copy-Item docs $target -Recurse -Force }
if(Test-Path agents){ Copy-Item agents $target -Recurse -Force }

Write-Host "BACKUP CREATED: $target"
