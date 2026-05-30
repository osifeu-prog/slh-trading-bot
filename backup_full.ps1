$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupRoot = "C:\Users\USER\Desktop\SLH\backups"
$snapshotDir = "$backupRoot\snapshot_$timestamp"
New-Item -ItemType Directory -Path $snapshotDir -Force | Out-Null

# 1. קבצי פרויקט (קוד + config)
Copy-Item -Path "C:\Users\USER\Desktop\SLH\algo-bot" -Destination "$snapshotDir\code" -Recurse -Force

# 2. .env (עם הסודות – נשמור מוצפן? כרגע רגיל)
Copy-Item "C:\Users\USER\Desktop\SLH\algo-bot\.env" "$snapshotDir\.env"

# 3. Docker images list
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}" > "$snapshotDir\docker_images.txt"

# 4. מצב containers (ps -a)
docker ps -a > "$snapshotDir\docker_ps.txt"

# 5. logs של כל containers
docker logs slh_api --tail 1000 > "$snapshotDir\api_logs.txt"
docker logs slh_trader --tail 1000 > "$snapshotDir\trader_logs.txt"
docker logs slh_supervisor --tail 1000 > "$snapshotDir\supervisor_logs.txt"

# 6. דחיסת התיקייה
Compress-Archive -Path "$snapshotDir" -DestinationPath "$backupRoot\slh_backup_$timestamp.zip" -Force
Remove-Item -Recurse -Force $snapshotDir

Write-Host "Backup completed: $backupRoot\slh_backup_$timestamp.zip"
