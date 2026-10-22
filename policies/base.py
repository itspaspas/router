"""Routing policy interface shared by every policy (B0 pass-through and later ones)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RouteRequest:
    body: dict
    app_id: str
    conversation_id: str | None
    language: str


@dataclass(frozen=True)
class Decision:
    # "auto", a tier name ("small" | "medium" | "frontier"), or a concrete Hooshyar model id.
    target: str
    policy: str
    probs: dict[str, float]
    reasons: tuple[str, ...] = ()
    effort: str | None = None


class RoutingPolicy(Protocol):
    name: str

    def decide(self, req: RouteRequest) -> Decision: ...
