import asyncio
import websockets
import json

async def binance_trade_stream():
    """Stream live trade data from Binance Testnet (BTCUSDT)."""
    url = "wss://testnet.binance.vision/ws/btcusdt@trade"
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            yield float(data['p'])  # trade price
