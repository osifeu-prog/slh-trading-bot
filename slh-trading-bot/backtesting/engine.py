import pandas as pd

class BacktestEngine:
    def __init__(self, df, strategy, risk_engine, context_builder, broker):
        self.df = df
        self.strategy = strategy
        self.risk_engine = risk_engine
        self.context_builder = context_builder
        self.broker = broker
        self.results = {}

    def run(self):
        for idx, row in self.df.iterrows():
            bar = {"timestamp": row["timestamp"], "open": row["open"], "high": row["high"], "low": row["low"], "close": row["close"], "volume": row["volume"]}
            self.strategy.on_bar(bar)
            signal = self.strategy.get_signal()
            if signal == "HOLD":
                continue
            trade_signal = {"symbol": "BTCUSDT", "side": signal, "size_usd": 50}
            context = self.context_builder.build()
            ok, reason = self.risk_engine.approve(context, trade_signal)
            if not ok:
                self.broker.log_event(f"RISK BLOCKED: {reason}")
                continue
            self.broker.execute(trade_signal, bar)
        self.results = self.broker.get_results()
        return self.results
