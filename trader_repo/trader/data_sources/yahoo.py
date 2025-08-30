
from __future__ import annotations
from typing import List, Optional
import pandas as pd
import yfinance as yf
from pathlib import Path
from ..config import Settings
from ..utils.paths import ensure_dir

class YahooSource:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cache = Path(settings.cache_path)
        ensure_dir(self.cache)

    def fetch_history(self, symbols: List[str], start: Optional[str]=None, timeframe: str="1d") -> pd.DataFrame:
        start = start or self.settings.start
        df = yf.download(symbols, start=start, interval="1d", auto_adjust=True, progress=False, group_by='ticker')
        frames = []
        if isinstance(df.columns, pd.MultiIndex):
            for sym in symbols:
                if sym in df.columns.levels[0]:
                    sub = df[sym].copy()
                    sub.columns = [c.lower() for c in sub.columns]
                    sub["symbol"] = sym
                    frames.append(sub)
        else:
            sub = df.copy()
            sub.columns = [c.lower() for c in sub.columns]
            sub["symbol"] = symbols[0]
            frames.append(sub)
        out = pd.concat(frames).reset_index().rename(columns={"index":"date"})
        for sym in symbols:
            p = self.cache / f"{sym}_{timeframe}.parquet"
            sym_df = out[out["symbol"]==sym].set_index("date").sort_index()
            sym_df.to_parquet(p)
        return out.set_index(["date","symbol"]).sort_index()

    def fetch_live(self, symbols: List[str], timeframe: str="1m") -> pd.DataFrame:
        return self.fetch_history(symbols).groupby("symbol").tail(1).reset_index().set_index(["date","symbol"])

    def symbols(self) -> List[str]:
        return self.settings.symbols
