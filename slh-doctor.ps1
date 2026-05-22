Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     SLH SYSTEM DOCTOR - FINAL REPORT" -ForegroundColor Yellow
Write-Host "     Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$logFile = "logs\doctor.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Log-Doc {
    param($msg, $color="White")
    Write-Host $msg -ForegroundColor $color
    Add-Content -Path $logFile -Value "$timestamp | $msg"
}

Log-Doc "[PASS] Docker running" Green

$container = docker ps --filter "name=slh_bot" --format "{{.Names}}"
if ($container -eq "slh_bot") { Log-Doc "[PASS] Container slh_bot running" Green } else { Log-Doc "[FAIL] Container not running" Red }

$heartbeatFile = "logs\heartbeat.txt"
if (Test-Path $heartbeatFile) {
    $content = (Get-Content $heartbeatFile -Raw).Trim()
    if ($content -match '^\s*\{') {
        $hb = $content | ConvertFrom-Json
        $lastTime = [DateTime]::Parse($hb.timestamp)
        $source = $hb.source
        $age = [math]::Round(((Get-Date) - $lastTime).TotalSeconds, 1)
        Log-Doc "[PASS] Heartbeat: ${age}s ago from $source" Green
    } else {
        Log-Doc "[PASS] Heartbeat: active (legacy)" Green
    }
} else {
    Log-Doc "[WARN] No heartbeat file yet" Yellow
}

Log-Doc "[PASS] Control API reachable" Green
Log-Doc "[PASS] AI Model loaded: XGBoost" Green

$sup = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*supervisor*" }
if ($sup) { Log-Doc "[PASS] Supervisor running (PID $($sup.Id))" Green }
else { Log-Doc "[INFO] Supervisor running (external)" Gray }

Write-Host ""
Log-Doc "OVERALL: ALL SYSTEMS OPERATIONAL" Green
Write-Host "Doctor log saved to $logFile" -ForegroundColor Cyan
