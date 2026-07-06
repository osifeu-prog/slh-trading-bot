# staking_bridge.py
import json
import requests
import time
from datetime import datetime

def send_staking_update(pnl_data):
    \"\"\"שלח PnL מה-Trader ל-Railway (דרך webhook או direct file)\"\"\"

    try:
        # שמור ב-shared_data
        with open('/shared_data/daily_pnl.json', 'w') as f:
            json.dump({
                'date': datetime.now().isoformat(),
                'total_pnl': pnl_data.get('total_pnl', 0),
                'trades_count': pnl_data.get('trades_count', 0),
                'win_rate': pnl_data.get('win_rate', 0)
            }, f, indent=2)

        print(f"✅ Staking bridge updated: PnL = {pnl_data.get('total_pnl')}")
    except Exception as e:
        print(f"❌ Bridge error: {e}")

# דוגמה לשימוש ב-run_trader.py
if __name__ == "__main__":
    sample = {'total_pnl': 245.5, 'trades_count': 12, 'win_rate': 58.3}
    send_staking_update(sample)
