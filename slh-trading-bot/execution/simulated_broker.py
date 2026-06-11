class SimulatedBroker:
    def __init__(self):
        self.position = None
        self.trades = []
        self.logs = []

    def log_event(self, msg):
        self.logs.append(msg)

    def execute(self, signal, bar):
        price = bar["close"]
        if signal["side"] == "BUY":
            if self.position is None:
                self.position = {"entry_price": price, "size_usd": signal["size_usd"]}
                self.log_event(f"BUY at {price}")
            else:
                self.log_event("BUY ignored - already in position")
        elif signal["side"] == "SELL":
            if self.position is not None:
                pnl = (price - self.position["entry_price"]) / self.position["entry_price"]
                pnl_usd = pnl * self.position["size_usd"]
                self.trades.append({"entry": self.position["entry_price"], "exit": price, "pnl_usd": pnl_usd})
                self.log_event(f"SELL at {price} | PnL: {pnl_usd:.2f}")
                self.position = None
            else:
                self.log_event("SELL ignored - no open position")

    def get_results(self):
        total_pnl = sum(t["pnl_usd"] for t in self.trades)
        win_rate = sum(1 for t in self.trades if t["pnl_usd"] > 0) / len(self.trades) if self.trades else 0
        return {"total_pnl": total_pnl, "win_rate": win_rate, "trades": self.trades, "logs": self.logs}
