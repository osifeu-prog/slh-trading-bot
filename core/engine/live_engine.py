import asyncio
import time
import logging

class LiveEngine:
    def __init__(self, strategy, broker, risk):
        self.strategy = strategy
        self.broker = broker
        self.risk = risk

        self.position_open = False
        self.last_trade_time = 0
        self.cooldown = 5

        self.logger = logging.getLogger("LiveEngine")

    async def on_data(self, candle):
        try:
            signal = self.strategy.on_data(candle)
            now = time.time()

            if now - self.last_trade_time < self.cooldown:
                return

            if not self.risk.allow_trade():
                return

            if signal == "BUY" and not self.position_open:
                await self.broker.buy()
                self.position_open = True
                self.last_trade_time = now
                self.logger.info("BUY executed")

            elif signal == "SELL" and self.position_open:
                await self.broker.sell()
                self.position_open = False
                self.last_trade_time = now
                self.logger.info("SELL executed")

        except Exception as e:
            self.logger.error(f"LiveEngine crash: {e}")