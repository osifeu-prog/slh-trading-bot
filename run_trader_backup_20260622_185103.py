import os, time, json, logging
from datetime import datetime
import requests

logging.basicConfig(level=logging.INFO)

SYMBOL = "BTCUSDT"
INTERVAL = "1m"
LIMIT = 300
SMA_SHORT, SMA_LONG = 9, 21
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

in_position = False
entry_price = 0.0

def fetch_klines(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [float(k[4]) for k in data]  # closing prices

def calculate_sma(data, period):
    if len(data) < period:
        return None
    return sum(data[-period:]) / period

def calculate_rsi(data, period=14):
    if len(data) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(data)):
        change = data[i] - data[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

print("SLH Trader starting (using public Binance API)...")

while True:
    try:
        closes = fetch_klines(SYMBOL, INTERVAL, LIMIT)
        price = closes[-1]

        sma_short = calculate_sma(closes, SMA_SHORT)
        sma_long = calculate_sma(closes, SMA_LONG)
        rsi = calculate_rsi(closes, RSI_PERIOD)

        if sma_short and sma_long and rsi:
            diff = sma_short - sma_long
            print(f"BTC ${price:,.2f} | SMA9: {sma_short:.2f} | SMA21: {sma_long:.2f} | Diff: {diff:+.2f} | RSI: {rsi:.1f}")

            # Buy signal: SMA crossover up, diff > 40, RSI not overbought
            if sma_short > sma_long and diff > 40 and rsi < RSI_OVERBOUGHT and not in_position:
                print("?? STRONG BUY SIGNAL")
                in_position = True
                entry_price = price
            # Sell signal: SMA crossover down, diff < -40, RSI not oversold
            elif sma_short < sma_long and diff < -40 and rsi > RSI_OVERSOLD and in_position:
                profit_pct = (price - entry_price) / entry_price * 100
                print(f"?? STRONG SELL SIGNAL (Profit: {profit_pct:.2f}%)")
                in_position = False
                entry_price = 0.0
        else:
            print(f"Collecting data... Price: ${price:,.2f}")

        # Write to shared file for API endpoint
        os.makedirs("/shared_data", exist_ok=True)
        with open("/shared_data/last_price.json", "w") as f:
            json.dump({
                "symbol": SYMBOL,
                "price": price,
                "sma_short": sma_short,
                "sma_long": sma_long,
                "rsi": rsi,
                "in_position": in_position,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)