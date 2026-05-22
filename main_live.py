import os, time, threading, json
from dotenv import load_dotenv
from data.connectors.binance_ws import BinanceWebSocket
from strategy.sma_crossover import SmaCrossoverStrategy
from strategy.ai_filter import AISignalFilter
from risk.risk_engine import RiskEngine
from risk.context_builder import ContextBuilder
from risk.rules.max_position_size import MaxPositionSizeRule
from risk.rules.max_daily_loss import MaxDailyLossRule
from execution.binance_adapter import BinanceAdapter
from monitoring.dashboard_api import start_dashboard
import requests, decimal
from datetime import datetime, timezone

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(text):
    if not telegram_token or not telegram_chat_id: return
    try:
        requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                      json={"chat_id": telegram_chat_id, "text": text})
    except: pass

adapter = BinanceAdapter(api_key, api_secret, testnet=True) if api_key and api_secret else None
strategy = SmaCrossoverStrategy()
ai_filter = AISignalFilter()
risk_engine = RiskEngine([
    MaxPositionSizeRule(50),
    MaxDailyLossRule(100)
])
context_builder = ContextBuilder(adapter, adapter)

HEARTBEAT_FILE = "logs/heartbeat.txt"

def update_heartbeat():
    hb = {"source": "MainBot", "timestamp": datetime.now(timezone.utc).isoformat(), "status": "alive"}
    with open(HEARTBEAT_FILE, "w") as f:
        json.dump(hb, f)

def round_step(value, step=0.00001):
    d = decimal.Decimal(str(step))
    val = decimal.Decimal(str(value))
    return float((val // d) * d)

def on_bar(bar):
    update_heartbeat()
    if not adapter: return
    ai_filter.add_bar(bar)
    strategy.on_bar(bar)
    signal = strategy.get_signal()
    if signal == "HOLD": return
    if not ai_filter.should_accept(signal):
        print(f"AI rejected {signal}")
        return

    trade_signal = {"symbol": "BTCUSDT", "side": signal, "size_usd": 20}
    context = context_builder.build()
    ok, reason = risk_engine.approve(context, trade_signal)
    if not ok:
        msg = f"RISK BLOCKED: {reason}"
        print(msg)
        send_telegram(msg)
        return
    try:
        btc_qty = round_step(20 / bar["close"])
        if btc_qty * bar["close"] < 10: return
        adapter.place_order("BTCUSDT", signal, btc_qty)
        msg = f"Trade: {signal} {btc_qty} BTC at {bar['close']}"
        print(msg)
        send_telegram(msg)
    except Exception as e:
        msg = f"Trade error: {e}"
        print(msg)
        send_telegram(msg)

if adapter:
    ws = BinanceWebSocket(symbol="btcusdt", interval="1m", callback=on_bar)
    t_ws = threading.Thread(target=ws.start, daemon=True)
    t_ws.start()
    send_telegram("SLH Bot started")

start_dashboard(8080)

while True:
    time.sleep(1)

