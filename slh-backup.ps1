
$date = Get-Date -Format yyyyMMdd_HHmmss

$target = "backups\daily\backup_$date"

New-Item -ItemType Directory -Force $target

Copy-Item docker-compose.yml $target -Force

if(Test-Path .env){
    Copy-Item .env $target -Force
}

Copy-Item TASKS.md $target -Force

if(Test-Path PHASE12_ROADMAP.md){
    Copy-Item PHASE12_ROADMAP.md $target -Force
}

if(Test-Path docs){
    Copy-Item docs $target -Recurse -Force
}

if(Test-Path agents){
    Copy-Item agents $target -Recurse -Force
}

Copy-Item main.py $target -Force

if(Test-Path supervisor_agent.py){
    Copy-Item supervisor_agent.py $target -Force
}

Write-Host ""
Write-Host "BACKUP CREATED:"
Write-Host $target

