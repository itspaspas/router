import asyncio
import dataclasses
import json
import time

import httpx
import pytest

from gateway.app import create_app
from gateway.config import Prices
from gateway.decision_log import hash_user
from gateway.hooshyar import UpstreamError
from policies.auto_passthrough import AutoPassthrough
from tests.conftest import (
    AUTH,
    BODY,
    BODY_FA,
    UP,
    app_settings,
    ok_json,
    ok_text,
    route_by_model,
    serve_app,
    slow_then_error,
)


def sent_models(respx_mock) -> list[str]:
    return [json.loads(c.request.content)["model"] for c in respx_mock.calls]


# --- brief tests -------------------------------------------------------------------------------


async def test_unauthorized(app_client):
    r = await app_client.post("/v1/chat/completions", json=BODY)
    assert r.status_code == 401


async def test_passthrough_to_auto_and_logs(app_client, respx_mock, log_lines):
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": [{"message": {"content": "سلام"}}], "usage": {"prompt_tokens": 5, "completion_tokens": 3}})
    r = await app_client.post("/v1/chat/completions", json=BODY_FA, headers=AUTH)
    assert r.status_code == 200 and r.headers["x-router-policy"] == "b0_auto"
    rec = (await log_lines())[0]
    assert rec["language"] == "fa" and rec["target"] == "auto" and rec["response_model"] == "m1"
    assert rec["text"] is None and rec["cost"] is None and rec["cost_verified"] is False


async def test_upstream_400_passes_through(app_client, respx_mock):
    respx_mock.post(UP).respond(400, json={"error": {"message": "bad"}})
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 400 and len(respx_mock.calls) == 1


async def test_streaming_passthrough(app_client, respx_mock):
    sse = b'data: {"choices":[{"delta":{"content":"hi"}}]}\n\ndata: [DONE]\n\n'
    respx_mock.post(UP).respond(200, content=sse, headers={"content-type": "text/event-stream"})
    r = await app_client.post("/v1/chat/completions", json={**BODY, "stream": True}, headers=AUTH)
    assert r.headers["content-type"].startswith("text/event-stream") and r.content == sse


async def test_slow_failing_shadow_does_not_delay(app_client_shadow, respx_mock):
    respx_mock.post(UP).mock(side_effect=route_by_model({"auto-judge": slow_then_error(seconds=5)}, default=ok_json))
    t0 = time.monotonic()
    r = await app_client_shadow.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and time.monotonic() - t0 < 1.0


async def test_budget_cap_downgrades_auto_only(app_client_capped, respx_mock):   # cfg_capped: cap 0.0 for app "chat"
    respx_mock.post(UP).respond(200, json={"model": "s1", "choices": []})
    await app_client_capped.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert json.loads(respx_mock.calls[-1].request.content)["model"] == "s1"            # auto -> small
    await app_client_capped.post("/v1/chat/completions", json={**BODY, "model": "frontier"}, headers=AUTH)
    assert json.loads(respx_mock.calls[-1].request.content)["model"] == "f1"            # explicit honoured


async def test_policy_exception_falls_back_to_auto(app_client_broken_policy, respx_mock):
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await app_client_broken_policy.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and json.loads(respx_mock.calls[0].request.content)["model"] == "auto"


# --- auth and request validation (decision 1) --------------------------------------------------


@pytest.mark.parametrize("headers", [{}, {"Authorization": "Bearer nope"}, {"Authorization": "k1"},
                                     {"Authorization": "Basic k1"}])
async def test_auth_failures_are_401_and_logged(app_client, respx_mock, log_lines, headers):
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=headers)
    assert r.status_code == 401 and r.json()["error"]["message"]
    assert len(respx_mock.calls) == 0
    (rec,) = await log_lines()
    assert rec["status"] == 401 and rec["error_kind"] == "auth"


class SpyPolicy(AutoPassthrough):
    def __init__(self):
        self.calls = 0

    def decide(self, req):
        self.calls += 1
        return super().decide(req)


@pytest.mark.parametrize("content", [b"{not json", b"[1, 2]", b'"hi"', b"", "\u00ff".encode("latin-1")])
async def test_non_object_body_is_400_before_policy(app_factory, cfg_tiers, respx_mock, log_lines, content):
    spy = SpyPolicy()
    c = await app_factory(dataclasses.replace(cfg_tiers, shadow_enabled=False), spy)
    r = await c.post("/v1/chat/completions", content=content,
                     headers={**AUTH, "content-type": "application/json"})
    assert r.status_code == 400 and r.json()["error"]["type"] == "invalid_request_error"
    assert len(respx_mock.calls) == 0 and spy.calls == 0
    (rec,) = await log_lines()
    assert rec["status"] == 400 and rec["app_id"] == "chat" and rec["attempts"] == []


# --- budget (decision 3 / R7) ------------------------------------------------------------------


async def test_capped_small_failure_falls_back_to_medium_never_frontier(app_client_capped, respx_mock, log_lines):
    respx_mock.post(UP).mock(side_effect=route_by_model({"s1": lambda req: httpx.Response(503)}, default=ok_json))
    r = await app_client_capped.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and r.headers["x-router-served-by"] == "m1"
    assert sent_models(respx_mock) == ["s1", "m1"]
    (rec,) = await log_lines()
    assert rec["target"] == "small" and "budget_cap" in rec["reasons"]
    assert rec["attempts"] == ["small", "medium"] and rec["served_by"] == "m1"


async def test_capped_chain_never_reaches_frontier(app_client_capped, respx_mock):
    respx_mock.post(UP).respond(503)
    r = await app_client_capped.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 503 and "f1" not in sent_models(respx_mock)


async def test_capped_with_unconfigured_small_keeps_auto(app_factory, cfg_capped, respx_mock, log_lines):
    cfg = dataclasses.replace(cfg_capped, shadow_enabled=False, tiers={"small": "", "medium": "", "frontier": ""})
    c = await app_factory(cfg)
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await c.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and sent_models(respx_mock) == ["auto"]
    (rec,) = await log_lines()
    assert rec["target"] == "auto" and "budget_cap_unenforceable" in rec["reasons"]
    assert "budget_cap" not in rec["reasons"] and rec["error_kind"] is None


async def test_capped_with_unconfigured_small_goes_to_auto_not_medium(app_factory, cfg_capped, respx_mock, log_lines):
    cfg = dataclasses.replace(cfg_capped, shadow_enabled=False, tiers={"small": "", "medium": "m1", "frontier": "f1"})
    c = await app_factory(cfg)
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await c.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and sent_models(respx_mock) == ["auto"]
    assert r.headers["x-router-served-by"] == "auto"
    (rec,) = await log_lines()
    assert rec["target"] == "auto" and "budget_cap_unenforceable" in rec["reasons"]


async def test_capped_unenforceable_auto_fallback_skips_frontier(app_factory, cfg_capped, respx_mock):
    cfg = dataclasses.replace(cfg_capped, shadow_enabled=False, tiers={"small": "", "medium": "m1", "frontier": "f1"})
    c = await app_factory(cfg)
    respx_mock.post(UP).respond(503)
    r = await c.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 503 and sent_models(respx_mock) == ["auto", "m1"]


async def test_capped_internal_error_reserve_excludes_frontier(app_client_capped, respx_mock, log_lines, monkeypatch):
    from gateway import app as app_module

    real = app_module.execute
    calls = 0

    async def flaky(*a, **k):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("executor glitch")
        return await real(*a, **k)

    monkeypatch.setattr(app_module, "execute", flaky)
    respx_mock.post(UP).respond(503)
    r = await app_client_capped.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 503 and sent_models(respx_mock) == ["auto", "m1"]   # no f1
    (rec,) = await log_lines()
    assert rec["target"] == "auto" and "internal_error" in rec["reasons"]


async def test_cost_is_recorded_into_budget(app_factory, cfg_tiers, respx_mock):
    priced = dataclasses.replace(cfg_tiers, shadow_enabled=False, per_app_budget={"chat": 1.0},
                                 prices=Prices(verified=False, models={"m1": (1_000_000.0, 0.0)}))
    c = await app_factory(priced)
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": [], "usage": {"prompt_tokens": 1, "completion_tokens": 0}})
    await c.post("/v1/chat/completions", json=BODY, headers=AUTH)   # costs 1.0: reaches the cap
    await c.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert sent_models(respx_mock) == ["auto", "s1"]


# --- upstream errors (decision 4) --------------------------------------------------------------


async def test_exhausted_5xx_returns_status_without_upstream_text(app_client, respx_mock, log_lines):
    respx_mock.post(UP).respond(503, text="secret upstream detail")
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 503 and "secret" not in r.text
    assert r.json()["error"]["type"] == "upstream_5xx" and r.headers["x-router-policy"] == "b0_auto"
    assert sent_models(respx_mock) == ["auto", "m1", "f1"]
    (rec,) = await log_lines()
    assert rec["status"] == 503 and rec["error_kind"] == "upstream_5xx"
    assert rec["attempts"] == ["auto", "medium", "frontier"] and rec["served_by"] is None


@pytest.mark.parametrize("exc,kind", [(httpx.ReadTimeout("t"), "timeout"), (httpx.ConnectError("c"), "connection")])
async def test_exhausted_transport_errors_are_502(app_client, respx_mock, log_lines, exc, kind):
    respx_mock.post(UP).mock(side_effect=exc)
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 502 and r.json()["error"]["type"] == kind
    (rec,) = await log_lines()
    assert rec["status"] == 502 and rec["error_kind"] == kind


async def test_upstream_4xx_body_is_not_forwarded(app_client, respx_mock):
    respx_mock.post(UP).respond(400, json={"error": {"message": "secret detail"}})
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 400 and "secret" not in r.text and r.json()["error"]["type"] == "upstream_4xx"


# --- decision 2: router failures degrade to auto ------------------------------------------------


async def test_policy_error_reason_logged(app_client_broken_policy, respx_mock, log_lines):
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    await app_client_broken_policy.post("/v1/chat/completions", json=BODY, headers=AUTH)
    (rec,) = await log_lines()
    assert rec["policy"] == "b0_auto" and rec["reasons"][-1] == "policy_error"
    assert rec["status"] == 200 and rec["error_kind"] is None


async def test_unexpected_router_error_serves_via_auto(app_client_capped, respx_mock, log_lines, monkeypatch):
    def boom(self, app_id):
        raise RuntimeError("guard broke")

    monkeypatch.setattr("gateway.budget.BudgetGuard.over_cap", boom)
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await app_client_capped.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and sent_models(respx_mock) == ["auto"]   # not "s1": the cap check broke
    (rec,) = await log_lines()
    assert rec["target"] == "auto" and "internal_error" in rec["reasons"] and rec["error_kind"] is None


@pytest.mark.parametrize("target", ["gateway.app.request_features", "gateway.app.hash_user"])
async def test_feature_extraction_failure_still_serves(app_client, respx_mock, log_lines, monkeypatch, target):
    def boom(*a, **k):
        raise RuntimeError("features broke")

    monkeypatch.setattr(target, boom)
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await app_client.post("/v1/chat/completions", json=BODY, headers={**AUTH, "X-User-Id": "u1"})
    assert r.status_code == 200 and sent_models(respx_mock) == ["auto"]
    (rec,) = await log_lines()
    assert rec["status"] == 200 and rec["error_kind"] is None


async def test_budget_record_failure_still_emits_record(app_client, respx_mock, log_lines, monkeypatch):
    def boom(self, app_id, cost):
        raise RuntimeError("guard broke")

    monkeypatch.setattr("gateway.budget.BudgetGuard.record", boom)
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200
    (rec,) = await log_lines()
    assert rec["status"] == 200 and rec["response_model"] == "m1"


async def test_unrecoverable_internal_error_is_500(app_client, respx_mock, log_lines, monkeypatch):
    async def boom(*a, **k):
        raise RuntimeError("executor broke")

    monkeypatch.setattr("gateway.app.execute", boom)
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 500 and "broke" not in r.text
    (rec,) = await log_lines()
    assert rec["status"] == 500 and rec["error_kind"] == "internal"


# --- streaming (decision 5) --------------------------------------------------------------------


async def test_stream_record_has_model_usage_cost_and_headers(app_factory, cfg_tiers, respx_mock, log_lines):
    priced = dataclasses.replace(cfg_tiers, shadow_enabled=False,
                                 prices=Prices(verified=False, models={"m1": (1.0, 2.0)}))
    c = await app_factory(priced)
    sse = (b'data: {"model":"m1","choices":[{"delta":{"content":"hi"}}]}\n\n'
           b'data: {"model":"m1","choices":[],"usage":{"prompt_tokens":4,"completion_tokens":2}}\n\n'
           b"data: [DONE]\n\n")
    respx_mock.post(UP).respond(200, content=sse, headers={"content-type": "text/event-stream"})
    r = await c.post("/v1/chat/completions", json={**BODY, "stream": True}, headers=AUTH)
    assert r.content == sse
    assert r.headers["x-router-policy"] == "b0_auto" and r.headers["x-router-served-by"] == "auto"
    (rec,) = await log_lines()
    assert rec["stream"] is True and rec["status"] == 200 and rec["response_model"] == "m1"
    assert rec["prompt_tokens"] == 4 and rec["completion_tokens"] == 2
    assert rec["cost"] == pytest.approx(8e-6) and rec["cost_verified"] is False


class FakeStreamClient:
    """Stands in for HooshyarClient: streams `chunks`, then (if endless) repeats the last one forever."""

    def __init__(self, chunks, endless=False):
        self.chunks = chunks
        self.endless = endless
        self.closed = False

    async def open_stream(self, body):
        try:
            for c in self.chunks:
                yield c
            while self.endless:
                yield self.chunks[-1]
                await asyncio.sleep(0)
        finally:
            self.closed = True

    async def chat(self, body):
        raise AssertionError("not used")

    async def aclose(self):
        pass


async def test_stream_parses_events_split_across_chunks(app_factory, cfg_tiers, log_lines):
    fake = FakeStreamClient([b'data: {"model":"m', b'1","choices":[{"delta":{"content":"a"}}]}\r\n\r\nda',
                             b'ta: {"choices":[],"usage":{"prompt_tokens":7,"completion_tokens":1}}\n\n',
                             b"data: [DONE]\n\n"])
    c = await app_factory(dataclasses.replace(cfg_tiers, shadow_enabled=False), client=fake, log_text=True)
    r = await c.post("/v1/chat/completions", json={**BODY, "stream": True}, headers=AUTH)
    assert r.content == b"".join(fake.chunks) and fake.closed
    (rec,) = await log_lines()
    assert rec["response_model"] == "m1" and rec["prompt_tokens"] == 7
    assert rec["text"] == {"query": "hi", "answer": "a"}


def chat_scope() -> dict:
    return {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": "POST",
            "scheme": "http", "path": "/v1/chat/completions", "raw_path": b"/v1/chat/completions",
            "query_string": b"", "root_path": "", "client": ("t", 1), "server": ("gw", 80),
            "headers": [(b"authorization", b"Bearer k1"), (b"content-type", b"application/json")]}


async def test_client_disconnect_closes_upstream_stream_and_logs(tmp_path, cfg_tiers):
    fake = FakeStreamClient([b'data: {"choices":[{"delta":{"content":"x"}}]}\n\n'], endless=True)
    app = create_app(app_settings(tmp_path), dataclasses.replace(cfg_tiers, shadow_enabled=False), client=fake)
    first_body = asyncio.Event()
    received = 0

    async def receive():
        nonlocal received
        received += 1
        if received == 1:
            return {"type": "http.request", "body": json.dumps({**BODY, "stream": True}).encode(), "more_body": False}
        await first_body.wait()
        return {"type": "http.disconnect"}

    async def send(msg):
        if msg["type"] == "http.response.body" and msg.get("body"):
            first_body.set()
        await asyncio.sleep(0)

    async with app.router.lifespan_context(app):
        await asyncio.wait_for(app(chat_scope(), receive, send), 5)
        assert fake.closed
        await app.state.gateway.drain()
    recs = [json.loads(line) for line in (tmp_path / "d.jsonl").read_text().splitlines()]
    assert len(recs) == 1 and recs[0]["stream"] is True


class MidStreamErrorClient(FakeStreamClient):
    """Yields one chunk, then fails like an upstream read timeout."""

    async def open_stream(self, body):
        try:
            yield self.chunks[0]
            raise UpstreamError("timeout")
        finally:
            self.closed = True


async def test_mid_stream_upstream_error_cuts_stream_and_logs_kind(tmp_path, cfg_tiers):
    first = b'data: {"choices":[{"delta":{"content":"x"}}]}\n\n'
    fake = MidStreamErrorClient([first])
    app = create_app(app_settings(tmp_path), dataclasses.replace(cfg_tiers, shadow_enabled=False), client=fake)
    sent = []
    received = 0

    async def receive():
        nonlocal received
        received += 1
        if received == 1:
            return {"type": "http.request", "body": json.dumps({**BODY, "stream": True}).encode(), "more_body": False}
        await asyncio.sleep(10)
        return {"type": "http.disconnect"}

    async def send(msg):
        sent.append(msg)

    async with app.router.lifespan_context(app):
        with pytest.raises(UpstreamError):
            await asyncio.wait_for(app(chat_scope(), receive, send), 5)
        assert fake.closed
        await app.state.gateway.drain()
    assert sent[0]["type"] == "http.response.start" and sent[0]["status"] == 200
    bodies = [m for m in sent if m["type"] == "http.response.body"]
    assert bodies[0]["body"] == first and all(m.get("more_body") for m in bodies)   # cut, never completed
    (rec,) = [json.loads(line) for line in (tmp_path / "d.jsonl").read_text().splitlines()]
    assert rec["status"] == 200 and rec["error_kind"] == "timeout" and rec["stream"] is True


# --- shadow (decision 7) -----------------------------------------------------------------------


async def test_shadow_result_merged_into_record(app_client_shadow, respx_mock, log_lines):
    respx_mock.post(UP).mock(side_effect=route_by_model({"auto-judge": ok_text("I would pick m1")}, default=ok_json))
    r = await app_client_shadow.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200
    (rec,) = await log_lines()
    assert rec["shadow_auto_judge"]["ok"] is True and rec["shadow_auto_judge"]["parsed_model"] == "m1"
    judge = [json.loads(c.request.content) for c in respx_mock.calls if json.loads(c.request.content)["model"] == "auto-judge"]
    assert judge == [{"model": "auto-judge", "stream": False, "messages": BODY["messages"]}]


async def test_shutdown_cancels_slow_shadow_and_still_logs(tmp_path, cfg_tiers, respx_mock, monkeypatch):
    monkeypatch.setattr("gateway.app.SHUTDOWN_GRACE_S", 0.1)
    respx_mock.post(UP).mock(side_effect=route_by_model({"auto-judge": slow_then_error(seconds=5)}, default=ok_json))
    app = create_app(app_settings(tmp_path), dataclasses.replace(cfg_tiers, shadow_enabled=True, shadow_sample_rate=1.0))
    t0 = time.monotonic()
    async with serve_app(app) as c:
        assert (await c.post("/v1/chat/completions", json=BODY, headers=AUTH)).status_code == 200
    assert time.monotonic() - t0 < 1.0 and not app.state.gateway.tasks
    (rec,) = [json.loads(line) for line in (tmp_path / "d.jsonl").read_text().splitlines()]
    assert rec["status"] == 200 and rec["shadow_auto_judge"] is None


async def test_shadow_sample_rate_zero_skips_shadow(app_factory, cfg_tiers, respx_mock, log_lines):
    c = await app_factory(dataclasses.replace(cfg_tiers, shadow_enabled=True, shadow_sample_rate=0.0))
    respx_mock.post(UP).mock(side_effect=ok_json)
    await c.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert sent_models(respx_mock) == ["auto"]
    assert (await log_lines())[0]["shadow_auto_judge"] is None


# --- record features (decision 6) --------------------------------------------------------------


async def test_record_features_and_hashes(app_factory, cfg_tiers, respx_mock, log_lines):
    c = await app_factory(dataclasses.replace(cfg_tiers, shadow_enabled=False), log_text=True)
    respx_mock.post(UP).mock(side_effect=ok_text("پاسخ"))
    body = {"messages": [
        {"role": "system", "content": "be brief"},
        {"role": "user", "content": "first question"},
        {"role": "assistant", "content": "ok"},
        {"role": "user", "content": [{"type": "text", "text": "سلام"}, {"type": "image_url", "image_url": {"url": "x"}},
                                     {"type": "text", "text": "دنیا"}]},
    ]}
    r = await c.post("/v1/chat/completions", json=body,
                     headers={**AUTH, "X-User-Id": "u1", "X-Conversation-Id": "conv-9"})
    assert r.status_code == 200
    (rec,) = await log_lines()
    last = "سلام\nدنیا"
    assert rec["app_id"] == "chat" and rec["conversation_id"] == "conv-9"
    assert rec["user_hash"] == hash_user("u1", "s") and rec["last_user_hash"] == hash_user(last, "s")
    assert rec["language"] == "fa" and rec["n_messages"] == 4
    assert rec["prompt_chars"] == len("be brief") + len("first question") + len("ok")
    assert rec["text"] == {"query": last, "answer": "پاسخ"}
    assert rec["latency_ms"] >= 0 and rec["request_id"] and rec["ts"]
    assert "سلام" not in json.dumps(rec["reasons"] + rec["attempts"], ensure_ascii=False)


# --- other endpoints ---------------------------------------------------------------------------


async def test_models_and_healthz(app_client):
    r = await app_client.get("/v1/models")
    assert r.json()["object"] == "list"
    assert [m["id"] for m in r.json()["data"]] == ["auto", "small", "medium", "frontier"]
    assert all(m["object"] == "model" for m in r.json()["data"])
    assert (await app_client.get("/healthz")).json() == {"ok": True}
