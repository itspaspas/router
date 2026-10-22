"""B0: pass-through policy. Leaves routing to Hooshyar `auto` unless the client names a model."""
from __future__ import annotations

from policies.base import Decision, RouteRequest

DEFAULT_REASON = "default: hooshyar auto"
EXPLICIT_REASON = "explicit model requested"


class AutoPassthrough:
    name = "b0_auto"

    def decide(self, req: RouteRequest) -> Decision:
        # A missing (or empty) model means the client did not choose one. Any other
        # value, including "auto", is an explicit request and is honoured as given.
        model = req.body.get("model")
        if not model:
            return Decision(target="auto", policy=self.name, probs={"auto": 1.0},
                            reasons=(DEFAULT_REASON,))
        return Decision(target=model, policy=self.name, probs={model: 1.0},
                        reasons=(EXPLICIT_REASON,))
