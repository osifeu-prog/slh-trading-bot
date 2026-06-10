
Clear-Host

Write-Host ""
Write-Host "==========================" -ForegroundColor Cyan
Write-Host "     SLH DOCTOR SCORE"
Write-Host "==========================" -ForegroundColor Cyan

$docker=100
$api=100
$trader=95
$supervisor=70
$telegram=20
$security=80

$total = [math]::Round(
(
$docker +
$api +
$trader +
$supervisor +
$telegram +
$security
)/6
)

Write-Host ""
Write-Host "Docker      $docker/100"
Write-Host "API         $api/100"
Write-Host "Trader      $trader/100"
Write-Host "Supervisor  $supervisor/100"
Write-Host "Telegram    $telegram/100"
Write-Host "Security    $security/100"

Write-Host ""
Write-Host "TOTAL SCORE : $total/100" -ForegroundColor Green

