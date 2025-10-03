from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from cfd_trader.config import SETTINGS
from cfd_trader.execution.orchestrator import ORCH


app = FastAPI(title="CFD Trader Admin")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory=str(__file__).replace("app.py", "static"), html=True), name="static")


@dataclass
class AppState:
    equity: float = SETTINGS.account_equity
    balance: float = SETTINGS.account_equity
    open_positions: int = 0
    daily_pnl: float = 0.0
    equity_curve: list[float] = field(default_factory=list)


STATE = AppState()


class Metrics(BaseModel):
    equity: float
    balance: float
    open_positions: int
    daily_pnl: float
    equity_curve: list[float]


@app.get("/api/metrics", response_model=Metrics)
async def get_metrics():
    return Metrics(
        equity=STATE.equity,
        balance=STATE.balance,
        open_positions=STATE.open_positions,
        daily_pnl=STATE.daily_pnl,
        equity_curve=STATE.equity_curve[-200:],
    )


class CommandRequest(BaseModel):
    text: str


@app.post("/api/command")
async def post_command(cmd: CommandRequest):
    # Simple command parser placeholder
    t = cmd.text.lower()
    if "стоп" in t or "stop" in t:
        return {"status": "ok", "action": "stop"}
    if "заработай" in t or "earn" in t:
        return {"status": "ok", "action": "target_return", "value": 0.10}
    return {"status": "ok", "action": "noop"}


@app.get("/")
async def root():
    return {"service": "cfd-trader-admin", "broker": SETTINGS.broker, "paper": SETTINGS.paper_trading}


@app.post("/api/start")
async def start_orchestrator():
    await ORCH.start()
    return {"status": "started"}
