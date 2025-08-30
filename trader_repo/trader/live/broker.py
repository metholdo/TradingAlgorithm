
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..config import Settings
from loguru import logger

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
except Exception:
    TradingClient = None  # type: ignore
    MarketOrderRequest = None  # type: ignore
    OrderSide = None  # type: ignore
    TimeInForce = None  # type: ignore

@dataclass
class OrderResult:
    id: str
    symbol: str
    qty: float
    status: str

class AlpacaBroker:
    def __init__(self, settings: Settings):
        self.s = settings
        if not TradingClient or not self.s.alpaca_api_key or not self.s.alpaca_secret:
            logger.warning("Alpaca not configured, running in DRY mode.")
            self.client = None
        else:
            self.client = TradingClient(self.s.alpaca_api_key, self.s.alpaca_secret, paper=self.s.alpaca_paper)

    def place_market_order(self, symbol: str, qty: float, side: str="buy") -> Optional[OrderResult]:
        if self.s.dry_run or not self.client:
            logger.info(f"[DRY] {side.upper()} {qty} {symbol}")
            return OrderResult("dry", symbol, qty, "accepted")
        req = MarketOrderRequest(symbol=symbol, qty=qty, side=OrderSide.BUY if side=='buy' else OrderSide.SELL,
                                 time_in_force=TimeInForce.DAY)
        o = self.client.submit_order(req)
        return OrderResult(str(o.id), symbol, float(qty), str(o.status))
