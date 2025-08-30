
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import pandas as pd

@dataclass
class StrategyResult:
    name: str
    positions: pd.Series  # -1..1 per date

class Strategy:
    name: str = "BaseStrategy"
    def generate_signals(self, prices: pd.Series, **params: Any) -> StrategyResult:
        raise NotImplementedError
