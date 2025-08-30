
from __future__ import annotations
import pandas as pd

def apply_costs(positions: pd.Series, returns: pd.Series, fees_bps: float, slippage_bps: float) -> pd.Series:
    turn = positions.diff().abs().fillna(0.0)
    cost = (fees_bps + slippage_bps) / 10000.0
    pnl = positions.shift().fillna(0.0) * returns - turn * cost
    return pnl
