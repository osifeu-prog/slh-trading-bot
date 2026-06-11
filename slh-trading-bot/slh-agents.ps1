Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     SLH AGENT STATUS REPORT" -ForegroundColor Yellow
Write-Host "     Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Check Supervisor
$supLock = Test-Path "logs\supervisor.lock"
$supProc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*supervisor*" }
Write-Host "Supervisor Agent:" -ForegroundColor White
if ($supProc) { Write-Host "  Status: ACTIVE (PID $($supProc.Id))" -ForegroundColor Green }
elseif ($supLock) { Write-Host "  Status: STALE (lock exists but no process)" -ForegroundColor Yellow }
else { Write-Host "  Status: INACTIVE" -ForegroundColor Red }

# Check Main Telegram Listener
$mainLock = Test-Path "logs\main_telegram.lock"
$mainProc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*main_telegram*" }
Write-Host "Main Telegram Listener:" -ForegroundColor White
if ($mainProc) { Write-Host "  Status: ACTIVE (PID $($mainProc.Id))" -ForegroundColor Green }
elseif ($mainLock) { Write-Host "  Status: STALE (lock exists but no process)" -ForegroundColor Yellow }
else { Write-Host "  Status: INACTIVE" -ForegroundColor Red }

# Check Main Bot (Docker)
$container = docker ps --filter "name=slh_bot" --format "{{.Status}}"
Write-Host "Main Bot (Docker):" -ForegroundColor White
if ($container -match "Up") { Write-Host "  Status: ACTIVE ($container)" -ForegroundColor Green }
else { Write-Host "  Status: NOT RUNNING" -ForegroundColor Red }

# Check Heartbeat
$heartbeatFile = "logs\heartbeat.txt"
if (Test-Path $heartbeatFile) {
    $content = Get-Content $heartbeatFile -Raw
    if ($content -match '\{') {
        $hb = $content | ConvertFrom-Json
        $lastTime = [DateTime]::Parse($hb.timestamp)
        $age = [math]::Round(((Get-Date) - $lastTime).TotalSeconds, 1)
        Write-Host "Heartbeat: ${age}s ago from $($hb.source)" -ForegroundColor $(if($age -lt 120){"Green"}else{"Red"})
    }
} else { Write-Host "Heartbeat: MISSING" -ForegroundColor Red }

# Agents from agents.json
if (Test-Path "agents.json") {
    $agents = Get-Content "agents.json" | ConvertFrom-Json
    Write-Host "`nRegistered Agents:" -ForegroundColor Cyan
    foreach ($a in $agents.agents) {
        Write-Host "  $($a.id) ($($a.role)): $($a.status)" -ForegroundColor White
    }
}

Write-Host "========================================" -ForegroundColor Cyan
