# SLH Progress Tracker
$startTime = Get-Date
function Show-Progress {
    $elapsed = (Get-Date) - $startTime
    Write-Host "⏱ זמן עבודה: " -ForegroundColor Cyan
}

# דוגמה לשימוש:
Show-Progress
Write-Host "Phase 8 (Security) - 70% complete" 
