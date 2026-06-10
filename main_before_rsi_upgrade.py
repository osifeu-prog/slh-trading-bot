from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import httpx
import time
import statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

prices = []

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"status": "SLH Trading Bot running"}

@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(BINANCE_URL, params={"symbol": symbol.upper()})
        data = r.json()
        return {"symbol": data["symbol"], "price": float(data["price"])}

@app.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    await websocket.accept()
    async with httpx.AsyncClient() as client:
        while True:
            try:
                r = await client.get(BINANCE_URL, params={"symbol": "BTCUSDT"})
                data = r.json()

                price = float(data["price"])

                # cache prices
                prices.append(price)
                if len(prices) > 50:
                    prices.pop(0)

                sma9 = sum(prices[-9:]) / min(len(prices), 9)
                sma21 = sum(prices[-21:]) / min(len(prices), 21)

                rsi = 50  # בסיס (נשדרג אחר כך)

                await websocket.send_json({
                    "symbol": data["symbol"],
                    "price": price,
                    "sma9": round(sma9, 2),
                    "sma21": round(sma21, 2),
                    "rsi": rsi,
                    "position": "FLAT",
                    "timestamp": int(time.time() * 1000)
                })

            except Exception as e:
                await websocket.send_json({
                    "error": str(e),
                    "timestamp": int(time.time() * 1000)
                })

            await asyncio.sleep(2)
