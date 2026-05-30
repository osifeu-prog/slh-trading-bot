import sys
import pandas as pd
from pathlib import Path
from strategies.sma_crossover import SMACrossover
from backtest.backtest_engine import BacktestEngine
from broker.simulated_broker import SimulatedBroker
from risk.risk_engine import RiskEngine

def main(symbol="BTCUSDT", start="2025-01-01", end="2026-05-30"):
    # טעינת נתונים מהיסטוריים
    data_path = Path(f"data/historical/{symbol}.csv")
    if not data_path.exists():
        print(f"❌ No data for {symbol}. Run download first.")
        return
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    df = df[(df.index >= start) & (df.index <= end)]
    
    # אתחול רכיבים
    strategy = SMACrossover(short_window=9, long_window=21)
    broker = SimulatedBroker(initial_balance=10000)
    risk = RiskEngine(max_drawdown=0.2, stop_loss=0.05)
    engine = BacktestEngine(strategy, broker, risk)
    
    # הרצת Backtest
    results = engine.run(df)
    print(f"✅ Backtest completed: {results['total_return']:.2f}%")

if __name__ == "__main__":
    main()
