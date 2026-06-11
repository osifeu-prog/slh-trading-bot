class MaxPositionSizeRule:
    def __init__(self, max_usd_per_trade):
        self.max_usd_per_trade = max_usd_per_trade

    def validate(self, context, signal):
        if signal["size_usd"] > self.max_usd_per_trade:
            return False, f"size_usd {signal['size_usd']} > {self.max_usd_per_trade}"
        return True, ""
