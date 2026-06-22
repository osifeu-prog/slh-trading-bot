Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SLH FULL SYSTEM AUDIT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------
# Docker
# ------------------------------------------------

Write-Host "[1] Docker Containers" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}"

Write-Host ""

# ------------------------------------------------
# Health Endpoints
# ------------------------------------------------

Write-Host "[2] API Health" -ForegroundColor Yellow

try {
    Invoke-RestMethod http://localhost:8080/health
}
catch {
    Write-Host "API FAILED" -ForegroundColor Red
}

Write-Host ""

# ------------------------------------------------
# Shared Data
# ------------------------------------------------

Write-Host "[3] Shared Data" -ForegroundColor Yellow

if(Test-Path ".\shared_data\last_price.json")
{
    Get-Content .\shared_data\last_price.json
}
else
{
    Write-Host "last_price.json missing" -ForegroundColor Red
}

Write-Host ""

# ------------------------------------------------
# Memory Docs
# ------------------------------------------------

Write-Host "[4] Project Memory" -ForegroundColor Yellow

$docs = @(
"docs\PROJECT_MASTER.md",
"docs\STATUS.md",
"docs\MEMORY.md",
"docs\DECISIONS.md",
"docs\ROADMAP.md",
"docs\ARCHITECTURE.md",
"docs\SESSION_HANDOFF.md"
)

foreach($d in $docs)
{
    if(Test-Path $d)
    {
        Write-Host "OK $d" -ForegroundColor Green
    }
    else
    {
        Write-Host "MISSING $d" -ForegroundColor Red
    }
}

Write-Host ""

# ------------------------------------------------
# Trader Logs
# ------------------------------------------------

Write-Host "[5] Trader Activity" -ForegroundColor Yellow

docker compose logs trader --tail 20

Write-Host ""

# ------------------------------------------------
# Frontend
# ------------------------------------------------

Write-Host "[6] Frontend" -ForegroundColor Yellow

try
{
    $r = Invoke-WebRequest http://localhost:3000 -UseBasicParsing
    Write-Host "Frontend OK" -ForegroundColor Green
}
catch
{
    Write-Host "Frontend DOWN" -ForegroundColor Red
}

Write-Host ""

# ------------------------------------------------
# API
# ------------------------------------------------

Write-Host "[7] API" -ForegroundColor Yellow

try
{
    $r = Invoke-WebRequest http://localhost:8080/docs -UseBasicParsing
    Write-Host "Swagger OK" -ForegroundColor Green
}
catch
{
    Write-Host "Swagger DOWN" -ForegroundColor Red
}

Write-Host ""

# ------------------------------------------------
# Docker Resources
# ------------------------------------------------

Write-Host "[8] Resources" -ForegroundColor Yellow

docker stats --no-stream

Write-Host ""

# ------------------------------------------------
# Final Score
# ------------------------------------------------

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AUDIT COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
