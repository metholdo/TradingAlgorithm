
from __future__ import annotations
import pandas as pd
import numpy as np

def volatility_targeting(returns: pd.Series, target_annual_vol: float=0.15, window: int=20) -> pd.Series:
    vol = returns.rolling(window).std()
    daily_target = target_annual_vol / np.sqrt(252.0)
    scale = daily_target / (vol.replace(0, np.nan))
    return scale.fillna(0.0).clip(upper=1.0)

def fractional_kelly(mu: float, sigma2: float, fraction: float=0.5) -> float:
    if sigma2 <= 0:
        return 0.0
    k = mu / sigma2
    return float(max(min(fraction * k, 1.0), -1.0))
