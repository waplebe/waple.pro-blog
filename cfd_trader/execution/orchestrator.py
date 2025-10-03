from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from cfd_trader.config import SETTINGS
from cfd_trader.data.sources import SyntheticDataSource
from cfd_trader.execution.strategy_rsi_mean_reversion import RSIMeanReversionStrategy
from cfd_trader.execution.engine import ExecutionEngine
from cfd_trader.broker.factory import create_broker
from cfd_trader.web.app import STATE


@dataclass
class OrchestratorConfig:
    symbol: str = "XAUUSD"
    timeframe: str = "15m"
    poll_seconds: int = 10


class Orchestrator:
    def __init__(self, config: OrchestratorConfig | None = None):
        self.config = config or OrchestratorConfig()
        self.data = SyntheticDataSource()
        self.strategy = RSIMeanReversionStrategy()
        self.engine = ExecutionEngine(create_broker())
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        if self._task and not self._task.done():
            return
        self._task = asyncio.create_task(self._run_loop())

    async def _run_loop(self):
        while True:
            try:
                df = self.data.fetch_candles(self.config.symbol, self.config.timeframe, limit=400)
                df.set_index(pd.to_datetime(df["time"]), inplace=True)
                sig = self.strategy.generate(df, symbol=self.config.symbol)
                if sig:
                    report = self.engine.process_signal(sig)
                # Update metrics (demo)
                STATE.equity_curve.append(STATE.equity)
            except Exception as exc:
                # In production log via loguru
                pass
            await asyncio.sleep(self.config.poll_seconds)


ORCH = Orchestrator()
