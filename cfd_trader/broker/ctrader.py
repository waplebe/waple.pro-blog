from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from loguru import logger

from cfd_trader.broker.interface import Broker, OrderResult
from cfd_trader.broker.paper import PaperBroker


@dataclass
class cTraderCredentials:
    client_id: str
    client_secret: str
    access_token: str
    account_id: str


class cTraderBroker(Broker):
    def __init__(self, creds: Optional[cTraderCredentials] = None, simulate: bool = True):
        self.creds = creds
        self.simulate = simulate
        self._paper = PaperBroker() if simulate else None

    def _is_configured(self) -> bool:
        return bool(
            self.creds
            and self.creds.client_id
            and self.creds.client_secret
            and self.creds.access_token
            and self.creds.account_id
        )

    def submit_market_order(self, symbol: str, side: str, size: float) -> OrderResult:
        if self.simulate or not self._is_configured():
            logger.info("cTrader STUB -> delegating market order to PaperBroker")
            return self._paper.submit_market_order(symbol, side, size) if self._paper else OrderResult(False, 0.0, 0.0, "paper-disabled")
        # TODO: Integrate with Spotware cTrader Open API for real orders
        return OrderResult(False, 0.0, 0.0, "ctrader-openapi-not-implemented")

    def close_position(self, symbol: str, side: str) -> OrderResult:
        if self.simulate or not self._is_configured():
            logger.info("cTrader STUB -> delegating close to PaperBroker")
            return self._paper.close_position(symbol, side) if self._paper else OrderResult(False, 0.0, 0.0, "paper-disabled")
        # TODO: Integrate with Spotware cTrader Open API for real closes
        return OrderResult(False, 0.0, 0.0, "ctrader-openapi-not-implemented")
