
from __future__ import annotations
import pandas as pd
import numpy as np

def _dd(equity: pd.Series) -> pd.Series:
    peak = equity.cummax()
    return (equity / peak) - 1.0

def summary_stats(returns: pd.Series) -> dict:
    if returns.empty:
        return {"sharpe":0,"sortino":0,"calmar":0,"max_dd":0,"hit_rate":0,"turnover":0,"exposure":0,"var_95":0,"tail_ratio":0}
    ann = (1 + returns).prod() ** (252/len(returns)) - 1
    vol = returns.std() * (252 ** 0.5)
    sharpe = ann / (vol + 1e-12)
    downside = returns.copy()
    downside[downside > 0] = 0
    sortino = ann / ((downside.std() * (252 ** 0.5)) + 1e-12)
    equity = (1 + returns).cumprod()
    dd = _dd(equity)
    max_dd = dd.min()
    calmar = (-ann / (max_dd + 1e-12)) if max_dd < 0 else 0.0
    hit_rate = (returns > 0).mean()
    turnover = returns.abs().rolling(2).sum().mean()
    exposure = returns.ne(0).mean()
    var_95 = np.percentile(returns, 5)
    tail_ratio = (np.percentile(returns, 95) / (abs(var_95) + 1e-12))
    return {"sharpe":float(sharpe), "sortino":float(sortino), "calmar":float(calmar), "max_dd":float(max_dd),
            "hit_rate":float(hit_rate), "turnover":float(turnover), "exposure":float(exposure),
            "var_95":float(var_95), "tail_ratio":float(tail_ratio)}

def equity_curve(returns: pd.Series) -> pd.Series:
    return (1 + returns).cumprod()
