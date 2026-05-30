from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import os

# ייבוא הפונקציה מה-websocket_price (קובץ שניצור באותה תיקייה)
try:
    from websocket_price import price_websocket
except ImportError:
    async def price_websocket(websocket):
        await websocket.accept()
        while True:
            try:
                with open("/shared_data/last_price.json") as f:
                    data = json.load(f)
                await websocket.send_json(data)
            except:
                pass
            await asyncio.sleep(1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
        return {"symbol": data["symbol"], "price": data["price"]}
    except:
        return {"error": "no data"}

@app.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    await price_websocket(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
