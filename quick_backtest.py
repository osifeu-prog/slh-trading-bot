import pandas as pd
from pathlib import Path

# פונקציות חישוב SMA ו-RSI (מועתקות מה-trader)
def calculate_sma(data, period):
    if len(data) < period: return None
    return sum(data[-period:]) / period

def calculate_rsi(data, period=14):
    if len(data) < period+1: return None
    gains, losses = [], []
    for i in range(1, len(data)):
        change = data[i] - data[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + avg_gain/avg_loss))

def backtest(symbol="BTCUSDT", start="2025-01-01", end="2026-05-30"):
    data_path = Path(f"data/historical/{symbol}.csv")
    if not data_path.exists():
        print(f"❌ No data for {symbol}")
        return
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    df = df[(df.index >= start) & (df.index <= end)]
    closes = df['close'].values
    
    in_position = False
    entry_price = 0
    balance = 10000
    trades = []
    
    for i in range(100, len(closes)):
        window = closes[i-100:i+1]
        sma9 = calculate_sma(window, 9)
        sma21 = calculate_sma(window, 21)
        rsi = calculate_rsi(window, 14)
        if None in (sma9, sma21, rsi):
            continue
        price = closes[i]
        diff = sma9 - sma21
        
        if not in_position and sma9 > sma21 and diff > 40 and rsi < 70:
            in_position = True
            entry_price = price
            trades.append(('BUY', price))
        elif in_position and sma9 < sma21 and diff < -40 and rsi > 30:
            profit = (price - entry_price) / entry_price
            balance += profit * balance
            trades.append(('SELL', price, profit))
            in_position = False
    
    print(f"Backtest {symbol} {start} → {end}")
    print(f"Final balance: ${balance:.2f}")
    print(f"Trades: {len(trades)}")
