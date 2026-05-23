import asyncio
import websockets
import json

async def binance_trade_stream():
    """Stream live trade data from Binance Public (BTCUSDT)."""
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            yield float(data['p'])  # trade price
