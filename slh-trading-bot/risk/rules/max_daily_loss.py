class MaxDailyLossRule:
    def __init__(self, max_daily_loss_usd):
        self.max_daily_loss_usd = max_daily_loss_usd

    def validate(self, context, signal):
        if context["daily_pnl"] <= -self.max_daily_loss_usd:
            return False, f"daily_pnl {context['daily_pnl']} <= -{self.max_daily_loss_usd}"
        return True, ""
