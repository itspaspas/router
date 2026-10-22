import pytest

from policies.auto_passthrough import AutoPassthrough
from policies.base import RouteRequest


def req(model=None):
    body = {"messages": [{"role": "user", "content": "سلام"}]}
    if model: body["model"] = model
    return RouteRequest(body=body, app_id="chat", conversation_id=None, language="fa")

def test_b0_routes_auto_by_default():
    d = AutoPassthrough().decide(req())
    assert d.target == "auto" and d.policy == "b0_auto" and d.probs == {"auto": 1.0}
    assert d.reasons[0] == "default: hooshyar auto"

@pytest.mark.parametrize("m", ["auto", "small", "medium", "frontier", "some-hooshyar-model"])
def test_b0_honours_explicit_model(m):
    d = AutoPassthrough().decide(req(m))
    assert d.target == m and d.probs == {m: 1.0}
    assert d.reasons == ("explicit model requested",)


def raw_req(model):
    """Build a request whose body carries `model` exactly as given (including None)."""
    body = {"messages": [{"role": "user", "content": "سلام"}], "model": model}
    return RouteRequest(body=body, app_id="chat", conversation_id=None, language="fa")


@pytest.mark.parametrize("m", ["", None])
def test_b0_missing_or_empty_model_uses_default(m):
    d = AutoPassthrough().decide(raw_req(m))
    assert d.target == "auto" and d.probs == {"auto": 1.0}
    assert d.reasons == ("default: hooshyar auto",)


@pytest.mark.parametrize("m", [["x"], {"a": 1}, 123, True, "   "])
def test_b0_malformed_model_falls_back_to_auto_without_raising(m):
    d = AutoPassthrough().decide(raw_req(m))
    assert isinstance(d.target, str)
    assert d.target == "auto" and d.probs == {"auto": 1.0}
    assert d.reasons == ("invalid model value: using hooshyar auto",)


def test_b0_strips_surrounding_whitespace_from_explicit_model():
    d = AutoPassthrough().decide(raw_req("  small \n"))
    assert d.target == "small" and d.probs == {"small": 1.0}
    assert d.reasons == ("explicit model requested",)
