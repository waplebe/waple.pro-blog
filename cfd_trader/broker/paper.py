from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from cfd_trader.broker.interface import Broker, OrderResult


@dataclass
class PaperPosition:
    symbol: str
    side: str
    size: float
    entry_price: float


class PaperBroker(Broker):
    def __init__(self):
        self.positions: Dict[tuple[str, str], PaperPosition] = {}

    def submit_market_order(self, symbol: str, side: str, size: float) -> OrderResult:
        if size <= 0:
            return OrderResult(False, 0.0, 0.0, message="size<=0")
        price = self._get_mark_price(symbol)
        key = (symbol, side)
        self.positions[key] = PaperPosition(symbol, side, size, price)
        return OrderResult(True, size, price)

    def close_position(self, symbol: str, side: str) -> OrderResult:
        key = (symbol, side)
        pos = self.positions.get(key)
        if not pos:
            return OrderResult(False, 0.0, 0.0, message="no position")
        price = self._get_mark_price(symbol)
        del self.positions[key]
        return OrderResult(True, pos.size, price)

    def _get_mark_price(self, symbol: str) -> float:
        # Simplified: constant price
        return 100.0
