from datetime import datetime, timezone

import dataclasses

from gateway.budget import BudgetGuard

UTC = timezone.utc


def test_budget_cap_and_midnight_reset(cfg_with_budget):   # fixture: default 5.0, per_app {"chat": 1.0}
    now = [datetime(2026, 10, 22, 23, 0, tzinfo=UTC)]
    g = BudgetGuard(cfg_with_budget, clock=lambda: now[0])
    g.record("chat", 0.6); assert not g.over_cap("chat")
    g.record("chat", 0.5); assert g.over_cap("chat")
    g.record("chat", None); assert g.over_cap("chat")           # unknown cost ignored
    assert not g.over_cap("other")                               # default cap 5.0
    now[0] = datetime(2026, 10, 23, 0, 1, tzinfo=UTC); assert not g.over_cap("chat")


def test_zero_cap_is_over_from_start(cfg_with_budget):
    cfg = dataclasses.replace(cfg_with_budget, per_app_budget={"chat": 0.0})
    assert BudgetGuard(cfg).over_cap("chat")


def test_non_utc_clock_is_converted_to_utc(cfg_with_budget):
    from datetime import timedelta
    tehran = timezone(timedelta(hours=3, minutes=30))
    now = [datetime(2026, 10, 23, 2, 0, tzinfo=tehran)]  # 22:30 UTC on the 22nd
    g = BudgetGuard(cfg_with_budget, clock=lambda: now[0])
    g.record("chat", 2.0)
    assert g.over_cap("chat")
    now[0] = datetime(2026, 10, 23, 4, 0, tzinfo=tehran)  # 00:30 UTC on the 23rd
    assert not g.over_cap("chat")
