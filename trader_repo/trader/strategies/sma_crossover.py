
from __future__ import annotations
import pandas as pd
import numpy as np
from .base import Strategy, StrategyResult

class SMACrossover(Strategy):
    name = "SMA Crossover"

    def generate_signals(self, prices: pd.Series, **params):
        fast = int(params.get("fast", 20))
        slow = int(params.get("slow", 100))
        vol_window = int(params.get("vol_window", 20))
        vol_target = float(params.get("vol_target", 0.15))  # annual

        fast_ma = prices.rolling(fast).mean()
        slow_ma = prices.rolling(slow).mean()
        raw = pd.Series(np.where(fast_ma > slow_ma, 1.0, -1.0), index=prices.index).ffill().fillna(0.0)

        daily_ret = prices.pct_change()
        vol = daily_ret.rolling(vol_window).std().fillna(0.0)
        daily_target = vol_target / np.sqrt(252.0)
        scale = (daily_target / (vol.replace(0, np.nan))).clip(upper=1.0).fillna(0.0)
        positions = (raw * scale).clip(-1.0, 1.0)
        return StrategyResult(self.name, positions)
