"""Shared constants and fixtures. Tests import constants via `from tests.conftest import URL`."""
from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from gateway.config import load_config
from gateway.decision_log import DecisionRecord
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


def make_record(**overrides) -> DecisionRecord:
    """A valid DecisionRecord with neutral values; override any field by keyword."""
    fields = dict(
        request_id="r1",
        ts="2026-10-22T00:00:00+00:00",
        app_id="chat",
        user_hash=None,
        conversation_id=None,
        language="fa",
        n_messages=1,
        prompt_chars=10,
        policy="auto_passthrough",
        target="auto",
        probs={},
        reasons=[],
        attempts=[],
        served_by="auto",
        response_model="m1",
        prompt_tokens=None,
        completion_tokens=None,
        cost=None,
        cost_verified=False,
        latency_ms=5,
        status=200,
        error_kind=None,
        stream=False,
    )
    fields.update(overrides)
    return DecisionRecord(**fields)
