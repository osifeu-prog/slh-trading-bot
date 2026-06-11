from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import os

async def price_websocket(websocket: WebSocket):
    await websocket.accept()
    last_data = None
    try:
        while True:
            try:
                with open("/shared_data/last_price.json", "r") as f:
                    data = json.load(f)
                if data != last_data:
                    await websocket.send_json(data)
                    last_data = data
            except:
                pass
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")
