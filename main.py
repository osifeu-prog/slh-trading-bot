from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import httpx
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public APIs (no keys required)
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
BITFINEX_URL = "https://api-pub.bitfinex.com/v2/ticker/tBTCUSD"

prices = []

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"status": "SLH Trading Bot running"}

@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    """Fetch BTC price from Binance, fallback to Bitfinex."""
    # Try Binance first
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(BINANCE_URL, params={"symbol": symbol.upper()})
            r.raise_for_status()
            data = r.json()
            return {"symbol": data["symbol"], "price": float(data["price"])}
    except Exception as e:
        logger.warning(f"Binance failed ({e}), trying Bitfinex")

    # Fallback to Bitfinex
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(BITFINEX_URL)
            r.raise_for_status()
            data = r.json()
            # Bitfinex response: [BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, ...]
            last_price = float(data[6])  # index 6 = last price
            return {"symbol": "BTCUSDT", "price": last_price, "source": "bitfinex"}
    except Exception as e:
        logger.error(f"Bitfinex also failed: {e}")
        return {"error": "All price sources failed"}, 500

@app.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    await websocket.accept()

    async with httpx.AsyncClient() as client:
        while True:
            try:
                r = await client.get(BITFINEX_URL)
                r.raise_for_status()
                data = r.json()
                last_price = float(data[6])

                prices.append(last_price)

                if len(prices) > 50:
                    prices.pop(0)

                sma9 = sum(prices[-9:]) / min(len(prices), 9)
                sma21 = sum(prices[-21:]) / min(len(prices), 21)

                rsi = 50.0
                if len(prices) >= 15:
                    gains, losses = [], []
                    for i in range(-14, 0):
                        change = prices[i] - prices[i - 1]
                        if change > 0:
                            gains.append(change); losses.append(0)
                        else:
                            gains.append(0); losses.append(abs(change))
                    avg_gain = sum(gains) / 14
                    avg_loss = sum(losses) / 14
                    if avg_loss == 0: rsi = 100
                    else: rsi = 100 - (100 / (1 + (avg_gain/avg_loss)))

                position = "FLAT"
                if len(prices) >= 21:
                    if sma9 > sma21: position = "LONG"
                    elif sma9 < sma21: position = "SHORT"

                await websocket.send_json({
                    "symbol": "BTCUSDT",
                    "price": last_price,
                    "sma9": round(sma9,2),
                    "sma21": round(sma21,2),
                    "rsi": round(rsi,2),
                    "position": position,
                    "timestamp": int(time.time()*1000)
                })
            except Exception as e:
                await websocket.send_json({"error": str(e), "timestamp": int(time.time()*1000)})
            await asyncio.sleep(2)
