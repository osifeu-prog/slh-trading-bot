$ErrorActionPreference = "Continue"
$global:SLH_LOG_FILE = "logs\menu_output.log"

trap {
    Write-Host "ERROR: $_" -ForegroundColor Red
    pause
    continue
}

function Invoke-SLHAction {
    param([string]$Label, [scriptblock]$Action)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host " $Label" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    & $Action 2>&1 | Tee-Object -FilePath $global:SLH_LOG_FILE -Append
    Write-Host "`n[Output saved to $global:SLH_LOG_FILE]" -ForegroundColor Gray
    pause
}

function Show-SLHMenu {
    Write-Host "╔══════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║      SLH TRADING BOT - MASTER CONTROL       ║" -ForegroundColor Cyan
    Write-Host "╠══════════════════════════════════════════════╣" -ForegroundColor Cyan
    Write-Host "║ 1. Start/Re-start Main Bot                  ║" -ForegroundColor White
    Write-Host "║ 2. Start Ngrok (Dashboard remote access)     ║" -ForegroundColor White
    Write-Host "║ 3. Show Status & Tasks                      ║" -ForegroundColor White
    Write-Host "║ 4. View Journal (last 20 entries)           ║" -ForegroundColor White
    Write-Host "║ 5. Manual Backup                            ║" -ForegroundColor White
    Write-Host "║ 6. Restart Docker Container                 ║" -ForegroundColor White
    Write-Host "║ 7. View Docker Logs (live)                  ║" -ForegroundColor White
    Write-Host "║ 8. Start Supervisor AI Agent                ║" -ForegroundColor White
    Write-Host "║ 9. Generate Project Handoff Document        ║" -ForegroundColor White
    Write-Host "║ 10. FINAL SECURITY CHECK & TOKEN ROTATION   ║" -ForegroundColor Yellow
    Write-Host "║ 11. FULL SYSTEM TEST (no Telegram needed)   ║" -ForegroundColor White
    Write-Host "║ 12. SYSTEM DOCTOR (slh-doctor.ps1)         ║" -ForegroundColor White
    Write-Host "║ 13. VIEW TASKS (TASKS.md)                  ║" -ForegroundColor White
    Write-Host "║ 14. CREATE AGENT HANDOFF PACKAGE           ║" -ForegroundColor White
    Write-Host "║ 15. VIEW UI/UX PLAN                        ║" -ForegroundColor White
    Write-Host "║ 16. HELP (System overview)                 ║" -ForegroundColor White
    Write-Host "║ 17. FULL SYSTEM REPORT (copy-paste ready)  ║" -ForegroundColor White
    Write-Host "║ 18. AGENT STATUS REPORT                    ║" -ForegroundColor White
    Write-Host "║ 19. AUTO RECOVER SYSTEM (self-heal)       ║" -ForegroundColor Green
    Write-Host "║ 20. LIVE HEALTH PANEL                      ║" -ForegroundColor Green
    Write-Host "║ Q. Quit                                     ║" -ForegroundColor White
    Write-Host "╚══════════════════════════════════════════════╝" -ForegroundColor Cyan

    do {
        $choice = Read-Host "Enter choice"
        switch ($choice) {
            "1"  { Invoke-SLHAction "Start Bot" { .\restart.ps1 } }
            "2"  { Invoke-SLHAction "Start Ngrok" { .\start_ngrok.ps1 } }
            "3"  { Invoke-SLHAction "Status & Tasks" { & "C:\Users\USER\Desktop\SLH\slh-status.ps1" } }
            "4"  { Invoke-SLHAction "Journal" { Get-Content "C:\Users\USER\Desktop\SLH\SLH_JOURNAL.md" -Tail 20 } }
            "5"  { Invoke-SLHAction "Backup" { .\backup.ps1 } }
            "6"  { Invoke-SLHAction "Restart Docker" { docker-compose restart } }
            "7"  { docker logs -f slh_bot }
            "8"  {
                Remove-Item "logs\supervisor.lock" -Force -ErrorAction SilentlyContinue
                Invoke-SLHAction "Start Supervisor" { Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "supervisor_agent.py" }
            }
            "9"  { Invoke-SLHAction "Handoff Document" { .\generate_handoff.ps1 } }
            "10" { Invoke-SLHAction "Security Check" { .\pre_release_check.ps1 } }
            "11" { Invoke-SLHAction "Full System Test" { .\full_system_test.ps1 } }
            "12" { Invoke-SLHAction "System Doctor" { .\slh-doctor.ps1 } }
            "13" { Invoke-SLHAction "TASKS.md" { Get-Content "TASKS.md" } }
            "14" { Invoke-SLHAction "Agent Handoff Package" { .\agent_handoff.ps1 } }
            "15" { Invoke-SLHAction "UI/UX Plan" { Get-Content "docs\slh-ui-plan.md" } }
            "16" { Invoke-SLHAction "Help" { .\slh-help.ps1 } }
            "17" { Invoke-SLHAction "Full System Report" { .\slh-full-report.ps1 } }
            "18" { Invoke-SLHAction "Agent Status" { .\slh-agents.ps1 } }
            "19" { Invoke-SLHAction "Auto Recover" {
                Write-Host "Cleaning stale locks..." -ForegroundColor Cyan
                Remove-Item "logs\*.lock" -Force -ErrorAction SilentlyContinue
                docker-compose up -d
                Start-Sleep -Seconds 10
                Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "supervisor_agent.py"
                Start-Sleep -Seconds 3
                Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main_telegram.py"
                Write-Host "Recovery complete. Check Agent Status (18)." -ForegroundColor Green
            } }
            "20" { Invoke-SLHAction "Live Health Panel" { .\slh-health.ps1 } }
            "Q"  { return }
            "q"  { return }
            default { Write-Host "Invalid choice" -ForegroundColor Red; Start-Sleep -Seconds 1 }
        }
    } while ($choice -notmatch "^(Q|q)$")
}
