
from __future__ import annotations
from typing import List, Optional
import pandas as pd
from ..config import Settings
from datetime import datetime, timezone

try:
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
except Exception:
    StockHistoricalDataClient = None  # type: ignore
    StockBarsRequest = None  # type: ignore
    TimeFrame = None  # type: ignore

class AlpacaSource:
    def __init__(self, settings: Settings):
        self.s = settings
        self.historical = None
        if StockHistoricalDataClient and self.s.alpaca_api_key and self.s.alpaca_secret:
            self.historical = StockHistoricalDataClient(self.s.alpaca_api_key, self.s.alpaca_secret)

    def fetch_history(self, symbols: List[str], start: Optional[str]=None, timeframe: str="1Min") -> pd.DataFrame:
        if not self.historical:
            raise RuntimeError("Alpaca credentials missing or alpaca-py not installed.")
        tf = TimeFrame.Minute if timeframe.lower().startswith("1") else TimeFrame.Day
        start_dt = datetime.fromisoformat(start or self.s.start).replace(tzinfo=timezone.utc)
        req = StockBarsRequest(symbol_or_symbols=symbols, timeframe=tf, start=start_dt)
        bars = self.historical.get_stock_bars(req).df
        bars.index = bars.index.tz_convert(None)
        bars = bars.rename(columns={"close":"close","open":"open","high":"high","low":"low","volume":"volume"})
        bars["symbol"] = bars.index.get_level_values("symbol")
        bars = bars.reset_index().rename(columns={"timestamp":"date"}).set_index(["date","symbol"]).sort_index()
        return bars

    def fetch_live(self, symbols: List[str], timeframe: str="1Min") -> pd.DataFrame:
        return pd.DataFrame()

    def symbols(self) -> List[str]:
        return self.s.symbols
