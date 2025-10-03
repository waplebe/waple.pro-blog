from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
import pandas as pd


@dataclass
class Candle:
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class DataSource:
    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        raise NotImplementedError


class SyntheticDataSource(DataSource):
    def __init__(self, seed: int = 42):
        self.random = np.random.default_rng(seed)

    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        now = datetime.utcnow().replace(second=0, microsecond=0)
        dt = self._timeframe_to_timedelta(timeframe)
        times = [now - i * dt for i in range(limit)][::-1]
        price = 100 + np.cumsum(self.random.normal(0, 0.2, size=limit))
        noise = self.random.normal(0, 0.1, size=limit)
        close = price + noise
        high = np.maximum(price + np.abs(noise) * 1.5, close)
        low = np.minimum(price - np.abs(noise) * 1.5, close)
        open_ = np.concatenate([[price[0]], close[:-1]])
        volume = np.abs(self.random.normal(1000, 100, size=limit))
        df = pd.DataFrame(
            {
                "time": times,
                "open": open_,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
            }
        )
        return df

    @staticmethod
    def _timeframe_to_timedelta(tf: str) -> timedelta:
        if tf.endswith("m"):
            return timedelta(minutes=int(tf[:-1]))
        if tf.endswith("h"):
            return timedelta(hours=int(tf[:-1]))
        if tf.endswith("d"):
            return timedelta(days=int(tf[:-1]))
        raise ValueError(f"Unsupported timeframe: {tf}")


class OandaStubDataSource(DataSource):
    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        # Placeholder: return synthetic for now
        return SyntheticDataSource().fetch_candles(symbol, timeframe, limit)
