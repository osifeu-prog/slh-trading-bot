Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     SLH SYSTEM BOOTSTRAP ORCHESTRATOR" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$steps = @(
    @{Name="Validate .env"; Action={ if (-not (Test-Path ".env")) { throw ".env missing" } }},
    @{Name="Clean stale locks"; Action={ Remove-Item "logs\*.lock" -Force -ErrorAction SilentlyContinue }},
    @{Name="Start Docker Compose"; Action={ docker-compose up -d; Start-Sleep -Seconds 15 }},
    @{Name="Wait for Docker health"; Action={
        $retries = 0
        while ($retries -lt 10) {
            $status = docker ps --filter "name=slh_bot" --format "{{.Status}}"
            if ($status -match "Up") { break }
            $retries++
            Start-Sleep -Seconds 5
        }
    }},
    @{Name="Start Supervisor Agent"; Action={ Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "supervisor_agent.py"; Start-Sleep -Seconds 5 }},
    @{Name="Start Main Telegram Listener"; Action={ Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main_telegram.py"; Start-Sleep -Seconds 5 }},
    @{Name="Start Dashboard (Frontend)"; Action={
        Set-Location "C:\Users\USER\Desktop\SLH\frontend"
        if (-not (Get-Process -Name "node" -ErrorAction SilentlyContinue)) {
            Start-Process cmd -ArgumentList "/c npm run dev" -WindowStyle Minimized
        }
        Set-Location "C:\Users\USER\Desktop\SLH\algo-bot"
        Start-Sleep -Seconds 5
    }},
    @{Name="Write Agent Registry"; Action={
        $reg = @{
            agents = @(
                @{id="main_bot"; status="active"; last_seen=(Get-Date -Format "o"); pid=$null},
                @{id="supervisor"; status="active"; last_seen=(Get-Date -Format "o"); pid=(Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*supervisor*" } | Select -ExpandProperty Id)},
                @{id="telegram_listener"; status="active"; last_seen=(Get-Date -Format "o"); pid=(Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*main_telegram*" } | Select -ExpandProperty Id)}
            )
        }
        $reg | ConvertTo-Json -Depth 3 | Set-Content -Path "runtime\agent_registry.json"
    }},
    @{Name="Verify Heartbeat"; Action={
        $hb = Get-Content "logs\heartbeat.txt" -Raw | ConvertFrom-Json
        $age = ((Get-Date) - [DateTime]::Parse($hb.timestamp)).TotalSeconds
        if ($age -gt 60) { Write-Host "WARNING: Heartbeat age is ${age}s" -ForegroundColor Yellow }
    }}
)

foreach ($step in $steps) {
    Write-Host ">>> $($step.Name)" -ForegroundColor Cyan
    try {
        & $step.Action
        Write-Host "  OK" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $_" -ForegroundColor Red
        Write-Host "  Retrying once..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        try {
            & $step.Action
            Write-Host "  OK (retry)" -ForegroundColor Green
        } catch {
            Write-Host "  FAILED again. Continuing..." -ForegroundColor Red
        }
    }
}
Write-Host "`nBootstrap complete." -ForegroundColor Green
