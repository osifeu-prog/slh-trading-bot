import os, time, json, logging
from datetime import datetime
from dotenv import load_dotenv
from binance import Client

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_KEY = os.getenv('BINANCE_TESTNET_API_KEY')
SECRET_KEY = os.getenv('BINANCE_TESTNET_API_SECRET')
if not API_KEY or not SECRET_KEY:
    raise ValueError("Missing API keys")

client = Client(API_KEY, SECRET_KEY)
client.API_URL = 'https://testnet.binance.vision/api'

SYMBOL = "BTCUSDT"
SMA_SHORT, SMA_LONG = 9, 21
in_position = False

def get_historical_data(limit=300):
    klines = client.get_klines(symbol=SYMBOL, interval="1m", limit=limit)
    return [float(k[4]) for k in klines]

def calculate_sma(data, period):
    return sum(data[-period:]) / period if len(data) >= period else None

print("SLH Trader starting...")

while True:
    try:
        closes = get_historical_data(300)
        price = closes[-1]
        sma_short = calculate_sma(closes, SMA_SHORT)
        sma_long = calculate_sma(closes, SMA_LONG)
        if sma_short and sma_long:
            diff = sma_short - sma_long
            print(f"BTC ${price:,.2f} | SMA9: {sma_short:.2f} | SMA21: {sma_long:.2f} | Diff: {diff:+.2f}")
            if sma_short > sma_long and not in_position and diff > 35:
                print("STRONG BUY SIGNAL")
                in_position = True
            elif sma_short < sma_long and in_position and diff < -35:
                print("STRONG SELL SIGNAL")
                in_position = False
        else:
            print(f"BTC ${price:,.2f} (collecting data...)")
        with open("/shared_data/last_price.json", "w") as f:
            json.dump({"symbol": SYMBOL, "price": price, "sma_short": sma_short, "sma_long": sma_long, "in_position": in_position, "timestamp": datetime.now().isoformat()}, f)
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)