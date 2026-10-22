import asyncio
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
    assert e.value.attempts == ["auto"]


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
    assert e.value.attempts == ["auto", "medium", "frontier"]


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
    assert e.value.attempts == ["small:unconfigured", "medium:unconfigured", "frontier:unconfigured"]


async def test_body_not_mutated(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(200, json={})
    body = {**BODY, "model": "orig"}
    await execute(AUTO, body, client, cfg_tiers, stream=False)
    assert body["model"] == "orig"


class _SpyStream:
    """Async-iterator spy over scripted items. Counts aclose() calls made by the executor.

    Unlike a plain async generator, it stays "open" until aclose() is called, so a test can
    only pass if the executor itself closes it. A script item "hang" blocks forever.
    """

    def __init__(self, script):
        self._script = list(script)
        self.aclose_calls = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._script:
            raise StopAsyncIteration
        item = self._script.pop(0)
        if item == "hang":
            await asyncio.Event().wait()
        if isinstance(item, Exception):
            raise item
        return item

    async def aclose(self):
        self.aclose_calls += 1


class _FakeClient:
    def __init__(self, *scripts):
        self.spies = [_SpyStream(s) for s in scripts]
        self.bodies = []
        self._next = 0

    def open_stream(self, body):
        self.bodies.append(body)
        spy = self.spies[self._next]
        self._next += 1
        return spy


async def test_early_consumer_stop_closes_upstream(cfg_tiers):
    fake = _FakeClient([b"a", b"b", b"c"])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    assert await r.stream.__anext__() == b"a"
    assert fake.spies[0].aclose_calls == 0
    await r.stream.aclose()
    assert fake.spies[0].aclose_calls == 1


async def test_unstarted_stream_aclose_closes_upstream(cfg_tiers):
    fake = _FakeClient([b"a"])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    await r.stream.aclose()
    assert fake.spies[0].aclose_calls == 1


async def test_mid_stream_error_propagates_without_fallback(cfg_tiers):
    fake = _FakeClient([b"a", UpstreamError("connection")], [b"zzz"])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    got = []
    with pytest.raises(UpstreamError):
        async for c in r.stream:
            got.append(c)
    assert got == [b"a"] and r.attempts == ["auto"] and len(fake.bodies) == 1
    # the stream's own error path must close the upstream (consumer never calls aclose)
    assert fake.spies[0].aclose_calls == 1


async def test_failed_attempt_stream_is_closed(cfg_tiers):
    fake = _FakeClient([UpstreamError("upstream_5xx", 502)], [b"ok"])
    r = await execute(AUTO, BODY, fake, cfg_tiers, stream=True)
    assert r.attempts == ["auto", "medium"]
    assert fake.spies[0].aclose_calls == 1  # abandoned attempt closed by the executor
    assert fake.spies[1].aclose_calls == 0  # winning stream still open
    assert [c async for c in r.stream] == [b"ok"]
    assert fake.spies[1].aclose_calls == 1


async def test_cancelled_first_chunk_closes_upstream(cfg_tiers):
    fake = _FakeClient(["hang"])
    task = asyncio.create_task(execute(AUTO, BODY, fake, cfg_tiers, stream=True))
    await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert fake.spies[0].aclose_calls == 1


async def test_stream_4xx_not_escalated(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).respond(400, json={"error": {"message": "bad"}})
    with pytest.raises(UpstreamError) as e:
        await execute(AUTO, {**BODY, "stream": True}, client, cfg_tiers, stream=True)
    assert e.value.status == 400 and len(respx_mock.calls) == 1


async def test_stream_all_attempts_fail_raises_last_error(respx_mock, cfg_tiers, client):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(500), httpx.Response(502), httpx.Response(503)])
    with pytest.raises(UpstreamError) as e:
        await execute(AUTO, {**BODY, "stream": True}, client, cfg_tiers, stream=True)
    assert e.value.status == 503 and len(respx_mock.calls) == 3
