from fastapi import APIRouter
import json, os, time

router = APIRouter(prefix="/api/trades", tags=["trades"])

TRADES_LOG = "logs/trades.json"

def load_trades():
    if not os.path.exists(TRADES_LOG):
        return []
    with open(TRADES_LOG) as f:
        return json.load(f)

@router.get("/history")
def trade_history(limit: int = 20):
    trades = load_trades()
    return trades[-limit:]

@router.get("/pnl")
def get_pnl():
    trades = load_trades()
    if not trades:
        return {"total_pnl": 0.0, "win_rate": 0.0}
    buy_trades = [t for t in trades if t["side"] == "BUY"]
    sell_trades = [t for t in trades if t["side"] == "SELL"]
    pnl = 0.0
    wins = 0
    total = min(len(buy_trades), len(sell_trades))
    for i in range(total):
        trade_pnl = (sell_trades[i]["price"] - buy_trades[i]["price"]) * buy_trades[i]["qty"]
        pnl += trade_pnl
        if trade_pnl > 0:
            wins += 1
    win_rate = wins / total if total > 0 else 0.0
    return {"total_pnl": round(pnl, 4), "win_rate": round(win_rate, 4), "total_trades": total}
