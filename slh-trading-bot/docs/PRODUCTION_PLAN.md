# SLH Production Roadmap

## 1. Security Hardening
- [ ] Rotate all tokens (Telegram + Binance)
- [ ] Ensure .env is in .gitignore (already)
- [ ] Set JWT expiry to 15 minutes
- [ ] Enable rate limiting on all API endpoints
- [ ] Full RBAC enforcement on every route

## 2. Infrastructure
- [ ] Push code to GitHub (without .env)
- [ ] Set up Oracle Cloud Free Tier VM
- [ ] Deploy Docker containers to VPS
- [ ] Set up CI/CD with GitHub Actions
- [ ] Configure SSL/TLS with Let's Encrypt

## 3. Monitoring & Observability
- [ ] Add Prometheus metrics endpoint
- [ ] Create Grafana dashboard
- [ ] Set up UptimeRobot or similar
- [ ] Log aggregation (ELK/Loki)

## 4. Trading Improvements
- [ ] Backtest on multiple timeframes
- [ ] Implement multi-asset trading
- [ ] Add stop-loss / take-profit logic
- [ ] Paper trade for 2 weeks minimum

## 5. UI/UX
- [ ] Complete React dashboard with live WebSocket
- [ ] Add TradingView chart widget
- [ ] Mobile responsive design
- [ ] Dark/light mode toggle

## 6. Go Live
- [ ] Generate real Binance API keys (restricted IP)
- [ ] Start with minimum capital ($50-100)
- [ ] Monitor closely for 48 hours
- [ ] Gradually increase position size
