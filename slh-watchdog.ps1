Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SLH WATCHDOG PRO MAX" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$score = 100

if (!(Test-Path logs)) { New-Item logs -ItemType Directory | Out-Null }

$log = "logs\watchdog.log"

function LogMsg {
    param($msg)

    $t = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content $log "$t | $msg"
    Write-Host $msg
}

# API CHECK
try {
    Invoke-RestMethod http://localhost:8080/health | Out-Null
    LogMsg "[PASS] API healthy"
}
catch {
    LogMsg "[FAIL] API down"
    $score -= 15
}

# CONTAINERS CHECK
$containers = @("slh_api","slh_frontend","slh_trader","slh_supervisor")

foreach ($c in $containers) {
    $exists = docker ps --format "{{.Names}}" | Select-String $c

    if ($exists) {
        LogMsg "[PASS] $c running"
    }
    else {
        LogMsg "[FAIL] $c missing -> restarting stack"
        docker compose up -d
        $score -= 10
    }
}

# HEARTBEAT
if (Test-Path ".\logs\heartbeat.txt") {
    LogMsg "[PASS] Heartbeat OK"
}
else {
    LogMsg "[WARN] No heartbeat"
    $score -= 5
}

# FINAL SCORE
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " HEALTH SCORE: $score / 100" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

@{time=(Get-Date);score=$score} | ConvertTo-Json | Set-Content .\SLH_SCORE.json
