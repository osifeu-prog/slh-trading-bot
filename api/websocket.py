from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json

# פונקציה לדוגמה – יש להחליף בנתונים אמיתיים מה-bot
async def get_live_data():
    return {
        "pnl": 0.0,
        "win_rate": 0.0,
        "positions": [],
        "last_trade": None,
        "timestamp": None
    }

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await get_live_data()
            await websocket.send_json(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
