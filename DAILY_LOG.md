# SLH Trading Bot – Daily Log (2026-05-25)

## 📌 Objectives for Today (May 25, 4h left)
- [ ] Fix frontend (port 3000) – currently ERR_CONNECTION_REFUSED
- [ ] Run smoke tests (binance connection, trade simulation, RBAC)
- [ ] Enable auto token rotation (cron job every 6h)
- [ ] Verify live WebSocket feeds are stable
- [ ] Prepare for small real-money test (paper trading only today)

## 🧪 Current System Status (as of 13:00)
| Component   | Status               | Notes                          |
|-------------|----------------------|--------------------------------|
| API         | ✅ Healthy           | port 8080                      |
| Trader      | ✅ Running           | printing live BTCUSDT prices   |
| Supervisor  | ✅ Running           | responds to /health            |
| Frontend    | ❌ Not responding    | port 3000 connection refused   |
| Token rot.  | ⚠️ Manual script     | auto_rotate.ps1 exists         |
| Backups     | ✅ Scheduled hourly  | backup_full.ps1 + task         |

## 🔧 Useful Commands (PowerShell)

### Start/stop everything
\\\powershell
docker compose up -d
docker compose down
\\\

### View logs
\\\powershell
docker logs slh_trader -f
docker logs slh_api --tail 50
docker logs slh_supervisor -f
\\\

### Manual backup
\\\powershell
.\backup_full.ps1
\\\

### Rotate tokens (auto)
\\\powershell
.\auto_rotate.ps1
\\\

### Check containers and health
\\\powershell
docker ps
curl http://localhost:8080/health
\\\

### Rebuild everything
\\\powershell
docker compose down
docker compose up -d --build
\\\

### Smoke test (live test)
\\\powershell
# Check trader prints price every few seconds (already seen)
docker logs slh_trader --tail 5
# Test API endpoints
curl http://localhost:8080/api/system/status
curl http://localhost:8080/api/admin/test-rbac
\\\

## 🗓️ Next Steps (after frontend fix)
1. Test RBAC on all endpoints
2. Connect Telegram bot to send price alerts
3. Deploy to VPS (if time permits)
4. Start paper trading with  simulated

## 🔐 Security Reminders
- Never commit .env to git
- Run auto_rotate.ps1 before sharing screen/code
- Keep backups at least 7 days
