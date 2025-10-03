from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


Side = Literal["long", "short"]


@dataclass
class OrderResult:
    success: bool
    filled_size: float
    avg_fill_price: float
    message: str = ""


class Broker:
    def submit_market_order(
        self, symbol: str, side: Side, size: float
    ) -> OrderResult:
        raise NotImplementedError

    def close_position(self, symbol: str, side: Side) -> OrderResult:
        raise NotImplementedError
