from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Settings:
    # General
    base_currency: str = os.getenv("BASE_CCY", "USD")
    account_equity: float = float(os.getenv("ACCOUNT_EQUITY", "10000"))
    max_leverage: float = float(os.getenv("MAX_LEVERAGE", "20"))

    # Risk
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.01"))  # 1% equity
    max_open_positions: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
    daily_loss_limit_pct: float = float(os.getenv("DAILY_LOSS_LIMIT_PCT", "0.05"))

    # Data
    data_provider: str = os.getenv("DATA_PROVIDER", "synthetic")
    oanda_api_key: Optional[str] = os.getenv("OANDA_API_KEY")
    oanda_account_id: Optional[str] = os.getenv("OANDA_ACCOUNT_ID")

    # Broker
    broker: str = os.getenv("BROKER", "paper")
    ctrader_client_id: Optional[str] = os.getenv("CTRADER_CLIENT_ID")
    ctrader_client_secret: Optional[str] = os.getenv("CTRADER_CLIENT_SECRET")
    ctrader_access_token: Optional[str] = os.getenv("CTRADER_ACCESS_TOKEN")
    ctrader_account_id: Optional[str] = os.getenv("CTRADER_ACCOUNT_ID")

    # Execution
    paper_trading: bool = os.getenv("PAPER_TRADING", "true").lower() == "true"

    # AI / NLP
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")


SETTINGS = Settings()
