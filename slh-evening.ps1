$date = Get-Date

Write-Host ""
Write-Host "SLH EVENING REPORT"
Write-Host ""

$report = @"
Date: $date

Completed Today:

Issues Found:

Tomorrow:

"@

$report | Out-File .\docs\DAILY_REPORT.txt

notepad .\docs\DAILY_REPORT.txt
