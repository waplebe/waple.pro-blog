from __future__ import annotations

from typing import Optional

from cfd_trader.config import SETTINGS
from cfd_trader.broker.interface import Broker
from cfd_trader.broker.paper import PaperBroker
from cfd_trader.broker.ctrader import cTraderBroker, cTraderCredentials


def create_broker() -> Broker:
    broker_name = (SETTINGS.broker or "paper").lower()
    if broker_name == "ctrader":
        creds: Optional[cTraderCredentials] = None
        if SETTINGS.ctrader_client_id and SETTINGS.ctrader_client_secret and SETTINGS.ctrader_access_token and SETTINGS.ctrader_account_id:
            creds = cTraderCredentials(
                client_id=SETTINGS.ctrader_client_id,
                client_secret=SETTINGS.ctrader_client_secret,
                access_token=SETTINGS.ctrader_access_token,
                account_id=SETTINGS.ctrader_account_id,
            )
        return cTraderBroker(creds=creds, simulate=SETTINGS.paper_trading or creds is None)
    return PaperBroker()
