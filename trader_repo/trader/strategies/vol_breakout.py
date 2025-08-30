
from __future__ import annotations
import pandas as pd
import numpy as np
from .base import Strategy, StrategyResult

def atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int=14) -> pd.Series:
    tr = pd.concat([
        (high - low),
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(window).mean()

class VolBreakout(Strategy):
    name = "Volatility Breakout"

    def generate_signals(self, prices: pd.Series, **params):
        df = prices.to_frame("close")
        df["high"] = df["close"].rolling(2).max().fillna(df["close"])
        df["low"] = df["close"].rolling(2).min().fillna(df["close"])
        window = int(params.get("atr_window", 14))
        mult = float(params.get("atr_mult", 2.0))
        trail = float(params.get("trail_mult", 2.0))

        a = atr(df["high"], df["low"], df["close"], window)
        upper = df["close"].rolling(window).max() - mult * a
        lower = df["close"].rolling(window).min() + mult * a

        pos = pd.Series(0.0, index=prices.index)
        holding = 0.0
        stop = None
        for i in range(len(prices)):
            price = df["close"].iloc[i]
            if holding > 0:
                stop = max(stop or (price - trail*a.iloc[i]), price - trail*a.iloc[i])
                if price < stop:
                    holding = 0.0
            elif holding < 0:
                stop = min(stop or (price + trail*a.iloc[i]), price + trail*a.iloc[i])
                if price > stop:
                    holding = 0.0
            else:
                if price > upper.iloc[i]:
                    holding = 1.0; stop = price - trail*a.iloc[i]
                elif price < lower.iloc[i]:
                    holding = -1.0; stop = price + trail*a.iloc[i]
            pos.iloc[i] = holding
        return StrategyResult(self.name, pos)
