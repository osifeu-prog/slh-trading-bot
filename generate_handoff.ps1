$date = Get-Date -Format "yyyyMMdd_HHmm"
$handoffPath = "C:\Users\USER\Desktop\SLH\Handoff_$date.md"
@"
# SLH Trading Bot – Project Handoff Document
**Generated:** $date

## 1. Quick Start
- Open PowerShell and navigate to `C:\Users\USER\Desktop\SLH\algo-bot`
- Run `.\SLH_Menu.ps1` (or it may auto?start)
- Select option **1** to start the main bot (Docker).

## 2. Important Files
- `.env` – Contains all API keys (never commit to Git)
- `main_live.py` – Main bot script
- `supervisor_agent.py` – Optional second AI bot for supervision
- `docker-compose.yml` – Docker service definition
- `backup.ps1` – Manual backup script
- `restart.ps1` – Quick restart script

## 3. Current Status
- Main bot: trading BTC/USDT on **Binance Testnet** (paper money)
- AI Filter: XGBoost model (accuracy ~48%, baseline)
- Dashboard: http://localhost:8080 (inside Docker)
- Telegram alerts: sent to group chat (`-5294800328`)
- Commands in group: `/myid`, `/start`, `/status` (if supervisor active)

## 4. Daily Operations
- **Monitor trades:** In Telegram group, or run `docker logs -f slh_bot`
- **Backup:** Option 5 in menu, or automatic daily at 2 AM via Task Scheduler
- **Update AI model:** Re-run `train_advanced.py` periodically with fresh data

## 5. Troubleshooting
- **Docker not running:** Start Docker Desktop manually.
- **Bot not responding to commands:** Ensure Telegram privacy mode is OFF (via @BotFather).
- **Check errors:** `docker logs slh_bot --tail 50`
- **Restart cleanly:** `docker-compose down` then `docker-compose up -d`

## 6. Roadmap
- [ ] Improve AI model (add more features, better data)
- [ ] Activate supervisor bot (get second Telegram token)
- [ ] Transition to **real Binance** after successful testnet
- [ ] Multi-asset support
- [ ] Deploy to cloud server (VPS) for 24/7 operation

## 7. Key Contacts / Resources
- Binance Testnet: https://testnet.binance.vision/
- Telegram BotFather: https://t.me/BotFather
- SLH Channel: https://t.me/+37XWeJ87enw4YjJk
- Project Journal: `C:\Users\USER\Desktop\SLH\SLH_JOURNAL.md`
"@ | Set-Content -Path $handoffPath
Write-Host "Handoff document created: $handoffPath" -ForegroundColor Green
