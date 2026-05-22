from binance.client import Client
from binance.enums import *

class BinanceAdapter:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.API_URL = "https://testnet.binance.vision/api"
        self.symbol = "BTCUSDT"

    def place_order(self, symbol, side, quantity):
        try:
            if side == "BUY":
                order = self.client.order_market_buy(symbol=self.symbol, quantity=quantity)
            else:
                order = self.client.order_market_sell(symbol=self.symbol, quantity=quantity)
            print(f"[Binance Testnet] {side} {quantity} {self.symbol}")
            return order
        except Exception as e:
            print(f"Order error: {e}")
            return None

    def get_positions(self):
        # Simplified: return account balance for BTC
        try:
            btc_balance = self.client.get_asset_balance(asset='BTC')
            return float(btc_balance['free'])
        except:
            return 0.0
