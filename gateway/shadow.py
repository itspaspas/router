"""Shadow comparison against Hooshyar's auto-judge.

auto-judge returns (as message content) the model its "auto" router would pick. The gateway calls it
in the background to compare decisions. It must never affect the user request, so this function never
raises: every failure is reported as ok=False.
"""
from __future__ import annotations

import asyncio
import time

from gateway.hooshyar import HooshyarClient

_RAW_MAX_CHARS = 200


async def shadow_auto_judge(
    client: HooshyarClient,
    messages: list[dict],
    known_models: set[str],
    timeout_s: float = 30.0,
) -> dict:
    """Ask auto-judge which model it would pick for `messages`.

    Returns {"raw": str | None, "parsed_model": str | None, "latency_ms": int, "ok": bool,
    "usage": dict | None}. raw is the first 200 characters of the reply content. parsed_model is
    the longest id in known_models that occurs in raw, or None. ok is True only when a string
    content was obtained. usage is the reply's usage object when it is a dict, else None.
    asyncio.CancelledError is not caught, so cancellation propagates.
    """
    body = {"model": "auto-judge", "stream": False, "messages": messages}
    start = time.monotonic()
    raw: str | None = None
    parsed: str | None = None
    usage: dict | None = None
    ok = False
    try:
        resp = await asyncio.wait_for(client.chat(body), timeout_s)
        content = resp["choices"][0]["message"]["content"]
        u = resp.get("usage")
        usage = u if isinstance(u, dict) else None
        if isinstance(content, str):
            raw = content[:_RAW_MAX_CHARS]
            ok = True
            matches = [m for m in known_models if m and m in raw]
            parsed = max(matches, key=len) if matches else None
    except Exception:
        raw = None
        parsed = None
        usage = None
        ok = False
    latency_ms = int((time.monotonic() - start) * 1000)
    return {"raw": raw, "parsed_model": parsed, "latency_ms": latency_ms, "ok": ok, "usage": usage}
