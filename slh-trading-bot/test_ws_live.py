import websocket, json

def on_open(ws):
    print("CONNECTED")

def on_message(ws, msg):
    data = json.loads(msg)
    price = data["last_trade"]["price"]
    print(f"Live price: {price}")
    if data["update"] >= 2:
        ws.close()

ws = websocket.WebSocketApp("ws://localhost:8080/ws",
                            on_open=on_open,
                            on_message=on_message)
ws.run_forever()
