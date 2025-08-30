
from __future__ import annotations
from typing import Iterator, Dict, Any
import time
import yfinance as yf

def yahoo_bar_stream(symbol: str, interval: str="1d", lookback_days: int=30) -> Iterator[Dict[str, Any]]:
    data = yf.download(symbol, period=f"{lookback_days}d", interval=interval, auto_adjust=True, progress=False)
    for t, row in data.iterrows():
        yield {"symbol": symbol, "time": t.to_pydatetime(), "close": float(row["Close"])}
        time.sleep(0.01)
