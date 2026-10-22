"""Executes a routing Decision against Hooshyar with a tier fallback chain."""
from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator

from gateway.config import RouterConfig
from gateway.hooshyar import HooshyarClient, UpstreamError
from policies.base import Decision

TIERS = ("small", "medium", "frontier")


class TierNotConfigured(Exception):
    """No entry of the chain (the tier and its fallbacks) has a configured model: nothing was sent.

    Not an UpstreamError: it is a configuration/client problem, never retried or re-served.
    """

    def __init__(self, tier: str, attempts: list[str]):
        self.tier = tier
        self.attempts = attempts
        super().__init__(f"model tier {tier!r} is not configured")


@dataclass
class ExecResult:
    served_by: str  # upstream model id actually sent ("auto" or a Hooshyar id)
    attempts: list[str]  # targets tried, in order
    response: dict | None
    stream: AsyncIterator[bytes] | None


class _ReplayStream:
    """Re-yields an already-read first chunk, then the rest of the upstream stream.

    Closing it (aclose, or exhaustion/error) closes the underlying generator, even if
    iteration never started.
    """

    def __init__(self, first: bytes | None, rest: AsyncIterator[bytes]):
        self._first = first
        self._rest = rest

    def __aiter__(self) -> "_ReplayStream":
        return self

    async def __anext__(self) -> bytes:
        if self._first is not None:
            chunk, self._first = self._first, None
            return chunk
        try:
            return await self._rest.__anext__()
        except BaseException:
            await self.aclose()
            raise

    async def aclose(self) -> None:
        self._first = None
        await self._rest.aclose()


def _resolve(name: str, cfg: RouterConfig) -> str | None:
    """Upstream model id for a chain entry; None for an unconfigured tier."""
    if name in TIERS:
        return cfg.model_for(name)
    return name  # "auto" or a concrete model id, sent verbatim


async def _open_first(client: HooshyarClient, body: dict) -> tuple[bytes | None, AsyncIterator[bytes]]:
    gen = client.open_stream(body)
    try:
        try:
            first = await gen.__anext__()
        except StopAsyncIteration:
            first = None  # upstream 200 with zero bytes: a successful empty stream
    except BaseException:
        await gen.aclose()
        raise
    return first, gen


async def execute(
    decision: Decision, body: dict, client: HooshyarClient, cfg: RouterConfig, stream: bool
) -> ExecResult:
    chain = [decision.target] + cfg.fallback.get(decision.target, [])
    if decision.target not in TIERS and decision.target != "auto":
        chain = [decision.target]  # concrete model id: no fallback
    attempts: list[str] = []
    last_error: UpstreamError | None = None
    for name in chain:
        model = _resolve(name, cfg)
        if model is None:
            attempts.append(f"{name}:unconfigured")
            continue
        attempts.append(name)
        req = {**body, "model": model}
        try:
            if stream:
                first, gen = await _open_first(client, req)
                return ExecResult(model, attempts, None, _ReplayStream(first, gen))
            return ExecResult(model, attempts, await client.chat(req), None)
        except UpstreamError as e:
            if not e.retryable:
                e.attempts = attempts
                raise
            last_error = e
    if last_error is None:  # every chain entry was unconfigured: no request was possible
        raise TierNotConfigured(decision.target, attempts)
    last_error.attempts = attempts  # for the decision log: what was tried before giving up
    raise last_error
