from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="SLH LIVE CONTROL TOWER v3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_price = None

@app.get("/")
async def root():
    return {"status": "LIVE", "system": "SLH"}

@app.get("/health")
async def health():
    return {"status": "ok", "mode": "live"}

@app.get("/api/v1/status")
async def status():
    return {
        "system": "SLH",
        "status": "LIVE",
        "mode": "production",
        "phase": 3
    }

# ====================== חשוב ======================
@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    """הנתיב שהפרונטאנד מחפש"""
    global last_price
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {
                "symbol": symbol.upper(),
                "price": data.get("price"),
                "status": "success"
            }
    except:
        return {
            "symbol": symbol.upper(),
            "price": last_price,
            "status": "no_data_yet"
        }

@app.get("/api/last-price")
async def get_last_price():
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {"price": data.get("price")}
    except:
        return {"price": last_price}

@app.post("/api/price")
async def receive_price(data: dict):
    global last_price
    last_price = data.get("price")
    try:
        os.makedirs("/shared_data", exist_ok=True)
        with open("/shared_data/last_price.json", "w") as f:
            json.dump({
                "price": last_price,
                "symbol": data.get("symbol", "BTCUSDT")
            }, f)
    except:
        pass
    return {"status": "ok", "price": last_price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)