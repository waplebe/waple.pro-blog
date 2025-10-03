from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from cfd_trader.data.indicators import rsi, atr
from cfd_trader.execution.signals import Signal, SignalSide


@dataclass
class RSIMeanReversionConfig:
    rsi_low: int = 30
    rsi_high: int = 70
    atr_mult_sl: float = 1.5
    atr_mult_tp: float = 2.5


class RSIMeanReversionStrategy:
    def __init__(self, config: RSIMeanReversionConfig | None = None):
        self.config = config or RSIMeanReversionConfig()

    def generate(self, df: pd.DataFrame, symbol: str, contract_value: float = 1.0) -> Optional[Signal]:
        if len(df) < 100:
            return None
        df = df.copy()
        df["rsi"] = rsi(df["close"], 14)
        df["atr"] = atr(df, 14)
        last = df.iloc[-1]
        if pd.isna(last["rsi"]) or pd.isna(last["atr"]):
            return None

        price = float(last["close"])
        if last["rsi"] < self.config.rsi_low:
            side: SignalSide = "long"
            stop_loss = price - self.config.atr_mult_sl * float(last["atr"])
            take_profit = price + self.config.atr_mult_tp * float(last["atr"])
        elif last["rsi"] > self.config.rsi_high:
            side = "short"
            stop_loss = price + self.config.atr_mult_sl * float(last["atr"])
            take_profit = price - self.config.atr_mult_tp * float(last["atr"])
        else:
            return None

        size = 0.0  # will be decided by risk manager later
        return Signal(
            symbol=symbol,
            side=side,
            price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            size=size,
            timestamp=df.index[-1] if isinstance(df.index, pd.DatetimeIndex) else pd.Timestamp.utcnow(),
        )
