import websocket, json, time

def on_open(ws):
    print("CONNECTED")

def on_message(ws, msg):
    data = json.loads(msg)
    pnl = data["pnl"]
    update = data["update"]
    print(f"PnL: {pnl}, Update: {update}")
    if update >= 2:
        time.sleep(0.5)
        ws.close()

ws = websocket.WebSocketApp("ws://localhost:8080/ws",
                            on_open=on_open,
                            on_message=on_message)
ws.run_forever()
