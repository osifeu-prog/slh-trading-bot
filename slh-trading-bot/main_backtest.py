import pandas as pd
from backtesting.engine import BacktestEngine
from strategy.sma_crossover import SmaCrossoverStrategy
from execution.simulated_broker import SimulatedBroker
from risk.risk_engine import RiskEngine
from risk.context_builder import ContextBuilder
from risk.rules.max_position_size import MaxPositionSizeRule
from risk.rules.max_daily_loss import MaxDailyLossRule

df = pd.read_csv("data/historical/btc_1h.csv")
strategy = SmaCrossoverStrategy()
broker = SimulatedBroker()
risk_engine = RiskEngine([MaxPositionSizeRule(50), MaxDailyLossRule(100)])
context_builder = ContextBuilder(broker, broker)
engine = BacktestEngine(df, strategy, risk_engine, context_builder, broker)
results = engine.run()
print(results)
