import dataclasses
import json

import httpx
import pytest

from gateway.executor import execute
from gateway.hooshyar import UpstreamError
from policies.base import Decision
from tests.conftest import BODY, URL

AUTO = Decision("auto", "b0_auto", {"auto": 1.0})


async def test_auto_success_no_fallback(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(200, json={"model": "x"})
    r = await execute(AUTO, BODY, client, cfg_tiers, stream=False)
    assert r.served_by == "auto" and r.attempts == ["auto"]
    assert r.response == {"model": "x"} and r.stream is None
    assert json.loads(respx_mock.calls[0].request.content)["model"] == "auto"


async def test_auto_500_falls_back_to_medium(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(500), httpx.Response(200, json={"model": "m1"})])
    r = await execute(AUTO, BODY, client, cfg_tiers, stream=False)
    assert r.served_by == "m1" and r.attempts == ["auto", "medium"]
    assert json.loads(respx_mock.calls[1].request.content)["model"] == "m1"


async def test_4xx_is_not_retried(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(400, json={"error": {"message": "context too long"}})
    with pytest.raises(UpstreamError) as e:
        await execute(AUTO, BODY, client, cfg_tiers, stream=False)
    assert e.value.status == 400 and len(respx_mock.calls) == 1


async def test_unconfigured_tier_skipped(respx_mock, cfg_no_medium, client):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(503), httpx.Response(200, json={"model": "f1"})])
    r = await execute(AUTO, BODY, client, cfg_no_medium, stream=False)
    assert r.attempts == ["auto", "medium:unconfigured", "frontier"] and r.served_by == "f1"


async def test_stream_fallback_only_before_first_byte(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(502), httpx.Response(200, content=b"data: [DONE]\n\n")])
    r = await execute(AUTO, {**BODY, "stream": True}, client, cfg_tiers, stream=True)
    assert r.attempts == ["auto", "medium"] and b"".join([c async for c in r.stream]) == b"data: [DONE]\n\n"
    assert r.served_by == "m1" and r.response is None


async def test_empty_stream_does_not_crash(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(200, content=b"")
    r = await execute(AUTO, {**BODY, "stream": True}, client, cfg_tiers, stream=True)
    assert r.attempts == ["auto"] and r.served_by == "auto"
    assert [c async for c in r.stream] == []


async def test_all_attempts_fail_raises_last_error(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(500), httpx.Response(502), httpx.Response(503)])
    with pytest.raises(UpstreamError) as e:
        await execute(AUTO, BODY, client, cfg_tiers, stream=False)
    assert e.value.status == 503 and len(respx_mock.calls) == 3


async def test_tier_target_resolves_and_falls_back(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).mock(side_effect=[httpx.ConnectError("x"), httpx.Response(200, json={"model": "f1"})])
    r = await execute(Decision("medium", "p", {}), BODY, client, cfg_tiers, stream=False)
    assert r.attempts == ["medium", "frontier"] and r.served_by == "f1"
    assert json.loads(respx_mock.calls[0].request.content)["model"] == "m1"


async def test_concrete_model_verbatim_no_fallback(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(500)
    with pytest.raises(UpstreamError) as e:
        await execute(Decision("some-model", "p", {}), BODY, client, cfg_tiers, stream=False)
    assert e.value.status == 500 and len(respx_mock.calls) == 1
    assert json.loads(respx_mock.calls[0].request.content)["model"] == "some-model"


async def test_no_attempt_possible_raises_connection_error(respx_mock, cfg_no_medium, client):
    cfg = dataclasses.replace(cfg_no_medium, tiers={"small": "", "medium": "", "frontier": ""})
    with pytest.raises(UpstreamError) as e:
        await execute(Decision("small", "p", {}), BODY, client, cfg, stream=False)
    assert e.value.kind == "connection" and e.value.status is None
    assert len(respx_mock.calls) == 0


async def test_body_not_mutated(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(200, json={})
    body = {**BODY, "model": "orig"}
    await execute(AUTO, body, client, cfg_tiers, stream=False)
    assert body["model"] == "orig"


class _FakeClient:
    """Open_stream stand-in that records whether its generators were closed."""

    def __init__(self, scripts):
        self.scripts = list(scripts)
        self.closed = []

    def open_stream(self, body):
        script = self.scripts.pop(0)
        idx = len(self.closed)
        self.closed.append(False)

        async def gen():
            try:
                for item in script:
                    if isinstance(item, Exception):
                        raise item
                    yield item
            finally:
                self.closed[idx] = True

        return gen()


async def test_early_consumer_stop_closes_upstream(cfg_tiers):
    fake = _FakeClient([[b"a", b"b", b"c"]])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    it = r.stream.__aiter__()
    assert await it.__anext__() == b"a"
    await r.stream.aclose()
    assert fake.closed == [True]


async def test_mid_stream_error_propagates_without_fallback(cfg_tiers):
    fake = _FakeClient([[b"a", UpstreamError("connection")], [b"zzz"]])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    got = []
    with pytest.raises(UpstreamError):
        async for c in r.stream:
            got.append(c)
    assert got == [b"a"] and r.attempts == ["auto"] and len(fake.scripts) == 1
    assert fake.closed == [True]


async def test_failed_attempt_stream_is_closed(cfg_tiers):
    fake = _FakeClient([[UpstreamError("upstream_5xx", 502)], [b"ok"]])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    assert r.attempts == ["auto", "medium"] and fake.closed[0] is True
    assert [c async for c in r.stream] == [b"ok"]
