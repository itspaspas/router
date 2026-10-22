"""Shared constants and fixtures. Tests import constants via `from tests.conftest import URL`."""
from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from gateway.config import load_config
from gateway.hooshyar import HooshyarClient

URL = UP = "https://h.test/v1/chat/completions"
MODELS = "https://h.test/v1/models"
BODY = {"messages": [{"role": "user", "content": "hi"}]}
BODY_FA = {"messages": [{"role": "user", "content": "سلام"}]}
MSGS = BODY["messages"]
AUTH = {"Authorization": "Bearer k1"}

_ROUTER_YAML = Path(__file__).resolve().parent.parent / "config" / "router.yaml"


@pytest.fixture
def client():
    return HooshyarClient("https://h.test/v1", "T", 5)


@pytest.fixture
def cfg_with_budget():
    return dataclasses.replace(
        load_config(_ROUTER_YAML),
        default_daily_budget=5.0,
        per_app_budget={"chat": 1.0},
    )


def _cfg_with_tiers(**tiers):
    return dataclasses.replace(load_config(_ROUTER_YAML), tiers=tiers)


@pytest.fixture
def cfg_tiers():
    return _cfg_with_tiers(small="s1", medium="m1", frontier="f1")


@pytest.fixture
def cfg_no_medium():
    return _cfg_with_tiers(small="s1", medium="", frontier="f1")
