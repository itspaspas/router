import httpx
import pytest

from gateway.config import Prices
from gateway.hooshyar import HooshyarClient, UpstreamError, compute_cost
from tests.conftest import MODELS


async def test_chat_sends_bearer_and_returns_json(respx_mock):
    route = respx_mock.post("https://h.test/v1/chat/completions").respond(200, json={"model": "m1", "choices": []})
    c = HooshyarClient("https://h.test/v1", "TOKEN", 5)
    assert (await c.chat({"model": "auto", "messages": []}))["model"] == "m1"
    assert route.calls[0].request.headers["authorization"] == "Bearer TOKEN"


async def test_trailing_slash_in_base_url_is_normalized(respx_mock):
    route = respx_mock.post("https://h.test/v1/chat/completions").respond(200, json={})
    await HooshyarClient("https://h.test/v1/", "T", 5).chat({})
    assert route.called


@pytest.mark.parametrize(
    "status,retryable,kind",
    [(400, False, "upstream_4xx"), (413, False, "upstream_4xx"), (500, True, "upstream_5xx"), (503, True, "upstream_5xx")],
)
async def test_chat_error_classification(respx_mock, status, retryable, kind):
    respx_mock.post("https://h.test/v1/chat/completions").respond(status, json={"error": {"message": "x"}})
    with pytest.raises(UpstreamError) as e:
        await HooshyarClient("https://h.test/v1", "T", 5).chat({})
    assert e.value.status == status and e.value.retryable is retryable
    assert e.value.kind == kind


async def test_timeout_is_retryable(respx_mock):
    respx_mock.post("https://h.test/v1/chat/completions").mock(side_effect=httpx.ReadTimeout("t"))
    with pytest.raises(UpstreamError) as e:
        await HooshyarClient("https://h.test/v1", "T", 5).chat({})
    assert e.value.retryable is True and e.value.status is None
    assert e.value.kind == "timeout"


async def test_connection_error_kind(respx_mock):
    respx_mock.post("https://h.test/v1/chat/completions").mock(side_effect=httpx.ConnectError("c"))
    with pytest.raises(UpstreamError) as e:
        await HooshyarClient("https://h.test/v1", "T", 5).chat({})
    assert e.value.retryable is True and e.value.status is None
    assert e.value.kind == "connection"


async def test_error_message_does_not_leak_body(respx_mock):
    respx_mock.post("https://h.test/v1/chat/completions").respond(400, json={"error": {"message": "SECRET-USER-TEXT"}})
    with pytest.raises(UpstreamError) as e:
        await HooshyarClient("https://h.test/v1", "T", 5).chat({"messages": [{"content": "PRIVATE"}]})
    assert "SECRET-USER-TEXT" not in str(e.value) and "PRIVATE" not in str(e.value)


async def test_stream_yields_raw_bytes(respx_mock):
    sse = b'data: {"choices":[{"delta":{"content":"hi"}}]}\n\ndata: [DONE]\n\n'
    respx_mock.post("https://h.test/v1/chat/completions").respond(200, content=sse, headers={"content-type": "text/event-stream"})
    chunks = [c async for c in HooshyarClient("https://h.test/v1", "T", 5).open_stream({"stream": True})]
    assert b"".join(chunks) == sse


async def test_stream_non_200_raises_before_yielding(respx_mock):
    respx_mock.post("https://h.test/v1/chat/completions").respond(503, content=b"nope")
    got = []
    with pytest.raises(UpstreamError) as e:
        async for chunk in HooshyarClient("https://h.test/v1", "T", 5).open_stream({"stream": True}):
            got.append(chunk)
    assert got == [] and e.value.status == 503 and e.value.kind == "upstream_5xx" and e.value.retryable


async def test_list_models(respx_mock):
    route = respx_mock.get(MODELS).respond(200, json={"data": [{"id": "auto"}]})
    out = await HooshyarClient("https://h.test/v1", "TOKEN", 5).list_models()
    assert out["data"][0]["id"] == "auto"
    assert route.calls[0].request.headers["authorization"] == "Bearer TOKEN"


async def test_client_fixture(client, respx_mock):
    respx_mock.get(MODELS).respond(200, json={"data": []})
    assert await client.list_models() == {"data": []}


def test_cost_known_and_unknown():
    p = Prices(verified=False, models={"m1": (1.0, 2.0)})
    assert compute_cost("m1", {"prompt_tokens": 1_000_000, "completion_tokens": 500_000}, p) == pytest.approx(2.0)
    assert compute_cost("unpriced", {"prompt_tokens": 10, "completion_tokens": 10}, p) is None
    assert compute_cost("m1", None, p) is None
    assert compute_cost(None, {"prompt_tokens": 1, "completion_tokens": 1}, p) is None
