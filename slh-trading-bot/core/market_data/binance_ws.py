import asyncio
import json
import websockets

BINANCE_WS = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

class BinanceStream:
    def __init__(self, callback):
        self.callback = callback

    async def run(self):
        async with websockets.connect(BINANCE_WS) as ws:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                await self.callback(data)