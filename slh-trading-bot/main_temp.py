from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI(title="SLH LIVE CONTROL TOWER v3")

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

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text("SLH HEARTBEAT LIVE")
            await asyncio.sleep(3)
    except:
        await websocket.close()


@app.post("/api/price")
async def receive_price(price: float):
    from api.websocket import manager
    import json
    await manager.broadcast(json.dumps({"type": "price", "price": price}))
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


# הוסף אחרי import statements
last_price = None

@app.post("/api/price")
async def receive_price(price: float):
    global last_price
    last_price = price
    # גם broadcast ל-WebSocket (לא חובה, אבל נשאיר)
    from api.websocket import manager
    import json
    await manager.broadcast(json.dumps({"type": "price", "price": price}))
    return {"status": "ok"}

@app.get("/api/last-price")
async def get_last_price():
    return {"price": last_price}

@app.get("/api/last-price2")
async def get_last_price2():
    import json
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {"price": data.get("price")}
    except:
        return {"price": None}
