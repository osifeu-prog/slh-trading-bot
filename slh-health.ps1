Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     SLH LIVE HEALTH PANEL" -ForegroundColor Yellow
Write-Host "     $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# CPU
$cpu = (Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
Write-Host "CPU: $cpu%" -ForegroundColor $(if($cpu -lt 50){"Green"}elseif($cpu -lt 80){"Yellow"}else{"Red"})

# RAM
$os = Get-WmiObject Win32_OperatingSystem
$totalRAM = [math]::Round($os.TotalVisibleMemorySize/1MB, 1)
$freeRAM = [math]::Round($os.FreePhysicalMemory/1MB, 1)
$usedRAM = $totalRAM - $freeRAM
Write-Host "RAM: ${usedRAM}MB / ${totalRAM}MB ($([math]::Round($usedRAM/$totalRAM*100))%)" -ForegroundColor $(if($usedRAM/$totalRAM -lt 0.7){"Green"}else{"Yellow"})

# Disk
$disk = Get-PSDrive C
$diskUsed = [math]::Round(($disk.Used/1GB), 1)
$diskFree = [math]::Round(($disk.Free/1GB), 1)
Write-Host "Disk C: ${diskUsed}GB used, ${diskFree}GB free" -ForegroundColor $(if($diskFree -gt 10){"Green"}else{"Red"})

# Docker
$dockerStatus = docker ps --filter "name=slh_bot" --format "{{.Status}}"
if ($dockerStatus -match "Up") { Write-Host "Docker: ACTIVE ($dockerStatus)" -ForegroundColor Green }
else { Write-Host "Docker: INACTIVE" -ForegroundColor Red }

# Heartbeat
$hbFile = "logs\heartbeat.txt"
if (Test-Path $hbFile) {
    $hb = Get-Content $hbFile -Raw | ConvertFrom-Json
    $age = [math]::Round(((Get-Date) - [DateTime]::Parse($hb.timestamp)).TotalSeconds, 1)
    Write-Host "Heartbeat: ${age}s ago" -ForegroundColor $(if($age -lt 60){"Green"}else{"Red"})
} else { Write-Host "Heartbeat: MISSING" -ForegroundColor Red }

# Agents
Write-Host "`nAgents:"
$agents = @("supervisor", "main_telegram")
foreach ($a in $agents) {
    $proc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*$a*" }
    if ($proc) { Write-Host "  $a : ACTIVE (PID $($proc.Id))" -ForegroundColor Green }
    else { Write-Host "  $a : INACTIVE" -ForegroundColor Red }
}

# PnL (quick API call)
try {
    $pnl = Invoke-RestMethod -Uri "http://localhost:8080/api/trades/pnl" -TimeoutSec 3
    Write-Host "`nPnL: $($pnl.total_pnl) USDT | Win Rate: $($pnl.win_rate*100)% | Trades: $($pnl.total_trades)" -ForegroundColor Cyan
} catch { Write-Host "PnL: N/A" -ForegroundColor Gray }

# Last backup
$lastBackup = Get-ChildItem "C:\Users\USER\Desktop\SLH\Backups" -Filter "*.zip" | Sort-Object LastWriteTime -Descending | Select -First 1
if ($lastBackup) { Write-Host "Last Backup: $($lastBackup.LastWriteTime)" -ForegroundColor Green }
Write-Host "========================================" -ForegroundColor Cyan
