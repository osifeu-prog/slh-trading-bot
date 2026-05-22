from collections import deque
from .base_strategy import BaseStrategy

class SmaCrossoverStrategy(BaseStrategy):
    def __init__(self, short_window=20, long_window=50, cooldown_bars=10):
        self.short_window = short_window
        self.long_window = long_window
        self.cooldown_bars = cooldown_bars
        self.prices = deque(maxlen=long_window)
        self.last_signal = "HOLD"
        self.bars_since_signal = 999  # allow initial signal
        self.current_side = None  # track if we are in position

    def on_bar(self, bar):
        price = bar["close"]
        self.prices.append(price)
        self.bars_since_signal += 1

        if len(self.prices) < self.long_window:
            self.last_signal = "HOLD"
            return

        if self.bars_since_signal < self.cooldown_bars:
            self.last_signal = "HOLD"
            return

        short_sma = sum(list(self.prices)[-self.short_window:]) / self.short_window
        long_sma = sum(self.prices) / self.long_window

        # Generate signal only on cross
        if short_sma > long_sma and self.current_side != "BUY":
            self.last_signal = "BUY"
            self.current_side = "BUY"
            self.bars_since_signal = 0
        elif short_sma < long_sma and self.current_side != "SELL":
            self.last_signal = "SELL"
            self.current_side = "SELL"
            self.bars_since_signal = 0
        else:
            self.last_signal = "HOLD"

    def get_signal(self):
        return self.last_signal
