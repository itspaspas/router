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
    assert d.target == m and d.probs == {m: 1.0} and "explicit" in d.reasons[0]
