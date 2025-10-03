from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from cfd_trader.broker.interface import Broker
from cfd_trader.execution.signals import Signal
from cfd_trader.risk.manager import SevenRuleRiskManager


@dataclass
class ExecutionReport:
    accepted: bool
    reason: str = ""


class ExecutionEngine:
    def __init__(self, broker: Broker, risk: Optional[SevenRuleRiskManager] = None):
        self.broker = broker
        self.risk = risk or SevenRuleRiskManager()

    def process_signal(self, signal: Signal, contract_value: float = 1.0) -> ExecutionReport:
        if not self.risk.can_open(signal):
            return ExecutionReport(False, reason="risk_reject")
        size = self.risk.decide_position_size(signal, contract_value)
        if size <= 0:
            return ExecutionReport(False, reason="size_zero")
        order = self.broker.submit_market_order(signal.symbol, signal.side, size)
        if not order.success:
            return ExecutionReport(False, reason=f"broker_reject:{order.message}")
        self.risk.register_fill(signal, order.filled_size)
        return ExecutionReport(True)
