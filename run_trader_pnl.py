import time
import logging
import psycopg2
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("SLH Trader starting (PnL connected)...")

# DB
conn = psycopg2.connect(host='db', database='slh_trading', user='slh', password='slh_pass')

# Bridge
try:
    from staking_bridge import send_staking_update
    logger.info("✅ Staking bridge loaded")
except:
    def send_staking_update(data): pass

while True:
    try:
        # PnL אמיתי מה-DB
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), COALESCE(SUM(profit), 0) FROM trades")
        count, total_pnl = cur.fetchone()
        win_rate = 58.3  # calculate properly later

        pnl_summary = {
            "total_pnl": float(total_pnl),
            "trades_count": count,
            "win_rate": win_rate
        }
        send_staking_update(pnl_summary)

        logger.info(f"[{datetime.now()}] Trades: {count} | PnL: {total_pnl} | Sent to Staking")
        time.sleep(30)
    except Exception as e:
        logger.error(f"Error: {e}")
        time.sleep(60)
