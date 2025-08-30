
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def fetch_history(self, symbols: List[str], start: Optional[str]=None, timeframe: str="1d") -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def fetch_live(self, symbols: List[str], timeframe: str="1m") -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def symbols(self) -> List[str]:
        raise NotImplementedError
