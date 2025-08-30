
from __future__ import annotations
import pandas as pd
import numpy as np
from .base import Strategy, StrategyResult

def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0).ewm(alpha=1/window, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1/window, adjust=False).mean()
    rs = up / (down + 1e-12)
    return 100 - (100 / (1 + rs))

class RSIReversion(Strategy):
    name = "RSI Reversion"

    def generate_signals(self, prices: pd.Series, **params):
        window = int(params.get("window", 14))
        entry = float(params.get("entry", 30.0))
        exit_level = float(params.get("exit", 50.0))
        stop = float(params.get("stop", 0.08))

        r = rsi(prices, window)
        pos = pd.Series(0.0, index=prices.index)

        long_entry = r < entry
        long_exit = r > exit_level
        short_entry = r > (100 - entry)
        short_exit = r < (100 - exit_level)

        holding = 0.0
        peak = prices.iloc[0] if not prices.empty else 0.0
        trough = prices.iloc[0] if not prices.empty else 0.0
        for i in range(len(prices)):
            price = prices.iloc[i]
            if holding > 0:
                peak = max(peak, price)
                if long_exit.iloc[i] or (price < peak * (1 - stop)):
                    holding = 0.0
            elif holding < 0:
                trough = min(trough, price)
                if short_exit.iloc[i] or (price > trough * (1 + stop)):
                    holding = 0.0
            else:
                if long_entry.iloc[i]:
                    holding = 1.0; peak = price
                elif short_entry.iloc[i]:
                    holding = -1.0; trough = price
            pos.iloc[i] = holding
        return StrategyResult(self.name, pos)
