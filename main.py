from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="SLH Trading Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to load Binance client
BINANCE_AVAILABLE = False
client = None
try:
    from binance import Client
    key = os.getenv("BINANCE_TESTNET_API_KEY")
    secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    if key and secret:
        client = Client(key, secret)
        client.API_URL = 'https://testnet.binance.vision/api'
        BINANCE_AVAILABLE = True
        print("✅ Binance client loaded successfully")
    else:
        print("⚠️ Binance keys not found in environment")
except Exception as e:
    print(f"⚠️ Binance import failed: {e}")

@app.get("/")
async def root():
    return {"message": "SLH API ONLINE", "status": "live", "binance": BINANCE_AVAILABLE}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/price/{symbol}")
async def get_price(symbol: str = "BTCUSDT"):
    # 1. Try shared file
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {"symbol": data.get("symbol"), "price": data.get("price"), "source": "shared"}
    except:
        pass

    # 2. Direct Binance
    if BINANCE_AVAILABLE and client:
        try:
            ticker = client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            return {"symbol": symbol, "price": price, "source": "binance_direct"}
        except Exception as e:
            return {"error": f"Binance error: {str(e)}"}

    return {"error": "no data", "message": "Check Binance keys in Render Environment"}

@app.get("/api/last-price")
async def last_price():
    return await get_price("BTCUSDT")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
