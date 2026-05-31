from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
import asyncio

app = FastAPI(title="SLH Trading Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fallback Binance client
try:
    from binance import Client
    BINANCE_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
    BINANCE_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    client.API_URL = 'https://testnet.binance.vision/api'
    BINANCE_AVAILABLE = True
except:
    BINANCE_AVAILABLE = False

@app.get("/")
async def root():
    return {"message": "SLH API ONLINE", "status": "live"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/price/{symbol}")
async def get_price(symbol: str = "BTCUSDT"):
    # Try shared file first (Render / local)
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {"symbol": data["symbol"], "price": data["price"], "source": "shared"}
    except:
        pass

    # Direct Binance fallback
    if BINANCE_AVAILABLE:
        try:
            ticker = client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            return {"symbol": symbol, "price": price, "source": "binance_direct"}
        except Exception as e:
            return {"error": f"Binance error: {str(e)}"}
    
    return {"error": "no data"}

@app.get("/api/last-price")
async def last_price():
    return await get_price("BTCUSDT")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
