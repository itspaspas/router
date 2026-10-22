"""In-memory per-app daily spend guard (UTC day)."""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Callable

from gateway.config import RouterConfig


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BudgetGuard:
    def __init__(self, cfg: RouterConfig, clock: Callable[[], datetime] = utcnow):
        self._cfg = cfg
        self._clock = clock
        self._day: date | None = None
        self._spend: dict[str, float] = {}

    def _today(self) -> date:
        now = self._clock()
        if now.tzinfo is not None:
            now = now.astimezone(timezone.utc)
        today = now.date()
        if today != self._day:
            self._day = today
            self._spend = {}
        return today

    def _cap(self, app_id: str) -> float:
        return self._cfg.per_app_budget.get(app_id, self._cfg.default_daily_budget)

    def over_cap(self, app_id: str) -> bool:
        self._today()
        return self._spend.get(app_id, 0.0) >= self._cap(app_id)

    def record(self, app_id: str, cost: float | None) -> None:
        if cost is None:
            return
        self._today()
        self._spend[app_id] = self._spend.get(app_id, 0.0) + cost
