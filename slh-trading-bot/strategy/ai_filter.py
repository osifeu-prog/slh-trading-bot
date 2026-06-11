import joblib, pandas as pd, os

class AISignalFilter:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "ai_models", "xgb_classifier.pkl")
        feat_path = os.path.join(os.path.dirname(__file__), "..", "ai_models", "feature_names_xgb.txt")
        self.model = joblib.load(model_path)
        with open(feat_path) as f:
            self.feature_names = f.read().strip().split(",")
        self.recent_bars = []

    def add_bar(self, bar):
        self.recent_bars.append(bar)
        if len(self.recent_bars) > 100:
            self.recent_bars.pop(0)

    def should_accept(self, signal):
        if len(self.recent_bars) < 50:
            return True
        closes = [b["close"] for b in self.recent_bars]
        volumes = [b["volume"] for b in self.recent_bars]
        rets = pd.Series(closes).pct_change()
        f = {
            "sma_20": pd.Series(closes).rolling(20).mean().iloc[-1],
            "sma_50": pd.Series(closes).rolling(50).mean().iloc[-1],
            "volume_ratio": volumes[-1] / (pd.Series(volumes).rolling(50).mean().iloc[-1] if len(volumes)>=50 else 1),
            "volatility": rets.rolling(20).std().iloc[-1],
            "coingecko_volume_avg": 0  # placeholder, can be updated live
        }
        X = pd.DataFrame([f], columns=self.feature_names).fillna(0)
        pred = self.model.predict(X)[0]
        if signal == "BUY":
            return pred == 1
        else:
            return pred == 0
