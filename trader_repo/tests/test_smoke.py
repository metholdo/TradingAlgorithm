
import pandas as pd
import numpy as np
from trader.backtest.engine import run

def test_backtest_smoke():
    idx = pd.date_range("2020-01-01", periods=100, freq="B")
    prices = pd.Series(100+np.cumsum(np.random.randn(len(idx))), index=idx).abs()
    signals = pd.Series(0.0, index=idx)
    signals.iloc[::10] = 1.0
    res = run(prices, signals)
    assert len(res.equity) == len(prices)
