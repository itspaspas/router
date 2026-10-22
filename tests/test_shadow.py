import asyncio
import json
import time

import httpx
import pytest

from gateway.shadow import shadow_auto_judge
from tests.conftest import MSGS, URL, ok_json, ok_text, slow_then_error


async def test_parses_known_model(client, respx_mock):
    respx_mock.post(URL).respond(200, json={"choices": [{"message": {"content": "  gpt-4o-mini\n"}}]})
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o", "gpt-4o-mini"})
    assert r["ok"] and r["parsed_model"] == "gpt-4o-mini" and r["raw"].strip() == "gpt-4o-mini"
    assert json.loads(respx_mock.calls[0].request.content)["model"] == "auto-judge"


async def test_never_raises_on_error_or_timeout(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=httpx.ConnectError("x"))
    r = await shadow_auto_judge(client, MSGS, set())
    assert r == {"raw": None, "parsed_model": None, "latency_ms": r["latency_ms"], "ok": False, "usage": None}


async def test_body_is_non_streaming_auto_judge_with_messages(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=ok_json)
    await shadow_auto_judge(client, MSGS, set())
    sent = json.loads(respx_mock.calls[0].request.content)
    assert sent == {"model": "auto-judge", "stream": False, "messages": MSGS}


async def test_longest_known_model_wins(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=ok_text("gpt-4o-mini"))
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o", "gpt-4o-mini"})
    assert r["parsed_model"] == "gpt-4o-mini"


async def test_no_known_model_in_raw_gives_none_but_ok(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=ok_text("some-other-model"))
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o"})
    assert r["ok"] is True and r["raw"] == "some-other-model" and r["parsed_model"] is None


async def test_empty_known_model_id_never_matches(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=ok_text("gpt-4o"))
    r = await shadow_auto_judge(client, MSGS, {""})
    assert r["parsed_model"] is None


async def test_raw_is_first_200_characters(client, respx_mock):
    content = "x" * 150 + "gpt-4o" + "y" * 200
    respx_mock.post(URL).mock(side_effect=ok_text(content))
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o"})
    assert r["raw"] == content[:200] and len(r["raw"]) == 200
    assert r["parsed_model"] == "gpt-4o"


async def test_latency_is_non_negative_int(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=ok_json)
    r = await shadow_auto_judge(client, MSGS, set())
    assert isinstance(r["latency_ms"], int) and r["latency_ms"] >= 0


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"choices": []},
        {"choices": [{"message": {}}]},
        {"choices": [{"message": {"content": None}}]},
        {"choices": [{"message": {"content": 123}}]},
        {"choices": "not-a-list"},
        ["not", "an", "object"],
    ],
)
async def test_malformed_response_is_not_ok_and_never_raises(client, respx_mock, payload):
    respx_mock.post(URL).respond(200, json=payload)
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o"})
    assert r["ok"] is False and r["raw"] is None and r["parsed_model"] is None


async def test_non_json_response_is_not_ok(client, respx_mock):
    respx_mock.post(URL).respond(200, content=b"<html>oops</html>")
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o"})
    assert r["ok"] is False and r["raw"] is None


async def test_upstream_status_error_is_not_ok(client, respx_mock):
    respx_mock.post(URL).respond(503, json={"error": {"message": "down"}})
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o"})
    assert r == {"raw": None, "parsed_model": None, "latency_ms": r["latency_ms"], "ok": False, "usage": None}


async def test_timeout_returns_not_ok_promptly(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=slow_then_error(1.0))
    start = time.monotonic()
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o"}, timeout_s=0.05)
    elapsed = time.monotonic() - start
    assert r["ok"] is False and r["raw"] is None and r["parsed_model"] is None
    assert elapsed < 0.5


async def test_cancellation_propagates(client, respx_mock):
    respx_mock.post(URL).mock(side_effect=slow_then_error(5.0))
    task = asyncio.create_task(shadow_auto_judge(client, MSGS, set(), timeout_s=30.0))
    await asyncio.sleep(0.05)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


async def test_usage_is_included(client, respx_mock):
    usage = {"prompt_tokens": 9, "completion_tokens": 2, "total_tokens": 11}
    respx_mock.post(URL).respond(200, json={"choices": [{"message": {"content": "m1"}}], "usage": usage})
    r = await shadow_auto_judge(client, MSGS, {"m1"})
    assert r["ok"] is True and r["usage"] == usage


@pytest.mark.parametrize("usage", [None, "x", 5])
async def test_usage_none_when_missing_or_not_a_dict(client, respx_mock, usage):
    respx_mock.post(URL).respond(200, json={"choices": [{"message": {"content": "m1"}}], "usage": usage})
    r = await shadow_auto_judge(client, MSGS, {"m1"})
    assert r["ok"] is True and r["usage"] is None
