import websocket
import json
import threading

class BinanceWebSocket:
    def __init__(self, symbol="btcusdt", interval="1m", callback=None):
        self.symbol = symbol.lower()
        self.interval = interval
        self.callback = callback
        # Binance changed testnet URL from wss://testnet.binance.vision/ws
        # to wss://stream.testnet.binance.vision/ws (May 2025)
        self.ws_url = f"wss://stream.testnet.binance.vision/ws/{self.symbol}@kline_{self.interval}"

    def on_message(self, ws, message):
        data = json.loads(message)
        candle = data['k']
        bar = {
            "timestamp": candle['t'],
            "open": float(candle['o']),
            "high": float(candle['h']),
            "low": float(candle['l']),
            "close": float(candle['c']),
            "volume": float(candle['v'])
        }
        if self.callback:
            self.callback(bar)

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def start(self):
        ws = websocket.WebSocketApp(self.ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error)
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
