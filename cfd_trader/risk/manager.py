from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from cfd_trader.config import SETTINGS
from cfd_trader.execution.signals import Signal


@dataclass
class RiskState:
    daily_loss_accumulated: float = 0.0
    open_positions: int = 0


@dataclass
class Position:
    symbol: str
    side: str
    entry_price: float
    size: float
    stop_loss: float
    take_profit: float


class SevenRuleRiskManager:
    """Implements a pragmatic 7-rule risk policy for CFDs.

    Rules:
    1) Risk per trade capped at SETTINGS.risk_per_trade of equity
    2) Hard daily loss limit: SETTINGS.daily_loss_limit_pct of equity
    3) Max concurrent open positions: SETTINGS.max_open_positions
    4) Require positive reward:risk >= 1.5
    5) Stop-loss distance must be >= instrument min tick (assumed here) and <= 3% price
    6) Position leverage must not exceed SETTINGS.max_leverage
    7) No averaging down: reject new signals in same symbol+direction if already open
    """

    def __init__(self, equity: Optional[float] = None):
        self.equity = equity or SETTINGS.account_equity
        self.state = RiskState()
        self.open_positions: list[Position] = []

    def _reward_risk(self, sig: Signal) -> float:
        risk = abs(sig.price - sig.stop_loss)
        reward = abs(sig.take_profit - sig.price)
        return reward / (risk + 1e-12)

    def decide_position_size(self, sig: Signal, contract_value: float = 1.0) -> float:
        rule4_rr = self._reward_risk(sig)
        if rule4_rr < 1.5:
            return 0.0

        stop_distance = abs(sig.price - sig.stop_loss)
        if stop_distance <= 0 or stop_distance / sig.price > 0.03:  # rule 5
            return 0.0

        risk_budget = self.equity * SETTINGS.risk_per_trade
        size = risk_budget / (stop_distance * contract_value)

        notional = size * sig.price * contract_value
        leverage = notional / self.equity
        if leverage > SETTINGS.max_leverage:  # rule 6
            size = (SETTINGS.max_leverage * self.equity) / (sig.price * contract_value)

        return max(0.0, float(size))

    def can_open(self, sig: Signal) -> bool:
        if self.state.daily_loss_accumulated <= -SETTINGS.daily_loss_limit_pct * self.equity:  # rule 2
            return False
        if self.state.open_positions >= SETTINGS.max_open_positions:  # rule 3
            return False
        for pos in self.open_positions:  # rule 7
            if pos.symbol == sig.symbol and pos.side == sig.side:
                return False
        return True

    def register_fill(self, sig: Signal, size: float):
        if size <= 0:
            return
        self.state.open_positions += 1
        self.open_positions.append(
            Position(
                symbol=sig.symbol,
                side=sig.side,
                entry_price=sig.price,
                size=size,
                stop_loss=sig.stop_loss,
                take_profit=sig.take_profit,
            )
        )

    def register_close(self, symbol: str, side: str, pnl: float):
        self.state.open_positions = max(0, self.state.open_positions - 1)
        self.state.daily_loss_accumulated += min(0.0, pnl)
        self.open_positions = [p for p in self.open_positions if not (p.symbol == symbol and p.side == side)]
