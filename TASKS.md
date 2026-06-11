# SLH Trading Bot – Master Task List

## Phase 0: Environment Setup
- [X] Create algo-bot folder structure
- [X] Generate placeholder Python files
- [X] Create Python venv and install deps
- [X] Initialize Git repository
- [ ] GitHub remote repository created
- [ ] Push initial commit to GitHub
- [X] PowerShell profile with aliases
- [X] log_work.ps1 time tracking working
- [X] slh-status.ps1 operational

## Phase 1: Core Modules (Code)
- [X] Base Strategy Interface
- [X] SMA Crossover Strategy
- [X] Simulated Broker
- [X] Backtesting Engine
- [X] Risk Engine and Rules
- [X] Main Backtest Runner

## Phase 2: Historical Data
- [X] Download OHLCV data (BTC 1h/5m)
- [X] Place CSV in data/historical/

## Phase 3: Backtesting Execution
- [X] First backtest run (SMA crossover)
- [X] Generate PnL / Win Rate / Drawdown metrics
- [X] Risk Engine integrated and tested

## Phase 4: Live / Testnet
- [X] Binance Testnet API keys configured
- [X] WebSocket data feed (Binance Testnet)
- [X] Testnet paper trading bot running
- [X] Telegram alerts for trades/errors
- [X] Telegram /myid + channel invite

## Phase 5: Advanced
- [X] AI/ML Strategy (XGBoost)
- [X] Web3 Adapters (PancakeSwap)
- [X] Web3 Adapters (TON)
- [X] CoinGecko Data Connector
- [X] Dashboard (FastAPI)

## Phase 6: Docker & Deploy
- [X] Dockerfile & docker-compose.yml
- [X] Container running (slh_bot)
- [X] Power: Never sleep
- [X] Auto-start on reboot (Task Scheduler)
- [X] Daily backup (Task Scheduler)

## Phase 7: Production Ready
- [X] Supervisor AI agent (active)
- [X] Project handoff document
- [X] Functional PowerShell master menu
- [X] Comprehensive journal & logs
- [X] Single Instance Lock
- [X] JSON Heartbeat

## Phase 8: Security & Privacy
- [X] Token rotation tool (rotate_tokens.ps1)
- [X] ZK-PoC (DID + Verifiable Credentials)
- [X] Railgun Privacy PoC (simulation)
- [ ] Real Railgun/Aztec integration
- [ ] Polygon ID real implementation

## Phase 9: UI/UX & Control Tower
- [X] Basic React Dashboard (Login, Status, AI, Admin)
- [X] PnL & Trade History widgets
- [X] Real-time WebSocket updates
- [X] Open Positions from Binance
- [ ] Advanced charts (TradingView)
- [ ] Mobile responsive

## Phase 10: VPS & Production
- [ ] Deploy to cloud server (VPS)
- [ ] Live Binance API keys (secured)
- [ ] Multi-asset support
- [ ] CI/CD auto-deploy

## Phase 11: Authentication & RBAC
- [X] JWT Auth (register, login, me)
- [X] RBAC Engine (core/rbac_engine.py)
- [X] Admin user management API
- [X] Full RBAC enforcement on all endpoints
- [ ] ABAC policies (time/IP based)





# ========================================
# PHASE 12 - AUTONOMOUS OPERATIONS
# ========================================

## Telegram Control Center

[ ] /status
[ ] /dashboard
[ ] /doctor
[ ] /positions
[ ] /pnl

## Startup & Monitoring

[ ] Startup Report
[ ] Health Watchdog
[ ] Telegram Alerts

## Auto Recovery

[ ] API Auto Restart
[ ] Trader Auto Restart
[ ] Frontend Auto Restart
[ ] Supervisor Auto Restart

## Control Tower

[ ] Control Tower API
[ ] Live Metrics Feed
[ ] Mobile Operations Center

## Reporting

[ ] Daily Health Report
[ ] Weekly Health Report


# ========================================
# PHASE 12B - HARDENING
# ========================================

[ ] Git repository cleanup
[ ] Automated backups verification
[ ] Docker health watchdog
[ ] Telegram Control Center

[ ] PRO Doctor Score
[ ] Telegram restart commands
[ ] Telegram diagnostics

[ ] Daily health reports
[ ] Weekly system reports

[ ] VPS readiness audit
[ ] Disaster recovery package

[ ] Secrets inventory
[ ] Environment validation

# ========================================
# PHASE 12B - HARDENING
# ========================================

[ ] Git repository cleanup
[ ] Automated backups verification
[ ] Docker health watchdog
[ ] Telegram Control Center

[ ] PRO Doctor Score
[ ] Telegram restart commands
[ ] Telegram diagnostics
[ ] Daily health reports
[ ] Weekly system reports
[ ] VPS readiness audit
[ ] Disaster recovery package
[ ] Secrets inventory
[ ] Environment validation
