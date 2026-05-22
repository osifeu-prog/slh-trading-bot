Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SLH SYSTEM FULL HEALTH CHECK" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$errors = 0

# Docker
Write-Host "Checking Docker..." -ForegroundColor Cyan
$dockerOk = $false
try { docker ps > $null 2>&1; $dockerOk = $true } catch {}
if ($dockerOk) {
    Write-Host "  [PASS] Docker is running" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Docker not accessible" -ForegroundColor Red
    $errors++
}

# Container
Write-Host "Checking Container..." -ForegroundColor Cyan
$container = docker ps --filter "name=slh_bot" --format "{{.Names}}"
if ($container -eq "slh_bot") {
    Write-Host "  [PASS] Container slh_bot running" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Container not running" -ForegroundColor Red
    $errors++
}

# Control API
Write-Host "Checking Control API..." -ForegroundColor Cyan
try {
    $sys = Invoke-RestMethod -Uri "http://localhost:8080/api/system/status" -ErrorAction Stop
    Write-Host "  [PASS] API reachable. Docker=$($sys.docker), BinanceWS=$($sys.binance_ws)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] API not reachable" -ForegroundColor Red
    $errors++
}

# AI model
Write-Host "Checking AI Model..." -ForegroundColor Cyan
try {
    $ai = Invoke-RestMethod -Uri "http://localhost:8080/api/ai/status" -ErrorAction Stop
    if ($ai.loaded) {
        Write-Host "  [PASS] AI Model loaded: $($ai.model)" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] AI Model not loaded" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  [FAIL] Could not query AI endpoint" -ForegroundColor Red
    $errors++
}

# Ngrok
Write-Host "Checking Ngrok..." -ForegroundColor Cyan
try {
    $ngrok = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
    $url = $ngrok.tunnels[0].public_url
    Write-Host "  [PASS] Ngrok active: $url" -ForegroundColor Green
} catch {
    Write-Host "  [INFO] Ngrok not running (optional)" -ForegroundColor Gray
}

# Telegram reachability
Write-Host "Checking Telegram API..." -ForegroundColor Cyan
try {
    $tg = Invoke-RestMethod -Uri "https://api.telegram.org/bot7591051736:AAGM3GteHnhCpzc0QsCgivD8Rlv7_I6Bab8/getMe" -ErrorAction Stop
    if ($tg.ok) {
        Write-Host "  [PASS] Telegram API reachable" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] Telegram API error" -ForegroundColor Red
        $errors++
    }
} catch {
    Write-Host "  [FAIL] Cannot reach Telegram" -ForegroundColor Red
    $errors++
}

Write-Host ""
if ($errors -eq 0) {
    Write-Host "OVERALL: ALL SYSTEMS OPERATIONAL" -ForegroundColor Green
} else {
    Write-Host "OVERALL: $errors component(s) need attention" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
pause
