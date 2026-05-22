from datetime import datetime

class ContextBuilder:
    def __init__(self, portfolio_store, trades_store):
        self.portfolio_store = portfolio_store
        self.trades_store = trades_store

    def build(self):
        today = datetime.utcnow().date()
        trades_today = self.trades_store.get_trades_for_date(today) if hasattr(self.trades_store, "get_trades_for_date") else []
        daily_pnl = sum(t["pnl_usd"] for t in trades_today)
        trades_count = len(trades_today)
        current_exposure = self.portfolio_store.get_total_exposure_usd() if hasattr(self.portfolio_store, "get_total_exposure_usd") else 0
        return {"daily_pnl": daily_pnl, "trades_today": trades_count, "current_exposure": current_exposure}
