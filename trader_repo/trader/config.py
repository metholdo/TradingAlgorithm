
from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import os
import yaml
from pydantic import BaseModel, Field
from dotenv import load_dotenv

class Costs(BaseModel):
    fees_bps: float = 10
    slippage_bps: float = 5

class Risk(BaseModel):
    target_vol_annual: float = 0.15
    kelly_fraction: float = 0.0

class Settings(BaseModel):
    symbols: List[str] = Field(default_factory=lambda: ["AAPL", "MSFT", "SPY"])
    timeframe: str = "1d"
    data_source: str = "yahoo"
    start: str = "2015-01-01"
    costs: Costs = Costs()
    risk: Risk = Risk()
    broker: str = "alpaca"
    cache_path: str = "data/raw"
    reports_path: str = "reports"
    seed: int = 42

    alpaca_api_key: Optional[str] = None
    alpaca_secret: Optional[str] = None
    alpaca_paper: bool = True
    dry_run: bool = True

def load_settings(path: str | Path = "config/settings.yaml") -> Settings:
    load_dotenv()
    cfg_path = Path(path)
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    s = Settings(**data)
    s.alpaca_api_key = os.getenv("ALPACA_API_KEY") or None
    s.alpaca_secret = os.getenv("ALPACA_SECRET") or None
    s.alpaca_paper = (os.getenv("ALPACA_PAPER", "True").lower() == "true")
    s.dry_run = (os.getenv("DRY_RUN", "True").lower() == "true")
    s.cache_path = os.getenv("DATA_CACHE", s.cache_path)
    return s
