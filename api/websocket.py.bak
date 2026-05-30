from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime
from api.binance_ws import binance_trade_stream

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("? WebSocket connected - sending live Binance data every 3s")
    trade_stream = binance_trade_stream()
    try:
        i = 0
        async for price in trade_stream:
            data = {
                "pnl": None,          # יעודכן כשיהיה PnL אמיתי
                "win_rate": None,
                "positions": [],      # ימולא ממודול הפקודות
                "last_trade": {
                    "symbol": "BTCUSDT",
                    "price": price,
                    "timestamp": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat(),
                "status": "live",
                "update": i,
                "source": "binance"
            }
            await websocket.send_json(data)
            print(f"?? Sent Binance price #{i}: {price}")
            i += 1
            await asyncio.sleep(3)   # עיכוב קל כדי לא להציף
    except WebSocketDisconnect:
        print("?? Client disconnected")
    except Exception as e:
        print("? Error:", e)
