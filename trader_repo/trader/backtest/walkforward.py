
from __future__ import annotations
import pandas as pd
from typing import Callable, Any

def expanding(prices: pd.Series, split_dates: list[str], fit: Callable[[pd.Series], Any],
              evaluate: Callable[[pd.Series, Any], float]) -> dict:
    results = []
    for d in split_dates:
        train = prices[:d]
        test = prices[d:]
        model = fit(train)
        score = evaluate(test, model)
        results.append({"split": d, "score": score})
    return {"scheme":"expanding", "results": results}

def rolling(prices: pd.Series, window_days: int, step_days: int,
            fit: Callable[[pd.Series], Any], evaluate: Callable[[pd.Series, Any], float]) -> dict:
    idx = prices.index
    res = []
    start = 0
    while start + window_days < len(idx):
        train = prices.iloc[start:start+window_days]
        test = prices.iloc[start+window_days : start+window_days+step_days]
        model = fit(train)
        score = evaluate(test, model)
        res.append({"start": str(idx[start].date()), "score": score})
        start += step_days
    return {"scheme":"rolling", "results": res}
