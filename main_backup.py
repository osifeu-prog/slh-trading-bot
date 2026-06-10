from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"status": "SLH Trading Bot running"}

@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(BINANCE_URL, params={"symbol": symbol.upper()})
            data = r.json()
            return {"symbol": data["symbol"], "price": float(data["price"])}
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    await websocket.accept()
    async with httpx.AsyncClient() as client:
        while True:
            try:
                r = await client.get(BINANCE_URL, params={"symbol": "BTCUSDT"})
                data = r.json()
                await websocket.send_json({
                    "symbol": data["symbol"],
                    "price": float(data["price"])
                })
            except Exception as e:
                await websocket.send_json({"error": str(e)})
            await asyncio.sleep(2)
