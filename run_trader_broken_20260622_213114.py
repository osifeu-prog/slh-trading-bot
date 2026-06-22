import os, time, json, logging
from datetime import datetime
import requests
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
sys.path.append(os.path.join(os.path.dirname(__file__), 'risk'))
from position_size import calculate_position_size
from stop_loss import calculate_stop_loss
from max_drawdown import check_max_drawdown

logging.basicConfig(level=logging.INFO)

SYMBOL = "BTCUSDT"
INTERVAL = "1m"
LIMIT = 300
SMA_SHORT, SMA_LONG = 9, 21
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

INITIAL_BALANCE = 10000.0
BALANCE = INITIAL_BALANCE
RISK_PERCENT = 1.0
MAX_DRAWDOWN_PCT = 20.0
ATR_PERIOD = 14
STOP_MULTIPLIER = 2.0

in_position = False
entry_price = 0.0
position_units = 0.0
peak_equity = INITIAL_BALANCE

# DB connection
DB_CONFIG = {
    "host": "db",
    "database": "slh_trading",
    "user": "slh",
    "password": "slh_pass"
}

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            side TEXT,
            price REAL,
            units REAL,
            profit REAL,
            balance REAL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def log_trade(side, price, units, profit, balance):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO trades (side, price, units, profit, balance) VALUES (%s,%s,%s,%s,%s)",
                    (side, price, units, profit, balance))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"DB log failed: {e}")

def fetch_klines(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    closes = [float(k[4]) for k in data]
    highs = [float(k[2]) for k in data]
    lows = [float(k[3]) for k in data]
    return closes, highs, lows

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

def calculate_atr(highs, lows, closes, period=14):
    if len(closes) < period + 1:
        return None
    tr = []
    for i in range(1, len(closes)):
        h = highs[i]
        l = lows[i]
        prev_c = closes[i-1]
        tr.append(max(h - l, abs(h - prev_c), abs(l - prev_c)))
    return sum(tr[-period:]) / period

print("SLH Trader starting (with Risk Engine + PostgreSQL)...")
init_db()

while True:
    try:
        closes, highs, lows = fetch_klines(SYMBOL, INTERVAL, LIMIT)
        price = closes[-1]

        sma_short = calculate_sma(closes, SMA_SHORT)
        sma_long = calculate_sma(closes, SMA_LONG)
        rsi = calculate_rsi(closes, RSI_PERIOD)
        atr = calculate_atr(highs, lows, closes, ATR_PERIOD)

        if sma_short and sma_long and rsi and atr:
            diff = sma_short - sma_long
            current_equity = BALANCE
            if in_position:
                current_equity = BALANCE + (price - entry_price) * position_units
            peak_equity = max(peak_equity, current_equity)

            print(f"BTC {price:,.2f} | SMA9: {sma_short:.2f} | SMA21: {sma_long:.2f} | "
                  f"Diff: {diff:+.2f} | RSI: {rsi:.1f} | ATR: {atr:.2f} | Equity: {current_equity:,.2f}")

            if sma_short > sma_long and diff > 40 and rsi < RSI_OVERBOUGHT and not in_position:
                if check_max_drawdown(current_equity, peak_equity, MAX_DRAWDOWN_PCT):
                    print("MAX DRAWDOWN HIT - SKIPPING BUY")
                else:
                    stop_loss_price = calculate_stop_loss(price, atr, STOP_MULTIPLIER)
                    units = calculate_position_size(BALANCE, RISK_PERCENT, price, stop_loss_price)
                    print(f"STRONG BUY SIGNAL | Units: {units:.6f} | Stop Loss: {stop_loss_price:.2f}")
                    in_position = True
                    entry_price = price
                    position_units = units
                    log_trade("BUY", price, units, 0, BALANCE)
            send_telegram(f"BUY {SYMBOL} @ {price:.2f} Units: {units:.6f}")

            elif sma_short < sma_long and diff < -40 and rsi > RSI_OVERSOLD and in_position:
                profit = (price - entry_price) * position_units
                BALANCE += profit
                profit_pct = (price - entry_price) / entry_price * 100
                print(f"STRONG SELL SIGNAL | Profit: {profit:,.2f} ({profit_pct:.2f}%) | Balance: {BALANCE:,.2f}")
                log_trade("SELL", price, position_units, profit, BALANCE)
            send_telegram(f"SELL {SYMBOL} @ {price:.2f} Profit: {profit:.2f} ({profit_pct:.2f}%)")
                in_position = False
                entry_price = 0.0
                position_units = 0.0
        else:
            print(f"Collecting data... Price: {price:,.2f}")

        os.makedirs("/shared_data", exist_ok=True)
        with open("/shared_data/last_price.json", "w") as f:
            json.dump({
                "symbol": SYMBOL,
                "price": price,
                "sma_short": sma_short,
                "sma_long": sma_long,
                "rsi": rsi,
                "in_position": in_position,
                "balance": BALANCE,
                "equity": current_equity if 'current_equity' in locals() else BALANCE,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)
