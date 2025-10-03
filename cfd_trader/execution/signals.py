from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

import pandas as pd


SignalSide = Literal["long", "short"]


@dataclass
class Signal:
    symbol: str
    side: SignalSide
    price: float
    stop_loss: float
    take_profit: float
    size: float  # units (CFD contracts)
    timestamp: pd.Timestamp


class Strategy:
    def generate(self, df: pd.DataFrame) -> Optional[Signal]:
        raise NotImplementedError
