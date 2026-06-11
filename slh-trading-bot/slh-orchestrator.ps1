Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     SLH ORCHESTRATOR v1 - STARTING" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

$stateFile = "runtime\orchestrator_state.json"
$logFile = "logs\orchestrator.log"

function Write-OrchLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $Message" | Tee-Object -FilePath $logFile -Append
    Write-Host "$timestamp | $Message" -ForegroundColor Gray
}

# Update State
$containerStatus = docker ps --filter "name=slh_bot" --format "{{.Status}}"
$apiAlive = try { 
    $null = Invoke-RestMethod -Uri "http://localhost:8080/api/system/status" -TimeoutSec 3 -UseBasicParsing
    $true 
} catch { $false }

$state = @{
    timestamp = (Get-Date -Format "o")
    docker = if ($containerStatus -like "*Up*") { "UP" } else { "DOWN" }
    api = if ($apiAlive) { "ALIVE" } else { "DEAD" }
    heartbeat_age_minutes = 0
}

# Heartbeat check
if (Test-Path "logs\heartbeat.txt") {
    try {
        $hb = Get-Content "logs\heartbeat.txt" -Raw | ConvertFrom-Json
        $age = [math]::Round(((Get-Date) - [DateTime]::Parse($hb.timestamp)).TotalMinutes, 1)
        $state.heartbeat_age_minutes = $age
    } catch {}
}

$state | ConvertTo-Json | Set-Content $stateFile -Force

# Decision Logic
if ($state.docker -ne "UP" -or $state.api -ne "ALIVE" -or $state.heartbeat_age_minutes -gt 5) {
    Write-OrchLog "System unhealthy → Repairing..."
    docker-compose down
    Start-Sleep -Seconds 3
    docker-compose up -d
    Start-Sleep -Seconds 8
    Write-OrchLog "Repair completed"
} else {
    Write-OrchLog "System Stable"
}

Write-Host "`nOrchestrator check completed. Status: $($state.docker) | API: $($state.api) | Heartbeat age: $($state.heartbeat_age_minutes) min" -ForegroundColor Green
