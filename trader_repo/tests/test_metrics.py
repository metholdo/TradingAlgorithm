
import pandas as pd
from trader.backtest.metrics import summary_stats

def test_metrics_known_series():
    returns = pd.Series([0.01, -0.005, 0.0, 0.02, -0.01])
    s = summary_stats(returns)
    assert "sharpe" in s and "max_dd" in s
