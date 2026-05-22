Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SLH AGENT HANDOFF PACKAGE" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$outputDir = "handoff_$(Get-Date -Format 'yyyyMMdd_HHmm')"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

# Copy real existing files only
$files = @(
    "TASKS.md",
    "docs\slh-ui-plan.md",
    "docs\slh-project-management.md",
    "core\rbac_engine.py",
    "SLH_JOURNAL.md",
    "main_live.py",
    "supervisor_agent.py",
    "main_telegram.py",
    "docker-compose.yml",
    "Dockerfile",
    "requirements.txt",
    "start_ngrok.ps1",
    "slh-doctor.ps1",
    "slh-help.ps1",
    "slh-start-all.ps1",
    "slh-full-report.ps1"
)

foreach ($f in $files) {
    if (Test-Path $f) {
        $dest = Join-Path $outputDir $f
        New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
        Copy-Item $f $dest -Force
    }
}

@"
# SLH Agent Handoff Package
Generated: $(Get-Date)

This package contains the current state of the SLH Trading Bot project.
Please review TASKS.md for remaining tasks.

## Quick Start
- Run `.\slh-start-all.ps1` to start all services.
- Open `http://localhost:3000` for the dashboard.
- Use @SLH_Supervisor_bot on Telegram for commands.

## Files included
$($files -join "`n")
"@ | Set-Content -Path "$outputDir\README.md"

Compress-Archive -Path $outputDir -DestinationPath "$outputDir.zip" -Force
Remove-Item $outputDir -Recurse -Force
Write-Host "Handoff package: $outputDir.zip" -ForegroundColor Green
Write-Host "Send this to the executing agent." -ForegroundColor Yellow
