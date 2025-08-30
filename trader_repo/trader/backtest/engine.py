
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from .costs import apply_costs
from .metrics import summary_stats, equity_curve

@dataclass
class Result:
    equity: pd.Series
    returns: pd.Series
    positions: pd.Series
    trades: pd.DataFrame
    summary: dict

def run(prices: pd.Series, signals: pd.Series, fees_bps: float=10, slippage_bps: float=5,
        cash: float=1.0, leverage: float=1.0) -> Result:
    prices = prices.ffill().dropna()
    rets = prices.pct_change().fillna(0.0)
    sig = signals.reindex(prices.index).fillna(0.0).clip(-1,1) * leverage
    pnl = apply_costs(sig, rets, fees_bps, slippage_bps)
    eq = cash * (1 + pnl).cumprod()
    chg = sig.diff().fillna(sig)
    entries = chg[chg != 0].index
    trades = []
    prev = None; prev_pos = 0.0; entry_px = None
    for t in prices.index:
        if t in entries:
            if prev is not None and prev_pos != 0:
                if prev_pos > 0:
                    ret = prices.loc[t] / entry_px - 1
                else:
                    ret = entry_px / prices.loc[t] - 1
                trades.append({"entry": prev, "exit": t, "position": prev_pos, "ret": float(ret)})
            prev = t; prev_pos = sig.loc[t]; entry_px = prices.loc[t]
    trades_df = pd.DataFrame(trades)
    summ = summary_stats(pnl)
    return Result(eq, pnl, sig, trades_df, summ)
