"""B0: pass-through policy. Leaves routing to Hooshyar `auto` unless the client names a model."""
from __future__ import annotations

from policies.base import Decision, RouteRequest

DEFAULT_REASON = "default: hooshyar auto"
EXPLICIT_REASON = "explicit model requested"
INVALID_REASON = "invalid model value: using hooshyar auto"


class AutoPassthrough:
    """Last-resort policy: must never raise and must always return a str target."""

    name = "b0_auto"

    def decide(self, req: RouteRequest) -> Decision:
        # Missing, None or "" means the client did not choose a model. A non-string or
        # whitespace-only value is malformed and also falls back to auto. Any other
        # string, including "auto", is an explicit request and is honoured (stripped).
        model = req.body.get("model")
        if model is None or (isinstance(model, str) and model == ""):
            return self._auto(DEFAULT_REASON)
        if not isinstance(model, str) or not model.strip():
            return self._auto(INVALID_REASON)
        target = model.strip()
        return Decision(target=target, policy=self.name, probs={target: 1.0},
                        reasons=(EXPLICIT_REASON,))

    def _auto(self, reason: str) -> Decision:
        return Decision(target="auto", policy=self.name, probs={"auto": 1.0},
                        reasons=(reason,))
