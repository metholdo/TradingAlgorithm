
from __future__ import annotations
from pathlib import Path
import pandas as pd
from loguru import logger
from ..config import load_settings
from ..strategies.sma_crossover import SMACrossover
from ..backtest.engine import run as run_bt
from .broker import AlpacaBroker
from .stream import yahoo_bar_stream

def _get_strategy(name: str):
    name = name.lower()
    if name == "sma_crossover":
        return SMACrossover().generate_signals
    from ..strategies.rsi_reversion import RSIReversion
    from ..strategies.vol_breakout import VolBreakout
    if name == "rsi_reversion":
        return RSIReversion().generate_signals
    if name == "vol_breakout":
        return VolBreakout().generate_signals
    raise ValueError(f"Unknown strategy {name}")

def run_live(strategy: str="sma_crossover") -> None:
    s = load_settings()
    strat_fn = _get_strategy(strategy)
    broker = AlpacaBroker(s)

    prices = []
    logs_dir = Path(s.reports_path) / "live"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "decisions.log"

    for bar in yahoo_bar_stream("SPY", interval="1d", lookback_days=200):
        prices.append((bar["time"], bar["close"]))
        ser = pd.Series([p for _, p in prices], index=[t for t,_ in prices], name="close")
        sig = strat_fn(ser).positions
        pos = float(sig.iloc[-1]) if not sig.empty else 0.0
        action = "hold"
        if len(sig) > 1:
            if sig.iloc[-1] > sig.iloc[-2]: action = "buy"
            elif sig.iloc[-1] < sig.iloc[-2]: action = "sell"
        if action in ("buy","sell"):
            broker.place_market_order("SPY", qty=1, side=action)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{bar['time']},{bar['close']},{pos},{action}\n")
