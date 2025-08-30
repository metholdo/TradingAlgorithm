
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class RiskLimits:
    max_daily_loss: float = 0.02
    max_exposure: float = 1.0
    max_leverage: float = 1.0
    circuit_breaker: float = 0.05

def check_daily_loss(equity: pd.Series, lim: RiskLimits) -> bool:
    if equity.empty:
        return True
    today = equity.iloc[-1] / equity.iloc[0] - 1.0
    return today > -lim.max_daily_loss

def check_exposure(pos: float, lim: RiskLimits) -> bool:
    return abs(pos) <= lim.max_exposure

def check_leverage(lev: float, lim: RiskLimits) -> bool:
    return lev <= lim.max_leverage
