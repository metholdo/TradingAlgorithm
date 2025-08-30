
import pandas as pd
import numpy as np
from trader.strategies.sma_crossover import SMACrossover
from trader.strategies.rsi_reversion import RSIReversion
from trader.strategies.vol_breakout import VolBreakout

idx = pd.date_range("2020-01-01", periods=200, freq="B")
prices = pd.Series(100+np.cumsum(np.random.randn(len(idx))), index=idx).abs()

def test_sma_positions_shape():
    s = SMACrossover().generate_signals(prices)
    assert len(s.positions) == len(prices)

def test_rsi_positions_shape():
    s = RSIReversion().generate_signals(prices)
    assert len(s.positions) == len(prices)

def test_breakout_positions_shape():
    s = VolBreakout().generate_signals(prices)
    assert len(s.positions) == len(prices)
